---
title: scrapy重要操作
date: 2023-03-05 13:43:20
tags:
---
## scrapy对接selenium操作

在项目目录下创建request.py文件。创建seleniumrequest类，继承request父类，用于判断当前传入的请求是否需要selenium请求。
\```

	from scrapy import Request
	
	class SeleniumRequest(Request):
    	pass
\```
2.打开middleware.py文件。找到process_request()函数，判断当前请求的request是否是SeleniumRequest。修改代码如下：
\```

    def process_request(self, request, spider):
        if isinstance(request,SeleniumRequest):
            driver = webdriver.Edge()
            driver.get(request.url)
            page_source = driver.page_source
            return HtmlResponse(
                url = request.url
                ,status=200,body=page_source,
                request = request,
                encoding='utf-8'
                )
        respuest.cookies
        return None
\```