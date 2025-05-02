from flask import Flask,render_template,request
from datetime import datetime
import pandas as pd
import pymysql
from pm25 import get_pm25_data_from_my_sql

def open_db():
    conn=None
    try:
        conn=pymysql.connect(
            host="127.0.0",port=3306,user="root",passwd="12345678",db="demo"
        )
    except Exception as e:
        print("資料庫開啟失敗",e)

    return conn

def get_pm25_data_from_my_sql():
    conn = None
    columns, datas = None, None
    try:
        conn = open_db()
        cur=conn.cursor()
        #sqlstr="select MAX(datacreationdata)* from pm25;"
        #cur.execute(sqlstr)
        #last_time=cur.fetchone()[0]
        #print(last_time)
        sqlstr = "select * from pm25 where datacreationdata=(select MAX(datacreationdata)* from pm25);"
        cur.execute(sqlstr)
        print(cur.description)
        columns=[col[0] for col in cur.description]
        datas = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    return columns,datas

if_name_ == "_main_":
    updata_db()