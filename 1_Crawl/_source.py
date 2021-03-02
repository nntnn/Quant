from selenium import webdriver
from bs4 import BeautifulSoup as bs

import lxml

def webdriver(lnk, **kwarg):
    # kwarg 확인
    for k,v in kwarg.items():
        print(k,v)
    
    # 옵션값 설정
    opt = webdriver.ChromeOptions()
    opt.add_argument('headless')

    # 웹드라이버를 통해 네이버 금융 ETF 페이지에 접속
    drv = webdriver.Chrome('_exec/chromedriver.exe', options=opt)
    drv.implicitly_wait(3)
    try:
        drv.get(lnk)
        
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