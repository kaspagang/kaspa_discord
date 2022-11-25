from defines import kaspa_constants as kc
import re
import time
from datetime import datetime
import random

def random_colour():
        return random.choice(["yaml", "http", "arm"], )

def adjoin_messages(user_id, blockify = True, *msgs):
  sep="  ==============================================================================="
  nl = f'\n{sep}'
  if blockify:
    if user_id is None:
      return f"""```{random_colour()}
{nl.join(msgs)}```"""
    else:
      return f""""<@{user_id}>```{random_colour()}
{nl.join(msgs)}```"""
  elif not blockify:
    if user_id is None:
      return f"{nl.join(msgs)}"
    else:
      return f"<@{user_id}> \n\n {nl.join(msgs)}"


def sompis_to_kas(sompis, round_amount=None):
  if round:
    return round(sompis / 100000000, round_amount)
  return sompis / 100000000

def daa_score_to_date(current_daa, target_daa, current_timestamp):
  current_timestamp = round(current_timestamp)
  daa_diff = target_daa - current_daa
  return datetime.utcfromtimestamp(current_timestamp + round(daa_diff*1)).strftime('%d-%m-%Y %H:%M:%S')
  
def get_current_halving_phase(current_daa_score):
  for phase, def_phase in enumerate(kc.DEFLATIONARY_TABLE.values()):
    if def_phase['daa_range'].start <= current_daa_score < def_phase['daa_range'].stop:
      return phase

def get_coin_supply(target_daa_score):
  if target_daa_score >= list(kc.DEFLATIONARY_TABLE.values())[-1]['daa_range'].start:
    return kc.TOTAL_COIN_SUPPLY
  coin_supply = 0
  for i, def_phase in enumerate(kc.DEFLATIONARY_TABLE.values()):
    if target_daa_score in def_phase['daa_range']:
      coin_supply += def_phase['reward_per_daa']*(target_daa_score - def_phase['daa_range'].start)
      break
    else:
      coin_supply += def_phase['reward_per_daa']*(def_phase['daa_range'].stop - def_phase['daa_range'].start-1)
  return round(coin_supply) + kc.EXTRA_GAMENET_KAS

def rewards_in_range(daa_start, daa_end):
  if daa_start >= list(kc.DEFLATIONARY_TABLE.values())[-1]['daa_range'].start:
    return 0
  mining_rewards = 0
  for i, def_phase in enumerate(kc.DEFLATIONARY_TABLE.values()):
    if daa_start >= def_phase['daa_range'].start:
      start_phase = i
  for def_phase in list(kc.DEFLATIONARY_TABLE.values())[start_phase:]:
    if def_phase['daa_range'].start <= daa_end < def_phase['daa_range'].stop and def_phase['daa_range'].start <= daa_start < def_phase['daa_range'].stop:
      mining_rewards = (daa_end - daa_start) * def_phase['reward_per_daa']
      break
    elif def_phase['daa_range'].start <= daa_start < def_phase['daa_range'].stop:
      mining_rewards += (def_phase['daa_range'].stop - daa_start - 1) * def_phase['reward_per_daa']
    elif def_phase['daa_range'].start <= daa_end < def_phase['daa_range'].stop:
      mining_rewards += (daa_end - def_phase['daa_range'].start) * def_phase['reward_per_daa']
      break
    else:
      mining_rewards += (def_phase['daa_range'].stop - def_phase['daa_range'].start -1)*def_phase['reward_per_daa']
  return mining_rewards


