# -*- coding:utf8 -*-


import scrapy


class DomainsSpider(scrapy.Spider):
    name = "domains"

    start_urls = ['https://trends.builtwith.com/media/video-players']

    def parse(self, response):
        filename = 'domains.html'

        domains_table = response.css("table.table")[0]
        links = domains_table.css("tbody tr td a::attr(href)").extract()

        with open(filename, 'wb') as f:
            f.write('\n'.join(links))

        #follow for href domain links
        for link in links:
            yield scrapy.Request(response.urljoin(link),
                                 callback=self.parse_domain)

    def parse_domain(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
            }
