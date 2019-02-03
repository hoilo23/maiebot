from plugins import new_message
import requests
from bs4 import BeautifulSoup
from telegram import ChatAction


# sends a ddg result with the args as the search q
def search_ddg(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/google <keyword(s)>`')
        return

    # join the list of words into a single string with '+' between every word
    all_keywords = '+'.join(args)

    bot.send_chat_action(update.message.chat_id, ChatAction.TYPING)
    url = f'https://duckduckgo.com/html/?q={all_keywords}'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    image = soup.find('div', class_="result results_links results_links_deep web-result ")
    # split the title, text and url in a list
    image = image.text.splitlines()
    # filter whitespace and empty strings from list
    result = list(filter(None, image))[1:-1]
    try:
        result = f'{result[0]} \n\n{result[1]} \n\n{result[2]}'
    except IndexError:
        bot.send_message(chat_id=update.message.chat_id, text=f'No results found for {all_keywords}')
        return
    bot.send_message(chat_id=update.message.chat_id, text=result)
