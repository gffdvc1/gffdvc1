# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:49:16 2023

@author: 20495
"""

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'


import redis
from random import choice

class RedisClient(object):
    def __init__(self,host = REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD,decode_responses = True):
        #链接redis
        self.db = redis.StrictRedis(host = host,port = port, password = password,decode_responses = True)
    
    #添加代理操作
    def add(self,proxy,score = INITIAL_SCORE):
        if not self.db.zscore(REDIS_KEY,proxy):
            mapping = {proxy:score}
            return self.db.zadd(REDIS_KEY,mapping)
        
    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY,0,100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError
                
    def decrease(self,proxy):
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print("代理",proxy,"当前分数",score)
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print("代理",proxy,"当前分数",score,"移除")
            return self.db.zrem(REDIS_KEY,proxy)
            
    def exist(self,proxy):
        return not self.db.zscore(REDIS_KEY,proxy) == None
    
    def max(self,proxy):
        print("代理",proxy,"可用，设置为",MAX_SCORE)
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)
    def count(self):
        return self.db.zcard(REDIS_KEY)
    
    def all(self):
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)
                
                
class PoolEmptyError:
    def __init__(self,):
        print("代理池为空！！！")
        
        
#获取模块
import json
#from utils import get_page
from pyquery import PyQuery as pq
import requests
import time


class ProxyMetaclass(type):
    def __new__(cls,name,bases,attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k,v in attrs.items():
            if "crawl" in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)
    
    
    
class Crawler(object,metaclass = ProxyMetaclass):
    def get_proxy(self,callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("成功获取到代理",proxy)
            proxies.append(proxy)
            
        return proxies
    
    
    def crawl_daili66(self,page_count = 10):
        start_url = 'http://www.66ip.cn/'
        urls = [start_url+str(page)+".html" for page in range(1,page_count+1)]
        for url in urls:
            print("Crawler",url)
            res = requests.get(url)
            html = res.text
            if html:
                doc = pq(html)
                trs = doc(".containerbox table tr:gt(0)").items()
                
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ":".join([ip,port])
    """

    def crawl_kuaidaili(self,page_count=10):
        start_url = 'https://www.kuaidaili.com/free/'
        urls = [start_url+'inha/'+str(page) for page in range(1,page_count+1)]
        for url in urls:
            print("Crawler",url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50'}
            res = requests.get(url,headers)
            
            print(res)
            html = res.text
            if html:
                doc = pq(html)
                trs = doc(".table tbody tr")
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text()
                    port = tr.find("td:nth-child(2)").text()
                    yield ":".join([ip,port])
            time.sleep(1)
    """
    
                
POOL_UPPER_THRESHOLD = 1000
class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    
    def isoverthreshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
        
    def run(self):
        print("开始执行")
        if not self.isoverthreshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxy(callback)
                for proxy in proxies:
                    self.redis.add(proxy)

        