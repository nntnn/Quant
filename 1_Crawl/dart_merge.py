#_*_ coding:utf-8 _*_#
import pandas as pd
import pandasgui as pg
import os
#import xlsxwriter

from charset_normalizer import CharsetNormalizerMatches as CnM
from charset_normalizer import detect
import chardet

def txtdetect(file):
    try:        
        rawdata = open(file, "r").read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        print(charenc)

        #blob = open(file, 'rb').read()
        #m = magic.open(magic.MAGIC_MIME_ENCODING)
        #m.load()
        #encoding = m.buffer(blob)
        #print(encoding)

        ##txt = CnM.normalize(file)
        #rf = open(file, 'r').read()#, encoding="euc-kr").read()
        #res = chardet.detect(rf)
        #enc_res = res['encoding']
        #print(enc_res)
        
        #txt = rf.read()
        #rf.close()
    except Exception as e:
        print(e)

def txt2exl(filename:str):
    try:
        filename_excel = filename[:filename.find('.txt')] + '.xlsx'
        filename_csv = filename[:filename.find('.txt')] + '.csv'
        #print(filename, filename_excel)
        ##path = 'opendart_txtmerged/2020_1분기보고서_01_재무상태표_연결_20210221.txt'
        
        df = pd.read_csv(filename, sep='\t')#, encoding='euc-kr')
        pg.show(df)
        print(df)
    
        #excel_writer = pd.ExcelWriter(filename_excel)#, engine='xlsxwriter')
        #df.to_excel(excel_writer, sheet_name=filename[:filename.find('.txt')] )
        #excel_writer.save()
        
        df.to_csv(filename_csv, encoding='euc-kr')#, columns=list_of_dataframe_columns)
        print('save comp')

    except Exception as ex:
        print(ex)

def findtxt(path:str):
    try:
        #path = 'C:/Users/Admin/source/repos/nntnn/Quant/1_Crawl/opendart_txtmerged/'
        filelist = os.listdir(path)
        reslist = []
        for file in filelist:
            #print(file)
            if (file.find('.txt') != -1):
                reslist.append(file)
        #filename = '2015_사업보고서_01_재무상태표_연결_20210219.txt'
        #print(reslist)
        return reslist
    except Exception as ex:
        print(ex)
        return []

def __main__():
    path = 'C:/Users/Admin/source/repos/nntnn/Quant/1_Crawl/opendart_txtmerged/'
    filelist = findtxt(path)
    for file in filelist:
        print(file)
        txtdetect(path + file)

        #if file.find('-utf_8') != -1:
        #    txt2exl(path + file)
        #txtdetect(path + file)    
        #if file.find('_utf-8.txt') != -1:
        #    txt2exl(path + file)
    
    #filelist = findtxt(path)
    #for file in filelist:
    #    print(
    #        file[ file.find('.txt') + 1 : ], (file[ file.find('.txt') + 1 : ] == 'txt'), '\n',
    #        file.find('-cp949.txt') , (file.find('-cp949.txt') != -1), '\n\n'
    #        )
    #    if (file[ file.find('.txt') + 1 : ] == 'txt') & (file.find('-cp949.txt') != -1):
    #        txt2exl(path + file)


if __name__ == "__main__":
    __main__()