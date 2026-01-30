#!/usr/bin/env python3

import os
import pathlib
import ssl
import sys
from dotenv import load_dotenv

# ⬅️ 1. Charger le .env AVANT TOUT
BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

# ⬇️ 2. logging
from logging_config import setup_logging
setup_logging(level=20)

# ⬇️ 3. imports applicatifs
import logging
from aiohttp import web

from routes import index, answer, webhook

app = web.Application()
app.add_routes(index.routes)
app.add_routes(answer.routes)
app.add_routes(webhook.routes)

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
LISTENER_PORT = int(os.getenv("LISTENER_PORT", 8000))
PROXY = os.getenv("PROXY", "false").lower() == "true"

TLS_CERT = os.getenv("TLS_CERTIFICATE")
TLS_KEY  = os.getenv("TLS_KEY")

ssl_context = None

if PROXY:
    logging.info("PROXY=true → démarrage en HTTP (TLS désactivé) 🐑")
else:
    # TLS obligatoire
    if not TLS_CERT or not TLS_KEY:
        logging.critical(
            "PROXY=false mais TLS_CERTIFICATE ou TLS_KEY manquant ❌🔥"
        )
        sys.exit(1)

    cert_path = pathlib.Path(TLS_CERT)
    key_path = pathlib.Path(TLS_KEY)

    if not cert_path.exists() or not key_path.exists():
        logging.critical(
            "Certificat ou clé TLS introuvable ❌🔐"
        )
        sys.exit(1)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    logging.info("PROXY=false → démarrage en HTTPS avec TLS ✔️🔐")

# ──────────────────────────────────────────────
# RUN
# ──────────────────────────────────────────────
scheme = "https" if ssl_context else "http"
logging.info(f"Server listening on {scheme}://0.0.0.0:{LISTENER_PORT}")

web.run_app(
    app,
    host="0.0.0.0",
    port=LISTENER_PORT,
    ssl_context=ssl_context
)
