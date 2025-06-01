from telegram.ext import MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from collections import defaultdict
import time

# Store user message counts and timestamps
user_messages = defaultdict(list)
SPAM_THRESHOLD = 5  # messages
SPAM_WINDOW = 60  # seconds

def setup_anti_spam_handlers(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam))

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_time = time.time()
    
    # Clean old messages
    user_messages[user_id] = [t for t in user_messages[user_id] if current_time - t < SPAM_WINDOW]
    
    # Add new message timestamp
    user_messages[user_id].append(current_time)
    
    # Check for spam
    if len(user_messages[user_id]) >= SPAM_THRESHOLD:
        # Delete the message
        await update.message.delete()
        
        # Warn the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ {update.effective_user.mention_html()}, please don't spam! "
                 f"Wait {SPAM_WINDOW} seconds between messages.",
            parse_mode='HTML'
        )
        
        # Clear user's message history
        user_messages[user_id] = []