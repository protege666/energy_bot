# -*- coding: utf-8 -*-
import telebot
import sqlite3
from telebot import types
from emoji import emojize
from registration import *
from first_test import questions, answers
from module_11 import ques, answerss, teory
import wiki


bot = telebot.TeleBot("5051697514:AAEvyLM2LXkv54lmzTC9idXFjdt367tiKCE")
smile = [emojize(':wink:', use_aliases=True), emojize(':exclamation:', use_aliases=True)]
global q_1, q_2,q_3,q_4,q_5,q_6,q_7,q_8,q_9,q_10,q_11,q_12,q_13,q_14,q_15,q_16,q_17,q_18,q_19, const_ans, const_ans1, w, a, a1
modlist = ["Не пройден", "Не пройден","Не пройден","Не пройден","Не пройден","Не пройден","Не пройден",]

const_ans = 0


@bot.message_handler(commands=['wiki'])
def welcome_start(message):
    bot.send_message(message.chat.id, 'Какой термин вам непонятен?')
    bot.register_next_step_handler(message, get_wiki)


def get_wiki(message):
    text = message.text
    bot.send_message(message.chat.id, wiki.getwiki(text))


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
    markup_inline = types.InlineKeyboardMarkup()
    firsttest = types.InlineKeyboardButton(text='Пройти начальное тестирование', callback_data='first_test')
    markup_inline.add(firsttest)
    bot.send_message(message.chat.id,
                     f"{smile[1]} Ваш профиль {smile[1]}\n\nФамилия: {surname}\nИмя: {name}\nОтчество: {pat}\nДолжность: {post}\nУникальный идентификатор: {telegram_id}\n\n{smile[1]} Успеваемость {smile[1]}\n\nМодуль 1: {modlist[0]}\nМодуль 2: {modlist[1]}\nМодуль 3: Не пройден\nМодуль 4: Не пройден\nМодуль 5: Не пройден\nМодуль 6: Не пройден\nМодуль 7: Не пройден\n", reply_markup=markup_inline)


@bot.message_handler(commands=['reg'])
def registration(message):
    bot.send_message(message.chat.id, 'Укажите свою фамилию: ')
    bot.register_next_step_handler(message, get_surname)


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


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def callback_yes(call):
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
            bot.register_next_step_handler(call.message, vst_test)


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def callback_yes(call):
    if call.message:
        if call.data == 'no':
            bot.send_message(call.message.chat.id, 'Пройдите регистрацию еще раз /reg')
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=msg.message_id)
            bot.delete_message(call.message.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'profile')
def profile(call):
    if call.message:
        if call.data == 'profile':
            result = check_profile(telegram_id)
            name = result[2]
            surname = result[1]
            pat = result[3]
            post = result[4]

            print(result)
            bot.send_message(call.message.chat.id,
                             f"{smile[1]} Ваш профиль {smile[1]}\n\nФамилия: {surname}\nИмя: {name}\nОтчество: {pat}\nДолжность: {post}\nУникальный идентификатор: {telegram_id}\n\n{smile[1]} Успеваемость {smile[1]}\n\nМодуль 1: {modlist[0]}\nМодуль 2: {modlist[1]}\nМодуль 3: {modlist[2]}\nМодуль 4: Не пройден\nМодуль 5: Не пройден\nМодуль 6: Не пройден\nМодуль 7: Не пройден\n")


@bot.callback_query_handler(func=lambda call: call.data == 'first_test')
def vst_test(call):
    if call.message:
        if call.data == 'first_test':
            markup = types.InlineKeyboardMarkup()
            global w
            w = bot.send_message(call.message.chat.id, 'Итак,присутпим к тесту, всего будет 19 вопросов.',
                             reply_markup=markup)
            answ1 = types.InlineKeyboardButton(text=answers[1][0], callback_data='otl')
            answ2 = types.InlineKeyboardButton(text=answers[1][1], callback_data='hor')
            answ3 = types.InlineKeyboardButton(text=answers[1][2], callback_data='ud')
            answ4 = types.InlineKeyboardButton(text=answers[1][3], callback_data='pl')
            markup.add(answ1, answ2, answ3, answ4)
            global q_1
            q_1 = bot.send_message(call.message.chat.id, questions[1], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_2)
    else:
        bot.send_message(call.message.chat.id, 'Что то пошло не так')

@bot.callback_query_handler(
    func=lambda call: call.data == 'otl' or call.data == 'hor' or call.data == 'ud' or call.data == 'pl')
