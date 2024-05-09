from config import TELEGRAM_TOKEN
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

chat_ids = set() 

class BotService:
    @staticmethod
    def notify(msg):
        pass

    @staticmethod
    def send_message(msg, recipient):
        pass

    @staticmethod
    def send_message_broadcast(msg):
        pass