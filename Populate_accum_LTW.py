import pymysql
import csv 
import time
from datetime import datetime, timedelta

connect = pymysql.connect(host='127.0.0.1', port=3306, db='ptls')
cursor = connect.cursor(pymysql.cursors.DictCursor)

 
#UPDATE accum TO THE MOST RECENT READ on dials
sql = f""" SELECT max(RealReadDate) as date FROM dials """
cursor.execute(sql)
latest_date = cursor.fetchall()[0]["date"]
if latest_date.minute < 23:
    latest_date = latest_date - timedelta(hours=1, minutes=latest_date.minute)

print(latest_date) 

sql = f""" SELECT * FROM accum WHERE RealReadDate = (SELECT MAX(RealReadDate) FROM accum) """
cursor.execute(sql)
latest_readigs = cursor.fetchall()
if len(latest_readigs) == 0:
    print("No readings in accum. Getting the min date in dials")
    sql = f""" SELECT * FROM dials WHERE RealReadDate = (SELECT MIN(RealReadDate) FROM dials) """
    cursor.execute(sql)
    latest_readigs = cursor.fetchall()

date = latest_readigs[0]["RealReadDate"]

print("Filling accum from {} to {}".format(date))

date = date + timedelta(hours=1)

while date <= latest_date:
    #print(date)
    for r in latest_readigs:
        try:
            #print(r)
            sql = f""" SELECT * FROM dials WHERE SN = '{r["SN"]}' AND RealReadDate = '{date}'"""
            cursor.execute(sql)
            read = cursor.fetchall()[0]
            #print(read)
            r["RealReadDate"] = date
            r["ReadDate"] = time.mktime(date.timetuple())
            r["TCh1"] = r["TCh1"] + read["Ch1"]
            r["TCh2"] = r["TCh2"] + read["Ch2"]
            r["TCh3"] = r["TCh3"] + read["Ch3"]
            r["TCh4"] = r["TCh4"] + read["Ch4"]
            r["TCh5"] = r["TCh5"] + read["Ch5"]
            r["TCh6"] = r["TCh6"] + read["Ch6"]
            r["TCh7"] = r["TCh7"] + read["Ch7"]
            r["TCh8"] = r["TCh8"] + read["Ch8"]
            #print(r)
            
            sql = f""" INSERT INTO accum VALUES (
                       '{r['SN']}',
                       '{r['ReadDate']}',
                       '{r['RealReadDate']}',
                       '{r["TCh1"]}',
                       '{r["TCh2"]}',
                       '{r["TCh3"]}',
                       '{r["TCh4"]}',
                       '{r["TCh5"]}',
                       '{r["TCh6"]}',
                       '{r["TCh7"]}',
                       '{r["TCh8"]}'
                       )"""
            cursor.execute(sql)
            connect.commit()
        except Exception as e:
            print(e)
    date = date + timedelta(hours=1)
    print(date)