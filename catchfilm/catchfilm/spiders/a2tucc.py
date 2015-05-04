# coding=utf8
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from catchfilm.items import BaseItem, TuccItem
import pymongo
from datetime import datetime
import re

client = pymongo.MongoClient()
db = client["dysoso"]
table = db.film

class A2tuccSpider(CrawlSpider):
    name = '2tucc'
    allowed_domains = ['www.2tu.cc']
    start_urls = ['http://www.2tu.cc/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/Html/GP\d+.html'), callback='parse_item', process_links='parse_links'),
        # 这里表示每个列表只取前几页
        Rule(SgmlLinkExtractor(allow=r'/GvodHtml/\d+(_[1-3])?\.html')),
        # Rule(SgmlLinkExtractor(allow=r'/GvodHtml/\d+(_\d+)?\.html') ),
    )

    def parse_item(self, response):
        sel = Selector(response)
        atype = sel.xpath('//*[@id="main"]/div[2]/div[1]/a[2]/text()').extract()[0]
        mtype = sel.xpath('//*[@id="main"]/div[2]/div[3]/ul/li[2]/a/text()').extract()
        title = sel.xpath('//*[@id="main"]/div[2]/div[2]/img/@alt').extract()[0]
        country = sel.xpath('//*[@id="main"]/div[2]/div[3]/ul/li[4]/text()').extract()
        year = sel.xpath('//*[@id="main"]/div[2]/div[3]/ul/li[1]/text()[1]').extract()[0]
        cast = sel.xpath('//*[@id="main"]/div[2]/div[3]/ul/li[3]/a/text()').extract()
        summary = '\n'.join(sel.xpath('//div[@class="endtext"]/text()').extract())
        imageurl = sel.xpath('//*[@id="main"]/div[2]/div[2]/img/@src').extract()
        downdivlist = sel.xpath('//div[@class="hdownlist"]/ul/li/span').extract()
        downurllist = []
        for one in downdivlist:
            if one.__contains__(r'https://d.miwifi.com/d2r/?url="'):
                pp = re.compile(r'Base64\.encodeURI\(ThunderEncode\(\'(.*?)\'\)\)\+')
                downurl = pp.search(one).groups()[0]
                downurllist.append(downurl)
        downlistDivs = sel.xpath("//div[@class='downlist']").extract()
        for one in downlistDivs:
            if one.__contains__(r'<script>var GvodUrls ='):
                pp = re.compile(r'<script>var GvodUrls = "(.*?)";</script>')
                downurl = pp.search(one).groups()[0]
                downurls = downurl.split("###")
                downurllist += downurls

        item = TuccItem()
        if title and downurllist:
            title = title.split('/')
            item["title"] = title
            item["mtype"] = mtype
            item["atype"] = atype
            item["url"] = response.url
            item["country"] = country
            item["year"] = year
            item["cast"] = cast
            item["downurllist"] = downurllist
            item["updatetime"] = datetime.now()
            item["summary"] = summary
            item["fromtype"] = '迅播影院'
            item["image_urls"] = imageurl
            return [item]
        else:
            return []

    def parse_links(self, links):
        return links



