#!/usr/bin/python
import numpy as np


def make_linelist(ares):
    """
    This function creates a MOOG readable file from the ARES output using the
    line list and atomic data of make_linelist.dat file
    """

    # Read the line list and check for multiple identical lines
    linelist = np.genfromtxt('make_linelist.dat', dtype=None, skiprows=1,
                             names=['line', 'excitation', 'loggf',
                                    'elem', 'atomic', 'ew_sun'])
    linelist_wave = linelist['line']
    linelist_excitation = linelist['excitation']
    linelist_loggf = linelist['loggf']
    linelist_atomic = linelist['atomic']
    linelist_element = linelist['elem']
    assert (len(np.unique(linelist_wave)) == len(linelist_wave)), 'Check for multiple\
                                                    lines in make_linelist.dat'
    print 'Number of elements in line list: ', len(linelist_wave)
    ########################################################################

    # Read the lines and ews in the ares data and check for identical lines
    data = np.genfromtxt(ares, dtype=None, names=['wave', 'fit', 'c1', 'c2',
                                                  'ew', 'c3', 'c4', 'c5'])
    wave_ares = data['wave']
    ew_ares = data['ew']
    assert (len(np.unique(wave_ares)) == len(wave_ares)), 'Check for multiple\
                                                    lines in line.star.ares'
    print 'Number of lines measured by ares:', len(wave_ares)
    ########################################################################

    # Wavelength and EW taken from the ares file.
    # Test whether each element of a 1D array is also present in a second array
    index_ares = np.in1d(wave_ares, linelist_wave)
    common_wave = wave_ares[index_ares]
    ew = ew_ares[index_ares]

    # Sort common elements from ares by wavelength
    ares_values = np.column_stack((common_wave, ew))
    ares_sorted = sorted(ares_values, key=lambda row: row[0])
    ares_sorted = np.transpose(ares_sorted)
    ########################################################################

    # Wavelength and atomic data taken from the make_linelist.dat file.
    # Test whether each element of a 1D array is also present in a second array
    linelist_index = np.in1d(linelist_wave, wave_ares)
    index_lines_not_found = np.invert(np.in1d(linelist_wave, wave_ares))
    lines_not_found = linelist_wave[index_lines_not_found]
    print 'ARES did not find ', len(lines_not_found)
    print 'lines: ', lines_not_found

    wave = linelist_wave[linelist_index]
    excitation = linelist_excitation[linelist_index]
    loggf = linelist_loggf[linelist_index]
    atomic = linelist_atomic[linelist_index]
    print 'Lines in the new line list: ', len(wave)

    # Sort common elements from line list by wavelength
    linelist_values = np.column_stack((wave, atomic, excitation, loggf))
    linelist_sorted = sorted(linelist_values, key=lambda row: row[0])
    linelist_sorted = np.transpose(linelist_sorted)
    ########################################################################

    # Merge line list data with the EW from ARES
    # Sort the FeI and the FeII lines using the atomic number
    values = np.column_stack((ares_sorted[0], linelist_sorted[1],
                             linelist_sorted[2], linelist_sorted[3],
                             ares_sorted[1]))
    sorted_values = sorted(values, key=lambda row: row[1])
    sorted_values = np.transpose(sorted_values)
    ########################################################################

    # Write results in MOOG readable format
    assert np.array_equal(ares_sorted[0], linelist_sorted[0]), 'There is\
    something wrong with the common elements of ARES and the line list'
    data = zip(sorted_values[0], sorted_values[1], sorted_values[2],
               sorted_values[3], sorted_values[4])
    np.savetxt('lines.'+ares, data, fmt=('%9.2f', '%7.1f', '%11.2f',
                                         '%10.3f', '%27.1f'),
               header= '  '+ares)


###############################################################################
###############################################################################
# Main program
try:
    with open('makelines', 'r') as lines:
        for line in lines:
            make_linelist(line)
except IOError, e:
    print 'Sorry! To run this program, you need to create a "makelines"\
           file with the ares output.'
    raise SystemExit