def question_2(call):
    if call.message:
        if call.data == 'otl' or call.data == 'hor' or call.data == 'ud' or call.data == 'pl':
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[2][0], callback_data='q_2_1')
            answ2 = types.InlineKeyboardButton(text=answers[2][1], callback_data='q_2_2')
            answ3 = types.InlineKeyboardButton(text=answers[2][2], callback_data='q_2_3')
            answ4 = types.InlineKeyboardButton(text=answers[2][3], callback_data='q_2_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_1.message_id)
            bot.delete_message(call.message.chat.id, q_1.message_id)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=w.message_id)
            bot.delete_message(call.message.chat.id, w.message_id)
            global q_2
            q_2 = bot.send_message(call.message.chat.id, questions[2], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_3)


@bot.callback_query_handler(
    func=lambda call: call.data == 'q_2_1' or call.data == 'q_2_2' or call.data == 'q_2_3' or call.data == 'q_2_3')
def question_3(call):
    if call.message:
        global const_ans1
        if call.data == 'q_2_2' or call.data == 'q_2_3' or call.data == 'q_2_3':

            const_ans1 = const_ans + 0
            #global const_ans1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[3][0], callback_data='q_3_1')
            answ2 = types.InlineKeyboardButton(text=answers[3][1], callback_data='q_3_2')
            answ3 = types.InlineKeyboardButton(text=answers[3][2], callback_data='q_3_3')
            answ4 = types.InlineKeyboardButton(text=answers[3][3], callback_data='q_3_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_2.message_id)
            bot.delete_message(call.message.chat.id, q_2.message_id)
            global q_3
            q_3 = bot.send_message(call.message.chat.id, questions[3], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_4)
        elif call.data == 'q_2_1':
            #global const_ans1
            const_ans1 = const_ans + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[3][0], callback_data='q_3_1')
            answ2 = types.InlineKeyboardButton(text=answers[3][1], callback_data='q_3_2')
            answ3 = types.InlineKeyboardButton(text=answers[3][2], callback_data='q_3_3')
            answ4 = types.InlineKeyboardButton(text=answers[3][3], callback_data='q_3_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_2.message_id)
            bot.delete_message(call.message.chat.id, q_2.message_id)
            #global q_3
            q_3 = bot.send_message(call.message.chat.id, questions[3], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_4)


@bot.callback_query_handler(
    func=lambda call: call.data == 'q_3_1'  or call.data == 'q_3_3' or call.data == 'q_3_3')
def question_4(call):
    if call.message:
        if call.data == 'q_3_1' or call.data == 'q_3_2' or call.data == 'q_3_3' or call.data == 'q_3_3':
            global const_ans2
            const_ans2 = const_ans1 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[4][0], callback_data='q_4_1')
            answ2 = types.InlineKeyboardButton(text=answers[4][1], callback_data='q_4_2')
            answ3 = types.InlineKeyboardButton(text=answers[4][2], callback_data='q_4_3')
            answ4 = types.InlineKeyboardButton(text=answers[4][3], callback_data='q_4_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_3.message_id)
            bot.delete_message(call.message.chat.id, q_3.message_id)
            global q_4
            q_4 = bot.send_message(call.message.chat.id, questions[4], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_5)
        elif call.data == 'q_3_2':
            #global const_ans2
            const_ans2 = const_ans1 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[4][0], callback_data='q_4_1')
            answ2 = types.InlineKeyboardButton(text=answers[4][1], callback_data='q_4_2')
            answ3 = types.InlineKeyboardButton(text=answers[4][2], callback_data='q_4_3')
            answ4 = types.InlineKeyboardButton(text=answers[4][3], callback_data='q_4_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_3.message_id)
            bot.delete_message(call.message.chat.id, q_3.message_id)
            #global q_4
            q_4 = bot.send_message(call.message.chat.id, questions[4], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_5)


@bot.callback_query_handler(
    func=lambda call: call.data == 'q_4_1' or call.data == 'q_4_2' or call.data == 'q_4_3' or call.data == 'q_4_4')
def question_5(call):
    if call.message:
        if call.data == 'q_4_1' or call.data == 'q_4_2' or call.data == 'q_4_3':
            global const_ans3
            const_ans3 = const_ans2 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[5][0], callback_data='q_5_1')
            answ2 = types.InlineKeyboardButton(text=answers[5][1], callback_data='q_5_2')
            answ3 = types.InlineKeyboardButton(text=answers[5][2], callback_data='q_5_3')
            answ4 = types.InlineKeyboardButton(text=answers[5][3], callback_data='q_5_4')
            answ5 = types.InlineKeyboardButton(text=answers[5][4], callback_data='q_5_5')
            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_4.message_id)
            bot.delete_message(call.message.chat.id, q_4.message_id)
            global q_5
            q_5 = bot.send_message(call.message.chat.id, questions[5], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_6)
        elif call.data == 'q_4_4':
            #global const_ans3
            const_ans3 = const_ans2 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[5][0], callback_data='q_5_1')
            answ2 = types.InlineKeyboardButton(text=answers[5][1], callback_data='q_5_2')
            answ3 = types.InlineKeyboardButton(text=answers[5][2], callback_data='q_5_3')
            answ4 = types.InlineKeyboardButton(text=answers[5][3], callback_data='q_5_4')
            answ5 = types.InlineKeyboardButton(text=answers[5][4], callback_data='q_5_5')
            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_4.message_id)
            bot.delete_message(call.message.chat.id, q_4.message_id)
            #global q_5
            q_5 = bot.send_message(call.message.chat.id, questions[5], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_6)


