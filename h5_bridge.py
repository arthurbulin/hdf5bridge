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
	type = np.dtype(np.float64)
	x = np.genfromtxt(dat[1:],usecols=cols,dtype=type)
	
	body_set = np.genfromtxt(dat[1:],usecols=(0),dtype='str')
	bodies = get_bodies(body_set)
	index = get_indexs(body_set, bodies)
	for i in xrange(len(header)):
		if 'id' in header[i]:
			header.pop(i)
			break
	return header,bodies,index,x

def assemble_sets(header,bodies,inds,dat,sim,set):
	data_file = h5.File('./data.hdf5','a')
	print 'HDF5 file opened for all access'
	for i in xrange(len(bodies)):
		print 'For: ' + bodies[i],
		index = inds[bodies[i]]
		print " Index retrieved",
		body_data = dat[index]
		print ' Data sorted',
		body_data_rot = np.rot90(body_data)
		print ' Data rotated',
		body_data_flip = np.flipud(body_data_rot)
		print ' Data flipped',
		for j in xrange(len(header)):
			commit_dat = body_data_flip[j]
			print ' Commit_data created',
			data_file.create_dataset(sim+'/'+set+'/'+bodies[i]+'/'+header[j], data=commit_dat)
			print ' Commited.'
	
	data_file.close()
	print 'File closed'
