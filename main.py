'''
Description: 
Author: Liu Heng
Date: 2022-04-22 23:44:03
LastEditors: Liu Heng
LastEditTime: 2022-04-23 12:40:11
'''
import time
import sys
import requests
from icecream import ic
from jsonpath import jsonpath

# 词云
import stylecloud
from PIL import Image
import csv

def save(list):
    f = open('D:/Study/course/Python/NO8/format.csv','a',encoding='utf-8-sig',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(list)
    f.close()

class ToDo():
    def __init__(self, username='nobody'):
        self.username = username

    def search(self):
        big_list = []
        save(["昵称","性别","签名","回复数","点赞数","评论内容","等级","评论时间"])

        for i in range(10):
            print('爬取第{}个懒加载数据!'.format(i))
            time.sleep(0.5)

            start_url = f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={i}&type=1&oid=507855067&mode=3&plat=1&_=1650361573280'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
                'referer': 'https://www.bilibili.com/video/BV1Zu411m72m?spm_id_from=333.999.0.0'
            }
            response = requests.get(start_url, headers = headers).json()
            message_list = response['data']['replies']

            for message in message_list:
                item = []
                name = message['member']['uname']       # 昵称
                item.append(name)

                sex = message['member']['sex']          # 性别
                item.append(sex)

                sign = message['member']['sign']          # 签名
                item.append(sign)

                rcount = message['rcount']                # 回复数
                item.append(rcount)

                like = message['like']                    # 点赞数
                item.append(like)
                
                content = message['content']['message']      # 评论内容
                item.append(content)
                
                level = message['member']['level_info']['current_level']      # 等级
                item.append(level)

                t = message['ctime']
                timeArray = time.localtime(t)
                otherStyleTime = time.strftime("%Y%m%d", timeArray)   # 评论时间
                item.append(otherStyleTime)

                save(item)


    def clean_dir1(self):
        print("选项二!")

    def clean_dir2(self):
        print("选项三!")


class Menu():
    def __init__(self):
        self.thing = ToDo()
        self.choices = {
            "1": self.thing.search,
            "2": self.thing.clean_dir1,
            "3": self.thing.clean_dir2,
            "4": self.quit
        }

    def display_menu(self):
        print("""
操作菜单:
1. 爬取数据
2. 选项二
3. 选项三
4. 退出
""")

    def run(self):
        while True:
            self.display_menu()
            try:
                choice = input("键入选项: ")
            except Exception as e:
                print("输入无效!");continue

            choice = str(choice).strip()
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} 不是有效选择".format(choice))

    def quit(self):
        print("\n感谢使用!\n")
        sys.exit(0)


if __name__ == '__main__':
    Menu().run()