@bot.callback_query_handler(func=lambda
        call: call.data == 'q_5_1' or call.data == 'q_5_2' or call.data == 'q_5_3' or call.data == 'q_5_4' or call.data == 'q_5_5')
def question_6(call):
    if call.message:
        if call.data == 'q_5_1' or call.data == 'q_5_3' or call.data == 'q_5_4' or call.data == 'q_5_5':
            global const_ans4
            const_ans4 = const_ans3 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[6][0], callback_data='q_6_1')
            answ2 = types.InlineKeyboardButton(text=answers[6][1], callback_data='q_6_2')
            answ3 = types.InlineKeyboardButton(text=answers[6][2], callback_data='q_6_3')

            markup.add(answ1, answ2, answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_5.message_id)
            bot.delete_message(call.message.chat.id, q_5.message_id)
            global q_6
            q_6 = bot.send_message(call.message.chat.id, questions[6], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_7)
        elif call.data == 'q_5_2' :
            #global const_ans4
            const_ans4 = const_ans3 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[6][0], callback_data='q_6_1')
            answ2 = types.InlineKeyboardButton(text=answers[6][1], callback_data='q_6_2')
            answ3 = types.InlineKeyboardButton(text=answers[6][2], callback_data='q_6_3')

            markup.add(answ1, answ2, answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_5.message_id)
            bot.delete_message(call.message.chat.id, q_5.message_id)
            #global q_6
            q_6 = bot.send_message(call.message.chat.id, questions[6], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_7)


@bot.callback_query_handler(func=lambda call: call.data == 'q_6_1' or call.data == 'q_6_2' or call.data == 'q_6_3')
def question_7(call):
    if call.message:
        if call.data == 'q_6_1' or call.data == 'q_6_2' :
            global const_ans5
            const_ans5 = const_ans4 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[7][0], callback_data='q_7_1')
            answ2 = types.InlineKeyboardButton(text=answers[7][1], callback_data='q_7_2')
            answ3 = types.InlineKeyboardButton(text=answers[7][2], callback_data='q_7_3')

            markup.add(answ1, answ2, answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_6.message_id)
            bot.delete_message(call.message.chat.id, q_6.message_id)
            global q_7
            q_7 = bot.send_message(call.message.chat.id, questions[7], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_8)
        elif call.data == 'q_6_3':
            #global const_ans5
            const_ans5 = const_ans4 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[7][0], callback_data='q_7_1')
            answ2 = types.InlineKeyboardButton(text=answers[7][1], callback_data='q_7_2')
            answ3 = types.InlineKeyboardButton(text=answers[7][2], callback_data='q_7_3')

            markup.add(answ1, answ2, answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_6.message_id)
            bot.delete_message(call.message.chat.id, q_6.message_id)
            #global q_7
            q_7 = bot.send_message(call.message.chat.id, questions[7], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_8)


@bot.callback_query_handler(func=lambda call: call.data == 'q_7_1' or call.data == 'q_7_2' or call.data == 'q_7_3')
def question_8(call):
    if call.message:
        if  call.data == 'q_7_2' or call.data == 'q_7_3':
            global const_ans6
            const_ans6 = const_ans5 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[8][0], callback_data='q_8_1')
            answ2 = types.InlineKeyboardButton(text=answers[8][1], callback_data='q_8_2')
            answ3 = types.InlineKeyboardButton(text=answers[8][2], callback_data='q_8_3')
            answ4 = types.InlineKeyboardButton(text=answers[8][3], callback_data='q_8_4')
            answ5 = types.InlineKeyboardButton(text=answers[8][4], callback_data='q_8_5')

            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_7.message_id)
            bot.delete_message(call.message.chat.id, q_7.message_id)
            global q_8
            q_8 = bot.send_message(call.message.chat.id, questions[8], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_9)

        elif call.data == 'q_7_1':
            #global const_ans6
            const_ans6 = const_ans5 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[8][0], callback_data='q_8_1')
            answ2 = types.InlineKeyboardButton(text=answers[8][1], callback_data='q_8_2')
            answ3 = types.InlineKeyboardButton(text=answers[8][2], callback_data='q_8_3')
            answ4 = types.InlineKeyboardButton(text=answers[8][3], callback_data='q_8_4')
            answ5 = types.InlineKeyboardButton(text=answers[8][4], callback_data='q_8_5')

            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_7.message_id)
            bot.delete_message(call.message.chat.id, q_7.message_id)
           # global q_8
            q_8 = bot.send_message(call.message.chat.id, questions[8], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_9)


