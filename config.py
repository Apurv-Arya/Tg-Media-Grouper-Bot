from os import getenv

# --- Telegram Bot Configuration ---
# Get the bot token from the environment variable.
# The script will raise an error if the token is not found.
BOT_TOKEN = getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found. Please set it in your .env file.")