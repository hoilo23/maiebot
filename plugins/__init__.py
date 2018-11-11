import os

file_list = [f for f in os.listdir("plugins") if os.path.isfile(f)]
file_list = file_list[:-1]


plugin_list = []
for item in file_list:
    item = item[:-3]
    plugin_list.append(item)


plugin_list = ['add_quote', 'delete_all_files', 'dogify', 'echo', 'get_id', 'get_quote', 'isup', 'kickme', 'magic8ball',
               'new_message', 'restricted', 'search_ddg', 'send_help', 'send_media_from_url', 'send_tweet',
               'set_group_avatar', 'upload_file', 'wheeldecide']

plugins = '\n'.join(plugin_list)
print(f"Currently installed plugins: \n{plugins}")


__all__ = plugin_list
