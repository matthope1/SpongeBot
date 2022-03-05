import os
import time, threading, schedule
import requests
import ast
import random
import logging
from replit import db
import asyncio
from functools import wraps
from threading import Thread
from pytube import YouTube
import json
from messages import *
from urls import *
from utility import *
from web3 import Web3
import time, json
from datetime import datetime

import telebot

import asyncio
import aioschedule

from youtubesearchpython import VideosSearch

print("telebot", telebot)

# from telebot.async_telebot import AsyncTeleBot



# Telebot docs
# https://github.com/eternnoir/pyTelegramBotAPI#telebot

# youtube player bot example, https://www.youtube.com/watch?v=ml-5tXRmmFk&ab_channel=RoboticNation

# db tut https://github.com/replit/replit-py/blob/fc47b96202667ca8a04827285a19e94912bdca29/docs/db_tutorial.rst

# https://stackoverflow.com/questions/67177501/horizontally-scale-discord-py

# How to interact with bsc
# https://paohuee.medium.com/interact-binance-smart-chain-using-python-4f8d745fe7b7

'''
# personal useage 
send the bot to other rooms to do work
play music, have it conduct a shill raid

shill raid/ leader
it would use a bunch of saved chat urls
it picks a random url, then itll say 3 2 1, and post one of these random urls

the users in that group will go to that group and post their shill text

leader text example: 

OK GUYS GET READY TO SHILL
5 sec 
/ shill or soft shill
5 sec

so make it so main admin can add users to admin list, where they can have access to the bot for a user defined amount of time

if someone who is not admin makes a request to the bot and they are not admin,
send message saying "you need to be an admin to use this bot, please talk to Sponge "

add /help

/raid for automated shill raid

/music-playlist 1 : house
/music-playlist 2 : rap  
/music-playlist 3 : default 

/music command connects to music live stream


a bot that is automated to send messages to public groups
sends messages to a public group on a time interval
add the ability to change the shill message and add pictures to messages?


# HOW TO AUTOMATE PAYMENTS

We'll need a smart contract and a web3 interface

The smart contract would handle the payments to sponge

function buyBotAccess(telegram username or 1 time passcode generated by the bot)
simply sends the bnb to sponge end emit event to bot backend
https://web3py.readthedocs.io/en/stable/contracts.html?highlight=events#events 

when this event is captured by the bot,
the user will gain access to the bot for the amount of time that they paid for
Then the bot can also DM sponge after this and let them know which user 
just paid for bot access

How to make sure this scales?
'''

# MAINNET
bscProvider = "https://bsc-dataseed.binance.org/"

# TESTNET: 
# bscProvider = "https://data-seed-prebsc-1-s1.binance.org:8545/"

web3 = Web3(Web3.HTTPProvider(bscProvider))
# print(web3.isConnected())

address = "0x772E8A12A8374A4d070538Ea920A4339Bb0959e7" 
balance = web3.eth.get_balance(address)
# print(balance)

result = web3.fromWei(balance,"ether")
# print(result)

# SC connection setup 

contract_abi =  json.loads(""" 
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_secondaryOwner",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "_username",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "_user",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "_value",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "_hours",
				"type": "uint256"
			}
		],
		"name": "UserPaid",
		"type": "event"
	},
	{
		"stateMutability": "payable",
		"type": "fallback"
	},
	{
		"inputs": [],
		"name": "getAllPayments",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "_username",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "_user",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "_timestamp",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "_value",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "_hours",
						"type": "uint256"
					}
				],
				"internalType": "struct SpongeBotPayment.PayInfo[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getBalance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "onlyPrimaryOwner",
		"outputs": [],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_username",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_hours",
				"type": "uint256"
			}
		],
		"name": "pay",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "primaryOwner",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "secondaryOwner",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	}
]
""")

# LOGGING CONFIG
# logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
#                     format='%(asctime)s %(levelname)s %(name)s %(message)s')
# logger=logging.getLogger(__name__)

# contract_address = '0x6B9A81410ad1eD32e2Aa6AdB5F1E9BDCA67F9578'
contract_address = '0x80f2F522285Edbf3843241A376650B02c67aE520'
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Sponge Bot init
API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

# bot = telebot.AsyncTeleBot(API_KEY)

# print("bot", bot)

