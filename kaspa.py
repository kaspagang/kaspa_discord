from defines import answers as ans
from kaspy.kaspa_clients import RPCClient

def get_balance(addr):
    try:
        cli = RPCClient()
        cli.auto_connect(min_kaspad_version='v0.11.9')
        balance = cli.request('getBalanceByAddressRequest', {'addr' : addr})['balance']
        cli.close()
        return balance
    except:
        return ans.FAILED 

def get_hashrate():
    try:
        cli = RPCClient()
        cli.auto_connect()
        diff =  int(cli.request('getBlockDagInfoRequest')['difficulty'])
        return diff * 2
    except:
        return ans.FAILED 