@bot.callback_query_handler(func=lambda
        call: call.data == 'q_8_1' or call.data == 'q_8_2' or call.data == 'q_8_3' or call.data == 'q_8_4' or call.data == 'q_8_5')
def question_9(call):
    if call.message:
        if call.data == 'q_8_1' or call.data == 'q_8_2' or call.data == 'q_8_3' or call.data == 'q_8_4':
            global const_ans7
            const_ans7 = const_ans6 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[9][0], callback_data='q_9_1')
            answ2 = types.InlineKeyboardButton(text=answers[9][1], callback_data='q_9_2')
            answ3 = types.InlineKeyboardButton(text=answers[9][2], callback_data='q_9_3')
            answ4 = types.InlineKeyboardButton(text=answers[9][3], callback_data='q_9_4')
            answ5 = types.InlineKeyboardButton(text=answers[9][4], callback_data='q_9_5')
            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_8.message_id)
            bot.delete_message(call.message.chat.id, q_8.message_id)
            global q_9
            q_9 = bot.send_message(call.message.chat.id, questions[9], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_10)

        elif call.data == 'q_8_5':
            #global const_ans7
            const_ans7 = const_ans6 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[9][0], callback_data='q_9_1')
            answ2 = types.InlineKeyboardButton(text=answers[9][1], callback_data='q_9_2')
            answ3 = types.InlineKeyboardButton(text=answers[9][2], callback_data='q_9_3')
            answ4 = types.InlineKeyboardButton(text=answers[9][3], callback_data='q_9_4')
            answ5 = types.InlineKeyboardButton(text=answers[9][4], callback_data='q_9_5')
            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_8.message_id)
            bot.delete_message(call.message.chat.id, q_8.message_id)
           # global q_9
            q_9 = bot.send_message(call.message.chat.id, questions[9], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_10)


@bot.callback_query_handler(func=lambda
        call: call.data == 'q_9_1' or call.data == 'q_9_2' or call.data == 'q_9_3' or call.data == 'q_9_4' or call.data == 'q_9_5')
def question_10(call):
    if call.message:
        if call.data == 'q_9_2' or call.data == 'q_9_3' or call.data == 'q_9_4' or call.data == 'q_9_5':
            global const_ans8
            const_ans8 = const_ans7 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[10][0], callback_data='q_10_1')
            answ2 = types.InlineKeyboardButton(text=answers[10][1], callback_data='q_10_2')
            answ3 = types.InlineKeyboardButton(text=answers[10][2], callback_data='q_10_3')
            answ4 = types.InlineKeyboardButton(text=answers[10][3], callback_data='q_10_4')
            answ5 = types.InlineKeyboardButton(text=answers[10][4], callback_data='q_10_5')
            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_9.message_id)
            bot.delete_message(call.message.chat.id, q_9.message_id)
            global q_10
            q_10 = bot.send_message(call.message.chat.id, questions[10], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_11)

        elif call.data == 'q_9_1':
            #global const_ans8
            const_ans8 = const_ans7 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[10][0], callback_data='q_10_1')
            answ2 = types.InlineKeyboardButton(text=answers[10][1], callback_data='q_10_2')
            answ3 = types.InlineKeyboardButton(text=answers[10][2], callback_data='q_10_3')
            answ4 = types.InlineKeyboardButton(text=answers[10][3], callback_data='q_10_4')
            answ5 = types.InlineKeyboardButton(text=answers[10][4], callback_data='q_10_5')
            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_9.message_id)
            bot.delete_message(call.message.chat.id, q_9.message_id)
            #global q_10
            q_10 = bot.send_message(call.message.chat.id, questions[10], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_11)


@bot.callback_query_handler(func=lambda
        call: call.data == 'q_10_1' or call.data == 'q_10_2' or call.data == 'q_10_3' or call.data == 'q_10_4' or call.data == 'q_10_5')
