#!/usr/bin/env python3

import json
import logging
import pathlib
import datetime

from aiohttp import web
import tomlkit
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# =====================
# PATHS
# =====================

BASE_DIR = pathlib.Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
DEFAULT_TEMPLATE = "default.toml.j2"

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

    logging.info("Request from %s:\n%s",
        request.remote,
        json.dumps(payload, indent=2),
    )

    mac = extract_mac(payload)
    template_name = find_template(mac)
    context = build_context(payload, mac)

    try:
        rendered = render_template(template_name, context)
        logging.info("Using template: %s", template_name)
        return web.Response(text=rendered)
    except Exception as e:
        logging.exception("Template rendering failed")
        return web.Response(status=500, text=str(e))

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

# =====================
# MAIN
# =====================

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)

    logging.info("Server listening on 0.0.0.0:8000")
    web.run_app(app, host="0.0.0.0", port=8000)
