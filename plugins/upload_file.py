from plugins import new_message, restricted
import random
from telegram import ChatAction
import ftplib  # used for /upload
import posixpath
import urllib.parse
import string
import os
import json


# load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

ftp_url = config['FTP']['URL']
ftp_username = config['FTP']['USERNAME']
ftp_password = config['FTP']['PASSWORD']


# Replies to a file with a http link to that same file.
@restricted.restricted
def upload_file(bot, update):
    new_message.new_message(update.message.from_user.username, update.message.text)

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
