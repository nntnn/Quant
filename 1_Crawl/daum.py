import pandas as pd
import pandasgui as pg

import requests as rq
from urllib import parse
from bs4 import BeautifulSoup as bs
import lxml

import time
import os

lnk = 'https://wisefn.finance.daum.net/v1/company/c1040001_1.aspx?cmp_cd='
code = '001529'

def report(code):
    try:
        # 가치지표 파싱
        lnk = 'https://wisefn.finance.daum.net/v1/company/c1040001_1.aspx?cmp_cd='
        lnk = 'https://wisefn.finance.daum.net/v1/company/cF4002.aspx?cmp_cd='
        lnk += code
        lnk += '&frq=0&rpt=1&finGubun=MAIN'

        lnk = 'https://finance.daum.net/quotes/A001529#analysis/main'

        resp = rq.get(lnk)
        bs_res = bs(resp.content, "lxml")
        tbs = bs_res.find_all('table', {'class':'tbl'})#{'id':'draggable-table-body'})
        
        print(resp.content.decode('utf-8'))

        if len(tbs) != 0:
            try:
                dfs = pd.read_html(str(tbs))
                for df in dfs:
                    print(df)
                    #df = df.set_index(df.columns.tolist()[0]) # 테이블의 iloc[0,0]을 index로 설정.

                    ## 중복열 drop
                    #df = pd_dup_col(df)

                    ## 인덱스 문자 깔끔하게 정리
                    #df = pd_remove_txt(df, '계산에 참여한 계정')

                    ## 행열 바꾸기
                    #df = df.transpose()

                    ## index를 종목코드:연도/최종월 형태로 바꾸기
                    #indexlist = df.index.tolist()
                    #for lst_idx, lst in enumerate(indexlist):
                    #    #print(code[:code.find('\n')])
                    #    indexlist[lst_idx] = code[:code.find('\n')] + ':' + lst
                    #    indexlist[lst_idx] = indexlist[lst_idx][:indexlist[lst_idx].find('/')]
                    #print(indexlist)
                    #df = df.set_index(pd.Series(indexlist))
                    #df.index.name = 'ticker:year'
                    #df.reset_index()
                    #print(df)

                    ## df dtype 정의. dict={'column name':sqlalchemy.types.type(n), }
                    #columnlist = df.columns.tolist()
                    #idxname = df.index.name
                    #print(columnlist, idxname)
                    
                    #dd = {}     # stands for df_dtype
                    #dd[idxname]=sqlalchemy.types.String(12)
                    #for col in columnlist:
                    #    dd['col'] = sqlalchemy.types.Float()
                    #print(dd)

                    ## DB 연결
                    #df.to_sql(name = lnks_name[lnk_i], con = conn, if_exists='append', index=True, dtype=dd)

                    ## 
                    pg.show(df)

                    # IFRS 연결
            except Exception as ex2:
                print(ex2)
        else:
            print('no table found.', len(tbs))
    
    except Exception as ex:
        print('rq.get failed.', ex)

report('001529')