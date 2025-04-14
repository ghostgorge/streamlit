import os
import copy
import streamlit as st
import pandas as pd
import plotly.express as px


def get_file_list(suffix, path):
    """获取指定路径下所有特定后缀文件的完整路径"""
    file_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(suffix):
                file_paths.append(os.path.join(root, file))
    return file_paths  # 直接返回完整路径列表


# 页面配置
st.set_page_config(layout="wide")
st.title("数据分析工具")

# 侧边栏设置
with st.sidebar:
    input_folder = st.text_input(
        "请输入文件夹路径：",
        value=os.path.abspath('.'),
        help="支持绝对路径和相对路径"
    )

    # 获取.xlsx文件列表（直接获取完整路径）
    file_list = get_file_list('.xlsx', input_folder)

    # 文件选择器
    if file_list:
        selected_file = st.selectbox(
            "选择分析文件：",
            file_list,
            format_func=lambda x: os.path.basename(x)  # 显示文件名
        )
    else:
        st.warning("该路径下没有Excel文件！")

# 主界面
if file_list and selected_file:
    # 数据加载（带缓存）
    @st.cache_data
    def load_data(file_path):
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.lower().str.strip()  # 标准化列名
        return df


    try:
        df = load_data(selected_file)
        st.success(f"成功加载文件：{os.path.basename(selected_file)}")

        # 数据处理
        if len(df.columns) > 1:
            # 创建列名副本
            cols = copy.deepcopy(df.columns.tolist())

            # 创建子数据集（排除第一列）
            sub_df = df.iloc[:, 1:]  # 直接使用iloc更高效

            # 可视化设置
            st.subheader("时序数据趋势")
            fig = px.line(
                sub_df,
                x=sub_df.index,
                y=sub_df.columns,
                labels={'value': '数值', 'variable': '指标'},
                height=600
            )

            # 优化图例显示
            fig.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            # 显示统计数据
            st.subheader("基础统计")
            st.dataframe(sub_df.describe(), use_container_width=True)

        else:
            st.warning("数据需要至少两列才能进行趋势分析")

    except Exception as e:
        st.error(f"文件读取失败：{str(e)}")

elif not file_list:
    st.info("请在上方输入有效文件夹路径")
