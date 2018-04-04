'''
create on: 2018/4/3
author:落空
此项目为爬取百思不得姐官网的内容
获取内容：1、发布者昵称
          2、发布时间
          3、发布的内容
          4、发布的图片
'''
from Spider import Spider

'''爬虫入口'''
class Main():

    @staticmethod
    def start_spider():
        page_number = input('请输入你要爬取的页数（页数越多爬取速度越慢）：')
        bsbdj=Spider()
        bsbdj.crawler_data(page_number)
        print('数据爬取完成。')

if __name__ == '__main__':
    Main().start_spider()

