'''
Description: 
Author: Liu Heng
Date: 2022-04-22 23:44:03
LastEditors: Liu Heng
LastEditTime: 2022-04-24 09:01:58
'''
import time
import sys
import requests
from icecream import ic
from jsonpath import jsonpath

# 正则
import re

# 词云
import stylecloud
import csv
import pandas as pd
import numpy as np
from PIL import Image

def save(list):
    f = open('data/Comment.csv','a',encoding='utf-8-sig',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(list)
    f.close()

class ToDo():
    def __init__(self, username='nobody'):
        self.username = username

    #  爬取评论数据
    def CommentSearch(self):
        big_list = []
        # save(["昵称","性别","签名","回复数","点赞数","评论内容","等级","评论时间"])

        #  获取评论数据
        for i in range(20):
            print('爬取第{}个懒加载数据!'.format(i))
            time.sleep(0.2)

            #  包装请求头
            start_url = f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={i}&type=1&oid=626608698&mode=3&plat=1&_=1650726513443'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
                'referer': 'https://www.bilibili.com/video/BV1Zu411m72m?spm_id_from=333.999.0.0'
            }

            #  数据清洗
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

                #  写入评论数据
                save(item)
        print('写入成功')

    #  爬取弹幕数据
    def BarrageSearch(self):
        print('正在爬取ing')
        time.sleep(0.5)

        #  包装请求头
        start_url = f'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=250832329&pid=626608698&segment_index=2'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
            'referer': 'https://www.bilibili.com/video/BV1Zu411m72m?spm_id_from=333.999.0.0'
        }
        response = requests.get(start_url, headers = headers)

        #  数据清洗
        res = re.findall('.*?([\u4e00-\u9fa5]+).*',response.text)

        #  数据写入
        print('爬取成功，正在写入ing')
        f = open('data/Barrage.csv','a',encoding='utf-8-sig',newline='')
        csv_writer = csv.writer(f)
        # csv_writer.writerow(["弹幕内容"])
        csv_writer.writerow(res)
        f.close()
        print('写入成功')

    #  数据分析
    def Analyse(self):
        print('----------词云生成中------------')

class Menu():
    def __init__(self):
        self.thing = ToDo()
        self.choices = {
            "1": self.thing.CommentSearch,
            "2": self.thing.BarrageSearch,
            "3": self.thing.Analyse,
            "4": self.quit
        }

    def display_menu(self):
        print("""
操作菜单:
1. 爬取数据
2. 爬取弹幕
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