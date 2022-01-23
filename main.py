import discord
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
import kaspa
import random
from defines import (answers as ans, devfund_addresses as dev_addrs, DEV_ID, TOKEN, SER_TO_ALLOWED_CHANS, SER_TO_ANSWER_CHAN, CALL_FOR_DONATION_PROB, DISCLAIMER_INTERVAL)
import helpers
from requests import get
import grpc
keep_alive()

discord_client = discord.Client()
discord_client = commands.Bot(command_prefix='$')

@discord_client.event
async def on_ready():
  print(f'running {discord_client.user}...')
  discord_client.loop.create_task(send_disclaimer())

async def send_disclaimer():
  trade_chan = discord_client.get_channel(910316340735262720)
  while True:
    trade_chan = discord_client.get_channel(910316340735262720)
    if random.random() < CALL_FOR_DONATION_PROB:
      msg = helpers.adjoin_messages(
        None, 
        True, 
        ans.DISCLAIMER,
        ans.DONATION_ADDRS
        )
    else:
      msg = helpers.adjoin_messages(
        None, 
        True, 
        ans.DISCLAIMER
        )
    await asyncio.sleep(DISCLAIMER_INTERVAL)
    await trade_chan.send(msg)


@discord_client.command()
async def balance(cxt, address, *args):
  '''Get balance of address'''
  here = True if 'here' in args else False
  try:
    balances = kaspa.get_balances(address)
    msg = ans.BALANCE(*balances)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)


@discord_client.command()
async def devfund(cxt, *args):
  '''Display devfund balance'''
  here = True if 'here' in args else False
  try:
    balances = kaspa.get_balances(
      dev_addrs.MINING_ADDR,
      dev_addrs.DONATION_ADDR,
      )
    msg = ans.DEVFUND(*balances)
    await _send(cxt, msg, here)
  except Exception as e:
    await _process_exception(cxt, e, here)


@discord_client.command()
async def hashrate(cxt, *args):
  '''Get network hashrate'''
  here = True if 'here' in args else False
  try:
    hashrate = kaspa.get_hashrate(      
      use_dedicated_node = False
    )
    norm_hashrate = helpers.normalize_hashrate(hashrate)
    msg = ans.HASHRATE(norm_hashrate)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@discord_client.command()
async def useful_links(cxt, *args):
  '''List of useful links'''
  here = True if 'here' in args else False
  try:
    msg = ans.USEFUL_LINKS
    await _send(cxt, msg, here, blockify=False)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)


@discord_client.command()
async def mining_reward(cxt, own_hashrate, *args):
  '''Calculate mining rewards with specified hashrate
      
      Input: <float_or_integer>xH/s (without spaces!)
      
      Formular: <own_h/s>/<net_h/s>*500*<timeframe_in_secounds>
      
      Disclaimer: output is only an approximation, and influenced by current dips and spikes in the network hashrate, as well as growth of the network over time. Also, halving events are currently not included in the calculation. 
  '''
  here = True if 'here' in args else False
  try:
    network_hashrate = kaspa.get_hashrate()
    own_hashrate = helpers.hashrate_to_int(own_hashrate)
    percent_of_network = own_hashrate/network_hashrate
    msg = ans.MINING_CALC(percent_of_network)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@discord_client.command()
async def suggest(cxt, *suggestion):
  '''Send a suggestion for the development of kasperbot'''
  here = True if 'here' == suggestion[-1] else False
  try:
    suggestion = "SUGGESTION: " + ' '.join(suggestion)
    await _send(cxt, suggestion, here, blockify = False, dm_dev = True)
    thanks = ans.SUGGESTION
    await _send(cxt, thanks, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)


@discord_client.command()
async def joke(cxt, *args):
  '''I tell a joke, you laugh'''
  here = True if 'here' in args else False
  try:
    msg = get('https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt').text
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)


@discord_client.command()
async def my_source_code(cxt, *args):
  '''source code for reference'''
  here = True if 'here' in args else False
  try:
    msg = 'https://github.com/kaspagang/kaspa_discord'
    await _send(cxt, msg, here, blockify=False)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@discord_client.command()
async def search_wiki(cxt, *queries):
  '''query the kaspa wiki with search terms'''
  here = True if 'here' in queries[-1] else False
  try:
    j = '+'
    msg = f"https://kaspawiki.net/index.php?search={j.join(queries)}"
    await _send(cxt, msg, here, blockify=False)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@discord_client.command()
async def donate(cxt, *args):
  '''Tips are welcome! - Displays donation addresses'''
  here = True if 'here' in args else False
  try:
    msg = ans.DONATION_ADDRS
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@discord_client.command()
async def dag_info(cxt, *args):
  '''Query dag information'''
  here = True if 'here' in args else False
  try:
    stats = kaspa.get_stats()
    msg = ans.DAG_STATS(stats)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

def _post_process_msg(cxt, msg, blockify=True):
  if random.random() < CALL_FOR_DONATION_PROB:
    return helpers.adjoin_messages(
      cxt.author.id,
      blockify, 
      msg,
      ans.DONATION_ADDRS
      )
  else:
    return helpers.adjoin_messages(
      cxt.author.id,
      blockify,
      msg
      )

@discord_client.command()
async def coin_supply(cxt, *args):
  '''Get current coin supply'''
  here = True if 'here' in args else False
  try:
    stats = kaspa.get_stats()
    circ_supply = int(stats['daa_score'])*500
    msg = ans.COIN_STATS(circ_supply)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)


async def _process_exception(cxt, e, here):
  print(e)
  recv_msg = str(cxt.message.content)
  msg = ans.FAILED(recv_msg)
  await _send(cxt, msg, here)

async def _send(cxt, msg, here, blockify=True, dm_dev=False, dm_user=False):
  msg = _post_process_msg(cxt, msg, blockify)
  if dm_dev:
    dev_chan = await discord_client.fetch_user(int(DEV_ID))
    await dev_chan.send(msg)
  elif dm_user:
    user_chan = await discord_client.fetch_user(int(cxt.author.id))
    await user_chan.send(msg)
  elif isinstance(cxt.channel, discord.channel.DMChannel): #is dm
    await cxt.send(msg)
  elif here is True:
    await cxt.send(msg)
  elif cxt.channel.id in SER_TO_ALLOWED_CHANS[cxt.guild.id]:
    await cxt.send(msg)
    # await cxt.message.delete()
  else:
    dedicated_chan = discord_client.get_channel(SER_TO_ANSWER_CHAN[cxt.guild.id])
    await dedicated_chan.send(msg)
    # await cxt.message.delete()
discord_client.run(TOKEN)