# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exceptions import DropItem
import os
import errno
import json

class NhkEasyNewsPipeline:
    def __init__(self):
        self.exporters = {}
        self.files = []
        self.crawled = {} # dictionary with 'yyyy-mm-dd' key and value of a set of all news_id of that day

    def read_archive(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                data = json.loads(line)
                try:
                    self.crawled[data['date']].add(data['news_id'])
                except KeyError:
                    self.crawled[data['date']] = {data['news_id']}

    def process_item(self, item, spider):
        if item['news_id'] == '-1':
            raise DropItem('Not in correct format')
        yyyymm = item['date'][0:7]
        if yyyymm not in self.exporters:
            file_name = './../result/output-'+ yyyymm + '.jl'
            if os.path.exists(os.path.dirname(file_name)):
                if os.path.exists(file_name):
                    self.read_archive(file_name)    # read in archived ids for later dropping
            else:
                try:    
                    os.makedirs(os.path.dirname(file_name)) # create dir for storing archive
                    self.crawled[yyyymm] = {} 
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
            output_file = open(file_name, 'ab+') # create or append
            self.files.append(output_file)
            self.exporters[yyyymm] = JsonLinesItemExporter(output_file, ensure_ascii=False)

        if item['date'] in self.crawled and item['news_id'] in self.crawled[item['date']]:
            raise DropItem(f'News item {item["news_id"]} is crawled already')
        else:
            self.exporters[yyyymm].export_item(item)
            try:
                self.crawled[item['date']].add(item['news_id'])
            except KeyError:
                self.crawled[item['date']] = {item['news_id']}
            return item

    def close_spider(self, spider):
        for file in self.files:
            file.close()
