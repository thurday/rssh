import rssh.client as rssh

user = 'root'
passwd = 'root'
server_ip = '127.0.0.1'

ssh = rssh.SSHClient(user,passwd,server_ip)
ssh.connect()

while True:
    command = str(input(f'{user}@{server_ip}~# '))
    if command == 'exit':
        break
    else:
        print(ssh.send(command))
ssh.kill()
