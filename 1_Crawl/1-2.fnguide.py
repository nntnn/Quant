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

def_path = 'C:/Users/Admin/source/repos/nntnn/Quant/'

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
    df = df.drop(dellist)
    print('deleted columns', dellist)
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

def report(code, conn, code_idx):
    opt = webdriver.ChromeOptions()
    opt.add_argument('headless')

    # 웹드라이버를 통해 fnguide 페이지에 접속
    drv = webdriver.Chrome(def_path + '_exec/chromedriver.exe', options=opt)
    drv.implicitly_wait(10)
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
        lnks_captions = [
            '기업가치 지표',
            '재무비율',
            ]
        lnks_comment = [
            {0:['기업가치 지표','']},
            {1:['재무비율 [누적]','재무비율 [3개월]']}
            ]

        for lnk_i, lnk in enumerate(lnks):
            lnks[lnk_i] += code
        
        #for lnk_i in list(range(0, len(lnks))):
        lnk_i = code_idx 
        lnk = lnks[lnk_i]
        print(lnk, lnk_i)

        # 뷰티풀 수프로 테이블을 스크래핑
        drv.get(lnk)
        #print(type(drv.page_source), drv.page_source)
        
        #find comments in lnks_comment
        txts = drv.page_source
        print( ((lnks_comment[lnk_i])[lnk_i])[0], ((lnks_comment[lnk_i])[lnk_i])[1] )
        start = txts.find(((lnks_comment[lnk_i])[lnk_i])[0])
        end = txts.find(((lnks_comment[lnk_i])[lnk_i])[1])
        
        if(((lnks_comment[lnk_i])[lnk_i])[1] == ''):
            txts = txts[start:]
        else:
            txts = txts[start:end]    
        #print(txts)
        #bs_res = bs(drv.page_source, 'lxml')
        bs_res = bs(txts, 'lxml')
        drv.quit()

        # find specific captions 
        for caption in bs_res.find_all('caption'):
            if caption.get_text() == lnks_captions[lnk_i]:
                tbs = caption.find_parent('table', lnks_params[lnk_i])

        # VS
        # tbs = bs_res.find_all('table', lnks_params[lnk_i])

        if len(tbs) != 0:
            try:
                dfs = pd.read_html(str(tbs))
                for df_i, df in enumerate(dfs):
                    print('df_index : ', df_i,'/',len(dfs))
                    if df_i > 0:
                        break
                    #print(df)
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
                    #print(columnlist, idxname)
                    dd = {}     # stands for df_dtype
                    dd[idxname]=sqlalchemy.types.String(12)
                    #for col in columnlist:
                    #    dd['col'] = sqlalchemy.types.Float()
                    print(dd)

                    # DB 연결
                    df.to_sql(name = lnks_name[lnk_i], con = conn, if_exists='append', index=True, dtype=dd)

                    # df 확인해보기
                    #pg.show(df)
                    # IFRS 연결
            except Exception as ex2:
                print(ex2)
        else:
            print('no table found.', len(tbs))
        time.sleep(2)
    except Exception as ex:
        print('rq.get failed.', ex)
        drv.quit()
    time.sleep(2)

def __main__():
    corpcode_txt = open(def_path + "1_Crawl/corplist.txt", "r")
    lines = corpcode_txt.readlines()
    conn = mysqlCON()

    for line in lines:
        for i in list(range(0,2)):
            report('A'+line, conn, i)
    #for i in list(range(0,2)):
    #    report('A172580', conn, i)
        
if __name__ == "__main__":
    __main__()