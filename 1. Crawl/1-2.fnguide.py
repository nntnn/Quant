import pandas as pd
import pandasgui as pg

import requests as rq
from urllib import parse
from bs4 import BeautifulSoup as bs
import lxml

lnk = 'https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&gicode=A005930'
#lnk_parse = parse.urlparse(lnk)
#lnk_parts = parse.parse_qs(lnk_parse.query)

#code = '000660'
#lnk_parts['gicode'] = 'A'+code
#parse.urlunparse(lnk_parts)
##lnk_parts = lnk_parts._replace(query = parse.urlencode(qs))
#print(lnk_parts)
#url = parse.urlunparse(lnk_parts)

try:
    resp = rq.get(lnk)
    bs_res = bs(resp.content, "lxml")
    tbs = bs_res.find_all('table', {'class':'us_table_ty1 h_fix zigbg_no'})
    print(tbs)
    try:
        dfs = pd.read_html(str(tbs))
        for df in dfs:
            print(df.duplicated().sum())
            df = df.set_index('IFRS 연결')
            #df = df.drop(['Per Share','Dividends','Multiples','FCF'])
            pg.show(df)
            # IFRS 연결
    except Exception as ex2:
        print(ex2)

except Exception as ex:
    print('rq.get failed.', ex)
