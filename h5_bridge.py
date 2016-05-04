import h5py as h5 
import numpy as np
import os
import subprocess
import copy
from decimal import Decimal

#Utilizes a python subprocess to capture the data necessary
def element_capture(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout = list()
	while True:
		line = p.stdout.readline()
		stdout.append(line)
		if line == '' and p.poll() != None: break
	return stdout
	
def get_header(dat):
	data = dict()
	header = dat[0]
	values = header.split()
	for h in xrange(len(values)): 
		if 'years' in values[h]:
			values.pop(h)
			break
	return values	

def get_bodies(dat):
#	f = h5.File(where+file,'a')
	bodies = list()
	for i in xrange(len(dat)):
		if dat[i] not in bodies:
			bodies.append(dat[i])
		else: break
	return bodies

def get_indexs(body_index, bodies):
	set = dict()
	for i in xrange(len(bodies)):
		temp = np.where(body_index == bodies[i])
		set[bodies[i]] = temp[0]
	return set

def refine_raw(dat):
	header = get_header(dat)
	size = len(header) - 1
	cols = np.linspace(1,size,num=size,dtype=int)
	type = np.dtype(Decimal)
	x = np.genfromtxt(dat[1:],usecols=cols,dtype=type)
	
	body_set = np.genfromtxt(dat[1:],usecols=(0),dtype='str')
	bodies = get_bodies(body_set)
	index = get_indexs(body_set, bodies)
	return header,bodies,index,x
