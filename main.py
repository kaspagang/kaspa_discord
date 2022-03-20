import discord
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
import kaspa
import random
from defines import (answers as ans, devfund_addresses as dev_addrs, DEV_ID, TOKEN, SER_TO_ANSWER_CHAN, CALL_FOR_DONATION_PROB, INTERVAL, TRADE_OFFER_CHANS, DONATORS, TRADE_DIS_INTERVALS, SER_TO_TRADE_CHANS)
import helpers
from requests import get
import grpc
import traceback
from Levenshtein import ratio as levenshtein_ratio

keep_alive()
intents = discord.Intents.default().all()
bot = commands.Bot(command_prefix='$', intents=intents)

## events ##

@bot.event
async def on_ready():
  print(f'running {bot.user}...')
  bot.loop.create_task(send_intermittently())

#fraud detectiion
  
@bot.event
async def on_member_update(member_before, member_after):
  #print(f'member updated: {member_before.display_name} -> {member_after.display_name}')
  if member_before.display_name != member_after.display_name:
    print(f'checking altered user: {member_before.display_name} -> {member_after.display_name}')
    await check_impersonations(member_after)
  pass

@bot.event
async def on_user_update(member_before, member_after):
  #print(f'user updated: {member_before.display_name} -> {member_after.display_name}')
  if member_before.display_name != member_after.display_name:
    print(f'checking altered user: {member_before.display_name} -> {member_after.display_name}')
    await check_impersonations(member_after)
  pass

@bot.event
async def on_member_join(member_new):
  #print(f'checking new user: {member_new}')
  await check_impersonations(member_new)    
   
async def check_impersonations(member_check):
  for guild_member in member_check.guild.members:
      if guild_member.id != member_check.id:
        lev_percent = levenshtein_ratio(member_check.display_name, guild_member.display_name)
        if lev_percent > 0.75:
          print(f'found {round(lev_percent*100)} simularity between target :{guild_member.display_name} and impersonator: {member_check.display_name}')
          if random.random() < CALL_FOR_DONATION_PROB:
            msg = helpers.adjoin_messages(
              None, 
              False, 
              ans.SIMILAR_MEMBER(member_check.id, member_check.display_name, guild_member.id, guild_member.display_name, lev_percent),
              ans.DONATION_ADDRS
              )
          else:
            msg = helpers.adjoin_messages(
              None, 
              False, 
              ans.SIMILAR_MEMBER(member_check.id, member_check.display_name, guild_member.id, guild_member.display_name, lev_percent),
              )
          trade_chan_id = SER_TO_TRADE_CHANS[int(member_check.guild.id)]
          trade_chan = await bot.fetch_channel(trade_chan_id)
          await trade_chan.send(msg)
      
## intermittent posts ##

async def send_intermittently():
  i = 1
  while True:
    if i % TRADE_DIS_INTERVALS == 0:
      for trade_chan_id in TRADE_OFFER_CHANS:
        await trade_disclaimer(trade_chan_id)
    await asyncio.sleep(INTERVAL)

##time_based events###

async def trade_disclaimer(chan_id):
  '''send disclaimer to trade channel every hour'''
  trade_chan = await bot.fetch_channel(chan_id)
  messages = await trade_chan.history(limit=10).flatten()
  message_ids = [message.author.id for message in messages]
  if bot.user.id in message_ids:
    pass
  else:
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
    await trade_chan.send(msg)

## commands ###

@bot.command()
async def balance(cxt, address, *args):
  '''Get balance of address'''
  here = True if 'here' in args else False
  try:
    balances = kaspa.get_balances(address)
    msg = ans.BALANCE(*balances)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command()
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

@bot.command()
async def hashrate(cxt, *args):
  '''Get network hashrate'''
  here = True if 'here' in args else False
  try:
    stats = kaspa.get_stats()
    norm_hashrate = helpers.normalize_hashrate(int(stats['hashrate']))
    msg = ans.HASHRATE(norm_hashrate)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    print(e)
    await _process_exception(cxt, e, here)

@bot.command()
async def useful_links(cxt, *args):
  '''List of useful links'''
  here = True if 'here' in args else False
  try:
    msg = ans.USEFUL_LINKS
    await _send(cxt, msg, here, blockify=False)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)


