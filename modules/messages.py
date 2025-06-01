from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from modules.database import db

class Messages:
    # Button Text
    CLOSE_BUTTON = "๏ ᴄʟᴏsᴇ ๏"
    BACK_BUTTON = "๏ ʙᴀᴄᴋ ๏"

    # General Messages
    GENERAL_1 = "» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ."
    GENERAL_2 = "» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ.\n\nᴇxᴄᴇᴘᴛɪᴏɴ : <code>{0}</code>"
    GENERAL_3 = "ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ᴄʜᴀᴛ, ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғᴏʀ ᴜsɪɴɢ ᴍᴇ."
    GENERAL_4 = "» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs.\n\nʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ ᴠɪᴀ /reload"
    GENERAL_5 = "» ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ."

    # Start Messages
    START_1 = "{0} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ.\n\n<b>✫ ᴜᴘᴛɪᴍᴇ :</b> {1}"
    START_2 = """ʜᴇʏ, {0} \nɪ'ᴍ {1},\n\n┏━━━━━━━━━━━━━━━━━⧫
┠ ◆ ɪ ʜᴀᴠᴇ sᴘᴇᴄɪᴀʟ ғᴇᴀᴛᴜʀᴇs.
┠ ◆ ᴀʟʟ-ɪɴ-ᴏɴᴇ ʙᴏᴛ.
┗━━━━━━━━━━━━━━━━━⧫
┏━━━━━━━━━━━━━━━━━⧫
┠ ◆ ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ꜱᴏɴɢꜱ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.
┠ ◆ ʏᴏᴜ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ɪᴍᴀɢᴇs.
┠ ◆ ʏᴏᴜ ᴄᴀɴ ᴛʀᴀɴꜱʟᴀᴛᴇ ᴍᴜʟᴛɪᴘʟᴇ ʟᴀɴɢᴜᴀɢᴇꜱ.
┠ ◆ ɪ ᴄᴀɴ ᴍᴜᴛᴇ,ᴜɴᴍᴜᴛᴇ,ʙᴀɴ,ᴜɴʙᴀɴ,ᴋɪᴄᴋ..
┠ ◆ ꜱᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ 
┠ ◆ ᴍᴏʀᴇ ғᴇᴀᴛᴜʀᴇs ᴄʟɪᴄᴋ ᴄᴏᴍᴍᴀɴᴅs ʙᴜᴛᴛᴏɴ...
┗━━━━━━━━━━━━━━━━━⧫
๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs.\n\n🫧 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🪽 ➪ [🥀ʙʏ »  ⃪ͥ͢ ᷟ●𝁂꯭𝗭𝗲‌𝗳𝗿𝗼‌𝗻 ‌⃪ ✔︎](https://t.me/crush_hu_tera)"""
    START_3 = "ʜᴇʏ {0},\nᴛʜɪs ɪs {1}\n\nᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {2}, {3} ᴄᴀɴ ɴᴏᴡ ᴩʟᴀʏ sᴏɴɢs ɪɴ ᴛʜɪs ᴄʜᴀᴛ."
    START_4 = """🎄 <b>sᴜᴘᴇʀɢʀᴏᴜᴘ ɴᴇᴇᴅᴇᴅ</b> 🎄\n\nᴘʟᴇᴀsᴇ ᴄᴏɴᴠᴇʀᴛ ʏᴏᴜʀ <b>ɢʀᴏᴜᴘ</b> ᴛᴏ <b>sᴜᴘᴇʀɢʀᴏᴜᴘ</b> ᴀɴᴅ ᴛʜᴇɴ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ.\n\n<b>ʜᴏᴡ ᴛᴏ ᴍᴀᴋᴇ sᴜᴘᴇʀɢʀᴏᴜᴘ ?</b>\n- ᴍᴀᴋᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ's ᴄʜᴀᴛ ʜɪsᴛᴏʀʏ <b>ᴠɪsɪʙʟᴇ</b> ᴏɴᴄᴇ."""
    START_5 = "<b>↝ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ ↜</b>\n\nᴛʜɪs ᴄʜᴀᴛ ɪs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴏɴ {0} ᴅᴀᴛᴀʙᴀsᴇ.\nʀᴇǫᴜᴇsᴛ ᴀ <a href={1}>sᴜᴅᴏ ᴜsᴇʀ</a> ᴛᴏ ᴜɴʙʟᴀᴄᴋʟɪsᴛ ʏᴏᴜʀ ᴄʜᴀᴛ ᴏʀ ᴠɪsɪᴛ <a href={2}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ.</a>"

    # Help Messages
    HELP_1 = "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ <a href={0}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a>\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : <code>/</code>"
    HELP_2 = "ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴍʏ ʜᴇʟᴘ ᴍᴇɴᴜ ɪɴ ʏᴏᴜʀ ᴘᴍ."

    # Admin Messages
    ADMIN_1 = "» ᴅɪᴅ ʏᴏᴜ ʀᴇᴍᴇᴍʙᴇʀ ᴛʜᴀᴛ ʏᴏᴜ'ᴠᴇ ʀᴇsᴜᴍᴇᴅ ᴛʜᴇ sᴛʀᴇᴀᴍ ?"
    ADMIN_2 = "➻ sᴛʀᴇᴀᴍ ᴘᴀᴜsᴇᴅ 🎄\n│ \n└ʙʏ : {0} 🥀"
    ADMIN_3 = "» ᴅɪᴅ ʏᴏᴜ ʀᴇᴍᴇᴍʙᴇʀ ᴛʜᴀᴛ ʏᴏᴜ'ᴠᴇ ᴘᴀᴜsᴇᴅ ᴛʜᴇ sᴛʀᴇᴀᴍ ?"
    ADMIN_4 = "➻ sᴛʀᴇᴀᴍ ʀᴇsᴜᴍᴇᴅ 🎄\n│ \n└ʙʏ : {0} 🥀"
    ADMIN_5 = "➻ sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ/sᴛᴏᴩᴩᴇᴅ 🎄\n│ \n└ʙʏ : {0} 🥀"

    @staticmethod
    def get_help_keyboard():
        keyboard = [
            [
                InlineKeyboardButton("Aᴄᴛɪᴏɴ", callback_data="help_action"),
                InlineKeyboardButton("Aᴅᴍɪɴ", callback_data="help_admin")
            ],
            [
                InlineKeyboardButton("Aᴜᴛʜ", callback_data="help_auth"),
                InlineKeyboardButton("Bʟ-ᴄʜᴀᴛ", callback_data="help_blchat")
            ],
            [
                InlineKeyboardButton("Bʟ-ᴜꜱᴇʀ", callback_data="help_bluser"),
                InlineKeyboardButton("C-ᴘʟᴀʏ", callback_data="help_cplay")
            ],
            [
                InlineKeyboardButton("Exᴛʀᴀ", callback_data="help_extra"),
                InlineKeyboardButton("G-ʙᴀɴ", callback_data="help_gban")
            ],
            [
                InlineKeyboardButton("G-ᴄᴀꜱᴛ", callback_data="help_gcast"),
                InlineKeyboardButton("Gᴀᴍᴇꜱ", callback_data="help_games")
            ],
            [
                InlineKeyboardButton("Gᴘᴛ", callback_data="help_gpt"),
                InlineKeyboardButton("Iɴғᴏ", callback_data="help_info")
            ],
            [
                InlineKeyboardButton("Iᴍᴀɢᴇ", callback_data="help_image"),
                InlineKeyboardButton("Lᴏɢ", callback_data="help_log")
            ],
            [
                InlineKeyboardButton("Lᴏᴏᴘ", callback_data="help_loop"),
                InlineKeyboardButton("Gʀᴏᴜᴘ", callback_data="help_group")
            ],
            [
                InlineKeyboardButton("Mᴀꜱᴛɪ", callback_data="help_masti"),
                InlineKeyboardButton("Mᴀꜱꜱ ᴀᴄᴛɪᴏɴꜱ", callback_data="help_mass")
            ],
            [
                InlineKeyboardButton("Pɪɴɢ", callback_data="help_ping"),
                InlineKeyboardButton("Pʟᴀʏ", callback_data="help_play")
            ],
            [
                InlineKeyboardButton("Rᴇᴘᴏ ɪɴғᴏ", callback_data="help_repo"),
                InlineKeyboardButton("Sᴇᴀʀᴄʜ", callback_data="help_search")
            ],
            [
                InlineKeyboardButton("Sᴇᴇᴋ", callback_data="help_seek"),
                InlineKeyboardButton("Sʜᴜғғʟᴇ", callback_data="help_shuffle")
            ],
            [
                InlineKeyboardButton("Sᴏɴɢ", callback_data="help_song"),
                InlineKeyboardButton("Sᴘᴇᴇᴅ", callback_data="help_speed")
            ],
            [
                InlineKeyboardButton("Sᴛɪᴄᴋᴇʀ", callback_data="help_sticker"),
                InlineKeyboardButton("Tᴀɢ-ᴀʟʟ", callback_data="help_tagall")
            ],
            [
                InlineKeyboardButton("Tᴇxᴛ ᴇᴅɪᴛɪɴɢ", callback_data="help_text")
            ],
            [
                InlineKeyboardButton(Messages.CLOSE_BUTTON, callback_data="close")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_start_keyboard():
        keyboard = [
            [
                InlineKeyboardButton("˹ᴋɪᴅɴᴀᴘ ᴍᴇ ʙᴀʙᴇs˼", url="https://t.me/crush_hu_tera"),
                InlineKeyboardButton("🍂 ᴄʜᴀɴɴᴇʟ 🍂", url="https://t.me/crush_hu_tera")
            ],
            [
                InlineKeyboardButton("ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs ❓", callback_data="help"),
                InlineKeyboardButton("❄️sᴜᴘᴘᴏʀᴛ❄️", url="https://t.me/crush_hu_tera")
            ],
            [
                InlineKeyboardButton("💗 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 💗", url="https://t.me/crush_hu_tera"),
                InlineKeyboardButton("ʏᴏᴜᴛᴜʙᴇ", url="https://t.me/crush_hu_tera")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

# Create a global messages instance
messages = Messages() 