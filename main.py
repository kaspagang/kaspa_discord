import os
import discord
from keep_alive import keep_alive
from .message_processor import message_processor
from .defines import *


keep_alive()

kaspabot_client = discord.client(os.environ['TOKEN'])

@kaspabot_client.event
async def on_ready():
  print(f'running {kaspabot_client.user}...')

@kaspabot_client.event
async def on_message(msg :discord.Message):
  if msg.content.startswith(f'@{kaspabot_client.user}'):
    if msg.author == kaspabot_client.user: 
      pass
    await msg.channel.send(message_processor(msg, kaspabot_client).answer())