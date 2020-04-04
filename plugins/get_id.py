from plugins import new_message, enable_check


# sends the current group chat id or the users id
def get_id(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, text=f'Your user id is: {update.message.from_user.id}')
        return
    if context.args[0] == 'group':
        context.bot.send_message(chat_id=update.message.chat_id, text=f'This group\'s id is: {update.message.chat_id}')
