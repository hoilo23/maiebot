import os

# the list of currently used plugins
if os.path.isfile('./config.json'):
    dir_list = os.listdir("plugins")
    plugin_list = []
    for file_name in dir_list:
        if file_name[0] != "_":
            plugin_list.append(file_name[:-3])

    plugins = '\n'.join(plugin_list)
    print(f"Currently installed plugins: \n{plugins}")

    __all__ = plugin_list
else:
    print("No config.json file found, make sure to add your info to config.json.example and rename it to config.json")
    quit()

