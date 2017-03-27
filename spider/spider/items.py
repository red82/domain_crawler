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


class RegistrantItem(Item):
    name = Field()
    organization = Field()
    email = Field()
    country = Field()
    private = Field()


class WhoisItem1(Item):
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


class WhoisItem2(Item):
    domain_name = Field()
    registry_domain_id = Field()
    registrar_whois_server = Field()
    registrar_url = Field()
    updated_date = Field()
    creation_date = Field()
    registrar_registration_expiration_date = Field()
    registrar = Field()
    registrar_iana_id = Field()
    registrar_abuse_contact_email = Field()
    registrar_abuse_contact_phone = Field()
    domain_status = Field()
    registry_registrant_id = Field()
    registrant_name = Field()
    registrant_organization = Field()
    registrant_street = Field()
    registrant_city = Field()
    registrant_stateprovince = Field()
    registrant_postal_code = Field()
    registrant_country = Field()
    registrant_phone = Field()
    registrant_phone_ext = Field()
    registrant_fax = Field()
    registrant_fax_ext = Field()
    registrant_email = Field()
    registry_admin_id = Field()
    admin_name = Field()
    admin_organization = Field()
    admin_street = Field()
    admin_city = Field()
    admin_stateprovince = Field()
    admin_postal_code = Field()
    admin_country = Field()
    admin_phone = Field()
    admin_phone_ext = Field()
    admin_fax = Field()
    admin_fax_ext = Field()
    admin_email = Field()
    registry_tech_id = Field()
    tech_name = Field()
    tech_organization = Field()
    tech_street = Field()
    tech_city = Field()
    tech_stateprovince = Field()
    tech_postal_code = Field()
    tech_country = Field()
    tech_phone = Field()
    tech_phone_ext = Field()
    tech_fax = Field()
    tech_fax_ext = Field()
    tech_email = Field()
    name_server = Field()
    dnssec = Field()
