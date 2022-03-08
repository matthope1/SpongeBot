
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

# TODO: try to get this to work with that other api
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




# decorators

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