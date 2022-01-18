from kaspy.kaspa_clients import RPCClient
from kaspy.utils.version_comparer import version as ver 
import logging 
from defines import HOST_IP, HOST_PORT
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_balances(*addrs, use_dedicated_node=True, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  if use_dedicated_node:
    cli.connect(HOST_IP, int(HOST_PORT))
  else:
    cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  balances = list()
  try:
    for addr in addrs:
      balance = cli.request('getBalanceByAddressRequest', {'address' : addr})
      if not balance['getBalanceByAddressResponse'].values():
        cli.close()
        get_balances(*addrs)
      balance = balance['getBalanceByAddressResponse']['balance']
      balances.append(int(balance) / 100000000)
  except:
    cli.close()
    get_balances(*addrs, use_dedicated_node=False, tries=tries+1)
  cli.close()
  return balances
   
def get_hashrate(use_dedicated_node=True, tries = 0):
  cli = RPCClient()
  if use_dedicated_node:
    cli.connect(HOST_IP, int(HOST_PORT))
  else:
    cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  try:
    diff =  int(cli.request('getBlockDagInfoRequest')['getBlockDagInfoResponse']['difficulty'])
  except:
    cli.close()
    get_hashrate(use_dedicated_node=False, tries=tries+1)
  return diff * 2
'''
def get_stats(use_dedicated_node=True, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  if use_dedicated_node:
    cli.connect(HOST_IP, int(HOST_PORT))
  else:
    cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  try:
    stats = defaultdict()
    blockdag_info = cli.request('getBlockDagInfoRequest')['getBlockDagInfoResponse']
    stats['circulating_supply'] = blockdag_info['blockCount']
    total_supply = 28_500_000_000
    percent_of_coins_mined = c
    virtualDaaScore = blockdag_info['virtualDaaScore']
    info = cli.request('getInfoRequest')['getInfoResponse']
    Transaction_rate 
  except:
    cli.close()
    get_hashrate(use_dedicated_node=False, tries=tries+1)
  pass
  '''