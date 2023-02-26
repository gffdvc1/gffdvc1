---
title: 增量式爬虫爬取tianya网站
date: 2023-02-26 09:22:30
tags:
---
## 增量式爬虫相关知识
增量爬虫的核心：去重。
目标网站：一般会时时更新的网站，比如获取新闻，微博等评论。
增量爬虫如何去重：

1. 在请求发起之前，判断此url是否爬取过
2. 在解析内容之后，判断该内容是否被爬取过
3. 在保存数据时，判断将要写入的内容是否存在于存储介质中

## 创建爬虫项目
1. 创建项目命令：
` scrapy startproject tianya `
2. cd命令进入文件tianya后，创建spider爬虫文件
`cd tianya`
`scrapy genspider ty tianya.cn`

## settings相关配置

将是否顺从robot协议的值该为false，并且将log等级该为提醒，取消注释item_pipeline.


` ROBOTSTXT_OBEY = False `
` LOG_LEVEL = 'WARNING '`

## 连接数据库

定义内置函数连接数据库（这里的host，port，password均为默认值）

`def __init__(self):`
`	self.redis = Redis(decode_responses = True)`


## 分析网页源代码获取详情页url及请求下一页

![如图](img/天涯网.png#pic_center =300x100 ''图片title'')

首先确定获取目标，这里要获取网站中个新闻标题的href属性内容，分析网页源代码可以发现，所有的超链接a标签都放在属性class为mt5的div标签的子孙标签td中，这里获取td标签需要先获取tr标签之后西安则填入标签下的第一个td标签下的a标签属性href。需要注意的是第一个tr标签显示的是整个框架的标题，所以写下path路径是要将第一个标签排除在外。这时确定详情页的url后，就可以完成parse方法代码，如下：

----------------------------------------
1). 发送请求前判断此url是否爬取过
方法：使用数据库中的set集合去重判断当前url是否爬取过。使用sismember()方法在请求之前判断是否已经存在集合set中，，如果存在直接跳转到下一个url判断，否则请求此网页。这里需要注意当前判断并没有添加url到redis中，需要请求之后将刚请求到数据url添加到redis中。

\```

	#代码
	def parse(self, response):
        print(response)
        #print(response.text)
        trs = response.xpath("//div[@class='mt5']//tr[position()>1]/td[1]")
        for i,tr in enumerate(trs):
            href = tr.xpath("./a/@href").extract_first()
            #这里判断一下当前下载的url是否存入数据库
            if self.redis.sismember(REDIS_KEY,response.urljoin(href)):#判断当前url是否存在在集合中，
                print("已经抓取过")
                continue
            else:#不存在发送请求
                yield scrapy.Request(
                    url = response.urljoin(href),
                    method = "get",
                    callback = self.parse_detail
                    )

        #分页操作
        next_page = response.xpath('//div[@class="short-pages-2 clearfix"]/div[1]/a[2]/@href').extract_first()
        if next_page:
            yield scrapy.Request(
                url = response.urljoin(next_page),
                callback = self.parse
                )
\```

------------------------------------------
2) 解析内容之后，判断该内容是否被爬取过，在详情页的解析之后判断内容是否存在与数据库中，使用sismember()方法，代码如下：

\```

	def parse_detail(self,response):
        title = response.xpath('//span[@class="s_title"]/span/text()').extract_first()
        content = response.xpath('//div[@class="atl-content"]/div[2]/div/text()').extract_first()
        result = self.redis.sismember("titles2",title)
        if not result:
            self.redis.sadd("titles2",title)
            item = Tianya2Item()
            item["title"] = title
            item['content'] = content
            self.redis.sadd(REDIS_KEY,response.url)
            print(title+"已经存储到redis")
            yield item
        else:
            print(title+"已经抓取过了")
\```

-----------------------------------------------------
3）在保存数据时，判断将要写入的内容是否存在于存储介质中
暂时还不会

[完整代码](C:\Users\20495\blog\source\_posts\python文件\tianya2)


## 总结
还未搞懂，连接数据库的__init__()方法为什么要继承父类