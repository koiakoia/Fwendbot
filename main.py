import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person. Or bot. I won't judge."
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if message.content.startswith('@imshpire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if db ["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
     options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("@teach"):
    encouraging_message = msg.split("@teach ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouragement learned. A+!")

  if msg.startswith("@del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("@del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("@list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("@responding"):
    value = msg.split("@responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("I'm paying perfect attention and not playing Minecraft.")
    else:
      db["responding"] = False
      await message.channel.send("I'm playing Minecraft and not paying perfect attention.")

  if message.content.startswith('@tomato'):
    await message.channel.send("tuh-maw-tow")
    
  if message.content.startswith('@commandlist'):
    await message.channel.send("You can say sad words to get encouragements, @list to see encouragements, @tomato for a fun surprise, @teach to teach me new encouragements, @responding true or false to enable or disable responding to sad words, and @imshpire to see an inspiring quote.")

keep_alive()
client.run(os.getenv('FWENDSHIPKEY'))