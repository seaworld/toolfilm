# coding=utf8
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from catchfilm.items import DyttItem
import pymongo
from datetime import datetime
import re

client = pymongo.MongoClient()
db = client["dysoso"]
table = db.film


class DyttSpider(CrawlSpider):
    name = 'dytt'
    allowed_domains = ['www.dytt8.net', 'www.ygdy8.net']
    start_urls = ['http://www.dytt8.net/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/html/gndy/dyzz/\d+/\d+.html'), callback='parse_dianyin'),
        Rule(SgmlLinkExtractor(allow=r'/html/gndy/jddy/\d+/\d+.html'), callback='parse_dianyin'),

        Rule(SgmlLinkExtractor(allow=r'/html/gndy/china/index.html'), process_links='parse_links'),
        # Rule(SgmlLinkExtractor(allow=r'/html/gndy/china/list_4_\d+.html'), process_links='parse_links'),
        Rule(SgmlLinkExtractor(allow=r'/html/gndy/oumei/index.html'), process_links='parse_links'),
        # Rule(SgmlLinkExtractor(allow=r'/html/gndy/oumei/list_7_\d+.html'), process_links='parse_links'),
        Rule(SgmlLinkExtractor(allow=r'/html/gndy/rihan/index.html'), process_links='parse_links'),
        # Rule(SgmlLinkExtractor(allow=r'/html/gndy/rihan/list_6_\d+.html'), process_links='parse_links'),
        Rule(SgmlLinkExtractor(allow=r'/html/gndy/jddy/index.html'), process_links='parse_links'),
        # Rule(SgmlLinkExtractor(allow=r'/html/gndy/jddy/list_63_\d+.html'), process_links='parse_links'),
        Rule(SgmlLinkExtractor(allow=r'/html/gndy/dyzz/index.html'), process_links='parse_links'),
        # Rule(SgmlLinkExtractor(allow=r'/html/gndy/dyzz/list_23_\d+.html'), process_links='parse_links'),
        Rule(SgmlLinkExtractor(allow=r'/html/gndy/index.html'), process_links='parse_links'),
    )

    def parse_dianyin(self, response):
        atype = '电影'
        sel = Selector(response)
        title = []
        cast = []
        summary = ""
        downurllist = []
        year = ""
        country = []

        cast_in = False
        summary_in = False

        text_all = sel.xpath('//*[@id="Zoom"]//text()').extract()
        for oneline in text_all:
            if oneline.startswith(u'◎') or oneline.startswith(u'【下载地址】'):
                cast_in = False
                summary_in = False
            if oneline.startswith(u'◎译　　名'):
                title_all = oneline.replace(u'◎译　　名', '').strip()
                title += title_all.split("/")
            if oneline.startswith(u'◎又　　名'):
                title_all = oneline.replace(u'◎又　　名', '').strip()
                title += title_all.split("/")
            if oneline.startswith(u'◎片　　名'):
                title_all = oneline.replace(u'◎片　　名', '').strip()
                title += title_all.split("/")
            if oneline.startswith(u'◎国　　家'):
                country_text = oneline.replace(u'◎国　　家', '').strip()
                country = country_text.split("/")
            if oneline.startswith(u'◎类　　别'):
                mtype_text = oneline.replace(u'◎类　　别', '').strip()
                mtype = mtype_text.split("/")
            if oneline.startswith(u'◎语　　言'):
                lang = oneline.replace(u'◎语　　言', '').strip()
            if oneline.startswith(u'◎年　　代'):
                year = oneline.replace(u'◎年　　代', '').strip()
            if oneline.startswith(u'◎导　　演'):
                director_text = oneline.replace(u'◎导　　演', '').strip()
                director = director_text.split("/")
            if oneline.startswith(u'◎主　　演') or cast_in:
                cast_in = True
                oneCast = oneline.replace(u'◎主　　演', '').strip()
                cast.append(oneCast)

            if oneline.startswith(u'◎简　　介') or summary_in or oneline.startswith(u'◎幕后花絮'):
                summary_in = True
                summary_text = oneline.replace(u'◎简　　介', '').strip()
                summary_text = summary_text.replace(u'◎幕后花絮', '').strip()
                summary += summary_text

            if oneline.startswith('ftp://'):
                downurllist.append(oneline)

        imageurl = sel.xpath('//*[@id="Zoom"]//img/@src').extract()
        item = DyttItem()
        if title and downurllist:
            item["title"] = title
            item["mtype"] = mtype
            item["atype"] = atype
            item["lang"] = lang
            item["director"] = director
            item["url"] = response.url
            item["country"] = country
            item["year"] = year
            item["cast"] = cast
            item["downurllist"] = downurllist
            item["updatetime"] = datetime.now()
            item["summary"] = summary
            item["fromtype"] = '电影天堂'
            item["image_urls"] = imageurl
            return [item]
        else:
            return []

        def parse_links(self, links):
            return links



