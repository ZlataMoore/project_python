# -*- coding: utf-8 -*-

import scrapy
from ..items import SpiderCianItem
import re
from urllib.parse import urlencode
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="my_request")


class CianspiderSpider(scrapy.Spider):

    name = 'CianSpider'
    allowed_domains = ['gdeetotdom.ru']
    start_urls = ['https://www.gdeetotdom.ru/kupit-kvartiru-moskva/']



    def parse(self, response):

        pages = response.xpath('//*[@class="search-result__bottom-panel"]'
                               '/*[@class="b-paginator2 pager robots-nocontent"]'
                               '/*[@class="b-paginator2__item"]'
                               '/a/@href').extract()
        print(len(pages))
        page = pages[0]
        #yield scrapy.Request(url=page, callback=self.parse_page)

        page_ = page[:-1]
        page = page_ + str(1201)
        i = 1201
        while i <= 1300:
            i += 1
            yield scrapy.Request(url=page, callback=self.parse_page)
            page = page_ + str(i)


    def parse_page(self, response):

        flats_premium = response.xpath('//*[@class="b-objects-list"]'
                               '/*[@class="c-card premium "]'
                               '/*[@class="c-card__description"]'
                               '/*[@class="c-card__container"]'
                               '/*[@class="c-card__column-left"]'
                               '/a/@href').extract()
        flats = response.xpath('//*[@class="b-objects-list"]'
                                '/*[@class="c-card "]'
                                '/*[@class="c-card__description"]'
                                '/*[@class="c-card__container"]'
                                '/*[@class="c-card__column-left"]'
                                '/a/@href').extract()

        print(len(flats_premium))
        print(len(flats))
        all_flats = flats + flats_premium
        for flat in all_flats:
            yield scrapy.Request(url=flat, callback=self.parse_flat)



    def parse_flat(self, response):
        item = SpiderCianItem()

        address = response.xpath('//*[@class="page__row top-row"]'
                                 '/*[@class="page__row-inner"]'
                                 '/*[@class="title-block"]'
                                 '/*[@class="address-line"]'
                                 '/text()').extract()

        address_premium = response.xpath('//*[@class="page__row top-row"]'
                                         '/*[@class="page__row-inner"]'
                                         '/*[@class="title-block premium"]'
                                         '/*[@class="address-line"]'
                                         '/text()').extract()
        cost = response.xpath('//*[@class="info-row js-header-border"]'
                                 '/*[@class="page__row"]'
                                 '/*[@class="page__row-inner"]'
                                 '/*[@class="main-info-container"]'
                                 '/*[@class="main-info"]'
                                 '/*[@class="realtor-contacts"]'
                                 '/*[@class="price-container"]'
                                 '/*[@class="price-block"]'
                                 '/*[@itemprop="offers"]'
                                 '/*[@itemprop="price"]'
                                 '/text()').extract()

        title = response.xpath('//*[@id="container"]'
                                       '//*[@class="page__container"]'
                                       '/*[@class="page__content js-parallax-content"]'
                                       '/*[@itemtype="https://schema.org/Product"]'
                                       '/*[@class="page__row top-row"]'
                                       '/*[@class="page__row-inner"]'
                                       '/*[@class="title-block"]'
                                       '/*[@class="title"]'
                                       '/*[@itemprop="name"]'
                                       '/text()').extract()
        title_premium = response.xpath('//*[@id="container"]'
                                       '//*[@class="page__container"]'
                                       '/*[@class="page__content js-parallax-content"]'
                                       '/*[@itemtype="https://schema.org/Product"]'
                                       '/*[@class="page__row top-row"]'
                                       '/*[@class="page__row-inner"]'
                                       '/*[@class="title-block premium"]'
                                       '/*[@class="title"]'
                                       '/*[@itemprop="name"]'
                                       '/text()').extract()

        if title:
            title = title[0].replace(u'\xa0', u' ')
            item['title'] = title
        else:
            title = title_premium[0].replace(u'\xa0', u' ')
            item['title'] = title
        nums = re.findall(r'\d+', cost[0])
        cost = ''.join(nums)
        item['cost'] = cost
        #item['details'] = details
        address_final = ''
        if address:
            address_final = address
        if address_premium:
            address_final = address_premium
        address = address_final
        item['address'] = address

        lst = address[0].split(',')
        address = lst[0] + ', ' + lst[-2] + ', ' + lst[-1]

        location = geolocator.geocode(address)
        if location:
            coordinates = (location.latitude, location.longitude)
            item['coordinates'] = coordinates
            yield item
        else:
            address = lst[0] + ', ' + lst[-2]
            location = geolocator.geocode(address)
            if location:
                coordinates = (location.latitude, location.longitude)
                item['coordinates'] = coordinates
                yield item



