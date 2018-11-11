from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from telegram.error import BadRequest
import random
import posixpath
import urllib.parse
import requests
import string
from datetime import datetime
from bs4 import BeautifulSoup
import os  # used for os.remove
from functools import wraps
import ftplib  # used for /upload
import json  # used for the config.json file
import logging
import tweepy  # used by /tweet command
import urllib.request

# from plugins import send_help, get_quote, add_quote
from plugins import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

api_key = config['TELEGRAM']['API_KEY']
list_of_admins = config['TELEGRAM']['LIST_OF_ADMINS']

ftp_url = config['FTP']['URL']
ftp_username = config['FTP']['USERNAME']
ftp_password = config['FTP']['PASSWORD']

consumer_key = config['TWITTER']['CONSUMER_KEY']
consumer_secret = config['TWITTER']['CONSUMER_SECRET']
access_token = config['TWITTER']['ACCESS_TOKEN']
access_token_secret = config['TWITTER']['ACCESS_TOKEN_SECRET']


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
dispatcher.add_handler(CommandHandler('upload', upload_file.upload_file))
dispatcher.add_handler(CommandHandler('delete_all_files', delete_all_files.delete_all_files))
dispatcher.add_handler(CommandHandler('isup', isup.isup, pass_args=True))
dispatcher.add_handler(CommandHandler('echo', echo.echo, pass_args=True))
dispatcher.add_handler(CommandHandler('tweet', send_tweet.send_tweet, pass_args=True))
dispatcher.add_handler(CommandHandler('getid', get_id.get_id, pass_args=True))
dispatcher.add_handler(MessageHandler((Filters.entity('url')), send_media_from_url))

updater.start_polling(clean=True)
