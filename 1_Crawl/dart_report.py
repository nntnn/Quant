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
import time
import zipfile
import xmltodict
import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

import pandas as pd
import pandasgui as pg
import pickle

crtfc_key = '5350c2e7125f743afc8946f8e5885f7bf992079c'

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

def code_list():
    lnk = 'https://opendart.fss.or.kr/api/corpCode.xml'
    today = datetime.datetime.now().strftime('%Y%m%d')
    cd_file = 'codelist'+today+'.dump'
    
    try:
        if ~(os.path.isfile(cd_file)):
            resp = rq.get(lnk, params={'crtfc_key':crtfc_key})
            with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
                print(z.namelist())
                data_xml = z.read('CORPCODE.xml').decode('utf-8')
                data_odict = xmltodict.parse(data_xml)
                data_dict = json.loads(json.dumps(data_odict))
                data = data_dict.get('result', {}).get('list')
                #pg.show(data)
                savedict(cd_file, data)
        else:
            data = opendict(cd_file)
        return data 
    except Exception as ex:
        print(ex)

def savedict(filename, dct):
    #filename = '20200330004441.dump'
    try:
        with open(filename,'wb') as fw:
            pickle.dump(dct, fw)
    except Exception as ex:
        print(ex)

def opendict(filename):
    try:
        with open(filename, 'rb') as handle:
            b = pickle.load(handle)
            return b
    except Exception as ex:
        print(ex)

def report_list(code):
    # https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
    lnk = 'https://opendart.fss.or.kr/api/list.json'
    #prs = url.parse.urlparse(lnk)
    print('get report - ' + str(code))
    today = datetime.datetime.now().strftime("%Y%m%d")
    repname = 'rep/'+code+'_'+today+'.rep'
    if not os.path.isfile(repname):
        keys = {
            'crtfc_key':'5350c2e7125f743afc8946f8e5885f7bf992079c', # 발급받은 인증키(40자리)
            'corp_code':code,             # 공시대상회사의 고유번호(8자리)
            'bgn_de':'19000101',                # 검색시작 접수일자(YYYYMMDD) : 없으면 종료일(end_de)
                                        # 고유번호(corp_code)가 없는 경우 검색기간은 3개월로 제한
            'end_de':today,                # 검색종료 접수일자(YYYYMMDD) : 없으면 당일
            'last_reprt_at':'Y',         # 최종보고서만 검색여부(Y or N) 기본값 : N (정정이 있는 경우 최종정정만 검색)
            'pblntf_ty':'A',             # A : 정기공시
                                        # B : 주요사항보고
                                        # C : 발행공시
                                        # D : 지분공시
                                        # E : 기타공시
                                        # F : 외부감사관련
                                        # G : 펀드공시
                                        # H : 자산유동화
                                        # I : 거래소공시
                                        # j : 공정위공시
            'pblntf_detail_ty':'',      # (※ 상세 유형 참조 : pblntf_detail_ty)
            'corp_cls':'',              # 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) ※ 없으면 전체조회, 복수조건 불가
            'sort':'',                  # 
            'sort_mth':'',              # 오름차순(asc), 내림차순(desc) 기본값 : desc
            'page_no':'1',               # 페이지 번호(1~n) 기본값 : 1
            'page_count':'100',            # 페이지당 건수(1~100) 기본값 : 10, 최대값 : 100
            }
        resp = rq.get(lnk, params=keys)
        #print(resp.content.decode('utf-8'))
        #report_dict = resp.json() #json.load(resp.content.decode('utf-8'))
        try:
            print(resp.content.decode('utf-8'))
            report_dict = json.loads(resp.content.decode('utf-8'))
            print(report_dict.keys())
            if (report_dict['status'] == '000'):
                with open(repname, 'w') as outfile:
                    json.dump(report_dict, outfile, ensure_ascii=False)
        except Exception as ex:
            print(ex)
        time.sleep(0.5)
    else:
        with open(repname, 'rb') as handle:
            print(handle)
            report_dict = json.loads(handle)
    #print(report_dict['list'])
    #pg.show(report_dict['list'])

def jsonparse(lnk:str):
    try:
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
    except Exception as ex:
        print(ex)

def __main__():
    lnk = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20200330004441'
    #jsonparse(lnk)
    corplist = code_list()
    dic = {'corp_code':[],
           'corp_name':[],
           'stock_code':[],
           'modify_date':[],
           }
    for item in corplist:
        #print(item['stock_code'])
        if not (item['stock_code'] == None):
            #print(item)
            for k,v in item.items():
                dic[k].append(v)
    #print(dic)
    #pg.show(dic)
    dartcodes = dic['corp_code']
    print(dartcodes)
    for clim, code in enumerate(dartcodes):
        print(code)
        report_list(code)
        clim += 1
        #if clim > 10:
        #    break


if __name__ == "__main__":
    __main__()