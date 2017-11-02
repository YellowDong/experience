#!/usr/bin/env python3.6
#  _*_coding:utf8_*_

import requests
from urllib3.exceptions import ConnectionError
from bs4 import BeautifulSoup
from lxml import etree
import jieba
import sys
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
from PIL import Image
import numpy as np

jieba.load_userdict("dictNew.txt")


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.text
    except ConnectionError:
        print('connection error')


def get_title(html):
    titlelist = ''
    if html:
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find_all('table', attrs={'class': '12v'})
        for i in title:
            titlelist += i.a.text.strip()
        return titlelist


def get_link(html):
    if html:
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all('table', attrs={'class': '12v'})
        for i in links:
            link = i.a['href'].strip()
            yield link


def get_detail(html):
    if html:
        doc = etree.HTML(html)
        plist = doc.xpath('//div[@class="left_zw"]/p/text()')
        return plist


def main(keword, page):
    allcontent = ''
    for page in range(page):
        url = 'http://channel.chinanews.com/cns/cl/fortune-lccp.shtml?pager={0}'.format(page)
        html = get_html(url)
        if keword == 'title':
            data = get_title(html)
            allcontent += data
        else:
            link = get_link(html)
            for i in link:
                html = requests.get(i).content
                allcontent = ''.join(get_detail(html))
    datalist = jieba.cut(allcontent, cut_all=False)
    haha = " ".join(datalist)
    font = os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf") #wget http://labfile.oss.aliyuncs.com/courses/756/DroidSansFallbackFull.ttf下载中文词库
    png_font = np.array(Image.open(os.path.join(os.path.dirname(__file__), "love.png")))
    wc = WordCloud(font_path=font,
                   background_color="black", max_words=400, mask=png_font,
                   max_font_size=60, random_state=30)

    my_wordcloud=wc.generate(haha)
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    keyword, page = str(sys.argv[1]), int(sys.argv[2])
    main(keyword, page)
