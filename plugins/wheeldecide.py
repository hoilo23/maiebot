from plugins import new_message
import random


# sends a random reply from the args
def wheeldecide(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    list_of_decisions = [word for word in args]

    if not list_of_decisions:
        bot.send_message(chat_id=update.message.chat_id, text='Please enter text!')
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text=list_of_decisions[random.randint(0, len(list_of_decisions) - 1)])
