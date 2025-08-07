import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Telegram Bot Configuration ---
# Get the bot token from the environment variable.
# The script will raise an error if the token is not found.
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found. Please set it in your .env file.")