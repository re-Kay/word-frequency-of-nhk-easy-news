# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from nhk_easy_news.exporters import NhkEasyNewsItemExporter
from pathlib import Path
import datetime

class NhkEasyNewsPipeline:
    def __init__(self):
        output_path = Path('./../result/').resolve()
        self.output_name = str(output_path) + '\\'+ 'output-'+ datetime.datetime.today().strftime('%y-%m-%d') + '.json'
        self.output_file = open(self.output_name, 'wb')

    def open_spider(self, spider):
        self.exporter = NhkEasyNewsItemExporter(self.output_file, ensure_ascii=False) # utf-8 encoding
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.output_file.close()

    def process_item(self, item, spider):
        # to do: check if item exists in last crawling
        self.exporter.export_item(item)
        return item
