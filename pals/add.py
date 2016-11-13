from time import sleep
from bs4 import BeautifulSoup
import re
from .models import UserProfile
import random
import string
import sys

# b = webrdiver Selenium
urls=0
def login(b, username, password):
	b.get('https://www.interpals.net/app/auth/logout')
	login = b.find_element_by_id('topLoginEmail')
	login.send_keys(username)
	passField = b.find_element_by_id('topLoginPassword')
	passField.send_keys(password)
	signIn = b.find_elements_by_tag_name('input')[2]
	signIn.click()
# n = length of string
def randomString(n):
	s=''
	for i in range(n):
		s+=random.choice(string.ascii_letters)
	return s


def register(b):
	b.get('https://www.interpals.net/app/auth/logout')
	x=b.find_elements_by_name('username')[1]

	username=randomString(10)
	x.send_keys(username)
	x=b.find_element_by_name('email')
	x.send_keys(username+"@hotmail.com")
	x=b.find_elements_by_name('password')[1]
	x.send_keys(username)
	b.execute_script('document.getElementById("day").selectedIndex='+str(rand.randint(1, 28)))
	b.execute_script('document.getElementById("day").selectedIndex='+str(rand.randint(1, 8)))
	b.execute_script('document.getElementById("day").selectedIndex='+str(rand.randint(20, 60)))
	x=b.find_elements_by_class_name('f_left')[1]
	x.click()
	# Check robot failed



def AddToDb(url, b):
	 # soup = BeautifulSoup(html, 'html.parser')
	# lst = b.find_elements_by_tag_name('h1')
	username = url.split('.net/')[1]
	username = username.split('?')[0]
	exists=False
	try:
		x=UserProfile.objects.get(username=username)
		exists=True
	except:
		pass
	if (exists):
		return
	
	b.get(url)
	lst = b.find_elements_by_tag_name('img')

	html = b.page_source
	country = re.search(r'<a href="country/\w+">(\w+(\s\w+){0,2})</a>', html).group(1)
	city = re.search(r'<a href="/app/search\?todo=search&amp;city=\d+">(\w+(\s\w+){0,2})</a>', html).group(1)
	state = city

	# city = lst[23].text
	# state = lst[24].text

	languages = b.find_elements_by_class_name('prLangName')

	languageLevels = b.find_elements_by_class_name('proflLevel')
	#Get level for all the languages
	pos=0
	for i in languageLevels:
		link = i.get_attribute('src')
		levelWithPng = link.split('lang_bars/')
		level = levelWithPng[1].split('.png')[0]
		languages[pos] = (languages[pos].text, level)
		pos+=1
	#languages is now a list of pairs - (Language, Level of Skill)

	pos=b.page_source.find('y.o.')
	age = b.page_source[pos-3:pos-1]

	soup = BeautifulSoup(html, 'html.parser')
	imageUrl = soup.find('img', {'height':'180', 'width':'180'})
	if (imageUrl==None):
		return
	imageUrl=imageUrl['src']	
	imageUrl = 'https:'+imageUrl

	description=b.find_element_by_class_name("profDataBox")
	description=description.text

	# print('username = ', username)
	# print('city = ', city)
	# print('state = ', state)
	# print('country = ', country)
	# print('age = ', age)

	# print('languages : ')
	# for (a, b) in languages:
	# 	print("%s Level: %s" %(a, b))

	q = UserProfile(username=username, 
			city=city,
			state=state,
			country=country,
			age = int(age),
			imageUrl = imageUrl,
			description=description,
			)
	q.save()
	# print(soup.prettify())

def AddAll(b, url):
	b.get(url)
	soup = BeautifulSoup(b.page_source,'html.parser')
	people = soup.findAll('a', {'class':'female'})+soup.findAll('a', {'class':'male'})
	for x in people:
		newUrl='https://interpals.net'+x['href']
		# print(newUrl)
		try:
			AddToDb(newUrl, b)
		except:
			pass
		if (b.page_source.find('Hold on! You have been visiting too many pages')>0):
			print('User expired')
			break
	del people
	del soup
	
def AddCustom(b):
	url1 = 'https://www.interpals.net/app/search?todo=search&offset='
	url2 = '&sort=&age1=16&age2=110&sex%5B%5D=MALE&sex%5B%5D=FEMALE&continents%5B%5D=AF&continents%5B%5D=AS&continents%5B%5D=EU&continents%5B%5D=NA&continents%5B%5D=OC&continents%5B%5D=SA&countries%5B%5D=---&languages%5B%5D=---&languages%5B%5D=EN&lfor%5B%5D=lfor_email&lfor%5B%5D=lfor_snail&lfor%5B%5D=lfor_langex&lfor%5B%5D=lfor_friend&lfor%5B%5D=lfor_flirt&lfor%5B%5D=lfor_relation&keywords=&sort=last_login&username=&csrf_token=YjkzNTVkOWU%3D'
	for i in range(70, 100):
		AddAll(b, url1+str(i*20)+url2)
