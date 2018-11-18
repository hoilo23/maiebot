from plugins import new_message


# sends the current group chat id or the users id
def get_id(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, text=f'Your user id is: {update.message.from_user.id}')
        return
    if args[0] == 'group':
        bot.send_message(chat_id=update.message.chat_id, text=f'This group\'s id is: {update.message.chat_id}')
