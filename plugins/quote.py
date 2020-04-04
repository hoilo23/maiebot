from plugins import new_message, enable_check
import os
import random


def quote(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not os.path.exists('quotes'):
        os.makedirs('quotes')

    if not context.args:
        if os.path.exists(f'./quotes/{update.message.chat_id}.txt'):
            with open(f'./quotes/{update.message.chat_id}.txt', 'r', encoding='utf-8') as list_of_quotes:
                quotes = list_of_quotes.readlines()
                quote = quotes[random.randint(0, len(quotes) - 1)]
                context.bot.send_message(chat_id=update.message.chat_id, text=quote)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='This chat doesn\'t have any quotes, add one using `/quote add <your quote>`')
    elif context.args[0] == 'add' and len(context.args) > 1:
        with open(f'./quotes/{update.message.chat_id}.txt', 'a', encoding='utf-8') as list_of_quotes:
            all_words = ' '.join(context.args[1:])
            list_of_quotes.write(f'{all_words} \n')
            context.bot.send_message(chat_id=update.message.chat_id, text='done!')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/quote [add <your quote>]`')

