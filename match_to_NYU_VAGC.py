#!/usr/bin/python

#Author: Duncan Campbell
#Written: January 21, 2015
#Yale University
#Description: find the matches in the NYU_VAGC

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
    
    print("number of objects in MPA-JHU catalogue: {0}".format(len(dset_1)))
    print("number of objects in NYU catalogue: {0}".format(len(dset_2)))
    
    da = 1/3600.0 * 2.0 #match length is 2"
    ind1, ind2, ds = cu.spherematch(dset_1['RA'], dset_1['DEC'],\
                                    dset_2['RA'], dset_2['DEC'],\
                                    tol=da, nnearest=1)
    
    print("minimum angular seperation: {0}''".format(np.min(ds)*3600.0))
    print("maximum angular seperation: {0}''".format(np.max(ds)*3600.0))
    print("number of matchs: {0}".format(len(ind1)))
    
    print(dset_1[ind1]['Z'])
    print(dset_2[ind2]['Z'])
    
    #save matching file
    filename = 'matches_into_nyu_vagc'
    np.save(filepath_1+'matches/'+filename,ind1)
    filename = 'nyu_vagc_matched_to_mpa'
    np.save(filepath_1+'matches/'+filename,ind1)


if __name__ == '__main__':
  main()
