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
    MINING_ADDR = ''
    DONATION_ADDR = ''

class answers:
    
    class placeholders:
        ADDR = '<kaspa_address>'
        ADDRS = f'{ADDR} {ADDR} ...'
        MSG = '<message>'
        HASHRATE = '<mhash/sec>'
        WINDOWSIZE = '<windowsize>'
        
    FAILED = 'Could not process you command'
    INITAL_GREETING = lambda partner : f'Hello {partner}!'
    TIPS = lambda botname : f''' 
    Thanks for using {botname}\n\n
    Please consider a donation:\n
    discord guy : kaspa:qzyjckdvgyxgwqj8zztw7qkqylsp864fyquzg8ykmmwkz58snu85zlk0mfy89
    devfund     : {devfund_addresses.DONATION_ADDR}
    
    '''
    HELP = f'''
        ${commands.DEVFUND}:
        list addresses and balances associated with the devfund

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

        `${commands.BALANCE} {placeholders.ADDRS}`
        NotImplemented
        Display balance of the supplied kaspa addresses.

        `${commands.SUGGESTION} {placeholders.MSG}`
        NotImplemented
        Send a suggestion for the discord bot development
        note suggestions will be sent to via this bot to 'me' as a dm
        
        `${commands.USEFUL_LINKS} `
        NotImplemented
        returns useful links and guides related to kaspa
        '''
    
    DEVFUND = lambda mining_addr_value, donation_addr_value : f'''
    {devfund_addresses.DONATION_ADDR}     :   {donation_addr_value} KAS 
    {devfund_addresses.MINING_ADDR}     :   {mining_addr_value} KAS
    TOTAL:  {mining_addr_value + donation_addr_value} KAS  
    '''