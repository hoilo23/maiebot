from plugins import new_message, enable_check


# sends all of the available commands
def send_help(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    all_commands = '''
    Available commands:
    /dogify <your words> - Create a doge image with your words
    /echo <your words> - Echo your message
    /get_id [group] - Get your user id, or the group id.
    /google <keyword(s)> - Return Google search results
    /help - Send this help text
    /isup <url> - Check if a URL is working or not
    /kickme - Kick yourself from the chat
    /magic8ball - magic8Ball
    /plugin - Enable and disable plugins or view all plugins
    /quote [add] - Add or get a random quote
    /random - Generate a random number between 1-100 or the specified range
    /rate <thing> - Rates the thing you specified 
    /setpic - Set the picture you replied to as group avatar
    /tweet <message> - Tweet your message.
    /wheeldecide <option 1> <option 2> - Randomly choose an option
    '''
    context.bot.send_message(chat_id=update.message.chat_id, text=all_commands)
