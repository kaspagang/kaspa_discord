import discord
import asyncio
from discord.ext import commands
from discord.utils import get as gt
from keep_alive import keep_alive
from datetime import datetime
import kaspa
import json
import random
import time
from defines import (answers as ans, devfund_addresses as dev_addrs, DEV_ID, TOKEN, SER_TO_ALLOWED_CHANS, SER_TO_ANSWER_CHAN, CALL_FOR_DONATION_PROB, INTERVAL, TRADE_OFFER_CHANS, DEVFUND_CHANS, DONATORS, DONATE_APPENDAGE_REACTS, TRADE_DIS_INTERVALS, DEVFUND_UPDATE_INTERVALS)
import helpers
from requests import get
import grpc
keep_alive()

discord_client = discord.Client()
discord_client = commands.Bot(command_prefix='$')

## events ##

@discord_client.event
async def on_ready():
  print(f'running {discord_client.user}...')
  discord_client.loop.create_task(send_intermittently())
'''
@discord_client.event
async def on_message(recv_msg):
  if int(recv_msg.channel.id) in VOTES_CHANS: #auto react to votes message
    reactions = ['✅', '⛔', '⚠️']
    for react in reactions:
      await recv_msg.add_reaction(react)
  await discord_client.process_commands(recv_msg)
'''

'''
@discord_client.event
async def on_raw_reaction_add(payload):
    channel = payload.channel_id
    if payload.user_id != discord_client.user.id:
      if int(channel) in VOTES_CHANS:
        channel = await discord_client.fetch_channel(channel)
        vote_msg = await channel.fetch_message(payload.message_id)
        if datetime.timestamp(vote_msg.created_at) < (time.time() -60*60*24):
          await vote_msg.remove_reaction(payload.emoji, payload.member)
        elif f'{payload.emoji}' not in VOTE_REACTIONS:
          channel = vote_msg.channel
          await vote_msg.remove_reaction(payload.emoji, payload.member)
'''

## intermittent posts ##

async def send_intermittently():
  i = 1
  while True:
    if i % TRADE_DIS_INTERVALS == 0:
      for trade_chan_id in TRADE_OFFER_CHANS:
        await trade_disclaimer(trade_chan_id)
    await asyncio.sleep(INTERVAL)
    if i % DEVFUND_UPDATE_INTERVALS == 0: 
      for dev_chan_id in DEVFUND_CHANS:
        await devfund_update(dev_chan_id)
    i += 1
    
async def devfund_update(chan_id):
  devfund_chan = await discord_client.fetch_channel(chan_id)
  balances = kaspa.get_balances(
      dev_addrs.MINING_ADDR,
      dev_addrs.DONATION_ADDR,
      )
  if random.random() < CALL_FOR_DONATION_PROB:
    msg = helpers.adjoin_messages(
      None, 
      True, 
      ans.DEVFUND(*balances),
      ans.DONATION_ADDRS
      )
    reactions = DONATE_APPENDAGE_REACTS
  else:
    msg = helpers.adjoin_messages(
      None, 
      True, 
      ans.DEVFUND(*balances)
      )
    reactions = None
  send_msg = await devfund_chan.send(msg)
  if reactions:
    for react in reactions:
      await send_msg.add_reaction(react)

##time_based events###
#no longer implement voting stuff
'''
async def listen_vote():
  vote_chan = await discord_client.fetch_channel(VOTES_CHANS[1])
  after = datetime.fromtimestamp(time.time() - 60*60*24)
  messages = await vote_chan.history(limit=10, before=after).flatten()
  for message in messages:
    await save_vote(message)

async def save_vote(vote_msg):
  msg_sent = datetime.timestamp(vote_msg.created_at)
  if 
  await asyncio.sleep((msg_sent+60*60*24)-time.time())
  votes = list()
  for react in VOTE_REACTIONS:
      reactions = gt(vote_msg.reactions, emoji=react)
      votes.append(reactions.count - 1)
  with open('votes.json', 'r+') as js:
    data = json.load(js)
    data.update({
      vote_msg.id : {'votes' :{
      'Agree'   : votes[0],
      'Disagree': votes[1],
      'Reservations' : votes[2] 
      }},
      'Message' : vote_msg.content,
      'Begin'   : msg_sent,
      'End'     : time.time(),
      })
    js.seek(0)
    json.dump(data, js)
  await vote_msg.clear_reaction('🔓')
  await vote_msg.add_reaction('🔒')
'''

