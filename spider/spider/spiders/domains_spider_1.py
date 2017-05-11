# 2017.03.27 13:16:33 EEST
#Embedded file name: /Users/andrey/Documents/AlterEgoParsing/domain_crawler/spider/spider/spiders/domains_spider_1.py
from spider.items import DomainItem, RegistrantItem, WhoisItem1, WhoisItem2
from spider.settings import URL_WEBUI

import re
import requests
import scrapy
import sys
import time


DB_API = u'/db'
DB_WHOIS1 = u'whois1'
DB_WHOIS2 = u'whois2'

PATTERN_NO = r'^(<td\s[\w\d\s.=\'\"\>]+)no'


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

    @staticmethod
    def connector(dct):
        return [', '.join(dct[x]) for x in dct]

    @staticmethod
    def chunks(l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

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

        for domain_name_chunk in self.chunks(domain_name_list, 20):
            time.sleep(3)
            for domain_name in domain_name_chunk:
                url = ''.join([self.start_urls[0], domain_name])
                request = scrapy.Request(url=url, method='GET', callback=self.after_get)
                request.meta['domain_name'] = domain_name

                yield request

    def after_get(self, response):
        dom_item = DomainItem()
        reg_item = RegistrantItem()

        item = dict()
        item['dom_item'] = dom_item
        item['reg_item'] = reg_item

        data = response.xpath('//table[@class="websiteglobalstats em-td2 trhov"]')

        dom_item['domain_name'] = response.meta['domain_name']
        dom_item['domain'] = data.xpath('//tr[@id="tr1"]/td[2]/text()').extract_first()
        dom_item['words_in_domainname'] = data.xpath('//tr[@id="trWordsInDomainName"]/td[2]/text()').extract_first()
        dom_item['title'] = data.xpath('//tr[@id="trTitle"]/td[2]/text()').extract_first()
        dom_item['date_creation'] = data.xpath('//tr[@id="trDateCreation"]/td[2]/text()').extract_first()
        dom_item['web_age'] = data.xpath('//tr[@id="trWebAge"]/td[2]/text()').extract_first()
        dom_item['ip_address'] = data.xpath('//tr[@id="trIP"]/td[2]/a/text()').extract_first()
        dom_item['ip_geolocation'] = data.xpath('//tr[@id="trIPGeolocation"]/td[2]/img/@alt').extract_first()

        data = response.xpath('//table[@class="websiteglobalstats em-td2 trhov"]')

        reg_item['name'] = data.xpath('//tr[@id="trRegistrantName"]/td[2]/a/text()').extract_first()
        reg_item['organization'] = data.xpath('//tr[@id="MainMaster_trRegistrantOrganization"]/td[2]/a/text()').extract_first()
        reg_item['email'] = data.xpath('//tr[@id="trRegistrantEmail"]/td[2]/a/text()').extract_first()
        reg_item['country'] = data.xpath('//tr[@id="trRegistrantCountry"]/td[2]/img/@alt').extract_first()

        try:
            private_field = data[1].xpath('//table[@class="websiteglobalstats em-td2 trhov"]/tr/td[2]').extract()
        except Exception as e:
            print "Couldn't get data from 'Private' field"
            private_field = []

        if len(private_field):
            private_field = private_field[-1]
            m = re.match(PATTERN_NO, private_field)
            if m:
                reg_item['private'] = 'no'
            else:
                reg_item['private'] = 'yes'
        else:
            reg_item['private'] = None

        data = response.xpath('//div[@class="col-md-12 pd5"]')
        domain_field = data.re(r'domain:\s*([A-Za-z0-9-]+)')

        if domain_field:
            dom_item['table'] = DB_WHOIS1

            who_item1 = WhoisItem1()
            item['who_item1'] = who_item1

            nserver = [d[:-1] for d in data.re(r'nserver:\s*([A-Za-z0-9-.]+)')]
            who_item1['nserver'] = ', '.join(nserver)
            state = data.re('state:\s*([\w\s,]*)<br>')
            who_item1['state'] = ', '.join(state)
            org = data.re('org:\s*([\w\s,.]*)<br>')
            who_item1['org'] = ', '.join(org)
            who_item1['registrar'] = data.re('registrar:\s*([-a-zA-Z0-9]+)')
            who_item1['admin_contact'] = data.re('admin-contact:\s*(.*?)<br>')
            who_item1['created'] = data.re('created:\s*(\d{2,4}\.\d{2,4}\.\d{2,4})<br>')
            who_item1['paid_till'] = data.re('paid-till:\s*(\d{2,4}\.\d{2,4}\.\d{2,4})<br>')
            who_item1['free_date'] = data.re('free-date:\s*(\d{2,4}\.\d{2,4}\.\d{2,4})<br>')
            who_item1['source'] = data.re('source:\s*(\w+)<br>')

            for who_item in who_item1:
                who_item1[who_item] = ', '.join(who_item1[who_item])
        else:
            dom_item['table'] = DB_WHOIS2

            who_item2 = WhoisItem2()
            item['who_item2'] = who_item2

            who_item2['domain_name'] = data.re('Domain Name:\s*([-a-zA-Z0-9]+)')
            who_item2['registry_domain_id'] = data.re('Registry Domain ID:\s*([_-a-zA-Z0-9]+)')
            who_item2['registrar_whois_server'] = data.re('Registrar WHOIS Server:\s*([-a-zA-Z0-9.]+)')

            registrar_url = data.re('Registrar URL:\s*((https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?))')
            if len(registrar_url):
                who_item2['registrar_url'] = registrar_url[0:1]
            else:
                who_item2['registrar_url'] = []

            who_item2['updated_date'] = data.re('Updated Date:\s*([-a-zA-Z0-9.:]+)')
            who_item2['creation_date'] = data.re('Creation Date:\s*([-a-zA-Z0-9.:]+)')
            who_item2['registrar_registration_expiration_date'] = data.re('Registrar Registration Expiration Date: \s*([-a-zA-Z0-9.:]+)')
            who_item2['registrar'] = data.re('Registrar:\s*([a-zA-Z0-9.,\s]+)')
            who_item2['registrar_iana_id'] = data.re('Registrar IANA ID:\s*([0-9]+)')

            registrar_abuse_contact_email = data.re('Registrar Abuse Contact Email:\s*(([\w\._]+)*.(\(at\))([\w\_]+)*.([a-z]{2,6}\.?))')
            if len(registrar_abuse_contact_email):
                who_item2['registrar_abuse_contact_email'] = registrar_abuse_contact_email[0:1]
            else:
                who_item2['registrar_abuse_contact_email'] = []

            who_item2['registrar_abuse_contact_phone'] = data.re('Registrar Abuse Contact Phone:\s*([+0-9.]+)')
            who_item2['domain_status'] =  data.re('Domain Status:\s*([a-zA-Z0-9\s\(\.:\\\#\/)]+)')
            who_item2['registry_registrant_id'] = data.re('Registry Registrant ID:\s*([0-9]+)')
            who_item2['registrant_name'] = data.re('Registrant Name:\s*([a-zA-Z0-9\s]+)')
            who_item2['registrant_organization'] = data.re('Registrant Organization:\s*([a-zA-Z0-9\s]+)')
            who_item2['registrant_street'] = data.re('Registrant Street:\s*([a-zA-Z0-9\s]+)')
            who_item2['registrant_city'] = data.re('Registrant City:\s*([a-zA-Z\s]+)')
            who_item2['registrant_stateprovince'] = data.re('Registrant State/Province:\s*([a-zA-Z]+)')
            who_item2['registrant_postal_code'] = data.re('Registrant Postal Code:\s*([0-9]+)')
            who_item2['registrant_country'] = data.re('Registrant Country:\s*([a-zA-Z\s]+)')
            who_item2['registrant_phone'] = data.re('Registrant Phone:\s*([+0-9.]+)')
            who_item2['registrant_phone_ext'] = data.re('Registrant Phone Ext:\s*([+0-9.]+)')
            who_item2['registrant_fax'] = data.re('Registrant Fax:\s*([+0-9.]+)')
            who_item2['registrant_fax_ext'] = data.re('Registrant Fax Ext:\s*([+0-9.]+)')

            registrant_email = data.re('Registrant Email:\s*(([\w\._-]+)*.(\(at\))([\w\_]+)*.([a-z]{2,6}\.?))')
            if len(registrant_email):
                who_item2['registrant_email'] = registrant_email[0:1]
            else:
                who_item2['registrant_email'] = []

            who_item2['registry_admin_id'] = data.re('Registry Admin ID:\s*([0-9]+)')
            who_item2['admin_name'] = data.re('Admin Name:\s*([a-zA-Z0-9\s]+)')
            who_item2['admin_organization'] = data.re('Admin Organization:\s*([a-zA-Z0-9\s]+)')
            who_item2['admin_street'] = data.re('Admin Street:\s*([a-zA-Z0-9\s]+)')
            who_item2['admin_city'] = data.re('Admin City:\s*([a-zA-Z\s]+)')
            who_item2['admin_stateprovince'] = data.re('Admin State/Province:\s*([a-zA-Z]+)')
            who_item2['admin_postal_code'] = data.re('Admin Postal Code:\s*([0-9]+)')
            who_item2['admin_country'] = data.re('Admin Country:\s*([a-zA-Z\s]+)')
            who_item2['admin_phone'] = data.re('Admin Phone:\s*([+0-9.]+)')
            who_item2['admin_phone_ext'] = data.re('Admin Phone Ext:\s*([+0-9.]+)')
            who_item2['admin_fax'] = data.re('Admin Fax:\s*([+0-9.]+)')
            who_item2['admin_fax_ext'] = data.re('Admin Fax Ext:\s*([+0-9.]+)')

            admin_email = data.re('Admin Email:\s*(([\w\._-]+)*.(\(at\))([\w\_]+)*.([a-z]{2,6}\.?))')
            if len(admin_email):
                who_item2['admin_email'] = admin_email[0:1]
            else:
                who_item2['admin_email'] = []

            who_item2['registry_tech_id'] = data.re('Registry Tech ID:\s*([0-9]+)')
            who_item2['tech_name'] = data.re('Tech Name:\s*([a-zA-Z0-9\s]+)')
            who_item2['tech_organization'] = data.re('Tech Organization:\s*([a-zA-Z0-9\s]+)')
            who_item2['tech_street'] = data.re('Tech Street:\s*([a-zA-Z0-9\s]+)')
            who_item2['tech_city'] = data.re('Tech City:\s*([a-zA-Z\s]+)')
            who_item2['tech_stateprovince'] = data.re('Tech State/Province:\s*([a-zA-Z]+)')
            who_item2['tech_postal_code'] = data.re('Tech Postal Code:\s*([0-9]+)')
            who_item2['tech_country'] = data.re('Tech Country:\s*([a-zA-Z\s]+)')
            who_item2['tech_phone'] = data.re('Tech Phone:\s*([+0-9.]+)')
            who_item2['tech_phone_ext'] = data.re('Tech Phone Ext:\s*([+0-9.]+)')
            who_item2['tech_fax'] = data.re('Tech Fax:\s*([+0-9.]+)')
            who_item2['tech_fax_ext'] = data.re('Tech Fax Ext:\s*([+0-9.]+)')

            tech_email = data.re('Tech Email:\s*(([\w\._-]+)*.(\(at\))([\w\_]+)*.([a-z]{2,6}\.?))')
            if len(tech_email):
                who_item2['tech_email'] = tech_email[0:1]
            else:
                who_item2['tech_email'] = []

            who_item2['name_server'] = data.re('Name Server:\s*([-a-zA-Z0-9.]+)')
            who_item2['dnssec'] = data.re('DNSSEC:\s*([-a-zA-Z0-9]+)')

            for who_item in who_item2:
                who_item2[who_item] = ', '.join(who_item2[who_item])

        yield item
