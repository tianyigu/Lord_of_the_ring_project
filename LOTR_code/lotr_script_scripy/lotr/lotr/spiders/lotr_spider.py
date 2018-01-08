
from scrapy import Spider, Request
from lotr.items import LotrItem


class LotrSpider(Spider):
	name = 'lotr'
	allowed_urls = ['http://www.ageofthering.com/']
	start_urls = ['http://www.ageofthering.com/atthemovies/']

	def parse(self, response):
		url_list = ['atthemovies/scripts/fellowshipoftheringscript.php','atthemovies/scripts/thetwotowersscript.php','atthemovies/scripts/returnofthekingscript.php']
		url_list = ['http://www.ageofthering.com/' + url for url in url_list]

		movie = ['The Fellowship of the Ring Movie Script','The Two Towers Movie Script','The Return of the King Movie Script']
		for i in range(3):
			yield Request(url_list[i], callback = self.parse_app, meta={'movie':movie[i]})


	def parse_app(self,response):
		urllist = response.xpath('//table[@id="AutoNumber5"or"AutoNumber3"][@border="2"]//*/a/@href').extract()[0:int(len(response.xpath('//table[@id="AutoNumber5"or"AutoNumber3"][@border="2"]//*/a/@href').extract())/2)]
		movie = response.meta['movie']
		#urllist = response.xpath('//table[@id="AutoNumber5" or "AutoNumber3"][@border="2"]//*/a/@href').extract()
		urllist = ['http://www.ageofthering.com/' + url for url in urllist]
		scene = response.xpath('//table[@id="AutoNumber4"][@border="2"]//*/a/text()').extract()
		for i in urllist:
			yield Request(i, callback = self.parse_word, meta={'movie':movie,'scene':scene})


	def parse_word(self,response):
		movie = response.meta['movie']
		scene = response.meta['scene']
		q = response.xpath('//table[@id="AutoNumber1"]/tr')
		char = ""
		dialog = ""
		for i in q:
			chara = i.xpath('.//td[@valign="top"]/text()').extract()
			if len(chara) != 0:
				if ":" in chara[0]:
					char = i.xpath('.//td[@valign="top"]/text()').extract()
					dialog = i.xpath('.//td/text()').extract()[1:]



					item = LotrItem()
					item['char'] = char
					item['dialog'] = dialog
					item["movie"] = movie
					#item['scene'] = scene
					yield item
		#q[6].xpath('.//td[@valign="top"]/text()').extract()

	 	# if manu:
		 # 	for i in manu:
		 # 		a = i.xpath(".//h3/text()").extract()
		 # 		if a == ["Race"]:
		 # 			race_ = i.xpath(".//div/a/text()").extract()
		 # 		elif a == ["Gender"]:
		 # 			gender_ = i.xpath(".//div/text()").extract()
		 # 		elif a == ["Spouse"]:
		 # 			spouse_ = i.xpath(".//*/text()").extract()[1:len(i.xpath(".//*/text()").extract())]
		 # 		elif a == ["Hair"]:
		 # 			hair_ = i.xpath(".//div/text()").extract()
		 # 		elif a == ["Death"]:
		 # 			death_ = i.xpath(".//*/text()").extract()[1:len(i.xpath(".//*/text()").extract())]
		 # 		elif a == ["Birth"]:
		 # 			birth_ = i.xpath(".//*/text()").extract()[1:len(i.xpath(".//*/text()").extract())]
		 # 		elif a == ["Height"]:
		 # 			height_ = i.xpath(".//div/text()").extract()
		 # 		elif a == ["Realms"]:
		 # 			realm_ = i.xpath(".//div/a/text()").extract()
	 	
	 	# item = LotrItem()
	 	# item['name'] = cha_name
	 	# item['race'] = race_
	 	# item["gender"] = gender_
	 	# item['spouse'] = spouse_
	 	# item['hair'] = hair_
	 	# item['birth'] = birth_
	 	# item['death'] = death_
	 	# item['height'] = height_
	 	# item['realm'] = realm_
	 	# yield item

	

