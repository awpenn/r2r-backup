import paramiko
from scp import SCPClient
from dotenv import load_dotenv
import os

load_dotenv()
SERVER = os.getenv('SERVER')
PORT = os.getenv('PORT')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
SOURCE_DIR = os.getenv('SOURCE-DIR')
LOCAL_DIR = os.getenv('LOCAL-DIR')
REMOTE_DIR = os.getenv('REMOTE-DIR')
KEY_FILENAME = os.getenv('KEY_FILENAME')



def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password, allow_agent=False,look_for_keys=False)
    client.connect(server, port, user, password, key_filename)
    return client

ssh = createSSHClient(SERVER, PORT, USER, PASSWORD, key_filename)
scp = SCPClient(ssh.get_transport())