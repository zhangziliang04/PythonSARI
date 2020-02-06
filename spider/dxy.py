from requests_html import HTMLSession
import random
import csv
import json
import datetime

session = HTMLSession()
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def getTime():
    curtime = datetime.datetime.now()
    strtime = curtime.strftime('_%Y_%m_%d_%H_%M_%S')
    return strtime


class DxySARI(object):
    def __init__(self):
        self.start = 0
        # self.headers = {'User-Agent': 'Mozilla/5.0(Windows NT 6.1; WOW64)'}
        self.headers = {"User-Agent": random.choice(USER_AGENTS)}
        self.dxyurl = 'https://3g.dxy.cn/newh5/view/pneumonia'
        self.items = []
        self.province_list = []
        self.city_list = []
        self.city_csv = '../data/city.csv'
        self.province_csv = '../data/province'

    # 页面数据 + 目标字符串
    def get_html_page(self):
        response = session.get(self.dxyurl)
        page = response.html.html
        # print(page)
        start = page.find("window.getAreaStat = [")
        # print(start)
        temp = page[start+22:]
        end = temp.find("]}catch(e){}")
        temp = temp[0:end]
        items = temp.split("]},")
        # 最后一个元素，特殊处理（尾部没有“，”号）
        last = items[-1]
        items.pop()
        newitems = []
        for item in items:
            item = item + "]}"
            newitems.append(item)
            # print(item)
        newitems.append(last)

        self.items = newitems
        return newitems

    # 数据结构化
    def get_detail_info(self,items):
        # 格式转换:字符串->JSON
        for item in items:
            js = json.loads(item)
            # print(js)
        # 格式转换:JSON->字典
            dc = {}
            dc = dict(js)
            # 省份数据（含城市）
            self.province_list.append(dc)
            # 城市数据（前缀增加省份）
            # print(self.province_list)
            cities = dc["cities"]
            # 需要增加判断，处理列表为空的情况（直辖市和特区的问题）
            if cities:
                for city in cities:
                    city["provinceName"] = dc["provinceName"]
                    self.city_list.append(city)
                    # print(city.keys())
        # 保存至文件
        # print(self.province_list)
        # print(self.city_list)

    # 省份数据写入CSV：城市数据作为整体存储，不使用
    def write_province_csv(self):
        filename = self.province_csv + getTime() + '.csv'
        # print(filename)
        header = ['provinceName', 'provinceShortName', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount', 'comment','cities']
        with open(filename, 'w', newline='',encoding='utf-8-sig') as csvfile:
            file_pro = csv.writer(csvfile)
            file_pro.writerow(header)
            try:
                for item in self.province_list:
                    print(item.values())
                    file_pro.writerow(item.values())
            except Exception as e:
                print('Province数据写入异常' + e + '异常')

    # 城市数据写入CSV
    def write_city_csv(self):
        filename = self.city_csv + getTime() + '.csv'
        print(filename)
        header = [['cityName', 'confirmedCount', 'suspectedCount', 'curedCount', 'deadCount', 'provinceName']]
        with open(filename, 'w', newline='',encoding='utf-8-sig') as csvfile:
            file_city = csv.writer(csvfile)
            file_city.writerow(header)
            try:
                for item in self.city_list:
                    print(item.values())
                    file_city.writerow(item.values())
            except Exception as e:
                print('City数据写入异常' + e + '异常')


# 主函数
if __name__ == '__main__':
    dxy = DxySARI()
    page = dxy.get_html_page()
    dxy.get_detail_info(page)
    #dxy.write_province_csv()
    #dxy.write_city_csv()


