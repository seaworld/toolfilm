# Scrapy settings for catchfilm project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'catchfilm'

SPIDER_MODULES = ['catchfilm.spiders']
NEWSPIDER_MODULE = 'catchfilm.spiders'
IMAGES_STORE = '/data/dysoso/pic/'
IMAGES_EXPIRES=365
IMAGES_THUMBS = {
    'small': (128, 183),
}

LOG_FILE='/home/ttpod/scrapy.log'
LOG_LEVEL='INFO'

ITEM_PIPELINES = [
    'scrapy.contrib.pipeline.images.ImagesPipeline',
    'catchfilm.pipelines.BasePipeline',
]

DOWNLOADER_MIDDLEWARES = {
    #'catchfilm.downloader.A2tuccDownloader': 1,
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
