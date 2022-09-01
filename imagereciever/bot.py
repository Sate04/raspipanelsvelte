from tokenize import Token
import discord
import json
  
# Opening JSON file
f = open('./secrets.json')
  
# returns JSON object as 
# a dictionary

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

client = MyClient()
print(f)
#client.run(data.token)