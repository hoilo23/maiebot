from plugins import new_message, restricted, enable_check
import tweepy
import yaml


# load config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)
#  todo check if these are actually in config.yaml
username = config['TWITTER']['USERNAME']
consumer_key = config['TWITTER']['CONSUMER_KEY']
consumer_secret = config['TWITTER']['CONSUMER_SECRET']
access_token = config['TWITTER']['ACCESS_TOKEN']
access_token_secret = config['TWITTER']['ACCESS_TOKEN_SECRET']


# sends args as tweet
@restricted.restricted
def send_tweet(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/tweet <your tweet>`')
        return

    # join the list of words into a single string
    tweet_text = ' '.join(context.args)

    if len(tweet_text) > 280:
        context.bot.send_message(chat_id=update.message.chat_id, text='Can\'t send tweet, because it is longer than 280 characters')
        return

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweet = api.update_status(status=tweet_text)

    context.bot.send_message(chat_id=update.message.chat_id, text=f'Tweet send: https://twitter.com/statuses/{tweet.id}')  # todo url might not always work?
