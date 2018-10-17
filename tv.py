from requests import get
import datetime
from bs4 import BeautifulSoup as soup


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