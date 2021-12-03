import telebot

bot = telebot.TeleBot("5051697514:AAEvyLM2LXkv54lmzTC9idXFjdt367tiKCE")

@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.send_message(message.chat.id, f'Приветствую тебя {message.chat.first_name} {message.chat.last_name} ')
    bot.send_message(message.chat.id, 'Для выполнения заданий пройдите регистрацию!')


bot.infinity_polling()