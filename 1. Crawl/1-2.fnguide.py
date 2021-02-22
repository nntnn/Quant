import pandas as pd
import pandasgui as pg

import requests as rq
from urllib import parse
from bs4 import BeautifulSoup as bs
import lxml



def linkparse():
    lnk = 'https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&gicode=' #A005930
    lnk_parse = parse.urlparse(lnk)
    lnk_parts = parse.parse_qs(lnk_parse.query)

    code = '000660'
    lnk_parts['gicode'] = 'A'+code
    parse.urlunparse(lnk_parts)
    #lnk_parts = lnk_parts._replace(query = parse.urlencode(qs))
    print(lnk_parts)
    url = parse.urlunparse(lnk_parts)

def report(code):
    try:
        lnk = 'https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&gicode='
        lnk += code

        resp = rq.get(lnk)
        bs_res = bs(resp.content, "lxml")
        tbs = bs_res.find_all('table', {'class':'us_table_ty1 h_fix zigbg_no'})
        #print(tbs)

        try:
            dfs = pd.read_html(str(tbs))
            for df in dfs:
                print(df.duplicated().sum())
                df = df.set_index('IFRS 연결')
                df = df.drop(['Per\xa0Share','Dividends','Multiples','FCF'])

                indexlist = df.index.tolist()
                rm_txt = '계산에 참여한 계정'
                for lst_idx, lst in enumerate(indexlist):
                    print(lst, lst.find(rm_txt))
                    if lst.find(rm_txt) != -1:
                        indexlist[lst_idx] = lst[:lst.find(rm_txt)]
                    #lst = lst.replace(lst, rm_txt)
                print(indexlist)
            
                df = df.set_index(pd.Series(indexlist))
                df = df.transpose()

                indexlist = df.index.tolist()
                for lst_idx, lst in enumerate(indexlist):
                    indexlist[lst_idx] = code + ':' + lst
                print(indexlist)
                df = df.set_index(pd.Series(indexlist))
                pg.show(df)

                # IFRS 연결
        except Exception as ex2:
            print(ex2)

    except Exception as ex:
        print('rq.get failed.', ex)


def __main__():
    corpcode_txt = open("1. Crawl/corplist.txt", "r")
    lines = corpcode_txt.readlines()

    for line in lines:
        report('A'+line)

if __name__ == "__main__":
    __main__()