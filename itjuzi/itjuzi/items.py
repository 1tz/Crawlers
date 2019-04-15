# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 创业者
class Person(scrapy.Item):
    name = scrapy.Field()
    des = scrapy.Field()
    intro = scrapy.Field()


# 投资人
class Investor(scrapy.Item):
    name = scrapy.Field()
    des = scrapy.Field()
    intro = scrapy.Field()


# 天使投资人
class AngelInvester(scrapy.Item):
    name = scrapy.Field()
    des = scrapy.Field()
    intro = scrapy.Field()


# 公司/项目
class Company(scrapy.Item):
    name = scrapy.Field()  # 公司名称
    slogan = scrapy.Field()  # 公司简介
    description = scrapy.Field()  # 基本信息
    full_name = scrapy.Field()  # 公司全称
    founding_time = scrapy.Field()  # 成立时间
    scale = scrapy.Field()  # 公司规模
    tags = scrapy.Field()  # 公司标签
    summary = scrapy.Field()  # 现状简介


# 投融资速递
class InvestEvent(scrapy.Item):
    cat_name = scrapy.Field()
    com_id = scrapy.Field()
    com_name = scrapy.Field()
    currency = scrapy.Field()
    date = scrapy.Field()
    invest_id = scrapy.Field()
    invest_with = scrapy.Field()
    amount = scrapy.Field()
    round = scrapy.Field()


# 投资机构
class InvestFirm(scrapy.Item):
    firm_name = scrapy.Field()
    firm_tags = scrapy.Field()
    firm_url = scrapy.Field()
    description = scrapy.Field()
    total_scale = scrapy.Field()
    scale_distribute = scrapy.Field()
    invest_field = scrapy.Field()
    invest_round = scrapy.Field()
    fund_manager = scrapy.Field()
    partner_together = scrapy.Field()
    partner_next = scrapy.Field()
    partner_before = scrapy.Field()

