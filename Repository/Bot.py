import os
import telebot
import random
from telebot import types
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from threading import Thread

load_dotenv()


class Bot:
    def __init__(self, key=os.getenv('BOT-TOKEN')):
        self.bot = telebot.TeleBot(key)
        self.__bot_users = {}
        self.__bot_usernames = {}

        self.__times_type = ['Утром', 'Днем', 'Вечером']
        self.__wow_words = ['Супер', 'Волшебно', 'Класс']
        self.__heart_icons = ['❤️', '💕', '💖']

        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("👋 Поздороваться")
            markup.add(btn1)
            self.bot.send_message(message.from_user.id,
                                  "👋 Привет! Я твой бот-помощник, который поможет тебе сохранить хорошее настроение 😊",
                                  reply_markup=markup)

        @self.bot.message_handler(commands=['help'])
        def print_hi(message):
            self.bot.send_message(message.chat.id, 'help')

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
            self.__bot_users[message.from_user.id] = message.text
            self.__bot_usernames[message.from_user.id] = message.from_user.first_name
            print(f'Users: {self.__bot_users}')

    def start(self):
        x = Thread(target=self.bot.polling)
        x.start()

    def send_messages(self, interval):
        users_to_sent = [key for key, val in self.__bot_users.items() if val == interval]
        picture_url = self.__get_image_url()
        for user_id in users_to_sent:
            text = f'{self.__bot_usernames[user_id]} ты лучший!'
            self.bot.send_photo(user_id, picture_url, caption=text)

    @staticmethod
    def __get_image_url():
        word = 'cute animal'
        url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'lxml')
        images = soup.findAll('img')
        url = random.choice(images).get('src')
        return url
