# coding=utf8
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
import pymongo
from datetime import datetime
from catchfilm.items import PoxiaoItem

client = pymongo.MongoClient()
db = client["dysoso"]
table = db.film


class TutuzxSpider(CrawlSpider):
    name = 'poxiao'
    allowed_domains = ['www.poxiao.com']
    #start_urls = ['http://www.poxiao.com/']
    start_urls = ['http://www.poxiao.com/movie/38319.html']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/movie/\d+\.html'), callback='parse_item', process_links='parse_links'),
        Rule(SgmlLinkExtractor(allow=r'/type/.*/index(_2)?\.html'), process_links='parse_links'),  # 迭代更新时候使用,前3页
        Rule(SgmlLinkExtractor(allow=r'/type/movie/$'), process_links='parse_links'),
    )

    def parse_item(self, response):
        sel = Selector(response)
        item = PoxiaoItem()
        title = sel.xpath('//*[@id="film"]/h1/text()').extract()
        filminfo = sel.xpath('//div[@id="film"]/div/table/tr')
        for oneinfo in filminfo:
            keyvalue = oneinfo.xpath("td")
            if len(keyvalue) == 2:
                key = keyvalue[0].xpath('text()').extract()[0]
                if key == u"主演：":
                    cast = keyvalue[1].xpath('a/text()').extract()
                    item["cast"] = cast
                elif key == u"别名：":
                    alt_title = keyvalue[1].xpath('strong/text()').extract()
                    title = title + alt_title
                elif key == u"导演：":
                    director = keyvalue[1].xpath('a/text()').extract()
                    item["director"] = director
                elif key == u"国家/地区：":
                    country = keyvalue[1].xpath('text()').extract()
                    item["country"] = country
                elif key == u"类型：":
                    movie_type = keyvalue[1].xpath('text()').extract()
                    item["mtype"] = movie_type
                elif key == u"上映日期：":
                    year = keyvalue[1].xpath('text()').extract()[0]
                    item["year"] = year
                elif key == u"对白语言：":
                    status = keyvalue[1].xpath('text()').extract()
                    if status and status[0]:
                        item["lang"] = status[0]
        image_urls = sel.xpath('//div[@class="detail_pic"]//img/@src').extract()
        downlistSel = sel.xpath('//div[@class="resourcesmain"]/table/tr/td')
        downurllist = []
        for oneSel in downlistSel:
            urllist = oneSel.xpath("input/@value").extract()
            if urllist:
                onedownurl = urllist[0]
                if onedownurl.startswith("xzurl="):
                    onedownurl = onedownurl.replace("xzurl=", "")
                    if onedownurl.__contains__("&mc="):
                        onedownurl = onedownurl.split("&")[0]
                    if onedownurl.startswith("cid="):
                        onefilename = oneSel.xpath("a/text()").extract()[0]
                        cid = onedownurl.replace("cid=", "")
                        if len(cid) < 15:
                            continue
                        downurllist.append("http://thunder.ffdy.cc/" + cid + "/" + onefilename)
                    else:
                        downurllist.append(onedownurl)
        summary = " ".join(sel.xpath('//*[@class="filmcontents"]//*/text()').extract())
        if title and downurllist:
            item["title"] = title
            item["url"] = response.url
            item["summary"] = summary
            item["image_urls"] = image_urls
            item["downurllist"] = downurllist
            item["updatetime"] = datetime.now()
            item["atype"] = "电影"
            item["fromtype"] = '破晓电影'
            return [item]
        else:
            return []

    def parse_links(self, links):
        return links


