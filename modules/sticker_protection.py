from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from modules.database import db
from modules.messages import messages

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.sticker:
        return
    
    chat_id = update.effective_chat.id
    sticker_id = update.message.sticker.file_id
    user_id = update.effective_user.id
    
    # Get chat settings
    chat_settings = db.get_chat_settings(chat_id)
    if not chat_settings or not chat_settings.get('sticker_protection', True):
        return
    
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ['creator', 'administrator']:
        return
    
    # Check if sticker is approved
    if db.is_sticker_approved(chat_id, sticker_id):
        return
    
    # Delete the sticker
    await update.message.delete()
    
    # Send approval request to admins
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_sticker_{sticker_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_sticker_{sticker_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"⚠️ New sticker from {update.effective_user.mention_html()} needs approval.",
        reply_markup=reply_markup
    )

async def handle_sticker_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not query.data:
        return
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status not in ['creator', 'administrator']:
        await query.answer("Only admins can approve/reject stickers!", show_alert=True)
        return
    
    action, sticker_id = query.data.split('_', 1)
    
    if action == "approve":
        db.add_sticker_approval(chat_id, sticker_id, user_id)
        await query.edit_message_text("✅ Sticker has been approved!")
    elif action == "reject":
        db.remove_sticker_approval(chat_id, sticker_id)
        await query.edit_message_text("❌ Sticker has been rejected!")

def setup_sticker_handlers(application):
    application.add_handler(MessageHandler(filters.STICKER, handle_sticker))
    application.add_handler(CallbackQueryHandler(handle_sticker_callback, pattern=r"^(approve|reject)_sticker_")) 