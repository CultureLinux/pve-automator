import json
import logging
from aiohttp import web

from services.gotify import send_gotify_message

logger = logging.getLogger("route.webhook")
routes = web.RouteTableDef()

@routes.post("/webhook")
async def webhook(request):
    real_ip = (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.headers.get("X-Real-IP")
        or request.remote
    )

    logger.info("POST /webhook from %s", real_ip)

    payload = await request.json()
    logger.debug("Webhook payload: %s", json.dumps(payload))

    system = payload.get("dmi", {}).get("system", {})
    hostname = system.get("name", "unknown")
    uuid = system.get("uuid", "N/A")

    fqdn = payload.get("fqdn", "unknown")
    reboot_mode = payload.get("reboot-mode", "unknown")

    product = payload.get("product", {})
    pve_version = product.get("version", "unknown")

    iso = payload.get("iso", {})
    iso_release = iso.get("release", "unknown")

    mgmt_ip = "unknown"
    mgmt_mac = "unknown"

    for iface in payload.get("network-interfaces", []):
        if iface.get("is-management"):
            mgmt_ip = iface.get("address", "unknown")
            mgmt_mac = iface.get("mac", "unknown")
            break

    logger.info(
        "PVE ready: hostname=%s fqdn=%s uuid=%s mgmt_ip=%s",
        hostname, fqdn, uuid, mgmt_ip
    )

    await send_gotify_message(
        title="🖥️ Proxmox VE installé",
        message=(
            f"✅ Hôte prêt\n"
            f"🖥️ Hostname : {hostname}\n"
            f"🌐 FQDN : {fqdn}\n"
            f"🆔 UUID : {uuid}\n"
            f"📡 IP mgmt : {mgmt_ip}\n"
            f"🔌 MAC mgmt : {mgmt_mac}\n"
            f"📦 PVE : {pve_version} (ISO {iso_release})\n"
            f"🔄 Reboot mode : {reboot_mode}"
        ),
        priority=7
    )

    return web.json_response({"status": "ok"})
