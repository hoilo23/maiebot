from plugins import new_message, enable_check
import random


# sends a random reply from the list
def magic8ball(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    answers = ['It is certain', 'It is decidedly so', 'Without a doubt',
               'Yes definitely', 'You may rely on it', 'As I see it, yes',
               'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
               'Reply hazy try again', 'Ask again later',
               'Better not tell you now', 'Cannot predict now',
               'Concentrate and ask again', 'Don\'t count on it',
               'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
    context.bot.send_message(chat_id=update.message.chat_id, text=answers[random.randint(0, len(answers) - 1)])
