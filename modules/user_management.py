from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from modules.database import db

def setup_user_management_handlers(application):
    application.add_handler(CommandHandler("warn", warn_user))
    application.add_handler(CommandHandler("mute", mute_user))
    application.add_handler(CommandHandler("unmute", unmute_user))
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("unban", unban_user))

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id
    )
    
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("❌ Only admins can warn users.")
        return
    
    try:
        user_id = int(context.args[0])
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
        
        # Add warning to database
        warning_count = db.add_warning(user_id, update.effective_chat.id, reason)
        
        await update.message.reply_text(
            f"⚠️ User {user_id} has been warned ({warning_count}/3).\nReason: {reason}"
        )
        
        if warning_count >= 3:
            # Auto-ban after 3 warnings
            await ban_user(update, context)
            
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid user ID and reason.")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id
    )
    
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("❌ Only admins can mute users.")
        return
    
    try:
        user_id = int(context.args[0])
        duration = int(context.args[1]) if len(context.args) > 1 else 24  # Default 24 hours
        reason = ' '.join(context.args[2:]) if len(context.args) > 2 else "No reason provided"
        
        # Mute user
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions={"can_send_messages": False},
            until_date=datetime.now() + timedelta(hours=duration)
        )
        
        # Add mute to database
        db.add_mute(user_id, update.effective_chat.id, duration, reason)
        
        await update.message.reply_text(
            f"🔇 User {user_id} has been muted for {duration} hours.\nReason: {reason}"
        )
        
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid user ID, duration (hours), and reason.")

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id
    )
    
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("❌ Only admins can unmute users.")
        return
    
    try:
        user_id = int(context.args[0])
        
        # Unmute user
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions={"can_send_messages": True}
        )
        
        # Remove mute from database
        db.remove_mute(user_id, update.effective_chat.id)
        
        await update.message.reply_text(f"🔊 User {user_id} has been unmuted.")
        
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid user ID.")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id
    )
    
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("❌ Only admins can ban users.")
        return
    
    try:
        user_id = int(context.args[0])
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
        
        # Ban user
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id
        )
        
        # Update user status in database
        db.add_user(user_id, is_banned=True)
        
        await update.message.reply_text(
            f"🚫 User {user_id} has been banned.\nReason: {reason}"
        )
        
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid user ID and reason.")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is admin
    chat_member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id
    )
    
    if chat_member.status not in ['creator', 'administrator']:
        await update.message.reply_text("❌ Only admins can unban users.")
        return
    
    try:
        user_id = int(context.args[0])
        
        # Unban user
        await context.bot.unban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id
        )
        
        # Update user status in database
        db.add_user(user_id, is_banned=False)
        
        await update.message.reply_text(f"✅ User {user_id} has been unbanned.")
        
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Please provide a valid user ID.")