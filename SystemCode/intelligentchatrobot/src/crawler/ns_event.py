from bs4 import BeautifulSoup
import requests
from openpyxl import workbook 
from openpyxl import load_workbook
import pandas as pd

class getcontent(object):
	def __init__(self):
		self.server = 'https://www.wrs.com.sg'
		self.server2 = '.html'
		self.firstpage = 'https://www.wrs.com.sg/en/singapore-zoo/whats-on/circle-of-life-festival.html?intcmp=1ccc%7C%7CCircle+of+Life+Festival%7Cpri%7CFind+Out+More%7Cnight-safari%3Awhats-on#nsactivities'
		self.position = []         
		self.date = []         
		self.time = []         
		self.tips = []         
		self.name = []
		self.content = []
		self.img = []

		

	def get_attrictions_content(self):



  
	
		target = self.firstpage
		req = requests.get(url = target)
		html = req.text
		bf = BeautifulSoup(html,'lxml')
		#两个buffet + gift
		div = bf.find_all('div', class_ = 'thumbnails-content') 
		an_bf = BeautifulSoup(str(div),'lxml')
		#name
		an_fa = an_bf.find_all('h3')
		n = 0
		for each in an_fa:
			n +=1
			if n<4:
				
				continue
			self.name.append(str(each.get_text()))
		#img
		n = 0
		an_fa = an_bf.find_all('img')
		for each in an_fa:
			n +=1
			if n<4:
				continue
			self.img.append(self.server + each.get('src'))
		#position
		# #position time居然是反的
		an_fa = an_bf.find_all('div',class_ = "list-label-thumb")
		n = 0
		for each in an_fa:
			n +=1
			if n<4:
				continue
			index_time = str(each).find("fa fa-clock-o")
			index_date = str(each).find("fa fa-calendar")
			index_location = str(each).find("fa fa-map-marker")
			list_str =  each.get_text().split("\n")
			if(len(list_str)) == 5:
				self.date.append(list_str[1])
				self.time.append(list_str[2])
				self.position.append(list_str[3])
			if(len(list_str)) == 4:
				if index_time<0:
					self.time.append("")
					self.date.append(list_str[1])
					self.position.append(list_str[2])
					pass
				if index_date<0:
					self.date.append("")
					self.time.append(list_str[1])
					self.position.append(list_str[2])
					pass
		#content
		n = 0
		an_fa = an_bf.find_all('div',class_ = "desc")
		info_bf = BeautifulSoup(str(an_fa),'lxml')
		info = info_bf.find_all('p')
		for each in info:
			n +=1
			if n<25:
				continue
			if len(str(each.get_text()))<2:
				continue
			self.content.append(self.dealstr(each.get_text().replace('\n','')))

		#combine


		result = ''
		for n in range(0,3):
		  head_str = "{\n"
		  img_str = '"img":"' + self.img[n] + '",\n'
		  name_str = '"name":"' + self.name[n] + '",\n'
		  date_str = '"date":"' + self.date[n] + '",\n'
		  time_str = '"time":"' + self.time[n] + '",\n'
		  position_str = '"position":"' + self.position[n] + '",\n'
		  content_str = '"content":"' + self.content[n] + '"\n},\n'
		  result = result+head_str+img_str+name_str+date_str+time_str+position_str+ content_str
		print(result[:-1])


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


