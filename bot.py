import asyncio
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import TOKEN, CHAT_ID

'''
чтобы бот заработал необходимо создать config.py и прописать в конфиге 
TOKEN и CHAT_ID в таком виде
TOKEN = "6267516757:AAFdKjFF7no4JqHuraYu5oDQ3amjE2WMW00"
CHAT_ID = "-0000000000000"
'''

async def send_message(messege_str):
    text = messege_str
    bot = Bot(TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)