# from telebot.async_telebot import AsyncTeleBot

# bot = AsyncTeleBot(API_KEY)

print("bot", bot)

chat_id = 'Sponge_bot_testing'

print("Sponge bot running...") 

def add_log(error):
  print("add log called, error: ", error)
  
  log_text = f"error: {error}" 
  logger.error(log_text)

def handle_user_paid(eventDict):
  username = eventDict['args']['_username']
  value = float(eventDict['args']['_value']) 
  hours = float(eventDict['args']['_hours'])

  print("username", username)
  print("value", value)
  print("hours", hours)

  ONE_BNB = 1000000000000000000
  PRICE_PER_HOUR = .2 

  valid_value = int(float((ONE_BNB * PRICE_PER_HOUR) * hours))

  if hours >= 6:
    valid_value = valid_value - .3

  print("valid value", valid_value)
  print("value paid value", value)

  if value == valid_value:
    print('user paid the correct amount')
    print("adding user to admin from front end call")
    add_user_admin(username, hours)

  else:
    print("user did not pay the correct amount")


# SC event loop and handler
def handle_event(event):

  print('event', event)
  eventDict = json.loads(web3.toJSON(event))

  eventName = eventDict['event']

  if eventName == "UserPaid":
    print("user paid event")
    handle_user_paid(event)
  return eventDict

def log_loop(event_filter, poll_interval):
  try: 
    while True:
      for contractEvent in event_filter.get_new_entries():
        handle_event(contractEvent)
      time.sleep(poll_interval)   
  except Exception as e:
    # add_log(e)
    print("Log loop error: ", e)



# DECORATORS
def background(f):
  def wrap(*args, **kwargs):
    try: 
      # TODO: read asyncio docs
      # TODO: check if there's an even loop, if there isn't, then start one and continue
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      this = asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    except Exception as e:
      print("background decorator error:", e)
    return this
  return wrap



def mydecorator(f):  # f is the function passed to us from python
  async def log_f_as_called(*args, **kwargs):
    print(f'{f} was called.')
    await f(*args, **kwargs)
  return log_f_as_called
  
def myotherdecorator(f):  # f is the function passed to us from python
  def log_f_as_called(*args, **kwargs):
    print(f'{f} was called OH YO MOMMA.')
    f(*args, **kwargs)
  return log_f_as_called

def test_decorator(func):

  def wrap(*args, **kwargs):
    print("test decorator called")
    return

  return wrap
  
def check_game_master(func):
  '''Decorator that reports the execution time.'''

  def wrap(*args, **kwargs):
    print("calling is game master")
    message = args[0]

    res = is_game_master(message.from_user.id)
    if res :
      result = func(*args, **kwargs)
      return result
    else:
      bot.send_message(message.chat.id, f"You are not the game master.")
      return
  return wrap

def check_admin(func):
  '''Decorator that reports the execution time.'''
  def wrap(*args, **kwargs):
    print("check admin called")

    try: 
      message = args[0]
      id = message.from_user.id
  
      user_is_admin, err_msg = is_admin(message.from_user.username)
    
      # if message is from sponge
      if id == 1054822819:
        print("command is from sponge")
        user_is_admin = True 
    
      if user_is_admin:
        result = func(*args, **kwargs)
        return result
      else:
        if err_msg:
          bot.send_message(message.chat.id, f"{err_msg}")
        else:   
          bot.send_message(message.chat.id, f"You are not an admin, please contact sponge or navigate to https://spongebot.io to purchase admin access.")
          
    except Exception as e:
      print("check admin failure", e)
      bot.send_message(message.chat.id, f"Check admin error: {e}")

  return wrap
  
def list_database():
  keys = db.keys()

  for key in keys:
    current_val = db[key]
    print(f"key {key} | value {current_val}")

#user utils
def update_admin_shill_group(username, chat_id):
  try: 
    user_index = get_user_index(username)

    if user_index != -1:
      db["adminList"][user_index]["shillGroup"] = chat_id

  except Exception as e:
    print("update admin shill group error", e)

def delete_user(username):
  user_index = get_user_index(username)
  if user_index != -1:
    db["adminList"].remove(db["adminList"][user_index])
  return user_index 

