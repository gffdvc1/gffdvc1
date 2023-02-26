import scrapy
from scrapy_redis.spiders import RedisSpider
from tianya2.items import Tianya2Item
from redis import Redis
REDIS_KEY = "ty_title_url"
class Ty2Spider(scrapy.Spider):
    name = 'ty2'
    allowed_domains = ['tianya.cn']
    start_urls = ['http://bbs.tianya.cn/list-worldlook-1.shtml']
    #redis_key = "ty_start_url"
    
    def __init__(self,name=None,**kwargs):
        self.redis = Redis(decode_responses = True)
        super(Ty2Spider,self).__init__(name)

    def parse(self, response):
        print(response)
        #print(response.text)
        trs = response.xpath("//div[@class='mt5']//tr[position()>1]/td[1]")
        for i,tr in enumerate(trs):
            href = tr.xpath("./a/@href").extract_first()
            """
            #这里判断一下当前下载的url是否存入数据库
            if self.redis.sismember(REDIS_KEY,response.urljoin(href)):#判断当前url是否存在在集合中，
                print("已经抓取过")
                continue
            else:#不存在发送请求
            """
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
                callback = self.parse)
            
    def parse_detail(self,response):
        title = response.xpath('//span[@class="s_title"]/span/text()').extract_first()
        content = response.xpath('//div[@class="atl-content"]/div[2]/div/text()').extract_first()
        item = Tianya2Item()
        item["title"] = title
        item['content'] = content
        yield item
     
 
        

