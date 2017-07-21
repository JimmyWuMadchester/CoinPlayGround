'''This is a test to get coin history data from coinmarketcap'''

import helpers
import sqlserver_test

def main():
    '''entry point'''
    
    
    df_coinsymbols = sqlserver_test.get_allcoinsymbols()
    for symbol in df_coinsymbols['symbol']:
        print symbol
        history_json = helpers.get_full_history(symbol)
        df_history = helpers.get_df_full_history_usd(history_json)

        tuples = [tuple(x) for x in df_history.values]
        for row in tuples:
           sqlserver_test.set_coin_history(row)
    
    
if __name__ == "__main__":
    main()
