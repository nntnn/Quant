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

def pd_dup_col(df:pd.DataFrame):
    # df = df.drop(['Per\xa0Share','Dividends','Multiples','FCF'])
    indexlist = df.index.tolist()   # indexlist 최신화
    dellist = []
    for i,v in enumerate(indexlist):
        chklist = df.iloc[i,:].tolist()
        chk_sum = 0
        for chk in chklist:
            if v == chk:
                chk_sum += 1
        if chk_sum == len(chklist):
            dellist.append(v)
    print(dellist)
    df = df.drop(dellist)
    return df

def pd_remove_txt(df:pd.DataFrame, rm_txt):
    indexlist = df.index.tolist()
    for lst_idx, lst in enumerate(indexlist):
        print(lst, lst.find(rm_txt))
        if lst.find(rm_txt) != -1:
            indexlist[lst_idx] = lst[:lst.find(rm_txt)]
        #lst = lst.replace(lst, rm_txt)
    print(indexlist)
    df = df.set_index(pd.Series(indexlist))
    return df

def report(code):
    try:
        # 가치지표 파싱
        lnks = ['https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&gicode=',        # 투자지표
               'http://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=',   # 재무비율
               ]
        lnks_params = [
            {'class':'us_table_ty1 h_fix zigbg_no'},    # 투자지표
            {'class':'us_table_ty1 h_fix zigbg_no'},     # 재무비율
                      ]
        for lnk_i, lnk in enumerate(lnks):
            lnks[lnk_i] += code
        
        lnk_i = 1
        lnk = lnks[lnk_i]

        resp = rq.get(lnk)
        bs_res = bs(resp.content, "lxml")
        tbs = bs_res.find_all('table', lnks_params[lnk_i])
        #print(tbs)

        try:
            dfs = pd.read_html(str(tbs))
            for df in dfs:
                #print(df)
                df = df.set_index(df.columns.tolist()[0]) # 테이블의 iloc[0,0]을 index로 설정.

                # 중복열 drop
                df = pd_dup_col(df)

                # 인덱스 문자 깔끔하게 정리
                df = pd_remove_txt(df, '계산에 참여한 계정')


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