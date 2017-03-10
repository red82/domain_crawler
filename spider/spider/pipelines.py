# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import DomainItem, WhoisItem
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session

import os


Base = declarative_base()


class DomainTable(Base):
    __tablename__ = 'domain'
    id = Column(Integer, primary_key=True)
    domain = Column(String)
    words_in_domainname = Column(String)
    title = Column(String)
    date_creation = Column(String)
    web_age = Column(String)
    ip_address = Column(String)
    ip_geolocation = Column(String)

    def __init__(self, domain, words_in_domain, title, date_creation, web_age, ip_address, ip_geolocation):
        self.domain = domain
        self.words_in_domainname = words_in_domain
        self.title = title
        self.date_creation = date_creation
        self.web_age = web_age
        self.ip_address = ip_address
        self.ip_geolocation = ip_geolocation

    def __repr__(self):
        return 'Data %s %s %s %s %s %s %s' % (self.domain,
                                              self.words_in_domainname,
                                              self.title,
                                              self.date_creation,
                                              self.web_age,
                                              self.ip_address,
                                              self.ip_geolocation)


class WhoisTable(Base):
    __tablename__ = 'whois'
    id = Column(Integer, primary_key=True)
    domain = Column(String)
    nserver = Column(String)
    state = Column(String)
    org = Column(String)
    registrar = Column(String)
    admin_contact = Column(String)
    created = Column(String)
    paid_till = Column(String)
    free_date = Column(String)
    source = Column(String)

    def __init__(self, domain, nserver, state, org, registrar, admin_contact, created, paid_till, free_date, source):
        self.domain = domain
        self.nserver = nserver
        self.state = state
        self.org = org
        self.registrar = registrar
        self.admin_contact = admin_contact
        self.created = created
        self.paid_till = paid_till
        self.free_date = free_date
        self.source = source

    def __repr__(self):
        return 'Data %s %s %s %s %s %s %s %s %s %s' % (self.domain,
                                                       self.nserver,
                                                       self.state,
                                                       self.org,
                                                       self.registrar,
                                                       self.admin_contact,
                                                       self.created,
                                                       self.paid_till,
                                                       self.free_date,
                                                       self.source)


class SpiderPipeline(object):
    def __init__(self):
        # import pdb;pdb.set_trace()
        basename = 'spider.db'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)

    def process_item(self, item, spider):
        dom_item = item['dom_item']
        who_item = item['who_item']

        dt = DomainTable(dom_item['domain'], dom_item['words_in_domainname'],
                         dom_item['title'], dom_item['date_creation'],
                         dom_item['web_age'], dom_item['ip_address'],
                         dom_item['ip_geolocation'])

        self.session.add(dt)

        wt = WhoisTable(who_item['domain'], who_item['nserver'], who_item['state'],
                            who_item['org'], who_item['registrar'], who_item['admin_contact'],
                            who_item['created'], who_item['paid_till'], who_item['free_date'],
                            who_item['source'])

        self.session.add(wt)

        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)