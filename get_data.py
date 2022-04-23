'''
Description: 
Author: Liu Heng
Date: 2022-04-19 14:45:44
LastEditors: Liu Heng
LastEditTime: 2022-04-23 16:12:31
'''
import requests
from icecream import ic
from jsonpath import jsonpath
# 词云
import stylecloud
from PIL import Image

def main():
    big_list = []
    for i in range(10):
        #  获取数据
        print('爬取懒加载第{}的数据!'.format(i))
        start_url = f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={i}&type=1&oid=507855067&mode=3&plat=1&_=1650361573280'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
            'referer': 'https://www.bilibili.com/video/BV1Zu411m72m?spm_id_from=333.999.0.0'
        }
        response = requests.get(start_url, headers = headers).json(

        #  清洗数据
        replies = jsonpath(response,'$..replies')[0]
        message_list = jsonpath(replies,'$..message')

        
        for message in message_list:
            big_list.append(message)
        # ic(big_list)
    parse_img(big_list)

if __name__ == '__main__':
    main()
