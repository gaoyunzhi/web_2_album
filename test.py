#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web_2_album

def test():
	print(web_2_album.get(
		'https://www.weibo.com/1648544895/IyEMGc6xw'))
	
if __name__=='__main__':
	test()