import discord
from discord.ext import commands
from keep_alive import keep_alive
import kaspa
import random
from defines import (answers as ans, devfund_addresses as dev_addrs, DEV_ID, TOKEN)
import helpers
from requests import get
from replit import db
import grpc
keep_alive()

discord_client = discord.Client()
discord_client = commands.Bot(command_prefix='$')

@discord_client.event
async def on_ready():
  print(f'running {discord_client.user}...')

@discord_client.command()
async def balance(cxt, address):
  '''Get balance of address'''
  try:
    await cxt.send(
      helpers.post_process_messages(
        ans.BALANCE(
          *kaspa.get_balances(
            address,
            use_dedicated_node = False
            )
        )
      )
    )
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED + ' - or your balance might be 0')
      )

@discord_client.command()
async def devfund(cxt):
  '''Display devfund balance'''
  try:
    balances = kaspa.get_balances(
      dev_addrs.MINING_ADDR,
      dev_addrs.DONATION_ADDR,
      use_dedicated_node = False
      )
    await cxt.send(
      helpers.post_process_messages(
        ans.DEVFUND(*balances)
        )
    )
  except Exception as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def hashrate(cxt):
  '''Get network hashrate'''
  try:
    hashrate = kaspa.get_hashrate(      
      use_dedicated_node = False
    )
    await cxt.send(
      helpers.post_process_messages(
        ans.HASHRATE(
          helpers.normalize_hashrate(hashrate)
          )
        )
      )
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def useful_links(cxt):
  '''List of useful links'''
  try:
    await cxt.send(helpers.post_process_messages(ans.USEFUL_LINKS))
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def mining_reward(cxt, own_hashrate):
  '''Calculate mining rewards with specified hashrate
      
      Input: <float_or_integer>xH/s (without spaces!)
      
      Formular: <own_h/s>/<net_h/s>*500*<timeframe_in_secounds>
      
      Disclaimer: output is only an approximation, and influenced by current dips and spikes in the network hashrate, as well as growth of the network over time. Also, halving events are currently not included in the calculation. 
      '''
  try:
    network_hashrate = kaspa.get_hashrate(
      use_dedicated_node = False
    )
    own_hashrate = helpers.hashrate_to_int(own_hashrate)
    percent_of_network = own_hashrate/network_hashrate
    await cxt.send(helpers.post_process_messages(ans.MINING_CALC(percent_of_network)))
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def suggest(cxt, *suggestion):
  '''Send a suggestion for the development of kasperbot'''
  try:
    dev = await discord_client.fetch_user(DEV_ID)
    await dev.send(' '.join(suggestion))
    await cxt.send(helpers.post_process_messages(ans.SUGGESTION))
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def joke(cxt):
  '''I tell a joke, you laugh'''
  try:
    joke = get('https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt').text
    await cxt.send(helpers.post_process_messages(joke))
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def my_source_code(cxt):
  '''source code for reference'''
  try:
    await cxt.send('https://github.com/kaspagang/kaspa_discord')
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def search_wiki(cxt, *queries):
  '''query the kaspa wiki with search terms'''
  try:
    j = '+'
    await cxt.send(
      f"https://kaspawiki.net/index.php?search={j.join(queries)}"
    )
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def donate(cxt):
  '''Tips are welcome! - Displays donation addresses'''
  try:
    await cxt.send(helpers.post_process_messages(
        (
      ans.DONATION_ADDRS
        )
      )
    )
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

@discord_client.command()
async def dag_info(cxt):
  '''Query dag information'''
  try:
    await cxt.send(helpers.post_process_messages(
        (
      ans.DAG_STATS(kaspa.get_stats(
        use_dedicated_node = False
      ))
        )
        ))
  except (Exception, grpc.RpcError) as e:
    print(e)
    await cxt.send(
      helpers.post_process_messages(ans.FAILED)
      )

discord_client.run(TOKEN)