#coding=utf8
from time import sleep
import urllib2
import datetime

__author__ = 'wan'

from sinaweibopy import weibo
from pymongo import MongoClient


app_key= '472611526'
app_secret = '100bdfd52821e3953058903afb227d76'

#code ='ab5264a79e6781cfa9cc61fb9f2003cb'

access_token ='2.00lRFKDE0YqBzVedaa37d6eeSgsJXD'
expires_in=1394650801

client = weibo.APIClient(app_key,app_secret,redirect_uri="http://dysoso.com/weiboback")
#url = client.get_authorize_url()
#print url

#r = client.request_access_token(code)
#access_token = r.access_token
#expires_in = r.expires_in
#print access_token,expires_in
client.set_access_token(access_token, expires_in)


oldTime = datetime.datetime.now()-datetime.timedelta(hours=2)

mclient = MongoClient()
db = mclient["dysoso"]
tabledouban = db.douban
tablefilm = db.film

films = tablefilm.find({"updatetime":{"$gte":oldTime}})
for onefilm in films:
    if tabledouban.find_one({"title":{"$regex":onefilm.get("title")[0]}}):
	try:
	    weibotxt = u'《'+onefilm.get("title")[0]+u'》电影下载，由 ' + onefilm.get('fromtype')+u' 提供，http://dysoso.com/dy/'+unicode(onefilm.get('_id'))+u'.html'
            #print client.statuses.upload.post(status=weibotxt , pic=urllib2.urlopen('http://dysoso.com/static/film-pic/%s'%onefilm.get('images')[0].get('path')))
            print client.statuses.upload.post(status=weibotxt , pic=open('/data/dysoso/pic/%s'%onefilm.get('images')[0].get('path'),'rb'))
	    sleep(5)
	except Exception,e:
	    print e
