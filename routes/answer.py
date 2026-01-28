import json
import logging
import time
from aiohttp import web

from helpers.network import extract_mac
from helpers.template import find_template, build_context, render_template
from services.gotify import send_gotify_message

logger = logging.getLogger("route.answer")
routes = web.RouteTableDef()

@routes.post("/answer")
async def answer(request):
    start = time.time()

    logger.info("POST /answer from %s", request.remote)

    payload = await request.json()
    logger.debug("Payload: %s", json.dumps(payload))

    mac = extract_mac(payload)
    logger.info("Detected MAC: %s", mac)

    template_name = find_template(mac)
    logger.info("Template selected: %s", template_name)

    await send_gotify_message(
        title="Installation Proxmox",
        message=f"Installation démarrée pour {mac}",
        priority=6,
    )

    context = build_context(payload, mac)
    rendered = render_template(template_name, context)

    duration = round(time.time() - start, 3)
    logger.info(
        "Answer completed for %s in %ss",
        mac,
        duration
    )

    return web.Response(text=rendered)
