import requests
import telebot # pip3 install PyTelegramBotAPI
from token_telegram import _token

bot = telebot.TeleBot(_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я старый Wikibot от Вовы. Приятно познакомиться, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    numbers = [str(_) for _ in range(100)]
    inq = message.text
    responce = requests.get('http://ru.wikipedia.org/wiki' + '/' + str(inq))
    if inq in responce.text:
        bot.send_message(message.from_user.id,
                         responce.text[responce.text.index('<title>') + len('<title>'):responce.text.index('</title>')])
        var = responce.text[responce.text.index('<p>') + len('<p>'):responce.text.index('</p>')]
        var_exit = list(var)
        while "<" in var_exit or "&" in var_exit:
            if "<" in var_exit:
                del var_exit[var_exit.index('<'):var_exit.index('>') + 1]

            if ";" in var_exit:
                if var_exit[var_exit.index(';') + 1] in numbers:
                    del var_exit[var_exit.index(';') + 1]

            if "&" in var_exit:
                del var_exit[var_exit.index("&"):var_exit.index(";") + 1]

        bot.send_message(message.from_user.id, ''.join(var_exit))
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, тебя, дружище!')

bot.polling(none_stop=True)