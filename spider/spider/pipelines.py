# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship, backref

import os


Base = declarative_base()


class DomainTable(Base):
    __tablename__ = 'domain'
    id = Column(Integer, primary_key=True)
    domain_name = Column(String)
    domain = Column(String)
    words_in_domainname = Column(String)
    title = Column(String)
    date_creation = Column(String)
    web_age = Column(String)
    ip_address = Column(String)
    ip_geolocation = Column(String)
    table = Column(String)

    registrant_id = Column(Integer, ForeignKey('registrant.id'))

    registrant = relationship('RegistrantTable',  back_populates='domain')
    whois1 = relationship('WhoisTable1', back_populates='domain_table')
    whois2 = relationship('WhoisTable2', back_populates='domain_table')

    def __init__(self, domain_name, domain, words_in_domain, title,
                 date_creation, web_age, ip_address, ip_geolocation, table):
        self.domain_name = domain_name
        self.domain = domain
        self.words_in_domainname = words_in_domain
        self.title = title
        self.date_creation = date_creation
        self.web_age = web_age
        self.ip_address = ip_address
        self.ip_geolocation = ip_geolocation
        self.table = table

    def __repr__(self):
        return 'Data %s %s %s %s %s %s %s %s %s' % (self.domain_name,
                                                       self.domain,
                                                       self.words_in_domainname,
                                                       self.title,
                                                       self.date_creation,
                                                       self.web_age,
                                                       self.ip_address,
                                                       self.ip_geolocation,
                                                       self.table)


class RegistrantTable(Base):
    __tablename__ = 'registrant'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    organization = Column(String)
    email = Column(String)
    country = Column(String)
    private = Column(String)

    domain = relationship('DomainTable', back_populates='registrant')

    def __init__(self, name, organization, email, country, private):
        self.name = name
        self.organization = organization
        self.email = email
        self.country = country
        self.private = private

    def __repr__(self):
        return 'Data %s %s %s %s %s' % (self.name,
                                        self.organization,
                                        self.email,
                                        self.country,
                                        self.private)


class WhoisTable1(Base):
    __tablename__ = 'whois1'
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

    domain_table_id = Column(Integer, ForeignKey('domain.id'))
    domain_table = relationship('DomainTable', uselist=False, back_populates='whois1')

    def __init__(self, domain, nserver, state, org, registrar, admin_contact,
                 created, paid_till, free_date, source):
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


