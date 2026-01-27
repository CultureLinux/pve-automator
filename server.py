#!/usr/bin/env python3

import json
import logging
import pathlib
import datetime
import aiohttp

from aiohttp import web
import tomlkit
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# =====================
# PATHS
# =====================

BASE_DIR = pathlib.Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
DEFAULT_TEMPLATE = "default.toml.j2"


GOTIFY_URL = "https://gotify.clinux.fr"
GOTIFY_TOKEN = "ACY6E8ZzlYA7VXi"



# =====================
# LOGGING
# =====================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# =====================
# JINJA
# =====================

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=False,
)

# =====================
# AIOHTTP
# =====================

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.json_response(
        {
            "status": "ok",
            "service": "pve-automator",
            "time": datetime.datetime.utcnow().isoformat() + "Z",
        }
    )

@routes.post("/answer")
async def answer(request):
    try:
        payload = await request.json()
    except Exception as e:
        return web.Response(status=400, text=f"Invalid JSON: {e}")

    logging.info(
        "Request from %s:\n%s",
        request.remote,
        json.dumps(payload, indent=2),
    )

    mac = extract_mac(payload)

    # 🔔 Gotify : début d'installation
    await send_gotify_message(
        title="Installation Proxmox",
        message=f"Installation démarrée pour la machine {mac}",
        priority=6,
    )

    template_name = find_template(mac)
    context = build_context(payload, mac)

    try:
        rendered = render_template(template_name, context)
        logging.info("Using template: %s", template_name)
        return web.Response(text=rendered)
    except Exception as e:
        logging.exception("Template rendering failed")
        return web.Response(status=500, text=str(e))


@routes.post("/webhook")
async def webhook(request: web.Request):
    try:
        payload = await request.json()
    except Exception as e:
        logging.exception("Webhook: impossible de parser le JSON")
        return web.json_response({"status": "error", "reason": str(e)}, status=400)

    logging.info("Webhook reçu de %s", request.remote)
    logging.info(json.dumps(payload, indent=2))

    hostname = payload.get("dmi", {}).get("system", {}).get("name", "PVE inconnu")
    uuid = payload.get("dmi", {}).get("system", {}).get("uuid", "N/A")

    await send_gotify_message(
        title="PVE installé",
        message=f"{hostname} prêt (UUID: {uuid})",
        priority=7
    )

    return web.json_response({"status": "ok", "received": True})


# =====================
# HELPERS
# =====================

def extract_mac(payload):
    for nic in payload.get("network_interfaces", []):
        mac = nic.get("mac")
        if mac:
            return mac.lower()
    return None

def find_template(mac):
    if mac:
        candidate = f"mac/{mac}.toml.j2"
        try:
            env.get_template(candidate)
            return candidate
        except TemplateNotFound:
            pass
    return DEFAULT_TEMPLATE

def build_context(payload, mac):
    return {
        "mac": mac or "unknown",
        "hostname": f"pve-{mac.replace(':','')[:6]}" if mac else "pve-node",
        "timezone": "Europe/Paris",
        "keyboard": "fr",
        "country": "FR",
    }

def render_template(template_name, context):
    template = env.get_template(template_name)
    rendered = template.render(context)

    # Validation TOML
    tomlkit.parse(rendered)
    return rendered

async def send_gotify_message(title: str, message: str, priority: int = 5):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{GOTIFY_URL}/message",
            params={"token": GOTIFY_TOKEN},
            data={
                "title": title,
                "message": message,
                "priority": priority,
            },
            ssl=False  # ⚠️ mets True si ton cert est valide
        ) as resp:
            text = await resp.text()
            logging.info("Gotify response: %s - %s", resp.status, text)


# =====================
# MAIN
# =====================

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)

    logging.info("Server listening on 0.0.0.0:8000")
    web.run_app(app, host="0.0.0.0", port=8000)
