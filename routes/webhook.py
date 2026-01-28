import json
import logging
from aiohttp import web

from services.gotify import send_gotify_message

logger = logging.getLogger("route.webhook")
routes = web.RouteTableDef()

@routes.post("/webhook")
async def webhook(request):
    logger.info("POST /webhook from %s", request.remote)

    payload = await request.json()
    logger.debug("Webhook payload: %s", json.dumps(payload))

    system = payload.get("dmi", {}).get("system", {})
    hostname = system.get("name", "unknown")
    uuid = system.get("uuid", "N/A")

    logger.info(
        "PVE ready: hostname=%s uuid=%s",
        hostname,
        uuid
    )

    await send_gotify_message(
        title="PVE installé",
        message=f"{hostname} prêt (UUID: {uuid})",
        priority=7
    )

    return web.json_response({"status": "ok"})
