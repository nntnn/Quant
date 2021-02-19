import requests as rq       #
from urllib import parse    # url의 param을 파싱하기 위함.
from selenium import webdriver

from bs4 import BeautifulSoup as bs
import lxml

import pandas as pd
import pandasgui as pg

lnk = ['https://finance.naver.com/sise/sise_index.nhn?code=KOSPI']

def method_01():
    rsp = rq.get(lnk[0])
    bs_source = rsp.content#.decode('utf-8')
    print(bs_source)

    sp = bs(bs_source, "lxml")                    # request로 받은 내용을 beautifulsoup과 lxml 파서로 따냄
    find_all_dict = {'class':'type_1',}
    tb = sp.find_all('table', attrs=find_all_dict)      # 각 api 설명 페이지의 주소를 정리해 놓은 테이블을 찾아
    #print(type(tb), tb)                                                    # 반환 결과가 있으면
    df = pd.read_html(str(tb))                 # dataFrame 형태로 받아옴.

    pg.show(df)

def method_02():
    # 옵션값 설정
    opt = webdriver.ChromeOptions()
    opt.add_argument('headless')

    # 웹드라이버를 통해 네이버 금융 ETF 페이지에 접속
    drv = webdriver.Chrome('_exec/chromedriver.exe', options=opt)
    drv.implicitly_wait(3)
    lnk.append('https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI')
    try:
        drv.get(lnk[1])
        
        # 뷰티풀 수프로 테이블을 스크래핑
        bs_result = bs(drv.page_source, 'lxml')
        drv.quit()
        print(bs_result)

        find_all_dict = {'class':'type_1',}
        tbs = bs_result.find_all('table', attrs=find_all_dict)      # 각 api 설명 페이지의 주소를 정리해 놓은 테이블을 찾아
        #print(type(tb), tb)                                                    # 반환 결과가 있으면
        for tb in tbs:
            df = pd.read_html(str(tb))                 # dataFrame 형태로 받아옴.
            pg.show(df)

    except Exception as ex:
        print(ex)

def method_03():

def __main__():
    method_02()

if __name__ == "__main__":
    __main__()

