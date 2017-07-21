import json
import requests
import pandas as pd
import numpy as np

"""This is a test"""
def get_answer():
    """Get an answer."""
    return True

def get_full_history(coin_symbol):
    '''Get a full history of coin history'''
    request_url = 'http://coinmarketcap.northpole.ro/api/v6/history/' + coin_symbol + '_2016.json'
    response = requests.get(request_url)
    history2016 = json.loads(response.text)
    request_url = 'http://coinmarketcap.northpole.ro/api/v6/history/' + coin_symbol + '_2017.json'
    response = requests.get(request_url)
    history2017 = json.loads(response.text)

    history = {'symbol': coin_symbol, 'history': history2016['history'].items() + history2017['history'].items()}
    return history

def get_df_full_history_usd(history):
    '''Only select USD as price currency into pandas DataFrame'''

    column_names = [
        "position",
        "name",
        "symbol",
        "category",
        "marketCap",
        "price",
        "availableSupply",
        "volume24",
        "change1h",
        "change24h",
        "change7d",
        "timestamp"
    ]

    data = []
    for date in history['history']:
        if hasattr(date[1]['marketCap'], 'usd'):
            date[1]['marketCap'] = date[1]['marketCap']['usd']
        else:
            date[1]['marketCap'] = None

        if hasattr(date[1]['price'], 'usd'):
            date[1]['price'] = date[1]['price']['usd']
        else:
            date[1]['price'] = None

        if hasattr(date[1]['volume24'], 'usd'):
            date[1]['volume24'] = date[1]['volume24']['usd']
        else:
            date[1]['volume24'] = None

        selected_row = []
        selected_row.append(date[0])
        for item in column_names:
            selected_row.append(date[1][item])
        data.append(selected_row)

    df = pd.DataFrame(data, columns = ["date"] + column_names)
    df['date'] = pd.to_datetime(df['date'], dayfirst='true')
    df['marketCap'] = df['marketCap'].astype('float64')
    df['price'] = df['marketCap'].astype('float64')
    df['volume24'] = df['marketCap'].astype('float64')
    df['availableSupply'] = df['availableSupply'].astype('float64')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.sort_values(by='date')
    del df['timestamp']
    return df
