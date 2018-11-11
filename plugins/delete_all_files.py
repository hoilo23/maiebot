from plugins import new_message, restricted
import json
import ftplib


# load config.json
with open('config.json', 'r') as f:
    config = json.load(f)

ftp_url = config['FTP']['URL']
ftp_username = config['FTP']['USERNAME']
ftp_password = config['FTP']['PASSWORD']


# deletes all of the files in the FTP folder
@restricted.restricted
def delete_all_files(bot, update):
    new_message.new_message(update.message.from_user.username, update.message.text)

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
