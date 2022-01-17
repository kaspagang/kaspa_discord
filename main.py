import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
import kaspa
from defines import answers as ans, devfund_addresses as dev_addrs

keep_alive()

discord_client = discord.Client()
discord_client = commands.Bot(command_prefix='$')


@discord_client.event
async def on_ready():
  print(f'running {discord_client.user}...')

@discord_client.command()
async def list_commands(cxt):
  await cxt.send(ans.HELP)

@discord_client.command()
async def balance(cxt, address):
  print('got command')
  await cxt.send(kaspa.get_balance(address))

@discord_client.command()
async def devfund(cxt):
  await cxt.send(
    ans.DEVFUND(
        kaspa.get_balance(dev_addrs.MINING_ADDR),
        kaspa.get_balance(dev_addrs.DONATION_ADDR)
    )
    )
@discord_client.command()
async def hashrate(cxt):
  await cxt.send(str(kaspa.get_hashrate()))


discord_client.run(os.environ['TOKEN'])