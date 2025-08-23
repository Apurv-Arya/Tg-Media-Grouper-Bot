from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found. Please set it in your .env file.")
