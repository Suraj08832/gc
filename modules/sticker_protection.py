from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from modules.database import db
from modules.messages import messages
import logging

logger = logging.getLogger(__name__)

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle sticker messages and check if they need approval"""
    if not update.message or not update.message.sticker:
        return

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    sticker_id = update.message.sticker.file_id

    try:
        # Get chat settings
        chat_settings = db.get_chat_settings(chat_id)
        if not chat_settings or not chat_settings.get('sticker_protection', False):
            return

        # Check if user is owner
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        if chat_member.status == 'creator':
            return

        # Check if sticker is approved
        if not db.is_sticker_approved(chat_id, sticker_id):
            # Delete the sticker first
            try:
                await update.message.delete()
                logger.info(f"Deleted unapproved sticker from user {user_id} in chat {chat_id}")
            except Exception as e:
                logger.error(f"Failed to delete sticker: {e}")
                return
            
            # Send approval request to owner
            keyboard = [
                [
                    InlineKeyboardButton("✅ Approve", callback_data=f"approve_sticker_{sticker_id}"),
                    InlineKeyboardButton("❌ Reject", callback_data=f"reject_sticker_{sticker_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🇺🇸 English\n\nSticker from {update.message.from_user.mention_html()} needs owner approval.",
                    reply_markup=reply_markup
                )
                logger.info(f"Sent sticker approval request for sticker {sticker_id} in chat {chat_id}")
            except Exception as e:
                logger.error(f"Failed to send approval request: {e}")
    except Exception as e:
        logger.error(f"Error in handle_sticker: {e}")

async def handle_sticker_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle sticker approval/rejection callbacks"""
    query = update.callback_query
    if not query:
        return

    chat_id = query.message.chat_id
    user_id = query.from_user.id

    try:
        # Check if user is owner
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        if chat_member.status != 'creator':
            await query.answer("Only group owner can approve/reject stickers!", show_alert=True)
            return

        action, sticker_id = query.data.split('_', 1)
        
        if action == "approve":
            if db.approve_sticker(chat_id, sticker_id):
                await query.edit_message_text("✅ Sticker approved by owner!")
                logger.info(f"Sticker {sticker_id} approved by owner {user_id} in chat {chat_id}")
            else:
                await query.edit_message_text("❌ Failed to approve sticker!")
                logger.error(f"Failed to approve sticker {sticker_id} in chat {chat_id}")
        else:
            await query.edit_message_text("❌ Sticker rejected by owner!")
            logger.info(f"Sticker {sticker_id} rejected by owner {user_id} in chat {chat_id}")
    except Exception as e:
        logger.error(f"Error in handle_sticker_callback: {e}")
        await query.answer("An error occurred while processing your request.", show_alert=True)

def setup_sticker_handlers(application: Application):
    """Set up sticker-related handlers"""
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    application.add_handler(CallbackQueryHandler(handle_sticker_callback, pattern=r"^(approve|reject)_sticker_")) 