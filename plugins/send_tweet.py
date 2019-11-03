from plugins import new_message, restricted, enable_check
import tweepy
import json


# load config.json
with open('config.json', 'r') as f:
    config = json.load(f)
#  todo check if these are actually in config.json
username = config['TWITTER']['USERNAME']
consumer_key = config['TWITTER']['CONSUMER_KEY']
consumer_secret = config['TWITTER']['CONSUMER_SECRET']
access_token = config['TWITTER']['ACCESS_TOKEN']
access_token_secret = config['TWITTER']['ACCESS_TOKEN_SECRET']


# sends args as tweet
@restricted.restricted  # restricted to admins only, could be abused.
def send_tweet(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not args:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/tweet <your tweet>`')
        return

    # join the list of words into a single string
    all_words = ' '.join(args)

    if len(all_words) > 280:
        bot.send_message(chat_id=update.message.chat_id, text='Can\'t send tweet, because it is longer than 280 characters')
        return

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweet = api.update_status(status=all_words)

    bot.send_message(chat_id=update.message.chat_id, text=f'Tweet send: https://twitter.com/statuses/{tweet.id}')  # todo url might not always work?
