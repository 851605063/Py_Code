
import re

import requests
from bs4 import BeautifulSoup
from threading import Thread

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}

proxies={"http":"http://114.99.3.109:3256"}
#定义获取IP函数
def get_ip():
   #写入txt
    write_ip = open('get_ip.txt', 'w')
    for page in range(1, 10):
        #url = 'http://www.xicidaili.com/nn/%s' % page
        url='https://www.kuaidaili.com/free/inha/%s/' % page
        r = requests.get(url, headers=headers,timeout=100,proxies=proxies)
        # 用beautifulsoup库解析网页
        # soup = BeautifulSoup(r.content,"html.parser")
        # #print(soup.prettify())
        # sty={"data-title":"IP"}
        # ips = soup.findall(attrs=sty)
        ips=re.findall('<td data-title="IP">(.*)</td>', r.text)
        ports = re.findall('<td data-title="PORT">(.*)</td>', r.text)
        for ip in ips:
            # tds = tr.find_all('td')
            # ip = tds[1].text.strip()
            # port = tds[2].text.strip()
            # write_ip.write('%s\n'%(ip+':'+port))
            #print(ip)
            write_ip.write('%s\n'%ip)
    write_ip.close()
    print('done')
    response = requests.get("http://httpbin.org/ip", proxies=proxies)
    print(response.text)
get_ip()