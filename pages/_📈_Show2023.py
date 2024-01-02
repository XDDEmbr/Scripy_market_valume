import pandas as pd
import streamlit as st

# 设置应用程序为宽屏模式
st.set_page_config(layout="wide")

st.title('_2023_ 年度:blue[股基]市场交易量数据（单位：/万元）:sunglasses:')
st.header('', divider='rainbow')
# 读取Excel文件
df = pd.read_excel(r'2023年度市场交易量.xlsx')

# 将日期列转换为日期时间格式并截断时间部分
df['交易日期'] = pd.to_datetime(df['交易日期']).dt.date

st.checkbox("Use container width", value=True, key="use_container_width")

# 在Streamlit应用程序中展示数据
st.dataframe(df,use_container_width=st.session_state.use_container_width)
  
st.write("\n\n\n")
st.subheader('截至目前2023年度每个月的交易量涨幅情况')

df['交易日期'] = pd.to_datetime(df['交易日期'])
df = df.set_index('交易日期')
monthly_volume = df.resample('M')['合计'].sum().sort_index()

# 计算每个月份的涨幅，并将其转换为百分比格式
monthly_pct_change = monthly_volume.pct_change().fillna(0) * 100

# 将 monthly_volume 拆分成每四个月一组的数据块
chunks = [monthly_volume[i:i+4] for i in range(0, len(monthly_volume), 4)]
pct_chunks = [monthly_pct_change[i:i+4] for i in range(0, len(monthly_pct_change), 4)]

# 每个数据块展示在同一行
for chunk, pct_chunk in zip(chunks, pct_chunks):
    cols = st.columns(4)
    for i, vol in chunk.items():
        col_idx = i.month % 4 - 1
        if col_idx == -1:
            col_idx = 3
        coli = cols[col_idx]
        pct_change = pct_chunk[i]
        coli.metric(f"{i.month}月交易量", f"{vol:.2f}", f"{pct_change:.2f}%")

st.write("\n\n\n")
st.subheader('2023年度每日股基交易量变动情况')
# 展示每天的市场交易量数据
st.line_chart(df['合计'])
