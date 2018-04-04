from bs4 import BeautifulSoup
from urllib import request
import xlwt
from time import sleep
import requests
import os
import re

class Spider():
    '''
    百思不得姐的网页爬取类
    '''
    def __init__(self):
        self.count = 0;
        self.data = []

    def crawler_data(self,page_number):
        '''
        爬取需要的信息
        :param page_number: 爬取的页数
        :return:
        '''
        for i in range(0,int(page_number)):
            url = 'http://www.budejie.com/pic/{}'.format(i)
            self.__html_download(url)
            sleep(2)
        if self.count >0:
            print('开始下载数据...')
            self.__image_download(self.data)
            print('图片已下载完成...')
            self.__write_to_excel(self.data)
            print('数据已保存至excel表中...')

    def __html_download(self,page_url):
        '''
        下载网页
        :param url:
        :return:
        '''
        #print('开始下载网页...')
        try:
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }
            response = requests.get(page_url,headers=headers)
            response.encoding = 'UTF-8'
            if response.status_code !=200:
                return
            self.__parse_data(response.text)

        except Exception as e:
            print('\n\n下载网页出现错误，错误信息是:{}\n\n'.format(e.message))

    def __parse_data(self,text):
        '''
        使用bs4来解析网页，获取字段信息。
        :param htmls:
        :return:
        '''
        #print('开始解析网页...')
        try:
            soup = BeautifulSoup(text,'html.parser')
            #问题：select会找到一些无用的标签，不知道什么原因。
            results = soup.select('div.j-r-c div.j-r-list ul li')
            for result in results:
                data_list =[]
                author = result.select('div.u-txt a')
                date = result.select('div.u-txt span.u-time')
                describe = result.select('div.j-r-list-c-desc a')
                img_url = result.select('div.j-r-list-c div.j-r-list-c-img a img')

                author = author[0].text if len(author) > 0 else ''
                date = date[0].text if len(date) > 0 else ''
                describe = describe[0].text if len(describe)>0 else ''
                img_url = img_url[0].attrs['data-original'] if len(img_url) > 0 else ''

                #判断匹配的内容是不是为空
                if author !='' and img_url != '':
                    data_list.append(author)
                    data_list.append(date)
                    data_list.append(describe)
                    data_list.append(img_url)
                    self.data.append(data_list)
                    self.count = self.count + 1
        except Exception as e:
            print('\n\n解析网页有误，错误信息为：{}'.format(e.meaasge))

    def __image_download(self,data_list):
        '''
        下载图像数据，并将图像数据按照日期进行分类。
        :param data_list:
        :return:
        '''
        date_pattern = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        count = 0
        for data in data_list:
            count = count +1
            #self.now_step += 1
            #解析日期，以天为单位创建文件夹
            folder_name = re.findall(date_pattern,data[1])[0]
            path = 'BSBDJ\%s'%(folder_name)
            if os.path.exists(path) == False:
                os.makedirs(path)
            try:
                name=data[3].split('/')[-1]
                request.urlretrieve(data[3],path+'\\'+name)
            except Exception as e:
                print('图像%s下载失败，错误信息为%s'%(data[3],e.message))
            if count % 10 == 0:
                percent = count*100.0/self.count
                percent = round(percent,2)
                print('下载图像已完成{}%'.format(percent))
                sleep(0.5)

    def __write_to_excel(self,data_list):
        '''
        将数据写入excel表格中
        :param data_list:
        :return:
        '''
        try:
            book = xlwt.Workbook(encoding='utf-8',style_compression=0)
            sheet = book.add_sheet('百思不得姐',cell_overwrite_ok=True)
            title = ['作者','时间','描述','图片网址']
            for i in range(len(title)):
                sheet.write(0,i,title[i])
            for i in range(1,len(data_list)):
                for j in range(0,len(title)):
                    sheet.write(i,j,data_list[i][j])
            book.save(r'百思不得姐.xls')
        except:
            print('\n\n写入excel出现错误，错误信息为:{}\n\n')
