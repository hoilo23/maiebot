from plugins import new_message
import requests

api_url = 'http://rapflame.ddns.net:8080/api'


# sends an image from the above api.
def send_ig_post(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not args:
        r = requests.get(api_url)
        api = r.json()

        url = api['message']
        caption = api['caption']
        user = api['user']

        if url[-4:] == '.jpg':
            bot.send_photo(chat_id=update.message.chat_id, photo=url, caption=f"{caption} \n*By {user}*", parse_mode='markdown')
        else:
            bot.send_video(chat_id=update.message.chat_id, video=url, caption=f"{caption} \n*By {user}*", parse_mode='markdown')
