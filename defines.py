import os

DEV_ID = os.environ['DEV_ID']
TOKEN = os.environ['TOKEN']
HOST_IP = os.environ['HOST_IP']
HOST_PORT = os.environ['HOST_PORT']
DONATOR1 = os.environ['DONATOR1']

DONATORS = [
  DONATOR1,
  DEV_ID #for testing
]

DEL_INTERVAL = 60
ALLOWED_SERVERS = [599153230659846165]

SER_TO_ALLOWED_CHANS = {
  599153230659846165 :{ # kaspa
    934815196361404467
  },
  932389256838643755 : [ #test server
    934753516575158282
    ]
  }

SER_TO_ANSWER_CHAN = {
  599153230659846165 : 934815196361404467, #kaspa
  932389256838643755 : 934753516575158282, #test server
}

TRY_DEDICATED_NODE = False

CALL_FOR_DONATION_PROB = 1/27 # more reduction 

DISCLAIMER_INTERVAL = 60*60

##channels##

TRADE_OFFER_CHAN = 910316340735262720
DEVFUND_CHAN = 922204606946234398

class kaspa_constants:
  TOTAL_COIN_SUPPLY = 28_500_000_000

class devfund_addresses:
    MINING_ADDR = 'kaspa:pzhh76qc82wzduvsrd9xh4zde9qhp0xc8rl7qu2mvl2e42uvdqt75zrcgpm00'
    DONATION_ADDR = 'kaspa:precqv0krj3r6uyyfa36ga7s0u9jct0v4wg8ctsfde2gkrsgwgw8jgxfzfc98'

class kasper_addresses:
    DONATION_ADDR = 'kaspa:qp33anhdnnsfzg474jd3s5csuaf0k9kn6cvy3pfcx9rnezak5qkhgskuztcum'

class answers:
    DISCLAIMER = '''Disclaimer:
  
  This is a kind reminder that #trade channel is not moderated by the server mods, core devs, treasurers or any other constituents of the Kaspa community. This channel was created to accommodate traders which bogged down the community channel, having created it does not impose any responsibility for the actions of any buyer, seller, escrow service etc. on any particular community member. Please be mindful of that and careful with your money.'''

    FAILED = lambda recv_msg : f'''
  Could not process: {recv_msg}'''

    SUCCESS = f'''SUCCESS!!''' # for test command

    DAG_STATS =lambda stats : f'''
    Hashrate      :   {stats['hashrate']}
    Difficulty    :   {stats['difficulty']}
    DAA score     :   {stats['daa_score']}
    Tip Hashes    :   {stats['tip_hashes']}'''

    COIN_STATS = lambda circulating_coins : f'''
    Circulating supply  : {circulating_coins}
    Total supply        : {kaspa_constants.TOTAL_COIN_SUPPLY}
    Percent mined       : {round(circulating_coins/kaspa_constants.TOTAL_COIN_SUPPLY*100, 2)}%'''
    
    DEVFUND = lambda mining_addr_value, donation_addr_value : f'''
  =======================================================================
  Donation addresses:

    • {devfund_addresses.DONATION_ADDR}

  -----------------------------------------------------------------------
    Amount: {donation_addr_value} KAS 
  =======================================================================
  Mining addresses:

    • {devfund_addresses.MINING_ADDR}
    
  -----------------------------------------------------------------------
    Amount: {mining_addr_value} KAS
  =======================================================================
  TOTAL:    {mining_addr_value + donation_addr_value} KAS'''

    BALANCE = lambda balance : f'''
    {balance} KAS'''

    SUGGESTION = f'''
  Thanks for your suggestion!'''

    HASHRATE = lambda norm_hashrate : f'''
  Kaspa is currently running @ {norm_hashrate}''' 
    
    CONSIDER_DONATION = f'''
    Please consider a donation:
    Kasper : {kasper_addresses.DONATION_ADDR}
    Devfund: {devfund_addresses.DONATION_ADDR}
    '''

    USEFUL_LINKS = '''
  Kaspa website: 
    https://kaspanet.org/
  Source code: 
    https://github.com/kaspanet/kaspad
  Quick start guide:
    tinyurl.com/ym8sbas7
  Node bootstrap:
    http://kaspadbase.com/
  Kaspa Wiki:
    https://kaspawiki.net/
  Kaspa for desktop (KDX):
    https://kdx.app/
  Web wallet:
    https://wallet.kaspanet.io/
  Paper wallet generator:
    https://github.com/svarogg/kaspaper/releases/latest 
  Faucet:
    https://faucet.kaspanet.io/
  Dashboards:
    http://kasboard-mainnet.daglabs-dev.com/
    http://kasboard.cbytensky.org/
  Livefeed:
    http://kgi-mainnet.daglabs-dev.com/
  Block explorers:
    http://katnip.cbytensky.org/
    http://blockexplorer.kaspanet.org/
  Cpu-miner:
    https://github.com/elichai/kaspa-miner/releases
  Gpu-miner:
    https://github.com/tmrlvi/kaspa-miner/releases'''

    MINING_CALC = lambda network_percent : f'''
  {500*network_percent} KAS/sec
  {500*60*network_percent} KAS/min
  {500*60*60*network_percent} KAS/hour
  {500*60*60*24*network_percent} KAS/day
  {500*60*60*24*7*network_percent} KAS/week
  {500*60*60*24*(365.25/12)*network_percent} KAS/month
  {500*60*60*24*365.25*network_percent} KAS/year'''

    DONATION_ADDRS = f'''
Please consider a donation towards:
• Kasperbot: {kasper_addresses.DONATION_ADDR}
• Devfund  : {devfund_addresses.DONATION_ADDR}'''