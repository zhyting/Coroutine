#!/usr/bin/env python
# encoding: utf-8

"""
    version 0.0
"""
from urllib import request
from lxml import etree

"""
    1 第一页的电影
    2 第一页所包含的链接 
"""
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

def fetch_page(url):
    response = request.Request(url, headers=headers)
    html = request.urlopen(response).read().decode('utf-8')
    return html


def crow():
    url = 'https://movie.douban.com/top250'

    """
        从第一页中解析出link (因为一张页面是无法显示完250部电影的，它是分页显示的)
    """
    html = fetch_page(url)
    html = etree.HTML(html)
    xpath_pages = '//*[@class="paginator"]/a'
    pages = []
    for link in html.xpath(xpath_pages):
        pages.append(url+link.get('href'))

    """
        爬取每一页的数据
    """
    for url in pages:
        html = fetch_page(url)
        html = etree.HTML(html)
        datas = html.xpath('//ol[@class="grid_view"]/li')

        for data in datas:
            data_title = data.xpath('div/div[2]/div[@class="hd"]/a/span[1]/text()')
            print(data_title)


def parse_page():
    url = 'https://movie.douban.com/top250?start='
    html = fetch_page(url)
    html = etree.HTML(html)
    xpath_pages = '//*[@class="paginator"]/a'
    pages = []
    for link in html.xpath(xpath_pages):
        pages.append(link)
    for ele in pages:
        print(ele.get('href'))

def main():
    crow()


if __name__ == "__main__":
    main()




