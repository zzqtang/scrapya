import scrapy
import re
import urllib
import MySQLdb
import sys
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request
from dbtop.items import DbtopItem

class dbtop250(scrapy.spiders.Spider):
    name='dbtop'
    allowed_domains=["movie.douban.com"]
    start_urls=["https://movie.douban.com/top250"]
    def parse(self,response):
        se=Selector(response)
        
        src=se.xpath("//*[@id='content']/div/div[1]/ol/li")
        # print(src)
        name=se.xpath("////*[@id='content']/div/div[1]/ol/li[25]/div/div[2]/div[1]/a/span[1]/text()").extract()
            
        # detail=se.xpath("//*[@id='content']/div/div[1]/ol/li[25]/div/div[2]/div[2]/p[1]/text()").extract()
        # rate=se.xpath("//*[@id='content']/div/div[1]/ol/li[25]/div/div[2]/div[2]/div/span[2]/text()").extract()
        # profile=se.xpath("//*[@id='content']/div/div[1]/ol/li[25]/div/div[2]/div[2]/p[2]/span/text()").extract()
        # detail1=','.join(''.join(detail).strip().lstrip().rstrip(',').split('\n'))
        # item=DbtopItem()
        # item['name']=name
        # item['detail']=detail1[:-2]
        # item['rate']=rate
        # item['profile']=profile
        # print(item['name'],item['detail'],item['rate'],item['profile'])
        for i in range(len(src)+1):
            name=se.xpath("////*[@id='content']/div/div[1]/ol/li[%d]/div/div[2]/div[1]/a/span[1]/text()"%i).extract()
            
            detail=se.xpath("//*[@id='content']/div/div[1]/ol/li[%d]/div/div[2]/div[2]/p[1]/text()"%i).extract()
            rate=se.xpath("//*[@id='content']/div/div[1]/ol/li[%d]/div/div[2]/div[2]/div/span[2]/text()"%i).extract()
            profile=se.xpath("//*[@id='content']/div/div[1]/ol/li[%d]/div/div[2]/div[2]/p[2]/span/text()"%i).extract()
            detail1=','.join(''.join(detail).strip().lstrip().rstrip(',').split('\n'))
            #print(','.join(detail1.strip().lstrip().rstrip(',').split('\n')))
            if profile:
                profile=profile
            else:
                profile=''
            item=DbtopItem()
            item['name']=name
            item['detail']=detail1[:-2]
            item['rate']=rate
            item['profile']=profile
            #print(item['name'],item['detail'],item['rate'],item['profile'])
            yield item
        next_url=se.xpath("//span[@class='next']/a/@href").extract()
        if next_url:
            url='https://movie.douban.com/top250'+next_url[0]
            yield Request(url,callback=self.parse)
            
