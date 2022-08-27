'''
Телеграмм-бот. Возвращает содержимое превого
тега параграфа из Википедии по запросу
'''
import requests
import telebot
from bs4 import BeautifulSoup

from token_telegram import _token

bot = telebot.TeleBot(_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я новый Wikibot от Вовы. Приятно познакомиться, '
                          f'{message.from_user.first_name}'
                 )

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    inq = message.text
    responce = requests.get('http://ru.wikipedia.org/wiki' + '/' + str(inq))
    if inq in responce.text:
        html_doc = BeautifulSoup(responce.text, features='html.parser')
        title = html_doc.find('h1', {'id': 'firstHeading'})
        content = html_doc.find_all('p')
        bot.send_message(message.from_user.id, title.text)
        bot.send_message(message.from_user.id, content[0].text)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, тебя, дружище!')

bot.polling(none_stop=True)