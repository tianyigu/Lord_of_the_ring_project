
from scrapy import Spider, Request
from lotr.items import LotrItem


class LotrSpider(Spider):
	name = 'lotr'
	allowed_urls = ['http://lotr.wikia.com']
	start_urls = ['http://lotr.wikia.com/wiki/Category:Characters?page='+ str(i) for i in range(1,6)]

	def parse(self, response):
		url_list = response.xpath('//td[@width="33.3%"]/ul/li/a/@href').extract()
		url_list = ['http://lotr.wikia.com' + url for url in url_list]

		cha_name = response.xpath("//td[@width='33.3%']/ul/li/a/text()").extract()
		for i in range(len(cha_name)):
		#for url in url_list:
		 	yield Request(url_list[i], callback = self.parse_app, meta={'name':cha_name[i]})


	def parse_app(self,response):
		cha_name = response.meta['name']
		race_ = "Unknow"
		gender_ = "Unknow"
		spouse_ = "Unknow"
		hair_ = "Unknow"
		death_ = "Unknow"
		birth_ = "Unknow"
		height_ = "Unknow"
		realm_ = "Unknow"
		manu = response.xpath('//section[@class="pi-item pi-group pi-border-color"]/div')
		
		
		for i in manu:
			a = i.xpath(".//h3/text()").extract()
			if a == ["Race"]:
				race_ = i.xpath(".//div/a/text()").extract()
			elif a == ["Gender"]:
				gender_ = i.xpath(".//div/text()").extract()
			elif a == ["Spouse"]:
				spouse_ = i.xpath(".//*/text()").extract()[1:len(i.xpath(".//*/text()").extract())]
			elif a == ["Hair"]:
				hair_ = i.xpath(".//div/text()").extract()
			elif a == ["Death"]:
				death_ = i.xpath(".//*/text()").extract()[1:len(i.xpath(".//*/text()").extract())]
			elif a == ["Birth"]:
				birth_ = i.xpath(".//*/text()").extract()[1:len(i.xpath(".//*/text()").extract())]
			elif a == ["Height"]:
				height_ = i.xpath(".//div/text()").extract()
			elif a == ["Realms"]:
				realm_ = i.xpath(".//div/a/text()").extract()
	
		item = LotrItem()
		item['name'] = cha_name
		item['race'] = race_
		item["gender"] = gender_
		item['spouse'] = spouse_
		item['hair'] = hair_
		item['birth'] = birth_
		item['death'] = death_
		item['height'] = height_
		item['realm'] = realm_
		yield item

	

