import os
import telebot
import random
from telebot import types
from dotenv import load_dotenv
from background import keep_alive

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT-TOKEN'))
bot_users = {}

times_type = ['Утром', 'Днем', 'Вечером']
wow_words = ['Супер', 'Волшебно', 'Класс']
heart_icons = ['❤️', '💕', '💖']


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id,
                     "👋 Привет! Я твой бот-помощник, который поможет тебе сохранить хорошее настроение 😊",
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def print_hi(message):
    bot.send_message(message.chat.id, 'help')


@bot.message_handler(func=lambda message:message.text == '👋 Поздороваться')
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Утром')
    btn2 = types.KeyboardButton('Днем')
    btn3 = types.KeyboardButton('Вечером')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, 'В какое время суток тебе напомнить ❓', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in times_type)
def get_time(message):
    bot.send_message(message.from_user.id,
                     f'{random.choice(wow_words)}, я напомню о себе {message.text} {random.choice(heart_icons)}',
                     parse_mode='Markdown',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot_users[message.from_user.id] = message.text
    print(bot_users)


def main():
    keep_alive()
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
