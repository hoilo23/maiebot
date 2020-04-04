from functools import wraps
import yaml


# load config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)

list_of_admins = config['TELEGRAM']['LIST_OF_ADMINS']


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in list_of_admins:
            print(f'Unauthorized access denied for {update.effective_user.id}.')
            context.bot.send_message(chat_id=update.message.chat_id, text='Permission denied')
            return
        return func(update, context, *args, **kwargs)
    return wrapped
