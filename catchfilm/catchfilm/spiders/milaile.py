# coding=utf8
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
import pymongo
from datetime import datetime
from catchfilm.items import MilaiItem

client = pymongo.MongoClient()
db = client["dysoso"]
table = db.film


class TutuzxSpider(CrawlSpider):
    name = 'milai'
    allowed_domains = ['www.milaile.com']
    start_urls = ['http://www.milaile.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/movie/\d+/\d+\.html'), callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=r'\?p=\d&s=&cid=0&mid=0&year=0&order=&today=0&sarea=&sactor=&sdirector=&slang=&iplay=&&pp=0&&top=0&stype=&isbest=0'), process_links='parse_links'), 
    )

    def parse_item(self, response):
        sel = Selector(response)
        item = MilaiItem()
        title = sel.xpath('//div[@class="movieinfo cl"]/ul/li[@class="movie-tit"]/text()').extract()
        if title and title[0]:
            title = title[0].split("/")
        filminfo = sel.xpath('//div[@class="movieinfo cl"]/ul/li')
        item["mtype"] = []
        for oneinfo in filminfo:
            keyvalue = oneinfo.xpath("span")
            if len(keyvalue) == 2:
                key = keyvalue[0].xpath('text()').extract()[0]
                if key == u"主演：":
                    cast = keyvalue[1].xpath('a/text()').extract()
                    item["cast"] = cast
                elif key == u"又名：":
                    alt_title = keyvalue[1].xpath('text()').extract()
                    if alt_title and alt_title[0]:
                        alt_title = alt_title[0].split("/")
                        title = title + alt_title
                elif key == u"导演：":
                    director = keyvalue[1].xpath('a/text()').extract()
                    item["director"] = director
                elif key == u"地区：":
                    country = keyvalue[1].xpath('a/text()').extract()
                    item["country"] = country
                elif key == u"类别：" or key == u"分类：":
                    movie_type = keyvalue[1].xpath('a/text()').extract()
                    item["mtype"] += movie_type
                elif key == u"编剧：":
                    writer = keyvalue[1].xpath('a/text()').extract()
                    item["writer"] = writer
                elif key == u"年份：":
                    year = keyvalue[1].xpath('a/text()').extract()[0]
                    item["year"] = year
                elif key == u"语言：":
                    status = keyvalue[1].xpath('a/text()').extract()
                    if status and status[0]:
                        item["lang"] = status[0]
        summary = " ".join(sel.xpath('//div[@class="zy"]//div[@id="content"]/text()').extract())
        image_urls = sel.xpath('//div[@class="moviedteail_img"]/a/img/@src').extract()
        downurllist = sel.xpath('//div[@class="downlist"]/a/@thunderhref').extract()
        if title and downurllist:
            title = list(set(title))
            item["title"] = title
            item["url"] = response.url
            item["summary"] = summary
            item["image_urls"] = image_urls
            item["downurllist"] = downurllist
            item["updatetime"] = datetime.now()
            item["atype"] = u"电影"
            item["fromtype"] = u'米来网'
            return [item]
        else:
            return []

    def parse_links(self, links):
        # newlinks = []
        # for link in links:
        # # 全站抓的时候，需要这样，避免重复抓取
        #     if not table.find_one({"url": link.url}):
        #         newlinks.append(link)
        # return newlinks
        return links