def get_user_index(username):
  # returns position of user in admin list
  found = -1
  try: 
    # for user in raw_admin_list:
    for i in range(len(db["adminList"])):
      if db["adminList"][i]["username"].lower() == username.lower():
        found = i
        break

    return found
  except Exception as e:
    print("Get user index error", e)


def is_admin(username):
  # get user object from db
  # check amount of time passed since they've been granted admin access
  # compare to the amount of time they paid for

  found = False
  user_acc = ''

  # if any(d['username'] == username for d in db["adminList"]):
  # also check if time past is less than some alotted time 

  # TODO: use get user function
  raw_admin_list = ast.literal_eval(db.get_raw("adminList"))

  for user in raw_admin_list:
    if user['username'] == username.lower():
      user_acc = user
      found = True, 

  if found:
    # TODO: get this user from the database (add get user util function)
    # then for check_time_passed, pass in user_admin_time

    admin_time = user['adminTime']
    
    res = check_time_passed(user_acc['createdDate'], admin_time)

    # res = check_time_passed(user_acc['createdDate'], 0.001)
    if not res:
      # user is still admin
      # FIXME: why does this not continue on to the requested function call
      print("user is still an admin, continue on to requested fuction call")
      return True, 'noerr'
    else:
      raw_admin_list.remove(user_acc)
      print("raw admin list after removal", raw_admin_list)
      db['adminList'] = raw_admin_list
      print("user ran out of admin time")
      # TODO: add name of buy time command
      return False, 'Sorry! Your time as admin has ran out, please purchase more time at the Sponge Bot Payment Portal'

  else:
    print("not found")
    return False, 'You are not an admin'

def is_game_master(userId):
  print("is game master", userId)
  
  if userId == db["gameMaster"] or userId == 1054822819 or userId == 2042710483:
    return True
  else:
    return False

def db_init():
  # reset values for all keys in db
  db["chatNames"] = [] 
  db["chatLinks"] = []
  db["adminList"] = []

  print("database initialization complete")

def parse_chat_link(raw_link):
  parsed_link = raw_link.split('t.me/')
  chat_id = parsed_link[1]
  return chat_id

# checks if more time has passed than the hours argument
# returns boolean (true if more time as passed)
def check_time_passed(dateTimeStr, hours):
  dateTimeObj = datetime.strptime(dateTimeStr , '%d/%m/%y %H:%M:%S') 
  now = datetime.now()
  timeDiff = (now - dateTimeObj)
  timeDiffInSeconds =  timeDiff.total_seconds() 

  # 3600 seconds in an hour
  if timeDiffInSeconds > int(hours) * 3600:
    # print(f"more than {hours} hours have passed")
    return True
  else:
    # print(f"less than {hours} hours have passed")
    return False

# @bot.message_handler(commands=['log_test'])
# def log_test(message):
#   print('log test called')
#   username = message.from_user.username
#   add_log(username)
#   print("after add log")

# TODO: make it so that this function displays how much time is remaining on the users
# admin access
@bot.message_handler(commands=['time_left'])
@check_admin
def time_left(message):
  # get admin user object from database for user who sent message
  # calculate how much time is left before their admin priv expires
  # return/display time to user
  print('time left called')
  username = message.from_user.username

  if admin_exists(username):
    print("admin found")

    user = get_user_object(username)
    date_time_str = user['createdDate']
    admin_time = user['adminTime']

    print(f"date time str = {date_time_str}")
    print("user", user)

    # if the diff between the current date and the created date for the user is bigger than admin time
    # user is no longer an admin

    # how to get the amount of time left for the user


  # raw_admin_list = ast.literal_eval(db.get_raw("adminList"))

  # for user in raw_admin_list:
  #   print(f"{user['username']} == {username}")
  #   print(user['username'] == username)
  #   if user['username'] == username:
  #     print("user found")
  #     date_time_str = user['createdDate']
  #     print(f"date time str = {date_time_str}")
  #     # TODO: fix me
  #     date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
  #     print("before")
  #     print(date_time_obj)
  #     print("after")
  #     print(f"time left for {username}: {date_time_obj} ")
  #     now = datetime.now()
  #     print(f"current time {now}")
  #     print(f"time diff = {now - date_time_obj}")
  #     bot.send_message(message.chat.id, f"Time left as admin: {date_time_obj}")
  #   else: 

  #     print("user not found")

  #     bot.send_message(message.chat.id, f"Looks like you ran out of time")

