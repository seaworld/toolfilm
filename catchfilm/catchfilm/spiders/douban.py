#coding=utf8
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
import scrapy
import pymongo
import datetime
import time

client = pymongo.MongoClient()
db = client["dysoso"]
table= db.plist

class TutuzxSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = [
                'http://movie.douban.com/later/shanghai/',
                ]

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/nowplaying/shanghai/'), callback='parse_nowplaying_item' , process_links='parse_links'),
        Rule(SgmlLinkExtractor(allow=r'/later/shanghai/'), callback='parse_laterplaying_item'),
    )

    def parse_laterplaying_item(self,response):

        today = datetime.datetime.combine(datetime.date.today(),datetime.time())
    	sel = Selector(response)
        mlist = sel.xpath('//div[@id="showing-soon"]/div[@class="item mod "]')
        doubanlist = []
        for one_movie in mlist :
            dnow = {}
            url = one_movie.xpath("div/h3/a/@href").extract()[0]
            title = one_movie.xpath("div/h3/a/text()").extract()[0]
            img = one_movie.xpath("a/img/@src").extract()[0]
            mid = url.split("/")[-2]
            dnow['id']=mid
            dnow['alt']=url
            dnow['title']=title
            dnow['img']=img
            doubanlist.append(dnow)

        laterindb = {"pname":"laterplaying","today":today,"plist":doubanlist}
        todayplist =  table.find_one({"pname":"laterplaying","today":today})
        if todayplist:
            laterindb['_id'] = todayplist['_id']
        table.save(laterindb)
            
        time.sleep(5)
        return []
            

    def parse_nowplaying_item(self,response):
        today = datetime.datetime.combine(datetime.date.today(),datetime.time())
    	sel = Selector(response)
        mlist = sel.xpath('//div[@id="nowplaying"]/div/ul[@class="lists"]/li')
        doubanlist = []
        for one_movie in mlist :
            dnow = {}
            mid = one_movie.xpath("@id").extract()[0]
            title = one_movie.xpath("@data-title").extract()[0]
            score = one_movie.xpath("@data-score").extract()[0]
            duration = one_movie.xpath("@data-duration").extract()[0]
            img = one_movie.xpath(".//img/@src").extract()[0]
            country = one_movie.xpath("@data-region").extract()[0]
            dnow['id']=mid
            dnow['alt']=u'http://movie.douban.com/subject/'+mid+u"/"
            dnow['title']=title
            dnow['score']=score
            dnow['duration']=duration
            dnow['img']=img
            dnow['country']=country
            doubanlist.append(dnow)

        nowindb = {"pname":"nowplaying","today":today,"plist":doubanlist}
        todayplist =  table.find_one({"pname":"nowplaying","today":today})
        if todayplist:
            nowindb['_id'] = todayplist['_id']
        table.save(nowindb)

        doubanlist = []
        plist = sel.xpath('//div[@id="billboard"]')
        bdate = plist.xpath("div[@class='mod-hd']/h2/span/text()").extract()[0]
        plist  = plist.xpath(".//div[@class='chart-item']")
        for one_movie in plist:
            paihang = {}
            mid = one_movie.xpath("@data-subject").extract()[0] 
            title = one_movie.xpath("@data-title").extract()[0] 
            money = one_movie.xpath("div/span/text()").extract()[0] 
            paihang['id']=mid
            paihang['title']=title
            paihang['money']=money
            paihang['alt']=u'http://movie.douban.com/subject/'+mid+u"/"
            doubanlist.append(paihang)

        
        piaofangindb = {"pname":"guoneipiaofang","today":today,"plist":doubanlist}
        todayplist =  table.find_one({"pname":"guoneipiaofang","today":today})
        if todayplist:
            piaofangindb['_id'] = todayplist['_id']
        table.save(piaofangindb)

        time.sleep(5)
        return []


    def parse_links(self, links):
        return links


