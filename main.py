import discord
import asyncio
from discord.ext import commands, tasks
import random

from defines import (answers as ans, devfund_addresses as dev_addrs, rustfund_addresses as rus_addrs, kaspa_constants as kc, STAT_CHANS, CALL_FOR_DONATION_PROB, DONATORS, SER_TO_ANSWER_CHAN)

import bs4
import helpers
import kaspa
from requests import get
import grpc
import traceback
import cryptoinfo
import time

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)


## events ##

@bot.event
async def on_ready():
  print(f'running {bot.user}...')
  my_background_task.start()

@tasks.loop(seconds= 1, count=1)
async def my_background_task():
        await bot.wait_until_ready()
        last_updates = dict()
        for _, ids in STAT_CHANS.items():
                for id in ids:
                        last_updates[id] = 0
        while True:
                for stat_type, chan_ids in STAT_CHANS.items():
                        all_valid_ids = [chan_id for chan_id in chan_ids if isinstance(chan_id, int)]
                        if bool(all_valid_ids):
                                if stat_type == "value":
                                        try:
                                                value = round(int(cryptoinfo.kaspa_market_info()["value"]) / 1_000_000, 7)
                                        except:
                                                value = "Error"
                                        
                                        for chan_id in all_valid_ids:
                                                if time.time() < last_updates[chan_id] + 60 * 5: continue
                                                channel = bot.get_channel(chan_id)
                                                if channel.name == f"value: {value}": continue
                                                print("updating: ", chan_id, " ", value)
                                                await channel.edit(name=f"value: {value}")
                                                last_updates[chan_id] = time.time()
                                if stat_type in ["hashrate", "TPS", "reward", "next-phase"]:
                                        try:
                                                        stats = kaspa.get_stats()
                                        except Exception as e:
                                                print(e)
                                                stats = "Error"
                                        if stat_type == "TPS":
                                                try:
                                                        if stats == "Error": raise Exception
                                                        blocks = kaspa.get_blocks(stats['pruning_point'])
                                                        detailed_blocks = kaspa.get_blocks_detailed(blocks[-100])
                                                        tps, kasps = 0, 0
                                                        for block in detailed_blocks:
                                                                #if not block['verboseData']['isChainBlock']: continue
                                                                tps += len(block['transactions'])
                                                                for tx in block['transactions']:
                                                                        for output in tx['outputs']:
                                                                                kasps += int(output['amount'])
                                                        tps = round(tps / len(detailed_blocks), 1)
                                                        kasps = round(helpers.sompis_to_kas(kasps) / len(detailed_blocks))
                                                except Exception as e:
                                                        print(e)
                                                        tps, kasps = "Error", "Error"
                                                for chan_id in all_valid_ids:
                                                        if time.time() < last_updates[chan_id] + 60 * 5: continue
                                                        channel = bot.get_channel(chan_id)
                                                        if channel.name == f"TPS: {tps} ({int(kasps):,} KAS/s)": continue
                                                        print("updating: ", chan_id, " ", tps, " ", kasps)
                                                        await channel.edit(name=f"TPS: {tps} ({int(kasps):,} KAS/s)")
                                                        last_updates[chan_id] = time.time()
                                        elif stat_type in  "hashrate":
                                                try:
                                                        if stats == "Error": raise Exception
                                                        norm_hashrate = helpers.normalize_hashrate(int(stats['hashrate']))
                                                except:
                                                        norm_hashrate = "Error"
                                                for chan_id in all_valid_ids:
                                                        if time.time() < last_updates[chan_id] + 60 * 5: continue
                                                        channel = bot.get_channel(chan_id)
                                                        if channel.name == f"hashrate: {norm_hashrate}": continue
                                                        print("updating: ", chan_id, " ", norm_hashrate)
                                                        await channel.edit(name=f"hashrate: {norm_hashrate}")
                                                        last_updates[chan_id] = time.time()
                                        elif stat_type in ["reward", "next-phase"]:
                                                try:
                                                        if stats == "Error": raise Exception
                                                        phase = helpers.get_current_halving_phase(int(stats['daa_score']))
                                                        reward = kc.DEFLATIONARY_TABLE[phase]["reward_per_daa"]
                                                except Exception as e:
                                                        print(e)
                                                        phase = "Error"
                                                if stat_type == "reward":
                                                        try:
                                                                if phase == "Error": raise Exception  
                                                                reward = round(kc.DEFLATIONARY_TABLE[phase]["reward_per_daa"], 2)  
                                                        except Exception as e:
                                                                print(e)
                                                                reward = "Error"
                                                        for chan_id in all_valid_ids:
                                                                if time.time() < last_updates[chan_id] + 60 * 5: continue
                                                                channel = bot.get_channel(chan_id)
                                                                if channel.name == f"block-reward: {reward}": continue
                                                                print("updating: ", chan_id, " ", reward)
                                                                await channel.edit(name=f"block-reward: {reward}")
                                                                last_updates[chan_id] = time.time()
                                                elif stat_type == "next-phase":
                                                        try:
                                                                if phase == "Error": raise Exception
                                                                next_daa = kc.DEFLATIONARY_TABLE[phase]["daa_range"].stop
                                                                date = helpers.daa_score_to_date(int(stats['daa_score']), next_daa, time.time()).split()[0]
                                                                #date = f"{date.day}/{date.month}/{date.year}"
                                                        except Exception as e:
                                                                print(e)
                                                                date = "Error"
                                                        for chan_id in all_valid_ids:
                                                                if time.time() < last_updates[chan_id] + 60 * 5: continue
                                                                channel = bot.get_channel(chan_id)
                                                                if channel.name == f"next-phase: {date}": continue
                                                                print("updating: ", chan_id, " ", date)
                                                                await channel.edit(name=f"next-phase: {date}")
                                                                last_updates[chan_id] = time.time()
                                elif stat_type == "supply":
                                        try:
                                                circ_supply = helpers.sompis_to_kas(kaspa.get_circ_supply())
                                        except:
                                                circ_supply = "Error"
                                        for chan_id in all_valid_ids:
                                                if time.time() < last_updates[chan_id] + 60 * 5: continue
                                                channel = bot.get_channel(chan_id)
                                                if channel.name == f"supply: {int(circ_supply):,}": continue
                                                print("updating: ", chan_id, " ", circ_supply)
                                                await channel.edit(name=f"supply: {int(circ_supply):,}")
                                                last_updates[chan_id] = time.time()
                                
                                elif stat_type == "twitter":
                                        try:
                                                followers = get("https://api.coingecko.com/api/v3/coins/kaspa?localization=false&tickers=false&market_data=false&community_data=true&developer_data=false&sparkline=false").json()["community_data"]["twitter_followers"]
                                        except Exception as e:
                                                print(e)
                                                followers = "Error"
                                        for chan_id in all_valid_ids:
                                                if time.time() < last_updates[chan_id] + 60 * 5: continue
                                                channel = bot.get_channel(chan_id)
                                                if channel.name == f"twitter: {followers}": continue
                                                print("updating: ", chan_id, " ", followers)
                                                await channel.edit(name=f"twitter: {followers}")
                                                last_updates[chan_id] = time.time()
                                
                                elif stat_type == "discord":
                                        try:
                                                guild = await bot.fetch_guild(ALLOWED_SERVERS[0], with_counts=True)
                                        except:
                                                guild = "Error"
                                        for chan_id in all_valid_ids:
                                                if time.time() < last_updates[chan_id] + 60 * 5: continue
                                                print(guild.approximate_member_count)
                                                channel = bot.get_channel(chan_id)
                                                if channel.name == f"discord: {guild.approximate_member_count}": continue
                                                print("updating: ", chan_id, " ", guild.approximate_member_count)
                                                await channel.edit(name=f"discord: {guild.approximate_member_count}")
                                                last_updates[chan_id] = time.time()
                                
                                elif stat_type == "telegram":
                                        try:
                                                members = get("https://api.coingecko.com/api/v3/coins/kaspa?localization=false&tickers=false&market_data=false&community_data=true&developer_data=false&sparkline=false").json()["community_data"]["telegram_channel_user_count"]
         
                                        except Exception as e:
                                                print(e)
                                                members = "Error"
                                        for chan_id in all_valid_ids:
                                                if time.time() < last_updates[chan_id] + 60 * 5:  continue
                                                channel = bot.get_channel(chan_id)
                                                if channel.name == f"telegram: {members}": continue
                                                print("updating: ", chan_id, " ", members)
                                                await channel.edit(name=f"telegram: {members}")
                                                last_updates[chan_id] = time.time()
                await asyncio.sleep(60 * 5)
