from plugins import new_message, enable_check
from random import randint


# random: number
def random(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/random number`')
        return
    if context.args[0] == 'number':
        if len(context.args) == 1:
            context.bot.send_message(chat_id=update.message.chat_id, text=f'{randint(1, 100)}')
        elif len(context.args) == 3:
            try:
                context.bot.send_message(chat_id=update.message.chat_id, text=f'{randint(int(context.args[1]), int(context.args[2]))}')
            except ValueError:
                context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/random number [range_start] [range_end]`')
        else:
            context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/random number [range_start] [range_end]`')
