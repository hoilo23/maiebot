from plugins import new_message


# dogify
def dogify(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    # join the list of words into a single string
    all_words = ' '.join(args)
    if all_words == '':
        bot.send_message(chat_id=update.message.chat_id, text='Please enter text!')
    else:
        bot.send_photo(chat_id=update.message.chat_id, photo=f'http://dogr.io/{all_words}.png?split=false&.png')
