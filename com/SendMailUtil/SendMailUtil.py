#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 上面这两行是因为python在默认的情况下不支持源码中的中文编码，加上后会忽略中文编码
import datetime
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from time import sleep




class SendMail(object):
    # 静态方法不需要第一个参数self，可以直接类名调用
    @staticmethod
    def sendmail(title, content, name,users,count):
        # 申明第三方服务关键信息
        mail_user = "1766934021@qq.com"

        #mail_pass ="nqxurekkdfmhijef" #1126967702  bigdtechnology
        #mail_pass ="jjufnnwlpjyvbagc" #1126967702  bigdtechnology
        mail_pass ="ydhawpqfhcjdbhaa" #1766934021  bigdtechnology1
        #mail_pass ="kfpsutaztpbnebfh" #2426435027  bigdtechnology2
        sender = 'bigdtechnology1@qq.com'  # 发送者邮箱
        receivers = users  # 接收者邮箱(数组)
        if receivers =='730621428' or receivers=='1433587852' or receivers=='617814296' or receivers=='730752863' or receivers=='3450511198' or receivers=='3374698922' or receivers=='2391758511':
            return
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header('群管理-李赞', 'utf-8')
        message['To'] = Header(name, 'utf-8') # 这里可以不用设置
        subject = title
        message['Subject'] = Header(subject, 'utf-8')
        # 邮件正文内容
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        try:
            sleep(6) #休息4秒，短了可能会被限制（根据日志显示共7秒）
            server = smtplib.SMTP_SSL("smtp.qq.com")
            server.login(mail_user, mail_pass)
            server.sendmail(sender, receivers, message.as_string())
            print(count,'-发送成功',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),receivers)
        except smtplib.SMTPRecipientsRefused as e1:
            print('没邮箱')
            return True;
        except smtplib.SMTPAuthenticationError as e2:
            print('被限制了休息1分钟重新调，预计',(datetime.datetime.now()+datetime.timedelta(minutes=11)).strftime("%Y-%m-%d %H:%M:%S"),'恢复...',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            sleep(60)
            SendMail.sendmail(title, content, name,users,count)

