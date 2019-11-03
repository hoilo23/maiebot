from plugins import new_message, enable_check
import os


# opens quotes_chat_id.txt and appends the quote
def add_quote(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not os.path.exists('quotes'):
        os.makedirs('quotes')

    with open(f'./quotes/{update.message.chat_id}.txt', 'a', encoding='utf-8') as list_of_quotes:
        # join the list of words into a single string
        if not args:
            bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/addquote <your quote>`')
        else:
            all_words = ' '.join(args)
            list_of_quotes.write(f'{all_words} \n')
            bot.send_message(chat_id=update.message.chat_id, text='done!')
