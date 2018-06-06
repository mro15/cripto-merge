#! /usr/bin/env python

import sys
import argparse
import os.path
import numpy as np
import unicodedata
import re

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-f', '--file', type=str, required=True, help='nome do arquivo a ser criptografado')
	parser.add_argument('-k', '--key', type=str, required=True, help='nome do arquivo com a chave')
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
	lol = []
	cont = 0
	for i in range(0, len(b)/64):
		for j in range(0, 64):
			lol.append(b[cont])
			cont +=1
		block = convert_to_matrix(lol)
		mult_by_key(block, key)
		lol = []
	m = len(b)%64
	if(m!=0):
		for i in range(0, m):
			lol.append(b[cont])
			cont+=1
		block = convert_to_matrix(lol)
		mult_by_key(block, key)

#a ideia dessa funcao e receber a matriz e a key e fazer o estencil
def mult_by_key(block, key):
	print "block"
	print block
	print "key"
	print key
	i, j = key.shape[:2]
	pass

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
	read_blocks(b, key)
	#TODO: as imagens resultantes serao escritas em um diretorio
	#			como serao os nomes dos arquivos
