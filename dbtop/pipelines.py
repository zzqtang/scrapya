# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi

import pymysql
import codecs
import json
from logging import log
class DbtopPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod    
    def from_settings(cls,settings):
        dbparams=dict(
        host=settings['MYSQL_HOST'],
        db=settings['MYSQL_DBNAME'],
        user=settings['MYSQL_USER'],
        passwd=settings['MYSQL_PASSWD'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
        use_unicode=False,
        )
        dbpool=adbapi.ConnectionPool('pymysql',**dbparams)
        return cls(dbpool)
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditional_insert,item)
        #query.addErrback(self._handle_error,item,spider)
        return item
    def _conditional_insert(self,tx,item):
        sql='insert into dbmovie(name,detail,rate,profile) values(%s,%s,%s,%s)'
        
        params=(item['name'],item['detail'],item['rate'],item['profile'])
        tx.execute(sql,params)
        
        
        
        
        
