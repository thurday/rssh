import rssh.client as rssh

user = 'root'
passwd = 'root'
server_ip = '127.0.0.1'

with open('public.key','rb') as fd:
    public = fd.read()
with open('private.key','rb') as fd:
    private = fd.read()

ssh = rssh.SSHClient(user,passwd,server_ip,public_key=public,private_key=private)
ssh.connect()

while True:
    command = str(input(f'{user}@{server_ip}~# '))
    if command == 'exit':
        break
    else:
        print(ssh.send(command))
ssh.kill()
