import socket,base64
from time import sleep
from . import rsa

class error(Exception):
    pass

class SSHClient:
    def __init__(self,user,passwd,ip,port=22,public_key=None,private_key=None):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd

        self.key = rsa.Rsa(public_key=public_key,private_key=private_key)
        self.server_key = None

    def handle_keys(self):
        key = self.sock.recv(4096)
        self.server_key = rsa.Rsa(public_key=key)
        self.sock.sendall(self.key.public_key)

        return True

    def login(self):
        try:
            self.sock.sendall(self.server_key.encrypt(str(f"{self.user}&{self.passwd}")))
            response = self.key.decrypt(self.sock.recv(8192))

            if response.startswith('error:'):
                err = response.split(':')[1]
                raise error(f"\n\tRSSH: {err}")
            elif 'success:true' in response:
                return True
        except socket.error as err:
            raise error(f"\n\tRSSH: Socket error: {err}")


    def connect(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.ip,self.port))
        self.handle_keys()
        self.login()

    def send(self,text):
        try:
            sleep(0.2)
            if not text:
                self.sock.sendall(self.server_key.encrypt("\n"))
            else:
                self.sock.sendall(self.server_key.encrypt(text))

            sleep(5)

            recv = self.recv()
            if recv:
                return recv
            else:
                return False
        except socket.error as err:
            raise error(f"\n\tRSSH: Socket error sending command: {err}")

    def recv(self):
        try:
            response = self.key.decrypt(self.sock.recv(8192))

            if response.startswith('error:'):
                erro = response.split(':')[1]
                raise error(f"\n\tRSSH: {erro}")
            elif 'RSSH:empty' in response:
                return "\n"
            else:
                return response
        except socket.error as err:
            raise error(f"\n\tRSSH: Error receiving response: {err}")

    def kill(self):
        self.sock.close()
        return True
