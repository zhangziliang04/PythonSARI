from flask import Flask, render_template,jsonify
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Line
from pyecharts.globals import ChartType, SymbolType
from pyecharts.globals import ThemeType

from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import json

app = Flask(__name__, static_folder="templates",)


# 第一部分：图表创建
# 01.实时疫情地图
def map_base()->Map:
    # 数据暂时写死：后续可以结合实时数据，进行更新

    # 省和直辖市
    province_distribution = {'河南': 566, '北京': 212, '河北': 21, '辽宁': 12, '江西': 391, '上海': 203, '安徽': 408, '江苏': 271,
                             '湖南': 521, '浙江': 724, '海南': 2, '广东': 725, '湖北': 11177, '黑龙江': 121, '澳门': 1, '陕西': 128, '四川': 254,
                             '内蒙古': 3, '重庆': 312, '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 259, '福建': 179, '青海': 1,
                             '天津': 1, '其他': 1}
    provice = list(province_distribution.keys())
    values = list(province_distribution.values())

    c = (
        Map()
        .add("确诊人数", [list(z) for z in zip(provice,values)], "china")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国实时疫情分布地图"),
            visualmap_opts=opts.VisualMapOpts(max_= 1000),)
        )
    return c


# 02. 疫情新增趋势图
def conf_new_base() -> Line:
    # 静态数据
    dataY1 = [59, 77, 149, 131, 256, 444, 688, 769, 1771, 1459, 1737, 1982, 2102, 2590, 2829, 3235, 3887]
    dataY2 = [59, 27, 149, 131, 680,1118,1309, 3806, 2077, 3248, 4148, 4812, 5019, 4562, 5173, 5072, 3971]
    dataX = ['2020.01.18', '2020.01.19', '2020.01.20', '2020.01.21', '2020.01.22','2020.01.23','2020.01.24','2020.01.25',
             '2020.01.26', '2020.01.27', '2020.01.28', '2020.01.29', '2020.01.30','2020.01.31','2020.02.01','2020.02.02',
             '2020.02.03', '2020.02.04']
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(dataX)
        .add_yaxis("新增确诊", dataY1, is_smooth=True)
        .add_yaxis("新增疑似", dataY2, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情新增确诊/疑似趋势图"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


# 03. 全国累计确诊/疑似趋势图
def conf_total_base() -> Line:
    # 静态数据
    dataY1 = [291, 440, 571, 830, 1287, 1975, 2744, 4515, 5974, 7711, 9692, 11791, 14380, 17205, 20438, 24324]
    dataY2 = [54, 37, 393, 1072, 1965, 2684, 5794, 6973, 9239, 12167, 15238, 17988, 19544, 21558,23214, 23260]

    dataX = ['2020.01.20', '2020.01.21', '2020.01.22', '2020.01.23', '2020.01.24', '2020.01.25', '2020.01.26',
             '2020.01.27', '2020.01.28', '2020.01.29', '2020.01.30', '2020.01.31', '2020.02.01', '2020.02.02',
             '2020.02.03', '2020.02.04']
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(dataX)
        .add_yaxis("累计确诊", dataY1, is_smooth=True)
        .add_yaxis("累计疑似", dataY2, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情累计确诊/疑似趋势图"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


# 04. 全国累计死亡/治愈趋势图
def dead_total_base() -> Line:
    # 静态数据
    dataY1 = [0, 9,	17,	25,	41,	56,	80,	106, 132, 170, 213,	259, 304, 361, 425, 490]
    dataY2 = [0, 0, 0, 34, 38, 49,	51,	60,	103, 124, 171, 243, 328, 475, 632, 892]

    dataX = ['2020.01.20', '2020.01.21', '2020.01.22', '2020.01.23', '2020.01.24', '2020.01.25', '2020.01.26',
             '2020.01.27', '2020.01.28', '2020.01.29', '2020.01.30', '2020.01.31', '2020.02.01', '2020.02.02',
             '2020.02.03','2020.02.04']
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(dataX)
        .add_yaxis("累计死亡", dataY1, is_smooth=True)
        .add_yaxis("累计治愈", dataY2, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情累计死亡/治愈趋势图"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


# 05. 全国各省市数据明细
def table_base():
    table = Table()

    headers = ["地区", "确诊", "死亡", "治愈"]
    rows = [
        ["湖北", 13522, 414, 397],
        ["浙江", 829, 0, 60],
        ["广东", 813, 0, 24],
        ["河南", 675, 2, 20],
        ["湖南", 593, 0, 29],
        ["安徽", 480, 0, 20],
        ["江西", 476, 2, 19],
        ["重庆", 344, 2, 9]
    ]
    table.add(headers, rows).set_global_opts(
        title_opts=ComponentTitleOpts(title="Table", subtitle="副标题")
    )
    # table.render("table_base.html")
    return rows


# 第二部分：路由配置
@app.route("/")
def index():
    content = table_base()
    return render_template("index.html", content=content)


@app.route("/mapChart")
def get_map_chart():
    c = map_base()
    return c.dump_options_with_quotes()


@app.route("/confChart")
def get_conf_chart():
    c = conf_new_base()
    return c.dump_options_with_quotes()


@app.route("/confTotalChart")
def get_conf_total_chart():
    c = conf_total_base()
    return c.dump_options_with_quotes()


@app.route("/deadTotalChart")
def get_dead_total_chart():
    c = dead_total_base()
    return c.dump_options_with_quotes()


# 主函数
if __name__ == "__main__":
    app.run()
