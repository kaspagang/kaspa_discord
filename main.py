import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
import kaspa
from defines import answers as ans, devfund_addresses as dev_addrs
import helpers

keep_alive()

DEV_ID = os.environ['DEV_ID']

discord_client = discord.Client()
discord_client = commands.Bot(command_prefix='$')

@discord_client.event
async def on_ready():
  print(f'running {discord_client.user}...')

@discord_client.command()
async def command_details(cxt):
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
  hashrate = kaspa.get_hashrate()
  await cxt.send(
    helpers.post_process_messages(
      ans.HASHRATE(
        helpers.normalize_hashrate(hashrate)
        )
      )
    )

@discord_client.command()
async def useful_links(cxt):
  await cxt.send(helpers.post_process_messages(ans.USEFUL_LINKS))

@discord_client.command()
async def mining_reward(cxt, own_hashrate):
  '''please supply hashrate in the format xH/s'''
  network_hashrate = kaspa.get_hashrate()
  print(network_hashrate, own_hashrate)
  percent_of_network = own_hashrate/network_hashrate
  await cxt.send(helpers.post_process_messages(ans.MINING_CALC(percent_of_network)))

@discord_client.command()
async def suggest(cxt, *suggestion):
  dev = await discord_client.fetch_user(DEV_ID)
  await dev.send(' '.join(suggestion))
  await cxt.send(helpers.post_process_messages(ans.SUGGESTION))

discord_client.run(os.environ['TOKEN'])