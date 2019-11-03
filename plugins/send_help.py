from plugins import new_message, enable_check


# sends all of the available commands
def send_help(bot, update):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    all_commands = '''
    Available commands:
    /help - Show this help text
    /quote - Send a random quote
    /addquote - Add a new quote
    /google - Returns Google search results
    /magic8ball - magic8Ball
    /wheeldecide - Randomly choose an option
    /dogify - Create a doge image with your words
    /kickme - Kick you from the chat
    /setpic - Set the picture you replied to as group avatar
    /isup - Checks if a URL is working or not
    /echo - Echoes your message
    /tweet - Tweet your message
    /getid [group] - Get your user id, or the groups id
    /rate - Lets you rate something.
    /plugin - Enable and disable plugins or view all plugins
    '''
    bot.send_message(chat_id=update.message.chat_id, text=all_commands)
