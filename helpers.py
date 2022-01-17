from defines import answers as ans
def adjoin_messages(*msgs):
  nl = '\n\n'
  return f"```{nl.join(msgs)}```"

def post_process_messages(*msgs):
  return adjoin_messages(ans.PREFACE, *msgs, ans.APPENDIX)

def normalize_hashrate(hashrate :int):
  if hashrate < 1_000: #kilo
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
  print(str_hashrate)
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