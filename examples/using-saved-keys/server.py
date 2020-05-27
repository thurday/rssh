import rssh.server as rssh
from threading import Thread
from time import sleep

ssh = None

with open('public.key','rb') as fd:
    public = fd.read()
with open('private.key','rb') as fd:
    private = fd.read()

def start():
    global ssh

    ssh = rssh.SSHServer('127.0.0.1',private_key=private,public_key=public)
    print('Key generated')
    
    ssh.start()
    print('Server started')

Thread(target=start).start()

while True:
    print("RSSH - Github: https://github.com/ReddyyZ/rssh\n1.List online clients\n2.Kill")
    option = int(input('-> '))
    if option == 1:
        for i in ssh.clients:
            print(ssh.clients[i].addr[0])
    elif option == 2:
        ip = str(input('IP -> '))
        ssh.kill(ip)
    else:
        print('Invalid option')
