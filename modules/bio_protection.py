from telegram.ext import MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import re

# Store user warnings
user_warnings = {}

def setup_bio_handlers(application):
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, check_bio))

async def check_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    
    # Check if user has bio
    if user.bio:
        # Check for links in bio
        links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', user.bio)
        
        if links:
            user_id = user.id
            if user_id not in user_warnings:
                user_warnings[user_id] = 0
            
            user_warnings[user_id] += 1
            
            if user_warnings[user_id] >= 3:
                # Auto-mute user
                await context.bot.restrict_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=user_id,
                    permissions={"can_send_messages": False}
                )
                await update.message.reply_text(
                    f"⚠️ User {user.mention_html()} has been muted for having unapproved links in bio after 3 warnings."
                )
            else:
                await update.message.reply_text(
                    f"⚠️ Warning {user_warnings[user_id]}/3: {user.mention_html()} has unapproved links in bio. "
                    "Please contact an admin for approval."
                )

async def approve_bio_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user.id == 7798461429:  # Bot owner check
        await update.message.reply_text("❌ Only the bot owner can approve bio links.")
        return
    
    try:
        user_id = int(context.args[0])
        if user_id in user_warnings:
            user_warnings[user_id] = 0
            await update.message.reply_text(f"✅ Bio link warnings for user {user_id} have been reset.")
        else:
            await update.message.reply_text("❌ No warnings found for this user.")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid user ID.")