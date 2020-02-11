import requests
import time
import json
import csv
import random


"""
本文原创：pk哥
公众号：Python知识圈（id：PythonCircle）
「Python知识圈」公众号定时分享大量有趣有料的 Python 爬虫和实战项目，值得你的关注。
关注后回复1024免费领取学习资料！
"""


class mp_spider(object):
    def __init__(self):
        self.offset = 0
        # 记得把offset后面的值改成{}
        self.base_url = 'http://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA3Nzc4MzY2NA==&f=json&offset={}&count=10'
        # 下面的值以自己的为准，部分省略了
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) Appl'
                                     'eWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/2.'
                                     '3.24(0x12031811) MacWechat Chrome/39.0.2171.95 Safari/'
                                     '537.36 NetType/WIFI WindowsWechat MicroMessenger/2.3.2'
                                     '4(0x12031811) MacWechat Chrome/39.0.2171.95 Safari/537'
                                     '.36 NetType/WIFI WindowsWechat',
                        'Cookie': 'devicetype=iPhoneiOS13.3; lang=zh_CN; pass_ticket=xxxx; version=17000a2c; wap_sid2=xxx++f3xBTgNQJVO; wxuin=1310962901',
                        'Referer':'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA3Nzc4MzY2NA==&scene=124&uin=xxx'}
        self.proxy = {'https': '124.152.32.140:53281'}  # 124.152.32.140:53281  183.129.207.91:11056

    def request_data(self):
        try:
            response = requests.get(self.base_url.format(self.offset), headers=self.headers, proxies=self.proxy)
            print(self.base_url.format(self.offset))
            if 200 == response.status_code:
               self.parse_data(response.text)
        except Exception as e:
            print(e)
            time.sleep(2)
            pass

    def parse_data(self, responseData):
            all_datas = json.loads(responseData)

            if 0 == all_datas['ret'] and all_datas['msg_count']>0:
                summy_datas = all_datas['general_msg_list']
                datas = json.loads(summy_datas)['list']
                a = []
                for data in datas:
                    try:
                        title = data['app_msg_ext_info']['title']
                        title_child = data['app_msg_ext_info']['digest']
                        article_url = data['app_msg_ext_info']['content_url']
                        md_url = '[{}]'.format(title) + '({})'.format(article_url)
                        info = {}
                        info['标题'] = title
                        info['小标题'] = title_child
                        info['文章链接'] = article_url
                        info['md链接'] = md_url
                        a.append(info)
                    except Exception as e:
                        print(e)
                        continue

                print('正在写入文件')
                with open('Python公众号文章合集2.csv', 'a', newline='', encoding='utf-8') as f:
                    fieldnames = ['标题', '小标题', '文章链接', 'md链接']  # 控制列的顺序
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(a)
                    print("写入成功")

                print('----------------------------------------')
                time.sleep(int(format(random.randint(2, 5))))
                self.offset = self.offset+10
                self.request_data()
            else:
                print('抓取数据完毕！')


if __name__ == '__main__':
    d = mp_spider()
    d.request_data()
