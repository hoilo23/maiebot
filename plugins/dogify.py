from plugins import new_message, enable_check


# dogify
def dogify(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    # join the list of words into a single string
    if not args:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/dogify <your words>`')
    else:
        all_words = ' '.join(args)
        bot.send_photo(chat_id=update.message.chat_id, photo=f'http://dogr.io/{all_words}.png?split=false&.png')
