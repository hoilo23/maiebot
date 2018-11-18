from functools import wraps
import json


# load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

list_of_admins = config['TELEGRAM']['LIST_OF_ADMINS']


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in list_of_admins:
            print(f'Unauthorized access denied for {update.effective_user.id}.')
            bot.send_message(chat_id=update.message.chat_id, text='Permission denied')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
