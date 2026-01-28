#!/usr/bin/env python3

import pathlib
from dotenv import load_dotenv

# ⬅️ 1. Charger le .env AVANT TOUT
BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

# ⬇️ 2. on charge le logging
from logging_config import setup_logging
setup_logging(level=20)  # INFO

# ⬇️ 3. ENSUITE seulement, on importe le reste
import logging
from aiohttp import web

from routes import index, answer, webhook

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = web.Application()
app.add_routes(index.routes)
app.add_routes(answer.routes)
app.add_routes(webhook.routes)

logging.info("Server listening on 0.0.0.0:8000")
web.run_app(app, host="0.0.0.0", port=8000)
