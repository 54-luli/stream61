import streamlit as st
import myfunctions
from streamlit_lottie import st_lottie

import socket


# PWD = os.path.dirname(os.path.dirname(__file__))


# 测试模块
def my_test():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]

    c1, c3 = st.columns(2)
    with c1:
        # 网页标题
        st.warning(myfunctions.web_title("TEST")['t'])
        st.caption(myfunctions.web_title("TEST")['c'])
        st.markdown('''---''')  # 分割线
    with c3:
        st_lottie(myfunctions.display_animation(4), key="1", height=225)
    # 显示当前时间
    myfunctions.show_datetime(1)
    st.markdown('''---''')  # 分割线
    c11, c12 = st.columns([1, 3])
    with c11:
        st.info("### 在这里输入您的链接:")
    with c12:
        url = st.text_input("本机IP地址是：http://" + ip + '，' + "视频流地址为：" + "http://" + ip + ":8000" + "/video_feed"
                            + "，复制此地址到下方输入栏中")
    st.markdown("[视频流地址超链接](https://www.bilibili.com/)")
    if url:
        myfunctions.display_url_video(url, 0)
        # display_url_video('https://www.bilibili.com/', 1)

    # 2022/2/24测试模块
    _, d11, _ = st.columns([1, 4, 1])
    # 这相当于一个按钮，在窗口底部
    with d11:
        img_file_buffer = st.camera_input(label="拍个照吧！", key='camera_test', help="点击底部Take Photo按钮进行拍照")
        if img_file_buffer is not None:
            img_shape, img_name = myfunctions.get_cv2_img(img_file_buffer)
            # Check the shape of cv2_img:Should output shape: (height, width, channels)
            st.write(img_shape)
            # st.write(type(cv2_img))
            # st.write(type(img_file_buffer))
            st.download_button(label="点击此处下载照片", data=img_file_buffer, file_name=img_name)
