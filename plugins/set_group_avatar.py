from plugins import new_message, enable_check
import os


# sets image in reply as group picture
def set_group_avatar(bot, update):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if update['message']['reply_to_message'] is None:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/setpic (as a reply to an image)`')
        return
    if not update['message']['reply_to_message']['photo']:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/setpic (as a reply to an image)`')
        return

    photo_update = update['message']['reply_to_message']['photo'][-1]
    profile_pic = bot.get_file(file_id=photo_update['file_id'])
    profile_pic.download('avatar.jpg')
    with open('avatar.jpg', 'rb') as file:
        try:
            bot.set_chat_photo(update.message.chat_id, file)
        except:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Either you don\'t have permission to change the avatar, '
                                  'or you\'re not currently chatting in a group.')
    os.remove('avatar.jpg')
