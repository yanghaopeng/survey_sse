#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/4 9:04
# @Author  : hyang
# @File    : scrapy_sse.py
# @Software: PyCharm

import requests
import time
from requests.exceptions import *
from urllib import parse
import re
import random
import utils
import json

class Scrapy_Sse(object):
    """
    爬上交所网站
    """
    PERPAGE = 10 # 每页记录数

    def __init__(self, keyword_str):
        """
        keywords 搜索关键字
        :param keywords:
        """
        self.session = requests.session()  # 包括了cookies信息
        self.session.verify = False  # 忽略证书认证
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer": "http://www.sse.com.cn/home/search/?webswd="+parse.quote(keyword_str)
        }
        self.search_keywords = keyword_str  # 搜索关键字
        self.main_url = "http://www.sse.com.cn/"



    def _getTime(self):
        """
        返回时间串
        :return:
        """
        return str(int(time.time()*1000))


    def _get_response(self, url,search_param):
        try:
            response = self.session.get(url, timeout=3, allow_redirects=False,
                                        headers=self.headers, params = search_param)
            if response.status_code == 200:
                response.encoding = 'utf-8'  # 设置编码
                utils.print_log('访问网站成功')
                return response
            else:
                utils.print_log('访问网站失败，继续访问……','error')
                time.sleep(1)
                response = self.session.get(url, timeout=3, allow_redirects=False,
                                            headers=self.headers, params=search_param)

                return response
        except ReadTimeout:
            print('ReadTimeout')
        except ConnectionError:  # 网络不通
            print('ConnectionError')
        except RequestException:
            print('Error')

    def getCount_info(self):
        """
        返回搜索关键字的总记录信息
        :return:
        """
        search_pdf = 'T_L CTITLE T_D E_KEYWORDS T_JT_E T_L{}T_RT_R'.format(self.search_keywords)
        main_url = "http://query.sse.com.cn/search/getCountSearchResult.do?"
        jsonCallBack = 'jQuery111205754136768616551_' + self._getTime()
        param_dict = {
            'search': 'lmmzs',
            'jsonCallBack': jsonCallBack,
            'searchword': search_pdf,
        }
        count_html = self._get_response(main_url, param_dict)
        if count_html:
            utils.print_log('获得记录数成功')
            return count_html.text
        else:
            return ''


    def parseCount_info(self,html):
        """
        解析记录数
        jQuery111205754136768616551_1522828623792({"data":[{"link":"search?channelid=274878&searchword=%28+CTITLE+%2C+E_KEYWORDS+%2B%3D+%28%E4%B8%87%E7%A7%91%29%29&
        classsql=CCHANNELCODE%3D%28%278349%27%29&
        keyword=%28+CTITLE+%2C+E_KEYWORDS+%2B%3D+%28%E4%B8%87%E7%A7%91%29%29&datatype=json",
        "num":"6",
        :param html:
        :return:
        """
        data = re.findall(r'jQuery\d+_\d+\((.*?)\)', html)  # 正则提取data
        count = 0
        if data:
            json_data = json.loads(data[0])
            num_data = json_data['data']
            if num_data:
                for item in num_data:
                    count += int(item['num'])
            # self.count = count  # 获得记录数
            msg = '数据num提取成功，记录数为{}'.format(count)
            utils.print_log(msg)
            return count


    def getPdf_info(self,page):
        """
        返回pdf信息
        :return:
        """
        search_pdf ='T_L CTITLE T_D E_KEYWORDS T_JT_E T_L{}T_RT_R'.format(self.search_keywords)
        url = "http://query.sse.com.cn/search/getSearchResult.do?"
        jsonCallBack = 'jQuery111205754136768616551_'+self._getTime()
        param_dict={
            'search': 'qwjs',
            'jsonCallBack': jsonCallBack,
            'page': page,
            'searchword': search_pdf,
            'orderby': '-CRELEASETIME',
            'perpage': self.PERPAGE,
            '_': self._getTime()
        }

        pdf_html = self._get_response(url,param_dict)
        if pdf_html:
            utils.print_log('获得PDF信息')
            return pdf_html.text
        else:
            return ''

    def parse_pdf_info(self,html):
        """
        解析pdf信息,返回data
        :param url_text:
        :return:
        """
        # print(html)
        """
        解析
        jQuery111205754136768616551_1522825042126({"count":"13","countPage":"2","data":[{"CCHANNELCODE":"8349","CONTENT":"证券代码：600239 证券简称：
        """
        data = re.findall(r'jQuery\d+_\d+\((.*?)\)', html)  # 正则提取data
        if data:
            json_data = json.loads(data[0])
            msg = '数据提取成功,获得记录数为{}'.format(len(json_data['data']))
            utils.print_log(msg)
            return json_data['data']
        else:
            utils.print_log('数据提取失败','error')
            return ''

    def parse_data(self, p_data):
        """
        解析pdf数据，获得文件
        :param p_data:
        :return:
        """
        pdf_li = []  # pdf文件信息
        pdf_title = []  # pdf信息列表
        if p_data:
            for item in p_data:
                pdf_li.append(self.main_url+item['CURL'])
                pdf_title.append(item['CTITLE_TXT'])
            utils.print_log(pdf_title)
            utils.print_log(pdf_li)

    def save_file(self, file_name):
        """
        保存文件
        :return:
        """


    def main(self):
        """
        主函数
        :return:
        """
        # main_html = self.getMain_info()
        # print(main_html.text)
        # se_html = self.getPdf_info(1)
        # se_data = self.parse_pdf_info(se_html)
        # self.parse_data(se_data)
        se_con_html = self.getCount_info()
        count = self.parseCount_info(se_con_html)
        if count:
            msg = '搜索关键字--{},得到相关记录数为{}，开始提取PDF信息'.format(self.search_keywords,count)
            utils.print_log(msg)
            pages = count // self.PERPAGE  # 得到页数
            surplus = count % self.PERPAGE  # 得到余数
            if surplus > 0:
                pages +=1
            for i in range(1, pages+1):
                se_html = self.getPdf_info(i)
                se_data = self.parse_pdf_info(se_html)
                self.parse_data(se_data)
        else:
            msg = '搜索关键字--{},得到相关记录数为{}'.format(self.search_keywords, 0)
            utils.print_log(msg,'error')


if __name__ == '__main__':
    keyword_str = '万科'
    se = Scrapy_Sse(keyword_str)
    se.main()

"""
T_L CTITLE T_D E_KEYWORDS T_JT_E T_L万科T_RT_R
var searchPdf = "T_L CTITLE T_D E_KEYWORDS T_JT_E likeT_L";
function searchpdf(indexf){
  if("1"==indexf){
    ispdf = false;
    searchPdf ="T_L CTITLE T_D E_KEYWORDS T_JT_E likeT_L";
  }else{
    ispdf = true;
    searchPdf ="T_L CTITLE T_D CONTENT T_JT_E likeT_L";
  }
}

http://query.sse.com.cn/search/getSearchResult.do?
search=qwjs&jsonCallBack=jQuery111205754136768616551_1522805294462&page=1&
searchword=T_L+CTITLE+T_D+E_KEYWORDS+T_JT_E+T_L%E4%B8%87%E7%A7%91T_RT_R&
orderby=-CRELEASETIME&perpage=10&_=1522805294463

http://query.sse.com.cn/search/getCountSearchResult.do?search=lmmzs&
jsonCallBack=jQuery111205754136768616551_1522805294460&
searchword=T_L+CTITLE+T_D+E_KEYWORDS+T_JT_E+T_L%E4%B8%87%E7%A7%91T_RT_R
得到count
"""
