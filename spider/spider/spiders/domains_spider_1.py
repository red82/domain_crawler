# 2017.03.27 13:16:33 EEST
#Embedded file name: /Users/andrey/Documents/AlterEgoParsing/domain_crawler/spider/spider/spiders/domains_spider_1.py
from spider.items import DomainItem, RegistrantItem, WhoisItem
from spider.settings import URL_WEBUI
import requests
import scrapy
import sys
DB_API = u'/db'

class CustomException(Exception):
    pass


class DomainsSpider(scrapy.Spider):
    name = 'domain_spider_1'
    allowed_domains = ['domainbigdata.com']
    start_urls = ['http://domainbigdata.com/']

    @staticmethod
    def convert_to_list(self, string):
        pass

    @staticmethod
    def splitter(string):
        return string.split('\n')

    def parse(self, response):
        url = ''.join(['http://', URL_WEBUI, DB_API])
        try:
            response = requests.get(url)
        except Exception:
            print "Couldn't send request to server."
            sys.exit()

        if response.status_code != 200:
            print 'Exception!!! Status code is %s' % response.status_code
            sys.exit()
        domain_name_list = response.json()['domains']
        domain_name_list = self.splitter(domain_name_list)
        for domain_name in domain_name_list:
            url = ''.join([self.start_urls[0], domain_name])
            yield scrapy.Request(url=url, method='GET', callback=self.after_get)

    def after_get(self, response):
        dom_item = DomainItem()
        reg_item = RegistrantItem()
        who_item = WhoisItem()
        item = dict()
        item['dom_item'] = dom_item
        item['reg_item'] = reg_item
        item['who_item'] = who_item
        data = response.xpath('//table[@class="websiteglobalstats em-td2 trhov"]')
        try:
            dom_item['domain'] = data.xpath('//tr[@id="tr1"]/td[2]/text()').extract()[0]
            dom_item['words_in_domainname'] = data.xpath('//tr[@id="trWordsInDomainName"]/td[2]/text()').extract()[0]
            dom_item['title'] = data.xpath('//tr[@id="trTitle"]/td[2]/text()').extract()[0]
            dom_item['date_creation'] = data.xpath('//tr[@id="trDateCreation"]/td[2]/text()').extract()[0]
            dom_item['web_age'] = data.xpath('//tr[@id="trWebAge"]/td[2]/text()').extract()[0]
            dom_item['ip_address'] = data.xpath('//tr[@id="trIP"]/td[2]/a/text()').extract()[0]
            dom_item['ip_geolocation'] = data.xpath('//tr[@id="trIPGeolocation"]/td[2]/img/@alt').extract()[0]
        except IndexError:
            print 'DOM object was changed in bigdomaindata.com'
            sys.exit()

        data = response.xpath('//table[@class="websiteglobalstats em-td2 trhov"]')
        try:
            reg_item['name'] = data.xpath('//tr[@id="trRegistrantName"]/td[2]/a/text()').extract()[0]
            reg_item['organization'] = data.xpath('//tr[@id="MainMaster_trRegistrantOrganization"]/td[2]/a/text()').extract()[0]
            reg_item['email'] = data.xpath('//tr[@id="trRegistrantEmail"]/td[2]/a/text()').extract()[0]
            reg_item['country'] = data.xpath('//tr[@id="trRegistrantCountry"]/td[2]/img/@alt').extract()[0]
            reg_item['private'] = data[1].xpath('//table[@class="websiteglobalstats em-td2 trhov"]/tr/td[2]/text()').extract()[-1]
        except IndexError:
            print 'DOM object was changed in bigdomaindata.com'
            sys.exit()

        yield item
