import json

import requests
from bs4 import BeautifulSoup
from django.core import serializers

from XiaoshuoWebAPI.modal import result

searchUrl = 'https://www.qu.la/book/'

req_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': '__cfduid=d577ccecf4016421b5e2375c5b446d74c1499765327; UM_distinctid=15d30fac6beb80-0bdcc291c89c17-9383666-13c680-15d30fac6bfa28; CNZZDATA1261736110=1277741675-1499763139-null%7C1499763139; tanwanhf_9821=1; Hm_lvt_5ee23c2731c7127c7ad800272fdd85ba=1499612614,1499672399,1499761334,1499765328; Hm_lpvt_5ee23c2731c7127c7ad800272fdd85ba=1499765328; tanwanpf_9817=1; bdshare_firstime=1499765328088',
    'Host': 'www.qu.la',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.qu.la/book/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}


def getBookInfo(request):
    code = request.GET.get("code")
    if code == '':
        return result.error(message='请传入name参数', data=None)
    req_url = searchUrl + code
    res = requests.get(req_url, params=req_header)
    soups = BeautifulSoup(res.text, "html.parser")
    data = {
        'info': None,
        'chapterList': [],
    }
    book = {
        'title': '',
        'author': '',
        'lastTime': '',
        'newChapter': '',
        'newChapterUrl': '',
        'image': '',
        'intro': ''
    }
    # 1.查找id为info的节点
    info = soups.find('div', id='info')
    # 标题
    title = info.h1.get_text()
    book['title'] = title
    ps = info.find_all('p')
    # 作者
    author = ps[0]
    authors = author.string.split('：')
    book['author'] = authors[1]
    # 最后更新
    lastTime = ps[2]
    lastTimes = lastTime.string.split('：')
    book['lastTime'] = lastTimes[1]
    # 最新章节
    newChapter = ps[3].a
    newChapterUrl = newChapter.get('href')
    book['newChapter'] = newChapter.string
    book['newChapterUrl'] = newChapterUrl
    # 图片
    fmimg = soups.find('div', id='fmimg')
    image = fmimg.img.get('src')
    book['image'] = image
    # 2.查找id为intro的节点
    intro = soups.find('div', id='intro').get_text()
    book['intro'] = intro
    print(book)
    # 3.查找所有的<dd>节点，然后去重
    dds = soups.find_all('dd')
    dds2 = []
    for dd in dds:
        if (dd not in dds2):
            dds2.append(dd)
    chapterList = []
    for dd in dds2:
        chapter = {
            'name': '',
            'url': ','
        }
        name = dd.a.get_text()
        url = dd.a.get('href')
        chapter['name'] = name
        chapter['url'] = url
        chapterList.append(chapter)
    print(chapterList)
    data['info'] = book
    data['chapterList'] = chapterList
    return result.success(data)
