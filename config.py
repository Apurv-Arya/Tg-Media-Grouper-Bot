import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Telegram Bot Configuration ---
# Get the bot token from the environment variable.
# The script will raise an error if the token is not found.
BOT_TOKEN = os.getenv('7080897951:AAEX_VM9sxtKSG0B7mSCWic7KOGsVT6PNGE')

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found. Please set it in your .env file.")