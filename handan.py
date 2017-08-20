#coding:utf-8

import requests
import os
from bs4 import BeautifulSoup
import sys
import urllib
from urllib import urlopen   
import redis
import pickle
import xlsxwriter
from xlsxwriter.workbook import Workbook
from xlrd.sheet import Sheet

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#download html
html_doc = open('page_1.html')
soup = BeautifulSoup(html_doc, 'html.parser')

#基础数据类
class Entity:
	_content = []
	_url = []

	_curent_page = ""
	_next_page = ""
	_pre_page = ""

	def set_url(self, url):
		self._url = url

	def set_content(self, content):
		self._content = content

	def get_all(self):
		return self._content, self._url 

	def set_curent_page(self, page):
		self._curent_page = page

	def set_next_page(self, page):
		self._next_page = page

	def set_pre_page(self, page):
		self._pre_page = page

class Method_Entity(Entity):
	x = 1

#查询条件数据
class PreCondData:
	__method_entity = ""
	__dist_entity = ""
	__price_entity = ""
	__alpha_entity = ""
	__type_entity = ""
	__status_entity = ""

	__data = []
	__urls = [] #所有分页的URL

	__default_main_url = "http://www.ljia.net"

	def __init__(self):
		self.__method_entity = Entity()
		self.__dist_entity = Entity()
		self.__price_entity = Entity()
		self.__alpha_entity = Entity()
		self.__type_entity = Entity()
		self.__status_entity = Entity()

	def get_methods(self):
		return self.__method_entity

	def get_dists(self):
		return self.__dist_entity

	def get_price(self):
		return self.__price_entity

	def get_alpha(self):
		return self.__alpha_entity

	def get_types(self):
		return self.__alpha_entity

	def get_status(self):
		return self.__status_entity

	def get_datas(self):
		return self.__data

	def _parse_method_condition(self):
		#查找方式
		for alls in soup.find_all('div', class_='hslist', limit=1):
			for child in alls.find_all('a', limit=2):
				self.__method_entity.set_content(child.string)
				self.__method_entity.set_url(child['href'])

	def _parse_dist_condition(self):
		#地区
		all_distritions = []
		distrition_hrefs = []
		for tag in soup.find_all('div', class_='cf', limit=1):
			for child in tag.find_all('a'):
				self.__dist_entity.set_content(child.string)
				self.__dist_entity.set_url(child['href'])

	def _parse_price_condition(self):
		#均价
		average_price = []
		price_hrefs = []
		alls = soup.find_all('div', class_='cf')
		price = alls[1]
		for child in price.find_all('a'):
			self.__price_entity.set_content(child.string)
			self.__price_entity.set_url(child['href'])

	def _parse_alpha_condition(self):
		#字母搜索
		alls = soup.find_all('div', class_='cf')
		alphbets = alls[2]
		for alpha in alphbets.find_all('a'):
			self.__alpha_entity.set_content(alpha.string)
			self.__alpha_entity.set_url(alpha['href'])

	def _parse_type_condition(self):
		#住宅类别
		alls = soup.find_all('div', class_='cf')
		houses = alls[3]
		for house in houses.find_all('a'):
			self.__type_entity.set_content(house.string)
			self.__type_entity.set_url(house['href'])

	def _parse_status_condition(self):
		#销售情况：全部，在售，待售
		alls = soup.find_all('ul', class_='xszt cf')
		status = alls[0]
		for s in status.find_all('a'):
			self.__status_entity.set_content(s.string)
			self.__status_entity.set_url(s['href'])

	def _parse_current_page_all(self):
		#不限 条件下的所有房子信息
		alls = soup.find_all('div', class_='conlist')
		alls = alls[0].find_all('div', class_='cf')
		for j in range(len(alls)):
			_data_ = Data()
			print j
			ent = alls[j]

			image_url = ent.find_all('img')[0].get('data-src')
			name = ent.find_all('img')[0].get('alt')
			address = ent.find_all('ul', class_='boxText')[0].find_all('li')[0].contents[1]
			tel = ent.find_all('ul', class_='boxText')[0].find_all('li')[1].contents[1].string
			price = ent.find_all('p', class_='price')[0].find_all('b')[0].string
			print image_url
			print name
			print address
			print tel
			print price
			print '\n'

			_data_.img_url = image_url
			_data_.title = name
			_data_.address = address
			_data_.tel = tel
			_data_.price = price

			self.__data.append(_data_)

		# self._parse_urls("/new/p-1.html")

	def _open_url(self, url):
		print "open url = %s" % url
		headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
		text = requests.get(url=url, headers=headers).text
		print text
		return text


	def _parse_next_page(self, text):
		#下一页
		next_page_url = soup.find_all('a', class_='next')[0]['href']
		return next_page_url


	def _parse_current_page(self):
		#curent
		current_page_url = soup.find_all('a', class_='curr')[0]['href']
		return current_page_url

		#前一页
		# alls = soup.find_all('a', class_='prev')
		# print alls[0]['href']

	def _parse_urls(self, first_url):
		cnt = 1

		url = "%s%s" % (self.__default_main_url, first_url)
		text = self._open_url(url)

		while(True):
			page = "page_%d.html" % cnt
			print page
			file_object = open(page, 'w')
			file_object.write(text)
			file_object.close()

			soup = BeautifulSoup(page, 'html.parser')
			cur = self._parse_current_page()
			if(cur != '#'):
				break

			next_page_url = self._parse_next_page(text)
			self.__urls.append(next_page_url)

			url = (self.__default_main_url+ next_page_url)
			text = self._open_url(url)

			cn += 1

		print self.__urls

