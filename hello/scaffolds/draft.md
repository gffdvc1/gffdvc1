---
title: {{ title }}
tags:
---
*学习scrapy结合selenium总结*

**DownLoaderMiddleware用法

**DownLoaderMiddleware简介**
调度器会从队列中拿出一个请求发送给下载器执行下载，会经过downloadermiddleware处理，下载器下载完成之后仍会经过downloadermiddleware。作用主要是在request执行之前和在生成response之后页能够进行修改。
程序中有多个中间件，setting中设置的键值对表示其中间件的优先级，优先级越小代表越靠近引擎，越大越靠近下载器。其核心方法有三个：process_request,process_response与process_exception.
process_request方法：返回值必须为None，request，response； 返回为None，表示继续执行之后的操作，
	返回参数|作用
	：----：|：-
	 None   |继续执行之后的操作，
	 request|之后的操作不在进行，这个request会返回给引擎，在加入调度器中队列中，等待被执行。
	 response|不断调用process_response方法，知道发送给引擎，进行后续操作。

##boss直聘爬虫练习
**创建项目**
新建scrapy框架：
\```
scrapy startproject zhipin
\```
新建爬虫的py文件
\```
	cd zhipin
	scrapy genspider boss boss.com
\```
更改setting配置：将ROBOT_OBAY = False并新添加LOG_LEVEL='ERROR';