async def trade_disclaimer(chan_id):
  '''send disclaimer to trade channel every hour'''
  trade_chan = await discord_client.fetch_channel(chan_id)
  messages = await trade_chan.history(limit=10).flatten()
  message_ids = [message.author.id for message in messages]
  if discord_client.user.id in message_ids:
    pass
  else:
    if random.random() < CALL_FOR_DONATION_PROB:
      msg = helpers.adjoin_messages(
        None, 
        True, 
        ans.DISCLAIMER,
        ans.DONATION_ADDRS
        )
      reactions = DONATE_APPENDAGE_REACTS
    else:
      msg = helpers.adjoin_messages(
        None, 
        True, 
        ans.DISCLAIMER
        )
      reactions = None
    send_msg = await trade_chan.send(msg)
    if reactions:
      for react in reactions:
        await send_msg.add_reaction(react)


## commands ###
'''
@discord_client.command()
async def get_votes(cxt, number, *args):
  #count votes
  here = True if 'here' in args else False
  try:
    vote_chan = await discord_client.fetch_channel(VOTES_CHANS[1])
    messages = await vote_chan.history(limit=100, oldest_first=True).flatten()
    messages = _clear_empty_msgs(messages)
    vote_msg = messages[int(number)]
    votes = list()
    for react in VOTE_REACTIONS:
      reactions = gt(vote_msg.reactions, emoji=react)
      votes.append(reactions.count - 1)
    msg = ans.VOTES(number, *votes)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)
'''

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
    hashrate = kaspa.get_hashrate()
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
  if here: queries.pop()
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
  
@discord_client.command(hidden=True)
async def trade(cxt, *args):
  here = True if 'here' in args else False
  try:
    raise Exception
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@discord_client.command(hidden=True)
async def test(cxt, *args):
  '''test command'''
  here = True if 'here' in args else False
  ghost = True if 'ghost' in args else False
  try:
    msg = ans.SUCCESS
    if 'fail' in args:
      raise Exception('intentional fail')
    await _send(cxt, msg, here, dm_user=ghost)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

##helpers##

def _clear_empty_msgs(messages):
  return [msg for msg in messages if msg.content]


## post-processing / routing###

def _post_process_msg(cxt, msg, blockify=True):
  if random.random() < CALL_FOR_DONATION_PROB:
    if str(cxt.author.id) in DONATORS:
      appendage = '\n   ' + get('https://complimentr.com/api').json()['compliment']
    else:
      appendage = ans.DONATION_ADDRS
    return helpers.adjoin_messages(
      cxt.author.id,
      blockify,
      msg,
      appendage
      ), None
  else:
    return helpers.adjoin_messages(
      cxt.author.id,
      blockify,
      msg
      ), None

async def _process_exception(cxt, e, here):
  print(e)
  recv_msg = str(cxt.message.content)
  msg = ans.FAILED(recv_msg)
  await _send(cxt, msg, here)

## routing ##

async def _send(cxt, msg, here, blockify=True, dm_dev=False, dm_user=False):
  msg, reactions = _post_process_msg(cxt, msg, blockify)
  if dm_dev:
    dev_chan = await discord_client.fetch_user(int(DEV_ID))
    send_msg = await dev_chan.send(msg)
  elif dm_user:
    user_chan = await discord_client.fetch_user(int(cxt.author.id))
    send_msg = await user_chan.send(msg)
  elif isinstance(cxt.channel, discord.channel.DMChannel): #is dm
    send_msg = await cxt.send(msg)
  elif here is True:
    send_msg = await cxt.send(msg)
  elif cxt.channel.id in SER_TO_ALLOWED_CHANS[cxt.guild.id]:
    send_msg = await cxt.send(msg)
  else:
    dedicated_chan = discord_client.get_channel(SER_TO_ANSWER_CHAN[cxt.guild.id])
    send_msg = await dedicated_chan.send(msg)
    await cxt.message.delete()
  if reactions:
    for react in reactions:
      await send_msg.add_reaction(react)

discord_client.run(TOKEN)