from plugins import new_message
import os


# opens quotes_chat_id.txt and appends the quote
def add_quote(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not os.path.exists('quotes'):
        os.makedirs('quotes')

    with open(f'./quotes/{update.message.chat_id}.txt', 'a', encoding='utf-8') as list_of_quotes:
        # join the list of words into a single string
        all_words = ' '.join(args)
        if all_words == '':
            bot.send_message(chat_id=update.message.chat_id, text='Please enter a quote!')
        else:
            list_of_quotes.write(f'{all_words} \n')
            bot.send_message(chat_id=update.message.chat_id, text='done!')