def get_mining_rewards(current_daa_score, percent_of_network):
  rewards = dict()
  rewards['secound'] = rewards_in_range(current_daa_score, current_daa_score+1)*percent_of_network
  rewards['minute'] = rewards_in_range(current_daa_score, current_daa_score+60)*percent_of_network
  rewards['hour'] = rewards_in_range(current_daa_score, current_daa_score+60*60)*percent_of_network
  rewards['day'] = rewards_in_range(current_daa_score, current_daa_score+60*60*24)*percent_of_network
  rewards['week'] = rewards_in_range(current_daa_score, current_daa_score+60*60*24*7)*percent_of_network
  rewards['month'] = rewards_in_range(current_daa_score, current_daa_score+60*60*24*(365.25/12))*percent_of_network            
  rewards['year'] = rewards_in_range(current_daa_score, current_daa_score+60*60*24*(365.25))*percent_of_network
  return rewards

def normalize_hashrate(hashrate :int):
  if hashrate < 1_000: #
    return f'{round(hashrate, 2)} H/s' #Hash
  elif hashrate < 1_000_000:
    return f'{round(hashrate/1_000, 2)} KH/s' #Kilo
  elif hashrate < 1_000_000_000:
    return f'{round(hashrate/1_000_000, 2)} MH/s' #Mega
  elif hashrate < 1_000_000_000_000:
    return f'{round(hashrate/1_000_000_000, 2)} GH/s'#Giga
  elif hashrate < 1_000_000_000_000_000:
    return f'{round(hashrate/1_000_000_000_000, 2)} TH/s' #Tera
  elif hashrate < 1_000_000_000_000_000_000:
    return f'{round(hashrate/1_000_000_000_000_000, 2)} PH/s' #Peta
  elif hashrate < 1_000_000_000_000_000_000_000:
    return f'{round(hashrate/1_000_000_000_000_000_000, 2)} EH/s' #Exa

def hashrate_to_int(str_hashrate : str):
  val, suffix = extract_hashrate(str_hashrate)
  if suffix == 'KH':
    return val*1_000
  elif suffix == 'MH':
    return val*1_000_000
  elif suffix == 'GH':
    return val*1_000_000_000
  elif suffix == 'TH':
    return val*1_000_000_000_000
  elif suffix == 'PH':
    return val*1_000_000_000_000_000
  elif suffix == 'EH':
    return val*1_000_000_000_000_000_000
  elif suffix == 'H':
    return val

def hashrate_from_percent_of_network(percent_of_network, hashrate):
  return hashrate * percent_of_network

def percent_of_network(miner_hashrate, network_hashrate):
  if miner_hashrate <= network_hashrate:
    return miner_hashrate/network_hashrate
  else:
    return (miner_hashrate)/(miner_hashrate+network_hashrate)

def extract_hashrate(str_hashrate):
  val = float(re.findall(r'\d+(?:\.\d+)?', str_hashrate)[0])
  for suf in ['KH', 'MH', 'GH', 'TH', 'PH', 'EH', 'H']:
    if suf.lower() in str_hashrate.lower():
      suffix = suf
      break
  return val, suffix

def mining_stats(addrs, utxo_entries, daa_cut_off, current_daa):
  mining_stats = dict()
  for utxo_entry in utxo_entries:
    if 'isCoinbase' in utxo_entry['utxoEntry'].keys() and utxo_entry['utxoEntry']['isCoinbase'] and int(utxo_entry['utxoEntry']['blockDaaScore']) >= daa_cut_off:
      if utxo_entry['address'] in mining_stats:
        mining_stats[utxo_entry['address']]['daas'].append(int(utxo_entry['utxoEntry']['blockDaaScore']))
      else:
        mining_stats[utxo_entry['address']] = dict()
        mining_stats[utxo_entry['address']]['daas']= list()
        mining_stats[utxo_entry['address']]['daas'] = [int(utxo_entry['utxoEntry']['blockDaaScore']),]
  for stat in mining_stats.values():
    stat['daas'] = sorted(stat['daas'], reverse=True)
    '''
    if len(stat['daas']) >= 3:
      stat['average_daa_dist'] = sum([stat['daas'][i] - stat['daas'][i+1] for i, _ in enumerate(stat['daas'][:-1])])
    else: 
      stat['average_daa_dist'] =  0
    #stat['network_percent'] = 1 / stat['average_daa_dist']
    '''
    stat['network_percent'] = len(stat['daas']) / (current_daa -daa_cut_off)
  return mining_stats
    
