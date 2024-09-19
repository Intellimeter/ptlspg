#-------------------------------------------------------------------------------
# Name:        send_file_LTW
#
# Author:      Arturo Hernández Gómez
# Date:        2023/09/08
#-------------------------------------------------------------------------------

import pymysql
import ftplib
import os
import csv
import logging
import pysftp
from datetime import datetime, timedelta

pfx='MiloFais'
project_number = '09-09-30-0798'
eq='daily'

logging.basicConfig(filename='C:\ptlspg\LTW_Cloud.log', encoding='utf-8', level=logging.INFO)

connect = pymysql.connect(host='127.0.0.1', port=3306, db='ptls', charset='utf8')
cursor = connect.cursor(pymysql.cursors.DictCursor)


def get_readings(start):
    reads = []
    endate = start + timedelta(hours=23,minutes=59) 

    # ONLY FOR WINDOWS MODBUS (comment if only PTLS) 

    '''sql =  """ SELECT meter.serial_number as SN, meter.name as MeterId, meter.utility as typeOfUtility, meter.units, time_stamping as RealReadDate, kwh as reading FROM reading_1
                JOIN meter ON meter.id = reading_1.meter
				WHERE time_stamping BETWEEN '{}' AND '{}' ORDER BY meter.serial_number, time_stamping
			""".format(start, endate)
    cursor.execute()
    reads += cursor.fetchall()'''

    # ONLY FOR WINDOWS MODBUS
    
    for ch in range(1,9):
        sql = """ SELECT meters.SN, meters.MeterId, meters.typeOfUtility, meters.units, RealReadDate, TCh{} as reading FROM accum
                JOIN meters ON meters.ModbusId = accum.SN
				WHERE RealReadDate BETWEEN '{}' AND '{}' AND meters.SN like '%{}' ORDER BY meters.SN, RealReadDate
			""".format(ch, start, endate, ch)
		
        cursor.execute(sql)
        reads += cursor.fetchall()

    if reads[len(reads)-1]['RealReadDate'].hour < 23:
        print("Incomplete data on", reads[len(reads)-1]['RealReadDate'])
        exit()
    
    return reads

def update_last_send(date):
	with open("C:\ptlspg\last_date.txt", "w") as f:
		f.write(date)

def connect_to_ftp_server():
	try:
		session = ftplib.FTP("intellimeter.info","ltw_cloud","ici315s01")
		#print("Connected to FTP server")
		return session
	except Exception as e:
		print(f"Failed to connect to Server. Due: {e}")
		
def send_file(session, filename, date):
    file = open(filename, 'rb')
    #print(f"Uploading File {filename} to Server")
    try:
        '''session.storbinary("STOR " + os.path.basename(filename), file)
        logging.info(f"{filename} sent successfully")
        print(f"{filename} sent successfully")
        update_last_send(date)'''
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection("intellimeter.info",username="ltw_cloud",password="ici315s01", cnopts=cnopts) as sftp:
            with sftp.cd('files'):
                sftp.putfo(file,os.path.basename(filename))
                
        logging.info(f"{filename} sent successfully")
        print(f"{filename} sent successfully")
        update_last_send(date)
    except Exception as e:
        logging.critical(f"An error ocurred: {e}")
        exit()
	
    file.close()
	
def create_file(filename, readings):
    with open(filename,'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Property','Project number','SN','Name','Utility','Units','Time stamp','Consumption'])
        for r in readings:
            writer.writerow([pfx,project_number,r['SN'],r['MeterId'],r['typeOfUtility'],r['units'],r['RealReadDate'],r['reading']])

def main():
    with open("C:\ptlspg\last_date.txt") as f:
        date = f.readlines()
    
    previous_date = datetime.strptime(date[0],"%Y-%m-%d")
    previous_date = previous_date + timedelta(days=1)

    today = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    #print(today)
    while previous_date < today:
        new_date = previous_date
        new_date_str = datetime.strftime(new_date, "%Y-%m-%d")
        date_name = datetime.strftime(new_date, "%Y%m%d")
        filename = "C:\ptlspg\csv\\" + pfx + "_" + eq + "_" + date_name + ".csv"

        readings = get_readings(new_date)
        if len(readings) > 0:
            create_file(filename,readings)
	    	#print(previous_date, new_date, filename)
            #session = connect_to_ftp_server()
            send_file(None, filename, new_date_str)
            #session.quit()

        previous_date = previous_date + timedelta(days=1)
		
main()