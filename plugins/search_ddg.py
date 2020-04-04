from plugins import new_message, enable_check
import requests
from bs4 import BeautifulSoup
from telegram import ChatAction


# sends a ddg result with the args as the search q
def search_ddg(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/google <keyword(s)>`')
        return

    # join the list of words into a single string with '+' between every word
    all_keywords = '+'.join(context.args)

    context.bot.send_chat_action(update.message.chat_id, ChatAction.TYPING)
    url = f'https://duckduckgo.com/html/?q={all_keywords}'
    # added user agent so we get blocked less often. it might still happen though
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'lxml')
    image = soup.find('div', class_="result results_links results_links_deep web-result ")
    # split the title, text and url in a list
    image = image.text.splitlines()
    # filter whitespace and empty strings from list
    result = list(filter(None, image))[1:-1]
    try:
        result = f'{result[0]} \n\n{result[1]} \n\n{result[2]}'
    except IndexError:  # todo this doesn't work, error at line 28 with AttributeError: NoneType has no attribute 'text'
        context.bot.send_message(chat_id=update.message.chat_id, text=f'No results found for {all_keywords}')
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=result)
