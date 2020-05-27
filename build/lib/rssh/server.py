import socket,base64,subprocess
from time import sleep
from threading import Thread
from . import rsa

class error(Exception):
    pass

class SSHServer:
    def __init__(self,ip,port=22,public_key=None,private_key=None,key_bits=4096,max_connections=5):
        self.ip = ip
        self.port = port
        self.max_connections = max_connections

        self.clients = {}

        if public_key and private_key:
            self.key = rsa.Rsa(public_key=public_key,private_key=private_key,key_bits=key_bits) # Import Key
        else:
            self.key = rsa.Rsa(key_bits=key_bits) # Generate Key

    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.bind((self.ip,self.port))
            self.sock.listen(self.max_connections)

            print(f"RSSH: Listening on {self.ip}:{self.port}")

            while True:
                conn, addr = self.sock.accept()
                self.clients[addr[0]] = HandleClient(conn,addr,self.key)

                print(f"RSSH: Received a new connection from {addr[0]}:{addr[1]}")
        except socket.error as err:
            raise error(f"Error binding socket: {err}")

    def kill(self,addr):
        if addr in self.clients:
            self.clients[addr].kill()
            self.clients.__delitem__(addr)
        return True

class HandleClient:
    def __init__(self,conn,addr,key):
        self.server_key = key
        self.client_key = None
        self.conn = conn
        self.addr = addr

        self.line_count = 0
        self.ok = True

        Thread(target=self.handle).start()

    def kill(self):
        self.conn.close()
        return True

    def handle_keys(self):
        try:
            print('RSSH: Sending key')
            self.conn.sendall(self.server_key.public_key)
            self.client_key = self.conn.recv(8192)
            print("RSSH: Received key")
            self.client_key = rsa.Rsa(self.client_key)
        except socket.error as err:
            raise error(f"\n\tRSSH: Error sendind server public key: {err}")

        return True

    def validate_user_passwd(self,user,passwd):
        FAIL = 'Password: \r\nsu: Authentication failure'
        FAIL = 'su: Authentication failure'

        try:
            cmd = f'{{ sleep 1; echo "{passwd}"; }} | script -q -c "su -l {user} -c ls" /dev/null'
            ret = subprocess.check_output(cmd, shell=True)
            res = ret.strip()

            if FAIL in res.decode():
                return 'error:Invalid Password'
            else:
                print('RSSH: User validated')
                return 'success:true'
        except Exception as err:
            raise error(f"\n\tRSSH: Error validating user password: {err}")

    def handle(self):
        self.handle_keys()

        user, passwd = self.server_key.decrypt(self.conn.recv(8192)).split("&")
        try:
            validate = self.validate_user_passwd(user,passwd)

            self.conn.sendall(self.client_key.encrypt(validate))

            if "error" in validate:
                self.conn.close()
                return False

        except error as err:
            print(err)
            self.conn.sendall(self.client_key.encrypt("error:Unknown Error"))
            self.conn.close()
            return False

        while True:
            try:
                original = self.server_key.decrypt(self.conn.recv(8192))
                
                command = ["echo",f"{passwd}","|","su","-l",f"{user}",'-c']
                command += original.split()
                
                cmd = f'{{ sleep 1; echo "{passwd}"; }} | script -q -c "su -l {user} -c {original}" /dev/null'

                self.proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

                data, derr = self.proc.communicate()

                self.conn.sendall(self.client_key.encrypt(str(data.decode()+derr.decode())))

            except Exception as err:
                print(err)
                break

        self.conn.close()
