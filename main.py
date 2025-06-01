import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from modules.bio_protection import setup_bio_handlers
from modules.message_control import setup_message_handlers
from modules.sticker_management import setup_sticker_handlers
from modules.copyright_protection import setup_copyright_handlers
from modules.commands import setup_command_handlers
from modules.welcome import setup_welcome_handlers
from modules.anti_spam import setup_anti_spam_handlers
from modules.user_management import setup_user_management_handlers
from modules.sticker_protection import setup_sticker_handlers

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', '0'))  # Default to 0 if not set

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Setup handlers from different modules
    setup_bio_handlers(application)
    setup_message_handlers(application)
    setup_sticker_handlers(application)
    setup_copyright_handlers(application)
    setup_command_handlers(application)
    setup_welcome_handlers(application)
    setup_anti_spam_handlers(application)
    setup_user_management_handlers(application)
    setup_sticker_handlers(application)
    
    # Start the bot
    await application.initialize()
    await application.start()
    await application.run_polling()
    await application.stop()
    await application.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")