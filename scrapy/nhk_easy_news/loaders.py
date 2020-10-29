from itemloaders.processors import TakeFirst, Join, MapCompose
from scrapy.loader import ItemLoader

class NhkEasyNewsItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    title_out = Join('')
    article_out = Join('')