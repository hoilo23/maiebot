from plugins import new_message
import random


# generates a random rating for the args
def rate(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/rate [thing]`')
    else:
        ratings = [", I'd say that this horribly sucks and gets what it deserves : a 0/10.",
                   ", I'd say that this horribly sucks and gets what it deserves : a 1/10.",
                   ", I'd say that this is bad and only deserves a 2/10.",
                   ", I'd say that this is bad and only deserves a 3/10.",
                   ", I'd say that this is quite average and can be rated something like 4/10.",
                   ", I'd say that this is quite average and can be rated something like 5/10.",
                   ", I'd say that this is quite good and should get a 6/10.",
                   ", I'd say that this is quite good and should get a 7/10.",
                   ", I'd say that this is (relatively) incredible and deserves a 8/10.",
                   ", I'd say that this is (relatively) incredible and deserves a 9/10.",
                   ", I'd say that this is incredibly awesome and should get the perfect score : 10/10."]

        rating = ratings[random.randint(0, 10)]
        bot.send_message(chat_id=update.message.chat_id, text=f'{update.message.from_user.username}{rating}')
