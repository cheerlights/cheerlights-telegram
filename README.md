# CheerLights Telegram Bot
This bot was created for use with Telegram.

It will allow you to get the current color and set a new color.

---

## Bot Commands

The following are the commands the bot will recognize.

| Command | Description | Example |
|---------|-------------|---------|
|/start or /help|Displays the starting Keyboard to select functions with|/start or /help|

## Installation/Setup

#### Installation Steps
1) Obtain API Keys
2) Install needed packages, clone Repo and install library dependencies
3) Configure the script

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi.

If you want to run this on a Windows or Mac machine, you will need to install Python3 and be familiar installing from a requirements.txt.

#### Obtaining API Keys

The first step in this process will be obtaining the API keys that you need. Some of the services you choose to use may take a couple of days to approve the access to their API's, so you will want to start this step before installing the script. That way when you are done installing the script and are ready to configure, you have everything ready to go.

###### Twitter

You will need to create a new app and get a consumer key, consumer secret, access token and access secret for the account you are wanting to post to. You can get those keys from the Twitter development site. Here is a walk through how: [Generate Twitter API Keys](https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/). You will also need to apply for elevated privledges for the API to be able to post Tweets to Twitter

Note that it takes a couple of days to get your app approved.

###### Telegram

- You will need to first need create a Telegram bot. If this is your first bot, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. You will need the bot token for the bot you are using/creating and this can also be obtained from talking to @BotFather.
- You will also need your chatid. This can be obtained once your bot is up and running by sending a message to your bot and using the Telegram API by going to this url: [https://api.telegram.org/bot'API-access-token'/getUpdates?offset=0](https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0) replacing 'API-access-token' with your bot access token you obtained in the previous step. You will see some json and you will be able to find your ID there in the From stanza.
- Note that Influx DB provides some examples of what to look for in the above 2 steps. You can go to their page by [clicking here](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/).
- NOTE: Telegram is required for APRS message notification to work.
- Once the bot is created, it will display a Bot Token in the chat window. Copy this token somewhere as you will need it when you configure the bot later.

Once you have the keys you need, you will eventually copy them into the appropriate places in the config.py file, but now we need to get the files and get things installed.


#### Installing the Script

The next step is installing the needed packages, cloning the repo to get the script and then installing the needed libraries for the script to work properly. 

This is probably the easiest step to accomplish.

Please run the following commands:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen

git clone https://github.com/cheerlights/cheerlights-telegram

cd cheerlights-telegram

pip3 install -r requirements.txt
```

Now you have everything installed and are ready to configure the script.

### Configure the Script
Once you have your API Keys, have cloned the repo and installed everything, you can now start configuring the bot. Open the config.py file in your editor of choice and copy in the keys you obtained from Twitter and Telegram into the appropriate spots. Make sure to save the file.


### Running the Script

Once you have the config file edited, start the bot by typing the following:

```bash
screen -R cheerlights-telegram-bot
```

Then in the new window:
```bash
cd cheerlights-telegram-bot

python3 cheerlights_telegram_bot.py
```

Once that is done, hit ```CTRL-A-D``` to disconnect from the screen session. If something ever happens, you can reconnect to the session by typing:

```bash
screen -R cheerlights-telegram-bot
```

---

## Change Log

- 10/07/2022 - Initial Release 1.0