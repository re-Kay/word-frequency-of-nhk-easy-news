from nhk_easy_news.items import NhkEasyNewsItem
from nhk_easy_news.loaders import NhkEasyNewsItemLoader
import scrapy
import json

class NhkEasyNewsSpider(scrapy.Spider):
    name = 'nhk_easy_news'
    allowed_domains = ['www3.nhk.or.jp']
    start_urls = ['https://www3.nhk.or.jp/news/easy/']
    prefix_url = 'https://www3.nhk.or.jp/news/easy/'

    def start_requests(self):
        news_list_url = 'https://www3.nhk.or.jp/news/easy/news-list.json'
        yield scrapy.Request(news_list_url, callback=self.get_news_lists)

    def convert_news_url(self, id):
        return self.prefix_url + id + '/' + id + '.html'

    def get_news_lists(self, response):
        data = json.loads(response.text)
        achieves = data[0]
        for achieve_day in achieves:
            for news in achieves[achieve_day]:
                news_url = self.convert_news_url(news['news_id'])
                yield scrapy.Request(news_url, callback=self.parse_article, meta={'date':achieve_day, 'id':news['news_id']})

    def parse_article(self, response):
        news_item_loader = NhkEasyNewsItemLoader(item=NhkEasyNewsItem(), response=response)
        news_item_loader.add_xpath('title', '//h1[@class="article-main__title"]/descendant::text()[not(parent::rt)]')
        news_item_loader.add_xpath('article', '//div[@class="article-main__body article-body"]/descendant::text()[not(parent::rt)]')
        news_item_loader.add_value('date', response.meta['date'])
        news_item_loader.add_value('news_id', response.meta['id'])
        yield news_item_loader.load_item()

        



