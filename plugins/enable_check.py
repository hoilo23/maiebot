import json


# check if a plugin is enabled before allowing it to run
def enable_check(plugin):
    with open('config.json', 'r') as f:
        config = json.load(f)
        # remove first 8 character from plugin name ("plugins.")
        return config['PLUGINS'][plugin[8:]] == "DISABLED"
