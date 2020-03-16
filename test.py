#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web_2_album

def test():
	assert len(list(web_2_album.cut('tmp/no_cut.jpg')))	== 0
	list(web_2_album.cut('tmp/no_cut_2.jpg'))
	list(web_2_album.cut('tmp/cut_1.jpg'))
	list(web_2_album.cut('tmp/cut_2.jpg'))
	
if __name__=='__main__':
	test()