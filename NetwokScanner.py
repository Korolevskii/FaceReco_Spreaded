import socket
import subprocess
import requests
from pythonping import ping


my_ip = socket.gethostbyname(socket.gethostname())
my_ip = my_ip.split('.')
print(my_ip)

macines = []


for i in range(1, 255):
    # r = ping('f{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}', timeout=1, count=1).success()
    # if r:
    port = 5000
    print(f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}:{port}/')
    try:
        r = requests.get(f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}:{port}/', 'Helloo', timeout=0.05)
        macines.append(f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}:{port}/')
        while r.status_code != 200:
            try:
                print(f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}:{port}/')
                port += 1
                r = requests.get(f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}:{port}/', timeout=0.05)
                macines.append(f'http://{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{i}:{port}/')
            except requests.exceptions.ConnectionError:
                continue
    except requests.exceptions.ConnectionError:
        continue
print(macines)
