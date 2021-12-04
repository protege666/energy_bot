import telebot
import sqlite3
from telebot import types
from emoji import emojize
from registration import *

bot = telebot.TeleBot("5051697514:AAEvyLM2LXkv54lmzTC9idXFjdt367tiKCE")
smile = [emojize(':wink:', use_aliases=True), emojize(':exclamation:', use_aliases=True)]

@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.send_message(message.chat.id, f'Приветствую тебя, {message.chat.first_name} {message.chat.last_name}')
    bot.send_message(message.chat.id, f'Для выполнения заданий пройдите регистрацию{smile[0]} \n\n(Команда /reg)')
    global telegram_id
    telegram_id = message.from_user.id

@bot.message_handler(commands=['check'])
def check_db(message):
    sqlcheck()


@bot.message_handler(commands=['del'])
def delete_table(message):
    global telegram_id
    telegram_id = message.from_user.id
    delete(telegram_id)

@bot.message_handler(commands=['reg'])
def registration(message):
    bot.send_message(message.chat.id, 'Укажите свою фамилию: ')
    bot.register_next_step_handler(message, get_surname)

@bot.message_handler(commands=['profile'])
def check_profilee(message):
    global telegram_id
    telegram_id = message.from_user.id
    result = check_profile(telegram_id)
    name = result[2]
    surname = result[1]
    pat = result[3]
    post = result[4]

    print(result)
    bot.send_message(message.chat.id, f"{smile[1]} Ваш профиль {smile[1]}\n\nФамилия: {surname}\nИмя: {name}\nОтчество: {pat}\nДолжность: {post}\n\n{smile[1]} Успеваемость {smile[1]}\n\nМодуль 1: Не пройден\nМодуль 2: Не пройден\nМодуль 3: Не пройден\nМодуль 4: Не пройден\nМодуль 5: Не пройден\nМодуль 6: Не пройден\nМодуль 7: Не пройден\n")


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Укажите свое имя: ')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Укажите свое отчество: ')
    bot.register_next_step_handler(message, get_patronymic)


def get_patronymic(message):
    global patronymic
    patronymic = message.text
    bot.send_message(message.from_user.id, 'Укажите свою должность: ')
    bot.register_next_step_handler(message, get_post)


def get_post(message):
    global telegram_id
    telegram_id = message.from_user.id
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    markup_inline.add(item_yes, item_no)
    global post
    global msg
    post = message.text
    bot.send_message(message.from_user.id,
                     f'{smile[1]}Проверьте свои данные{smile[1]}\n\nФамилия: {surname}\nИмя: {name}\nОтчество: {patronymic}\nДолжность: {post}')
    msg = bot.send_message(message.chat.id, 'Все верно?', reply_markup=markup_inline)
   # bot.register_next_step_handler(message, check)


"""def check(message):
    text = message.text
    print(telegram_id)
    if text == "Да":
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton('Далее')
        markup.add(btn1)
        sql(telegram_id, surname, name, patronymic, post)
        bot.send_message(message.from_user.id, 'Вы успешно зарегистрировались!', reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Пройдите регистрацию еще раз /reg')
        bot.register_next_step_handler(message, registration)"""


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'yes':
            markup_inline = types.InlineKeyboardMarkup()
            profile = types.InlineKeyboardButton(text='Профиль', callback_data='profile')
            firsttest = types.InlineKeyboardButton(text='Пройти начальное тестирование', callback_data='first_test')
            markup_inline.add(profile, firsttest)
            sql(telegram_id, surname, name, patronymic, post)
            bot.send_message(call.message.chat.id, 'Вы успешно зарегистрировались!', reply_markup=markup_inline)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=msg.message_id)
            bot.delete_message(call.message.chat.id, msg.message_id)
        elif call.data == 'no':
            bot.send_message(call.message.chat.id, 'Пройдите регистрацию еще раз /reg')
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=msg.message_id)
            bot.delete_message(call.message.chat.id, msg.message_id)
        elif call.data == "profile":
            result = check_profile(telegram_id)
            name1 = result[2]
            surname1 = result[1]
            pat1 = result[3]
            post1 = result[4]
            print(result)
            bot.send_message(call.message.chat.id,
                             f"{smile[1]} Ваш профиль {smile[1]}\n\nФамилия: {surname1}\nИмя: {name1}\nОтчество: {pat1}\nДолжность: {post1}\n\n{smile[1]} Успеваемость {smile[1]}\n\nМодуль 1: Не пройден\nМодуль 2: Не пройден\nМодуль 3: Не пройден\nМодуль 4: Не пройден\nМодуль 5: Не пройден\nМодуль 6: Не пройден\nМодуль 7: Не пройден\n")
        elif call.data == "first_test":
            pass



bot.polling(none_stop=True)