class WhoisTable2(Base):
    __tablename__ = 'whois2'
    id = Column(Integer, primary_key=True)
    domain_name = Column(String)
    registry_domain_id = Column(String)
    registrar_whois_server = Column(String)
    registrar_url = Column(String)
    updated_date = Column(String)
    creation_date = Column(String)
    registrar_registration_expiration_date = Column(String)
    registrar = Column(String)
    registrar_iana_id = Column(String)
    registrar_abuse_contact_email = Column(String)
    registrar_abuse_contact_phone = Column(String)
    domain_status = Column(String)
    registry_registrant_id = Column(String)
    registrant_name = Column(String)
    registrant_organization = Column(String)
    registrant_street = Column(String)
    registrant_city = Column(String)
    registrant_stateprovince = Column(String)
    registrant_postal_code = Column(String)
    registrant_country = Column(String)
    registrant_phone = Column(String)
    registrant_phone_ext = Column(String)
    registrant_fax = Column(String)
    registrant_fax_ext = Column(String)
    registrant_email = Column(String)
    registry_admin_id = Column(String)
    admin_name = Column(String)
    admin_organization = Column(String)
    admin_street = Column(String)
    admin_city = Column(String)
    admin_stateprovince = Column(String)
    admin_postal_code = Column(String)
    admin_country = Column(String)
    admin_phone = Column(String)
    admin_phone_ext = Column(String)
    admin_fax = Column(String)
    admin_fax_ext = Column(String)
    admin_email = Column(String)
    registry_tech_id = Column(String)
    tech_name = Column(String)
    tech_organization = Column(String)
    tech_street = Column(String)
    tech_city = Column(String)
    tech_stateprovince = Column(String)
    tech_postal_code = Column(String)
    tech_country = Column(String)
    tech_phone = Column(String)
    tech_phone_ext = Column(String)
    tech_fax = Column(String)
    tech_fax_ext = Column(String)
    tech_email = Column(String)
    name_server = Column(String)
    dnssec = Column(String)

    domain_table_id = Column(Integer, ForeignKey('domain.id'))
    domain_table = relationship('DomainTable', uselist=False, back_populates='whois2')

    def __init__(self,
            domain_name,
            registry_domain_id,
            registrar_whois_server,
            registrar_url,
            updated_date,
            creation_date,
            registrar_registration_expiration_date,
            registrar,
            registrar_iana_id,
            registrar_abuse_contact_email,
            registrar_abuse_contact_phone,
            domain_status,
            registry_registrant_id,
            registrant_name,
            registrant_organization,
            registrant_street,
            registrant_city,
            registrant_stateprovince,
            registrant_postal_code,
            registrant_country,
            registrant_phone,
            registrant_phone_ext,
            registrant_fax,
            registrant_fax_ext,
            registrant_email,
            registry_admin_id,
            admin_name,
            admin_organization,
            admin_street,
            admin_city,
            admin_stateprovince,
            admin_postal_code,
            admin_country,
            admin_phone,
            admin_phone_ext,
            admin_fax,
            admin_fax_ext,
            admin_email,
            registry_tech_id,
            tech_name,
            tech_organization,
            tech_street,
            tech_city,
            tech_stateprovince,
            tech_postal_code,
            tech_country,
            tech_phone,
            tech_phone_ext,
            tech_fax,
            tech_fax_ext,
            tech_email,
            name_server,
            dnssec):
        self.domain_name = domain_name
        self.registry_domain_id = registry_domain_id
        self.registrar_whois_server = registrar_whois_server
        self.registrar_url = registrar_url
        self.updated_date = updated_date
        self.creation_date = creation_date
        self.registrar_registration_expiration_date = registrar_registration_expiration_date
        self.registrar = registrar
        self.registrar_iana_id = registrar_iana_id
        self.registrar_abuse_contact_email = registrar_abuse_contact_email
        self.registrar_abuse_contact_phone = registrar_abuse_contact_phone
        self.domain_status = domain_status
        self.registry_registrant_id = registry_registrant_id
        self.registrant_name = registrant_name
        self.registrant_organization = registrant_organization
        self.registrant_street = registrant_street
        self.registrant_city = registrant_city
        self.registrant_stateprovince = registrant_stateprovince
        self.registrant_postal_code = registrant_postal_code
        self.registrant_country = registrant_country
        self.registrant_phone = registrant_phone
        self.registrant_phone_ext = registrant_phone_ext
        self.registrant_fax = registrant_fax
        self.registrant_fax_ext = registrant_fax_ext
        self.registrant_email = registrant_email
        self.registry_admin_id = registry_admin_id
        self.admin_name = admin_name
        self.admin_organization = admin_organization
        self.admin_street = admin_street
        self.admin_city = admin_city
        self.admin_stateprovince = admin_stateprovince
        self.admin_postal_code = admin_postal_code
        self.admin_country = admin_country
        self.admin_phone = admin_phone
        self.admin_phone_ext = admin_phone_ext
        self.admin_fax = admin_fax
        self.admin_fax_ext = admin_fax_ext
        self.admin_email = admin_email
        self.registry_tech_id = registry_tech_id
        self.tech_name = tech_name
        self.tech_organization = tech_organization
        self.tech_street = tech_street
        self.tech_city = tech_city
        self.tech_stateprovince = tech_stateprovince
        self.tech_postal_code = tech_postal_code
        self.tech_country = tech_country
        self.tech_phone = tech_phone
        self.tech_phone_ext = tech_phone_ext
        self.tech_fax = tech_fax
        self.tech_fax_ext = tech_fax_ext
        self.tech_email = tech_email
        self.name_server = name_server
        self.dnssec = dnssec

    def __repr__(self):
        return 'Data %s %s %s %s %s %s %s %s %s ' \
               '%s %s %s %s %s %s %s %s %s %s %s' \
               '%s %s %s %s %s %s %s %s %s %s %s' \
               '%s %s %s %s %s %s %s %s %s %s %s' \
               '%s %s %s %s %s %s %s %s %s %s' % (self.domain_name,
                                                  self.registry_domain_id,
                                                  self.registrar_whois_server,
                                                  self.registrar_url,
                                                  self.updated_date,
                                                  self.creation_date,
                                                  self.registrar_registration_expiration_date,
                                                  self.registrar,
                                                  self.registrar_iana_id,
                                                  self.registrar_abuse_contact_email,
                                                  self.registrar_abuse_contact_phone,
                                                  self.domain_status,
                                                  self.registry_registrant_id,
                                                  self.registrant_name,
                                                  self.registrant_organization,
                                                  self.registrant_street,
                                                  self.registrant_city,
                                                  self.registrant_stateprovince,
                                                  self.registrant_postal_code,
                                                  self.registrant_country,
                                                  self.registrant_phone,
                                                  self.registrant_phone_ext,
                                                  self.registrant_fax,
                                                  self.registrant_fax_ext,
                                                  self.registrant_email,
                                                  self.registry_admin_id,
                                                  self.admin_name,
                                                  self.admin_organization,
                                                  self.admin_street,
                                                  self.admin_city,
                                                  self.admin_stateprovince,
                                                  self.admin_postal_code,
                                                  self.admin_country,
                                                  self.admin_phone,
                                                  self.admin_phone_ext,
                                                  self.admin_fax,
                                                  self.admin_fax_ext,
                                                  self.admin_email,
                                                  self.registry_tech_id,
                                                  self.tech_name,
                                                  self.tech_organization,
                                                  self.tech_street,
                                                  self.tech_city,
                                                  self.tech_stateprovince,
                                                  self.tech_postal_code,
                                                  self.tech_country,
                                                  self.tech_phone,
                                                  self.tech_phone_ext,
                                                  self.tech_fax,
                                                  self.tech_fax_ext,
                                                  self.tech_email,
                                                  self.name_server,
                                                  self.dnssec)


