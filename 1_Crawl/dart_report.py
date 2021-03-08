import requests as rq
import urllib as url

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import lxml
#from jsonfinder import jsonfinder

import json
import re

import os

def wd(lnk, types='', params={}, unwanted_params={}):
    # wd stands for webdriver. Parse and Find
    # func(**{'type':'Event'}) is equivalent to func(type='Event')
    # unwanted_params 기능 추가

    # 옵션값 설정
    opt = webdriver.ChromeOptions()
    opt.add_argument('headless')

    # 웹드라이버로 lnk parse
    drv = webdriver.Chrome('_exec/chromedriver.exe', options=opt)
    drv.implicitly_wait(3)
    try:
        drv.get(lnk)
        # 뷰티풀 수프로 테이블을 스크래핑
        bs_result = bs(drv.page_source, 'lxml')
        drv.quit()
        #print(types, params)
        
        tbs = bs_result.find_all(types, attrs=params) 
        print(len(tbs))
        for tb_i, tb in enumerate(tbs):
            print(tb_i, tb.attrs)
        return tbs

        #print(type(tb), tb)                                                    # 반환 결과가 있으면
        #for tb in tbs:
        #    str(tb).find()
        #    #df = pd.read_html(str(tb))                 # dataFrame 형태로 받아옴.
        #    #pg.show(df)

    except Exception as ex:
        print(ex)

def bs_find(bs, start='', end=''):
    # <!-- x-xeries js libraries  -->
    # </script>
    ret_list = []
    try:
        for b in bs:
            if len(b) != 0:
                st_idx = str(b).find(start)
                ed_idx = str(b).find(end, st_idx)
                #print(str(b)[st_idx:ed_idx])
                ret_list.append(str(b)[st_idx:ed_idx])
        return ret_list
    except Exception as ex:
        print(ex)

def logfile_init(file=''):
    try:
        f = open(file, 'w')
        return f
    except Exception as ex:
        print(ex)

def logfile(f, file='', str_write=''):
    f = open(file, 'a')
    f.write(str_write)

def __main__():
    lnk = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20200330004441'
    lnk_param = url.parse.urlparse(lnk)
    parsekey=['scheme','netloc','path','params','query','fragment',]

    #ParseResult(   scheme='http', 
    #               netloc='dart.fss.or.kr', 
    #               path='/dsaf001/main.do', 
    #               params='', 
    #               query='rcpNo=20200330004441', 
    #               fragment='')

    parse_params={'type':'text/javascript'}
    tbs = wd(lnk, types='script', params = parse_params)

str_a = ['// 1','//팝업 순서']
scr_list = bs_find(tbs, str_a[0], str_a[1])
print(len(scr_list))
[m.start() for m in re.finditer('([{](.*?)[}])', scr_list[0])]
#[m.start() for m in re.finditer('test', 'test test test test')]
for m in re.finditer('([{](.*?)[}])', scr_list[0]):
    print(m.span(), m.group())

