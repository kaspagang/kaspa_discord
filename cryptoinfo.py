import requests

def kaspa_market_info(quote_asset: str = "usd"): #from coingeko 
        #nore: value is transalted to 1M kas
                
        quote_asset = quote_asset.lower()
        market_info = dict()
        
        resp = requests.get(
                "https://api.coingecko.com/api/v3/coins/kaspa?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
                ).json()
        
        print(resp)
        market_info["quote"] = quote_asset.upper()
        market_info["value"] = float(resp["market_data"]["current_price"][quote_asset]) * 1_000_000
        market_info['high'] = resp["market_data"]["high_24h"][quote_asset] * 1_000_000
        market_info['low'] = resp["market_data"]["low_24h"][quote_asset] * 1_000_000
        market_info['volume'] = resp["market_data"]["total_volume"][quote_asset] 
        market_info['price_change'] =  resp["market_data"]["price_change_percentage_24h_in_currency"][quote_asset]
       
        print(market_info)
         
        return market_info
        