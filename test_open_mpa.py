#!/usr/bin/python

#Author: Duncan Campbell
#Written: August 14, 2013
#Yale University
#Description: Read in hdf5 mpa catalogues and print out names

###packages###
import numpy as np
from astropy.io import ascii
import h5py
import sys
import glob
import custom_utilities as cu

def main():
  ###make sure to change these when running in a new enviorment!###
  #location of data directory
  filepath = cu.get_output_path() + 'processed_data/mpa_dr7/'
  #################################################################

  catalogues=['gal_totspecsfr_dr7_v5_2','gal_info_dr7_v5_2','totlgm_dr7_v5_2']

  for catalogue in catalogues:
      print catalogue
      f =  h5py.File(filepath+catalogue+'.hdf5', 'r')
      dset = f.get(catalogue)
      dset = np.array(dset)
      print 'length:', len(dset)
      for name in dset.dtype.names: print '\t', name

  

if __name__ == '__main__':
  main()
