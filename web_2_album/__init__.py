#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'pic_cut'

from PIL import Image
import math
import os

MARGIN = 0.05

def goodSize(w, h):
	return h < 2 * w

def computeSize(h, p):
	raw_h = h / (p - MARGIN * (p - 1))
	nh = math.ceil(raw_h)
	moves = [math.ceil(raw_h * ((1 - MARGIN) * step)) for step in range(p - 1)]
	moves.append(h - nh)
	return nh, moves

def cut(path):
	img = Image.open(path)

	w, h = img.size

	for piece in range(1, 19):
		nh, moves = computeSize(h, piece)
		if goodSize(w, nh):
			break

	if len(moves) <= 1 or not goodSize(w, nh):
		moves = []

	for p, m in enumerate(moves):
		working_slice = img.crop((0, m, w, m + nh))
		main_path, _ = os.path.splitext(path)
		fn = '%s_%d.png' % (main_path, p)
		working_slice.save(fn)
		yield fn

