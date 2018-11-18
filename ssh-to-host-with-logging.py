import paramiko
import socket
import logging

logging.basicConfig(level=logging.INFO, filename='myapp.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.debug('---Start logging----')

mydevices = ['vm1', 'vm2', 'adsads']
mycommand = ['uptime', 'ping -c 3 pi', 'vnstat']
myusername = ['xxxxx']
mypassword = ['xxxxx']


for i in mydevices[:]:
    try:
        print("Connection to host {}.".format(i))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(i, username=myusername[0], password=mypassword[0], timeout=30)
        logging.info('connected to %s: ', i)
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials:" )
        logging.error('%s raised an error', ssh)
        quit()
    except paramiko.SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
        logging.error('%s raised an error', ssh)
        quit()
    except paramiko.BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key: %s" % badHostKeyException)
        logging.error('%s raised an error', ssh)
        quit()
    except socket.error:
        print("Could not connect to {}.".format(i))
        logging.error('%s raised an error, Could not connect', ssh)
        quit()

    try:

        for m in mycommand[:]:
            stdin,stdout,stderr = ssh.exec_command(m)
            results = stdout.read()
            final_results = results.decode(encoding='UTF-8')
            print(final_results)
            logging.info('Command {} ran successfully!!'.format(m))
    except Exception as e:
        print("Operation error: %s", e)


logging.warning('---Stop logging----')
