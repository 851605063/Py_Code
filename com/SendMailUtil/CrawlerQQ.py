import csv
import time
from lxml import html
from selenium import webdriver
from com.SendMailUtil import ReadFileSendMail as SendMail
etree = html.etree
#332793905

def parser():
    driver = webdriver.Chrome("chromedriver.exe")
    return driver


def login(url):
    driver = parser()
    driver.get(url)
    time.sleep(5)
    get_data(driver)
    return driver


def get_data(driver):
    for _ in range(50): # 可根据群成员的数量大小调整此数值，数值越大耗时越长
        scroller(driver)
        time.sleep(1)
    data = driver.page_source
    html = etree.HTML(data)
    mem_info_list = html.xpath('//*[@id="groupMember"]/tbody[@class="list"]/tr')  # TODO  QQ群成员列表
    with open('QQ.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect="excel")
        writer.writerow(['成员', 'QQ号', '性别', 'Q龄', '入群时间', '最后发言'])
        count=0
        for mem_info in mem_info_list:
            count=count+1
            data = {'成员': str(mem_info.xpath('./td[3]//text()')[3]).replace('\U0001f60a', '').strip(),
                    'QQ号': str(mem_info.xpath('./td[5]//text()')[0]).replace('\U0001f60a', '').strip(),
                    '性别': str(mem_info.xpath('./td[6]//text()')[0]).replace('\U0001f60a', '').strip(),
                    'Q龄': str(mem_info.xpath('./td[7]//text()')[0]).replace('\U0001f60a', '').strip(),
                    '入群时间': str(mem_info.xpath('./td[8]//text()')[0]).replace('\U0001f60a', '').strip(),
                    '最后发言': str(mem_info.xpath('./td[9]//text()')[0]).replace('\U0001f60a', '').strip()}
            if data:
                # writer.writerow(['成员', 'QQ号', '性别', 'Q龄', '入群时间', '最后发言'])
                # writer.writerow(
                #     [data['成员'].replace('\xa0', ''), data['QQ号'].replace('\xa0', ''),
                #      data['性别'].replace('\xa0', ''), data['Q龄'].replace('\xa0', ''),
                #      data['入群时间'].replace('\xa0', ''), data['最后发言'].replace('\xa0', '')])
                writer.writerow(
                    [data['成员'], data['QQ号'],
                     data['性别'], data['Q龄'],
                     data['入群时间'], data['最后发言']])
                # 发送邮件
                sendmail(data['成员'],data['QQ号'] + "@qq.com",count)
def sendmail(name,user,count):
    main='缺客户？缺人脉 ? 产品没销量？没推广渠道我们通通帮你解决！360行不管任何行业，可以帮你采集到全国各地各行业公司，工厂，企业，批发商，经销商，代理，个体实体商户老板电话号码，包括电商淘宝，阿里等信息，另有淘宝，京东，拼多多等买过任何商品人员的号码,一键提取。，每天可以让几百万人看到你的广告信息，增加知名度曝光率，让客户主动合作。详细了解'
    SendMail.ReadFileSendMail.read_sendmail("好久没见你了，最近忙啥呢", main,name,user,count)
def logout(driver):
    driver.find_element_by_class_name("logout").click()
    # driver.close()需要在driver.quit()前面，因为driver.quit()方法会先关闭所有窗口并退出驱动，如果再次调用close则会报错
    driver.close()
    driver.quit()


def scroller(driver):
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)


def run():
    count=0
    QQnum = '378345147' #input('请输入一个【一个或多个QQ群号】:')
    for num in QQnum.split(','):
        url = "https://qun.qq.com/member.html#gid=" + num
        driver = login(url)

    #logout(driver)  # TODO  退出登录


if __name__ == '__main__':
    run()
