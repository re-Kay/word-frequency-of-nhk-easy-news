from scrapy.exporters import JsonItemExporter

class NhkEasyNewsItemExporter(JsonItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(file, **kwargs)
        
        # item to be buffered for sorting (less than 100 item)
        self.output_list = []

    def export_item(self, item):
        self.output_list.append(item)

    def finish_exporting(self):
        # sort by news_id
        self.output_list.sort(key=lambda x: x['news_id'])
        
        for item in self.output_list:
            super().export_item(item)
        super().finish_exporting()