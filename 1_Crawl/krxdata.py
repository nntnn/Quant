import requests as rq
import urllib as url

# krx data에서 월별 시가총액 파싱 후 리턴

# POST      http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd
# parameter mktId=ALL&trdDd=20210302&share=1&money=1&csvxls_isNo=false&name=fileDown&url=dbms%2FMDC%2FSTAT%2Fstandard%2FMDCSTAT01501
# response  s8Y8Ol512kBmldKcD255OtMzCVmC0CSmZ8DSQeQ1N8oRtSksuLS7Bnxpl86F7dAOkunw9BBwugQaSjGAcH15eVlgPXzGxCszF9PfZYDOkBht7Va4RvzEKgKIPAKhudWsZqIo4cIzoURnTI8+MmkJ4iJLNMtcar8P/Vjo+PspoD4UiUvMzto4SSLuiFnheu1enuMhsFT3ogTpRhhEPW0EZRRiy10m5/fSKm8JaNjYKT25pHf5lyxJ7LnF8/CZxMuN

# POST      http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd
# parameter code=s8Y8Ol512kBmldKcD255OtMzCVmC0CSmZ8DSQeQ1N8oRtSksuLS7Bnxpl86F7dAOkunw9BBwugQaSjGAcH15eVlgPXzGxCszF9PfZYDOkBht7Va4RvzEKgKIPAKhudWsZqIo4cIzoURnTI8%2BMmkJ4iJLNMtcar8P%2FVjo%2BPspoD4UiUvMzto4SSLuiFnheu1enuMhsFT3ogTpRhhEPW0EZRRiy10m5%2FfSKm8JaNjYKT25pHf5lyxJ7LnF8%2FCZxMuN

def gen(**kwargs):
    lnk = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    parameter = 'mktId=ALL&trdDd=20210302&share=1&money=1&csvxls_isNo=false&name=fileDown&url=dbms%2FMDC%2FSTAT%2Fstandard%2FMDCSTAT01501'
    p_qs = url.parse.parse_qs(parameter)
    #print(p_qs, type(p_qs))
    
    params = p_qs.keys()
    for par in params:
        print(par, p_qs[par])
        #p_qs[par] = 
    #print(p_qs)

def down():
    pass

gen()