from bs4 import BeautifulSoup
import requests
import re
from XiaoshuoWebAPI.modal import result

searchUrl = 'https://sou.xanbhx.com/search?siteid=qula&q='

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


def searchBoook(request):
    name = request.GET.get("name")
    if name == '':
        return result.error(message='请传入name参数', data=None)
    req_url = searchUrl + name
    res = requests.get(req_url, params=req_header)
    soups = BeautifulSoup(res.text, "html.parser")
    # 查找第一个ul节点
    ul = soups.find('ul')
    # 查找所有li节点
    lis = ul.find_all('li')
    # 删除第一行数据
    del lis[0]
    books = []
    # 遍历li标签，每一个li就是每一本书
    for li in lis:
        # 定义返回书的结构
        book = {
            'type': '',
            'name': '',
            'code': '',
            'chapter': '',
            'chapterCode': '',
            'author': '',
            'click': '',
            'time': '',
            'status': ''
        }
        spans = li.find_all('span')
        type_s = spans[0].string
        # 删除两边的[]
        book['type'] = type_s.strip().strip('[]')
        name_s = spans[1].a.string
        # 去除字符串中的\n\r\t
        name_s_re = re.sub('[\r\n\t]', '', name_s)
        # 去除前面的空格
        book['name'] = name_s_re.lstrip()
        url = spans[1].a.get('href')
        # 分割字符串
        url_s = url.split("/")
        # print(url_s)
        # 取分割后的第5个即为书号
        book['code'] = url_s[4]
        book['chapter'] = spans[2].a.string
        spans[2].a.get('href')
        chapter_url = spans[2].a.get('href')
        chapter_url_s = chapter_url.split('/')
        # print(chapter_url_s)
        # 去除章节号后面的.html
        book['chapterCode'] = chapter_url_s[5].rstrip().rstrip('.html')
        book['author'] = spans[3].string
        book['click'] = spans[4].string
        book['time'] = spans[5].string
        book['status'] = spans[6].string
        books.append(book)
    return result.success(books)
