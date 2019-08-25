from bs4 import BeautifulSoup
import requests
from openpyxl import workbook 
from openpyxl import load_workbook
import pandas as pd

class getcontent(object):
	def __init__(self):
		self.server = 'https://www.wrs.com.sg'
		self.server2 = '.html'
		self.firstpage = 'https://www.wrs.com.sg/en/night-safari/animals-and-zones.html'
		self.name = []          
		self.Time = []           
		self.info = []          
		self.location = []     
		self.animals = []         
		self.urls = []         
		self.title = []
		self.content = []
		self.img = []



	def get_attrictions_content(self):
		# initialize the string list or it will impact the excel writing

		#取动物数组
		target = self.firstpage
		req = requests.get(url = target)
		html = req.text
		bf = BeautifulSoup(html,'lxml')
		div = bf.find_all('div', class_ = 'list-animals') 
		an_bf = BeautifulSoup(str(div),'lxml')
		an_fa = an_bf.find_all('h4')
		#动物名 
		for each in an_fa:
			self.animals.append(each.string)
		an_fa = an_bf.find_all('a') 
		#去网址
		for each in an_fa:
			self.urls.append(self.server + each.get('href'))
		#取图片
		div = bf.find_all('div', class_ = 'list-animals') 
		an_bf = BeautifulSoup(str(div),'lxml')
		an_fa = an_bf.find_all('img',limit = 17) 
		for each in an_fa:
			self.img.append(self.server + each.get('src'))



		#animal
		for u_animal,n_animal,n_img in zip(self.urls,self.animals,self.img):

			n = n+1
			if n == 18:
				n = 0
				break

			target = u_animal
			# if target == "https://www.wrs.com.sg/en/night-safari/animals-and-zones/leopard.html":
			# 	continue
		#target = "https://www.wrs.com.sg/en/night-safari/animals-and-zones/asian-elephant.html"
			req = requests.get(url = target)
			html = req.text
			bf = BeautifulSoup(html,'lxml')
			div_2 = bf.find_all('div', class_ = 'label-head') 

			an_bf_2 = BeautifulSoup(str(div_2),'lxml')
			an_fa_2 = an_bf_2.find_all('h3') 

			for each in an_fa_2:
				self.info.append(each.string)
			result = f'"img":"{n_img}",\n"url":"{u_animal}",\n"name":"{n_animal}",\n"lifespan":"{self.info[0]}",\n"diet":"{self.info[1]}",\n"Habitat":"{self.info[2]}",\n"Range":"{self.info[3]}",\n'
			
			# #介绍  
			div_1 = bf.find_all('div', class_ = 'contentcarousel parsys aem-GridColumn aem-GridColumn--default--12') 

			an_bf_1 = BeautifulSoup(str(div_1),'lxml')
			div_2 = an_bf_1.find_all('div', class_ = 'detail') 

			an_bf_2 = BeautifulSoup(str(div_2),'lxml')
			an_fa_2 = an_bf_2.find_all('h3') 
			for each in an_fa_2:
				self.title.append(self.dealstr(str(each.string),0))
			an_fa_2 = an_bf_2.find_all('div', class_ = 'content rich-text') 
			
			for each in an_fa_2:
							#处理下有p的
				if(str(each).find('<p>')>-1):
					p_str = BeautifulSoup(str(each),'lxml')
					p_str_r = p_str.find_all('p') 
					
					str_result = ""
					for each_r in p_str_r:
						str_result = str_result+str(each_r)
					self.content.append(self.dealstr(str_result,3))
				else:
					str_result = str(each)
					self.content.append(self.dealstr(str_result,32))
			component = ""
			for title,content in zip(self.title,self.content):

				com_begin = '{\n'
				com_content = f'"name":"{title}",\n"content":"{content}"'
				com_end = '\n},\n'
				component = component + com_begin + com_content + com_end
				#最后一个为止
			info_result = '"info":['
			info_result_end = '\n]\n},'
			#combine
			result = '{\n' + result  + info_result +'\n' + component[:-2] + info_result_end
			print(result)

			self.info = []
			self.title = []
			self.content = []



#num：前段cut

	def dealstr(self,str_context,num):

		str_context = str_context.replace("<p>","").replace("<br/>","").replace("\n","").replace("</div>","").replace("</p>","")\
						.replace('<div class="content rich-text">','').replace("Â","")\
						.replace("â","'").replace("â","'")\
						.replace("â","-").replace("â",'\"').replace("â",'\"')\
						.replace('"','\\"')
		#去掉句号
		if num!=0:
			n_cut = 1
			if str_context[len(str_context)-1] != "." and str_context[len(str_context)-1] != "!":
				n_cut = 2
				if str_context[len(str_context)-2] != "." and str_context[len(str_context)-1] != "!":
					n_cut = 3
				pass
			return str_context[:-n_cut]
		else:
			return str_context
		


		
		

	
		
		
		
		

if __name__ == "__main__":

	dl = getcontent()
	dl.get_attrictions_content()