def question_11(call):
    if call.message:
        if call.data == 'q_10_1' or call.data == 'q_10_2' or call.data == 'q_10_3' or call.data == 'q_10_4' :
            global const_ans9
            const_ans9 = const_ans8 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[11][0], callback_data='q_11_1')
            answ2 = types.InlineKeyboardButton(text=answers[11][1], callback_data='q_11_2')
            answ3 = types.InlineKeyboardButton(text=answers[11][2], callback_data='q_11_3')
            answ4 = types.InlineKeyboardButton(text=answers[11][3], callback_data='q_11_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_10.message_id)
            bot.delete_message(call.message.chat.id, q_10.message_id)
            global q_11
            q_11 = bot.send_message(call.message.chat.id, questions[11], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_12)

        elif call.data == 'q_10_5':
            #global const_ans9
            const_ans9 = const_ans8 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[11][0], callback_data='q_11_1')
            answ2 = types.InlineKeyboardButton(text=answers[11][1], callback_data='q_11_2')
            answ3 = types.InlineKeyboardButton(text=answers[11][2], callback_data='q_11_3')
            answ4 = types.InlineKeyboardButton(text=answers[11][3], callback_data='q_11_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_10.message_id)
            bot.delete_message(call.message.chat.id, q_10.message_id)
            #global q_11
            q_11 = bot.send_message(call.message.chat.id, questions[11], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_12)


@bot.callback_query_handler(
    func=lambda call: call.data == 'q_11_1' or call.data == 'q_11_2' or call.data == 'q_11_3' or call.data == 'q_11_4')
def question_12(call):
    if call.message:
        if call.data == 'q_11_2' or call.data == 'q_11_3' or call.data == 'q_11_4':
            global const_ans10
            const_ans10 = const_ans9 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[12][0], callback_data='q_12_1')
            answ2 = types.InlineKeyboardButton(text=answers[12][1], callback_data='q_12_2')
            markup.add(answ1, answ2)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_11.message_id)
            bot.delete_message(call.message.chat.id, q_11.message_id)
            global q_12
            q_12 = bot.send_message(call.message.chat.id, questions[12], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_13)
        elif call.data == 'q_11_1' :
            #global const_ans10
            const_ans10 = const_ans9 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[12][0], callback_data='q_12_1')
            answ2 = types.InlineKeyboardButton(text=answers[12][1], callback_data='q_12_2')
            markup.add(answ1, answ2)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_11.message_id)
            bot.delete_message(call.message.chat.id, q_11.message_id)
            #global q_12
            q_12 = bot.send_message(call.message.chat.id, questions[12], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_13)


@bot.callback_query_handler(func=lambda call: call.data == 'q_12_1' or call.data == 'q_12_2')
def question_13(call):
    if call.message:
        if call.data == 'q_12_1':
            global const_ans11
            const_ans11 = const_ans10 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[13][0], callback_data='q_13_1')
            answ2 = types.InlineKeyboardButton(text=answers[13][1], callback_data='q_13_2')
            answ3 = types.InlineKeyboardButton(text=answers[13][1], callback_data='q_13_3')
            markup.add(answ1, answ2, answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_12.message_id)
            bot.delete_message(call.message.chat.id, q_12.message_id)
            global q_13
            q_13 = bot.send_message(call.message.chat.id, questions[13], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_14)
        elif call.data == 'q_12_2':
            #global const_ans11
            const_ans11 = const_ans10 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[13][0], callback_data='q_13_1')
            answ2 = types.InlineKeyboardButton(text=answers[13][1], callback_data='q_13_2')
            answ3 = types.InlineKeyboardButton(text=answers[13][1], callback_data='q_13_3')
            markup.add(answ1, answ2, answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_12.message_id)
            bot.delete_message(call.message.chat.id, q_12.message_id)
            #global q_13
            q_13 = bot.send_message(call.message.chat.id, questions[13], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_14)


