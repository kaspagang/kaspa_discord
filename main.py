import os
import discord
from keep_alive import keep_alive
from message_processor import message_processor

keep_alive()

discord_client = discord.client(os.environ['TOKEN'])

@discord_client.event
async def on_ready():
  print(f'running {discord_client.user}...')

@discord_client.event
async def on_message(msg :discord.Message):
  if msg.content.startswith(f'@{discord_client.user}'):
    if msg.author == discord_client.user: 
      pass
    await msg.channel.send(message_processor(msg, discord_client).answer())

discord_client.run()