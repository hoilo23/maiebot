# maiebot

A telegram bot built using python-telegram-bot, made to replace [yagop telegram bot](https://github.com/yagop/telegram-bot), which is unmaintained/deprecated.


Plugins
------------

Currently supported plugins and their usage:
 
 Plugin | Description | Usage
 ------ | ------------| -----
 dogify.py | Creates a doge image with the supplied words | `/dogify <your words>`
 echo.py | Echoes your words | `/echo <your words>`
 get_id.py | Returns your ID or the id of the group | `/get_id [group]`
 search_ddg.py | Searches Google and sends the results | `/google <keywords>`
 send_help.py | Sends a help text with information about every plugin | `/help`
 isup.py | Checks if a URL is up or not | `/isup <url>`
 kickme.py | Kicks you from the group chat | `/kickme`
 magic8ball.py | Magic 8-Ball | `/magic8ball`
 plugin.py | Allows you to list all plugins, and enable or disable them | <code>/plugin list &#124; enable <plugin name> &#124; disable <plugin name></code>
 quote.py | Allows you to add or retrieve a quote | `/quote [add]`
 random.py | Generate a random number between 1-100 or the specified range | `/random number [range start] [range end]`
 rate.py | Rates the thing you specified | `/rate [thing]`
 set_group_avatar.py | Sets the picture you replied to as the group avatar | `/setpic`
 send_tweet.py | Sends the specified text as a tweet | `/tweet [text]`
 wheeldecide.py | Randomly chooses between one of the options | `/wheeldecide <option 1> <option 2>`

Installation
------------

Download the latest version [here](https://github.com/bastiaanbiester/maiebot/releases/latest).   
Extract it, and you can run the program like:    

```
python maiebot.py
```
    
You can quit the bot like any other Python program, using `Ctrl` + `Break`   
Before the bot will work, you also need to add your api key to config.yaml.example and rename it to config.yaml


Requirements
------------

 - Python 3.6 or higher
 - All packages in requirements.txt, which can be installed by running   

```
pip install -r requirements.txt
```
    
Don't hesitate to open an issue if you're running into problems.
