import paramiko
from scp import SCPClient
from dotenv import load_dotenv
import os
import os.path
import tarfile
import shutil
import datetime

load_dotenv()
SERVER = os.getenv('SERVER')
PORT = os.getenv('PORT')
SOURCE_USER = os.getenv('SOURCE-USER')
REMOTE_USER = os.getenv('REMOTE-USER')
PASSWORD = os.getenv('PASSWORD')
SOURCE_DIR = os.getenv('SOURCE-DIR')
REMOTE_DIR = os.getenv('REMOTE-DIR')
KEY_FILENAME = os.getenv('KEY_FILENAME')

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
    folders = os.listdir(f"{dir_path}/r2r-backup/pulled-files")
    for folder in folders:
        if folder == 'bkps':
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

def main():
    global dir_path

    clear_dirs(dir_path)

    ssh = createSSHClient(SERVER, PORT, SOURCE_USER, PASSWORD)
    scp = SCPClient( ssh.get_transport() )

    timestamp = str( datetime.date.today() )

    print('Pulling files from db server...')
    scp.get( SOURCE_DIR, LOCAL_DIR, recursive=True )
    print('Files pulled from database server...')

    make_tarfile( f"{dir_path}/r2r-backup/output-files/{timestamp}-db-backup.tar.gz", LOCAL_DIR )


if __name__ == '__main__':
    main()



