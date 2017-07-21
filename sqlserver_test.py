import pyodbc
import pandas as pd

def get_db_cursor():
    server = 'tcp:coin.database.windows.net,1433'
    database = 'coinmarketcap'
    username = 'jimmy_ic@coin'
    password = '123qweASDF'
    driver= '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

def get_allcoinsymbols():
    sql = """\
        SELECT  Id,
                symbol,
                ticker,
                history,
                last14Days FROM dbo.coins
    """
    cursor = get_db_cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columnnames = [column[0] for column in cursor.description]
    df = pd.DataFrame.from_records(rows, columns=columnnames)
    
    return df


def set_coin_history(history):
    print history
    # for item in history:
    #     if not item:
    #         item = "NULL"
    sql = """\
        EXEC dbo.Stp_SetCoinHistory @date = ?,          
                                    @position = ?,         
                                    @name = ?,           
                                    @symbol = ?,         
                                    @category = ?,       
                                    @marketCap = ?,      
                                    @price = ?,          
                                    @availableSupply = ?,
                                    @volume24 = ?,       
                                    @change1h = ?,       
                                    @change24h = ?,      
                                    @change7d = ?        
    """
    cursor = get_db_cursor()
    cursor.execute(sql, history)
    cursor.commit()