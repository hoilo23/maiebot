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


def new_message(message_from_user, message_text):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}: New message from {message_from_user}')
    print(f'Message text: {message_text}')


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in list_of_admins:
            print(f'Unauthorized access denied for {update.effective_user.id}.')
            bot.send_message(chat_id=update.message.chat_id, text='Permission denied')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


# sends all of the available commands
def send_help(bot, update):
    new_message(update.message.from_user.username, update.message.text)

    all_commands = '''
    Available commands:
    /quote - Send a random quote
    /addquote - Add a new quote
    /google - Send a google url
    /magic8ball - magic8Ball
    /wheeldecide - Randomly choose an option
    /dogify - Create a doge image with your words
    /kickme - Kick you from the chat
    /setpic - Set the picture you replied to as group avatar
    /upload - Uploads the file you replied to, and returns the URL
    /delete_all_files - Deletes all of the uploaded files in the FTP.
    /isup - Checks if a URL is working or not
    /echo - Echoes your message
    /tweet - Tweet your message.
    /getid [group] - Get your user id, or the groups id.
    '''
    bot.send_message(chat_id=update.message.chat_id, text=all_commands)


# opens chat_id.txt and sends a random quote to the chat
def get_quote(bot, update):
    new_message(update.message.from_user.username, update.message.text)

    try:
        with open(f'./quotes/{update.message.chat_id}.txt', 'r', encoding='utf-8') as list_of_quotes:
            quotes = list_of_quotes.readlines()
            quote = quotes[random.randint(0, len(quotes) - 1)]
            bot.send_message(chat_id=update.message.chat_id, text=quote)
    except FileNotFoundError:
        bot.send_message(chat_id=update.message.chat_id, text='No quotes found.')


# opens quotes_chat_id.txt and appends the quote
def add_quote(bot, update, args):
    new_message(update.message.from_user.username, update.message.text)

    with open(f'./quotes/{update.message.chat_id}.txt', 'a', encoding='utf-8') as list_of_quotes:
        # join the list of words into a single string
        all_words = ' '.join(args)
        if all_words == '':
            bot.send_message(chat_id=update.message.chat_id, text='Please enter a quote!')
        else:
            list_of_quotes.write(f'{all_words} \n')
            bot.send_message(chat_id=update.message.chat_id, text='done!')


# sends the current group chat id or the users id
def getid(bot, update, args):
    new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, text=update.message.from_user.id)
        return
    if args[0] == 'group':
        bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)


# sends args as tweet
def send_tweet(bot, update, args):
    new_message(update.message.from_user.username, update.message.text)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # join the list of words into a single string
    all_words = ' '.join(args)

    api.update_status(status=all_words)

    bot.send_message(chat_id=update.message.chat_id, text='Tweet send: https://twitter.com/GertKwarckman')


# sends a ddg result with the args as the search q
def search_ddg(bot, update, args):
    new_message(update.message.from_user.username, update.message.text)

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


# sends a random reply from the list
def magic8ball(bot, update):
    new_message(update.message.from_user.username, update.message.text)

    answers = ['It is certain', 'It is decidedly so', 'Without a doubt',
               'Yes definitely', 'You may rely on it', 'As I see it, yes',
               'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
               'Reply hazy try again', 'Ask again later',
               'Better not tell you now', 'Cannot predict now',
               'Concentrate and ask again', 'Don\'t count on it',
               'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
    bot.send_message(chat_id=update.message.chat_id, text=answers[random.randint(0, len(answers) - 1)])


# sends a random reply from the args
def wheeldecide(bot, update, args):
    new_message(update.message.from_user.username, update.message.text)

    list_of_decisions = [word for word in args]

    if not list_of_decisions:
        bot.send_message(chat_id=update.message.chat_id, text='Please enter text!')
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text=list_of_decisions[random.randint(0, len(list_of_decisions) - 1)])


# dogify
def send_doge_pic(bot, update, args):
    new_message(update.message.from_user.username, update.message.text)

    # join the list of words into a single string
    all_words = ' '.join(args)
    if all_words == '':
        bot.send_message(chat_id=update.message.chat_id, text='Please enter text!')
    else:
        bot.send_photo(chat_id=update.message.chat_id, photo=f'http://dogr.io/{all_words}.png?split=false&.png')


