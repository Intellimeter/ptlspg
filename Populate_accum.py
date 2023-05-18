import pymysql
import csv 
import time
from datetime import datetime, timedelta

_FILE_NAME_ = "C://ptlspg/luxe_daily_20230125.csv"

connect = pymysql.connect(host='127.0.0.1', port=3306, db='ptls')
cursor = connect.cursor(pymysql.cursors.DictCursor)

#INSERT THE LAS FILE SENT INTO acuum
with open (_FILE_NAME_, newline="") as csvfile:
    reader = csv.reader(csvfile,delimiter=",")
    i = 0
    for row in reader:
        if i > 0:
            print(row)
            column = 'TCh'+row[2]
            date = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
            unix = time.mktime(date.timetuple()) 
            sql = f"""
                      INSERT INTO accum (SN, ReadDate, RealReadDate, {column}) 
                      VALUES ('{row[1]}', '{unix}', '{date}', '{(int(float(row[6])*100))}')
                      ON DUPLICATE KEY UPDATE 
                      {column} = VALUES({column})"""
            #print(sql)
            cursor.execute(sql)
            connect.commit()
        i = i + 1
        
    print(i,"Rows Loaded")
 
#UPDATE accum TO THE MOS RECENT READ
sql = f""" SELECT max(RealReadDate) as date FROM dials """
cursor.execute(sql)
latest_date = cursor.fetchall()[0]["date"]
print(latest_date) 

sql = f""" SELECT * FROM accum  WHERE RealReadDate = '{date}'"""
cursor.execute(sql)
reads = cursor.fetchall()
date = date + timedelta(hours=1)

while date <= latest_date:
    #print(date)
    for r in reads:
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