import requests
import json
import datetime

'''Not implemented yet'''

EXIBTRON = 'exibitron'
TXBIT = 'txbit'

EXCHANGE_TO_DISPLAYEXCHANGE = {
        EXIBTRON : 'EXIBTRON',
        TXBIT    : 'TxBit',
}

def format_pair_from_base(base_asset):
        return 'KAS/' + base_asset.upper() 

def create_ex_pair_from_base(base_asset, exchange):
        if exchange == EXIBTRON:
                return 'kas' + base_asset.lower()
        elif exchange == TXBIT:
                return 'KAS/'+base_asset.upper()
        else:
                raise Exception
        
def normalize_exchange_string(exchange):
        return exchange.lower()

def create_ex_pair_from_base(base_asset, exchange):
        if exchange == EXIBTRON:
                return 'kas' + base_asset.lower()
        elif exchange == TXBIT:
                return 'KAS/'+base_asset.upper()
        else:
                raise Exception
        
def get_trades(base_asset, exchnage, limit=10):
        if exchnage.lower() 

def get_trades_exibitron(base_asset, limit=10):
        ex_pair = create_ex_pair_from_base(base_asset, EXIBTRON)
        response = json.loads(requests.get(f'https://www.exbitron.com/api/v2/peatio/public/markets/{ex_pair}/trades?limit={limit}').text)
        orderbook = {
                'exchange': EXIBTRON,
                'pair' : format_pair_from_base(base_asset),
                'trades' : [
                        {       'Side' : 'Sell' if else 'buy'
                                'Amount' : float(trade['Quantity']), 
                                'Price' : float(trade['Price']),
                                'time' : datetime.datetime.fromtimestamp(float(trade['Tiestamp']))
                         } for trade in response
                        ]                    
        }
        return orderbook
        
def get_trades_txbit(base_asset, limit=10):
        ex_pair = create_ex_pair_from_base(base_asset, TXBIT)
        response = json.loads(requests.get(f'https://api.txbit.io/api/public/getmarkethistory?market={ex_pair}').text)['result']
        response = response[:min(len(response)-1, limit)]
        orderbook = {
                'exchange': TXBIT,
                'pair' : format_pair_from_base(base_asset),
                'trades' : [
                                {
                                'Amount' : float(trade['Quantity']), 
                                'Price' : float(trade['Price']),
                                'time' : datetime.datetime.fromtimestamp(float(trade['Tiestamp']))
                                } for trade in response
                        ]                    
        }
        return orderbook

def get_orderbook_exibitron(base_asset, limit=10):
        ex_pair = create_ex_pair_from_base(base_asset, EXIBTRON)
        response = json.loads(requests.get(f'https://www.exbitron.com/api/v2/peatio/public/markets/{ex_pair}/depth?limit={limit}').text)
        orderbook = {
                'exchange': EXIBTRON,
                'pair' : format_pair_from_base(base_asset),
                'bids' : response['high'],
                'asks'  : response['low'],
        }
        return orderbook
        
def get_orderbook_txbit(base_asset, limit=1):
        ex_pair = create_ex_pair_from_base(base_asset, TXBIT)
        response = json.loads(requests.get(f'https://api.txbit.io/api/public/getorderbook?market={ex_pair}&type=both').text)['result']
        response['buy'] = response['buy'][:min(len(response['buy'])-1, limit)]
        response['sell'] = response['sell'][:min(len(response['sell'])-1, limit)]
        orderbook = {
                'exchange': TXBIT,
                'pair' : format_pair_from_base(base_asset),
                'bids' : response['high'],
                'asks'  : response['low'],
        }
        return orderbook

def get_ticker_exibitron(base_asset):
        ex_pair = create_ex_pair_from_base(base_asset, EXIBTRON)
        response = json.loads(requests.get(f'https://www.exbitron.com/api/v2/peatio/public/{ex_pair}/kasusdt/tickers').text)
        ticker = {
                'exchange': EXIBTRON,
                'pair' : format_pair_from_base(base_asset),
                'high' : float(response['high']),
                'low'  : float(response['low']),
                'last' : float(response['last']),
                'volumne': float(response['volume']),
                'price_change' : float(response['price_change_percent'][:-1]) / 100
        }
        pass

def get_ticker_txbit(base_asset):
        ex_pair = create_ex_pair_from_base(base_asset, EXIBTRON)
        response = json.loads(requests.get(f'https://api.txbit.io/api/public/getmarketsummary?market={ex_pair}').text)['result']
        ticker = {
                'exchange'      :       TXBIT,
                'pair'          :       format_pair_from_base(base_asset),
                'high'          :       float(response['High']),
                'low'           :       float(response['Low']),
                'last'          :       float(response['Last']),
                'volumne'       :       float(response['BaseVolume']),
                'price_change'  :       (float(response['Last'])  - float(response['PrevDay'])) / 
                                        (float(response['Last'])  - float(response['PrevDay'])),
        }