## commands ###
        
@bot.command()
async def balance(cxt, address, *args):
  '''Get balance of address
     Note: command will fail if balance = 0
  '''
  here = True if 'here' in args else False
  try:
    balances = kaspa.get_balances(address)
    msg = ans.BALANCE(*balances)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception_balance(cxt, e, here)

@bot.command()
async def devfund(cxt, *args):
  '''Display devfund balance'''
  here = True if 'here' in list(args) else False
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
async def rustfund(cxt, *args):
  '''Display rustfund balance'''
  here = True if 'here' in list(args) else False
  try:
    rust_addresses = list(a[1] for a in vars(rus_addrs).items() if not a[0].startswith("_"))
    print(rust_addresses)
    balances = kaspa.get_balances(
      *rust_addresses
      )
    
    msg = ans.RUST_FUND(list(zip(rust_addresses, balances)))
    await _send(cxt, msg, here)
  except Exception as e:
    await _process_exception(cxt, e, here)


@bot.command()
async def address_mining(cxt, address, window_size = 7200, *args):
  '''Estimate network share associated with address
     note: this command will fail if 
              1) a certain treshold of mining is not met
              2) address is mining to a pool
  '''
  here = True if 'here' in [window_size,] + list(args) else False
  if window_size == 'here':
    window_size = 7200 #2hour 60*60*2
  try:
    balance = int(kaspa.get_balances(address)[0])
    utxos = kaspa.get_utxo_entries([address,])
    stats = kaspa.get_stats()
    start_block = kaspa.get_blocks(stats['pruning_point'])[-window_size]
    network_hashrate = kaspa.estimate_network_hashrate(start_block, window_size)
    cut_off = int(stats['daa_score']) - window_size
    addr_percent = helpers.mining_stats([address,], utxos, cut_off, int(stats['daa_score']))[address]['network_percent']
    addr_hashrate = helpers.hashrate_from_percent_of_network(addr_percent, network_hashrate)
    addr_hashrate = helpers.normalize_hashrate(addr_hashrate)
    network_hashrate = helpers.normalize_hashrate(network_hashrate)
    msg = ans.ADDR_STATS(address, network_hashrate, balance, addr_percent, addr_hashrate, window_size)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception_address_minging(cxt, e, here)


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
async def mining_reward(cxt, own_hashrate, suffix=None, *args):
  '''Calculate mining rewards with specified hashrate
      
      Input: <float_or_integer>xH/s (without spaces!)
      
      Formular: (<own_h/s>/<net_h/s> x reward x <timeframe_in_secounds>)*

      *Halving events are integrated into the reward calculation over the timeframe.
  
      Disclaimer: output is only an approximation, and influenced by current dips and spikes in the network hashrate, as well as growth of the network over time.
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
    circ_supply = helpers.sompis_to_kas(kaspa.get_circ_supply())
    msg = ans.COIN_STATS(circ_supply)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)
    
@bot.command()
async def market_data(cxt, quote_asset = "usd", *args):
  '''Get market_data'''
  here = True if 'here' in [quote_asset, *args] else False
  if quote_asset == None or quote_asset == "here":
          quote_asset = 'usd'
  try:
    circ_supply = helpers.sompis_to_kas(kaspa.get_circ_supply())
    market_data = cryptoinfo.kaspa_market_info(quote_asset)
    market_data.update(helpers.get_market_caps(market_data["value"], circ_supply))
    msg = ans.MARKET_DATA(market_data)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command()
async def value(cxt, quote_asset = "usd", *args):
  '''Get Kas value per 1M'''
  here = True if 'here' in [quote_asset, *args] else False
  if quote_asset == None or quote_asset == "here":
          quote_asset = 'usd'
  try:
    market_data = cryptoinfo.kaspa_market_info(quote_asset)
    msg = ans.VALUE(market_data)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)


@bot.command()
async def halving(cxt, start=None, end=None, *args):
  '''Display progress of deflationary periods'''
  here = True if 'here' in [start, end, *args] else False
  try:
    stats = kaspa.get_stats()
    circ_supply = helpers.sompis_to_kas(kaspa.get_circ_supply())
    if start == 'here':
      start = None
    if end =='here':
      end = None
    if start == 'all':
      start = 0
      end = 426
    phase_info, current_date, = helpers.deflationay_phases(int(stats['daa_score']), start, end)
    msg = ans.DEF_INFO(phase_info, current_date, circ_supply)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)
  
@bot.command(hidden=True)
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

@bot.command()
async def top_miners(cxt, amount = 5, window = 3600, *args):
  '''WORK IN PROGRESS : Displays info on current top miners''' 
  here = True if 'here' in (window, amount, *args) else False
  try:
    #raise Exception
    stats = kaspa.get_stats()
    blocks = kaspa.get_blocks(stats['pruning_point'])
    target_block = blocks[-100]
    detailed_blocks = kaspa.get_blocks_detailed(target_block)
    mining_addrs = dict(list(helpers.get_mining_addresses(detailed_blocks).items())[:20])
    msg = ans.TOP_GAINERS(mining_addrs)
    await _send(cxt, msg, here)
  except (Exception, grpc.RpcError) as e:
    await _process_exception(cxt, e, here)

@bot.command(hidden=True)
async def mining_rewards(cxt, own_hashrate, suffix=None, *args):
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
  
async def _process_exception_address_minging(cxt, e, here):
  print(e, traceback.format_exc())
  recv_msg = str(cxt.message.content)
  msg = ans.FAILED_ADDR_MINING(recv_msg)
  await _send(cxt, msg, here)
  
async def _process_exception_balance(cxt, e, here):
  print(e, traceback.format_exc())
  recv_msg = str(cxt.message.content)
  msg = ans.FAILED_BALANCE(recv_msg)
  await _send(cxt, msg, here)
    
## Exchanges ##

  #Maybe TO-DO

## Routing ##

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
