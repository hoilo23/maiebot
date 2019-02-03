# the list of currently used plugins # don't forget to add new plugins here
plugin_list = ['add_quote', 'dogify', 'echo', 'get_id', 'get_quote', 'isup', 'kickme', 'magic8ball',
               'new_message', 'restricted', 'search_ddg', 'send_help', 'send_media_from_url', 'send_tweet',
               'set_group_avatar', 'wheeldecide', 'rate']

plugins = '\n'.join(plugin_list)
print(f"Currently installed plugins: \n{plugins}")


__all__ = plugin_list
