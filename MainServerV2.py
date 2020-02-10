import socket
import cv2
import ipaddress
import pickle
import time
from select import select
from multiprocessing import Process, Manager

my_ip = socket.gethostbyname(socket.gethostname())
my_ip = my_ip.split('.')
print(my_ip)

video_capture = cv2.VideoCapture(0)
counter = 0
scale = 1
AdressList = []
ToMonitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setblocking(False)
server_socket.bind((f'{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{my_ip[3]}', 5000))
server_socket.listen()


# Methods to encode/decode ip adresses
# int(ipaddress.IPv4Address('192.168.1.1'))
# str(ipaddress.IPv4Address(3232235777))

# temp_adr = []

def print_req(client):
    r = client.recv(2048)
    print(pickle.loads(r))

def acceptRequest(server_socket):
    client_soc, adrr = server_socket.accept()
    # temp_adr.append({'Adress': adrr[0], 'Port': adrr[1]})
    print(str(adrr) + ' connected')

    ToMonitor.append(client_soc)


def handleRequest(client_soc):
    path = ''
    try:
        request = client_soc.recv(4096)
        http_res = repr(request)
        print(http_res)

        path = http_res.split()[1]
    except:
        ToMonitor.remove(client_soc )
        print('no way')
        return

    if path == '/':
        client_soc.send('200'.encode())
        client_soc.close()
        ToMonitor.remove(client_soc)
    elif path == '/new':
        if ({client_soc.getsockname()[0]}, {client_soc.getsockname()[1]}) not in AdressList:
            AdressList.append(({client_soc.getsockname()[0]}, {client_soc.getsockname()[1]}))
        print('Adress list - ' + str(AdressList))
        client_soc.send(f'{my_ip[0]}.{my_ip[1]}.{my_ip[2]}.{my_ip[3]}:/5000'.encode())
        client_soc.close()
        ToMonitor.remove(client_soc)
    elif path == '/print':
        print_req(client_soc)
        client_soc.close()
        ToMonitor.remove(client_soc)



def makeSendFrame():
    global counter
    print('sended')
    # if len(AdressList) > 0:
    #     ret, frame = video_capture.read()
    #
    #     small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
    #
    #     rgb_small_frame = small_frame[:, :, ::-1]
    #     # Encode image
    #     img = pickle.dumps(rgb_small_frame)
    #     # Send imagew
    #
    #     send_sok = socket.socket()
    #     send_sok.connect(AdressList[counter][0])
    #     send_sok.send('POST /handle '.encode() + img)
    #     send_sok.close()
    #
    #     counter += 1
    #     if counter > len(AdressList) - 1:
    #         counter = 0
    # else:
    #     time.sleep(1)


def ready_f(ToMonit, ready):

    ready, _, _ = select(ToMonit, [], [])



def eventLoop():
    while True:
        man = Manager()
        ready = man.list()
        process = Process(target=ready_f, args=(ToMonitor, ready))
        process.start()
        while process.is_alive():
            print('send')
            makeSendFrame()
        process.join()
        # process.close()
        input("-------------------------------------------------------------------")
        for sok in ready:
            if sok is server_socket:
                acceptRequest(sok)
            else:
                handleRequest(sok)

        makeSendFrame()


if __name__ == '__main__':
    ToMonitor.append(server_socket)
    eventLoop()


