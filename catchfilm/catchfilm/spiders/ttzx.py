# coding=utf8
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from catchfilm.items import BaseItem, TutuItem
import pymongo
from datetime import datetime
import re

client = pymongo.MongoClient()
db = client["dysoso"]
table = db.film


class Tutuzx(CrawlSpider):
    name = 'ttzx'
    allowed_domains = ['tutuzx.com']
    start_urls = ['http://tutuzx.com']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/view/index\d+\.html'), callback='parse_item'),

        Rule(SgmlLinkExtractor(allow=r'/list/index33\.html'), process_links='parse_links'),
        # 这里表示每个列表只取前几页
        Rule(SgmlLinkExtractor(allow=r'/list/index33(_[2-4])?\.html'), process_links='parse_links'),
    )

    def parse_item(self, response):
        sel = Selector(response)
        atype = u"电影"
        title_text = sel.xpath('//div[@class="infobox box"]/img/@alt').extract()[0]
        title = title_text.split("/")
        imageurl = sel.xpath('//div[@class="infobox box"]/img/@src').extract()

        text_all = sel.xpath('//div[@class="info l"]/p//text()').extract()
        cast = []
        year = ""
        mtype=[]
        in_year = False
        in_mtype = False
        in_cast = False
        for oneline in text_all:
            if oneline and oneline.strip() and oneline.strip != r"""\r\n""":
                if oneline.startswith(u'年份：') or oneline.startswith(u'热度：') \
                        or oneline.startswith(u'类型：') or oneline.startswith(u'主演：') \
                        or oneline.startswith(u'时间：'):
                    in_year = False
                    in_mtype = False
                    in_cast = False
                if in_year:
                    year = oneline
                if in_mtype:
                    mtype.append(oneline)
                if in_cast:
                    cast.append(oneline.replace("/", ""))
                if oneline.startswith(u'年份：'):
                    in_year = True
                if oneline.startswith(u'类型：'):
                    in_mtype = True
                if oneline.startswith(u'主演：'):
                    in_cast = True
        summary = " ".join(sel.xpath('//div["description"]/ul/span/text()').extract())
        downurllist = sel.xpath('//div["description"]/ul/span//a/@href').extract()

        item = TutuItem()
        if title and downurllist:
            item["title"] = title
            item["mtype"] = mtype
            item["atype"] = atype
            item["url"] = response.url
            item["year"] = year
            item["cast"] = cast
            item["downurllist"] = downurllist
            item["updatetime"] = datetime.now()
            item["summary"] = summary
            item["fromtype"] = u'兔兔在线'
            item["image_urls"] = imageurl
            return [item]
        else:
            return []

    def parse_links(self, links):
        # newlinks = []
        # for link in links:
        # if not table.find_one({"url":link.url}):
        # newlinks.append(link)
        # return newlinks
        return links



