from plugins import new_message, enable_check
from telegram.error import BadRequest


# kicks person that executed the command
def kickme(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    try:
        context.bot.kick_chat_member(chat_id=update.message.chat_id, user_id=update.message.from_user['id'])

    except BadRequest:
        context.bot.send_message(chat_id=update.message.chat_id, text=f'Sorry, I can\'t kick you.')
