import os
import logging
import aiohttp

GOTIFY_URL = os.getenv("GOTIFY_URL")
GOTIFY_TOKEN = os.getenv("GOTIFY_TOKEN")

GOTIFY_ENABLED = bool(GOTIFY_URL and GOTIFY_TOKEN)

if GOTIFY_ENABLED:
    logging.info(
        "Gotify enabled: url=%s token=%s****",
        GOTIFY_URL,
        GOTIFY_TOKEN[:4]
    )
else:
    logging.warning(
        "Gotify disabled: missing GOTIFY_URL or GOTIFY_TOKEN"
    )


async def send_gotify_message(title: str, message: str, priority: int = 5):
    if not GOTIFY_ENABLED:
        logging.info("Gotify disabled (missing env vars)")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{GOTIFY_URL}/message",
            params={"token": GOTIFY_TOKEN},
            data={
                "title": title,
                "message": message,
                "priority": priority,
            },
            ssl=False
        ) as resp:
            text = await resp.text()
            logging.info("Gotify response: %s - %s", resp.status, text)
