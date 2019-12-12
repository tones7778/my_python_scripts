import paramiko

import time

# This is working !!!!!


host = 'server'
username = 'XXXXXX'
password = 'XXXXXXXXX'
command = "sudo -k systemctl status systemd-resolved.service"

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=username, password=password)

transport = ssh.get_transport()
session = transport.open_session()
session.set_combine_stderr(True)
session.get_pty()
session.exec_command(command)
stdin = session.makefile('wb', -1)
stdout = session.makefile('rb', -1)
stdin.write(password + '\n')
stdin.flush()
for line in stdout.read().splitlines():
    print('host: {}: {}'.format(host, line))
ssh.close()
