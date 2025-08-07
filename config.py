from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN", "7080897951:AAEX_VM9sxtKSG0B7mSCWic7KOGsVT6PNGE")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found. Please set it in your .env file.")