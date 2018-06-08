#! /usr/bin/env python

import sys
import argparse
import os.path
import numpy as np
import unicodedata
import re
import cv2
import random

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-f', '--file', type=str, required=True, help='nome do arquivo de saida')
	parser.add_argument('-k', '--key', type=str, required=True, help='nome do arquivo com a chave')
	parser.add_argument('-i', '--image', type=str, required=True, help='nome da imagem criptografada')
	return parser.parse_args()

def open_file(file_in):
	if not(os.path.exists(file_in)) or not(os.path.isfile(file_in)):
		print "Arquivo de entrada nao existe"
		sys.exit()
	f = open(file_in, 'r')
	return f

#read key and mount the estencil
def read_key(key_file):
	key = []
	for line in key_file:
			key.append(map(int, line.strip().split(' ')))
	return np.array(key)

def decript(img, key, f):
	blocks = len(img)/8
	ik, jk = key.shape[:2]
	for b in range(0, blocks):
		dtext= np.zeros((8, 8), dtype=np.int)
		offset = b*8
		for i in range(0, 8):
			for j in range(0, 8):
				dtext[i][j] = ((img[offset+i][j][1]*255)+img[offset+i][j][2])/(key[i%ik][j%jk])
		dec_to_text(dtext, f)

def dec_to_text(block, f):
	text = ""
	for i in range(0, 8):
		for j in range(0, 8):
			text = text + chr(block[i][j])
	f.write(text)


if __name__ == "__main__":
	args = read_args()
	f = open(args.file, 'wt')
	k = open_file(args.key)
	key = read_key(k)
	img = cv2.imread(args.image)
	decript(img, key, f)
	f.close()
