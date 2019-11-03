import os
import json

# the list of currently used plugins
if os.path.isfile('./config.json'):
    dir_list = os.listdir("plugins")
    plugin_list = []
    # load config.json
    with open('config.json', 'r+') as f:
        config = json.load(f)

        try:  # todo clean up
            if not config['PLUGINS']:
                config['PLUGINS'] = []
        except KeyError:
            config['PLUGINS'] = {}

        for file_name in dir_list:
            if file_name[0] != "_":
                plugin_list.append(file_name[:-3])
                # if plugin not already in config.json, add it there
                # we don't want to make it possible to disable the 'new message', 'restricted', and 'plugin' plugins
                if file_name[:-3] not in config['PLUGINS'] and file_name[:-3] != 'new_message' and file_name[:-3] != 'restricted' and file_name[:-3] != 'plugin':
                    config['PLUGINS'][file_name[:-3]] = "ENABLED"
        f.seek(0)
        json.dump(config, f, indent=4)
    plugins = '\n'.join(plugin_list)
    print(f"Currently installed plugins ({len(plugin_list)})): \n{plugins}")

    __all__ = plugin_list
else:
    print("No config.json file found, make sure to add your info to config.json.example and rename it to config.json")
    quit()

