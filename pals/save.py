from time import sleep
import urllib.request
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from pals.models import UserProfile



driver = webdriver.Chrome('/home/anon/Downloads/chromedriver')

url = 'https://www.interpals.net/Thisiskittiya'
driver.get(url)
sleep(1)
lst = driver.find_elements_by_tag_name('h1')
username = lst[0].text
lst = driver.find_elements_by_tag_name('img')

html = driver.page_source
country = re.search(r'<a href="country/\w+">(\w+(\s\w+){0,2})</a>', html).group(1)
city = re.search(r'<a href="/app/search\?todo=search&amp;city=\d+">(\w+(\s\w+){0,2})</a>', html).group(1)
state = city

languages = driver.find_elements_by_class_name('prLangName')

languageLevels = driver.find_elements_by_class_name('proflLevel')
#Get level for all the languages
pos=0
for i in languageLevels:
	link = i.get_attribute('src')
	levelWithPng = link.split('lang_bars/')
	level = levelWithPng[1].split('.png')[0]
	languages[pos] = (languages[pos].text, level)
	pos+=1
#languages is now a list of pairs - (Language, Level of Skill)

pos=driver.page_source.find('y.o.')
age = driver.page_source[pos-3:pos-1]

soup = BeautifulSoup(html, 'html.parser')
imageUrl = soup.find('img', {'height':'180', 'width':'180'})['src']
imageUrl = 'https:'+imageUrl



# print('username = ', username)
# print('city = ', city)
# print('state = ', state)
# print('country = ', country)
# print('age = ', age)

# print('languages : ')
# for (a, b) in languages:
# 	print("%s Level: %s" %(a, b))

newUserProfile = UserProfile(username=username, 
	city=city,
	state=state,
	country=country,
	age = int(age),
	imageUrl = imageUrl,
	)
newUserProfile.save()
driver.close()

# print(soup.prettify())
