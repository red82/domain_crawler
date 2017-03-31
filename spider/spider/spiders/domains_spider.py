# -*- coding:utf8 -*-
from spider.items import DomainItem, WhoisItem1
# from scrapy.utils.response import open_in_browser
import scrapy


class DomainsSpider(scrapy.Spider):
    name = 'domain_spider'
    allowed_domains = ['domainbigdata.com']
    start_urls = ['http://domainbigdata.com/']

    def parse(self, response):
        url = ''.join([self.start_urls[0], 'www.google-analytics.com'])
        return [scrapy.Request(url=url, method='GET', callback=self.after_get)]

    def after_get(self, response):
        dom_item = DomainItem()
        who_item = WhoisItem1()

        data = response.xpath('//table[@class="websiteglobalstats em-td2 trhov"]')

        dom_item['domain'] = data.xpath('//tr[@id="tr1"]/td[2]/text()').extract()[0]
        dom_item['words_in_domainname'] = data.xpath('//tr[@id="trWordsInDomainName"]/td[2]/text()').extract()[0]
        dom_item['title'] = data.xpath('//tr[@id="trTitle"]/td[2]/text()').extract()[0]
        dom_item['date_creation'] = data.xpath('//tr[@id="trDateCreation"]/td[2]/text()').extract()[0]
        dom_item['web_age'] = data.xpath('//tr[@id="trWebAge"]/td[2]/text()').extract()[0]
        dom_item['ip_address'] = data.xpath('//tr[@id="trIP"]/td[2]/a/text()').extract()[0]

        dom_item['ip_geolocation'] = data.xpath('//tr[@id="trIPGeolocation"]/td[2]/img/@alt').extract()[0]

        data = response.xpath('//div[@class="col-md-12 pd5"]')

        who_item['domain'] = data.re(r'domain:\s*([A-Za-z0-9-]+)')
        if not who_item['domain']:
            who_item['domain'] = data.re(r'Domain Name:\s*([A-Za-z0-9-]+)')[0]
        else:
            who_item['domain'] = who_item['domain'][0]

        nserver = [d[:-1] for d in data.re(r'nserver:\s*([A-Za-z0-9-.]+)')]
        who_item['nserver'] = ', '.join(nserver)
        state = data.re('state:\s*([\w\s,]*)<br>')
        who_item['state'] = ', '.join(state)
        org = data.re('org:\s*([\w\s,.]*)<br>')
        who_item['org'] = ', '.join(org)
        who_item['registrar'] = data.re('registrar:\s*([-a-zA-Z0-9]+)')[0]
        who_item['admin_contact'] = data.re('admin-contact:\s*(.*?)<br>')[0]
        who_item['created'] = data.re('created:\s*(\d{2,4}\.\d{2,4}\.\d{2,4})<br>')[0]
        who_item['paid_till'] = data.re('paid-till:\s*(\d{2,4}\.\d{2,4}\.\d{2,4})<br>')[0]
        who_item['free_date'] = data.re('free-date:\s*(\d{2,4}\.\d{2,4}\.\d{2,4})<br>')[0]
        who_item['source'] = data.re('source:\s*(\w+)<br>')[0]

        item = dict()
        item['dom_item'] = dom_item
        item['who_item'] = who_item

        yield item