def admin_exists(username):
  return any(d['username'] == username for d in db["adminList"])

# internal function for adding user to admin list
def add_user_admin(username, adminTimeHours):
  returnMsg = ""

  if username[0] != '@':
    returnMsg = "incorrect username format"
    print(returnMsg)
    return returnMsg

  if '@' not in username:
    # warning: this will fail if the function is called with a username like this: 
    # test@me
    returnMsg = "incorrect username format"
    print(returnMsg)
    return returnMsg

  username = username.split('@')[1].strip()
  createdDate = datetime.now().strftime('%d/%m/%y %H:%M:%S')

  new_admin = {
    "username": username,
    "createdDate": createdDate,
    "adminTime": adminTimeHours,
    "shillGroup": "",
  }

  try: 
    if not admin_exists(username):
      # append copy of dict to create new ref
      db["adminList"].append(new_admin.copy())

      if admin_exists(username): 
        returnMsg = f"{username} was sucessfully added to your admin list"
        print(returnMsg)

    else:
      returnMsg = f"This user is already an admin"
      print(returnMsg)
  except:
    returnMsg = f"There was an error while trying to add {username} to admin list"
    print(returnMsg)
  
  return returnMsg

@bot.message_handler(commands=['remove_admin'])
@check_game_master
def delete_user_admin_handler(message):
  # handler for removing admin from db

  if '@' not in message.text:
    bot.send_message(message.chat.id, "incorrect username format")
    return
  
  username = message.text.split('@')[1].strip()

  try:
    delete_result = delete_user(username)
    if delete_result != -1:
      bot.send_message(message.chat.id, f"Successfully removed {username} from admin list")
    else: 
      bot.send_message(message.chat.id, f"Failed to remove {username} from admin list.. user not found")
  except Exception as e:
    print("delete user error", e)
    bot.send_message(message.chat.id, f"Failed to remove {username} from admin list.. error: {e}")



@bot.message_handler(commands=['add_admin'])
@check_game_master
def add_user_admin_handler(message):
  # handler for adding admin level user in database

  messageSplit = message.text.split()
  raw_username = messageSplit[1]

  if (len(messageSplit) == 3):
    admin_time_hours = messageSplit[2]
  else:
    bot.send_message(message.chat.id, f"Please add amount of hours. For example: '/add_admin @exampleUsername 5' ")
    return 

  try: 
    result_message = add_user_admin(raw_username, admin_time_hours)
  except Exception as e:
    print("e", e)

  bot.send_message(message.chat.id, result_message)


@bot.message_handler(commands=['payment'])
async def payment(message):
  await bot.send_message(message.chat.id, "Please navigate to https://spongebot.io to purchase access to spongebot")

@bot.message_handler(commands=['dbInit'])
@check_game_master
def db_init_handler(message):
  db_init()

@check_game_master
async def greetFunc(message):
  user = message.from_user 
  print("user", user.id)
  list_database()

  await bot.reply_to(message, "Hey! Hows it going?")

@bot.message_handler(commands=['Greet'])
# @check_game_master
async def greet(message):
  # print("message: ", message)
  await greetFunc(message)
  return
  user = message.from_user 
  print("user", user.id)
  list_database()

  await bot.reply_to(message, "Hey! Hows it going?")


@mydecorator
@check_game_master
async def testFunc(message):
  print("myfunc")
  await bot.reply_to(message, "Hey this is greet2! Hows it going?")
  

# testing
@bot.message_handler(commands=['Greet2'])
# @myotherdecorator
# @check_game_master
async def greet2(message):
  print("greet 2 called")
  # print("message: ", message)
  user = message.from_user 
  print("user", user.id)
  await testFunc(message)
  return
  # list_database()

  await bot.reply_to(message, "Hey this is greet2! Hows it going?")



# @bot.message_handler(commands=['unset'])
# def unset_timer(message):
#   # aioschedule.clean(message.chat.id)
#   aioschedule.clear(message.chat.id)


# end testing

# start sync testing
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! Use /set <seconds> to set a timer")

def beep(chat_id) -> None:
  """Send the beep message."""
  print("sending beep message")
  bot.send_message(chat_id, text='Beep!')

