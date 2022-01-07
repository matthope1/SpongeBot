from main import *

# API_KEY = os.getenv('API_KEY')
# bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['testing'])
def testing(message):
  print("testing called")