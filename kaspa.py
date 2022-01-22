from kaspy.kaspa_clients import RPCClient
from kaspy.utils.version_comparer import version as ver 
import logging 
import grpc
from defines import HOST_IP, HOST_PORT
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_balances(*addrs, use_dedicated_node=True, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT))
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  except (Exception, grpc.RpcError) as e:
    cli.close()
    get_balances(use_dedicated_node=False, tries=tries+1)
  balances = list()
  try:
    for addr in addrs:
      balance = cli.request('getBalanceByAddressRequest', {'address' : addr})
      if not balance['getBalanceByAddressResponse'].values():
        cli.close()
      balance = balance['getBalanceByAddressResponse']['balance']
      balances.append(int(balance) / 100000000)
  except (Exception, grpc.RpcError) as e:
    cli.close()
    get_balances(*addrs, use_dedicated_node=False, tries=tries+1)
  cli.close()
  return balances
   
def get_hashrate(use_dedicated_node=True, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT))
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  except (Exception, grpc.RpcError) as e:
    cli.close()
    get_hashrate(use_dedicated_node=False, tries=tries+1)
  try:
    diff = int(cli.request('getBlockDagInfoRequest', timeout=4)['getBlockDagInfoResponse']['difficulty'])
  except (Exception, grpc.RpcError) as e:
    cli.close()
    get_hashrate(use_dedicated_node=False, tries=tries+1)
  return diff * 2

def get_circulating_coins(use_dedicated_node=True, tries=0):
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT))
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  except (Exception, grpc.RpcError) as e:
    cli.close()
    cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  except (Exception, grpc.RpcError) as e:
    circulating_supply =  int(cli.request('getBlockDagInfoRequest')['getBlockDagInfoResponse']['blockCount'])*500
  except (Exception, grpc.RpcError) as e:
    cli.close()
    get_hashrate(use_dedicated_node=False, tries=tries+1)
  return circulating_supply

def get_stats(use_dedicated_node=True, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT))
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,9), utxoindex=True)
  except (Exception, grpc.RpcError) as e:
    cli.close()
    get_stats(use_dedicated_node=False, tries=tries+1)
  try:
    stats = dict()
    blockdag_info = cli.request('getBlockDagInfoRequest')['getBlockDagInfoResponse']
    print(blockdag_info)
    stats['block_count'] = blockdag_info['blockCount']
    stats['header_count'] = blockdag_info['headerCount']
    stats['parent_hashes'] = blockdag_info['virtualParentHashes']
    stats['tip_hashes'] = blockdag_info['tipHashes']
    stats['blocks_per_secound'] = blockdag_info['pastMedianTime']
    stats['difficulty'] = blockdag_info['difficulty']
    stats['hashrate'] = int(stats['difficulty'])*2
    stats['daa_score'] = blockdag_info['virtualDaaScore']
    print(stats)
  except (Exception, grpc.RpcError) as e:
    cli.close()
  return stats