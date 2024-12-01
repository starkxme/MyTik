import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler
from telegram.ext import filters
from TikTokApi import TikTokApi
import requests

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download TikTok video
def download_tiktok_video(url: str):
    try:
        api = TikTokApi.get_instance()
        video = api.video(url=url)
        video_bytes = video.bytes()  # Get video as bytes
        return video_bytes
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None

# Command handler for start
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a TikTok video URL to download the video.")

# Handler for message with TikTok URL
async def handle_message(update: Update, context):
    url = update.message.text.strip()
    if 'tiktok.com' in url:
        video_bytes = download_tiktok_video(url)
        if video_bytes:
            await update.message.reply_video(video=video_bytes)
        else:
            await update.message.reply_text("Sorry, I couldn't download the video. Try again later.")
    else:
        await update.message.reply_text("Please send a valid TikTok URL.")

# Error handler
def error(update: Update, context):
    logger.warning(f'Update {update} caused error {context.error}')

# Main function
async def main():
    # Replace with your bot's token from BotFather
    token = '8155781106:AAEBzXLXHn0kB_mhvVmBYg1z_BYtT3G3lRI'
    
    # Set up the Application and Dispatcher
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Log all errors
    application.add_error_handler(error)
    
    # Start polling for updates
    await application.run_polling()

# Check if the script is being run directly
if __name__ == '__main__':
    import sys
    if sys.version_info >= (3, 7):
        # If in a normal script, run the event loop
        import asyncio
        asyncio.run(main())
    else:
        # For versions below Python 3.7 (rare), run the event loop manually
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