@bot.callback_query_handler(func=lambda call: call.data == 'q_13_1' or call.data == 'q_13_2' or call.data == 'q_13_3')
def question_14(call):
    if call.message:
        if call.data == 'q_13_1' or call.data == 'q_13_2' :
            global const_ans12
            const_ans12 = const_ans11 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[14][0], callback_data='q_14_1')
            answ2 = types.InlineKeyboardButton(text=answers[14][1], callback_data='q_14_2')
            answ3 = types.InlineKeyboardButton(text=answers[14][2], callback_data='q_14_3')
            answ4 = types.InlineKeyboardButton(text=answers[14][3], callback_data='q_14_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_13.message_id)
            bot.delete_message(call.message.chat.id, q_13.message_id)
            global q_14
            q_14 = bot.send_message(call.message.chat.id, questions[14], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_15)

        elif call.data == 'q_13_3':
            #global const_ans12
            const_ans12 = const_ans11 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[14][0], callback_data='q_14_1')
            answ2 = types.InlineKeyboardButton(text=answers[14][1], callback_data='q_14_2')
            answ3 = types.InlineKeyboardButton(text=answers[14][2], callback_data='q_14_3')
            answ4 = types.InlineKeyboardButton(text=answers[14][3], callback_data='q_14_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_13.message_id)
            bot.delete_message(call.message.chat.id, q_13.message_id)
            #global q_14
            q_14 = bot.send_message(call.message.chat.id, questions[14], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_15)


@bot.callback_query_handler(
    func=lambda call: call.data == 'q_14_1' or call.data == 'q_14_2' or call.data == 'q_14_3' or call.data == 'q_14_4')
def question_15(call):
    if call.message:
        if call.data == 'q_14_1'  or call.data == 'q_14_3' or call.data == 'q_14_4':
            global const_ans13
            const_ans13 = const_ans12 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[15][0], callback_data='q_15_1')
            answ2 = types.InlineKeyboardButton(text=answers[15][1], callback_data='q_15_2')
            answ3 = types.InlineKeyboardButton(text=answers[15][2], callback_data='q_15_3')
            answ4 = types.InlineKeyboardButton(text=answers[15][3], callback_data='q_15_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_14.message_id)
            bot.delete_message(call.message.chat.id, q_14.message_id)
            global q_15
            q_15 = bot.send_message(call.message.chat.id, questions[15], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_16)
        elif call.data == 'q_14_2' :
            #global const_ans13
            const_ans13 = const_ans12 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[15][0], callback_data='q_15_1')
            answ2 = types.InlineKeyboardButton(text=answers[15][1], callback_data='q_15_2')
            answ3 = types.InlineKeyboardButton(text=answers[15][2], callback_data='q_15_3')
            answ4 = types.InlineKeyboardButton(text=answers[15][3], callback_data='q_15_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_14.message_id)
            bot.delete_message(call.message.chat.id, q_14.message_id)
           # global q_15
            q_15 = bot.send_message(call.message.chat.id, questions[15], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_16)


@bot.callback_query_handler(
    func=lambda call: call.data == 'q_15_1' or call.data == 'q_15_2' or call.data == 'q_15_3' or call.data == 'q_15_4')
def question_16(call):
    if call.message:
        if call.data == call.data == 'q_15_1' or call.data == 'q_15_2' or call.data == 'q_15_3':
            global const_ans14
            const_ans14 = const_ans13 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[16][0], callback_data='q_16_1')
            answ2 = types.InlineKeyboardButton(text=answers[16][1], callback_data='q_16_2')
            answ3 = types.InlineKeyboardButton(text=answers[16][2], callback_data='q_16_3')
            answ4 = types.InlineKeyboardButton(text=answers[16][3], callback_data='q_16_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_15.message_id)
            bot.delete_message(call.message.chat.id, q_15.message_id)
            global q_16
            q_16 = bot.send_message(call.message.chat.id, questions[16], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_17)
        elif call.data == 'q_15_4':
           # global const_ans14
            const_ans14 = const_ans13 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[16][0], callback_data='q_16_1')
            answ2 = types.InlineKeyboardButton(text=answers[16][1], callback_data='q_16_2')
            answ3 = types.InlineKeyboardButton(text=answers[16][2], callback_data='q_16_3')
            answ4 = types.InlineKeyboardButton(text=answers[16][3], callback_data='q_16_4')
            markup.add(answ1, answ2, answ3, answ4)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_15.message_id)
            bot.delete_message(call.message.chat.id, q_15.message_id)
           # global q_16
            q_16 = bot.send_message(call.message.chat.id, questions[16], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_17)


@bot.callback_query_handler(
    func=lambda call: call.data == 'q_16_1' or call.data == 'q_16_2' or call.data == 'q_16_3' or call.data == 'q_16_4')
