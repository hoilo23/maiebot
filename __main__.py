from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json  # used for the config.json file
import logging
# import all plugins
from plugins import *


def start_bot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # load config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    api_key = config['TELEGRAM']['API_KEY']

    updater = Updater(token=api_key)
    dispatcher = updater.dispatcher

    # Command Handlers
    dispatcher.add_handler(CommandHandler('help', send_help.send_help))
    dispatcher.add_handler(CommandHandler('quote', get_quote.get_quote))
    dispatcher.add_handler(CommandHandler('addquote', add_quote.add_quote, pass_args=True))
    dispatcher.add_handler(CommandHandler('google', search_ddg.search_ddg, pass_args=True))
    dispatcher.add_handler(CommandHandler('magic8ball', magic8ball.magic8ball))
    dispatcher.add_handler(CommandHandler('wheeldecide', wheeldecide.wheeldecide, pass_args=True))
    dispatcher.add_handler(CommandHandler('dogify', dogify.dogify, pass_args=True))
    dispatcher.add_handler(CommandHandler('kickme', kickme.kickme))
    dispatcher.add_handler(CommandHandler('setpic', set_group_avatar.set_group_avatar))
    dispatcher.add_handler(CommandHandler('isup', isup.isup, pass_args=True))
    dispatcher.add_handler(CommandHandler('echo', echo.echo, pass_args=True))
    dispatcher.add_handler(CommandHandler('tweet', send_tweet.send_tweet, pass_args=True))
    dispatcher.add_handler(CommandHandler('getid', get_id.get_id, pass_args=True))
    dispatcher.add_handler(CommandHandler('rate', rate.rate, pass_args=True))
    dispatcher.add_handler(MessageHandler((Filters.entity('url')), send_media_from_url.send_media_from_url))

    updater.start_polling(clean=True)


if __name__ == '__main__':
    start_bot()
