from bs4 import BeautifulSoup
import requests
from openpyxl import workbook 
from openpyxl import load_workbook
import pandas as pd

class getcontent(object):
	def __init__(self):
		self.firstpage = 'https://www.wrs.com.sg/en/night-safari/faq.html#ns'

		self.answer = []       
		self.question = []            


#处理符号
	def dealstr(self,str_context):

		str_context = str_context.replace("<p>","").replace("<br/>","").replace("\n","").replace("</div>","").replace("</p>","")\
						.replace('<div class="content rich-text">','').replace("Â","")\
						.replace("â","'").replace("â","'")\
						.replace("â","-").replace("â",'\"').replace("â",'\"')\
						.replace('"','\\"').replace('<a>','').replace('</a>','')
		
		return str_context


	def get_attrictions_content(self):
		# initialize the string list or it will impact the excel writing

		target = self.firstpage
		req = requests.get(url = target)
		html = req.text
		bf = BeautifulSoup(html,'lxml')


		
		panel = bf.find_all('div',limit=14 , class_ = 'faqcategories parsys aem-GridColumn aem-GridColumn--default--12') 
		ns_panel = ""
		for panel_div,n in zip(panel,range(0,13)):
			#前面有八个
			if n <8 :
				continue
			ns_panel = ns_panel + str(panel_div)
		panel_bf = BeautifulSoup(str(ns_panel),'lxml')
		#answer
		div = panel_bf.find_all('div', class_ = 'panel-inner') 
		div_temp_com = '<div></div>'+str(div)
		div_bf = BeautifulSoup(div_temp_com,'lxml')
		
		#要先处理第一个
		a = 0
		for sibling_div in div_bf.div.next_siblings:
			div_temp ='<p></p>' +  str(sibling_div)
			p_temp_bf = BeautifulSoup(div_temp,'lxml')
			p_temp = p_temp_bf.find_all('p') 
			p_bf = BeautifulSoup(str(p_temp),'lxml')
			
			result = ''
			for sibling in p_bf.p.next_siblings:
				content = ''
				if str(sibling).find(']')!=0 and str(sibling).find(', ')!=0\
				and str(sibling).find('<p></p>')<0 and str(sibling).find('[')!=0 and str(sibling).find('<p>\n</p>')<0 :
					content = str(sibling)
					#清理加粗符号
					
					content = content.replace('<b>','').replace('</b>','')

						
					#清理网址
					a = 1
					string_list2 = []

					while(a):
						a_index = content.find('<a href="')
						if a_index>-1:
							string_list1 = content.split('<a href="')
							content = string_list1[0]
							for list1_str in string_list1:
								if list1_str.find('">')<0:
									continue
								#分开后，开始循环 理论上第一段保持，第二...需要继续切
								
								string_list2 = list1_str.split('">')
								content = content + string_list2[1].replace('</a>','')
							content = self.dealstr(content)
						else:
							content = self.dealstr(content)
							a = 0
				#print(str(content))
				if len(content)>0:
					content = content + '.'
				result = result + content
			#处理邮箱 36
			index_email = result.find('<span class=')
			if index_email>-1:
				email = result.split('<span class=')
				result = email[0]+email[1][75:]
			if len(result)>2:
				self.answer.append(result.replace('. .','').replace('Email:','')\
					.replace('\xa0',' '))

		print(self.answer)
		#question
		#panel-title open
		div_title = panel_bf.find_all("div",class_ = "panel-heading")
		title_bf = BeautifulSoup(str(div_title),'lxml')
		title = title_bf.find_all("a")
		bf = BeautifulSoup(str(title),'lxml')
		for each in str(bf.get_text())[1:-1].split(', '):
			self.question.append(each)




if __name__ == "__main__":

	dl = getcontent()
	dl.get_attrictions_content()


	f = open('nsfaq_ss.txt','w')
	for question, answer in zip(dl.question,dl.answer):
		f.write(question+ '\n')
		f.write(answer '\n')
	 
	f.close()



