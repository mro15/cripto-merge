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
	print b
	#convert str to utf-8
	b = unicode(b, 'utf-8')
	#chnge to unicode and encode in ascii
	b = unicodedata.normalize('NFKD', b).encode('ASCII', 'ignore')
	print b
	b = re.sub('[^A-Za-z0-9]+', '', b)
	print b
	return b

def read_blocks(b):
	lol = []
	cont = 0
	for i in range(0, len(b)/64):
		for j in range(0, 64):
			lol.append(b[cont])
			cont +=1
		convert_to_matrix(lol)
		lol = []
	m = len(b)%64
	if(m!=0):
		for i in range(0, m):
			lol.append(b[cont])
			cont+=1
		convert_to_matrix(lol)
	print lol


#TODO: finish this function
def convert_to_matrix(b):
	size = (8, 8)
	m = np.zeros(size, dtype=np.int)
	print m
	print b
	print len(b)

if __name__ == "__main__":
	args = read_args()
	f = open_file(args.file)
	b = file_parser(f)
	read_blocks(b)
