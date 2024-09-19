#-------------------------------------------------------------------------------
# Name:        Populate_accum_LTW
#
# Author:      Arturo Hernández Gómez
# Date:        2023/09/08
#-------------------------------------------------------------------------------
import pymysql
import csv 
import time
import sys
from datetime import datetime, timedelta

connect = pymysql.connect(host='127.0.0.1', port=3306, db='ptls', charset='utf8', password='pickering', user='ICI')
cursor = connect.cursor(pymysql.cursors.DictCursor)


filename = sys.argv[1]
 

with open(filename,'r') as file:
    reader = csv.reader(file)
    for row in reader:
        dateToInsert = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        unixTime =  time.mktime(dateToInsert.timetuple())
        
        sql = f""" INSERT INTO dials VALUES (
                    '{row[0]}',
                    '{unixTime}',
                    '{dateToInsert}',
                    '{row[2]}',
                    '{row[3]}',
                    '{row[4]}',
                    '{row[5]}',
                    '{row[6]}',
                    '{row[7]}',
                    '{row[8]}',
                    '{row[9]}',
                    0
                    )"""
        try:
            cursor.execute(sql)
            connect.commit()
        except Exception as e:
            print(e)

        