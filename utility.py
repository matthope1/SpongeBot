from replit import db

def get_user_object(username):
  # returns user object from database  
  user = False
  try: 
    # for user in raw_admin_list:
    for i in range(len(db["adminList"])):
      if db["adminList"][i]["username"].lower() == username.lower():
        user = db["adminList"][i].value
        break
    
  except Exception as e:
    print("Get user object error", e)

  return user