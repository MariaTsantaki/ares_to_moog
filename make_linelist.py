#!/usr/bin/python
import numpy as np
from numpy import *

def make_linelist(ares):
	"""This function creates a MOOG readable file from the ARES output using the line list and atomic data of make_linelist.dat file
	"""
	#Read Tsantaki 2013 line list
	linelist = np.genfromtxt('make_linelist.dat', dtype=None, skiprows=1, names = ['line', 'excitation', 'loggf', 'elem', 'atomic', 'ew_sun'])
	linelist_wave = linelist['line']
	linelist_excitation = linelist['excitation']
	linelist_loggf = linelist['loggf']
	linelist_atomic = linelist['atomic']
	linelist_element = linelist['elem']
	if len(np.unique(linelist_wave)) > len(linelist_wave):	#Checking for multiple lines
		print 'Check for multiples in make_linelist.dat'
	else:
		print 'Number of elements in line list: ', len(linelist_wave)
	########################################################################

	#Read the lines and ews in the ares data
	data = np.genfromtxt(ares, dtype=None, names = ['wave', 'fit', 'c1', 'c2', 'ew', 'c3', 'c4', 'c5'])
	wave_ares = data['wave']
	ew_ares = data['ew']
	if len(np.unique(wave_ares)) > len(wave_ares):	#Checking for multiple lines
		print 'Check for multiples in line.star.ares'
	else:
		print 'Number of lines measured by ares:', len(wave_ares)
	########################################################################

	#Wavelength and EW taken from the ares file.
	#Test whether each element of a 1-D array is also present in a second array.
	index_ares = np.in1d(wave_ares, linelist_wave)
	common_wave = wave_ares[index_ares]
	ew = ew_ares[index_ares] 

	#Sort common elements from ares by wavelength
	ares_values = np.array([common_wave, ew])
	ares_values = np.transpose(ares_values)
	ares_sorted = sorted(ares_values, key=lambda row: row[0])
	ares_sorted = np.transpose(ares_sorted)
	########################################################################

	#Wavelength and atomic data taken from the make_linelist.dat file.
	#Test whether each element of a 1-D array is also present in a second array.
	linelist_index = np.in1d(linelist_wave, wave_ares)
	index_lines_not_found = np.invert(np.in1d(linelist_wave, wave_ares))
	lines_not_found = linelist_wave[index_lines_not_found]
	print 'ARES did not find ', len(lines_not_found), 'lines: ', lines_not_found

	wave = linelist_wave[linelist_index]
	excitation = linelist_excitation[linelist_index]
	loggf = linelist_loggf[linelist_index]
	atomic = linelist_atomic[linelist_index]
	print 'Lines in the new line list: ', len(wave)

	#Sort common elements from line list by wavelength
	linelist_values = np.array([wave, atomic, excitation, loggf])
	linelist_values = np.transpose(linelist_values)
	linelist_sorted = sorted(linelist_values, key=lambda row: row[0])
	linelist_sorted = np.transpose(linelist_sorted)
	########################################################################

	#Merge line list data with the EW from ARES
	#Sort the FeI and the FeII lines using the atomic number
	values = np.array([ares_sorted[0], linelist_sorted[1], linelist_sorted[2], linelist_sorted[3], ares_sorted[1]])
	values = np.transpose(values)
	sorted_values = sorted(values, key=lambda row: row[1])
	sorted_values = np.transpose(sorted_values)
	########################################################################

	#Write results in MOOG readable format
	if np.array_equal(ares_sorted[0], linelist_sorted[0]):
		np.savetxt('lines.'+ares, zip(sorted_values[0], sorted_values[1], sorted_values[2], sorted_values[3], sorted_values[4]), fmt=('%9.2f','%7.1f','%11.2f','%10.3f','%27.1f'), header= '  '+ares, footer='', comments='')
	else:
		'eRRoR! There is something wrong with the common elements of ares and the line list'
	return

################################################################################
################################################################################
#Main program
try:
	with open('makelines') as f:
			lines = f.readlines()[:]

	filename = []
	for line in lines:
	 	line = line.split('\n')
	       	filename.append(str(line[0]))

	for i,x in enumerate(filename):
		make_linelist(x)     

except IOError:
	print 'Sorry! To run this program, you need to create a "makelines" file with the ares output.'