@bot.command()
async def mining_reward(cxt, own_hashrate, suffix=None, *args):
  '''Calculate mining rewards with specified hashrate
      
      Input: <float_or_integer>xH/s (without spaces!)
      
      Formular: <own_h/s>/<net_h/s>*500*<timeframe_in_secounds>
      
      Disclaimer: output is only an approximation, and influenced by current dips and spikes in the network hashrate, as well as growth of the network over time. Also, halving events are currently not included in the calculation. 
  '''
  here = True if 'here' in [suffix, *args] else False
  try:
    stats = kaspa.get_stats()
    network_hashrate = int(stats['hashrate'])
    own_hashrate = own_hashrate + suffix if suffix else own_hashrate
    own_hashrate = helpers.hashrate_to_int(own_hashrate)
    percent_of_network = helpers.percent_of_network(own_hashrate, network_hashrate)
    rewards = helpers.get_mining_rewards(int(stats['daa_score']), percent_of_network)
    msg = ans.MINING_CALC(rewards)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command()
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


@bot.command()
async def joke(cxt, *args):
  '''I tell a joke, you laugh'''
  here = True if 'here' in args else False
  try:
    msg = get('https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt').text
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)


@bot.command()
async def my_source_code(cxt, *args):
  '''source code for reference'''
  here = True if 'here' in args else False
  try:
    msg = 'https://github.com/kaspagang/kaspa_discord'
    await _send(cxt, msg, here, blockify=False)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command()
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

@bot.command()
async def donate(cxt, *args):
  '''Tips are welcome! - Displays donation addresses'''
  here = True if 'here' in args else False
  try:
    msg = ans.DONATION_ADDRS
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command()
async def dag_info(cxt, *args):
  '''Query dag information'''
  here = True if 'here' in args else False
  try:
    stats = kaspa.get_stats()
    msg = ans.DAG_STATS(stats)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command()
async def coin_supply(cxt, *args):
  '''Get current coin supply'''
  here = True if 'here' in args else False
  try:
    stats = kaspa.get_stats()
    circ_supply = helpers.get_coin_supply(int(stats['daa_score']))
    msg = ans.COIN_STATS(circ_supply)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command()
async def halving(cxt, start=None, end=None, *args):
  '''Display progress of deflationary periods'''
  here = True if 'here' in [start, end, *args] else False
  try:
    stats = kaspa.get_stats()
    if start == 'here':
      start = None
    if end =='here':
      end = None
    if start == 'all':
      start = 0
      end = 426
    current_supply = helpers.get_coin_supply(int(stats['daa_score']))
    phase_info, current_date, = helpers.deflationay_phases(int(stats['daa_score']), start, end)
    msg = ans.DEF_INFO(phase_info, current_date, current_supply)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)
  
@bot.command(hidden=True)
async def test(cxt, *args):
  '''test command'''
  print(*args)
  here = True if 'here' in args else False
  ghost = True if 'ghost' in args else False
  print('test')
  try:
    msg = ans.SUCCESS
    if 'fail' in args:
      raise Exception('intentional fail')
    await _send(cxt, msg, here, dm_user=ghost)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command(hidden=True)
async def mining_rewards(cxt, own_hashrate, suffix=None, *args):
  print(own_hashrate, suffix, args)
  await cxt.invoke(bot.get_command('mining_reward'), own_hashrate=own_hashrate, suffix=suffix, *args)
  
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
  print(e, traceback.format_exc())
  recv_msg = str(cxt.message.content)
  msg = ans.FAILED(recv_msg)
  await _send(cxt, msg, here)

## routing ##

async def _send(cxt, msg, here, blockify=True, dm_dev=False, dm_user=False):
  msg, reactions = _post_process_msg(cxt, msg, blockify)
  print(msg)
  if dm_dev:
    dev_chan = await bot.fetch_user(int(DEV_ID))
    send_msg = await dev_chan.send(msg)
  elif dm_user:
    user_chan = await bot.fetch_user(int(cxt.author.id))
    send_msg = await user_chan.send(msg)
  elif isinstance(cxt.channel, discord.channel.DMChannel): #is dm
    send_msg = await cxt.send(msg)
  elif here is True:
    send_msg = await cxt.send(msg)
  elif int(cxt.channel.id) == SER_TO_ANSWER_CHAN[cxt.guild.id]:
    send_msg = await cxt.send(msg)
  else:
    dedicated_chan = bot.get_channel(SER_TO_ANSWER_CHAN[cxt.guild.id])
    send_msg = await dedicated_chan.send(msg)
    await cxt.message.delete()
  if reactions:
    for react in reactions:
      await send_msg.add_reaction(react)

bot.run(TOKEN)
