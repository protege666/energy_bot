import telebot
import sqlite3
from telebot import types
from emoji import emojize
from registration import *

bot = telebot.TeleBot("5051697514:AAEvyLM2LXkv54lmzTC9idXFjdt367tiKCE")

@bot.message_handler(commands=['start'])
def welcome_start(message):
    smile = emojize('U+1F609', use_aliases=True)
    bot.send_message(message.chat.id, f'Приветствую тебя {message.chat.first_name} {message.chat.last_name}')
    bot.send_message(message.chat.id, 'Для выполнения заданий пройдите регистрацию! (Команда /reg)')


@bot.message_handler(commands=['check'])
def check_db(message):
    sqlcheck()

@bot.message_handler(commands=['reg'])
def registration(message):
    bot.send_message(message.chat.id, 'Укажите свое имя: ')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Укажите свою фамилию: ')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Укажите свое отчество: ')
    bot.register_next_step_handler(message, get_patronymic)


def get_patronymic(message):
    global patronymic
    patronymic = message.text
    bot.send_message(message.from_user.id, 'Укажите свою должность: ')
    bot.register_next_step_handler(message, get_post)


def get_post(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Да')
    btn2 = types.KeyboardButton('Нет')
    markup.add(btn1, btn2)
    global post
    post = message.text
    bot.send_message(message.from_user.id,
                     f'Проверьте свои данные!\nИмя: {name}, Фамилия: {surname}, Отчество: {patronymic}, Должность: {post}')
    bot.send_message(message.from_user.id, 'Все верно?', reply_markup=markup)
    bot.register_next_step_handler(message, check)


def check(message):
    text = message.text
    if text == "Да":
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton('Далее')
        markup.add(btn1)
        sql(name, surname, patronymic, post)
        bot.send_message(message.from_user.id, 'Вы успешно зарегистрировались!',reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Пройдите регистрацию еще раз /reg')
        bot.register_next_step_handler(message, registration)




bot.polling(none_stop=True)