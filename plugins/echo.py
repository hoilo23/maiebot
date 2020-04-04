from plugins import new_message, enable_check


# echo
def echo(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/echo <your words>`')
    else:
        all_words = ' '.join(context.args)
        context.bot.send_message(chat_id=update.message.chat_id, text=all_words)
