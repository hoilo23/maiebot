from plugins import new_message, enable_check
import random
import os


# opens chat_id.txt and sends a random quote to the chat
def get_quote(bot, update):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not os.path.exists('quotes'):
        os.makedirs('quotes')

    if os.path.exists(f'./quotes/{update.message.chat_id}.txt'):
        with open(f'./quotes/{update.message.chat_id}.txt', 'r', encoding='utf-8') as list_of_quotes:
            quotes = list_of_quotes.readlines()
            quote = quotes[random.randint(0, len(quotes) - 1)]
            bot.send_message(chat_id=update.message.chat_id, text=quote)
    else:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown',
                         text='This chat doesn\'t have any quotes, add one using `/addquote <your quote>`')
