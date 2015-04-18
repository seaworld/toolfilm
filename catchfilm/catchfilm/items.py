#coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class BaseItem(Item):
    title= Field() #名字 list
    status = Field() #状态 string
    country = Field() #国家
    director = Field() #导演
    writer = Field() #编剧
    cast = Field() #演员 list<string>
    year = Field() #上映年代
    mtype= Field()  #电影类别
    atype = Field() #电影，电视剧，动漫,3D,预告
    summary = Field() #摘要
    downurllist = Field() #下载地址
    lang = Field() #string 紧紧显示使用
    updatetime = Field() #修改时间
    fromtype = Field() #来源


class DyttItem(BaseItem):
    url = Field()
    images = Field()
    image_urls = Field()
    pass


class TuccItem(BaseItem):
    url = Field()
    images = Field()
    image_urls = Field()
    pass

class TutuItem(BaseItem):
    url = Field()
    images = Field()
    image_urls = Field()
    pass


class PoxiaoItem(BaseItem):
    url = Field()
    images = Field()
    image_urls = Field()
    pass

class MilaiItem(BaseItem):
    url = Field()
    images = Field()
    image_urls = Field()
    pass

