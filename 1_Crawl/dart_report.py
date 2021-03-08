import requests as rq
import urllib as url

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import lxml

import json
import re
import os

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

import pandas as pd
import pandasgui as pg
import pickle

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

    str_a = ['// 1', 'function replaceHtml(']   #function initPage()    'var viewport = new Ext.Viewport']#'//팝업 순서']
    scr_list = bs_find(tbs, str_a[0], str_a[1])
    print(len(scr_list))
    
    txtlist = []
    #[m.start() for m in re.finditer('test', 'test test test test')]
    for m in re.finditer('(text: ")(.*?)(",)', scr_list[0]):
        #print(m.span(), m.group())
        txtlist.append(m.group()[m.group().find('text: "') + 7 : len(m.group()) - 2])
    print(len(txtlist), txtlist)

    idxdict = {}
    for m_idx, m in enumerate(re.finditer('(viewDoc\(\')(.*?)(\'\))', scr_list[0])):
        #print(m.span(), m.group())
        doclist = []
        for n in re.finditer('(\').*?(\')|(null)', m.group()):
            #print(n.span(), n.group())
            doclist.append(n.group())

        for i_lst, lst in enumerate(doclist):
            doclist[i_lst] = lst.replace('\'','')
        try:
            idxdict[doclist[2]] = [txtlist[m_idx], doclist[3], doclist[4], doclist[5]] # txtlist[m_idx], 
        except:
            pass
        #print(m_idx, txtlist[m_idx])
    print(len(idxdict), idxdict)

    filename = '20200330004441.dump'
    with open(filename,'wb') as fw:
        pickle.dump(idxdict, fw)

    with open(filename, 'rb') as handle:
        b = pickle.load(handle)
    
    for k,v in b.items():
        print(k, end='\t')
        for vi in v:
            print(vi, end='\t')
        print('')
    #print(b)

    for D_idx, DocValues in enumerate(re.finditer('(currentDocValues = {)(.*?)(};)', scr_list[0])):
        print(DocValues.span(), DocValues.group())
        curValues = DocValues.group()
        if D_idx != 0:
            break
    curValues = curValues[curValues.find('{')+1:curValues.find('}')-1]
    Values = curValues.split(',')
    #print(Values)

    # http://dart.fss.or.kr/report/viewer.do?
    # rcpNo=20200330004441&
    # dcmNo=7206202&
    # eleId=11&
    # offset=349311&
    # length=1264522&
    # dtd=dart3.xsd

if __name__ == "__main__":
    __main__()