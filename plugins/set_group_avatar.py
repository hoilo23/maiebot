from plugins import new_message, enable_check
from telegram.error import BadRequest
import os


# sets image in reply as group picture
def set_group_avatar(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    if not update['message']['reply_to_message'] or not update['message']['reply_to_message']['photo']:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/setpic (as a reply to an image)`')
        return

    photo_update = update['message']['reply_to_message']['photo'][-1]
    profile_pic = context.bot.get_file(file_id=photo_update['file_id'])
    profile_pic.download('avatar.jpg')
    with open('avatar.jpg', 'rb') as file:
        try:
            context.bot.set_chat_photo(update.message.chat_id, file)
        except BadRequest:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text='Either I don\'t have permission to change the avatar, or we\'re not currently chatting in a group.')
    os.remove('avatar.jpg')