#房子基本数据
class Data:
	img_url = ""
	title = ""
	address = ""
	tel = ""
	price = ""

	def dummy():
		x = 1

#查询方式
class Condition:
	dist = ""
	price = ""
	alpha = ""
	catel = ""
	num = 0 #前num个

	def condition_type(self):
		if(self.dist == "" and self.price == "" and self.alpha == "" and self.catel == "" and self.num == 0):
			return 0
		else:
			return 1

#manager
class Manager:
	__data = ""
	__condition = ""
	__preCondData = ""

	def __init__(self):
		self.__data = Data()
		self.__condition = Condition()
		self.__preCondData = PreCondData()

	def _save(self):
		r = redis.Redis(host='localhost', port=6379, db=0)

		lst = self.__preCondData.get_datas()

		for i in range(len(lst)):
			dt = lst[i]
			
			pickled_object = pickle.dumps(dt)
			r.set(dt.img_url, pickled_object)
		
		
		ll = []
		for key in r.scan_iter():
			if(len(key) < 10):
				pass
			else:
				unpacked_object = pickle.loads(r.get(key))
				ll.append(unpacked_object)
  
		print ll

	def _cal_result(self):
		lst = []
		less6 = 0
		b67 = 0
		b78 = 0
		b89 = 0
		b9 = 0
		other = 0

		datas = self.__preCondData.get_datas();
		for i in range(len(datas)):
			dt = datas[i]
			p = dt.price

			if(p.isdigit()):
				p = int(p)
				print p
				if(p < 6000):
					less6 += 1
				elif(p >= 6000) and (p < 7000):
					b67 += 1
				elif(p >= 7000) and (p < 8000):
					b78 += 1
				elif(p >= 8000) and (p < 9000):
					b89 += 1				
				else:
					b9 += 1
			else:
				other += 1

		lst.append(less6)
		lst.append(b67)
		lst.append(b78)
		lst.append(b89)
		lst.append(b9)
		lst.append(other)

		return lst

	def _put_to_chart(self):
		book = xlsxwriter.Workbook('chart.xlsx')
		sheet = book.add_worksheet()
		bold = book.add_format({'bold': 1})

		lst = self._cal_result()
		print lst
		chart = book.add_chart({'type': 'pie'})
		data = [['less 6000', '6000-7000', '7000-8000', '8000-9000', 'above 9000', 'NT'],
				lst,
				]

		sheet.write_row('A51',data[0],bold)
		sheet.write_row('A52',data[1])

		chart.add_series({
			'name':         '邯郸房价报表图',
        	'categories': '=Sheet1!$A$51:$F$51',
        	'values':     '=Sheet1!$A$52:$F$52',
        	'points':[
            	{'fill':{'color':'#00CD00'}},
            	{'fill':{'color':'red'}},
            	{'fill':{'color':'yellow'}},
            	{'fill':{'color':'gray'}},
            	{'fill':{'color':'black'}},
            	{'fill':{'color':'blue'}},
                  ],
			})

		chart.set_title({'name': '邯郸房价分布'})
		chart.set_style(3)

		sheet.insert_chart('B5', chart, {'x_offset': 25, 'y_offset': 10})
		book.close()

	def _search_all(self):
		#生成全部数据
		self.__preCondData._parse_current_page_all()

	def _cond_search(self):
		x = 1

	def _search(self):
		#根据不同的条件生成输出结果
		_seach_type = self.__condition.condition_type()
		if(_seach_type == 0):
			self._search_all()
		else:
			self._cond_search()

	def _get_args(self):
		#获取查询方式
		if(len(sys.argv) == 0 or len(sys.argv) == 5):
			print "Error."

		for i in range(len(sys.argv)):
			vari = sys.argv[i]
			if(i==0):
				__condition.dist = vari
			elif(i==1):
				__condition.price = vari
			elif(i==2):
				__condition.alpha = vari
			elif(i==3):
				__condition.catel = vari
			elif(i==4):
				__condition.num = vari
			else:
				print "params is error."

if __name__ == '__main__':
	_manager = Manager()
	_manager._search()
	# _manager._save()
	_manager._put_to_chart()








	


