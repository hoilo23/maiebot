from plugins import new_message
import requests


# sends an image from the above api.
def send_ig_post(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    api_url = 'http://rapflame.ddns.net:8080/api'

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
    else:
        user = args[0]
        try:
            amount_of_posts = args[1]
        except IndexError:
            amount_of_posts = 1

        try:
            api_url = api_url + f'/user.php?user={user}&limit={amount_of_posts}'
            r = requests.get(api_url)
            api = r.json()

            for idx, posts in enumerate(api):
                url = api[str(idx)]['message']
                caption = api[str(idx)]['caption']
                if url[-4:] == '.jpg':
                    bot.send_photo(chat_id=update.message.chat_id, photo=url, caption=f"{caption} \n*By {user}*", parse_mode='markdown')
                else:
                    bot.send_video(chat_id=update.message.chat_id, video=url, caption=f"{caption} \n*By {user}*", parse_mode='markdown')
        except:
            bot.send_message(chat_id=update.message.chat_id, text='Error')
