import json
import os
import random
import time

import scrapy
from fake_useragent import UserAgent

from itjuzi.items import Person, Investor, AngelInvester, Company, InvestEvent, InvestFirm

os.environ["https_proxy"] = "https://119.31.210.170:7777"


class ITJuziSpider(scrapy.Spider):
    name = 'itjuzi'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'www.itjuzi.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': str(UserAgent().random)
    }

    formdata = {
    # input id and password
        'identity': '',
        'password': '',
        'submit': '',
        'page': '',
        'url': ''
    }

    company_page, investment_page, person_page, investor_page, angel_investor_page, invest_firm_page = 1, 1, 1, 1, 1, 1

    def start_requests(self):
        yield scrapy.Request(url='https://www.itjuzi.com/user/login',
                             callback=self.parse_login,
                             headers=self.headers,
                             meta={'cookiejar': 1})

    def parse_login(self, response):
        # 登录，日后如需验证码在此补充
        yield scrapy.FormRequest(url='https://www.itjuzi.com/user/login?redirect=&flag=&radar_coupon=',
                                 formdata=self.formdata,
                                 headers=self.headers,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.after_login)

    def after_login(self, response):
        # 投创人物
        # 创业者
        # yield scrapy.Request(url='https://www.itjuzi.com/person',
        #                      meta={'cookiejar': response.meta['cookiejar']},
        #                      headers=self.headers,
        #                      callback=self.parse_person)
        # 投资者
        # yield scrapy.Request(url='https://www.itjuzi.com/investor',
        #                      meta={'cookiejar': response.meta['cookiejar']},
        #                      headers=self.headers,
        #                      callback=self.parse_investor)
        # 天使投资人
        # yield scrapy.Request(url='https://www.itjuzi.com/angel_investor',
        #                      meta={'cookiejar': response.meta['cookiejar']},
        #                      headers=self.headers,
        #                      callback=self.parse_angel_investor)
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Host'] = 'radar.itjuzi.com'
        # 公司/项目
        # yield scrapy.Request(url='http://radar.itjuzi.com/company/infonew',
        #                      meta={'cookiejar': response.meta['cookiejar']},
        #                      headers=self.headers,
        #                      callback=self.parse_company)
        # 投融资速递
        # yield scrapy.Request(url='http://radar.itjuzi.com/investevent/info',
        #                      meta={'cookiejar': response.meta['cookiejar']},
        #                      headers=self.headers,
        #                      callback=self.parse_invest_event)
        # 投资机构
        yield scrapy.Request(
            url='http://radar.itjuzi.com/investment/info?scope=&state=&location=&character=&orderby=def&page=1',
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.headers,
            callback=self.parse_invest_firm)

    # 创业者
    def parse_person(self, response):
        for person_item in response.xpath('//i[@class="right"]'):
            person = Person()
            person['name'] = person_item.xpath('a[1]/text()').extract_first()
            person['des'] = person_item.xpath('a[2]/text()').extract_first()
            person['intro'] = person_item.xpath('../p/text()').extract_first()
            yield person
        self.person_page = self.person_page + 1
        yield scrapy.Request(url='https://www.itjuzi.com/person?&page=' + str(self.person_page),
                             meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.parse_person,
                             dont_filter=True)

    # 投资者
    def parse_investor(self, response):
        for investor_item in response.xpath('//i[@class="right"]'):
            investor = Investor()
            investor['name'] = investor_item.xpath('a[1]/text()').extract_first()
            investor['des'] = investor_item.xpath('a[3]/text()').extract_first()
            investor['intro'] = investor_item.xpath('../p/text()').extract_first()
            yield investor
        self.investor_page = self.investor_page + 1
        yield scrapy.Request(url='https://www.itjuzi.com/investor?&page=' + str(self.investor_page),
                             meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.parse_investor,
                             dont_filter=True)

    # 天使投资人
    def parse_angel_investor(self, response):
        for angel_investor_item in response.xpath('//i[@class="right"]'):
            a = AngelInvester()
            a['name'] = angel_investor_item.xpath('a[1]/text()').extract_first()
            a['des'] = angel_investor_item.xpath('a[2]/text()').extract_first()
            a['intro'] = angel_investor_item.xpath('../p/text()').extract_first()
            yield a
        self.angel_investor_page = self.angel_investor_page + 1
        yield scrapy.Request(url='https://www.itjuzi.com/angel_investor?&page=' + str(self.angel_investor_page),
                             meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.parse_angel_investor,
                             dont_filter=True)

    # 公司/项目
    def parse_company(self, response):
        company_info = json.loads(response.body.decode('utf-8'))
        del self.headers['X-Requested-With']
        if isinstance(company_info['data'], dict) and isinstance(company_info['data']['rows'], list):
            self.headers['Host'] = 'www.itjuzi.com'
            for row in company_info['data']['rows']:
                company_url = 'https://www.itjuzi.com/company/' + row['com_id']
                yield scrapy.Request(url=company_url,
                                     meta={'cookiejar': response.meta['cookiejar']},
                                     headers=self.headers,
                                     callback=self.parse_company_info)
            self.company_page = self.company_page + 1
            self.headers['X-Requested-With'] = 'XMLHttpRequest'
            time.sleep(random.randint(0, 3))
            self.headers['Host'] = 'radar.itjuzi.com'
            yield scrapy.Request(url='http://radar.itjuzi.com/company/infonew?page=' + str(self.company_page),
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 headers=self.headers,
                                 callback=self.parse_company)

    def parse_company_info(self, response):
        c = Company()
        c['name'] = response.xpath('//h1[@class="seo-important-title"]/text()').extract()[0]
        c['slogan'] = response.xpath('//h2[@class="seo-slogan"]/text()').extract()[0]
        c['description'] = response.xpath('//div[@class="info-line"]/span/text()').extract_first()
        summary = response.xpath('//div[@class="block"][1]/div/text()').extract_first().strip()
        if summary == '' or summary.find('itjuzi') != -1:
            summary = response.xpath('//div[@class="block"][1]/div/text()').extract()[1].strip()
        c['summary'] = summary
        c['tags'] = response.xpath('//div[@class="rowfoot"]/div/div/a/text()').extract()
        c['full_name'] = response.xpath('//div[@class="des-more"]/h2/text()').extract_first()
        c['founding_time'] = response.xpath('//div[@class="des-more"]/h3[1]/span/text()').extract_first()
        c['scale'] = response.xpath('//div[@class="des-more"]/h3[2]/span/text()').extract_first()
        yield c

    # 投融资速递
    def parse_invest_event(self, response):
        invest_event_info = json.loads(response.body.decode('utf-8'))
        if isinstance(invest_event_info['data'], dict) and isinstance(invest_event_info['data']['rows'], list):
            for row in invest_event_info['data']['rows']:
                invest_event = InvestEvent()
                invest_event['cat_name'] = row['cat_name']
                invest_event['com_id'] = row['com_id']
                invest_event['com_name'] = row['com_name']
                invest_event['currency'] = row['currency']
                invest_event['date'] = row['date']
                invest_event['invest_id'] = row['invse_id']
                invest_event['invest_with'] = row['invsest_with']
                invest_event['amount'] = row['money']
                invest_event['round'] = row['round']
                yield invest_event
            yield scrapy.Request(
                url='http://radar.itjuzi.com/investevent/info?location=in&orderby=def&page=' + str(
                    self.investment_page),
                meta={'cookiejar': response.meta['cookiejar']},
                headers=self.headers,
                callback=self.parse_invest_event)

    # 投资机构
    def parse_invest_firm(self, response):
        investment_info = json.loads(response.body.decode('utf-8'))
        if isinstance(investment_info['data'], dict) and isinstance(investment_info['data']['rows'], list):
            self.headers['Host'] = 'www.itjuzi.com'
            for row in investment_info['data']['rows']:
                investment_url = 'https://www.itjuzi.com/investfirm/' + row['invst_id']
                yield scrapy.Request(url=investment_url,
                                     meta={'cookiejar': response.meta['cookiejar']},
                                     headers=self.headers,
                                     callback=self.parse_invest_firm_info)
                self.invest_firm_page = self.invest_firm_page + 1
                self.headers['X-Requested-With'] = 'XMLHttpRequest'
                time.sleep(random.randint(0, 3))
                self.headers['Host'] = 'radar.itjuzi.com'
                yield scrapy.Request(
                    url='http://radar.itjuzi.com/investment/info?scope=&state=&location=&character=&orderby=def&page=' + str(
                        self.invest_firm_page),
                    meta={'cookiejar': response.meta['cookiejar']},
                    headers=self.headers,
                    callback=self.parse_invest_firm)

    def parse_invest_firm_info(self, response):
        invest_firm = InvestFirm()
        invest_firm['firm_name'] = response.xpath('//div[@class="inner-box"]/h1/text()').extract_first()
        invest_firm['firm_tags'] = response.xpath(
            '//div[@class="inner-box"]/div[@class="tag-list"]/span/text()').extract()
        invest_firm['firm_url'] = response.xpath('//a[@class="website-box"]/attribute::href').extract_first()
        invest_firm['description'] = response.xpath(
            '//ul[@class="list-unstyled base-intro"]/li[1]/text()').extract_first()
        invest_firm['total_scale'] = response.xpath(
            '//ul[@class="list-unstyled base-intro"]/li[2]/div[2]/descendant::text()').extract()
        invest_firm['scale_distribute'] = response.xpath(
            '//ul[@class="list-unstyled base-intro"]/li[3]/div[2]/span/text()').extract_first()
        invest_firm['invest_field'] = response.xpath(
            '//ul[@class="list-unstyled base-intro"]/li[4]/div[2]/a/text()').extract()
        invest_firm['invest_round'] = response.xpath(
            '//ul[@class="list-unstyled base-intro"]/li[5]/div[2]/a/text()').extract()
        invest_firm['fund_manager'] = response.xpath(
            '//ul[@class="list-unstyled base-intro"]/li[6]/div[2]/a/text()').extract()
        yield invest_firm
