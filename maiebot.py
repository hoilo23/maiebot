from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yaml  # used for the config.yaml file
import logging
# import all plugins
from plugins import *


def start_bot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # load config.yaml
    with open('config.yaml', 'r') as f:
        config = yaml.full_load(f)

    api_key = config['TELEGRAM']['API_KEY']

    updater = Updater(token=api_key, use_context=True)
    dispatcher = updater.dispatcher

    # Command Handlers
    dispatcher.add_handler(CommandHandler('dogify', dogify.dogify))
    dispatcher.add_handler(CommandHandler('echo', echo.echo))
    dispatcher.add_handler(CommandHandler('get_id', get_id.get_id))
    dispatcher.add_handler(CommandHandler('google', search_ddg.search_ddg))
    dispatcher.add_handler(CommandHandler('help', send_help.send_help))
    dispatcher.add_handler(CommandHandler('isup', isup.isup))
    dispatcher.add_handler(CommandHandler('kickme', kickme.kickme))
    dispatcher.add_handler(CommandHandler('magic8ball', magic8ball.magic8ball))
    dispatcher.add_handler(CommandHandler('plugin', plugin.plugin))
    dispatcher.add_handler(CommandHandler('quote', quote.quote))
    dispatcher.add_handler(CommandHandler('random', random.random))
    dispatcher.add_handler(CommandHandler('rate', rate.rate))
    dispatcher.add_handler(CommandHandler('setpic', set_group_avatar.set_group_avatar))
    dispatcher.add_handler(CommandHandler('tweet', send_tweet.send_tweet))
    dispatcher.add_handler(CommandHandler('wheeldecide', wheeldecide.wheeldecide))
    dispatcher.add_handler(MessageHandler((Filters.entity('url')), send_media_from_url.send_media_from_url))

    updater.start_polling(clean=True)


if __name__ == '__main__':
    start_bot()
