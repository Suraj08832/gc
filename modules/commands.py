from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import os
from modules.bio_protection import approve_bio_link, user_warnings
from modules.message_control import delete_message
from modules.copyright_protection import toggle_copyright
from modules.sticker_management import approve_sticker_user
from modules.user_management import warn_user, mute_user, unmute_user, ban_user, unban_user

# Get owner ID from environment variable
OWNER_ID = int(os.getenv('OWNER_ID', '0'))

def setup_command_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("approve", approve_bio_link))
    application.add_handler(CommandHandler("reset_warnings", reset_warnings))
    application.add_handler(CommandHandler("delete", delete_message))
    application.add_handler(CommandHandler("copyright", toggle_copyright))
    application.add_handler(CommandHandler("approve_sticker", approve_sticker_user))
    application.add_handler(CommandHandler("warn", warn_user))
    application.add_handler(CommandHandler("mute", mute_user))
    application.add_handler(CommandHandler("unmute", unmute_user))
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("unban", unban_user))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! I'm your group management bot.\n"
        "Use /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤖 Available Commands:

Admin Commands:
• /approve [user_id] - Approve bio links
• /reset_warnings [user_id] - Reset user warnings
• /delete [message_id] [reason] - Delete messages
• /copyright - Toggle copyright protection
• /warn [user_id] [reason] - Warn a user
• /mute [user_id] [duration] [reason] - Mute a user
• /unmute [user_id] - Unmute a user
• /ban [user_id] [reason] - Ban a user
• /unban [user_id] - Unban a user

Group Owner Commands:
• /approve_sticker [user_id] - Approve users for stickers

User Commands:
• /start - Start the bot
• /help - Show this help message
• /info - Show bot information
"""
    await update.message.reply_text(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = """
🤖 Bot Information

Core Features:
• Bio Link Protection:
  - Monitors user bios for links
  - Warns users with unapproved links
  - Auto-mutes after 3 warnings
  - Admin approval system for links

• Message Control:
  - Deletes edited messages
  - Message deletion with reasons
  - Admin-only message deletion

• Sticker Management:
  - Group owner approval required
  - Admins need approval too
  - Auto-deletes unapproved stickers

• Copyright Protection:
  - 85% similarity detection
  - Auto-deletes copied content
  - Shows similarity percentage
  - Can be toggled by admins
"""
    await update.message.reply_text(info_text)

async def reset_warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user.id == OWNER_ID:  # Bot owner check
        await update.message.reply_text("❌ Only the bot owner can reset warnings.")
        return
    
    try:
        user_id = int(context.args[0])
        if user_id in user_warnings:
            user_warnings[user_id] = 0
            await update.message.reply_text(f"✅ Warnings for user {user_id} have been reset.")
        else:
            await update.message.reply_text("❌ No warnings found for this user.")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid user ID.")