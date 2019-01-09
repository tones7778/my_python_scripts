# update Jan 2019
#TODO: Produce json out put instead.
#TODO: Insert to sql database.


import paramiko
import socket
import configparser
import sys
from loguru import logger

config = configparser.ConfigParser()
config.read('secrets.ini')
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add("ssh-to-host.log", rotation="500 MB")


mydevices = ['vm1.home.lan', 'vm2.home.lan', 'FAKE-SERVER']
mycommand = ['uptime', 'ping -c 3 pi', 'free -m', 'BLAH-BLAH']
myusername = config['auth']['username']
mypassword = config['auth']['password']

while True:
    for i in mydevices[:]:
        try:
            print("Connection to host {}.".format(i))
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(i, username=myusername, password=mypassword, timeout=30)
            logger.opt(record=True).info("log: Connected to host: {}".format(i))
            try:
                for m in mycommand[:]:
                    stdin, stdout, stderr = ssh.exec_command(m)
                    results = stdout.read()
                    final_results = results.decode(encoding='UTF-8')
                    print(final_results)
            except Exception as e:
                print("Operation error: %s", e)
                logger.opt(record=True).info("log: Operation error: {}".format(i))

        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            logger.opt(record=True).info("log: Authentication failed, please verify your credentials: {}".format(i))
            quit()
        except paramiko.SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            logger.opt(record=True).info("log: Unable to establish SSH connection: {}".format(i))
            quit()
        except paramiko.BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            logger.opt(record=True).info("log: Unable to verify server's host key: {}".format(i))
            quit()
        except socket.error:
            print("Could not connect to {}".format(i))
            logger.opt(record=True).info("log: Could not connect server: {}".format(i))
            #quit()