# kicks person that executed the command
def kickme(bot, update):
    new_message(update.message.from_user.username, update.message.text)

    bot.kick_chat_member(chat_id=update.message.chat_id, user_id=update.message.from_user['id'])


# sets image in reply as group picture
def grouppic(bot, update):
    new_message(update.message.from_user.username, update.message.text)

    if update['message']['reply_to_message'] is None:
        bot.send_message(chat_id=update.message.chat_id, text='Not a reply!')
        return
    if not update['message']['reply_to_message']['photo']:
        bot.send_message(chat_id=update.message.chat_id, text='Not a reply to an image!')
        return

    photo_update = update['message']['reply_to_message']['photo'][-1]
    profile_pic = bot.get_file(file_id=photo_update['file_id'])
    profile_pic.download('avatar.jpg')
    with open('avatar.jpg', 'rb') as file:
        bot.set_chat_photo(update.message.chat_id, file)


# Replies to a file with a http link to that same file.
@restricted
def upload_file(bot, update):
    new_message(update.message.from_user.username, update.message.text)

    if not update['message']['reply_to_message']:
        bot.send_message(chat_id=update.message.chat_id, text='Please reply to a file.')
        return

    document_update = update['message']['reply_to_message']['document']
    video_update = update['message']['reply_to_message']['video']
    photo_update = update['message']['reply_to_message']['photo']
    audio_update = update['message']['reply_to_message']['audio']

    if document_update:
        file_update = document_update
    elif video_update:
        file_update = video_update
    elif photo_update:
        file_update = photo_update[-1]  # [-1] so it always uses the biggest photo available
    elif audio_update:
        file_update = audio_update
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Please reply to a file.')
        return

    if not file_update:
        bot.send_message(chat_id=update.message.chat_id, text='Please reply to a file, photo, or video.')
        return
    if file_update['file_size'] > 20971520:
        bot.send_message(chat_id=update.message.chat_id, text='File too big, you can only upload files <20MiB')
        return

    def bot_get_file():
        file = bot.get_file(file_id=file_update['file_id'])
        return file.download()

    file_name = bot_get_file()
    bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_DOCUMENT)
    open_file = open(file_name, 'rb')

    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=14))
    file_extension = posixpath.splitext(urllib.parse.urlparse(file_name).path)[1]

    random_filename = random_string + file_extension

    ftp = ftplib.FTP(ftp_url)
    ftp.login(user=ftp_username, passwd=ftp_password)
    ftp.storbinary(f'STOR {random_filename}', open_file)
    open_file.close()
    ftp.quit()

    os.remove(file_name)

    file_url = f'https://files.{ftp_url}/{random_filename}'
    bot.send_message(chat_id=update.message.chat_id, text=f'Successfully uploaded your file: {file_url}')


# deletes all of the files in the FTP folder
@restricted
def delete_all_files(bot, update):
    new_message(update.message.from_user.username, update.message.text)

    ftp = ftplib.FTP(ftp_url)
    ftp.login(user=ftp_username, passwd=ftp_password)

    list_of_files = ftp.nlst()[3:]  # delete first 3 entries from list ('.', '..', and '.htaccess')

    if not list_of_files:
        bot.send_message(chat_id=update.message.chat_id, text='Folder is already empty')
        return

    for file in list_of_files:
        try:
            ftp.delete(file)
        except ftplib.error_perm:
            continue

    bot.send_message(chat_id=update.message.chat_id, text='Successfully deleted all files')


# isup
def isup(bot, update, args):
    new_message(update.message.from_user.username, update.message.text)

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


# echo
def echo(bot, update, args):
    new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, text='Please enter some text')
    else:
        # join the list of words into a single string
        all_words = ' '.join(args)
        bot.send_message(chat_id=update.message.chat_id, text=all_words)


