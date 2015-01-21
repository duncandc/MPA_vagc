#!/usr/bin/python

#Author: Duncan Campbell
#Written: January 21, 2015
#Yale University
#Description: make a combined NYU-MPA dr7 catalogue using the MPA as the base

###packages###
from __future__ import print_function
import numpy as np
import h5py
import custom_utilities as cu
import matplotlib.pyplot as plt

def main():
    
    ###make sure to change these when running in a new enviorment!###
    #location of data directories
    filepath_1 = cu.get_output_path() + 'processed_data/mpa_dr7/'
    filepath_2 = cu.get_output_path() + 'processed_data/NYU_VAGC/'
    #################################################################

    catalogue_1 = 'mpa_dr7_unique'
    catalogue_2 = 'nyu_vagc_dr7'
  
    f_1 =  h5py.File(filepath_1+catalogue_1+'.hdf5', 'r')
    dset_1 = f_1.get(catalogue_1)
    dset_1 = np.array(dset_1)
    #print(dset_1.dtype.names)

    f_2 =  h5py.File(filepath_2+catalogue_2+'.hdf5', 'r')
    dset_2 = f_2.get(catalogue_2)
    dset_2 = np.array(dset_2)
    #print(dset_2.dtype.names)
    
    #open matching files.  these are created with the 'match_to_NYU_VAGC.py' script. 
    filename = 'matches_into_nyu_vagc.npy'
    match_1 = np.load(filepath_1+'matches/'+filename)
    filename = 'nyu_vagc_matched_to_mpa.npy'
    match_2 = np.load(filepath_1+'matches/'+filename)
    
    N_col_1 = len(dset_1.dtype.descr)
    N_col_2 = len(dset_2.dtype.descr[8:]) #number of columns used from NYU VAGC
    
    names_1 = dset_1.dtype.names
    names_2 = dset_2.dtype.names[8:]
    
    dtype = np.dtype(dset_1.dtype.descr + dset_2.dtype.descr[8:])
    
    combined_data = np.recarray((len(dset_1),),dtype=dtype)
    combined_data.fill(-99)
    
    for name in names_1:
        print(name)
        combined_data[name] = dset_1[name]
    
    for name in names_2:
        print(name)
        combined_data[name][match_1] = dset_2[name][match_2]
    
    filename = 'mpa_nyu_vagc_dr7'
    savepath = filepath_1
    f = h5py.File(savepath+filename+'.hdf5', 'w')
    dset = f.create_dataset(filename, data=combined_data)


if __name__ == '__main__':
  main()