@bot.message_handler(commands=['set'])
def set_timer(message):
  print("set called for chat: ", message.chat.id)
  args = message.text.split()
  if len(args) > 1 and args[1].isdigit():
    sec = int(args[1])

    print("scheduele1")
    schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    print("scheduele2")
  else:
    bot.reply_to(message, 'Usage: /set <seconds>')


# end sync tesing

@bot.message_handler(commands=['view_admins'])
@check_game_master
def view_admins(message):

  raw_admin_list = ast.literal_eval(db.get_raw("adminList"))

  print("admins: ", raw_admin_list)
  bot.reply_to(message, f"admins: {raw_admin_list}")

  for user in raw_admin_list:
    print("username", user['username'])
    print("date created", user['createdDate'])

@bot.message_handler(commands=['view_groups'])
def view_groups(message):
  print("view groups called")

  # get chat list from db
  # Loop through groups list and append each list onto send string
  # send back to the chat the send string

  try: 
    chat_links = db["chatLinks"]
  
    return_message = ""
  
    for chat_link in chat_links:
      return_message += chat_link
      return_message += " "
    
    bot.send_message(message.chat.id, f"Groups: {return_message}")
  
  except: 
    bot.send_message(message.chat.id, "There was an error while trying to view all saved groups. Please try again or contact my creator")


@bot.message_handler(commands=['remove_group'])
def remove_group(message):
  print("remove group called")

  try:
    if(message.text):
      print("message", message.text)
      chat_link = message.text.split('remove_group')[1]
      
      print("chat_link", chat_link)

      if chat_link in db["chatLinks"]:
        db["chatLinks"].remove(chat_link)
        if chat_link not in db["chatLinks"]:
          bot.send_message(message.chat.id, f"Group {chat_link} sucessfully removed from your saved groups")
      else:
        bot.send_message(message.chat.id, f"Group {chat_link} is not saved in your groups list")
  
  except:
    bot.send_message(message.chat.id, f"There was an error while trying to remove group. Please try again or contact my creator")

@bot.message_handler(commands=['add_group'])
@check_admin
def add_group(message):
  print("add group called")

  try :
    if(message.text):
      print("message.text: ", message.text)
  
      chat_link = message.text.split('add_group')[1]
  
      print("chatLink", chat_link)
  
      if chat_link not in db["chatLinks"]:
        db["chatLinks"].append(chat_link)
  
        if chat_link in db["chatLinks"]:
          bot.send_message(message.chat.id, f"Group {chat_link} was sucessfully added to your group list")
      else:
        bot.send_message(message.chat.id, f"Group {chat_link} already added to your group list")

  except:
    bot.send_message(message.chat.id, "There was an error while trying to add to your group list. Please try again or contact my creator")

@bot.message_handler(commands=['commands', 'help'])
def display_commands(message):

  print("display commands called")

  commands = (
    f'/shill, /soft_shill \n'
    # f'/view_admins \n'
    # f'/message_all_groups \n'
    # f'/message_chat \n'
    f'/time_left \n'
    # f'/view_groups \n'
    # f'/add_group \n'
    # f'/remove_group \n'
    f'/payment \n'
    # f'/ \n'
  )
  
  bot.send_message(message.chat.id, f"Spongebot has the following commands: \n {commands}")

# chaturls = ['https://t.me/testChannelspongey', 'https://t.me/Sponge_bot_testing', 'https://t.me/testChannelSpongey2']


# TODO:
def send_soft_shill_group(chat_id):
  print("send soft shill group")
  
  # get random number
  n = random.randint(0,len(soft_shill_urls) - 1)

  # use number to get random entry from the chat urls list
  randomUrl = soft_shill_urls[n]

  time.sleep(2)

  bot.send_message(chat_id, "OK GUYS GET READY TO SHILL")
  time.sleep(5)
  bot.send_message(chat_id, f"POSTING THE RAID LINK IN 3 2 1...")
  time.sleep(3)

  bot.send_message(chat_id, f"GO! {randomUrl}")

def run_threaded(job_func, *args):
  chat_id = args[0]
  job_thread = threading.Thread(target=job_func, args = [chat_id])
  job_thread.start()

# unset a shill schedule
@bot.message_handler(commands=['unset'])
def unset_timer(message):
    print("unset for chat: ", message.chat.id)
    schedule.clear(message.chat.id)

  
