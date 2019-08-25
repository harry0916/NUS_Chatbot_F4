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
		self.animals = []         
		self.urls = []         
		self.name = []
		self.info = []
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
		#名 
		for each,n in zip(an_fa,range(0,21)):
			if(n>16):
				self.name.append(each.string)
		
		an_fa = an_bf.find_all('a') 
		#网址
		for each,n in zip(an_fa,range(0,21)):
			if(n>16):
				self.urls.append(self.server + each.get('href'))
		#图片
		div = bf.find_all('div', class_ = 'list-animals') 
		an_bf = BeautifulSoup(str(div),'lxml')
		an_fa = an_bf.find_all('img') 
		for each,n in zip(an_fa,range(0,21)):
			if(n>16):
				self.img.append(self.server + each.get('data-src'))



		for u_animal,n_animal,n_img in zip(self.urls,self.name,self.img):

			target = u_animal
			# if target == "https://www.wrs.com.sg/en/night-safari/animals-and-zones/leopard.html":
			#   continue
		#target = "https://www.wrs.com.sg/en/night-safari/animals-and-zones/asian-elephant.html"
			req = requests.get(url = target)
			html = req.text
			bf = BeautifulSoup(html,'lxml')
			div_2 = bf.find_all('div', class_ = 'one-column-only-text') 

			an_bf_2 = BeautifulSoup(str(div_2),'lxml')
			

			def has_style(tag):
				return tag.has_attr('style')
			an_fa_2 = an_bf_2.find_all(has_style) 
			info_bf = BeautifulSoup(str(an_fa_2),'lxml')
			self.info.append(self.dealstr(str(info_bf.div.get_text()).replace('\n','')))

			#animals
			div_2 = bf.find_all('h4', class_ = 'title-animals') 
			animals = ''
			for each in div_2:
				animals = animals + str(each.get_text()) + ","
			self.animals.append(animals[:-1])
			
			#combine
			  # {
			#   "img":"https://www.wrs.com.sg/content/dam/wrs/night-safari/zones/sign-post/350x540/leopard-trail1-odd.jpg",
			#   "url":"https://www.wrs.com.sg/en/night-safari/animals-and-zones/leopard-trail.html",
			#   "name": "Leopard Trail",
			#   "info": "Trek down the Leopard Trail and watch as the nightly routine of leopards, lions, civets and porcupines unfolds. This trail also takes you through two spectacular walk-through exhibits for up-close encounters with furry creatures of the skies - the flying foxes and flying squirrels",
			#   "Animals": "Binturong,Clouded leopard,Common palm civet,Eagle owl,Fruit bat,Giraffe,Golden cat,Hog badger,Leopard,Leopard cat,Lesser whistling duck,Malayan flying fox,Porcupine,Red and white giant flying squirrel,Slow loris,Small-clawed otter,Tarsier,Yellow wattled lapwing"
			# },
		result = ''
		for n in range(0,4):
			head_str = "{\n"
			img_str = '"img":"' + self.img[n] + '",\n'
			url_str = '"url":"' + self.urls[n] + '",\n'
			name_str = '"name":"' + self.name[n] + '",\n'
			info_str = '"info":"' + self.info[n] + '",\n'
			Animals_str = '"Animals":"' + self.animals[n] + '"\n},\n'
			result = result+head_str+img_str+url_str+name_str+info_str+Animals_str
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


