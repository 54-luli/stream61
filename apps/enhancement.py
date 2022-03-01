import streamlit as st
import myfunctions
import time
from streamlit_lottie import st_lottie


# PWD = os.path.dirname(os.path.dirname(__file__))


# 图像增强
def photo_enhancement():
    c1, c3 = st.columns(2)
    with c1:
        # 网页标题
        st.warning(myfunctions.web_title("PE")['t'])
        st.caption(myfunctions.web_title("PE")['c'])
        st.markdown('''---''')  # 分割线
    with c3:
        st_lottie(myfunctions.display_animation(3), key="1", height=225)
    # 显示当前时间
    myfunctions.show_datetime(1)
    st.markdown('''---''')  # 分割线
    st.error("#### 该功能尚在调试中")
    # 上传多个文件 Upload multi files
    st.info("上传文件")
    up_loaded_files = st.file_uploader(label="请选择上传文件（upload）", accept_multiple_files=False,
                                       help="选择您想要上传的文件")
    if st.button(label="开始增强(Go Enhancement)"):
        if up_loaded_files:
            # 计算等待
            placeholder = st.empty()
            with st.spinner('### 计算中...'):
                # 这里以后加上运行命令
                time.sleep(1)
            placeholder.success('Done!')
            placeholder.empty()
            c1, c2 = st.columns(2)
            c1.info("# Before")
            c2.info("# After")
            st.image("dped/output/pic1.png", caption='This is a test')
        else:
            st.error("#### 您还未选择文件")
