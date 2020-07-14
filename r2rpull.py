import paramiko
from scp import SCPClient
from dotenv import load_dotenv
import os
import os.path
import tarfile

load_dotenv()
SERVER = os.getenv('SERVER')
PORT = os.getenv('PORT')
SOURCE_USER = os.getenv('SOURCE-USER')
REMOTE_USER = os.getenv('REMOTE-USER')
PASSWORD = os.getenv('PASSWORD')
SOURCE_DIR = os.getenv('SOURCE-DIR')
LOCAL_DIR = os.getenv('LOCAL-DIR')
REMOTE_DIR = os.getenv('REMOTE-DIR')
KEY_FILENAME = os.getenv('KEY_FILENAME')

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect(server, port, user, password, key_filename)
    client.connect(hostname=server,username=user, password=password)
    return client

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

ssh = createSSHClient(SERVER, PORT, SOURCE_USER, PASSWORD)
scp = SCPClient(ssh.get_transport())

scp.get(SOURCE_DIR, LOCAL_DIR, recursive=True)

make_tarfile("/Users/andrewwilk/Desktop/database-projects/r2r-backup/tada", LOCAL_DIR)




