import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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
def start(update: Update, context):
    update.message.reply_text("Welcome! Send me a TikTok video URL to download the video.")

# Handler for message with TikTok URL
def handle_message(update: Update, context):
    url = update.message.text.strip()
    if 'tiktok.com' in url:
        video_bytes = download_tiktok_video(url)
        if video_bytes:
            update.message.reply_video(video=video_bytes)
        else:
            update.message.reply_text("Sorry, I couldn't download the video. Try again later.")
    else:
        update.message.reply_text("Please send a valid TikTok URL.")

# Error handler
def error(update: Update, context):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    # Replace with your bot's token from BotFather
    token = '8155781106:AAEBzXLXHn0kB_mhvVmBYg1z_BYtT3G3lRI'
    
    # Set up the Updater and Dispatcher
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Log all errors
    dispatcher.add_error_handler(error)
    
    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
