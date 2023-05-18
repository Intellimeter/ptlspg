import pymysql
import csv 

_FILE_NAME_ = "C://ptlspg/luxe_daily_20230125.csv"

connect = pymysql.connect(host='127.0.0.1', port=3306, db='ptls')
cursor = connect.cursor(pymysql.cursors.DictCursor)

with open (_FILE_NAME_, newline="") as csvfile:
    reader = csv.reader(csvfile,delimiter=",")
    i = 0
    for row in reader:
        if i > 0:
            print(row)
            sql = f"""INSERT INTO info VALUES ('{row[1]}', '{row[2]}', '{row[5]}', 0.01, '{row[4]}', '{row[7]}')"""
            cursor.execute(sql)
            connect.commit()
        i = i + 1
        
    print(i,"Rows Loaded")