#coding:utf-8

import requests
import os
from bs4 import BeautifulSoup
import sys

#download html
html_doc = open('source.html')
soup = BeautifulSoup(html_doc, 'html.parser')


#查找方式
search_methods = []
search_hrefs = []
for alls in soup.find_all('div', class_='hslist', limit=1):
	for child in alls.find_all('a', limit=2):
		search_methods.append(child.string)
		search_hrefs.append(child['href'])

#地区
all_distritions = []
distrition_hrefs = []
for tag in soup.find_all('div', class_='cf', limit=1):
	for child in tag.find_all('a'):
		all_distritions.append(child['href'])
		distrition_hrefs.append(child.string)

#均价
average_price = []
price_hrefs = []
alls = soup.find_all('div', class_='cf')
price = alls[1]
for child in price.find_all('a'):
	average_price.append(child.string)
	price_hrefs.append(child['href'])

#字母搜索
alphbet_dic = []
alphbet_hrefs = []
alls = soup.find_all('div', class_='cf')
alphbets = alls[2]
for alpha in alphbets.find_all('a'):
	alphbet_dic.append(alpha['href'])
	alphbet_hrefs.append(alpha.string)

#住宅类别
house_type = []
house_hrefs = []
alls = soup.find_all('div', class_='cf')
houses = alls[3]
for house in houses.find_all('a'):
	house_type.append(house.string)
	house_hrefs.append(house['href'])

#销售情况：全部，在售，待售
sales_status = []
sales_hrefs = []
alls = soup.find_all('ul', class_='xszt cf')
status = alls[0]
for s in status.find_all('a'):
	sales_status.append(s.string)
	sales_hrefs.append(s['href'])


#不限 条件下的所有房子信息
alls = soup.find_all('div', class_='conlist')
for cf in alls:
	image = cf.find_all('img')
	for i in range(len(image)):
		print image[i].get('data-src')
	entry = cf.find_all('ul', class_='boxText')
	for i in range(len(entry)):
		# print entry[i].find_all('h3')[0].find('a').contents[0]
		print entry[i].find_all('li')[0].contents[1]
		print entry[i].find_all('li')[1].contents[1].string

#下一页
alls = soup.find_all('a', class_='next')
print alls[0]['href']

#前一页
alls = soup.find_all('a', class_='prev')
print alls[0]['href']

#curent
alls = soup.find_all('a', class_='curr')
print alls[0]['href']

#数据
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

	def __init__(self):
		self.__data = Data()
		self.__condition = Condition()

	def _fetch_data(self, url):
		#start fetch
		x = 1

	def _save(self):
		#save to redis
		x = 1

	def _put_to_chart(self):
		#save as xls
		x = 1

	def _search_all(self):
		#生成全部数据
		x = 1

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









	


