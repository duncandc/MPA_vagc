#!/usr/bin/python

#Author: Duncan Campbell
#Written: January 19, 2015
#Yale University
#Description: remove duplicates in MPA-JHU catalogue, choosing the observation with 
#    highest S/N

###packages###
import numpy as np
from astropy.io import ascii
import h5py
import custom_utilities as cu

def main():
    
    ######################################################################################
    savepath = cu.get_output_path() + 'processed_data/mpa_dr7/'
    ######################################################################################

    #open catalogue
    catalogue = 'mpa_dr7'
    filepath = cu.get_output_path() + 'processed_data/mpa_dr7/'
    f =  h5py.File(filepath+catalogue+'.hdf5', 'r')
    dset = f.get(catalogue)
    print dset.dtype.names
    
    
    filepath = cu.get_data_path() + 'mpa_DR7_catalogue/'
    f = open(filepath + "all_matches_dr7.dat",'r')
    highest_sn_inds = []
    
    #from progressbar import ProgressBar
    #pbar = ProgressBar().start()
    for i, line in enumerate(f):
        inds = np.array([int(entry) for entry in line.split()])
        keep = (inds>-1)
        inds = inds[keep]
        max_ind = inds[np.argmax(dset['SN_MEDIAN'][inds])]
        highest_sn_inds.append(max_ind)
        #print i
    #pbar.finish()
    
    unique_objects = np.unique(highest_sn_inds)
    
    #save indices as numpy array
    np.save(savepath + 'unique_objects.npz', unique_objects)
    
    #save indices as ascii table
    from astropy.table import Table
    data = Table([unique_objects], names=['ind'])
    ascii.write(data, savepath + 'unique_objects.dat')
    
    #save a catalogue with only unique galaxies
    data = dset[unique_objects]
    filename = 'mpa_dr7_unique'
    f1 = h5py.File(savepath+filename+'.hdf5', 'w')
    dset1 = f1.create_dataset(filename, data=data)


if __name__ == '__main__':
  main()
