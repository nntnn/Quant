from pykrx import stock
import pandasgui as pg 

# https://appia.tistory.com/430

df = stock.get_index_ticker_list()
pg.show(df)
indexdata = {}
for item in df :
    if item != '2001' and item != '1001':
        detailitem =stock.get_index_portfolio_deposit_file(item)
        indexname=stock.get_index_ticker_name(item)
        print(indexname)
 
        for eitem in detailitem :
            Value = stock.get_market_ticker_name(eitem)
            print(eitem +"\t"+Value)
