import discord
import asyncio
from discord.ext import commands
import random

from defines import (answers as ans, devfund_addresses as dev_addrs, DEV_ID, TOKEN, SER_TO_ANSWER_CHAN, CALL_FOR_DONATION_PROB, DONATORS)
import helpers
import kaspa
from requests import get
import grpc
import traceback
import cryptoinfo

intents = discord.Intents.default().all()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

## events ##

@bot.event
async def on_ready():
  print(f'running {bot.user}...') 

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
async def devfund(cxt, window_size=None, *args):
  '''Display devfund balance'''
  here = True if 'here' in [window_size,] + list(args) else False
  if window_size == None or window_size == 'here':
    window_size = 86400 #daa_window
  else:
    window_size = int(window_size)
  try:
    balances = kaspa.get_balances(
      dev_addrs.MINING_ADDR,
      dev_addrs.DONATION_ADDR,
      )
    utxos = kaspa.get_utxo_entries([dev_addrs.MINING_ADDR,])
    stats = kaspa.get_stats()
    network_hashrate = int(stats['hashrate'])
    cut_off = int(stats['daa_score']) - window_size
    addr_percent = helpers.mining_stats([dev_addrs.MINING_ADDR,], utxos, cut_off, int(stats['daa_score']))[dev_addrs.MINING_ADDR]['network_percent']
    addr_hashrate = helpers.hashrate_from_percent_of_network(addr_percent, network_hashrate)
    addr_hashrate = helpers.normalize_hashrate(addr_hashrate)
    msg = ans.DEVFUND(*balances, addr_percent, addr_hashrate)
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
    print(start_block)
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
    print(market_data)
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
    print('window', len(detailed_blocks))
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

## Auto Moderator ##

### RE matching code ###
# This could prbly be replaced with a very good RE
import re 
REGEX_FLAGS = re.IGNORECASE 
BLACKLIST_HINTS = ['admin', \ 
                    'administrator',\
                    'mod',\
                    'moderator',\
                    'support',\
                    'help',\
                    'helper',\
                    'assistance',\
                    'official']
BLACKLIST_PREFS = ['+[^a-zA-Z]', \ 
                    '\A']
BLACKLIST_SUFFS = ['[^a-zA-Z]+',\
                    '$']

def thorough_match(s,h):
    for pre in BLACKLIST_PREFS:
        for su in BLACKLIST_SUFF:
            #p = re.compile(pre + h + su, REGEX_FLAGS)
            p = re.compile(f"{pre}{h}{su}", REGEX_FLAGS)
            if None != p.search(s):
                return True
    return False

def filter_by_regex(member):
    for s in [member.name, member.nick, member.display_name, member.raw_status]:
        for blh in BLACKLIST_HINTS:
            if -1 != s.find(blh):
                if thorough_match(s, blh):
                    return True
    return False

### End of RE matching code ###

### Captcha code ###
import captcha.image
import hashlib
import os

def rnd_for_captcha():
    # seeds defaultly with system time
    # can try to think of better ones (kaspa current price related??!)
    random.seed()
    r = random.randint(0,2<<22)
    return r

# This example code is taken from the code in 
# the captchasDotNet github python project
# secret is constant "secret" for demo, and we
# use 6 letters and so
def generate_captcha_with_captchas_net(id)
    r = str(rnd_for_captcha())
    urlc = f"https://image.captchas.net/?client=demo&random={r}"
    png_data = get(urlc)
    f = open(f'tmp_captcha-{r}.png','wb')
    f.write(png_data)
    f.close()
    s = f'secret{r}'
    m = hashlib.md5()
    m.update(bytes(s,'charmap'))
    dig = m.digest()
    alph = 'abcdefghkmnopqrstuvwxyz'
    ps = ''
    for i in range(0,6):
        ps += alph[dig[i]%len(alph)]
    return f'tmp_captcha-{id}.png',ps

def generate_simple_captcha(id)
    # Uses default fonts files that we can override 
    # if we want
    image = captcha.image.ImageCaptcha()
    r = str(rnd_for_captcha())
    # This is not thread safe, could result in false negative
    # if two userwe can use a lock here if
    # we are really scared that there would
    image.write(r, f'tmp_captcha-{r}.png')
    return f'tmp_captcha-{id}.png',r


#
#   - Generates captcha png file (currently using the 
#       simple captcha, note we can use the captchas.net one
#       instead) and a solution for it.
#   - Sends the file and a message to user, asking to enter the text in the 
#       file.
#   - validates the user's response.
#   - returns True if the user responded correctly
#
def validate_captcha(member):
    theid = member.id
    pth, ps = generate_simple_captcha(str(theid))
    #dmc = member.create_dm()
    dmc = await bot.fetch_user(theid)
    # can try and catch here but better for now to
    # except on it.
    f = open(pth,'rb')
    df = discord.File(f, filename='captcha.png')
    await dmc.send("Hello there!\n\
            In order to enter the server, please prove you are not a bot, by responding \
            to this message with the text appearing in the following image:", file=df)
    resp = [m async for m in dmc.history(limit=1)][0]
    
    f.close()
    
    # First check everything works, then delete the local file.
    # Note this should all be moved to a dedicated resource directory
    
    #os.remove(pth)

    if resp == ps:
        return True
    return False

### End Captcha code ###

'''
Note banning according to discord doc at discord.fandom.com/Wiki/Ban 
also bans the ip address and phone number from joining the server 
again. This will give us a problem as discussed about ip based 
banning (as then vpns will be banned and we do not necessarily 
want that).
'''
def should_ban_based_on_rules(member):
    if True == member.bot:
        return True
    if True == filter_by_regex(member):
        return True
    return False

def validate_captcha_member(member):
    return validate_captcha(member)

@bot.event
async def on_member_join(member):
    mem_guild = member.guild
    if "Server von jwj" == mem_guild.name:
      dev_chan = await bot.fetch_user(int(DEV_ID))
      send_msg = await dev_chan.send(f"member '{member.name}' joined server von jwj")
      if "alonko" == member.name: 
          await member.ban(reason="auto-ban")
      if "СарtchаBоt" == member.name:
          await member.ban(reason="auto-ban")
    

bot.run(TOKEN)
