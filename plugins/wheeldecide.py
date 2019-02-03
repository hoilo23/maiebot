from plugins import new_message
import random


# sends a random reply from the args
def wheeldecide(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if len(args) < 2:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/wheeldecide <option 1> <option 2>`')
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text=args[random.randint(0, len(args) - 1)])
