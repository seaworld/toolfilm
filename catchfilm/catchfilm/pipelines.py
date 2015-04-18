# coding=utf-8
from pymongo import MongoClient
from items import  TutuItem, TuccItem, PoxiaoItem, MilaiItem ,DyttItem


class BasePipeline(object):
    def __init__(self):
        client = MongoClient()
        self.db = client["dysoso"]

    def process_item(self, item, spider):
        if item.__class__ == TutuItem:
            oneFilm = save_tutu(item)
            one = self.db.film.find_one({'url': oneFilm['url']})
            if one:
                oneFilm['_id'] = one['_id']
            self.db.film.save(oneFilm)

        elif item.__class__ == TuccItem:
            oneFilm = save_2tucc(item)
            one = self.db.film.find_one({'url': oneFilm['url']})
            if one:
                oneFilm['_id'] = one['_id']
            self.db.film.save(oneFilm)

        elif item.__class__ == DyttItem:
            oneFilm = save_dytt(item)
            one = self.db.film.find_one({'url': oneFilm['url']})
            if one:
                oneFilm['_id'] = one['_id']
            self.db.film.save(oneFilm)

        elif item.__class__ == PoxiaoItem:
            oneFilm = save_poxiao(item)
            one = self.db.film.find_one({'url': oneFilm['url']})
            if one:
                oneFilm['_id'] = one['_id']
            self.db.film.save(oneFilm)

        elif item.__class__ == MilaiItem:
            oneFilm = save_milai(item)
            one = self.db.film.find_one({'url': oneFilm['url']})
            if one:
                oneFilm['_id'] = one['_id']
            self.db.film.save(oneFilm)
        return item


def save_2tucc(item):
    #if item["year"].startswith(u"上映年代："):
    #    item['year'] = item["year"].replace(u"上映年代：", "").strip()
    #if item["country"].startswith(u"地区："):
    #    item['country'] = [item["country"].replace(u"地区：", "").strip()]
    #if item["status"].startswith(u"状态："):
    #    item['status'] = item["status"].replace(u"状态：", "").strip()
    return item._values



def save_tutu(item):
    return item._values

def save_dytt(item):
    return item._values

def save_poxiao(item):
    return item._values

def save_milai(item):
    return item._values
