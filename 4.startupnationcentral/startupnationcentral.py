# encoding: utf-8
import json
import string

from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess

# TODO you will need to subscrape in zyte to get the data
# TODO zyte is a paid service, but provide 5$ free credit
# TODO Each 10K requests cost 2$
# TODO you can use the free credit to get the data
# TODO replace this key with your zyte api key
# use my affiliate link to get 5$ free credit, https://refer.zyte.com/6JG63V
ZYTE_API_KEY = '3e98f18c45484acf899f13d0dd11e4f3'


class SpiderStartupnationcentral(Spider):
    name = "startupnationcentral"
    company_id_map = {}
    current_company_id = 1
    investor_id_map = {}
    current_investor_id = 1

    def start_requests(self):
        # the idea there is a limit 140 page max, each page with 7 items so have to do this logic
        # by searching for each two letters in the alphabet
        # and then go to the next page
        # i can then get all possible companies
        # and scrapy itself won't visit the company page twice, so no duplicates
        for char1 in string.ascii_lowercase:
            for char2 in string.ascii_lowercase:
                yield Request(
                    f'https://finder.startupnationcentral.org/startups/search?&searchname={char1 + char2}&page=1&days=30&status=Active',
                    callback=self.result_page)

    def result_page(self, response):
        for url in response.css('#main-table-content>div>a::attr(href)').getall():
            yield response.follow(url, callback=self.company_page)
            # yield response.follow(url + '?section=business', callback=self.company_business)

        if next_page := response.xpath("//a[contains(span,'Next')]/@href").get():
            self.logger.info(f'next_page: {next_page}')
            yield response.follow(next_page, callback=self.result_page)

    def company_page(self, response):
        last_update_date = response.css('#claimed-badge-desktop~ span:nth-child(3)::text').get('').replace('.', '-')
        logo = response.css('#company-header-image-container>img::attr(src)').get()
        company_name = response.css('.company-profile-name::text').get('').strip()
        company_id = self.get_or_create_id(company_name, self.company_id_map, 'current_company_id')
        summary = response.css('.company-profile-description::text').get('').strip()
        overview = response.css('#about::text').get('').strip()
        sector = response.xpath('//div[h3[text()="Primary sector"]]/a/text/text()').get()
        total_funding = response.xpath('//div[h3[text()="Total funding"]]/text/text()').get()
        funding_stage = response.xpath('//div[h3[text()="Funding stage"]]/a/text/text()').get()
        num_employees = response.xpath('//div[h3[text()="Number of employees"]]/a/text/text()').get()
        founded = response.xpath('//div[h3[text()="Founded"]]/a/text/text()').get()
        website = response.css('#social-links-website::attr(href)').get()
        address_in_occupied_palestine = response.xpath('//div[contains(h3,"Israel")]/div/text()').get('').strip()
        offices_abroad = response.xpath('//div[contains(h3,"Offices Abroad")]/div/text()').get('').strip()
        linked_in = response.xpath('//a[contains(@onclick,"linkedin")]/@href').get()
        facebook = response.xpath('//a[contains(@onclick,"facebook")]/@href').get()
        twitter = response.xpath('//a[contains(@onclick,"twitter")]/@href').get()
        instagram = response.xpath('//a[contains(@onclick,"instagram")]/@href').get()
        youtube = response.xpath('//a[contains(@onclick,"youtube")]/@href').get()

        yield {
            'row_type': 'company',
            'company_id': company_id,
            'logo': logo,
            'company_name': company_name,
            'last_update_date': last_update_date,
            'summary': summary,
            'overview': overview,
            'sector': sector,
            'total_funding': total_funding,
            'funding_stage': funding_stage,
            'num_employees': num_employees,
            'founded': founded,
            'website': website,
            'address_in_occupied_palestine': address_in_occupied_palestine,
            'offices_abroad': offices_abroad,
            'linked_in': linked_in,
            'facebook': facebook,
            'twitter': twitter,
            'instagram': instagram,
            'youtube': youtube,
            'url': response.url
        }
        charts_data = json.loads(response.css('#charts-data::attr(data)').get())

        if 'employeesTrend' in charts_data:
            for employee_data in charts_data['employeesTrend']:
                yield {
                    'row_type': 'employeesTrend',
                    'company_id': company_id,
                    'employeesTrend_year': employee_data.get('x') or '',
                    'employeesTrend_value': employee_data.get('y') or ''
                }
        if charts_data.get('cumulativeFunding'):
            if 'data' in charts_data['cumulativeFunding'][0]:
                for cumulative_data in charts_data['cumulativeFunding'][0]['data']:
                    yield {
                        'row_type': 'cumulativeFunding',
                        'company_id': company_id,
                        'cumulativeFunding_year': cumulative_data.get('x') or '',
                        'cumulativeFunding_value': cumulative_data.get('y') or ''
                    }
        for investor in response.css('.member-circle .member-avatar'):
            investor_name = investor.css('::attr(tooltip-title)').get()
            investor_id = self.get_or_create_id(investor_name, self.investor_id_map, 'current_investor_id')
            investor_position = investor.css('::attr(tooltip-content)').get()
            yield {
                'row_type': 'company_investor',
                'company_id': company_id,
                'investor_id': investor_id,
                'investor_name': investor_name,
                'investor_position': investor_position
            }


    def get_or_create_id(self, name, id_map, counter_name):
        # Get the ID for the given name, creating a new one if necessary,
        # this way solved me of the issue of returning the counter with the name
        if name not in id_map:
            id_map[name] = getattr(self, counter_name)  # Get the current value of the counter
            setattr(self, counter_name, getattr(self, counter_name) + 1)  # Increment the counter
        return id_map[name]


if __name__ == "__main__":
    Settings = {

        'ITEM_PIPELINES': {
            'startupnationcentral_pipelines.StartupNationCentralPipeline': 300,
        },

        'LOG_LEVEL': 'INFO',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_IGNORE_HTTP_CODES': [400, 403, 404, 413, 414, 429, 456, 503, 529, 500],
        'ADDONS': {
            "scrapy_zyte_api.Addon": 500,
        },
        'ZYTE_API_KEY': ZYTE_API_KEY,
    }
    process = CrawlerProcess(Settings)
    process.crawl(SpiderStartupnationcentral)
    process.start()

"""
 Created by [Ahmed Ellaban](https://upwork.com/freelancers/ahmedellban)
وَسَلَامٌ عَلَى الْمُرْسَلِينَ وَالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ 
"""
