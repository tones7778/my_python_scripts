#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import paramiko
import sqlite3
import logging
import configparser
import mysql.connector

# read a list of hosts from file.
# ssh to the linux host.
# run and capture the results of 'uptime'
# save to a mysql db




config = configparser.ConfigParser()
config.read('secrets.ini')

logging.basicConfig(filename='demo.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

logging.info("------------------- START ---------------------------------------")
mydate = datetime.datetime.now()
#mydevice = config['auth']['hostname']
mycommand = 'uptime'
myusername = config['auth']['username']
mypassword = config['auth']['password']
myport = 22
#mykey = paramiko.RSAKey.from_private_key_file('id_rsa', password=mypassword)

try:



    with open('hosts.txt', 'r') as in_file:
        content = in_file.readlines()

        for mydevice in content:
            try:
                conn = mysql.connector.connect(host='vm2.home.lan',
                                               database='monitoring_agent',
                                               user=config['auth']['username'],
                                               password=config['auth']['password'])
                if conn.is_connected():
                    print("Connected to MySQL Database .....")

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=mydevice.rstrip(), username=myusername, password=mypassword, port=myport, timeout=5, look_for_keys=False)
                stdin, stdout, stderr = ssh.exec_command(mycommand)
                results = stdout.readlines()
                for i in results:
                    print("Results for host:", mydevice, i)
                    mycursor = conn.cursor()
                    sql_insert = "INSERT INTO _tbl_uptime (datetime, hostname, uptime) VALUES (%s, %s, %s)"
                    mycursor.execute(sql_insert, (mydate, mydevice.strip(), i.strip()))
                    conn.commit()
                conn.close()
            except Exception as error:
                print("ERROR1: " + str(error) + " for: " + str(mydevice))
                logging.debug("ERROR: " + str(error))

            ssh.close()
        in_file.close()
        logging.info("--------------------- FINISHED -------------------------")

except Exception as error:
    print("ERROR2: " + str(error))
    logging.debug("ERROR: " + str(error))
    quit()










