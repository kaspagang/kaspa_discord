import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
import kaspa
from defines import answers as ans, devfund_addresses as dev_addrs
import helpers

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
  await cxt.send(ans.BALANCE(kaspa.get_balance(address)))

@discord_client.command()
async def devfund(cxt):
  balances = kaspa.get_balances(
    dev_addrs.MINING_ADDR,
    dev_addrs.DONATION_ADDR
    )
  await cxt.send(
    helpers.post_process_messages(
      ans.DEVFUND(*balances)
      )
  )

@discord_client.command()
async def hashrate(cxt):
  await cxt.send(str(kaspa.get_hashrate()))


discord_client.run(os.environ['TOKEN'])