from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async
import telebot 
import config
import requests
import re


bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def start_command(message):
    msg = bot.send_message(message.chat.id, 'Привет! Я doggy bot.\n' +
        'Нажми /help, что бы написать создателю.\n ' +
        'Что бы увидеть немного приятностей, используй комманду /boop!')


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Написать создателю', url='telegram.me/anastacia_igorevna'))

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

@run_async
def boop(update, context):
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater('1115596436:AAFp3qGXwQVv7JSNSHYUvccnPAcUDii7NQ0', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('boop',boop))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

bot.polling(none_stop=True)
