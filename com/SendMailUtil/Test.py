import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import sleep


def Test():
    mail_user = "1766934021@qq.com"
    # mail_pass ="nqxurekkdfmhijef" #1126967702
    # mail_pass ="jjufnnwlpjyvbagc" #1126967702
    mail_pass = "ydhawpqfhcjdbhaa"  # 1766934021
    sender = 'bigdtechnology1@qq.com'  # 发送者邮箱
    receivers = '1144091761@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText('是13868983125', 'plain', 'utf-8')
    message['From'] = Header("13868983125",'utf-8')  # 发送者
    message['To'] = Header("13868983125", 'utf-8')  # 接收者

    subject = '威心是13868983125'
    message['Subject'] = Header(subject, 'utf-8')
    server=smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(mail_user, mail_pass)
    server.sendmail(sender, receivers,message.as_string())
    print("邮件发送成功");


if __name__ == "__main__":
    for i in range(1,100):
        Test()
        print(i)
