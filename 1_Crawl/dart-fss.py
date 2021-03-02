import dart_fss as dart
import pandas as pd
import pandasgui as pg

# Open DART API KEY 설정
api_key='5350c2e7125f743afc8946f8e5885f7bf992079c'
dart.set_api_key(api_key=api_key)

# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()
#print(corp_list.corps, type(corp_list.corps))
# 삼성전자 검색
samsung = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]

# 2012년부터 연간 연결재무제표 불러오기
#fs = samsung.extract_fs(bgn_de='20120101')

# 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
#fs.save()
samsung = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]
#samsung = corp_list.find_by_corp_name(corp_code='005930')

# 2012년 01월 01일 부터 연결재무제표 검색
# fs = samsung.extract_fs(bgn_de='20120101') 와 동일
fs = dart.fs.extract(corp_code='005930', bgn_de='20170101')

# 연결재무상태표
df_fs = fs['bs'] # 또는 df = fs[0] 또는 df = fs.show('bs')
pg.show(df_fs)