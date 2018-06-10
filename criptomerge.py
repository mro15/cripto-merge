#! /usr/bin/env python

import sys
import argparse
import os.path
import numpy as np
import unicodedata
import re
import cv2
import random
from datetime import datetime as dt

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-f', '--file', type=str, required=True, help='nome do arquivo a ser criptografado')
	parser.add_argument('-k', '--key', type=str, required=True, help='nome do arquivo com a chave')
	parser.add_argument('-i', '--image', type=str, required=True, help='nome do arquivo para guardar a imagem (.png)')
	return parser.parse_args()

def open_file(file_in):
	if not(os.path.exists(file_in)) or not(os.path.isfile(file_in)):
		print "Arquivo de entrada nao existe"
		sys.exit()
	f = open(file_in, 'r')
	return f

def file_parser(f):
	b = f.read()
	f.close()
	#convert str to utf-8
	b = unicode(b, 'utf-8')
	#chnge to unicode and encode in ascii
	b = unicodedata.normalize('NFKD', b).encode('ASCII', 'ignore')
	b = re.sub('[^A-Za-z0-9]+', '', b)
	return b

#read key and mount the estencil
def read_key(key_file):
	key = []
	for line in key_file:
			key.append(map(int, line.strip().split(' ')))
	return np.array(key)

def read_blocks(b, key):
	final_image = 0
	lol = []
	cont = 0
	for i in range(0, len(b)/64):
		for j in range(0, 64):
			lol.append(b[cont])
			cont +=1
		block = convert_to_matrix(lol)
		mult = mult_by_key(block, key)
		img = mount_rgb_image(mult)
		final_image = concat_blocks(final_image, img)
		lol = []
	m = len(b)%64
	if(m!=0):
		for i in range(0, m):
			lol.append(b[cont])
			cont+=1
		block = convert_to_matrix(lol)
		mult = mult_by_key(block, key)
		img = mount_rgb_image(mult)
		final_image = concat_blocks(final_image, img)
	return final_image

def concat_blocks(img, block):
	if type(img) is int:
		return block
	return np.concatenate((img, block), axis=0)

def mount_rgb_image(mat):
	img = np.zeros((8, 8, 3), dtype=np.int)
	#channels = ['b', 'g', 'r'] [0, 1, 2]
	random.seed(dt.now()) #seria uma boa passar a seed por parametro sera
	for i in range(0, 8):
		for j in range(0, 8):
			img[i][j][0] = random.randint(0, 255)
			img[i][j][1] = mat[i][j]/255
			img[i][j][2] = mat[i][j]%255

	return img

def mult_by_key(block, key):
	res = np.zeros((8, 8), dtype=np.int)
	ik, jk = key.shape[:2]
	for i in range(0, 8):
		for j in range(0, 8):
			res[i][j] = block[i][j] * key[i%ik][j%jk]
	return res

def convert_to_matrix(b):
	size = (8, 8)
	m = np.zeros(size, dtype=np.int)
	if len(b)==64:
		cont =  0
		for i in range(0, 8):
			for j in range(0, 8):
				m[i][j] = ord(b[cont])
				cont +=1
	else:
		cont =  0
		for i in range(0, 8):
			for j in range(0, 8):
				if cont<len(b):
					m[i][j] = ord(b[cont])
					cont +=1
				else:
					break
	return m

if __name__ == "__main__":
	args = read_args()
	f = open_file(args.file)
	k = open_file(args.key)
	key = read_key(k)
	b = file_parser(f)
	print "TEXTO CLARO"
	print b
	img = read_blocks(b, key)
	cv2.imwrite(args.image, img)
