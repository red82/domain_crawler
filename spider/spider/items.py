# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DomainItem(Item):
    domain = Field()
    words_in_domainname = Field()
    title = Field()
    date_creation = Field()
    web_age = Field()
    ip_address = Field()
    ip_geolocation = Field()


class WhoisItem(Item):
    domain = Field()
    nserver = Field()
    state = Field()
    org = Field()
    registrar = Field()
    admin_contact = Field()
    created = Field()
    paid_till = Field()
    free_date = Field()
    source = Field()
