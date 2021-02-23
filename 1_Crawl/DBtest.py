import pandas as pd
from time import gmtime, strftime
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb	

def mysqlCON():
    HN, PORT, USER, PW, DB, CHARSET = 'ntntn.mooo.com', 6352, 'dart', 'kye6121!!', 'DART', 'utf8'
    con_str_fmt = "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}"
    con_str = con_str_fmt.format(USER, PW, HN, PORT, DB, CHARSET)
    print(con_str)
    
    engine = create_engine(con_str)
    conn = engine.connect()
    print(conn)

    return conn
