#coding=utf8
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import datetime
import urllib2
import time
import sys

today = datetime.datetime.combine(datetime.date.today(),datetime.time())

client = MongoClient()
db = client["dysoso"]
tabledouban = db.douban
tabledlist = db.plist
apikey = "0d1c89d4a9852bb727559d7dfc8f8325"

                                
def getInfoById(doubanid):
    doubaninfo = tabledouban.find_one({"id":doubanid})
    if not doubaninfo:
        try:
            searchBack = urllib2.urlopen("http://api.douban.com/v2/movie/subject/"+doubanid+"?apikey="+apikey,timeout=5).read()
            back = json.loads(searchBack)
            if back:
		back["today"] = today
                tabledouban.save(back)
	    print 'one ok'
            time.sleep(1.6)
        except:
	    print 'one error'

def doubanDetail():
    allPaihang = tabledlist.find()
    for onePaihang  in allPaihang:
	plist = onePaihang.get("plist")
	for onefilm in plist:
	    getInfoById(onefilm.get("id"))


def catchTop100():
    try:
        searchBack = urllib2.urlopen("http://api.douban.com/v2/movie/top250?start=0&count=100&apikey="+apikey).read()
        back = json.loads(searchBack)
        if back and back.get('subjects') :
	    subjects = back.get('subjects')
            savedb = {"pname":"top100","today":today,"plist":subjects}
            indbtop = tabledlist.find_one({"pname":"top100","today":today})
            if indbtop:
                savedb['_id']=indbtop['_id']
            tabledlist.save(savedb)
            print 'sucess'
    except:
        pass

if __name__ == '__main__':
    if len(sys.argv) <= 1 :
        print "input argv  > 1  :  top100 | douban_detail "
    else:     
        print 'start'
        if sys.argv[1] == "top100":
            catchTop100()
        if sys.argv[1] == "douban_detail":
            doubanDetail()
        print 'end'

