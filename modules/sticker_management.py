from telegram.ext import MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# Store approved users for stickers
approved_sticker_users = set()

def setup_sticker_handlers(application):
    application.add_handler(MessageHandler(filters.STICKER, handle_sticker))

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check if user is approved
    if user_id not in approved_sticker_users:
        # Delete the sticker
        await update.message.delete()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ {update.effective_user.mention_html()}, you need approval to send stickers in this group."
        )

async def approve_sticker_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is group owner
    chat_member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id
    )
    
    if chat_member.status != 'creator':
        await update.message.reply_text("❌ Only group owners can approve sticker users.")
        return
    
    try:
        user_id = int(context.args[0])
        approved_sticker_users.add(user_id)
        await update.message.reply_text(f"✅ User {user_id} has been approved to send stickers.")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid user ID.")