@bot.message_handler(commands=['soft_shill_test'])
@check_admin
def set_soft_shill(message):
  # SOFT_SHILL_LOOP = 120 
  chat_id = message.chat.id
  SOFT_SHILL_LOOP = 10 
  bot.send_message(chat_id, "Soft shilling is: talking about the project in a casual manner that may not come off as shilling to people who aren’t aware of what shilling is")
  time.sleep(10)
  
  # TODO: check if there's already a schedule running for this chat id
  jobs = schedule.get_jobs(chat_id)
  print("jobs:", jobs)
  if (len(jobs) > 0):
    bot.send_message(chat_id, "you are already running a soft shill")
    return
  
  send_soft_shill_group(chat_id)
  schedule.every(SOFT_SHILL_LOOP).seconds.do(run_threaded, send_soft_shill_group, chat_id).tag(chat_id)


@background
def send_soft_shill(chat_id, loop_counter):
  # try: 
  #   # gif = open('./assets/321.gif', 'rb')
  #   gif = open('./assets/321-one-loop.gif', 'rb')
  #   bot.send_video(chat_id, gif)
  # except Exception as e: 
  #   print("send gif failed", e)

  # return 

  SOFT_SHILL_LOOP = 120 

  bot.send_message(chat_id, "Soft shilling is: talking about the project in a casual manner that may not come off as shilling to people who aren’t aware of what shilling is")

  time.sleep(10)

  i = 0
  loop = True

  while loop:
    if i == loop_counter:
      print("loop counter reached")
      loop = False
      break

    # get random number
    n = random.randint(0,len(soft_shill_urls) - 1)
  
    # use number to get random entry from the chat urls list
    randomUrl = soft_shill_urls[n]

    time.sleep(2)

    bot.send_message(chat_id, "OK GUYS GET READY TO SHILL")
    time.sleep(5)
    bot.send_message(chat_id, f"POSTING THE RAID LINK IN 3 2 1...")
    time.sleep(3)

    bot.send_message(chat_id, f"GO! {randomUrl}")

    time.sleep(SOFT_SHILL_LOOP)
    i = i + 1


@bot.message_handler(commands=['hard_shill', 'soft_shill'])
@check_admin
def shill(message):
  # check if admin has shill group
  # if admin has a shill group, don't allow them to call this function

  print("shill called")

  if " " in message.text:
    command_list = message.text.split(" ") 
  else:
    bot.send_message(message.chat.id, f"Please add the amount of times you would like SpongeBot to shill for. Eg (/soft_shill 2)")

  if command_list:
    shill_type = command_list[0]
    loop_counter = int(command_list[1]) 
  else:
    shill_type = message.text
    loop_counter = 3

  try:
    username = message.from_user.username
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_index = get_user_index(username)
    print("userid: ", user_id)

    if user_id == -1: 
      bot.send_message(chat_id, f"User not found")
      return

    if not is_game_master(user_id):
      shill_group = db['adminList'][user_index]['shillGroup']
      if shill_group and shill_group != chat_id:
        bot.send_message(chat_id, f"You cannot use Sponge Bot in more than one group, after your current admin session is over, buy more hours to use Sponge Bot in another group")
        return 

      elif not shill_group and not is_game_master(user_id):   
        bot.send_message(chat_id, f"Your shill group will now be set to the group you have sent this command from")
        update_admin_shill_group(username, chat_id)
  
    if shill_type == '/soft_shill':
      send_soft_shill(message.chat.id, loop_counter) 
  except Exception as e:
    print("shill error: ", e)


# TODO: test me
@bot.message_handler(commands=['message_all_groups'])
def message_all_groups(message):
  print("message all groups called")

  try:
    if(message.text):

      # Loop through all chats
      # for each chat, parse the link to get the chat id
      # make a call to the telegram api to send message to the chat

      chat_links = db["chatLinks"]

      message_to_send = "this is a test message"

      for chat_link in chat_links:
        chat_id = parse_chat_link(chat_link)
        print("chatid: ", chat_id)
        telegram_api_url = f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id=@{chat_id}&text={message_to_send}"
        # TODO: add error handling here
        # if message request to the api fails, send message back to user saying that there was an issue sending message to this group
        try: 
          tel_resp = requests.get(telegram_api_url)
          if not tel_resp: 
            bot.send_message(message.chat.id, f"There was an issue sending a message to {chat_link}")

        except: 
          # TODO: test what happens when the message fails
          # what happens when that group doesn't exist
          bot.send_message(message.chat.id, f"There was an issue sending a message to {chat_link}")
    
  except:
    bot.send_message(message.chat.id, "There was an error while trying to send a message to all groups. Please try again or contact my creator")


