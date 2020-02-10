from flask import Flask, request
import requests
import socket
import pandas as pd
import ipaddress
import os
import pickle

app = Flask(__name__)

AdressList = []


@app.route("/print", methods=["POST"])
def sent_message():
    data = request.data
    print(pickle.loads(data))
    return '200'


# Methods to encode/decode ip adresses
# int(ipaddress.IPv4Address('192.168.1.1'))
    # str(ipaddress.IPv4Address(3232235777))


@app.route('/set', methods=['POST', 'GET'])
def setNewWorker():
    # Json {'Name' : str, 'Ip' : int, 'Port' : int, 'params' : str}
    jsn = request.json
    name = jsn['Name']
    ip = jsn['Ip']
    port = jsn['Port']
    params = jsn['params']
    AdressList.append('http://'+ip+':'+str(port))
    print('http://'+ip+':'+str(port))
    return '200'


@app.route('/get')
def getWorkerLinks():
    links = ''
    for i in AdressList:
        links += i + " "
    print('links done')
    return {'links': links}


@app.route('/start')
def start():
    links = ''
    for i in AdressList:
        links += i + " "
    print('start wanted')
    return '200'

req = requests.post('http://5.101.77.75:5000/setIp', json={'Ip': socket.gethostbyname(socket.gethostname())})

app.run(host=socket.gethostbyname(socket.gethostname()), port=5000)


