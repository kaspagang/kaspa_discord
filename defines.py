import os

DEV_ID = os.environ['DEV_ID']
TOKEN = os.environ['TOKEN']
HOST_IP = os.environ['HOST_IP']
HOST_PORT = os.environ['HOST_PORT']

class devfund_addresses:
    MINING_ADDR = 'kaspa:pzhh76qc82wzduvsrd9xh4zde9qhp0xc8rl7qu2mvl2e42uvdqt75zrcgpm00'
    DONATION_ADDR = 'kaspa:precqv0krj3r6uyyfa36ga7s0u9jct0v4wg8ctsfde2gkrsgwgw8jgxfzfc98'

class answers:

    FAILED = 'Could not process you command'
    
    DEVFUND = lambda mining_addr_value, donation_addr_value : f'''
    Donation addresses:
      1) {devfund_addresses.DONATION_ADDR}
        {donation_addr_value} KAS 
    Mining addresses:
      1) {devfund_addresses.MINING_ADDR} 
        {mining_addr_value} KAS
    ==========================================================
    TOTAL:  {mining_addr_value + donation_addr_value} KAS'''

    BALANCE = lambda balance : f'''
    {balance} KAS'''

    SUGGESTION = f'''Thanks for your suggestion!'''

    HASHRATE = lambda norm_hashrate : f'''
    Kaspa is currently running @ {norm_hashrate}''' 
    
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
    {500*60*60*24*365.25*network_percent} KAS/year
    For info type: $help mining_reward'''