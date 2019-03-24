from fabric.api import *
import getpass
import datetime
import configparser

config = configparser.ConfigParser()
config.read('secrets.ini')
# secrets.ini file should contain username, password and hostname ... = wording ... no quotes.

mydate = datetime.datetime.now()
username = config['auth']['username']
password = config['auth']['password']
hostname1 = config['auth']['hostname1']
hostname2 = config['auth']['hostname2']

env.hosts = [hostname1, hostname2]
env.user = username
env.password = password
# env.parallel = True
env.skip_bad_hosts = True
env.timeout = 20
env.warn_only = True

def test_variables():
    print("hostname: {}".format(env.hosts[:]))

def get_host_type():
    run('uname -s')

def print_hostname():
    run('This is the hostname: {}'.format(env.hosts[0]))

def get_host_uptime():
    run('uptime')

def get_host_name():
    run('hostname -f')

def apt_update_upgrade():
    sudo('apt-get update')
    sudo('apt-get upgrade -y')

def backup_mailhost():
    sudo('/home/tones/mailinabox/management/backup.py')

def archive_userdata():
    sudo('tar cvzf /home/USERNAME/backup_{}_com.tar.gz /home/user-data/'.format(env.hosts[0]))

def transfer_archive_locally():
    get(remote_path="/home/USERNAME/backup_{}_com.tar.gz".format(env.hosts[0]), local_path="backup_{}_com.tar.gz".format(env.hosts[0]))

# login to server run a backup, archive it and dl it to local dir. If exsits will overwrite.
def perform_full_backup_and_dl_archive():
    backup_mailhost()
    archive_userdata()
    transfer_archive_locally()
