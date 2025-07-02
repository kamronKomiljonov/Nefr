from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import sqlite3

TOKEN = '8034327628:AAFdIN_cUkaOPRNc2TlGDICMwrBKi5pY6zw'

CHANNELS = [
    ("https://t.me/uznefr", "@uznefr"),
    ("https://t.me/phonk2030", "@phonk2030"
]

# === DB Setup ===
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# === Helper Functions ===
def check_user_subscription(bot, user_id):
    unsubscribed = []
    for link, username in CHANNELS:
        try:
            member = bot.get_chat_member(chat_id=username, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                unsubscribed.append(link)
        except:
            unsubscribed.append(link)
    return unsubscribed

def save_user(user_id, username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

# === Command Handlers ===
def start(update, context):
    chat_id = update.effective_chat.id

    keyboard = [[InlineKeyboardButton("✅ Tasdiqlash", callback_data="verify")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    channels_text = "\n".join([f"👉 <a href='{link}'>{link}</a>" for link, _ in CHANNELS])

    message = (
        "🎮 <b>play.nefr.uz Minecraft serverida bo‘lib o‘tadigan Squid Game o‘yinida ishtirok etish uchun</b>\n\n"
        "Quyidagi kanallarga obuna bo‘ling va <b>Tasdiqlash</b> tugmasini bosing:\n\n"
        f"{channels_text}"
    )

    context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode="HTML", disable_web_page_preview=True)

def verify_callback(update, context):
    query = update.callback_query
    user = query.from_user
    user_id = user.id
    username = user.username

    unsubscribed = check_user_subscription(context.bot, user_id)

    if unsubscribed:
        text = "🚫 Quyidagi kanallarga hali obuna bo‘lmagansiz:\n\n"
        text += "\n".join([f"🔗 <a href='{link}'>{link}</a>" for link in unsubscribed])
        context.bot.send_message(chat_id=user_id, text=text, parse_mode="HTML", disable_web_page_preview=True)
    else:
        save_user(user_id, username)
        msg = (
            "✅ <b>Tabriklaymiz!</b> Siz Squid Game o‘yinida ishtirokchisiz!\n"
            "O‘yin boshlanishidan 1 kun oldin sizga eslatma yuboramiz.\n\n"
            "🌐 Server IP: <code>play.nefr.uz</code>"
        )
        context.bot.send_message(chat_id=user_id, text=msg, parse_mode="HTML")

    query.answer()

# === Botni ishga tushirish ===
def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))

    print("Bot ishlayapti...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
