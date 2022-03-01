# -- coding: utf-8 --
# import the necessary packages
from imutils.video import VideoStream
from flask import Response, Flask, render_template
import threading
import datetime
import imutils
import time
import cv2
import socket


cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ip = s.getsockname()[0]

# 初始化用于确保输出帧的线程安全交换的锁（当多个浏览器/选项卡正在查看流时很有用）
lock = threading.Lock()

# 初始化一个flask对象
app = Flask(__name__)

# 预热
vs = VideoStream(src=0).start()
time.sleep(2.0)


@app.route("/")
def index():
    # 返回渲染的模板
    return render_template("index.html")


def generate():
    # 获取对输出帧的全局引用并锁定变量
    global lock

    # 循环输出流中的帧
    while True:
        # 等到获得锁
        with lock:
            frame = vs.read()
            frame = imutils.resize(frame, width=480)

            # 打时间戳
            timestamp = datetime.datetime.now()
            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 215, 0), 1)

            # 图像灰化，降低计算复杂度
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 平滑滤波
            # gray = cv2.blur(frame, (3, 3))
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            # 利用分类器识别出哪个区域为人脸
            faceRects = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
            if len(faceRects) > 0:
                for faceRect in faceRects:
                    x, y, w, h = faceRect
                    # 在摄像头中实时检测跟踪框出人脸区域
                    cv2.rectangle(frame, (x - 3, y - 3), (x + w + 3, y + h + 3), (0, 255, 0), thickness=2)

            # 以JPEG格式编码帧
            (flag, encodedImage) = cv2.imencode(".jpg", frame)

            # 确保帧已成功编码
            if not flag:
                continue

        # Press 'ESC' for exiting video
        # k = cv2.waitKey(100) & 0xff
        # if k == 27:
        #     break

        # 产生字节格式的输出帧
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # 返回与特定媒体类型（mime 类型）一起生成的响应
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(host="192.168.1.101", port=8000, debug=True, threaded=True, use_reloader=False)
# release the video stream pointer
print("test")
vs.stop()
