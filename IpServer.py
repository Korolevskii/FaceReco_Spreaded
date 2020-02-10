from flask import Flask, request
import requests

app = Flask(__name__)

ip = 0

free_port = 5001


@app.route('/getIp')
def getMainIpByName():
    return {'Ip': ip}


@app.route('/setIp', methods=['POST'])
def setMainIp():
    global ip
    req = request.json
    print(req)
    ip = req['Ip']
    return '200'



@app.route('/getPort')
def getPort():
    global free_port
    free_port += 1
    return {"Port": free_port}


app.run(host='5.101.77.75', port=5000)
