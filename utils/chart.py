# 导入Altair库，这是一个用于创建声明式统计图表的Python库
import altair as alt

# 定义一个函数get_chart，它接受一个数据集作为参数
def get_chart(data):
    # 创建一个鼠标悬停选择器，用于交互式图表中高亮显示特定数据点
    hover = alt.selection_single(
        fields=["交易日期"],  # 指定选择器工作在'交易日期'字段上
        nearest=True,    # 当鼠标悬停在最近的点上时触发选择器
        on="mouseover",   # 鼠标悬停时触发选择器
        empty="none",     # 如果没有悬停的数据点，则不显示任何内容
    )

    # 创建一个基础的折线图，用于展示数据
    lines = (
        alt.Chart(data)  # 创建图表，设置标题
        .mark_line()  # 使用线条标记来绘制折线图
        .encode(
            x="交易日期",  # 指定x轴的字段为日期
            y="交易量", # 指定y轴的字段为交易量
            color="类别",
            strokeDash="类别"
        )
    )

    # 在折线图上添加可交互的点，并在悬停时高亮显示
    points = lines.transform_filter(hover).mark_circle(size=65)  # 使用筛选后的点绘制圆形标记

    # 创建一个辅助线图表，用于在悬停时显示当前点的准确位置和值
    tooltips = (
        alt.Chart(data)
        .mark_rule()  # 使用标记规则来绘制垂直线
        .encode(
            x="交易日期", 
            y="交易量",  
            # 根据悬停选择器的条件设置透明度，未悬停时透明度为0
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            # 设置工具提示，显示日期和价格信息
            tooltip=[
                alt.Tooltip("交易日期", title="日期"),
                alt.Tooltip("类别", title="类别"),
                alt.Tooltip("交易量", title="交易量")
            ],
        )
        .add_selection(hover)  # 将悬停选择器添加到辅助线图表中
    )

    # 将折线图、点和辅助线合并为一个交互式图表，并返回
    return (lines + points + tooltips).interactive()
