import logging
import datetime
from aiohttp import web

logger = logging.getLogger("route.index")
routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    logger.info(
        "GET / from %s",
        request.remote
    )

    return web.json_response(
        {
            "status": "ok",
            "service": "pve-automator",
            "time": datetime.datetime.utcnow().isoformat() + "Z",
        }
    )
