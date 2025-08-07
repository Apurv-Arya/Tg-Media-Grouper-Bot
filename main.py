import asyncio
from telegram import Bot, Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token you get from BotFather
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# This dictionary will store user media. The key is the user's ID.
# The value is another dictionary containing a list of media and a timer.
user_media_queues = {}

# --- Bot Logic ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "Hi! I can help you group photos.\n\n"
        "Just send me some photos one after another, and I'll group them into an album for you. "
        "I'll wait for a moment after you send the last photo before grouping them."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming photos, adding them to a user-specific queue."""
    user_id = update.message.from_user.id
    photo_file_id = update.message.photo[-1].file_id # Get the highest resolution photo

    # If the user is not in our queue, add them.
    if user_id not in user_media_queues:
        user_media_queues[user_id] = {'media': [], 'timer': None}

    # Cancel the previous timer if it exists
    if user_media_queues[user_id]['timer']:
        user_media_queues[user_id]['timer'].cancel()

    # Add the new photo to the user's media list
    user_media_queues[user_id]['media'].append(InputMediaPhoto(media=photo_file_id))

    # Set a new timer to send the media group after a short delay (e.g., 2 seconds)
    # This delay allows the user to send multiple photos.
    user_media_queues[user_id]['timer'] = asyncio.create_task(
        send_media_group_after_delay(update, context, user_id)
    )

async def send_media_group_after_delay(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """Waits for a delay, then sends the collected media as a group."""
    await asyncio.sleep(2)  # Wait for 2 seconds

    media_to_send = user_media_queues[user_id]['media']

    if len(media_to_send) > 1:
        # If there's more than one photo, send them as a media group
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_to_send)
    elif len(media_to_send) == 1:
        # If there's only one photo, just send it back normally
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=media_to_send[0].media)

    # Clear the user's queue after sending
    del user_media_queues[user_id]

def main() -> None:
    """Starts the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - handle the photo message
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Run the bot until the user presses Ctrl-C
    print("Bot is running... Press Ctrl-C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()
