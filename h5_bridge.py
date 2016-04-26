import h5py as h5 
import numpy as np
#import lib_merc as lme
import os
import subprocess

def element_capture(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout = list()
	while True:
		line = p.stdout.readline()
		stdout.append(line)
		if line == '' and p.poll() != None: break
	return stdout
