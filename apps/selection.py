import streamlit as st
from streamlit_lottie import st_lottie
import os
import time
import myfunctions
from PIL import Image
import xcc_ps.al_select as xcc


# PWD = os.path.dirname(os.path.dirname(__file__))


# 最佳照片挑选
def photo_selection():
    c1, c3 = st.columns(2)
    with c1:
        # 网页标题
        st.warning(myfunctions.web_title("PS")['t'])
        st.caption(myfunctions.web_title("PS")['c'])
        st.markdown('''---''')  # 分割线
    with c3:
        st_lottie(myfunctions.display_animation(2), key="1", height=225)
    # 显示当前时间
    myfunctions.show_datetime(1)
    st.markdown('''---''')  # 分割线

    # 上传照片 Upload multi files
    st.info("请上传您的照片：")
    uploaded_files = st.file_uploader(label="请选择上传文件（upload）", accept_multiple_files=True,
                                      type=['jpg', 'png', 'jpeg'], help="选择您想要上传的文件")
    # 展示结果
    if st.button(label="开始挑选(Go Selection)"):
        if uploaded_files:
            save_path = os.path.join(myfunctions.PWD, 'xcc_ps/data/61/')
            # 计算等待
            placeholder_1 = st.empty()
            placeholder_1.info("#### 正在计算中...")
            # 先将原始输入目录下的照片清空
            xcc.del_file(save_path)
            time.sleep(0.5)
            # 将上传的照片先保存到挑选算法的输入目录
            for file in uploaded_files:
                data = Image.open(file)
                data.save(f'{save_path}/{file.name}')
            time.sleep(2)
            # xcc挑选算法
            score_of_photo, out_photo, model_time, run_time = xcc.my_ps()
            # 计算完成
            placeholder_1.success('#### Done!')
            time.sleep(1)
            placeholder_1.empty()
            # 展示结果
            r11, r12, r13 = st.columns([2, 2, 2])
            r11.success("#### 输入图像")
            r12.success("#### 最佳图像")
            r13.success("#### 挑选结果(图片名-得分)")
            t11, t12 = st.columns([3, 3])
            t11.info("#### 输入图像")
            t12.info("#### 最佳图像")

            # 原始图片路径
            ps_path = os.path.join(myfunctions.PWD, "xcc_ps/data/61")
            ls = os.listdir(ps_path)
            c_path = []
            for i in ls:
                c_path.append(os.path.join(ps_path, i))
            # 增强后图片路径
            psed_path = os.path.join(myfunctions.PWD, "xcc_ps/output")
            # ls1 = os.listdir(psed_path)
            c1_path = []
            for i in out_photo:
                c1_path.append(os.path.join(psed_path, i))

            # 展示得分结果
            with r11:
                for i in ls:
                    r11.write(i)
            with r12:
                for i in score_of_photo:
                    r12.write(i[0])
            with r13:
                for i in score_of_photo:
                    r13.write(i)
                r13.write(f'模型计算耗时{model_time}s,项目总耗时{run_time}s')

            # 原始输入图片
            with t11:
                for x in c_path:
                    t11.image(myfunctions.show_select_image(x), width=400)
                # st.write(ls)
            # 最佳图像
            with t12:
                for x in c1_path:
                    t12.image(myfunctions.show_select_image(x), width=400)
                # st.write(out_photo)
        else:
            placeholder_2 = st.empty()
            placeholder_2.error("您还未选择照片")
            time.sleep(1)
            placeholder_2.empty()
