import os
from typing import Iterable

import scrapy
from scrapy import Request
# 导入response响应对象的类型
from scrapy.http import HtmlResponse, JsonRequest


class WinshangdataSpider(scrapy.Spider):
    # 爬虫名
    name = "winshangdata"
    # 允许爬取的域名
    allowed_domains = ["winshangdata.com"]
    # 请求头
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Authorization": "",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://www.winshangdata.com",
        "Pragma": "no-cache",
        "Referer": "http://www.winshangdata.com/brandList",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "appType": "bigdata",
        "platform": "pc",
        "token": "",
        "uid": "",
        "uuid": "123456"
    }
    # 获取品牌店的接口
    url = 'http://www.winshangdata.com/wsapi/brand/getBigdataList3_4'

    def start_requests(self) -> Iterable[Request]:
        # 请求1-82页的内容
        for page in range(1, 2):
            # 构造载荷
            param = {
                "isHaveLink": "",
                "isTuozhan": "",
                "isXxPp": "",
                "kdfs": "",
                "key": "",
                "orderBy": "1",
                "pageNum": page,
                "pageSize": 60,
                "pid": "",
                "qy_p": "",
                "qy_r": "",
                "xqMj": "",
                "ytlb1": "",
                "ytlb2": ""
            }
            # 发送Json请求
            yield JsonRequest(url=self.url, headers=self.headers, data=param, callback=self.parse, dont_filter=False)

    def parse(self, response: HtmlResponse, **kwargs):
        # 获取响应体的Json内容
        resp = response.json()
        # 解析品牌店列表
        for item in resp['data']['list']:
            # 获取brandId值并拼接详情页的url
            detail_url = f'http://www.winshangdata.com/brandDetail?brandId={item["brandId"]}'
            # 发送get请求
            yield Request(url=detail_url, headers=self.headers, callback=self.detail_parse)

    def detail_parse(self, response: HtmlResponse, **kwargs):
        # 获取li标签的列表
        li_list = response.xpath('//ul[@class="detail-option border-b"]/li')
        temp = dict()
        # 遍历每一个列表并提取所需字段
        for li in li_list:
            key = li.xpath('./span[1]/text()').extract_first().strip().replace('：', '')
            val = li.xpath('./span[2]/text()').extract_first().strip()
            # print({key: val})
            if key == '创立时间' or key == '开店方式' or key == '合作期限' or key == '面积要求':
                temp.update({key: val})
        yield temp


if __name__ == '__main__':
    os.system('scrapy crawl winshangdata --nolog')
