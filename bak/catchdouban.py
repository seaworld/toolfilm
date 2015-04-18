#coding=utf8
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import datetime
import urllib2
import time
import sys

#beforDate = datetime.datetime.now() - datetime.timedelta(minutes=40)

beforDate = datetime.datetime.now() - datetime.timedelta(days=5)
today = datetime.datetime.combine(datetime.date.today(),datetime.time())

client = MongoClient()
db = client["03soso"]
tablegood = db.good
tabledouban = db.douban
tablegood_douban = db.good_douban
tabledlist = db.dlist
apikey = "0d1c89d4a9852bb727559d7dfc8f8325"

def userInput(onegood,onedouban):
    print 'in good db'
    print onegood['title']
    print " ".join(onegood.get('cast')) if onegood.get('cast') else ""
    print " ".join(onegood.get('alt_title')) if onegood.get('alt_title') else ""
    print '---------------------'
    if not  onedouban:
        print "not douban in db "
    else:
        print 'in douban db'
        print onedouban['title']
        print " ".join([x['name'] for x in onedouban.get('casts')])
        print " ".join(onedouban.get('aka')) if onegood.get('aka') else ""
    print ''
    daan=raw_input('同意不?Y/N 或者豆瓣id:')

    if daan=='y' or daan =='':
        if not onedouban:
            return
        updateTheDoubanInfoToGood(onegood,onedouban)
    elif daan =='n':
        return 
    else:
        if daan.isalnum():
            daanint = int(daan)
            if daanint>0:
                onedouban = getInfoById(onegood['_id'],daan)
                if onedouban:
                    updateTheDoubanInfoToGood(onegood,onedouban)
                                
def getInfoById(goodid,doubanid):
    doubaninfo = tablegood_douban.find_one({"id":doubanid})
    if doubaninfo:
        return doubaninfo
    else:
        try:
            searchBack = urllib2.urlopen("http://api.douban.com/v2/movie/subject/"+doubanid+"?apikey="+apikey).read()
            back = json.loads(searchBack)
            if back:
                back['_id'] = goodid 
                tablegood_douban.save(back)
                return back
            time.sleep(1.6)
        except:
            pass

def goself(mins):
    beforDate = datetime.datetime.now() - datetime.timedelta(minutes=mins)
    dylist = tablegood.find({"douban":None,"updatedate":{"$gt":beforDate}}).sort("updatedate",-1)
    for dy in dylist:
        onedoubansearch = tabledouban.find_one({"_id":dy["_id"]})
        if not onedoubansearch :
            searchBack = urllib2.urlopen("http://api.douban.com/v2/movie/search?apikey="+apikey+"&q="+dy["title"].encode("utf8")).read()
            back = json.loads(searchBack)
            tabledouban.insert({"_id":dy["_id"],"data":back})
            time.sleep(1.6)
            onedoubansearch = tabledouban.find_one({"_id":dy["_id"]})

        if tablegood_douban.find_one({'_id':dy["_id"]}):
            continue
        else :
            ones = onedoubansearch.get("data").get("subjects")
            if ones:
                movie_id = ones[0]['id']
                newone = tablegood_douban.find_one({"id":movie_id})
                if newone:
                    newone['_id'] = dy['_id']
                    tablegood_douban.insert(newone)
                else:
                    try:
                        searchBack = urllib2.urlopen("http://api.douban.com/v2/movie/subject/"+movie_id+"?apikey="+apikey).read()
                        back = json.loads(searchBack)
                        if back:
                            back['_id'] = dy['_id']
                            tablegood_douban.insert(back)
                        time.sleep(1.6)
                    except:
                        pass
    seedm(mins)

def updateTheDoubanInfoToGood(onegood,onedouban):
    onegood['douban'] = {'id':onedouban['id'],'url':onedouban['alt'],'images':onedouban['images'],'rating':onedouban['rating'],'update':datetime.datetime.now()}
    onegood['titile'] = onedouban['title']
    onegood['director'] = [x['name'] for x in onedouban['directors']]
    onegood['cast'] =  onegood['cast'] if onegood.get('cast') else []
    onedouban['casts'] =  onedouban['casts'] if onedouban.get('casts') else []
    onegood['cast'] = list(set([x['name'] for x in onedouban['casts']]+onegood['cast']))
    onegood['movie_type'] = onedouban['genres']
    onegood['country'] = onedouban['countries']
    onegood['year'] = onedouban['year']
    onegood['summary'] = onedouban['summary']
    onegood['alt_title'] = onegood['alt_title'] if onegood.get('alt_title') else []  
    onedouban['aka'] = onedouban['aka'] if onedouban.get('aka') else [] 
    onegood['alt_title'] = list(set(onedouban['aka']+onegood['alt_title']))
    tablegood.save(onegood)
    

def seedm(mins):
    for onegood in tablegood.find({"douban":None,"updatedate":{"$gt":beforDate}}).sort("updatedate",-1):
        onedouban =  tablegood_douban.find_one({'_id':onegood['_id']})
        if onedouban and  onedouban['title']==onegood['title']:
            doubancast = [x['name'] for x in onedouban['casts']]
            right=0
            error=0
            if onegood.get('cast') and doubancast:
                for onecast in onegood.get('cast'):
                    if doubancast.__contains__(onecast):
                        right+=1
                    else:
                        error+=1
                if right>error:
                    updateTheDoubanInfoToGood(onegood,onedouban)


def iseedm(mins):
    for onegood in tablegood.find({"douban":None,"updatedate":{"$gt":beforDate}}).sort("updatedate",-1):
        onedouban =  tablegood_douban.find_one({'_id':onegood['_id']})
        userInput(onegood,onedouban)        

def you2he(goodid,doubanid):
    onegood= tablegood.find_one({"_id":ObjectId(goodid)})
    onedouban = getInfoById(goodid,doubanid)
    updateTheDoubanInfoToGood(onegood,onedouban)


def catchTop100():
    try:
        searchBack = urllib2.urlopen("http://api.douban.com/v2/movie/top250?start=0&count=100&apikey="+apikey).read()
        back = json.loads(searchBack)
        print back.get('subjects')
        if back and back.get('subjects'):
            savedb = {"pname":"top100","day":today,"plist":back['subjects']}
            indbtop = tabledlist.find_one({"pname":"top100","day":today})
            if indbtop:
                savedb['_id']=indbtop['_id']
            tabledlist.save(savedb)
            print 'sucess'
    except:
        pass

if __name__ == '__main__':
    if len(sys.argv) <= 1 :
        print "input argv  > 1  : goself(minutes) | seedm(minutes) | iseedm(minutes) | top100 |  you2he(goodid,doubanid) "
    else:     
        print 'start'
        if sys.argv[1] == "goself":
            if len(sys.argv) > 2:
                mins = int(sys.argv[2])
            else:
                muns = 60*24*30
            goself(mins)

        if sys.argv[1] == "seedm":
            if len(sys.argv) > 2:
                mins = int(sys.argv[2])
            else:
                mins = 60*24*30
            seedm(mins)

        if sys.argv[1] == "iseedm":
            if len(sys.argv) > 2:
                mins = int(sys.argv[2])
            else:
                mins = 60*24*30
            iseedm(mins)
        if sys.argv[1] == "top100":
            catchTop100()
        if sys.argv[1] == "you2he":
            if len(sys.argv) > 3:
                goodid = sys.argv[2]
                doubanid = sys.argv[3]
                you2he(goodid,doubanid)

        print 'end'