def get_mining_addresses(blocks):
  addrs = dict()
  for block in blocks:
    for transaction in block['transactions']:
      if 'payload' in transaction and transaction['payload']:
        for output in transaction['outputs']:
          if output['verboseData']['scriptPublicKeyAddress'] in addrs:
            addrs[output['verboseData']['scriptPublicKeyAddress']] += 1
          else:
             addrs[output['verboseData']['scriptPublicKeyAddress']] = 1
  addrs = {k: str(round((v/sum(addrs.values()))*100, 1)) + '%' for k, v in sorted(addrs.items(), key=lambda item: item[1], reverse = True)}
  return addrs

def get_market_caps(current_value, circ_supply):
        market_caps = dict()
        market_caps["circ_m-cap"] = circ_supply * current_value / 1_000_000
        market_caps["dil_m-cap"] = kc.TOTAL_COIN_SUPPLY * current_value / 1_000_000
        return market_caps
  
#work in progress

def deflationay_phases(current_daa_score, start=None, end=None):
  if not start:
    start = get_current_halving_phase(current_daa_score)
  start = int(start)
  if end:
    end = int(end)+1
  elif not end:
    end = int(start)+1
  if start > 426:
    start = 426
  phases = {}
  timestamp = time.time()
  current_date = datetime.fromtimestamp(round(timestamp)).strftime('%d-%m-%Y %H:%M:%S')
  for phase, def_phase in list(kc.DEFLATIONARY_TABLE.items())[start:end]:
    if phase == 0: # special case because of 3 days down time
      start_date = daa_score_to_date(
      current_daa_score, def_phase['daa_range'].start, timestamp - 259_200
    )
    else:
      start_date = daa_score_to_date(
      current_daa_score, def_phase['daa_range'].start, timestamp
    )
    if phase == 426:
      end_date = '∞'
    else:
      end_date = daa_score_to_date(current_daa_score, def_phase['daa_range'].stop-1, timestamp)
    if def_phase['daa_range'].start <= current_daa_score < def_phase['daa_range'].stop:
      phases[phase] = {
      'active_phase' : True,
      'start_date' : start_date,
      'start_supply'  :  get_coin_supply(def_phase['daa_range'].start) - (kc.EXTRA_GAMENET_KAS if phase == 0 else 0),
      'end_date' : end_date,
      'end_supply'  :  get_coin_supply(def_phase['daa_range'].stop-1),
      'completion' : round(((current_daa_score - def_phase['daa_range'].start) / (def_phase['daa_range'].stop - 1 - def_phase['daa_range'].start)*100), 2),
      'rewards' : def_phase['reward_per_daa'],
      }
    elif def_phase['daa_range'].stop < current_daa_score:  
      phases[phase] = {
      'active_phase' : False,
      'start_date' : start_date,
      'start_supply'  :  get_coin_supply(def_phase['daa_range'].start) - (kc.EXTRA_GAMENET_KAS if phase == 0 else 0),
      'end_date' : end_date,
      'end_supply'  :  get_coin_supply(def_phase['daa_range'].stop-1) ,
      'completion' : 100,
      'rewards' : def_phase['reward_per_daa'],
      }
    elif def_phase['daa_range'].start > current_daa_score:
      phases[phase] = {
      'active_phase' : True,
      'start_date' : start_date,
      'start_supply'  :  get_coin_supply(def_phase['daa_range'].start) - (kc.EXTRA_GAMENET_KAS if phase == 0 else 0),
      'end_date' : end_date,
      'end_supply'  :  get_coin_supply(def_phase['daa_range'].stop-1),
      'completion' : 0,
      'rewards' : def_phase['reward_per_daa'],
      }
  return phases, current_date