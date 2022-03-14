from defines import kaspa_constants as kc
import re
import time

def adjoin_messages(user_id, blockify = True, *msgs):
  sep="  ==============================================================================="
  nl = f'\n{sep}'
  if blockify:
    if user_id is None:
      return f"```{nl.join(msgs)}```"
    return f"<@{user_id}>```{nl.join(msgs)}```"
  elif not blockify:
    return f"{nl.join(msgs)}"
  return f"<@{user_id}>```{nl.join(msgs)}```"

def get_coin_supply(target_daa_score):
  if target_daa_score >= list(kc.DEFLATIONARY_TABLE.values())[-1]['daa_range'].start:
    return kc.TOTAL_COIN_SUPPLY
  coin_supply = 0
  for def_phase in kc.DEFLATIONARY_TABLE.values():
    print(def_phase)
    if target_daa_score in def_phase['daa_range']:
      coin_supply += def_phase['reward_per_daa']*(target_daa_score - def_phase['daa_range'].start)
      break
    else:
      coin_supply += def_phase['reward_per_daa']*(def_phase['daa_range'].stop - def_phase['daa_range'].start-1)
  return round(coin_supply)

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
      print(def_phase['reward_per_daa'])
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
  print(rewards)
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

#work in progress
'''
def deflationay_phases(current_daa_score, display_amount=5):
  if display_amount == 0:
    daa_start = current_daa_score
    daa_end = current_daa_score
  else:
    daa_start = current_daa_score - kc.DEF_PHASE_INCREMENT*display_amount
    daa_end = current_daa_score + kc.DEF_PHASE_INCREMENT*display_amount
  if daa_start < 0:
    daa_start = 0
  if daa_end > 1133184600:
    daa_end = 1133184600
  for phase, def_phase in kc.DEFLATIONARY_TABLE.items():
    if def_phase['daa_range'].start <= daa_start < def_phase['daa_range'].stop:
      pass
    elif def_phase['daa_range'].start <= daa_end < def_phase['daa_range'].stop:
      break
    else:

    
      current_phase = phase
  for phase in list(kc.DEFLATIONARY_TABLE.items())[current_phase-display: current_phase+displaye]:
  
'''