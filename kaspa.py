from defines import answers as ans
from kaspy.kaspa_clients import RPCClient
from kaspy.utils.version_comparer import version as ver 
import logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_balances(*addrs):
  cli = RPCClient()
  cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  balances = list()
  try:
    for addr in addrs:
      balance = cli.request('getBalanceByAddressRequest', {'address' : addr})
      print(balance)
      if not balance['getBalanceByAddressResponse'].values():
        cli.close()
        get_balances(*addrs)
      balance = balance['getBalanceByAddressResponse']['balance']
      balances.append(int(balance) / 100000000)
  except:
    cli.close()
    get_balances(*addrs)
  print(balance, 'kas')
  cli.close()
  return balances
   
def get_hashrate():
  cli = RPCClient()
  cli.auto_connect()
  diff =  int(cli.request('getBlockDagInfoRequest')['getBlockDagInfoResponse']['difficulty'])
  return diff * 2