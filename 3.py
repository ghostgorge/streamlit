import streamlit as st
import pandas as pd
from openai import OpenAI

# 页面基础配置
st.set_page_config(page_title="Excel智能分析平台", layout="wide")
st.title("📊 Excel数据分析 + DeepSeek AI集成")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None

# 侧边栏配置区域
with st.sidebar:
    st.header("🔑 配置中心")
    api_key = st.text_input("sk-3404675f1390407e9c623984aa98e47f", type="password", help="从DeepSeek官网获取API密钥")
    model_name = st.selectbox("选择模型版本", ["deepseek-chat", "deepseek-analysis"], index=0)
    temperature = st.slider("模型创造力", 0.0, 1.0, 0.7, step=0.1)

# 文件上传模块
uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx", "xls", "csv"],
                                 help="支持XLSX/XLS/CSV格式，文件大小不超过200MB")
if uploaded_file:
    try:
        # 读取数据并缓存
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df

        # 显示数据摘要
        with st.expander("📂 数据摘要（点击展开）", expanded=True):
            cols = st.columns(3)
            cols[0].metric("总行数", len(df))
            cols[1].metric("总列数", len(df.columns))
            cols[2].metric("缺失值总数", df.isnull().sum().sum())

            st.write("前5行数据预览：")
            st.dataframe(df.head(), use_container_width=True)

            # 自动生成数据统计信息
            if st.checkbox("显示详细统计"):
                st.write(df.describe(include='all'))
    except Exception as e:
        st.error(f"文件解析错误：{str(e)}")

# 分析对话模块
if st.session_state.df is not None and api_key:
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

    # 显示历史对话
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # 用户提问处理
    if prompt := st.chat_input("输入数据分析问题，例如'分析销售趋势'"):
        # 构建数据上下文
        data_context = f"""
        当前数据集摘要：
        - 维度：{len(st.session_state.df)}行 × {len(st.session_state.df.columns)}列
        - 列名：{', '.join(st.session_state.df.columns)}
        - 示例数据（前3行）：
        {st.session_state.df.head(3).to_markdown(index=False)}
        """

        # 组合完整提示词
        full_prompt = f"{data_context}\n\n用户问题：{prompt}"

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("🔍 正在分析中..."):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "你是一个专业的数据分析师，需要根据提供的数据集进行准确分析"},
                        {"role": "user", "content": full_prompt}],
                    temperature=temperature,
                    stream=False
                )
                answer = response.choices[0].message.content

                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.chat_message("assistant").markdown(answer)

            except Exception as e:
                st.error(f"API调用失败：{str(e)}")
else:
    st.info("👈 请先在侧边栏输入API密钥并上传数据文件")

# 添加帮助信息
with st.expander("💡 使用技巧"):
    st.markdown("""
    - **数据准备**：确保Excel文件第一行为列标题，数值列不含文本
    - **提问示例**：
        - "各月份的销售额趋势如何？"
        - "哪些产品的利润率低于平均水平？"
        - "生成数据质量报告"
    - **高级技巧**：使用Markdown语法提问可指定输出格式，例如：
""")
