from datetime import datetime


def new_message(message_from_user, message_text):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}: New message from {message_from_user}')
    print(f'Message text: {message_text}')
