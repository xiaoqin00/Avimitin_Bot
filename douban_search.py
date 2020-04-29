# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/29
# 爬虫搜索豆瓣
import requests
from bs4 import BeautifulSoup
import json

with open('header.json', 'r+', encoding='UTF-8') as header_file:
    header_dic = json.load(header_file)

def tv_search(tv_name):
    r = requests.get('https://www.douban.com/search', params={'q': tv_name}, headers=header_dic)
    soup = BeautifulSoup(r.text, 'html5lib')
    result = soup.find(class_='title')
    name = result.h3.a.string
    tag = result.h3.span.string
    rating = result.find(class_='rating_nums').string
    details = result.find(class_='subject-cast').string
    link = result.h3.a['href']
    text = "豆瓣搜索结果：\n{}\b{}\n评分{}分\n{}".format(tag, name, rating, details)
    return text, link

if __name__ == '__main__':
    tv_search('joker')
