import streamlit as st
import myfunctions
from streamlit_lottie import st_lottie


# PWD = os.path.dirname(os.path.dirname(__file__))
# cascade = cv2.CascadeClassifier("apps/haarcascade_frontalface_alt2.xml")


# 智能拍照
def intelligent_photographing():
    c1, c3 = st.columns(2)
    with c1:
        # 网页标题
        st.warning(myfunctions.web_title("IP")['t'])
        st.caption(myfunctions.web_title("IP")['c'])
        st.markdown('''---''')  # 分割线
    with c3:
        st_lottie(myfunctions.display_animation(1), key="1", height=225)
    # 显示当前时间
    myfunctions.show_datetime(1)
    st.markdown('''---''')  # 分割线
    col1, col2 = st.columns(2)
    with col1:
        st.header("实时视频流")
        img_file_buffer = st.camera_input(label="", key='camera1', help="点击底部Take Photo按钮进行拍照")
        if img_file_buffer is not None:
            cv2_img, img_shape, img_name = myfunctions.get_cv2_img(img_file_buffer)
            st.write(img_shape)
            st.download_button(label="点击此处下载照片", data=img_file_buffer, file_name=img_name)
        # placeholder = st.empty()
        # if placeholder.button(label="开启推流"):
        #     placeholder.empty()
        #     img_file_buffer = st.camera_input(label="拍个照吧！", help="点击底部Take Photo按钮进行拍照")
            # st.image(show_image("test/images/background.png"), caption='This is a test', width=800)
            # st.video(data=myfunctions.show_video("test/videos/02.mp4"), format='video/mp4')
            # myfunctions.display_url_video('http://192.168.1.101:8000/video_feed', 0)
            # display_url_video('http://192.168.1.106:8080/?action=stream', 0)
            # display_url_video('https://www.bilibili.com/')
    with col2:
        # 上传多个文件 Upload multi files
        st.info("上传文件")
        up_loaded_files = st.file_uploader(label="请选择上传文件（upload）", accept_multiple_files=True,
                                           help="选择您想要上传的文件")
        if st.button("开始上传文件"):
            myfunctions.upload_file(up_loaded_files)

        # 下载单个文件
        st.info("下载文件")
        down_loaded_files = st.file_uploader(label="请选择下载文件（download）", accept_multiple_files=False,
                                             help="选择您想要下载的文件")
        if st.button("确认"):
            myfunctions.download_file(down_loaded_files)
