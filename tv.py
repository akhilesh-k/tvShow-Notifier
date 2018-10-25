from requests import get
import datetime
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import time

def switcher(argument):
	switch={
	"Jan" : 1,
	"Feb" : 2,
	"Mar" : 3,
	"Apr" : 4,
	"May" : 5,
	"Jun" : 6,
	"Jul" : 7,
	"Aug" : 8,
	"Sep" : 9,
	"Oct" : 10,
	"Nov" : 11,
	"Dec" : 12
	}
	return switch.get(argument)

def get_date(a):
	d=[]
	d.append(int(a[0:2]))
	d.append(switcher(a[3:6]))
	d.append(int(a[8:12]))
	return d

def imdb_data():
	url="https://www.imdb.com/title/tt5420376/?ref_=ttep_ep_tt"
	response=get(url)
	html=soup(response.content,'html.parser')
	tag = html.find('div',class_="seasons-and-year-nav")
	seasons="https://www.imdb.com/{}".format(tag.find('a')['href'])
	response=get(seasons)
	html=soup(response.content,'html.parser')
	next=""
	flag=0
	for date in html.find_all('div',class_='airdate'):
		if len(date.text)==4:
			next="The next season begins in {}".format(date.text)
			flag=1
			break
		d=get_date(date.text.strip())
		now=datetime.datetime.now()
		if d[2]>now.year:
			next="The next episode airs on {}".format(date.text)
			flag=1
			break
		if d[2]<=now.year:
			if d[1]>=now.month:
				if(d[0]>now.day):
					next="The next episode airs on {}".format(date.text)
					flag=1
					break
	if flag==0:
		next="The show has finished streaming all its episodes."

	print(next)

imdb_data()

def seasons():
	print ('Which series do you want to download? \t:\t')
	print ('Make sure first letter is CAPS!!') 
	series = raw_input()
	print ('Enter the Season')
	season= int(input())
	print ('Enter the Episode')
	epi_start= int(input())
	print ('To which episode')
	epi_end=int(input())
	driver = webdriver.Firefox()
	actionChains = ActionChains(driver)
	for i in range(epi_start,epi_end):
		if i<10 :
			url="http://o2tvseries.com/"+series+"/Season-0"+str(season)+"/Episode-0"+str(i)+"/index.html"
		else:
			url="http://o2tvseries.com/"+series+"/Season-0"+str(season)+"/Episode-"+str(i)+"/index.html"
		message= "Downloading the wished episode"
		print (message)
		driver.get(url)
		textlink=movie+" - "+"S0"+str(series)+"E0"+str(i)+" (O2TvSeries.Com).mp4"
		linkElem = driver.find_element_by_link_text(textlink)
		linkElem.click()
	driver.close()
	print ('Thank you')

def imdb_rating(series):
	series = str(series)
	link = requests.get("https://www.google.co.in/search?q="+series+"+imdb")
	soup = BeautifulSoup(link.text,'html.parser')
	html = soup.find('h3',{'class' : 'r'})
	href = (html.a).get('href')
	href = href.split('&')
	link = requests.get(href[0][7:])
	soup = BeautifulSoup(link.text,'html.parser')
	html = soup.find('strong')
	title = html.get('title')
	print ("\n\nIMDB Rating of ",series," : ",title,"\n\n")
	print ("Description\n")
	des = soup.find('div',{'class','summary_text'})
	print (des.text).lstrip(),"\n\n"
	language = 'en'
	mytext = (des.text).lstrip()
	myobj = gTTS(text=mytext, lang=language, slow=False)
 	myobj.save(series.split()[0]+".mp3")
 	os.system("mpg321 "+series.split()[0]+".mp3")

print "Press 1 to See IMDB Rating \n 2 to Download Series\n"
choice = input()
if(choice == 1):
	imdb_rating()
else:
	seasons()

