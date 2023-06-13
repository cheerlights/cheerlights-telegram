#################################################################################

# CheerLights Telegram Bot
# Developed by: Jeff Lehman, N8ACL
# Date: 10/06/2022
# Current Version: 1.0
# https://github.com/cheerlights/cheerlights-telegram

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Twitter: @n8acl
# Discord: Ravendos
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

#############################
# Import Libraries
import config as cfg
import os
import json
import requests
import tweepy
from datetime import datetime, date, time, timedelta
from tweepy import OAuthHandler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # for reply keyboard (sends message)


#############################
# Telegram Bot Configuration
telegram_bot = Bot(cfg.telegram['token'])
dp = Dispatcher(telegram_bot)

# Define Color Keyboard
color1 = KeyboardButton('Red')
color2 = KeyboardButton('Green')
color3 = KeyboardButton('Blue')
color4 = KeyboardButton('Cyan')
color5 = KeyboardButton('White')
color6 = KeyboardButton('Old Lace')
color7 = KeyboardButton('Purple')
color8 = KeyboardButton('Magenta')
color9 = KeyboardButton('Yellow')
color10 = KeyboardButton('Orange')
color11 = KeyboardButton('Pink')

color_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(color1,color2,color3,color4,color5,color6,color7,color8,color9,color10,color11)

# Define Command Keyboard
cmd1 = KeyboardButton('Set Color')
cmd2 = KeyboardButton('Get Current Color')

cmd_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(cmd1).add(cmd2)




#############################
# Twitter API Object Configuration
auth = OAuthHandler(cfg.twitterkeys["consumer_key"], cfg.twitterkeys["consumer_secret"])
auth.set_access_token(cfg.twitterkeys["access_token"], cfg.twitterkeys["access_secret"])

twitter = tweepy.API(auth)

#############################
# Define Variables
# DO NOT CHANGE BELOW

cheerlights_api_url = 'http://api.thingspeak.com/channels/1417/field/2/last.json'
linefeed = "\r\n"

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
    return json['field2']

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

    valid_colors = ''

    for item in list(color_pick.keys()):
        valid_colors = valid_colors + item + linefeed

    return valid_colors

def send_color(color_name):

    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")

    status = "Set @CheerLights to " + color_name + " on " + timestamp 

    twitter.update_status(status)

#############################
# Define Telegram Bot Functions

@dp.message_handler(commands=['start','help'])
async def welcome(message: types.Message):
    await message.answer('Welcome to the CheerLights Bot! Control CheerLights around the world.', reply_markup = cmd_kb)

@dp.message_handler(regexp='Set Color')
async def set_color(message: types.Message):
    await message.answer('Please select one of the following colors', reply_markup = color_kb)

@dp.message_handler(regexp='Get Current Color')
async def get_color(message: types.Message):
    color_code = use_api()
    curr_color = get_key(color_code.upper(),color_pick)  
    await message.answer('Current CheerLights color: ' + curr_color)

@dp.message_handler(regexp='Red')
async def set_red(message: types.Message):

    color_name = 'Red'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Green')
async def set_greeb(message: types.Message):

    color_name = 'Green'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Blue')
async def set_blue(message: types.Message):

    color_name = 'Blue'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Cyan')
async def set_cyan(message: types.Message):

    color_name = 'Cyan'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='White')
async def set_white(message: types.Message):

    color_name = 'White'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Old Lace')
async def set_oldlace(message: types.Message):

    color_name = 'oldlace'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Purple')
async def set_purple(message: types.Message):

    color_name = 'Purple'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Magenta')
async def set_magenta(message: types.Message):

    color_name = 'Magenta'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Yellow')
async def set_yellow(message: types.Message):

    color_name = 'Yellow'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Orange')
async def set_orange(message: types.Message):

    color_name = 'Orange'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

@dp.message_handler(regexp='Pink')
async def set_pink(message: types.Message):

    color_name = 'Pink'

    send_color(color_name)

    await message.answer('Setting CheerLights to color: ' + color_name)

#############################
# Main Program

# Start Bot
executor.start_polling(dp)