# send image as file
def send_media_from_url(bot, update):
    new_message(update.message.from_user.username, update.message.text)

    image_extensions = {'.png', '.jpg'}
    document_extensions = {'.gif', '.pdf'}
    video_extensions = {'.mp4', '.mov'}

    msgent = update['message']['entities'][0]
    msgoffset = msgent['offset']
    msglength = msgent['length']
    url = update['message']['text']
    url = url[int(msgoffset):]
    url = url[:int(msglength)]

    # checks for Instagram post and send the full res image
    if 'https://www.instagram.com/p/' in url:
        bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
        bot.send_photo(chat_id=update.message.chat_id, photo=url)

    # checks Instagram username and sends full res avatar
    elif 'https://www.instagram.com' in url:
        username = posixpath.splitext(urllib.parse.urlparse(url).path)[0].replace('/', '')
        if username != '':
            bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
            url = f'http://rapflame.ddns.net:8080/pf/pf-full.php?user={username}'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            image = soup.find('img')['src']
            bot.send_photo(chat_id=update.message.chat_id, photo=image)

    # checks every received URL if it is a direct link to a file, and returns the file itself if it is
    # it also changes urls from rapflame.ddns.net:8080 to a proxy URL, because tg can't handle different port numbers...
    if posixpath.splitext(urllib.parse.urlparse(url).path)[1] in image_extensions:
        bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
        try:
            urllib.request.urlretrieve(url, "downloaded_photo.jpg")
            with open('downloaded_photo.jpg', 'rb') as downloaded_photo:
                files = {'photo': downloaded_photo}
                params = {'chat_id': update.message.chat_id}
                api_url = 'https://api.telegram.org/bot585735982:AAHYbhmYD50QiHfBSZTaCeQVpiNJxmmgiok/sendPhoto'
                requests.post(api_url, files=files, params=params)
            os.remove('downloaded_photo.jpg')
        except BadRequest:
            bot.send_photo(chat_id=update.message.chat_id, photo=url)
    elif posixpath.splitext(urllib.parse.urlparse(url).path)[1] in document_extensions:
        bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_DOCUMENT)
        bot.send_document(chat_id=update.message.chat_id, document=url)
    elif posixpath.splitext(urllib.parse.urlparse(url).path)[1] in video_extensions:
        bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_VIDEO)
        try:
            urllib.request.urlretrieve(url, "downloaded_video.mp4")
            with open('downloaded_video.mp4', 'rb') as downloaded_video:
                files = {'video': downloaded_video}
                params = {'chat_id': update.message.chat_id}
                api_url = 'https://api.telegram.org/bot585735982:AAHYbhmYD50QiHfBSZTaCeQVpiNJxmmgiok/sendVideo'
                requests.post(api_url, files=files, params=params)
            os.remove('downloaded_video.mp4')
        except BadRequest:
            bot.send_video(chat_id=update.message.chat_id, video=url)


# Command Handlers
dispatcher.add_handler(CommandHandler('help', send_help))
dispatcher.add_handler(CommandHandler('quote', get_quote))
dispatcher.add_handler(CommandHandler('addquote', add_quote, pass_args=True))
dispatcher.add_handler(CommandHandler('google', search_ddg, pass_args=True))
dispatcher.add_handler(CommandHandler('magic8ball', magic8ball))
dispatcher.add_handler(CommandHandler('wheeldecide', wheeldecide, pass_args=True))
dispatcher.add_handler(CommandHandler('dogify', send_doge_pic, pass_args=True))
dispatcher.add_handler(CommandHandler('kickme', kickme))
dispatcher.add_handler(CommandHandler('setpic', grouppic))
dispatcher.add_handler(CommandHandler('upload', upload_file))
dispatcher.add_handler(CommandHandler('delete_all_files', delete_all_files))
dispatcher.add_handler(CommandHandler('isup', isup, pass_args=True))
dispatcher.add_handler(CommandHandler('echo', echo, pass_args=True))
dispatcher.add_handler(CommandHandler('tweet', send_tweet, pass_args=True))
dispatcher.add_handler(CommandHandler('getid', getid, pass_args=True))
dispatcher.add_handler(MessageHandler((Filters.entity('url')), send_media_from_url))


updater.start_polling(clean=True)
