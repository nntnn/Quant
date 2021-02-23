import pandas as pd
import pandasgui as pg

import requests as rq
from urllib import parse
from bs4 import BeautifulSoup as bs
import lxml

from selenium import webdriver

import time
import os
# ============ DB파트 ========== 나중에 모듈로 만들어야함 -> 파이썬 패키지 관리하는 방법 배우기
import pandas as pd
from time import gmtime, strftime
#from sqlalchemy import create_engine
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb	

def mysqlCON():
    HN, PORT, USER, PW, DB, CHARSET = 'ntntn.mooo.com', 6352, 'dart', 'kye6121!!', 'DART', 'utf8'
    con_str_fmt = "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}"
    con_str = con_str_fmt.format(USER, PW, HN, PORT, DB, CHARSET)
    print(con_str)
    
    engine = sqlalchemy.create_engine(con_str)
    conn = engine.connect()
    print(conn)

    return conn
# ===========================================================================================

def linkparse():
    lnk = 'https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&gicode=' #A005930
    lnk_parse = parse.urlparse(lnk)
    lnk_parts = parse.parse_qs(lnk_parse.query)

    code = '000660'
    lnk_parts['gicode'] = 'A'+code
    parse.urlunparse(lnk_parts)
    #lnk_parts = lnk_parts._replace(query = parse.urlencode(qs))
    #print(lnk_parts)
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
        #print(lst, lst.find(rm_txt))
        if lst.find(rm_txt) != -1:
            indexlist[lst_idx] = lst[:lst.find(rm_txt)]
        #lst = lst.replace(lst, rm_txt)
    #print(indexlist)
    df = df.set_index(pd.Series(indexlist))
    return df

def report(code, conn):
    opt = webdriver.ChromeOptions()
    opt.add_argument('headless')

    # 웹드라이버를 통해 fnguide 페이지에 접속
    drv = webdriver.Chrome('_exec/chromedriver.exe', options=opt)
    drv.implicitly_wait(3)
    try:
        lnks = ['https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&gicode=',        # 투자지표
               'http://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=',   # 재무비율
               ]
        lnks_params = [
            {'class':'us_table_ty1 h_fix zigbg_no'},    # 투자지표
            {'class':'us_table_ty1 h_fix zigbg_no'},     # 재무비율
                      ]
        lnks_name = [
            'INV_INDEX_KOSPI',
            'FIN_PORTION_KOSPI',
            ]

        for lnk_i, lnk in enumerate(lnks):
            lnks[lnk_i] += code
        
        lnk_i = 1
        lnk = lnks[lnk_i]
        print(lnk)

        # 뷰티풀 수프로 테이블을 스크래핑
        drv.get(lnk)
        bs_res = bs(drv.page_source, 'lxml')
        drv.quit()

        # requests로 테이블 스크래핑
        #resp = rq.get(lnk)
        #print(resp.content.decode('utf-8'))
        #bs_res = bs(resp.content, "lxml")
        
        tbs = bs_res.find_all('table', lnks_params[lnk_i])

        if len(tbs) != 0:
            try:
                dfs = pd.read_html(str(tbs))
                for df in dfs:
                    print(df)
                    df = df.set_index(df.columns.tolist()[0]) # 테이블의 iloc[0,0]을 index로 설정.

                    # 중복열 drop
                    df = pd_dup_col(df)

                    # 인덱스 문자 깔끔하게 정리
                    df = pd_remove_txt(df, '계산에 참여한 계정')

                    # 행열 바꾸기
                    df = df.transpose()

                    # index를 종목코드:연도/최종월 형태로 바꾸기
                    indexlist = df.index.tolist()
                    for lst_idx, lst in enumerate(indexlist):
                        #print(code[:code.find('\n')])
                        indexlist[lst_idx] = code[:code.find('\n')] + ':' + lst
                        indexlist[lst_idx] = indexlist[lst_idx][:indexlist[lst_idx].find('/')]
                    print(indexlist)
                    df = df.set_index(pd.Series(indexlist))
                    df.index.name = 'ticker:year'
                    df.reset_index()
                    print(df)

                    # df dtype 정의. dict={'column name':sqlalchemy.types.type(n), }
                    columnlist = df.columns.tolist()
                    idxname = df.index.name
                    print(columnlist, idxname)
                    dd = {}     # stands for df_dtype
                    dd[idxname]=sqlalchemy.types.String(12)
                    #for col in columnlist:
                    #    dd['col'] = sqlalchemy.types.Float()
                    print(dd)

                    # DB 연결
                    df.to_sql(name = lnks_name[lnk_i], con = conn, if_exists='append', index=True, dtype=dd)

                    # df 확인해보기
                    #pg.show(df)
                    if idx_i == 1:
                        break
                    # IFRS 연결
            except Exception as ex2:
                print(ex2)
        else:
            print('no table found.', len(tbs))
    
    except Exception as ex:
        print('rq.get failed.', ex)
        drv.quit()
    time.sleep(2)

def __main__():
    corpcode_txt = open("1_Crawl/corplist.txt", "r")
    lines = corpcode_txt.readlines()
    conn = mysqlCON()

    for line in lines:
        report('A'+line, conn)

if __name__ == "__main__":
    __main__()