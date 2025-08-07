import asyncio
from telegram import Update, InputMediaPhoto, InputMediaVideo, InputMediaAnimation
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import the token from your config file
from config import BOT_TOKEN

# This dictionary will store user media and their associated timers.
# The key is the user's ID.
user_media_sessions = {}

# --- Bot Logic ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "Hi! I can now group photos, videos, and GIFs into albums.\n\n"
        "Simply send or forward me your files. I'll wait a moment after "
        "your last file to group them all automatically for you."
    )

async def process_and_send_albums(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Processes the user's queue and sends all media in albums of 10."""
    if user_id in user_media_sessions:
        media_queue = user_media_sessions[user_id]['media']
        
        # Keep sending albums as long as there are files in the queue
        while media_queue:
            # Take the first 10 items (or fewer if less than 10 remain)
            album_to_send = media_queue[:10]
            # Remove those items from the front of the queue
            user_media_sessions[user_id]['media'] = media_queue[10:]
            
            # Send the album
            if album_to_send:
                await context.bot.send_media_group(chat_id=chat_id, media=album_to_send)
                # A small delay to ensure messages are sent in order
                await asyncio.sleep(1)
            
            # Update the local reference to the queue
            media_queue = user_media_sessions[user_id]['media']
            
        # Clean up the session once everything is sent
        del user_media_sessions[user_id]


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming media, adding it to a queue and managing a timer."""
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    
    # Initialize the session for the user if it doesn't exist
    if user_id not in user_media_sessions:
        user_media_sessions[user_id] = {'media': [], 'timer': None}
    
    # If a timer is already running, cancel it to reset the countdown
    if user_media_sessions[user_id]['timer']:
        user_media_sessions[user_id]['timer'].cancel()
        
    # Determine the media type and add it to the queue
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        user_media_sessions[user_id]['media'].append(InputMediaPhoto(media=file_id))
    elif update.message.video:
        file_id = update.message.video.file_id
        user_media_sessions[user_id]['media'].append(InputMediaVideo(media=file_id))
    elif update.message.animation: # <-- This is the new part for GIFs
        file_id = update.message.animation.file_id
        user_media_sessions[user_id]['media'].append(InputMediaAnimation(media=file_id))
        
    # Set a new timer. The bot will wait 2.5 seconds after the last file is received.
    user_media_sessions[user_id]['timer'] = context.job_queue.run_once(
        lambda ctx: process_and_send_albums(chat_id, user_id, context), 
        2.5
    )

def main() -> None:
    """Starts the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for commands
    application.add_handler(CommandHandler("start", start))

    # Add a handler for photos, videos, AND animations (GIFs)
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.ANIMATION, handle_media))

    # Run the bot until the user presses Ctrl-C
    print("Bot is running... Press Ctrl-C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()
