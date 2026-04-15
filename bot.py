import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Railway se token lega
TOKEN = os.getenv("TOKEN")

# Yaha apne 2 backup channels daal
CHANNELS = ["@godcri_c", "@back_917"]

# Yaha apna main channel link daal (jaha content hai)
MAIN_CHANNEL = "https://t.me/desi_inks"


# Check join function
async def is_joined(bot, user_id):
    for ch in CHANNELS:
        member = await bot.get_chat_member(ch, user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            return False
    return True


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if await is_joined(context.bot, user_id):
        await update.message.reply_text(
            f"🔥 Access Granted!\n\n👉 Content yaha milega:\n{MAIN_CHANNEL}"
        )
    else:
        buttons = []

        for ch in CHANNELS:
            buttons.append([
                InlineKeyboardButton(
                    f"📢 Join {ch}",
                    url=f"https://t.me/{ch[1:]}"
                )
            ])

        buttons.append([
            InlineKeyboardButton("✅ I Joined", callback_data="check_join")
        ])

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text(
            "❌ Content unlock karne ke liye pehle dono channels join karo!",
            reply_markup=reply_markup
        )


# Button click check
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_joined(context.bot, user_id):
        await query.answer()
        await query.edit_message_text(
            f"🔥 Access Granted!\n\n👉 Ab content yaha milega:\n{MAIN_CHANNEL}"
        )
    else:
        await query.answer("❌ Abhi dono channel join nahi kiya!", show_alert=True)


# Run bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

app.run_polling()
