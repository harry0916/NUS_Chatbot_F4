from bs4 import BeautifulSoup
import requests
from openpyxl import workbook 
from openpyxl import load_workbook
import pandas as pd

class getcontent(object):
	def __init__(self):
		self.server = 'https://www.wrs.com.sg'
		self.server2 = '.html'
		self.firstpage = 'https://www.wrs.com.sg/en/night-safari/things-to-do/dine-and-shop.html'
		self.position = []         
		self.time = []         
		self.urls = []         
		self.name = []
		self.info = []
		self.img = []



	def get_attrictions_content(self):



  
		
		target = self.firstpage
		req = requests.get(url = target)
		html = req.text
		bf = BeautifulSoup(html,'lxml')
		#两个buffet + gift
		div = bf.find_all('div', class_ = 'onecolunmcontent parsys section') 
		an_bf = BeautifulSoup(str(div),'lxml')
		#name
		an_fa = an_bf.find_all('h3')
		for each in an_fa:
			self.name.append(str(each.get_text()))
		#position time居然是反的
		an_fa = an_bf.find_all('span',class_ = "label-thumb")
		n = 0
		for each in an_fa:
			if n == 0:
				n = 1
				self.time.append(str(each.get_text()).replace('\n',''))
			elif n == 1:
				n = 0
				self.position.append(str(each.get_text()).replace('\n',''))
		self.position[0],self.time[0] = self.time[0],self.position[0]
		#img
		an_fa = an_bf.find_all('img')
		for each in an_fa:
			self.img.append(self.server + each.get('src'))
		#info
		an_fa = an_bf.find_all('span',class_ = "content")
		for each in an_fa:
			self.info.append(self.dealstr(each.get_text().replace('\n','')))


		#the rest col-md-6 col-xs-12
		div = bf.find_all('div', class_ = 'col-md-6 col-xs-12') 
		an_bf = BeautifulSoup(str(div),'lxml')
		#name
		an_fa = an_bf.find_all('h3')
		for each in an_fa:
			self.name.append(str(each.get_text()))
		#position time
		an_fa = an_bf.find_all('p',class_ = "note")
		n = 0
		for each in an_fa:
			if n == 0:
				n = 1
				self.time.append(str(each.get_text()).replace('\n',''))
			elif n == 1:
				n = 2
				self.position.append(str(each.get_text()).replace('\n',''))
			elif n == 2:
				n = 0
		#img
		an_fa = an_bf.find_all('img')
		for each in an_fa:
			self.img.append(self.server + each.get('src'))
		#info
		an_fa = an_bf.find_all('div',class_ = "desc")
		info_bf = BeautifulSoup(str(an_fa),'lxml')
		info = info_bf.find_all('p')
		n = 0
		for each in info:
			if n == 0:
				n = 1
				continue
			self.info.append(self.dealstr(each.get_text().replace('\n','')))
		#url
		for n in range(1,8):
			self.urls.append("https://www.wrs.com.sg/en/night-safari/things-to-do/dine-and-shop.html")

		#combine
		result = ''
		for n in range(0,7):
			head_str = "{\n"
			url_str = '"url":"' + self.urls[n] + '",\n'
			img_str = '"img":"' + self.img[n] + '",\n'
			name_str = '"name":"' + self.name[n] + '",\n'
			loc_str = '"location":"' + self.position[n] + '",\n'
			time_str = '"time":"' + self.time[n] + '",\n'
			info_str = '"info":"' + self.info[n] + '"\n},\n'
			result = result+head_str+url_str+img_str+name_str+loc_str+time_str+ info_str
		print(result[:-1])
    # {
    #   "url":"https://www.wrs.com.sg/en/night-safari/things-to-do/dine-and-shop.html",
    #   "img":"https://www.wrs.com.sg/content/dam/wrs/singapore-zoo/dine-shop/ulu-restaurant--new.jpg",
    #   "name": "Ulu Ulu Safari Restaurant",
    #   "location": "ENTRANCE PLAZA",
    #   "time": "5.30PM TO 11.00PM",
    #   "info": "Drop by the Ulu Ulu Safari Restaurant for a quick supper after your Night Safari adventure. Here, you’ll find a mouthwatering selection of signature Indian dishes and salads to choose from, making it a perfect ending to your wild night out"
    # },


#num：前段cut

	def dealstr(self,str_context):

		str_context = str_context.replace("<p>","").replace("<br/>","").replace("\n","").replace("</div>","").replace("</p>","")\
						.replace('<div class="content rich-text">','').replace("Â ","")\
						.replace("â","'").replace("â","'")\
						.replace("â","-").replace("â",'\"').replace("â",'\"')\
						.replace('"','\\"')
		#去掉句号
		return str_context[:-1]
		


		
		

	
		
		
		
		

if __name__ == "__main__":

	dl = getcontent()
	dl.get_attrictions_content()


