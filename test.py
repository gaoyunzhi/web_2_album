#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web_2_album

def test():
	print(web_2_album.get(
		'http://weibointl.api.weibo.cn/share/131595305.html'))
	
if __name__=='__main__':
	test()