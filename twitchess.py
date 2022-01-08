"""
Owned by @akshaysmin on github
Target: Scrape info on all streams in category 'chess' on "https://www.twitch.tv/directory/game/Chess" every 15 minutes
"""
"""

    find_element_by_id
    find_element_by_name
    find_element_by_xpath
    find_element_by_link_text
    find_element_by_partial_link_text
    find_element_by_tag_name
    find_element_by_class_name
    find_element_by_css_selector

    find_elements_by_name
    find_elements_by_xpath
    find_elements_by_link_text
    find_elements_by_partial_link_text
    find_elements_by_tag_name
    find_elements_by_class_name
    find_elements_by_css_selector

    find_element
    find_elements

    driver.execute_script

"""

from selenium import webdriver
from json import loads,dump
from datetime import datetime
import time
#from pprint import pprint

#CONSTANTS
driver_path = "geckodriver.exe"
url = "https://www.twitch.tv/directory/game/Chess"

#with open("cookiestwitch.dat") as f:
#	raw = f.read()

#cookies_signin = loads(raw)

driver = webdriver.Firefox(executable_path=driver_path) #change to webdriver.Chrome

#functions

def scroll_down(n):
	for i in range(n):
		last_elem = driver.find_elements_by_xpath("//div[@data-target='']")[-1]
		driver.execute_script("arguments[0].scrollIntoView(true);",last_elem)
		time.sleep(2)

def toint(text):
	try:
		result = int(text)
	except:
		if text.endswith('K') or text.endswith('k'):
			text = text.rstrip('K').rstrip('k')
			result = float(text)*1000
		elif text.endswith('M') or text.endswith('m'):
			text = text.rstrip('M').rstrip('m')
			result = float(text)*1e6

		else: 
			print(text)
			log(text)
			result = None

	return result

#main
with open('scraped2.dat') as f:
	pass
driver.get(url)
#temp = [driver.add_cookie(c) for c in cookies_signin]
#time.sleep(5)


while True:

	print('Refreshing..')
	driver.get(url)
	
	driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
	
	while not driver.find_elements_by_xpath("//div[@data-target='directory-first-item']"):
		time.sleep(2)

	scroll_down(10)
	
	raw = [driver.find_element_by_xpath("//div[@data-target='directory-first-item']").text]
	for element in driver.find_elements_by_xpath("//div[@data-target='']"):
		raw.append(element.text)
	
	#save info
	time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	n_channels = str(len(raw))
	infodic = {'time_now':time_now, 'n_channels':n_channels, 'n_views':None,
	           'channels':[], 'titles':[], 'views':[], 'tags':[]}
	channels = {}
	n_views = 0
	for text in raw:
		data = text.split('\n')
		title = data[0]
		channel = data[1]
		views = toint(data[-1].split()[0])
		tags = data[2:-1]
		n_views += views

		#channels[channel] = {'title':title, 'views':views, 'tags':tags}
		infodic['channels'].append(channel)
		infodic['titles'].append(title)
		infodic['views'].append(views)
		infodic['tags'].append(tags)

	infodic['n_views'] = n_views
	infodic['channels'] = channels

	print(time_now)
	print(n_channels,n_views)
	print(infodic)
	with open('scraped2.dat','a',encoding="utf-8") as f:
		dump(infodic,f)
		f.write('\n')

	time.sleep(10*60)
	print('next refresh within 5 minutes')
	time.sleep(5*60)
		