import scrapy
import logging
from wodscrape.items import WodscrapeItem 

logger = logging.getLogger()

class BearFlagSpider(scrapy.Spider):
  name = "bearflag_scraper"
  allowed_domains = ["bearflagcrossfit.com"]
  start_urls = ["http://www.bearflagcrossfit.com/wod-blog"]

  def parse(self, response):
    for i in range(2, 34):
      URI = "http://www.bearflagcrossfit.com/wod-blog/page/" + str(i) + "/"
      yield scrapy.Request(URI, callback = self.get_info_url)

  def get_info_url(self, response):
    for sel in response.xpath('//h2[@class="blog-title"]'):
      for l in sel.xpath('a/@href').extract():
        yield scrapy.Request(l, callback = self.save_wod)

  def save_wod(self, response):
    section_tag = '//div[@class="blog-content-wrapper"]'
    for content in response.xpath(section_tag).extract():
      item = WodscrapeItem()
      item['url'] = response.url
      item['content_html'] = content
      yield item
