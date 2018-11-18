from plugins import new_message


# sends all of the available commands
def send_help(bot, update):
    new_message.new_message(update.message.from_user.username, update.message.text)

    all_commands = '''
    Available commands:
    /quote - Send a random quote
    /addquote - Add a new quote
    /google - Send a google url
    /magic8ball - magic8Ball
    /wheeldecide - Randomly choose an option
    /dogify - Create a doge image with your words
    /kickme - Kick you from the chat
    /setpic - Set the picture you replied to as group avatar
    /upload - Uploads the file you replied to, and returns the URL
    /delete_all_files - Deletes all of the uploaded files in the FTP.
    /isup - Checks if a URL is working or not
    /echo - Echoes your message
    /tweet - Tweet your message.
    /getid [group] - Get your user id, or the groups id.
    /rate - Lets you rate something. 
    '''
    bot.send_message(chat_id=update.message.chat_id, text=all_commands)
