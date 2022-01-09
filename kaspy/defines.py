from .utils.version_control import version as ver



#### KASPAD defines #####

# Available services:
RPC_SERVICE = 'RPC' # use _SERVICE suffix, RPC is defined in kaspy.proros.messages_pb_grpc.py
P2P_SERVICE = 'P2P' # use _SERVICE suffix, P2P is defined in kaspy.proros.messages_pb_grpc.py

## Default ports for services:
RPC_DEF_PORT = 16110
P2P_DEF_PORT = 16111

# Subnetworks:

## Subnetwork names:
MAINNET = 'mainnet'
TESTNET = 'testnet'
DEVNET = 'devnet'
SIMNET = 'simnet'

## Available subnetworks:
SUBNETWORKS = (MAINNET,TESTNET,DEVNET,SIMNET)

# Kaspad, latest version:
LATEST_KASPAD_VERSION = ver(0, 11, 9)

#### PORT defines #####

# PORT defines:
OPEN = 'open'
CLOSED = 'closed'