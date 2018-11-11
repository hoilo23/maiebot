from plugins import new_message
import requests


# isup
def isup(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, text='Please enter a URL to check')
        return
    else:
        if len(args) > 1:
            bot.send_message(chat_id=update.message.chat_id, text='Please enter a valid URL')
            return
        url = args[0]
    if 'https://' not in url and 'http://' not in url:  # if no http(s) in url, add it, and check if url is up
        url = 'http://' + url  # add http to url
        try:
            r = requests.get(url)
            if r.ok:
                bot.send_message(chat_id=update.message.chat_id, text=f'{url} Looks up from here!')
        except requests.exceptions.ConnectionError:
            pass
            bot.send_message(chat_id=update.message.chat_id, text=f'{url} Looks down from here, RIP')
    else:  # just check if url is up
        try:
            r = requests.get(url)
            if r.ok:
                bot.send_message(chat_id=update.message.chat_id, text=f'{url} Looks up from here!')
        except requests.exceptions.ConnectionError:
            pass
            bot.send_message(chat_id=update.message.chat_id, text=f'{url} Looks down from here, RIP')
