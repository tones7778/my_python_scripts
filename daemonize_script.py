from __future__ import print_function

 

import cx_Oracle

import datetime

import time

import logging

from logging.handlers import RotatingFileHandler

 

# Status: [DEVELOPMENT] Jan-10-2020

# Issues: data is mismatched in the logs, Leakage from fucnction calls.

 

#-----------------------------------------------------------------------------------------------------------

log_file = "subnet_reports.log"

 

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

#logger.propagate = False

 

#console_output = logging.StreamHandler()  # send logs to console (Working!!)

# console_output.setLevel(logging.DEBUG)

#logger.addHandler(console_output)

 

file_output = logging.handlers.RotatingFileHandler(log_file, mode='w', maxBytes=5242880, backupCount=5)  # 5 MByte Files / Total 5 files.

logger.addHandler(file_output)

 

#logger.info("{}, {}, {}, {}, {}".format(datetimestamp, subnet, dynamic_allocation_total, wireless_users_online, utilized))

 

 

 

 

def _10_1_152_0_21_subnet_report(cursor): # subnet_id=16143

    subnet = " _10_1_152_0_21_subnet_report"

 

    query1 = ("""

        SELECT count(*) as xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

       """)

    result1 = cursor.execute(query1)

 

    for row in result1:

        dynamic_allocation_total = row[0]

        # print(row)

 

    query2 = ("""

        SELECT count(*) as xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        """)

    result2 = cursor.execute(query2)

 

    for row in result2:

        wireless_users_online = row[0]

        # print(row)

 

    utilized = (100 * float(wireless_users_online) / float(dynamic_allocation_total)) # 100 * float(514) / float(2038)

 

    print("RESULTS: {}, {}, {}, {}, {}".format(datetimestamp, subnet, dynamic_allocation_total, wireless_users_online, utilized))

    logger.info("{}, {}, {}, {}, {}".format(datetimestamp, subnet, dynamic_allocation_total, wireless_users_online, utilized))

 

 

 

 

if __name__ == "__main__":

    while True:

 

        datetimestamp = datetime.datetime.now().ctime()  # get date and time for writing to log file.

 

        try:

            dsn_tns = cx_Oracle.makedsn('XXXXXXXXXXX', '1521', service_name='XXXXXXXXXXXX')

            connection = cx_Oracle.connect(user=’username’, password=’password, dsn=dsn_tns)  # Read/Only account.

            cursor = connection.cursor()

 

            _10_1_152_0_21_subnet_report(cursor)

           

        except Exception as e:

            print("Operation error: {}".format(e))

 

        cursor.close()

        connection.close()

 

        time.sleep(5) # Tell the time once an hour

 
