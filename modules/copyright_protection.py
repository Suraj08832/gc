from telegram.ext import MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from difflib import SequenceMatcher
from modules.database import db

def setup_copyright_handlers(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_copyright))

def calculate_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

async def check_copyright(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat = db.get_chat(chat_id)
    
    # Check if copyright protection is enabled
    if chat and not chat.get('copyright_protection', True):
        return
    
    message_text = update.message.text
    
    # Get recent messages for comparison
    async for message in context.bot.get_chat_history(chat_id, limit=10):
        if message.text and message.message_id != update.message.message_id:
            similarity = calculate_similarity(message_text, message.text)
            
            if similarity >= 0.85:  # 85% similarity threshold
                # Delete the message
                await update.message.delete()
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ Copyright violation detected!\nSimilarity: {similarity:.2%}\nMessage deleted."
                )
                return

async def toggle_copyright(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id
    )
    
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("❌ Only admins can toggle copyright protection.")
        return
    
    chat_id = update.effective_chat.id
    chat = db.get_chat(chat_id)
    
    # Toggle copyright protection
    new_status = not chat.get('copyright_protection', True)
    db.update_chat_settings(chat_id, {'copyright_protection': new_status})
    
    status = "enabled" if new_status else "disabled"
    await update.message.reply_text(f"✅ Copyright protection has been {status} for this chat.")