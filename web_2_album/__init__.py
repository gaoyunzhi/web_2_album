#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'web_2_album'

import math
import os
import cached_url
from bs4 import BeautifulSoup

def get(path):
	b = BeautifulSoup(cached_url.get(path), features="html.parser")
	for img in b.find_all('img'):
		if img.get('src') and 'width: 100%;' in str(img.attrs):
			print img.get('src')
	

