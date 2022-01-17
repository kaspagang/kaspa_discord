class commands:

    DEVFUND = 'devfund' 
    HELP = 'help'
    DONATE = 'donate'
    SUGGESTION = 'suggestion'
    TIP_OF_THE_DAY = 'tip-of-the-day'
    BALANCE = 'balanace'
    STATS = 'stats'
    MINING_REWARDS = 'mining_rewards'
    MINING_RATE = 'mining-rate'
    USEFUL_LINKS = 'links'
    VALUE = 'value'

class devfund_addresses:
    MINING_ADDR = 'kaspa:pzhh76qc82wzduvsrd9xh4zde9qhp0xc8rl7qu2mvl2e42uvdqt75zrcgpm00'
    DONATION_ADDR = 'kaspa:precqv0krj3r6uyyfa36ga7s0u9jct0v4wg8ctsfde2gkrsgwgw8jgxfzfc98'

class answers:
    
    class placeholders:
        ADDR = '<kaspa_address>'
        ADDRS = f'{ADDR} {ADDR} ...'
        MSG = '<message>'
        HASHRATE = '<mhash/sec>'
        WINDOWSIZE = '<windowsize>'
        
    FAILED = 'Could not process you command'
    PREFACE = '''Thanks for using kaspabot!'''
    APPENDIX =f'''Please consider a donation:
@devfund: {devfund_addresses.DONATION_ADDR}
@kaspabot: kaspa:qzyjckdvgyxgwqj8zztw7qkqylsp864fyquzg8ykmmwkz58snu85zlk0mfy89'''
    HELP = f'''
        ${commands.DEVFUND}:
        list addresses and balances associated with the devfund

        `${commands.BALANCE} {placeholders.ADDRS}`
        Display balance of the supplied kaspa addresses.

        `${commands.SUGGESTION} {placeholders.MSG}`
        Send a suggestion for the discord bot development
        note suggestions will be sent to via this bot to 'me' as a dm
        
        `${commands.USEFUL_LINKS} `
        NotImplemented
        returns useful links and guides related to kaspa
        '''
    
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
    'Kaspa website'(https://kaspanet.org/)
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
    {500*60*60*24*7*(365.25/12)*network_percent} KAS/month
    {500*60*60*24*7*365.25*network_percent} KAS/year'''

#for possible future:

'''
 `${commands.MINING_RATE} {placeholders.ADDRS} {placeholders.WINDOWSIZE}`:
        NotImplemented
        Infer approx. mining rate from address 
        note: This is not an accurate representation!
        1) mining rate is infered by 'last 5 '500 KAS' TXS recevied / num_of_seconds elapsed'

        `${commands.MINING_REWARDS} {placeholders.HASHRATE}`:
        NotImplemented
        calculate approx. blocks per second, minute, hour and day with your hashrate compared to the current network hashrate

        `${commands.TIP_OF_THE_DAY}`:
        NotImplemented
        return the tip of the day

        ${commands.DONATE}:
        NotImplemented
        list donation addresses - devfund

        ${commands.HELP}:
        repeat this response

        ${commands.STATS}:
        NotImplemented
        retrive network stats

        `${commands.VALUE}`:
        NotImplemented
        infer approx. KAS to USD value
        note: This is not an accurate representation!
        1) value is calculated by a rolling average of the last 3 SELL and BUY orders from the trade channel
        2) only orders in the format: 
        
        `Order: Sell/BUY KAS
        Price:  1M KAS = xxxUSDT`
        
        are respected  
        
        3) large deviations from mean are excluded as trolling
'''