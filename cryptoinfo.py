import requests

def kaspa_market_info(quote_asset: str = "usd"): #from coingeko 
        #nore: value is transalted to 1M kas
                
        quote_asset = quote_asset.lower()
        market_info = dict()
        
        resp = requests.get(
                "https://api.coingecko.com/api/v3/coins/kaspa?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
                ).json()
        
        
        market_info["quote"] = quote_asset.upper()
        market_info["value"] = float(resp["market_info"]["current_price"][quote_asset]) * 1_000_000
        market_info['high'] = resp["market_info"]["high_24h"][quote_asset]
        market_info['low'] = resp["market_info"]["low_24h"][quote_asset]
        market_info['volume'] = resp["market_info"]["total_volume"][quote_asset]
        market_info['price_change'] =  resp["market_info"]["price_change_24h_in_currency"][quote_asset]
        
        return market_info
        