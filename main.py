import os
import telebot
import time
import requests
from replit import db

from messages import *


# how to restrict access https://stackoverflow.com/questions/35368557/how-to-limit-access-to-a-telegram-bot


# youtube player bot example, https://www.youtube.com/watch?v=ml-5tXRmmFk&ab_channel=RoboticNation

# I think we'll want people or admin to be able to play songs with song names or url's


# db tut https://github.com/replit/replit-py/blob/fc47b96202667ca8a04827285a19e94912bdca29/docs/db_tutorial.rst

# https://stackoverflow.com/questions/67177501/horizontally-scale-discord-py


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





'''

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

chat_id = 'Sponge_bot_testing'

print("Sponge bot running...")

def db_init():
  db["chatNames"] = [] 
  db["chatLinks"] = []

  print("database init...")

def parse_chat_link(raw_link):
  print("link: ",raw_link)
  parsed_link = raw_link.split('t.me/')
  chat_id = parsed_link[1]
  return chat_id

@bot.message_handler(commands=['Greet'])
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")


"""

TODO: 

Create a message handler that can allow the addition of new messages to be sent?

"""

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

        tel_resp = requests.get(telegram_api_url)
    
  
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



# bot.polling()

def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=60) #constantly get messages from Telegram
    except:
        # traceback_error_string=traceback.format_exc()

        # with open("Error.Log", "a") as myfile:
        #     myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<ERROR polling>>\r\n"+ traceback_error_string + "\r\n<<ERROR polling>>")
            
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()

if __name__ == '__main__':    
    telegram_polling()