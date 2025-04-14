import os
import copy
import streamlit as st
import pandas as pd
import plotly.express as px

def get_file_list(suffix, path):
    imput_template_all = []
    imput_template_all_path = []
    for root, dirs, files in os.walk(path,topdown=False):
        for name in files:
            if os.path.splitext(name)[1] == suffix:
                imput_template_all.append(name)
                imput_template_all_path.append(os.path.join(root, name))
    return imput_template_all, imput_template_all_path

st.set_page_config(layout="wide")
st.title("数据分析")
imput_folder = st.sidebar.text_input("请在这里输入文件夹路径：",value=os.path.abspath('.'),key=None)
path = imput_folder
_, file_list_xlsx = get_file_list('.xlsx', path)
file_list = file_list_xlsx
if file_list:
    select_file = st.sidebar.selectbox(
    '选择需要加载的文件：',
    file_list
)
    st.write("文件加载成功！文件是",select_file)
    #提取数据
    @st.cache_data
    def load_data(path):
        df_ = pd.read_excel(path)
        df_.columns = df_.columns.str.lower()
        return df_
    df = load_data(select_file)
    col_list = df.columns
    #显示数据
    col_list = col_list.tolist()
    #绘制数据
    col_list_bak = copy.deepcopy(col_list)
    if len(col_list) > 1:
        sub_df = df[col_list_bak]
        sub_df = sub_df.drop(df.columns[0], axis=1)
        col_list_bak.pop(0)
        fig = px.line(sub_df, x=sub_df.index, y=col_list_bak)
        fig.update_layout(legend=dict(
            orientation="h",
        ))
        st.plotly_chart(fig,theme='plotly_white')
else:
        st.write("请选择需要加载的文件！")

