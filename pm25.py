from flask import Flask,render_template,request
from datetime import datetime
import pandas as pd
import pymysql
from pm25 import get_pm25_data_from_my_sql

def get_site_by_county(county):
    conn = None
    sites = []
    try:
        conn = open_db()
        cur = conn.cursor()
        sqlstr = "select distinct county from pm25 where county=%s;" 
        cur.execute(sqlstr,(county,))
        datas = cur.fetchall()
        print(datas)
        columns=[data[0] for data in datas]
        
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return sites


def get_all_counties():
    conn = None
    counties = []
    try:
        conn = open_db()
        cur = conn.cursor()
        sqlstr = "select distinct county from pm25;" 
        cur.execute(sqlstr)
        datas = cur.fetchall()
        columns=[data[0] for data in datas]
        
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    

def open_db():
    conn=None
    try:
        conn=pymysql.connect(
            host="127.0.0",port=3306,user="root",passwd="12345678",db="demo"
        )
    except Exception as e:
        print("資料庫開啟失敗",e)

    return conn

def get_pm25_data_by_site(county, site):
    conn = None
    columns, datas = None, None
    try:
        conn = open_db()
        cur=conn.cursor()
        sqlstr = "select * from pm25 where counyt=%s and site=%s" 
        cur.execute(sqlstr),(county,site)
        print(cur.description)
        columns=[col[0] for col in cur.description]
        datas = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


def get_pm25_data_from_my_sql():
    conn = None
    columns, datas = None, None
    try:
        conn = open_db()
        cur=conn.cursor()
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
    #updata_db()
    #print(get_pm25_data_by_site("新北市","富貴角"))
    print(get_all_counties)