def question_17(call):
    if call.message:
        if call.data == 'q_16_1' or call.data == 'q_16_2'  or call.data == 'q_16_4':
            global const_ans15
            const_ans15 = const_ans14 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[17][0], callback_data='q_17_1')
            answ2 = types.InlineKeyboardButton(text=answers[17][1], callback_data='q_17_2')
            answ3 = types.InlineKeyboardButton(text=answers[17][2], callback_data='q_17_3')
            answ4 = types.InlineKeyboardButton(text=answers[17][3], callback_data='q_17_4')
            answ5 = types.InlineKeyboardButton(text=answers[17][4], callback_data='q_17_5')
            answ6 = types.InlineKeyboardButton(text=answers[17][4], callback_data='q_17_6')
            answ7 = types.InlineKeyboardButton(text=answers[17][4], callback_data='q_17_7')
            markup.add(answ1, answ2, answ3, answ4, answ5, answ6, answ7)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_16.message_id)
            bot.delete_message(call.message.chat.id, q_16.message_id)
            global q_17
            q_17 = bot.send_message(call.message.chat.id, questions[17], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_18)
        elif call.data == 'q_16_3' :
           # global const_ans15
            const_ans15 = const_ans14 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[17][0], callback_data='q_17_1')
            answ2 = types.InlineKeyboardButton(text=answers[17][1], callback_data='q_17_2')
            answ3 = types.InlineKeyboardButton(text=answers[17][2], callback_data='q_17_3')
            answ4 = types.InlineKeyboardButton(text=answers[17][3], callback_data='q_17_4')
            answ5 = types.InlineKeyboardButton(text=answers[17][4], callback_data='q_17_5')
            answ6 = types.InlineKeyboardButton(text=answers[17][4], callback_data='q_17_6')
            answ7 = types.InlineKeyboardButton(text=answers[17][4], callback_data='q_17_7')
            markup.add(answ1, answ2, answ3, answ4, answ5, answ6, answ7)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_16.message_id)
            bot.delete_message(call.message.chat.id, q_16.message_id)
           # global q_17
            q_17 = bot.send_message(call.message.chat.id, questions[17], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_18)


@bot.callback_query_handler(func=lambda
        call: call.data == 'q_17_1' or call.data == 'q_17_2' or call.data == 'q_17_3' or call.data == 'q_17_4' or call.data == 'q_17_5' or call.data == 'q_17_6' or call.data == 'q_17_7')
def question_18(call):
    if call.message:
        if call.data == 'q_17_2' or call.data == 'q_17_3' or call.data == 'q_17_4' or call.data == 'q_17_5' or call.data == 'q_17_6' or call.data == 'q_17_7':
            global const_ans16
            const_ans16 = const_ans15 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[18][0], callback_data='q_18_1')
            answ2 = types.InlineKeyboardButton(text=answers[18][1], callback_data='q_18_2')
            answ3 = types.InlineKeyboardButton(text=answers[18][1], callback_data='q_18_3')
            markup.add(answ1, answ2, answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_17.message_id)
            bot.delete_message(call.message.chat.id, q_17.message_id)
            global q_18
            q_18 = bot.send_message(call.message.chat.id, questions[18], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_19)
        elif call.data == 'q_17_1' :
            #global const_ans16
            const_ans16 = const_ans15 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[18][0], callback_data='q_18_1')
            answ2 = types.InlineKeyboardButton(text=answers[18][1], callback_data='q_18_2')
            answ3 = types.InlineKeyboardButton(text=answers[18][1], callback_data='q_18_3')
            markup.add(answ1, answ2, answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_17.message_id)
            bot.delete_message(call.message.chat.id, q_17.message_id)
            #global q_18
            q_18 = bot.send_message(call.message.chat.id, questions[18], reply_markup=markup)
            bot.register_next_step_handler(call.message, question_19)


@bot.callback_query_handler(func=lambda call: call.data == 'q_18_1' or call.data == 'q_18_2' or call.data == 'q_18_3')
def question_19(call):
    if call.message:
        if call.data == 'q_18_1' or call.data == 'q_18_3':
            global const_ans17
            const_ans17 = const_ans16 + 0
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[19][0], callback_data='final')
            answ2 = types.InlineKeyboardButton(text=answers[19][1], callback_data='final')
            answ3 = types.InlineKeyboardButton(text=answers[19][2], callback_data='final')
            answ4 = types.InlineKeyboardButton(text=answers[19][3], callback_data='final')
            answ5 = types.InlineKeyboardButton(text=answers[19][4], callback_data='final')
            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_18.message_id)
            bot.delete_message(call.message.chat.id, q_18.message_id)
            global q_19
            q_19 = bot.send_message(call.message.chat.id, questions[19], reply_markup=markup)
            bot.register_next_step_handler(call.message, vst_test)
        elif call.data == 'q_18_2':
           # global const_ans17
            const_ans17 = const_ans16 + 1
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answers[19][0], callback_data='final')
            answ2 = types.InlineKeyboardButton(text=answers[19][1], callback_data='final')
            answ3 = types.InlineKeyboardButton(text=answers[19][2], callback_data='final')
            answ4 = types.InlineKeyboardButton(text=answers[19][3], callback_data='final')
            answ5 = types.InlineKeyboardButton(text=answers[19][4], callback_data='final')
            markup.add(answ1, answ2, answ3, answ4, answ5)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_18.message_id)
            bot.delete_message(call.message.chat.id, q_18.message_id)
            #global q_19
            q_19 = bot.send_message(call.message.chat.id, questions[19], reply_markup=markup)
            bot.register_next_step_handler(call.message, finall)


