import os
import telebot
import random
from telebot import types
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from threading import Thread

load_dotenv()

TIMES_TYPE = ['Утром', 'Днем', 'Вечером']
WOW_WORDS = ['Супер', 'Волшебно', 'Класс']
HEART_ICONS = ['❤️', '💕', '💖']
DATAFILE = './users.txt'


class Bot:
    def __init__(self, key=os.getenv('BOT-TOKEN'), times_type=TIMES_TYPE, wow_words=WOW_WORDS, heart_icons=HEART_ICONS,
                 file=DATAFILE):
        self.bot = telebot.TeleBot(key)
        self.__times_type = times_type
        self.__wow_words = wow_words
        self.__heart_icons = heart_icons
        self.__file = file

        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("👋 Поздороваться")
            markup.add(btn1)
            self.bot.send_message(message.from_user.id,
                                  "👋 Привет! Я твой бот-помощник, который поможет тебе сохранить хорошее настроение 😊",
                                  reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text == '👋 Поздороваться')
        def get_text_messages(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Утром')
            btn2 = types.KeyboardButton('Днем')
            btn3 = types.KeyboardButton('Вечером')
            markup.add(btn1, btn2, btn3)
            self.bot.send_message(message.from_user.id, 'В какое время суток тебе напомнить ❓', reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text in self.__times_type)
        def get_time(message):
            self.bot.send_message(message.from_user.id,
                                  f'{random.choice(self.__wow_words)}, я напомню о себе {message.text} {random.choice(self.__heart_icons)}',
                                  parse_mode='Markdown',
                                  reply_markup=telebot.types.ReplyKeyboardRemove())
            self.__write_user(message)

    def start(self):
        x = Thread(target=self.bot.polling)
        x.start()

    def __write_user(self, message):
        with open(self.__file, 'a') as file:
            values = ' '.join([str(message.from_user.id), str(message.from_user.first_name), str(message.text)])
            file.write(f'{values}  \n')

    def send_messages(self, interval):
        bot_users = self.__read_users()
        print(bot_users)
        users_to_sent = [key[1] for key, val in bot_users.items() if val == interval]
        picture_url = self.__get_image_url()
        for user_id in users_to_sent:
            text = f'{bot_users[user_id][0]} ты лучше всех!'
            self.bot.send_photo(user_id, picture_url, caption=text)

    def __read_users(self):
        users = {}
        with open(self.__file, 'r') as file:
            for line in file:
                users[line.split()[0]] = [line.split()[1], line.split()[2]]
            return users

    @staticmethod
    def __get_image_url():
        word = 'cute animal'
        url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'lxml')
        images = soup.findAll('img')
        url = random.choice(images).get('src')
        return url
