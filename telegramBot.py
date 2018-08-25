from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import random
import posixpath
import urllib.parse
import requests
import string
from datetime import datetime
from bs4 import BeautifulSoup
import os
from functools import wraps
from ftplib import FTP
import json


# load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

api_key = config['TELEGRAM']['API_KEY']
list_of_admins = config['TELEGRAM']['LIST_OF_ADMINS']

ftp_url = config['FTP']['URL']
ftp_username = config['FTP']['USERNAME']
ftp_password = config['FTP']['PASSWORD']


updater = Updater(token=api_key)
dispatcher = updater.dispatcher


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in list_of_admins:
            print("Unauthorized access denied for {}.".format(user_id))
            bot.send_message(chat_id=update.message.chat_id, text='Permission denied')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


# sends all of the available commands
def send_help(bot, update):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

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
    '''
    bot.send_message(chat_id=update.message.chat_id, text=all_commands)


send_help_handler = CommandHandler('help', help)
dispatcher.add_handler(send_help_handler)


# opens chat_id.txt and sends a random quote to the chat
def get_quote(bot, update):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    try:
        list_of_quotes = open('./quotes/' + str(update.message.chat_id) + '.txt', 'r', encoding="utf-8")
        quotes = list_of_quotes.readlines()
        quote = quotes[random.randint(0, len(quotes) - 1)]
        bot.send_message(chat_id=update.message.chat_id, text=quote)
        list_of_quotes.close()
    except FileNotFoundError:
        bot.send_message(chat_id=update.message.chat_id, text='No quotes found.')


get_quote_handler = CommandHandler('quote', get_quote)
dispatcher.add_handler(get_quote_handler)


# opens quotes_chat_id.txt and appends the quote
def add_quote(bot, update, args):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    all_words = ''
    list_of_quotes = open('./quotes/' + str(update.message.chat_id) + '.txt', 'a', encoding="utf-8")
    for word in args:
        all_words += word
        all_words += ' '
    if all_words == '':
        bot.send_message(chat_id=update.message.chat_id, text='Please enter a quote!')
    else:
        list_of_quotes.write(all_words)
        list_of_quotes.write('\n')
        bot.send_message(chat_id=update.message.chat_id, text='done!')


add_quote_handler = CommandHandler('addquote', add_quote, pass_args=True)
dispatcher.add_handler(add_quote_handler)


# sends a google URL with the args as the search q
def send_google_url(bot, update, args):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    all_keywords = ''
    for word in args:
        all_keywords += word
        all_keywords += '+'
    if all_keywords == '':
        bot.send_message(chat_id=update.message.chat_id, text='Please enter a search query!')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='https://www.google.com/search?q=' + all_keywords)


send_google_url_handler = CommandHandler('google', send_google_url, pass_args=True)
dispatcher.add_handler(send_google_url_handler)


# sends a random reply from the list
def magic8ball(bot, update):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    answers = ['It is certain', 'It is decidedly so', 'Without a doubt',
               'Yes definitely', 'You may rely on it', 'As I see it, yes',
               'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
               'Reply hazy try again', 'Ask again later',
               'Better not tell you now', 'Cannot predict now',
               'Concentrate and ask again', 'Don\'t count on it',
               'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
    bot.send_message(chat_id=update.message.chat_id, text=answers[random.randint(0, len(answers) - 1)])


magic8ball_handler = CommandHandler('magic8ball', magic8ball)
dispatcher.add_handler(magic8ball_handler)


# sends a random reply from the args
def wheeldecide(bot, update, args):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    list_of_decisions = []
    for word in args:
        list_of_decisions.append(word)
    if not list_of_decisions:
        bot.send_message(chat_id=update.message.chat_id, text='Please enter text!')
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text=list_of_decisions[random.randint(0, len(list_of_decisions) - 1)])


wheeldecide_handler = CommandHandler('wheeldecide', wheeldecide, pass_args=True)
dispatcher.add_handler(wheeldecide_handler)


# dogify
def send_doge_pic(bot, update, args):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    all_words = ''
    for word in args:
        all_words += word
        all_words += ' '
    if all_words == '':
        bot.send_message(chat_id=update.message.chat_id, text='Please enter text!')
    else:
        bot.send_photo(chat_id=update.message.chat_id, photo='http://dogr.io/' + all_words + '.png?split=false&.png')


send_doge_pic_handler = CommandHandler('dogify', send_doge_pic, pass_args=True)
dispatcher.add_handler(send_doge_pic_handler)


# kicks person that executed the command
def kickme(bot, update):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    print(update.message.from_user)
    bot.kick_chat_member(chat_id=update.message.chat_id, user_id=update.message.from_user['id'])


kickme_handler = CommandHandler('kickme', kickme)
dispatcher.add_handler(kickme_handler)


# sets image in reply as group picture
def grouppic(bot, update):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    if update['message']['reply_to_message'] is not None:
        if update['message']['reply_to_message']['photo']:
            photo_update = update['message']['reply_to_message']['photo'][-1]
            profile_pic = bot.get_file(file_id=photo_update['file_id'])
            profile_pic.download('avatar.jpg')
            with open('avatar.jpg', 'rb') as f:
                bot.set_chat_photo(update.message.chat_id, f)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Not a reply to an image!')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Not a reply!')


grouppic_handler = CommandHandler('setpic', grouppic)
dispatcher.add_handler(grouppic_handler)


# Replies to a file with a http link to that same file.
def upload_file(bot, update):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    file_update = update['message']['reply_to_message']['document']

    if file_update is None:
        bot.send_message(chat_id=update.message.chat_id, text='Not a reply to a file!')
        return
    if file_update['file_size'] > 10485760:
        bot.send_message(chat_id=update.message.chat_id, text='File too big, you can only upload files <10MB')
        return

    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=14))
    file_extension = posixpath.splitext(urllib.parse.urlparse(file_update['file_name']).path)[1]

    random_filename = random_string + file_extension

    file = bot.get_file(file_id=file_update['file_id'])
    file.download(random_filename)
    open_file = open(random_filename, 'rb')

    ftp = FTP(ftp_url)
    ftp.login(user=ftp_username, passwd=ftp_password)
    ftp.storbinary('STOR ' + random_filename, open_file)
    open_file.close()
    ftp.quit()

    os.remove(random_filename)

    file_url = 'https://www.' + ftp_url + '/files/' + random_filename
    bot.send_message(chat_id=update.message.chat_id, text='Successfully uploaded your file: ' + file_url)


upload_file_handler = CommandHandler('upload', upload_file)
dispatcher.add_handler(upload_file_handler)


# deletes all of the files in the FTP folder
@restricted
def delete_all_files(bot, update):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    ftp = FTP(ftp_url)
    ftp.login(user=ftp_username, passwd=ftp_password)
    for file in ftp.nlst():
        try:
            ftp.delete(file)
        except:
            continue
    bot.send_message(chat_id=update.message.chat_id, text='Successfully deleted all files')


delete_all_files_handler = CommandHandler('delete_all_files', delete_all_files)
dispatcher.add_handler(delete_all_files_handler)


# isup
def isup(bot, update, args):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

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
                bot.send_message(chat_id=update.message.chat_id, text=url + ' Looks up from here!')
        except requests.exceptions.ConnectionError:
            pass
            bot.send_message(chat_id=update.message.chat_id, text=url + ' Looks down from here, RIP')
    else:  # just check if url is up
        try:
            r = requests.get(url)
            if r.ok:
                bot.send_message(chat_id=update.message.chat_id, text=url + ' Looks up from here!')
        except requests.exceptions.ConnectionError:
            pass
            bot.send_message(chat_id=update.message.chat_id, text=url + ' Looks down from here, RIP')


isup_handler = CommandHandler('isup', isup, pass_args=True)
dispatcher.add_handler(isup_handler)


# echo
def echo(bot, update, args):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    all_words = ''
    if not args:
        bot.send_message(chat_id=update.message.chat_id, text='Please enter some text')
    else:
        for word in args:
            all_words += word
            all_words += ' '
        bot.send_message(chat_id=update.message.chat_id, text=all_words)


echo_handler = CommandHandler('echo', echo, pass_args=True)
dispatcher.add_handler(echo_handler)


# send image as file
def send_media_from_url(bot, update):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ': New message from ' + update.message.from_user.username)
    print('Message text: ' + update.message.text)

    image_extensions = {'.png', '.jpg'}
    document_extensions = {'.gif', '.pdf'}
    video_extensions = {'.mp4'}

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
            url = 'http://rapflame.ddns.net:8080/pf/pf-full.php?user=' + username
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            image = soup.find('img')['src']
            bot.send_photo(chat_id=update.message.chat_id, photo=image)

    # checks every received URL if it is a direct link to a file, and returns the file itself if it is
    # it also changes urls from rapflame.ddns.net:8080 to a proxy URL, because tg can't handle different port numbers...
    if posixpath.splitext(urllib.parse.urlparse(url).path)[1] in image_extensions:
        bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
        if 'rapflame.ddns.net:8080' in url:
            print('URL from rapflame.ddns.net detected...')
            url = list(urllib.parse.urlsplit(url))
            url[1] = 't45.nl/proxy'
            url = urllib.parse.urlunsplit(url)
        bot.send_photo(chat_id=update.message.chat_id, photo=url)
    elif posixpath.splitext(urllib.parse.urlparse(url).path)[1] in document_extensions:
        bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_DOCUMENT)
        bot.send_document(chat_id=update.message.chat_id, document=url)
    elif posixpath.splitext(urllib.parse.urlparse(url).path)[1] in video_extensions:
        bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_VIDEO)
        if 'rapflame.ddns.net:8080' in url:
            print('URL from rapflame.ddns.net detected...')
            url = list(urllib.parse.urlsplit(url))
            url[1] = 't45.nl/proxy'
            url = urllib.parse.urlunsplit(url)
        bot.send_video(chat_id=update.message.chat_id, video=url)


send_media_from_url_handler = MessageHandler((Filters.entity("url")), send_media_from_url)
dispatcher.add_handler(send_media_from_url_handler)

updater.start_polling()