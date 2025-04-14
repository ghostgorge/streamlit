import pandas as pd
import numpy as np


# 生成演示数据
def generate_demo_data(rows=30):
    """生成包含时序特征和多指标的测试数据"""
    np.random.seed(42)

    # 基础日期范围
    dates = pd.date_range(start="2023-01-01", periods=rows)

    # 生成测试指标
    data = {
        "date": dates,
        "product_a": np.round(np.linspace(100, 500, rows) + np.random.normal(0, 20, rows), 2),
        "product_b": np.round(np.linspace(200, 300, rows) + np.random.normal(0, 15, rows), 2),
        "product_c": np.round(np.linspace(150, 450, rows) * np.random.uniform(0.9, 1.1, rows), 2),
        "temperature": np.round(np.sin(np.linspace(0, 4 * np.pi, rows)) * 15 + 25, 1),
    }

    df = pd.DataFrame(data)

    # 添加辅助列
    df.insert(0, "id", range(1, len(df) + 1))
    df["weekday"] = df.date.dt.day_name()

    return df


# 生成并保存文件
if __name__ == "__main__":
    demo_df = generate_demo_data()

    # 保存为Excel文件（与Streamlit代码同目录）
    save_path = "demo_data.xlsx"
    demo_df.to_excel(save_path, index=False, sheet_name="SalesData")

    print(f"演示文件已生成：{save_path}")
    print("文件结构预览：")
    print(demo_df.head())
