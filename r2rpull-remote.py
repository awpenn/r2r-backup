## This code for two-machine process where script lives on "source server", creates tar and sends to remote storage

import paramiko
from scp import SCPClient
from dotenv import load_dotenv
import os
import os.path
import tarfile
import shutil
import datetime

load_dotenv()

SOURCE_DIR = os.getenv('SOURCE-DIR')

REMOTE_DIR = os.getenv('REMOTE-DIR')
REMOTE_SERVER = os.getenv('REMOTE-SERVER')
REMOTE_PORT = os.getenv('REMOTE-PORT')
REMOTE_USER = os.getenv('REMOTE-USER')
REMOTE_PASSWORD = os.getenv('REMOTE-PASSWORD')

dir_path = os.path.dirname(os.path.realpath('./'))

LOCAL_DIR = f"{dir_path}/r2r-backup/pulled-files"



def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect(server, port, user, password, key_filename)
    client.connect(hostname=server,username=user, password=password)
    
    return client

def clear_dirs(dir_path):
    tindex = SOURCE_DIR.rindex('/')
    ## name of target source folder
    tail = SOURCE_DIR[tindex+1:]

    folders = os.listdir(f"{dir_path}/r2r-backup/pulled-files")
    for folder in folders:
        if folder == tail:
            shutil.rmtree(f"{dir_path}/r2r-backup/pulled-files/{folder}")

    files = os.listdir(f"{dir_path}/r2r-backup/output-files")
    for file in files:
        if file not in ['README.md', '.gitignore']:
            os.remove(f"{dir_path}/r2r-backup/output-files/{file}")


def make_tarfile(output_filename, source_dir):
    print('building tar file...')

    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

    print('tar file created...')

def get_tarfile(dir_path):
    files = os.listdir(f"{dir_path}/r2r-backup/output-files")
    for file in files:
        if file not in [".gitignore", "README.md"]:
            tarname = file
            return tarname

def main():
    global dir_path

    clear_dirs(dir_path)

    timestamp = str( datetime.date.today() )

    print('pulling files into r2r...')
    ## getting files from source server
    
    ## name of target source folder
    tindex = SOURCE_DIR.rindex('/')
    tail = SOURCE_DIR[tindex+1:]
    shutil.copytree(SOURCE_DIR, f"{LOCAL_DIR}/{tail}")
    print('files pulled into r2r...')

    ## building tar file from pulled dirs
    make_tarfile( f"{dir_path}/r2r-backup/output-files/{timestamp}-db-backup.tar.gz", LOCAL_DIR )

    ## setting up connection to storage location
    ssh = createSSHClient(REMOTE_SERVER, REMOTE_PORT, REMOTE_USER, REMOTE_PASSWORD)
    scp = SCPClient( ssh.get_transport() )

    timestamp = str( datetime.date.today() )

    ## getting name of tar file to send
    print('pushing files to remote server...')
    tarname = get_tarfile(dir_path)
    print(tarname)
    ## putting tar file in storage location
    scp.put(f'{dir_path}/r2r-backup/output-files/{tarname}', REMOTE_DIR)
    print('files pushed to remote server...')

if __name__ == '__main__':
    main()



