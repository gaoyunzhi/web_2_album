from bs4 import BeautifulSoup
import cached_url
from test import test
import time

def findAlbumUrl(soup):
	for album in soup.find_all('div', class_='title'):
		a = album.find('a')
		if not a:
			continue
		yield a['href']

def process(root, total_page):
	for page in range(0, total_page):
		url = root + '?start=' + str(page * 25)
		soup = BeautifulSoup(cached_url.get(url))
		for album_url in findAlbumUrl(soup):
			try:
				test(album_url)
			except Exception as e:
				print(album_url, str(e))
			time.sleep(120)

if __name__=='__main__':
	process('https://www.douban.com/doulist/3589810/', 5)
		
