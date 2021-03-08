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

    str_a = ['function initPage()','function replaceHtml(']#'var viewport = new Ext.Viewport']#'//팝업 순서']
    scr_list = bs_find(tbs, str_a[0], str_a[1])
    print(len(scr_list))
    
    txtlist = []
    #[m.start() for m in re.finditer('test', 'test test test test')]
    for m in re.finditer('(text: ")(.*?)(",)', scr_list[0]):
        #print(m.span(), m.group())
        txtlist.append(m.group())
    print(len(txtlist))
    print(txtlist)

    idxdict = {}
    for m_idx, m in enumerate(re.finditer('(viewDoc\(\')(.*?)(\'\))', scr_list[0])):
        #print(m.span(), m.group())
        doclist = []
        for n in re.finditer('(\').*?(\')|(null)', m.group()):
            #print(n.span(), n.group())
            doclist.append(n.group())
        idxdict[doclist[2]] = [doclist[3], doclist[4], doclist[5]] # txtlist[m_idx], 
    print(len(idxdict))
    print(idxdict)
    for D_idx, DocValues in enumerate(re.finditer('(currentDocValues = {)(.*?)(};)', scr_list[0])):
        print(DocValues.span(), DocValues.group())
        curValues = DocValues.group()
        if D_idx != 0:
            break
    curValues = curValues[curValues.find('{')+1:curValues.find('}')-1]
    Values = curValues.split(',')
    print(Values)

    # http://dart.fss.or.kr/report/viewer.do?
    # rcpNo=20200330004441&
    # dcmNo=7206202&
    # eleId=11&
    # offset=349311&
    # length=1264522&
    # dtd=dart3.xsd
if __name__ == "__main__":
    __main__()