from flask import Flask, request
import requests
import socket
import cv2
import multiprocessing
import time
import pickle

app = Flask(__name__)

sess = requests.session()

AdressList = []


@app.route('/')
def home():
    return 'ok'


def makeAsyncLoop(links):  # Распредилитель изображений
    video_capture = cv2.VideoCapture(0)
    counter = 0
    scale = 1
    print(str(links) + ' - links are looped')
    while True:
        if len(links) == 0:
            return 0
        ret, frame = video_capture.read()  # Чтение кадра с камеры

        small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)  # При небходимости, уменьшение разрешения кадра
        rgb_small_frame = small_frame[:, :, ::-1]

        img = pickle.dumps(rgb_small_frame)  # Сериализация изображения
        try:
            requests.post(links[counter] + 'handle', data=img)  # Попытка отправить следующий кадр
        except:
            links.remove(links[counter])  # Удалить ссылку из списка если она не доступна

        counter += 1
        if counter > len(links) - 1:
            counter = 0


process = multiprocessing.Process(target=makeAsyncLoop, args=(AdressList,))


@app.route("/print", methods=["POST"])
def sent_message():  # Вывод результатов обработки кадра
    data = request.data
    print(pickle.loads(data))
    return '200'


@app.route('/new')
def setNewWorker():  # Метод регестрирующий новый компьютер
    url = request.json['url']
    AdressList.append(url)
    time.sleep(1.5)
    requests.get(url + 'setUrl', json={'url': 'http://' + socket.gethostbyname(socket.gethostname()) + ':5000/'})
    restart()
    return '200'



@app.route('/restart')
def restart():  # Перезапуск процесса, отправляющего изображения
    global process
    process.terminate()

    for lin in AdressList:
        try:
            requests.get(lin + 'ready')
        except:
            AdressList.remove(lin)

    process = multiprocessing.Process(target=makeAsyncLoop, args=(AdressList,))
    process.start()

    """
    Процесс распределяющий нагрузку запускается параллельно,
    для того чтобы главный процесс мог принимать и отправлять запросы
    """
    return "200"


if __name__ == '__main__':
    process.start()
    app.run(host=socket.gethostbyname(socket.gethostname()), port=5000)
