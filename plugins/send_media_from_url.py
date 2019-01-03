from plugins import new_message
from telegram import ChatAction
from telegram.error import BadRequest
import posixpath
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import requests
import os
import json

# load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

api_key = config['TELEGRAM']['API_KEY']


# send image as file
def send_media_from_url(bot, update):
    new_message.new_message(update.message.from_user.username, update.message.text)

    image_extensions = {'.png', '.jpg'}
    document_extensions = {'.gif', '.pdf', '.zip'}
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
            url = f'http://rapflame.ddns.net:8080/api/ava.php?user={username}'
            print(username)
            r = requests.get(url)
            api = r.json()
            image = api['url']
            bot.send_photo(chat_id=update.message.chat_id, photo=image)

    # checks t45 url and send the image
    elif 'https://t45.nl/image/?id=' in url:
        img_name = url[-6:]
        if img_name != '':
            bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
            image = f'https://t45.nl/3/{img_name}.png'
            bot.send_photo(chat_id=update.message.chat_id, photo=image)

    # checks every received URL if it is a direct link to a file, and returns the file itself if it is
    if posixpath.splitext(urllib.parse.urlparse(url).path)[1] in image_extensions:
        bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
        try:
            urllib.request.urlretrieve(url, "downloaded_photo.jpg")
            with open('downloaded_photo.jpg', 'rb') as downloaded_photo:
                files = {'photo': downloaded_photo}
                params = {'chat_id': update.message.chat_id}
                api_url = f'https://api.telegram.org/bot{api_key}/sendPhoto'
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
                api_url = f'https://api.telegram.org/bot{api_key}/sendVideo'
                requests.post(api_url, files=files, params=params)
            os.remove('downloaded_video.mp4')
        except BadRequest:
            bot.send_video(chat_id=update.message.chat_id, video=url)
