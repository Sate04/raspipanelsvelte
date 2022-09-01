import discord
import json
import base64

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Use a service account.
cred = credentials.Certificate('./hidden/appkey.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()
  
# Opening JSON file
f = open('./hidden/secrets.json')
  
# returns JSON object as 
# a dictionary
secrets = json.load(f)

intents = discord.Intents.all()
 # If you also want reaction events enable the following:
 # intents.reactions = True

 # Somewhere else:
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')

@client.event
async def on_message(message):
    if message.content.startswith('.upload'):
        try:
            sample_string = message.content[8:]
            sample_string_bytes = sample_string.encode("ascii")
            
            base64_bytes = base64.b64encode(sample_string_bytes)
            base64_string = base64_bytes.decode("ascii")

            doc_ref = db.collection(u'links').document(base64_string)
            doc_ref.set({
                u'link': base64_string
            })
            await message.channel.send("Link uploaded!")
        except:
            await message.channel.send("Error uploading link!")
    
    if message.content.startswith('.getimages'):
        try:
            docs = db.collection(u'links').stream()

            for doc in docs:
                base64link = doc.to_dict()['link']
                link = base64.b64decode(base64link).decode('utf-8')
                await message.channel.send(link)
        except:
            await message.channel.send("Error getting link!")


client.run(secrets['token'])