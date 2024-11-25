# CheerLights Telegram Bot
This bot was created for use with Telegram. This is for the Offical CheerLights Bot.

It will allow you to get the current color and set a new color.

---

## Bot Commands

The following are the commands the bot will recognize.

| Command | Description | Example |
|---------|-------------|---------|
|/start|Displays the starting Keyboard to select functions with|/start|

## Installation/Setup

#### Installation Steps
1) Obtain API Keys
2) Clone Repo 
3) Set Connection Configuration
4) Install Dependencies
   a) install library dependencies (if not running in Docker)
   b) Build container (if using Docker)
5) Start Script
   a) Use run scripts below (if not running in Docker)
   b) Start Container (if running in Docker)

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi.

If you want to run this on a Windows or Mac machine, you will need to install Python3 and be familiar installing from a requirements.txt.

#### Obtaining API Keys

The first step in this process will be obtaining the API keys that you need. Some of the services you choose to use may take a couple of days to approve the access to their API's, so you will want to start this step before installing the script. That way when you are done installing the script and are ready to configure, you have everything ready to go.

###### Telegram

- You will need to first need create a Telegram bot. If this is your first bot, you can use the [steps here](https://core.telegram.org/bots#6-botfather) and talk to @BotFather to create your bot. You will need the bot token for the bot you are using/creating and this can also be obtained from talking to @BotFather.
- Note that Influx DB provides some examples of what to look for. You can go to their page by [clicking here](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/).
- Once the bot is created, it will display a Bot Token in the chat window. Copy this token somewhere as you will need it when you configure the bot later.

Once you have the token you need, you will eventually copy them into the appropriate places in the ```config.json``` file, but now we need to get the files and get things installed.


#### Installing the Script

The next step is installing the needed packages, cloning the repo to get the script and then installing the needed libraries for the script to work properly. 

There are two methods to run this script, Manually (bare metal essentially) or in Docker (Recommended)

##### Manual Installation

If you choose to not run this in Docker, you will need to take some steps to get this script installed. First we need to install some additional programs and the libraries that the script needs.

Please run the following commands:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen

git clone https://github.com/cheerlights/cheerlights-telegram

cd cheerlights-telegram

pip3 install -r requirements.txt
```

Now you have everything installed and are ready to configure the script. See the configuarion steps below.

##### Docker Configuration (Recommended)

To run using Docker, it is assumed you already have Docker and Docker compose installed on a host and working. There are plenty of installation instructions online to get Docker working.

Please run the following commands:

```bash
git clone https://github.com/cheerlights/cheerlights-telegram

cd cheerlights-telegram

pip3 install -r requirements.txt
```

Then edit the ```docker-compose.yaml``` file in the repository.

Change the path under the volume that says ```/path/to/``` to the actual path where you have the bot directory at and save the file.


### Configure the Script
Once you have done that, you will need to edit the ```config.json``` file and configure the following:

```json
{
    "logging_enabled": true,
    "msg_wait_time": 30,
    "telegram": {
        "token": "TELEGRAM BOT TOKEN HERE"
    },
    "cl_wh": "CL WEBHOOK HERE",
    "wh_user": "CL WEBHOOK USER HERE",
    "wh_password": "CL WEBHOOK USER PASSWORD HERE",

    "database": {
    "rdbms_type": "mssql",
    "credentials": {
      "username": "DB USER NAME HERE",
      "password": "DB PASSWORD HERE",
      "host": "DB HOST HERE",
      "db": "LOGGING DB NAME HERE"
    }
  }

}
```
- ```logging_enabled```: This is ```True``` or ```False```. If True it is enabled and will log all messages sent through the bot. This does require a database system for this to work. Supported Databases are below.
- ```msg_wait_time```: This is the amount of time (in seconds) to delay letting a user send a message. This is to help with spamming.
- ```Telegram```: This section is Telegram Settings.
    - ```Token```: This is the bot token gotten from BotFather.
- ```cl_wh```: This is the CheerLights Processor Webhook.
- ```wh_user```: Webhook User Name
- ```wh_password```: Webhook Password
- ```database```: This is the database connection configuration for logging.
    - ```rdbms_type```: this is the database system type. Supported types are:
        - mysql - MySQL/MariaDB
        - postgresql - PostgreSQL
        - mssql - MS SQL Server
        - sqlite - SQLite (built in Database with Python)
    - ```credentials```: These are the credentials to connect to the database. These are not used if using the SQLite database connection type.
        - ```username```: SQL Username
        - ```password```: SQL Password
        - ```host```: ip address or FQDN of the host of the database server
        - ```db```: database name to use for logging. 
        - Note that if the Discord bot is being used, you should use the same database and credentials here.
        - Also note that you should not use a system administrator user/password. You should create a user/password that has the ability to create databases and tables and insert data into tables.


Save the file once the settings have been configured.

### Running the Script

Once you have the config file edited, you will need to install the database. 

Run the Following command:

```bash
python3 db_setup.py
```
##### Manually Running

Start the bot by typing the following:

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

##### Running with Docker

```bash
docker compose build

docker compose up -d
```
---

## Change Log

- 11/25/2024 - 2.0 Release
    - Different Python Library
    - Multiple Database support for logging instead of text files
- 10/07/2022 - Initial Release 1.0