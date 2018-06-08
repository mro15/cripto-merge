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


if __name__ == "__main__":
	args = read_args()
	k = open_file(args.key)
	img = cv2.imread(args.image)
	print img
