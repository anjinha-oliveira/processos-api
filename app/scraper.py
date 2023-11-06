import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "consltar_por_cnj"
    start_urls = ['https://www2.tjal.jus.br/cpopg/open.do']