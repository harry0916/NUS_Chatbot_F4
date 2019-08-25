from bs4 import BeautifulSoup
import requests
from openpyxl import workbook 
from openpyxl import load_workbook
import pandas as pd

class getcontent(object):
	def __init__(self):
		self.server = 'https://www.wrs.com.sg'
		self.server2 = '.html'
		self.firstpage = 'https://www.wrs.com.sg/en/night-safari/whats-on.html'
		self.img = []         
		self.urls = []     
		self.title = []         
		self.date = []           
		self.types = []         #ticket Friends of Wildlife Membership Retail Purchases
		self.info = []


#处理符号
	def dealstr(self,str_context):

		str_context = str_context.replace("<p>","").replace("<br/>","").replace("\n","").replace("</div>","").replace("</p>","")\
						.replace('<div class="content rich-text">','').replace("Â","")\
						.replace("â","'").replace("â","'")\
						.replace("â","-").replace("â",'\"').replace("â",'\"')\
						.replace('"','\\"')
		
		return str_context


	def get_attrictions_content(self):



		target = self.firstpage
		req = requests.get(url = target)
		html = req.text
		bf = BeautifulSoup(html,'lxml')
		div1 = bf.find_all('div', class_ = 'aem-Grid aem-Grid--12 aem-Grid--default--12') 
		div1_bf = BeautifulSoup(str(div1),'lxml')
		#Plus! Deals for NTUC Link 
		#
		div2 = div1_bf.find_all('div', class_ = 'onecolunmcontent parsys aem-GridColumn aem-GridColumn--default--12') 
		div2_bf = BeautifulSoup(str(div2),'lxml')
		#img
		img = div2_bf.find_all('img')
		for each,n in zip(img,range(0,3)):
			if n == 2:
				self.img.append('"img":"'+self.server + each.get('src') +'"'+",")
				pass
		#url
		self.urls.append('"url":"'+'https://www.wrs.com.sg/en/night-safari/whats-on.html' +'"')
		#title
		self.title.append('"name": "NTUC Link Members",')
		#date
		date_str = "15 FEB - 31 AUG 2019"
		self.date.append(f'"date": "in {date_str}",')
		#info
		info_head = '"info":{\n'
		self.type = ["ticket","Friends of Wildlife Membership","Retail Purchases"]
		#li 可以用兄弟节点来处理，但是我好懒
		li = div2_bf.find_all('li')
		li_list = []
		content = ""
		for each in li:
			li_list.append(each.string)
		for type_str,n in zip(self.type,range(0,3)):
			if n == 0:
				li_content = self.dealstr(li_list[0]+"."+li_list[1]+"."+li_list[2]+".")
			else:
				li_content = self.dealstr(li_list[2*n+1]+"."+li_list[2*n+2]+".")
			content = content+'"' + f'{type_str}' + '":"'+f'{li_content}' +'",\n'
		self.info.append(info_head+content[:-3]+"\n},")
		#rest
		#
		div2 = div1_bf.find_all('div', class_ = 'experiencegrid parsys aem-GridColumn aem-GridColumn--default--12') 
		div2_bf = BeautifulSoup(str(div2),'lxml')
		#name
		h3 = div2_bf.find_all('h3',limit=2)
		for h3_str in h3:
			self.title.append('"name": "'+self.dealstr(h3_str.string)+'",')
		#img
		img = div2_bf.find_all('img',limit=2)

		for img_str in img:

			self.img.append('"img":"'+self.server + img_str.get('src') +'"'+",")
		#date 好懒啊笑
		div3 = div2_bf.find_all('div', class_ = 'text-section') 
		div3_bf = BeautifulSoup(str(div3),'lxml')
		date = div3_bf.find_all('p',class_ = 'note')
		date_bf = BeautifulSoup(str(date),'lxml')
		for sibling in date_bf.span.next_siblings:
			sibling_str = repr(sibling).replace('\n','')
			self.date.append(f'"date": "in {sibling_str}",')
			self.date.append(f'"date": "in {sibling_str}",')
		#info
		div3 = div2_bf.find_all('div',class_="desc")
		div3_bf = BeautifulSoup(str(div3),'lxml')
		info = div3_bf.find_all('p')
		
		info_bf = BeautifulSoup(str(info),'lxml')
		for sibling in info_bf.p.next_siblings:
			if str(sibling).find('<sub>')<0 and str(sibling).find(',')<0 and str(sibling).find(']')<0 \
			and str(sibling).find('<p></p>')<0 and str(sibling).find('[')<0:
				content = '"'+f'{self.type[0]}'+ '":"' +(repr(sibling.string)) + '"'
				self.info.append(info_head+content+"\n},")
				pass
		#url
		link = div2_bf.find_all('a',class_="link link-1")
		for each in  link:
			self.urls.append('"url":"'+self.server + each.get('href') +'"')
		#combine

		result = ""
		for n in range(0,3):
			result = result+"{\n"
			result = result+ self.img[n] + "\n"
			result = result+ self.title[n] + "\n"
			result = result+ self.date[n] + "\n"
			result = result+ self.info[n] + "\n"
			result = result+ self.urls[n]
			result = result+ "\n}," + '\n'
		print(result)



if __name__ == "__main__":

	dl = getcontent()
	dl.get_attrictions_content()