@bot.callback_query_handler(func=lambda call: call.data == 'final')
def finall(call):
    if call.message:
        if call.data == 'final':
            finall_const = const_ans17
            proc = (const_ans17 / 17) * 100
            bot.send_message(call.message.chat.id, f"Вы набрали {finall_const} баллов из 17.\n\n {smile[1]} Вы подготовлены на {proc}%{smile[1]}")
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=q_19.message_id)
            bot.delete_message(call.message.chat.id, q_19.message_id)
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton("Перейти к модулю 1", callback_data='module1')
            markup.add(answ1)
            global  send
            send = bot.send_message(call.message.chat.id, f"Можете перейти к модулю 1 {smile[0]}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'module1')
def finall(call):
    if call.message:
        if call.data == 'module1':
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text="Далее", callback_data='dalee')
            markup.add(answ1)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=send.message_id)
            bot.delete_message(call.message.chat.id, send.message_id)
            global a
            a = bot.send_message(call.message.chat.id, teory[1], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'dalee')
def ques1(call):
    if call.message:
        if call.data == 'dalee':
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answerss[1][0], callback_data='q1')
            answ2 = types.InlineKeyboardButton(text=answerss[1][1], callback_data='q2')
            answ3 = types.InlineKeyboardButton(text=answerss[1][2], callback_data='q3')

            markup.add(answ1, answ2,answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=a.message_id)
            bot.delete_message(call.message.chat.id, a.message_id)
            global a1
            a1 = bot.send_message(call.message.chat.id, ques[1], reply_markup=markup)

            bot.register_next_step_handler(call.message, teory2)

@bot.callback_query_handler(func=lambda call: call.data == 'q1' or call.data == 'q2' or call.data == 'q3')
def teory2(call):
    if call.message:
        if call.data == 'q1' or call.data == 'q2' or call.data == 'q3':
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text="Далее", callback_data='dalee1')
            markup.add(answ1)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=a1.message_id)
            bot.delete_message(call.message.chat.id, a1.message_id)
            global a2
            a2 = bot.send_message(call.message.chat.id, teory[2], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'dalee1')
def ques1(call):
    if call.message:
        if call.data == 'dalee1':
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answerss[2][0], callback_data='q4')
            answ2 = types.InlineKeyboardButton(text=answerss[2][1], callback_data='q5')
            answ3 = types.InlineKeyboardButton(text=answerss[2][2], callback_data='q6')
            markup.add(answ1, answ2,answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=a2.message_id)
            bot.delete_message(call.message.chat.id, a2.message_id)
            global a3
            a3 = bot.send_message(call.message.chat.id, ques[2], reply_markup=markup)
            bot.register_next_step_handler(call.message, teory3)


@bot.callback_query_handler(func=lambda call: call.data == 'q4' or call.data == 'q5' or call.data == 'q6')
def teory3(call):
    if call.message:
        if call.data == 'q4' or call.data == 'q5' or call.data == 'q6':
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text="Далее", callback_data='dalee2')
            markup.add(answ1)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=a3.message_id)
            bot.delete_message(call.message.chat.id, a3.message_id)
            global a4
            a4 = bot.send_message(call.message.chat.id, teory[3], reply_markup=markup)
            bot.register_next_step_handler(call.message, ques3)

@bot.callback_query_handler(func=lambda call: call.data == 'dalee2')
def ques3(call):
    if call.message:
        if call.data == 'dalee2':
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text=answerss[3][0], callback_data='q7')
            answ2 = types.InlineKeyboardButton(text=answerss[3][1], callback_data='q8')
            answ3 = types.InlineKeyboardButton(text=answerss[3][2], callback_data='q9')
            markup.add(answ1, answ2,answ3)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=a4.message_id)
            bot.delete_message(call.message.chat.id, a4.message_id)
            global a5
            a5 = bot.send_message(call.message.chat.id, ques[3], reply_markup=markup)
            bot.register_next_step_handler(call.message, teory3)

@bot.callback_query_handler(func=lambda call: call.data == 'q7' or call.data == 'q8' or call.data == 'q9')
def teory3(call):
    if call.message:
        if call.data == 'q7' or call.data == 'q8' or call.data == 'q9':
            markup = types.InlineKeyboardMarkup(row_width=1)
            answ1 = types.InlineKeyboardButton(text="Далее", callback_data='daaalee')
            markup.add(answ1)
            bot.edit_message_text("result", chat_id=call.message.chat.id, message_id=a5.message_id)
            bot.delete_message(call.message.chat.id, a5.message_id)
            global a6
            a6 = bot.send_message(call.message.chat.id, "Вы успешно прошли тест!\nВаша оценка: Отлично")
            modlist[0] = "Пройден"



bot.polling(none_stop=True)
