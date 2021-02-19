# 기본 공시정보를 파싱하는 py파일입니다.
import datetime

import requests as rq       # 웹페이지 소스 받아오기 위함.
from urllib import parse    # url의 param을 파싱하기 위함.
#from urllib.parse import urlparse, parse_qs, parse_qsl

from bs4 import BeautifulSoup as bs
import lxml

import pandas as pd
import pandasgui as pg

def parse_instructions():
    lnk = ['https://opendart.fss.or.kr',
           '/guide/main.do?apiGrpCd=']
    find_all_dict = {
        'class':'tb01',
        }

    excel_path = '1. Crawl/a_dart/opendart_help.xlsx'
    excel_writer = pd.ExcelWriter(excel_path, engine = 'xlsxwriter')

    for lnk_idx in list(range(1, 4)):
        pth = 'DS' + f'{lnk_idx:03d}'               # string formatting 방법 중 가장 최신이며 빠른 방법
        webpage = rq.get(lnk[0] + lnk[1] + pth)     # opendart 설명 주소의 형식은 DS000형식
        print(lnk[0] + lnk[1] + pth)                # 완전한 주소로 만듦

        sp = bs(webpage.content, "lxml")                    # request로 받은 내용을 beautifulsoup과 lxml 파서로 따냄
        tb = sp.find_all('table', attrs=find_all_dict)      # 각 api 설명 페이지의 주소를 정리해 놓은 테이블을 찾아
        #print(type(tb), tb)                                                    # 반환 결과가 있으면
        df = pd.read_html(str(tb))                 # dataFrame 형태로 받아옴.

        for tb_idv in tb:  
            tb_lnk = tb_idv.find_all('a', attrs={'class':'link'})
            print(tb_lnk)
    #tb_lnk = sp.find_all('a', attrs={'class':'link'})   # find links

            for i, each in enumerate(tb_lnk):
                guide_lnk = each.get('href')
                print(lnk[0] + guide_lnk)

                guide_web = rq.get(lnk[0] + guide_lnk)
                guide_sp = bs(guide_web.content, "lxml")
                guide_tb = guide_sp.find_all('div', attrs={'class','DGCont'})
                guide_df = pd.read_html(str(guide_tb))      # html 형식에서 table 태그들을 읽어와서, df list 형태로 반환
                print(type(guide_df))
            
                for df_idx, idf in enumerate(guide_df):
                    qrys = parse.parse_qs((parse.urlparse(lnk[0] + guide_lnk)).query)   # http 주소 형식에서 parameter들을 따로 떼어내서 {'':[]} 형식으로 반환
                    #print(qrys)                                                        # {'apiGrpCd': ['DS001'], 'apiId': ['2019001']}            
                    sheetname = ''                      # sheetname 정의. 
                                                        # apiGrpCd + '_' + apiId + '_' + f'{설명표 순서:03d}'
                    for qry in qrys:                    
                        #print(qry,qrys[qry])           # apiGrpCd ['DS001'] \n apiId ['2019001']    
                        for qrlist in qrys[qry]:        
                            sheetname += (qrlist + '_')
                    sheetname += f'{df_idx:02d}'        
                    print(type(idf), sheetname)         
                    #pg.show(idf)
                    rsdf = inst_(idf)
                    #guide_lnk = guide_lnk.split('')
                    rsdf.to_excel(excel_writer, sheet_name = sheetname)
                    dict = rsdf.to_dict()         # dict{column:row}에서, row{index:} dict가 들어가게 된다.
                    #print(dict)
    excel_writer.save()
    excel_writer.close()

def inst_(df):  # 테이블 하나를 처리하는 함수.
    df = df.fillna(method='ffill')   # 병합된 행들을 불러오면 NaN으로 채워지게 되는데, 이를 ffill로 채울 수 있다.
    
    # dataframe Indexing
    col_list = df.columns.tolist()          # df.columns 요소를 .tolist()를 통해 list로 변환
    col_list = col_list[:len(col_list)-1]   # 맨 마지막 설명칸을 제외하고, df.groupby로 중복을 제거할 것임
    print(col_list)
    df = df.set_index(col_list[0])
    df = df.groupby(col_list).agg('\n'.join).reset_index() # groupby로 중복되는 행들을 합칠 수 있다. 원래는 ['키','명칭'] 두 개로 정렬했음
    #pg.show(df)

    return df