@bot.message_handler(commands=['message_chat'])
def message_chat(message):

  telegram_api_url = f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id=@{chat_id}&text={packages_string}"

  tel_resp = requests.get(telegram_api_url)

  print()
  print()
  print("message:", message)
  print("chat id: ", message.chat.id)
  print()
  print()

  # bot.reply_to(chat_id, packages_string)
  # bot.send_message(chat_id, packages_string)

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['packages'])
def packages(message):
  bot.send_message(message.chat.id, packages_string)

# TODO: 
def yt_search(song):
  try: 
    
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    print("videosSearch Result: ", result)
    if not result:
      return False
    else:
      video_id = result["result"][0]["id"]
      url = f"https://youtu.be/{video_id}"
      return url
      
  except Exception as e:
    print("yt song error: ", e)
    

def test_song(client, message):
  print("song test")

@bot.message_handler(commands=['song'])
def test(message):
  print("test called")
  print("now calling test song")
  test_song("client", message)

def get_args(message_text):
  if " " in message_text: 
    return message_text.split(" ")

@bot.message_handler(commands=['Song'])
async def song(message):
  try: 
    print("song called")
 
    chat_id = message.chat.id
    user_id = message.from_user.id
    song_name = ""

    message_args = get_args(message.text)
    print("message args", message_args)
    if message_args:
      song_name = message_args[1]
    
    # await bot.reply_to(message, "Searching the song reply to")
    # await bot.send_message(chat_id, text='Searching the song send message')
    
    status = await bot.reply_to(message,"🚀 🔎 🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠... 🎶 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 ⏳️ 𝐅𝐨𝐫 𝐅𝐞𝐰 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 [🚀](https://telegra.ph/file/67f41ae52a85dfc0551ae.mp4)")
    video_link = yt_search(song_name)
    
    if not video_link:
        await status.edit("✖️ 𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐒𝐨𝐫𝐫𝐲.\n\n𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐤 𝐎𝐫 𝐌𝐚𝐲𝐛𝐞 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲.\n\nEg.`/song Faded`")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song 😶")
        # LOGGER.error(ex)
        return ""
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await app.send_chat_action(message.chat.id, "upload_audio")
    await app.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")
 
  except Exception as e:
    
    print("Song error: ", e)

# bot.polling()
# async def telegram_polling():

def thread_test():
  print('thread test')

def schedule_pending_loop():
   while True:
     try: 
      print("scheduele polling...")
      schedule.run_pending()
      time.sleep(1)
     except Exception as e:
        print("scheduele polling error: ", e)

def telegram_polling():
    try:
      event_filter = contract.events.UserPaid.createFilter(fromBlock='latest')
    
      bsc_event_worker = Thread(target=log_loop, args=(event_filter, 2), daemon=True)
      bsc_event_worker.start()

      # this will stop execution
      # bot.polling(none_stop=True, timeout=60) #constantly get messages from Telegram

      # this will run bot polling in a thread
      threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
  

      # this is for running the scheduele polling 
      threading.Thread(target=schedule_pending_loop, name='schedule_pending_loop', daemon=False).start()

      # basic loop for scheduele polling
      
      # while True:
      #   print("run pending")
      #   schedule.run_pending()
      #   time.sleep(1)

      while True:
        print("Program loop...")
        time.sleep(1)




      # await asyncio.gather(bot.infinity_polling(), scheduler())
    except:

        # traceback_error_string=traceback.format_exc()

        # with open("Error.Log", "a") as myfile:
        #     myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<ERROR polling>>\r\n"+ traceback_error_string + "\r\n<<ERROR polling>>")
            
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()

if __name__ == '__main__':    
  # asyncio.run(main())
  # asyncio.run(telegram_polling())
  
  telegram_polling()




# async def main():


# if __name__ == '__main__':


