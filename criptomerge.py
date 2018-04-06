#! /usr/bin/env python

import sys
import argparse
import os.path
import numpy as np

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

def convert_to_matrix(f):
  pass

if __name__ == "__main__":
	args = read_args()
	f = open_file(args.file)