class SpiderPipeline(object):
    def __init__(self):
        basename = 'spider.db'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)

    @staticmethod
    def dictionary_checker(dictionary):
        """ Check dictionary. If all elements are None or empty list, function
         return True otherwise return False.
        :param dictionary: data type is dict
        :return: Boolean
        """
        value_list = []
        for value in dictionary.values():
            value_list.append(value)

        value_set = set(value_list)
        if len(value_set) == 1:
            value_list = list(value_set)
            if (value_list[0] is None) or (value_list[0] == []):
                return True
        return False

    def process_item(self, item, spider):
        dom_item = item['dom_item']
        reg_item = item['reg_item']
        who_item1 = item.get('who_item1')
        who_item2 = item.get('who_item2')

        if not self.dictionary_checker(dom_item):
            dt = DomainTable(dom_item['domain_name'], dom_item['domain'],
                             dom_item['words_in_domainname'],
                             dom_item['title'], dom_item['date_creation'],
                             dom_item['web_age'], dom_item['ip_address'],
                             dom_item['ip_geolocation'], dom_item['table'])
        else:
            return item

        if not self.dictionary_checker(reg_item):
            rt = RegistrantTable(reg_item['name'], reg_item['organization'],
                                 reg_item['email'], reg_item['country'],
                                 reg_item['private'])

            rt.domain.append(dt)
            self.session.add(rt)

        if who_item1 and not self.dictionary_checker(who_item1):
            wt1 = WhoisTable1(who_item1['domain'], who_item1['nserver'],
                              who_item1['state'], who_item1['org'],
                              who_item1['registrar'], who_item1['admin_contact'],
                              who_item1['created'], who_item1['paid_till'],
                              who_item1['free_date'], who_item1['source'])

            dt.whois1.append(wt1)
            self.session.add(wt1)

        elif who_item2 and not self.dictionary_checker(who_item2):
            wt2 = WhoisTable2(who_item2['domain_name'],
                              who_item2['registry_domain_id'],
                              who_item2['registrar_whois_server'],
                              who_item2['registrar_url'],
                              who_item2['updated_date'],
                              who_item2['creation_date'],
                              who_item2['registrar_registration_expiration_date'],
                              who_item2['registrar'],
                              who_item2['registrar_iana_id'],
                              who_item2['registrar_abuse_contact_email'],
                              who_item2['registrar_abuse_contact_phone'],
                              who_item2['domain_status'],
                              who_item2['registry_registrant_id'],
                              who_item2['registrant_name'],
                              who_item2['registrant_organization'],
                              who_item2['registrant_street'],
                              who_item2['registrant_city'],
                              who_item2['registrant_stateprovince'],
                              who_item2['registrant_postal_code'],
                              who_item2['registrant_country'],
                              who_item2['registrant_phone'],
                              who_item2['registrant_phone_ext'],
                              who_item2['registrant_fax'],
                              who_item2['registrant_fax_ext'],
                              who_item2['registrant_email'],
                              who_item2['registry_admin_id'],
                              who_item2['admin_name'],
                              who_item2['admin_organization'],
                              who_item2['admin_street'],
                              who_item2['admin_city'],
                              who_item2['admin_stateprovince'],
                              who_item2['admin_postal_code'],
                              who_item2['admin_country'],
                              who_item2['admin_phone'],
                              who_item2['admin_phone_ext'],
                              who_item2['admin_fax'],
                              who_item2['admin_fax_ext'],
                              who_item2['admin_email'],
                              who_item2['registry_tech_id'],
                              who_item2['tech_name'],
                              who_item2['tech_organization'],
                              who_item2['tech_street'],
                              who_item2['tech_city'],
                              who_item2['tech_stateprovince'],
                              who_item2['tech_postal_code'],
                              who_item2['tech_country'],
                              who_item2['tech_phone'],
                              who_item2['tech_phone_ext'],
                              who_item2['tech_fax'],
                              who_item2['tech_fax_ext'],
                              who_item2['tech_email'],
                              who_item2['name_server'],
                              who_item2['dnssec'])

            dt.whois2.append(wt2)
            self.session.add(wt2)

        self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)