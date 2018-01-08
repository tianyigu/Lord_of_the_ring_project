
from scrapy import Spider, Request
from lotr.items import LotrItem


class LotrSpider(Spider):
	name = 'lotr'
	allowed_urls = ['http://lotr.wikia.com']
	start_urls = ['http://lotr.wikia.com/wiki/Category:Characters']

	def parse(self, response):
		url_list = response.xpath('//div [@id="mw-pages"]/div[1]/table/tbody/tr/td[1]/ul/li[1]/a/@href').extract()
		url_list = ['http://lotr.wikia.com' + url for url in url_list]

		for url in url_list:
			yield Request(url, callback = self.parse_top)

	def parse_top(self,response):
		app_list = response.xpath('//div[@class="cover"]/a/@href').extract()
		app_list = ['https://play.google.com' + url for url in app_list]

		top_list = response.xpath('//div[@class = "cluster-heading"]/h2/text()').extract_first()

		for url in app_list:
			yield Request(url, callback=self.parse_app, meta={'top_list':top_list})


	def parse_app(self,response):
		top_list = response.meta['top_list']
		app_name = response.xpath('//div[@class="id-app-title"]/text()').extract_first()
		company_name = response.xpath('//a[@class="document-subtitle primary"]/span/text()').extract_first()

		reviews = response.xpath('//div[@class="single-review"]')
		for review in reviews:
			raw_review = review.xpath('.//div[@class="review-body with-review-wrapper"]/text()').extract()
			raw_review = ''.join(raw_review).strip()

			item = GooglePlayItem()
			item['content'] = raw_review
			item['app_name'] = app_name
			item['company_name'] = company_name
			item['top_list'] = top_list

			yield item
			//*[@id="mw-pages"]/div[1]/table/tbody/tr/td[1]/ul/li[1]/a