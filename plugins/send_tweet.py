from plugins import new_message
import tweepy
import json


# load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

username = config['TWITTER']['USERNAME']
consumer_key = config['TWITTER']['CONSUMER_KEY']
consumer_secret = config['TWITTER']['CONSUMER_SECRET']
access_token = config['TWITTER']['ACCESS_TOKEN']
access_token_secret = config['TWITTER']['ACCESS_TOKEN_SECRET']


# sends args as tweet
def send_tweet(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, text='Please enter some text to tweet')
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

    bot.send_message(chat_id=update.message.chat_id, text=f'Tweet send: https://twitter.com/statuses/{tweet.id}')
