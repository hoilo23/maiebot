from plugins import new_message, enable_check
import requests


# check if url is up or not
def isup(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not context.args or len(context.args) > 1:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/isup <url>`')
        return
    else:
        url = context.args[0]
    if 'https://' not in url and 'http://' not in url:  # if no http(s) in url, add it, and check if url is up
        url = 'http://' + url  # add http to url
    try:
        r = requests.get(url)
        if r.ok:
            context.bot.send_message(chat_id=update.message.chat_id, text=f'{url} Looks up from here!')
    except requests.exceptions.ConnectionError:
        context.bot.send_message(chat_id=update.message.chat_id, text=f'{url} Looks down from here, RIP')
