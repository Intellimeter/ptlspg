#-------------------------------------------------------------------------------
# Name:        Populate_accum_LTW
#
# Author:      Arturo Hernández Gómez
# Date:        2023/09/08
#-------------------------------------------------------------------------------
import pymysql
import csv 
import time
from datetime import datetime, timedelta

connect = pymysql.connect(host='127.0.0.1', port=3306, db='ptls', charset='utf8')
cursor = connect.cursor(pymysql.cursors.DictCursor)

 
#UPDATE accum TO THE MOST RECENT READ on dials
sql = f""" SELECT max(RealReadDate) as date FROM dials """
cursor.execute(sql)
latest_date = cursor.fetchall()[0]["date"]
if latest_date.minute != 55:
    latest_date = latest_date - timedelta(minutes=latest_date.minute)

print(latest_date) 

sql = f""" SELECT * FROM accum WHERE RealReadDate = (SELECT MAX(RealReadDate) FROM accum) """
cursor.execute(sql)
latest_readigs = cursor.fetchall()

if len(latest_readigs) == 0:
    print("No readings in accum. Getting the sum until 2023-01-01 00:00:00")
    sql = f""" SELECT SN, SUM(Ch1) as Ch1, SUM(Ch2) as Ch2, SUM(Ch3) as Ch3, SUM(Ch4) as Ch4, SUM(Ch5) as Ch5, SUM(Ch6) as Ch6, SUM(Ch7) as Ch7, SUM(Ch8) as Ch8  
               FROM dials WHERE RealReadDate <= '2023-01-01 00:00:00' GROUP BY SN"""
    cursor.execute(sql)
    first_readigs = cursor.fetchall()

    mult = {}
    i = 0
    for r in first_readigs:
        mult[r["SN"]] = []
        for ch in range(1,9):
            sql = """ SELECT IFNULL(multiplier,1) as mult FROM meters where ModbusId = {} AND SN like '%0{}'
                """.format(r["SN"],ch)
            cursor.execute(sql)
            m = cursor.fetchall()
            if len(m) != 0:
                mult[r["SN"]].append(m[0]["mult"])
            else:
                mult[r["SN"]].append(1.0)

    for r in first_readigs:
        dateToInsert = datetime.strptime("2023-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        unixTime =  time.mktime(dateToInsert.timetuple())
        
        sql = f""" INSERT INTO accum VALUES (
                    '{r['SN']}',
                    '{unixTime}',
                    '{dateToInsert}',
                    '{round(float(r['Ch1']) * mult[r["SN"]][0], 3)}',
                    '{round(float(r['Ch2']) * mult[r["SN"]][1], 3)}',
                    '{round(float(r['Ch3']) * mult[r["SN"]][2], 3)}',
                    '{round(float(r['Ch4']) * mult[r["SN"]][3], 3)}',
                    '{round(float(r['Ch5']) * mult[r["SN"]][4], 3)}',
                    '{round(float(r['Ch6']) * mult[r["SN"]][5], 3)}',
                    '{round(float(r['Ch7']) * mult[r["SN"]][6], 3)}',
                    '{round(float(r['Ch8']) * mult[r["SN"]][7], 3)}'
                    )"""
        cursor.execute(sql)
        connect.commit()

        sql = f""" SELECT * FROM accum WHERE RealReadDate = (SELECT MAX(RealReadDate) FROM accum) """
        cursor.execute(sql)
        latest_readigs = cursor.fetchall()

date = latest_readigs[0]["RealReadDate"]

#Load multipliers
mult = {}
i = 0
for r in latest_readigs:
    mult[r["SN"]] = []
    for ch in range(1,9):
        sql = """ SELECT IFNULL(multiplier,1) as mult FROM meters where ModbusId = {} AND SN like '%0{}'
              """.format(r["SN"],ch)
        cursor.execute(sql)
        m = cursor.fetchall()
        if len(m) != 0:
            mult[r["SN"]].append(m[0]["mult"])
        else:
            mult[r["SN"]].append(1.0)

#print(mult)

print("Filling accum from {} to {}".format(date, latest_date))

while date < latest_date:
    print(date)
    for r in latest_readigs:
        try:
            #print(r)
            startDate = date + timedelta(minutes=1)
            endDate = date + timedelta(hours=1)

            sql = f""" SELECT * FROM dials WHERE SN = '{r["SN"]}' AND RealReadDate BETWEEN '{startDate}' AND '{endDate}'"""
            cursor.execute(sql)
            read = cursor.fetchall()
            #print(read)
            
            r["RealReadDate"] = endDate
            r["ReadDate"] = time.mktime(endDate.timetuple())

            for rs in read:
                r["TCh1"] = round(r["TCh1"] + (float(rs["Ch1"]) * mult[r["SN"]][0]),3)
                r["TCh2"] = round(r["TCh2"] + (float(rs["Ch2"]) * mult[r["SN"]][1]),3)
                r["TCh3"] = round(r["TCh3"] + (float(rs["Ch3"]) * mult[r["SN"]][2]),3)
                r["TCh4"] = round(r["TCh4"] + (float(rs["Ch4"]) * mult[r["SN"]][3]),3)
                r["TCh5"] = round(r["TCh5"] + (float(rs["Ch5"]) * mult[r["SN"]][4]),3)
                r["TCh6"] = round(r["TCh6"] + (float(rs["Ch6"]) * mult[r["SN"]][5]),3)
                r["TCh7"] = round(r["TCh7"] + (float(rs["Ch7"]) * mult[r["SN"]][6]),3)
                r["TCh8"] = round(r["TCh8"] + (float(rs["Ch8"]) * mult[r["SN"]][7]),3)
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
                       )
                       ON DUPLICATE KEY UPDATE
                        TCH1 = VALUES(TCH1),
                        TCH2 = VALUES(TCH2),
                        TCH3 = VALUES(TCH3),
                        TCH4 = VALUES(TCH4),
                        TCH5 = VALUES(TCH5),
                        TCH6 = VALUES(TCH6),
                        TCH7 = VALUES(TCH7),
                        TCH8 = VALUES(TCH8)
                        """
            cursor.execute(sql)
            connect.commit()
        except Exception as e:
            print(e)
    date = date + timedelta(hours=1)