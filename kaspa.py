from defines import answers as ans
from kaspy.kaspa_clients import RPCClient
from kaspy.utils.version_comparer import version as ver 
import logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_balance(addr):
  print('in balance')
  cli = RPCClient()
  cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  print('connected')
  try:
    balance = cli.request('getBalanceByAddressRequest', {'address' : addr})
    print(balance)
    if not balance['getBalanceByAddressResponse'].values():
      cli.close()
      get_balance(addr)
    balance = balance['getBalanceByAddressResponse']['balance']
  except:
    cli.close()
    get_balance(addr)
  print(balance, 'kas')
  cli.close()
  return int(balance) / 100000000
   
def get_hashrate():
    try:
        cli = RPCClient()
        cli.auto_connect()
        diff =  int(cli.request('getBlockDagInfoRequest')['getBlockDagInfoResponse']['difficulty'])
        return diff * 2
    except:
        return ans.FAILED 