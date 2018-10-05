# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from lxml import etree

from lxml import html

import pdb



class getProxy(scrapy.Spider):

	name = 'getProxy'

	domain = ''

	history = []

	output = []


	def __init__(self):

		dispatcher.connect(self.spider_closed, signals.spider_closed)

		self.myfile = 'output.txt'

		os.remove(self.myfile) if os.path.exists(self.myfile) else None

	
	def start_requests(self):

		url = 'https://free-proxy-list.net/'

		yield scrapy.Request(url=url, callback=self.parse, dont_filter=True) 


	def parse(self, response):

		with open('test.txt', 'wb') as f:

			f.write(response.body)

		proxy_list = response.xpath('//div[@class="table-responsive"]//tr')

		for proxy in proxy_list[1:]:

			detail = proxy.xpath('.//text()').extract()

			try:

				if ('us' in detail[2].lower() or 'ca' in detail[2].lower()) and 'yes' in detail[6].lower():

					temp = 'https://' + detail[0] + ':' + detail[1]

					self.output.append(temp)

			except Exception as e:

				pass


	def spider_closed(self, spider):

		try:

			with open(self.myfile, 'wb') as outfile:

				outfile.write('\n'.join(self.output))

		except Exception as e:

			pass


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp