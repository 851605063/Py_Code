from com.SendMailUtil import SendMailUtil as SendMail
import requests

class ReadFileSendMail(object):

    # 读取文件返回一个列表
    @staticmethod
    def readfile(filepath):
        file = open(filepath, "r")
        # file = open("emails.txt", "r")

        lines = file.readlines()

        return lines

    # 参数为接收者列表
    @staticmethod
    def read_sendmail(title, content, name,emails,count):
        # for _ in range(len(emails)):
        #     emails[_] = emails[_].strip()  # 去掉每一行前后的换行符

        SendMail.SendMail.sendmail(title, content, name,emails,count)


# if __name__ == "__main__":
#     path = input("输入列表文件的路径")
#
#     ReadFileSendMail.read_sendmail("JND-群：36103909709，上分，送烟", "你好；JND-群：36103909709，上分，送烟只是测试若有打扰；请您包含",
#                               ReadFileSendMail.readfile(path))
