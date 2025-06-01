import os
import logging
import asyncio
import signal
from dotenv import load_dotenv
from telegram import Update
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

class Bot:
    def __init__(self):
        self.application = None
        self._running = False

    async def start(self):
        """Start the bot."""
        try:
            # Create the Application
            self.application = Application.builder().token(BOT_TOKEN).build()
            
            # Setup handlers from different modules
            setup_bio_handlers(self.application)
            setup_message_handlers(self.application)
            setup_sticker_handlers(self.application)
            setup_copyright_handlers(self.application)
            setup_command_handlers(self.application)
            setup_welcome_handlers(self.application)
            setup_anti_spam_handlers(self.application)
            setup_user_management_handlers(self.application)
            setup_sticker_handlers(self.application)
            
            # Start the bot
            await self.application.initialize()
            await self.application.start()
            self._running = True
            
            # Start polling
            await self.application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            await self.stop()

    async def stop(self):
        """Stop the bot gracefully."""
        if self._running and self.application:
            logger.info("Shutting down...")
            try:
                await self.application.stop()
                await self.application.shutdown()
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
            finally:
                self._running = False

def run_bot():
    """Run the bot with proper event loop handling."""
    bot = Bot()
    
    async def main():
        try:
            await bot.start()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error running bot: {e}")
        finally:
            await bot.stop()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == '__main__':
    run_bot()