def instructions(sheet_name):
    filename = '1. Crawl/a_dart/opendart.xlsx'
    df = pd.read_excel(
        "a_dart/"+filename,     # 불러올 파일 이름
        sheet_name=sheet_name,  # 불러올 sheet 이름
        #index_col=0,             # index로 사용할 column 번호
        )
    df = df.fillna(method='ffill')  # 병합된 행들을 불러오면 NaN으로 채워지게 되는데, 이를 ffill로 채울 수 있다.
    
    # dataframe Indexing
    df = df.set_index('키')
    col_list = df.columns.tolist()      # df.columns 요소를 .tolist()를 통해 list로 변환
    col_list = col_list[:len(col_list)-1]
    print(col_list)

    df = df.groupby(col_list).agg('\n'.join).reset_index() # groupby로 중복되는 행들을 합칠 수 있다. 원래는 ['키','명칭'] 두 개로 정렬했음
    pg.show(df)
    dict = df.to_dict()         # dict 안에 dict가 들어가게 된다.
    print(dict)
    print(dict['명칭'])

    return dict

def disclosurelist(crtfc_key, **kwargs):
    # https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
    url = 'https://opendart.fss.or.kr/api/list.json'
    default_path = '1. Crawl/a_dart/'
    write_path = default_path + 'disclosureslist'+str(datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))+'.json'

    end_de = datetime.datetime.now()
    bgn_de = end_de - datetime.timedelta(seconds=365.25/6*24*60*60)


    kwargs_ = {'crtfc_key':crtfc_key, 
              'bgn_de':bgn_de.strftime('%Y%m%d'),
              'end_de':end_de.strftime('%Y%m%d'),
              'page_count':str(100),
              'page_no':str(1),
              'pblntf_ty':'A',
              #'':,
              }
    ## 입력인자 받아서 입력
    params = {}
    for key, value in kwargs_.items():
        params[key]=value
    print(params)

    # request로 json 요청
    rq_res = rq.get(url,params=kwargs_) # 
    #print(rq_res.url, rq_res.content)
    result = rq_res.content.decode('utf-8')
    open(write_path , 'wb').write(rq_res.content)
    df = pd.read_json(write_path)
    #pg.show(df)

    # list column 시리즈를 list로 변환
    lst = df['list'].tolist()
    #print(lst, type(lst))
    
    # 
    if len(lst) > 0:
        idf = pd.DataFrame(columns=lst[0].keys())#, index=['corp_code'])
        for indlst in lst:
            print(indlst, type(indlst))
            #ndf = pd.DataFrame.from_dict(indlst)#, orient=indlst['corp_code'])
            #ndf = pd.DataFrame.from_records(indlst, index=str(indlst['corp_code']) )
            #pd.concat([idf, ndf], sort=False)
        pg.show(idf)
    
def report_parse(lnk):
    # testlink : http://dart.fss.or.kr/report/viewer.do?rcpNo=20210203000132&dcmNo=7785217&eleId=1&offset=0&length=0&dtd=dart3.xsd
    #if lnk != '':
    #    lnkparse = urlparse.urlparse(lnk)
    #    print(lnkparse)

    # offset과 length 인자를 0으로 보내면 전체 리포트를 볼 수 있다. 
    lnk_raw = 'http://dart.fss.or.kr/report/viewer.do?rcpNo=20210203000132&dcmNo=7785217&eleId=1&offset=0&length=0&dtd=dart3.xsd'
    lnk_parse = parse.urlparse(lnk_raw)
    qrylst = parse.parse_qs(lnk_parse.query)
    for key in qrylst.keys():
        print(key, end='')
        for lst in qrylst[key]:
            print(lst)
    print( parse.parse_qs(lnk_parse.query) )

    params = {'rcpNo':'20210203000132',
              'dcmNo':'7785217',
              'eleId':'1',
              'offset':'0',
              'length':'0',
              'dtd':'dart3.xsd'
              }
    link = 'http://dart.fss.or.kr/report/viewer.do'
    resp = rq.post(link, data=params)
    res_tbs = pd.read_html(resp.content)
    print(type(res_tbs), len(res_tbs))
    
    for tb in res_tbs:
        pg.show(tb)
    print(resp.content)

def xbrl(crtfc_key):
    write_path = '1. Crawl/a_dart/xbrltest.xbrl'
    lnk = 'https://opendart.fss.or.kr/api/fnlttXbrl.xml'

    rcp_samples=['20210203000132', '20210218001114', '20190401004781']
    params = {
        'crtfc_key':crtfc_key,
        'rcpNo':rcp_samples[2],
        'reprt_code':'11011',
        }

    resp = rq.post(lnk, data=params)
    
    result = resp.content.decode('utf-8')
    open(write_path , 'wb').write(resp.content)
    print(resp.content)

    #res_tbs = pd.read_html(resp.content)
    #print(type(res_tbs), len(res_tbs))
    

def __main__():
    crtfc_key = "5350c2e7125f743afc8946f8e5885f7bf992079c"

    #parse_instructions()
    #disclosurelist(crtfc_key)
    #report_parse('report link in here')
    xbrl(crtfc_key)

if __name__ == "__main__":
    __main__()