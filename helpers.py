from defines import kaspa_constants as kc

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
  if target_daa_score >= list(kc.DEFLATIONARY_TABLE.items())[-1][0]:
    return kc.TOTAL_COIN_SUPPLY
  coin_supply = 0
  last_daa = 0
  last_reward = 500
  for item in kc.DEFLATIONARY_TABLE.items():
    if item[0] == 0:
      continue
    else:
      daa, reward = item
      if coin_supply < daa:
        coin_supply += last_reward*(target_daa_score-last_daa)
        break
      else:
        coin_supply += last_reward*(daa-last_daa)
      last_reward = reward
      last_daa = daa
  return coin_supply
  
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
  str_hashrate = str_hashrate.replace(" ", "")
  if str_hashrate[-4:] == 'KH/s':
    hash_digit = float(str_hashrate[:-4])
    return hash_digit*1_000
  elif str_hashrate[-4:] == 'MH/s':
    print(str_hashrate[:-4])
    hash_digit = float(str_hashrate[:-4])
    return hash_digit*1_000_000
  elif str_hashrate[-4:] == 'GH/s':
    hash_digit = float(str_hashrate[:-4])
    return hash_digit*1_000_000_000
  elif str_hashrate[-4:] == 'TH/s':
    hash_digit = float(str_hashrate[:-4])
    return hash_digit*1_000_000_000_000
  elif str_hashrate[-4:] == 'PH/s':
    hash_digit = float(str_hashrate[:-4])
    return hash_digit*1_000_000_000_000_000
  elif str_hashrate[-4:] == 'EH/s':
    hash_digit = float(str_hashrate[:-4])
    return hash_digit*1_000_000_000_000_000_000
  elif str_hashrate[-3:] == 'H/s':
    hash_digit = float(str_hashrate[:-3])
    return hash_digit
  