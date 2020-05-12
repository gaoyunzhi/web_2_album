from bs4 import BeautifulSoup
import cached_url
from test import test
import time

start = False
start_on = '74171797'

def findAlbumUrl(soup):
	for album in soup.find_all('div', class_='title'):
		a = album.find('a')
		if not a:
			continue
		yield a['href']

def process(root, total_page):
	global start
	
	for page in range(0, total_page):
		url = root + '?start=' + str(page * 25)
		soup = BeautifulSoup(cached_url.get(url))
		for album_url in findAlbumUrl(soup):
			if start_on in album_url:
				start = True
				continue
			if start:
				try:
					test(album_url)
				except:
					pass
				time.sleep(120)

if __name__=='__main__':
	process('https://www.douban.com/doulist/3589810/', 5)
		
