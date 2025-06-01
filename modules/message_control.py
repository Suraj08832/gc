from telegram.ext import MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

def setup_message_handlers(application):
    application.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, handle_edited_message))

async def handle_edited_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Delete edited messages
    await update.message.delete()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"⚠️ Message editing is not allowed in this group."
    )

async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id
    )
    
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("❌ Only admins can delete messages.")
        return
    
    try:
        # Get message ID and reason
        message_id = int(context.args[0])
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
        
        # Delete the message
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=message_id
        )
        
        await update.message.reply_text(
            f"✅ Message deleted.\nReason: {reason}"
        )
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid message ID and reason.")