#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time
import paramiko
import sqlite3
import logging
import configparser
import socket

# read list of hosts from the hosts.txt file, ssh to the host, run the command uptime, and insert into db.
# pause for 5 sec, and then run again.

config = configparser.ConfigParser()
config.read('secrets.ini')

conn = sqlite3.connect('monitoring-agent.db')

logging.basicConfig(filename='demo.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')


with open('hosts.txt', 'r') as in_file:
    hosts = in_file.readlines()
    print(hosts)

class uptimeData():

    def __init__(self, host):
        self.command = 'uptime'
        self.username = config['auth']['username']
        self.password = config['auth']['password']
        self.host = host


    def ssh_to_host(self):
        # connect to the linux host with paramiko ssh library and run command "uptime".
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, username=self.username, password=self.password, timeout=30, look_for_keys=False)
            try:
                # print(self.command)
                stdin, stdout, stderr = ssh.exec_command(self.command)
                results = stdout.read()
                final_results = results.decode(encoding='UTF-8')
                # print("Command executed: {} ... Results: --> {}".format(self.command, final_results))
                return final_results
            except Exception as e:
                print("Operation error: %s", e)
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")

        except paramiko.SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)

        except paramiko.BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)

        except socket.error:
            print("Could not connect to {}".format(self.host))



class databaseData():

    def __init__(self, host, data_results):
        self.my_date = datetime.datetime.now()
        self.host = host
        self.data_results = data_results


    def update_database(self):
        # insert data into database.
        try:
            print(self.my_date, self.host, self.data_results)
            cur = conn.cursor()
            sql = "INSERT INTO tbl_uptime (datetime, hostname, uptime) VALUES (?, ?, ?)"
            cur.execute(sql, (self.my_date, self.host, self.data_results))
            conn.commit()
        except Exception as e:
            print("Operation error: %s", e)



if __name__ == "__main__":

    while True:
        logging.info("------------------- START --------------------------")
        for i in hosts:
            go = uptimeData(i.strip())
            results = go.ssh_to_host()
            update_db = databaseData(i.strip(), results)
            update_db.update_database()
        time.sleep(5)


        logging.info("----------------- FINISHED -------------------------")








