from plugins import new_message, enable_check
import random


# sends a random reply from the args
def wheeldecide(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/wheeldecide <option 1> <option 2>`')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=context.args[random.randint(0, len(context.args) - 1)])
