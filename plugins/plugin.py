from plugins import new_message, restricted
import json

# todo: some plugins have different names than their commands, fix this
# used to enable and disable plugins
@restricted.restricted
def plugin(bot, update, args):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not args:
        bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/plugin list | enable <plugin name> | disable <plugin name>`')
        return

    # load config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    if args[0] == 'list':
        plugin_list = ''
        for plugins in config['PLUGINS']:
            if config['PLUGINS'][plugins] == 'ENABLED':
                plugins = '✅    ' + plugins + '\n'
            else:
                plugins = '❌    ' + plugins + '\n'
            plugin_list += plugins
        bot.send_message(chat_id=update.message.chat_id, text=plugin_list)
    if args[0] == 'enable':
        if not args[1]:
            bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown',
                             text='Usage: `/plugin enable <plugin name>`')
        if args[1] in config['PLUGINS']:
            if config['PLUGINS'][args[1]] != "ENABLED":
                config['PLUGINS'][args[1]] = "ENABLED"
                bot.send_message(chat_id=update.message.chat_id, text=f'{args[1]} has been enabled.')
            else:
                bot.send_message(chat_id=update.message.chat_id, text=f'{args[1]} has already been enabled.')
        else:
            bot.send_message(chat_id=update.message.chat_id, text=f'Can\'t find a plugin named "{args[1]}"')
    if args[0] == 'disable':
        if not args[1]:
            bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown',
                             text='Usage: `/plugin disable <plugin name>`')
        if args[1] in config['PLUGINS']:
            if config['PLUGINS'][args[1]] != "DISABLED":
                config['PLUGINS'][args[1]] = "DISABLED"
                bot.send_message(chat_id=update.message.chat_id, text=f'{args[1]} has been disabled.')
            else:
                bot.send_message(chat_id=update.message.chat_id, text=f'{args[1]} has already been disabled.')
        else:
            bot.send_message(chat_id=update.message.chat_id, text=f'Can\'t find a plugin named "{args[1]}"')

    # load config.json todo fixed bug with extra } at end of file, clean up this code
    with open('config.json', 'w') as f:
        # f.seek(0)
        json.dump(config, f, indent=4)
