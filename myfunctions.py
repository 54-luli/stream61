import streamlit as st
import streamlit.components.v1 as components
import datetime
from PIL import Image
import time
import json
import os

# from imutils.video import VideoStream
# import imutils
import numpy as np
import cv2
import threading

PWD = os.path.dirname(__file__)
# cascade = cv2.CascadeClassifier("apps/haarcascade_frontalface_alt2.xml")
# 初始化用于确保输出帧的线程安全交换的锁（当多个浏览器/选项卡正在查看流时很有用）
lock = threading.Lock()


@st.experimental_memo
def web_title(s0):
    title = ""
    if s0 == "IP":
        title = "## 智能拍照服务(Intelligent Photographing)"
    elif s0 == "PE":
        title = "## 图像增强服务(Photo Enhancement)"
    elif s0 == "PS":
        title = "## 照片挑选服务(Photo Selection)"
    elif s0 == "TEST":
        title = "## 这是一个测试模块"
    caption = "### 基于树莓派"
    s = {'t': title, 'c': caption}
    return s


def show_datetime(x):
    if x == 0:
        t11, t12, t13 = st.columns(3)
        t11.success('## ' + datetime.datetime.now().strftime("%Y-%m-%d"))
        t12.success('## ' + datetime.datetime.now().strftime("%A"))
        t13.success('## ' + datetime.datetime.now().strftime("%X"))
    elif x == 1:
        a11, a12, a13, a14 = st.columns([2, 2, 2, 6])
        a11.success('##### ' + datetime.datetime.now().strftime("%Y-%m-%d"))
        a12.success('##### ' + datetime.datetime.now().strftime("%A"))
        a13.success('##### ' + datetime.datetime.now().strftime("%X"))


@st.experimental_memo
def show_image(dir_path):
    show_img_path = os.path.join(PWD, dir_path)
    image = Image.open(show_img_path)
    return image


@st.experimental_memo
def show_select_image(dir_path):
    image = Image.open(dir_path)
    return image


@st.experimental_memo
def show_video(dir_path):
    show_vid_path = os.path.join(PWD, dir_path)
    return show_vid_path


def upload_file(uploaded_files):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # bytes_data = uploaded_file.read()
            # st.write("文件名:", uploaded_file.name)
            # st.write(bytes_data)  # 这里会卡死
            # st.write("文件名:", uploaded_file.name)
            save_path = os.path.join(PWD, 'test/upload')
            # bytes_data = cv2.imread(os.path.join(PWD, 'test/images', uploaded_file.name), 1)
            if uploaded_file.name.split('.')[1] in ['jpg', 'png', 'JPG', 'PNG']:
                data = Image.open(uploaded_file)
                data.save(f'{save_path}/{uploaded_file.name}')
            # else:
            #     bytes_data = uploaded_file.read()
            #     cv2.imwrite(save_path, bytes_data)
        placeholder_up = st.empty()
        placeholder_up.success("文件已上传！")
        time.sleep(1)
        placeholder_up.empty()
    else:
        placeholder = st.empty()
        placeholder.error("您还未选择文件！")
        time.sleep(0.5)
        placeholder.empty()


def download_file(down_loaded_files):
    # downloaded_file = open(down_path, "rb")   #   不影响
    # # 下载按钮效果设置
    # css = """<style>
    #  .stDownloadButton>button {
    #      background-color: #0099ff;
    #     color:#ffffff;
    # }
    # .stDownloadButton>button:hover {
    #     background-color: #FA8072;
    #     color:#000000;
    #     }
    # </style>
    # """
    # st.markdown(css, unsafe_allow_html=True)
    if down_loaded_files:
        if st.download_button(label="开始下载文件", data=down_loaded_files, file_name=down_loaded_files.name):
            placeholder_down = st.empty()
            placeholder_down.success("文件已下载！")
            time.sleep(1)
            placeholder_down.empty()
    else:
        placeholder = st.empty()
        placeholder.error("您还未选择文件！")
        time.sleep(1)
        placeholder.empty()


def display_url_video(src, status):
    if status == 0:
        components.iframe(src=src, width=640, height=480, scrolling=True)
    elif status == 1:
        components.iframe(src=src, width=1440, height=1080, scrolling=True)
    # m3u8_url = 'https://new.iskcd.com/20211108/emE2oR9c/1400kb/hls/index.m3u8'
    # components.html(
    #     """
    #    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/dplayer/dist/DPlayer.min.css">
    # <script src="https://cdn.jsdelivr.net/npm/dplayer/dist/DPlayer.min.js"></script>
    # <script src="https://cdn.jsdelivr.net/npm/hls.js/dist/hls.min.js"></script>
    # <div id="dplayer"></div>
    # <script>
    #     const dp = new DPlayer({
    #         container: document.getElementById('dplayer'),
    #         video: {
    #             url: '%s',
    #             type: # 'hls'
    #         },
    #     });
    # </script>
    #
    #     """ % m3u8_url,
    #     width=1440, height=1280
    # )


@st.experimental_memo
def display_animation(nums):
    file = ""
    if nums == 0:
        file = "test/animation/31675-programming.json"
    if nums == 1:
        file = "test/animation/88282-rocket.json"
    if nums == 2:
        file = "test/animation/15597-boots-your-site.json"
    if nums == 3:
        file = "test/animation/16949-placeholder-day-night.json"
    if nums == 4:
        file = "test/animation/7192-404.json"
    with open(file, "r", errors='ignore') as f:
        data = json.load(f)
        return data


@st.experimental_memo
def get_cv2_img(img_file_buffer):
    # 使用 OpenCV 读取图像文件缓冲区:
    bytes_data = img_file_buffer.getvalue()
    # 这里将二进制流bytes_data数据转化为了<class 'numpy.ndarray'>数据,即从二进制文件到图片(numpy.ndarray)
    # 功能上同cv2.imread('photo.jpg')函数一样
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    cv2_img_shape = cv2_img.shape
    cv2_img_name = datetime.datetime.now().strftime("%Y_%m_%d_%X") + '_' + str(cv2_img.shape[0]) + 'x' + str(
        cv2_img.shape[1]) + '.png'
    return cv2_img_shape, cv2_img_name

# def generate_video():
#     # 获取对输出帧的全局引用并锁定变量
#     global lock
#
#     vs = VideoStream(src=0).start()
#     # 循环输出流中的帧
#     while True:
#         # 等到获得锁
#         with lock:
#             frame = vs.read()
#             # frame = imutils.resize(frame, width=480)
#
#             # 打时间戳
#             timestamp = datetime.datetime.now()
#             cv2.putText(frame, timestamp.strftime(
#                 "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 215, 0), 1)
#
#             # 图像灰化，降低计算复杂度
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             # 平滑滤波
#             gray = cv2.GaussianBlur(gray, (3, 3), 0)
#             # 利用分类器识别出哪个区域为人脸
#             faceRects = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
#             if len(faceRects) > 0:
#                 for faceRect in faceRects:
#                     x, y, w, h = faceRect
#                     # 在摄像头中实时检测跟踪框出人脸区域
#                     cv2.rectangle(frame, (x - 3, y - 3), (x + w + 3, y + h + 3), (0, 255, 0), thickness=2)
