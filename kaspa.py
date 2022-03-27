from kaspy.kaspa_clients import RPCClient
from kaspy.utils.version_comparer import version as ver 
import logging 
import grpc
from defines import HOST_IP, HOST_PORT, TRY_DEDICATED_NODE 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_balances(*addrs, use_dedicated_node=TRY_DEDICATED_NODE, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT))
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,12), utxoindex=True)
  except (Exception, grpc.RpcError) as e:
    cli.close()
    return get_balances(use_dedicated_node=False, tries=tries+1)
  balances = list()
  try:
    for addr in addrs:
      balance = cli.request('getBalanceByAddressRequest', {'address' : addr}, timeout=4)
      if not balance['getBalanceByAddressResponse'].values():
        cli.close()
      balance = balance['getBalanceByAddressResponse']['balance']
      balances.append(int(balance) / 100000000)
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return get_balances(*addrs, use_dedicated_node=False, tries=tries+1)
  cli.close()
  return balances

def get_stats(use_dedicated_node=TRY_DEDICATED_NODE, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT))
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,12), utxoindex=True)
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return get_stats(use_dedicated_node=False, tries=tries+1)
  try:
    stats = dict()
    blockdag_info = cli.request('getBlockDagInfoRequest',timeout=4)['getBlockDagInfoResponse']
    stats['block_count'] = blockdag_info['blockCount']
    stats['header_count'] = blockdag_info['headerCount']
    stats['pruning_point'] = blockdag_info['pruningPointHash']
    stats['parent_hashes'] = blockdag_info['virtualParentHashes']
    stats['tip_hashes'] = blockdag_info['tipHashes']
    stats['timestamp'] = blockdag_info['pastMedianTime']
    stats['difficulty'] = blockdag_info['difficulty']
    stats['hashrate'] = stats['difficulty']*2
    stats['daa_score'] = blockdag_info['virtualDaaScore']
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return get_stats(use_dedicated_node=False, tries=tries+1)
  cli.close()
  return stats

def get_utxo_entries(addrs, use_dedicated_node=TRY_DEDICATED_NODE, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT),  max_receive_size= -1)
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,13), utxoindex=True, max_receive_size= -1)
  except (Exception, grpc.RpcError) as e:
    cli.close()
    return get_utxo_entries(use_dedicated_node=False, tries=tries+1)
  try:
    print(addrs)
    utxo_entries = list(cli.request('getUtxosByAddressesRequest', {'addresses' : addrs})['getUtxosByAddressesResponse']['entries'])
    #utxos = [utxo['utxoEntry'] for utxo in utxo_entries]
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return get_utxo_entries(addrs, use_dedicated_node=False, tries=tries+1)
  cli.close()
  return utxo_entries

def get_blocks(start_block_hash, use_dedicated_node=TRY_DEDICATED_NODE, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT),  max_receive_size= -1)
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,13), utxoindex=True,  max_receive_size= -1)
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return get_blocks(use_dedicated_node=False, tries=tries+1)
  try:
    blocks = cli.request('getVirtualSelectedParentChainFromBlockRequest', {'startHash' : start_block_hash})['getVirtualSelectedParentChainFromBlockResponse']['addedChainBlockHashes']
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return get_blocks(use_dedicated_node=False, tries=tries+1)
  cli.close()
  return blocks

def get_blocks_detailed(start_block_hash, use_dedicated_node=TRY_DEDICATED_NODE, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT),  max_receive_size= -1)
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,13), utxoindex=True,  max_receive_size= -1)
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return get_blocks_detailed(start_block_hash, use_dedicated_node=False, tries=tries+1)
  try:
    blocks_detailed = cli.request('getBlocksRequest', {'lowHash' : start_block_hash, 'includeBlocks': True, 'includeTransactions' : True})['getBlocksResponse']['blocks']
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return get_blocks_detailed(start_block_hash, use_dedicated_node=False, tries=tries+1)
  cli.close()
  return blocks_detailed

def estimate_network_hashrate(start_block_hash, window_size, use_dedicated_node=TRY_DEDICATED_NODE, tries = 0):
  if tries == 3:
    raise Exception
  cli = RPCClient()
  try:
    if use_dedicated_node:
      cli.connect(HOST_IP, int(HOST_PORT),  max_receive_size= -1)
    else:
      cli.auto_connect(min_kaspad_version=ver(0,11,13), utxoindex=True)
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return estimate_network_hashrate(start_block_hash, window_size, use_dedicated_node=False, tries=tries+1)
  try:
    network_hashrate = cli.request('estimateNetworkHashesPerSecondRequest', {'windowSize' : window_size, 'startHash' : start_block_hash})['estimateNetworkHashesPerSecondResponse']['networkHashesPerSecond']
    print('hashrate', network_hashrate)
  except (Exception, grpc.RpcError) as e:
    print(e)
    cli.close()
    return estimate_network_hashrate(start_block_hash, window_size, use_dedicated_node=False, tries=tries+1)
  cli.close()
  return int(network_hashrate)