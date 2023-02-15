---
title: Hello World
---
Welcome to [Hexo](https://hexo.io/)! This is your very first post. Check [documentation](https://hexo.io/docs/) for more info. If you get any problems when using Hexo, you can find the answer in [troubleshooting](https://hexo.io/docs/troubleshooting.html) or you can ask me on [GitHub](https://github.com/hexojs/hexo/issues).

## Quick Start

### Create a new post

``` bash
$ hexo new "学习scrapy结合selenium总结"
```
selenium 应该放到downmiddleware类中，
	首先downmiddleware中方法的简述：
	process_request()方法在引擎向下载器发送请求过程中，可以添加UA等请求头部，
		cookies等参数。
		
	process_response():
	此方法在下载器完成请求返回的过程中。
	
	process_exception():此方法用于处理当请求过程中出现的异常。

	spider_opened()：爬虫开始前要调用的方法，目前所学到的知识是可以添加selenium执行登录操作

	主要听讲案例：爬boss直聘网页


# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题


**这是加粗的文字** __这是加粗的文字__
*这是倾斜的文字*
***这是斜体加粗的文字***
~~这是加删除线的文字~~
==标记文本==
> 引用文本
