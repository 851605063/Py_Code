import os
import re
import time
import random
from collections import Counter

import requests
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 生成Session对象，用于保存Cookie
s = requests.Session()
# 词云形状图片
WC_MASK_IMG = 'Emile.jpg'
# 影评数据保存文件
COMMENTS_FILE_PATH = 'douban_comments.txt'
# 词云字体
WC_FONT_PATH = '/Library/Fonts/Songti.ttc'


def login_douban():
    """
    登录豆瓣
    :return:
    """
    # 登录URL
    login_url = 'https://accounts.douban.com/j/mobile/login/basic'
    # 请求头
    headers = {'user-agent': 'Mozilla/5.0', 'Referer': 'https://accounts.douban.com/passport/login?source=main'}
    # 传递用户名和密码
    data = {'name': '15888397035',
            'password': 'wjq636352653',
            'remember': 'false'}
    try:
        r = s.post(login_url, headers=headers, data=data)
        r.raise_for_status()
    except:
        print('登录请求失败')
        return 0
    # 打印请求结果
    print(r.text)
    return 1


def spider_comment(page=0):
    """
    爬取某页影评
    :param page: 分页参数
    :return:
    """
    print('开始爬取第%d页' % int(page))
    start = int(page * 20)
    Cookie='douban-fav-remind=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1625555291%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DCfNJ9V2d8zaJLMNZ32YjUbWwBVWfgdied-DuVirhcCkdh-m7MY5RmY9UO-l8ZWwL%26wd%3D%26eqid%3D8f78e0cb000bb03b0000000460e4015a%22%5D; _pk_id.100001.8cb4=b210a67f39936a98.1569829140.38.1625557892.1624350896.; __utma=30149280.470532256.1569829141.1625542307.1625555296.41; __utmz=30149280.1625555296.41.40.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; gr_user_id=858b2274-2653-46a4-8464-9a6c5fdf01a6; _vwo_uuid_v2=D030E68CB580A2B1FBBEF27E514BD7A21|8982bca35c956fcc535bd90abfceabe2; viewed="34865428_5353163_33461526"; __gads=ID=1e3b3ec5c73912d7-2289b0b887c40097:T=1604299094:S=ALNI_MZHD0JogZxDxdv2xGKmdb6G15xdhA; bid=koTU4W1Sp5M; __yadk_uid=8bovRq7hgYuzrJCllpzz8uNwVq9nTTB3; ll="118175"; __utmc=30149280; _pk_ses.100001.8cb4=*; __utmb=30149280.5.10.1625555296; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.24131; dbcl2="241318139:+AogeNJZK7o"; ck=I27W'
    Referer='https://movie.douban.com/subject/27110296/comments?start=240&limit=20&status=P&sort=new_score'
    comment_url = 'https://movie.douban.com/subject/27598254/comments?start=%d&limit=20&sort=new_score&status=P' % start
    print(comment_url)
    # 请求
    headers = {'user-agent': 'Mozilla/5.0','Cookie':Cookie}
    try:
        r = s.get(comment_url, headers=headers)
        r.raise_for_status()
    except:
        print('第%d页爬取请求失败' % page)
        return 0
    # 使用正则提取影评内容
    comments = re.findall('<span class="short">(.*)</span>', r.text)
    if not comments:
        return 0
    # 写入文件
    with open(COMMENTS_FILE_PATH, 'a+', encoding='utf-8') as file:
        file.writelines('\n'.join(comments))
    return 1


def batch_spider_comment():
    """
    批量爬取豆瓣影评
    :return:
    """
    # 写入数据前先清空之前的数据
    if os.path.exists(COMMENTS_FILE_PATH):
        os.remove(COMMENTS_FILE_PATH)
    page = 0
    while spider_comment(page):
        page += 1
        # 模拟用户浏览，设置一个爬虫间隔，防止ip被封
        time.sleep(random.random() * 3)
    print('爬取完毕')


def cut_word():
    """
    对数据分词
    :return: 分词后的数据
    """
    with open(COMMENTS_FILE_PATH,encoding='utf-8') as file:
        comment_txt = file.read()
        wordlist = jieba.lcut(comment_txt)
        # for  w in wordlist:
        #     if len(w)>1:
        #         wl = " ".join(w)
        #         print(w)
        c = Counter()
        for x in wordlist:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
        dict={}
        for (k,v) in c.most_common(100):
            print("%s:%d"%(k,v))
        wl = " ".join(wordlist)
        return wl


def create_word_cloud():
    """
    生成词云
    :return:
    """
    # 设置词云形状图片
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 数据清洗词列表
    stop_words = ['就是', '不是', '但是', '还是', '只是', '这样', '这个', '一个', '什么', '电影', '没有','的','了','习近平','总书记']
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", scale=1,
                   max_font_size=50, random_state=30, stopwords=stop_words, font_path="msyh.ttc",mode="RGBA")
    # 生成词云
    wc.generate(cut_word())

    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()


if __name__ == '__main__':
    # 登录成功才爬取
    # if login_douban():
    #spider_comment(11)
    #batch_spider_comment()
    create_word_cloud()
