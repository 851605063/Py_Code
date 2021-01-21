#!python3
# coding: utf-8
#

'''连接mysql数据库并执行SQL语句'''

import os,sys
import pymysql
try:
    conn = pymysql.connect(host='localhost',user='root',passwd='admin',db='bms')
except Exception as e:
    print ('异常',e)
    sys.exit()
cursor = conn.cursor()
sql = "select * from zwb"
cursor.execute(sql)
data = cursor.fetchall()
if data:
    for x in data:
        print (x[0])
cursor.close()
conn.close()