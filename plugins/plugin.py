from plugins import new_message, restricted
import yaml


# used to enable and disable plugins
@restricted.restricted
def plugin(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown',
                                 text='Usage: `/plugin list | enable <plugin name> | disable <plugin name>`')
        return

    def switch_state(args, desired_state):
        if not args[1]:
            context.bot.send_message(chat_id=update.message.chat_id, parse_mode='markdown', text='Usage: `/plugin disable <plugin name>`')
        if context.args[1] in config['PLUGINS']:
            if config['PLUGINS'][args[1]] != desired_state:
                config['PLUGINS'][args[1]] = desired_state
                context.bot.send_message(chat_id=update.message.chat_id, text=f'{args[1]} has been {args[0]}d.')
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text=f'{args[1]} has already been {args[0]}d.')
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=f'Can\'t find a plugin named "{args[1]}"')

    # load config.yaml
    with open('config.yaml', 'r+') as f:
        config = yaml.full_load(f)

        if context.args[0] == 'list':
            plugin_list = ['✅    ' + plugins + '\n' if config['PLUGINS'][plugins] else '❌    ' + plugins + '\n' for plugins in config['PLUGINS']]
            context.bot.send_message(chat_id=update.message.chat_id, text="".join(plugin_list))
        if context.args[0] == 'enable':
            switch_state(context.args, True)
        if context.args[0] == 'disable':
            switch_state(context.args, False)
        f.seek(0)
        yaml.dump(config, f)
