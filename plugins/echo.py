from plugins import new_message


# echo
def echo(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, text='Please enter some text')
    else:
        # join the list of words into a single string
        all_words = ' '.join(args)
        bot.send_message(chat_id=update.message.chat_id, text=all_words)
