#!/usr/bin/env python

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


import os
import json
import requests
from datetime import datetime, date, time, timedelta
import time
import sqlalchemy
from sqlalchemy import text as sqltext, select, MetaData, Table, update, insert

if os.path.exists('src'):
   # Import our Custom Libraries
   import src.db_functions as dbf
   import src.db_conn as dbc
else:
	#set the parent directory one level up and then import the src files
   current_dir = os.path.dirname(os.path.abspath(__file__))
   parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
   sys.path.insert(0, parent_dir)  

   import src.db_functions as dbf
   import src.db_conn as dbc 

#############################
# import config json file

config_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'config.json'))

with open(config_file, "r") as read_file:
    config = json.load(read_file)
read_file.close()

#############################
# set database connection

try:
    db_engine = dbc.db_connection()
    print("Database Connection established")

except Exception as e:
    print("Database Connection could not be established.", e)

metadata = sqlalchemy.MetaData()
metadata.reflect(bind=db_engine)

cheerlights_log = metadata.tables['cheerlights_logs']

#############################
# Define Variables
# DO NOT CHANGE BELOW

cheerlights_api_url = 'http://api.thingspeak.com/channels/1417/field/1/last.json'
linefeed = "\r\n"
rate_limiter = {}
color_pick = {
    "red" : "#FF0000",
    "green" : "#008000",
    "blue" : "#0000FF",
    "cyan" :"#00FFFF",
    "white" : "#FFFFFF",
    "oldlace" : "#FDF5E6",
    "purple" : "#800080",
    "magenta" : "#FF00FF",
    "yellow" : "#FFFF00",
    "orange" : "#FFA500",
    "pink" : "#FFC0CB"
}

#############################
# Define Functions

def use_api():
    # Pulls latest Color from Cheerlights API

    r = requests.get(cheerlights_api_url, timeout=None)
    json = r.json()
    return json['field1']

def hex_to_rgb(col_hex):
    #Convert a hex colour to an RGB tuple.

    col_hex = col_hex.lstrip('#')
    return bytearray.fromhex(col_hex)

def get_key(val, my_dict):
    # Return the Key from a value in a dictionary

    for key, value in my_dict.items():
         if val == value:
             return key

def valid_colors():
    # Returns list of valid colors

    valid_colors = []

    for item in list(color_pick.keys()):
        valid_colors.append(item)

    return valid_colors

def logging(log_message, full_name, color):

    sql = cheerlights_log.insert()
    values_list = [{
        'application': 'telegram',
        'username' : full_name,
        'userid': '',
        'message': log_message,
        'color': color}]

    dbf.insert_sql(db_engine,sql,values_list)

def send_to_webhook(color, username):

    cl_msg = {'source': 'telegram', 'colours': color, 'username': username.replace(' ','_')}

    response = requests.post(
        config['cl_wh'], data=json.dumps(cl_msg),
        headers={'Content-Type': 'application/json'},
        auth = (config['wh_user'],config['wh_password'])
    )

    return f"Setting CheerLights to color: {color[0]}"

################################
### Define bot

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Get Current Color", callback_data='get_color')],
        [InlineKeyboardButton("Set Color", callback_data='set_color')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the CheerLights Bot! Choose an option:", reply_markup=reply_markup)


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    if query.data == 'get_color':
        user = query.from_user
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip().replace(' ','_') or "Anonymous"
        current_color = use_api()
        log_message = f"Command: Get Current Color"
        logging(log_message, full_name, current_color)
        await query.edit_message_text(f"The current CheerLights color is: {current_color}")
    elif query.data == 'set_color':

        VALID_COLORS = valid_colors()

        color_keyboard = [
            [InlineKeyboardButton(color.capitalize(), callback_data=color) for color in VALID_COLORS[0:3]],
            [InlineKeyboardButton(color.capitalize(), callback_data=color) for color in VALID_COLORS[3:6]],
            [InlineKeyboardButton(color.capitalize(), callback_data=color) for color in VALID_COLORS[6:9]],
            [InlineKeyboardButton(color.capitalize(), callback_data=color) for color in VALID_COLORS[9:]]
 
        ]
        reply_markup = InlineKeyboardMarkup(color_keyboard)
        await query.edit_message_text("Choose a color to set:", reply_markup=reply_markup)
    elif query.data in valid_colors():
        now = int(time.time())        
        user = query.from_user
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip().replace(' ','_') or "Anonymous"
        if full_name not in rate_limiter:
            rate_limiter[full_name] = 9999999
        
        if rate_limiter[full_name] == 9999999 or (now - rate_limiter[full_name] >=config['msg_wait_time']):
            rate_limiter[full_name] = now
            
            color = []
            color.append(query.data)
            log_message = f"Command: Set Color to {color[0]}"
            logging(log_message, full_name, color[0])
            result = send_to_webhook(color, full_name)
            await query.edit_message_text(result) 
        else:
            await query.edit_message_text("Slow down there sport! You are trying to send colors way too fast. Please wait "+ str(config['msg_wait_time']) + " seconds before trying again.")

def main():

    # Create the application
    application = Application.builder().token(config['telegram']['token']).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Start the bot
    print("Bot Running...")
    application.run_polling() 


if __name__ == "__main__":
    main()