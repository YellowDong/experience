#!/usr/bin/env python3
#  _*_coding:utf8_*_

import requests
from urllib3.exceptions import ConnectionError
from bs4 import BeautifulSoup
from lxml import etree
import jieba
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os



def get_html(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
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



def main():
    alltitle = ''
    for page in range(11):
        url = 'http://channel.chinanews.com/cns/cl/fortune-lccp.shtml?pager={0}'.format(page)
        html = get_html(url)
        data = get_title(html)
        alltitle += data
    datalist = jieba.cut(alltitle)
    haha = " ".join(datalist)
    print(haha)
    font = '/usr/share/fonts/'
    wc = WordCloud(font_path=font,
                   background_color="white", max_words=300,
                   max_font_size=40, random_state=42)

    my_wordcloud=wc.generate(haha)
    #my_wordcloud = WordCloud().generate(haha)
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

    dic = {}
    for ele in datalist:
        if ele not in dic:
            dic[ele] = 1
        else:
            dic[ele] = dic[ele] + 1
    sorted_word = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)

    line = ''
    for ele in sorted_word:
        if (len(ele[0]) > 1):  # 只顯示一個字以上的詞，如需顯示一個字的詞請註解掉此行
            line += ele[0] + ' ' + str(ele[1]) + '\n'
    print(line)


if __name__ == '__main__':
    main()
