import requests
import telebot
from bs4 import BeautifulSoup

from token_telegram import _token

bot = telebot.TeleBot(_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я Wikibot от Вовы. Приятно познакомиться, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    inq = message.text
    responce = requests.get('http://ru.wikipedia.org/wiki' + '/' + str(inq))
    if inq in responce.text:

        html_doc = BeautifulSoup(responce.text, features='html.parser')
        title = html_doc.find('h1', {'id': 'firstHeading'})
        content = html_doc.find('<p>')

        print(title.text)
        print(content.text)

        bot.send_message(message.from_user.id, title.text)
    #     var = responce.text[responce.text.index('<p>') + len('<p>'):responce.text.index('</p>')]
    #     var_exit = list(var)
    #     while "<" in var_exit or "&" in var_exit:
    #         if "<" in var_exit:
    #             del var_exit[var_exit.index('<'):var_exit.index('>') + 1]
    #
    #         if ";" in var_exit:
    #             if var_exit[var_exit.index(';') + 1] in numbers:
    #                 del var_exit[var_exit.index(';') + 1]
    #
    #         if "&" in var_exit:
    #             del var_exit[var_exit.index("&"):var_exit.index(";") + 1]
    #
        bot.send_message(message.from_user.id, content.text)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, тебя, дружище!')


bot.polling(none_stop=True)