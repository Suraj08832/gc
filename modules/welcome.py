from telegram.ext import MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from modules.database import db

def setup_welcome_handlers(application):
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat = db.get_chat(chat_id)
    
    # Check if welcome messages are enabled
    if chat and not chat.get('welcome_enabled', True):
        return
    
    new_members = update.message.new_chat_members
    
    for member in new_members:
        if not member.is_bot:
            # Add user to database
            db.add_user(
                user_id=member.id,
                username=member.username,
                first_name=member.first_name
            )
            
            welcome_text = f"""
👋 Welcome {member.mention_html()} to the group!

📜 Group Rules:
1. No spam or advertising
2. No offensive content
3. Respect all members
4. No unauthorized links
5. No sticker spam

Use /help to see available commands.
"""
            await update.message.reply_text(welcome_text, parse_mode='HTML')