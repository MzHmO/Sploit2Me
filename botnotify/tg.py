import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import ForceReply
import asyncio

# COMMAND HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logging.warn(f"[*] New user {update.effective_chat.id}")
    BotService.chat_ids.add(update.effective_chat.id)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

# ENTRYPOINT CLASS
class BotService:
    chat_ids = set()
    application = None

    @staticmethod
    def start(bot_token: str) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        BotService.application = Application.builder().token(bot_token).build()

        BotService.application.add_handler(CommandHandler("start", start))
        BotService.application.add_handler(CommandHandler("help", help_command))
        BotService.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        loop.run_until_complete(BotService.application.run_polling(allowed_updates=Update.ALL_TYPES))

    @staticmethod
    async def notify(message: str):
        if BotService.application is None:
            logging.critical("[*] The application is not initialized yet.")
            return

        bot = BotService.application.bot
        if not bot:
            logging.critical("[*] Bot not initialized.")
            return
        
        failed_chats = []
        for chat_id in BotService.chat_ids:
            try:
                await bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                #logging.critical(f"[*] Could not send message to {chat_id}: {str(e)}")
                #failed_chats.append(chat_id)
                continue

def async_notify(message):
    asyncio.run(BotService.notify(message))

