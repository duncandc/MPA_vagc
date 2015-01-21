#!/usr/bin/python

#Author: Duncan Campbell
#Written: January 19, 2015
#Yale University
#Description: remove duplicates in MPA-JHU catalogue, choosing the observation with 
#  highest S/N.  Warning, this contains some list comprehension voodoo, but it makes it 
#  infinity faster.

###packages###
import numpy as np
from astropy.io import ascii
import h5py
import custom_utilities as cu
import sys

def main():
    
    ######################################################################################
    savepath = cu.get_output_path() + 'processed_data/mpa_dr7/'
    ######################################################################################

    #open catalogue
    catalogue = 'mpa_dr7'
    filepath = cu.get_output_path() + 'processed_data/mpa_dr7/'
    f =  h5py.File(filepath+catalogue+'.hdf5', 'r')
    dset = f.get(catalogue)
    dset = np.array(dset)
    print dset.dtype.names
    
    print "number of entries in the catalogue:", len(np.unique(dset['SN_MEDIAN']))
    
    filepath = cu.get_data_path() + 'mpa_DR7_catalogue/'
    f = open(filepath + "all_matches_dr7.dat",'r')
    highest_sn_inds = []
    
    #read in lines as a list of stings
    lines = [line for line in f]
    print "number of lines:", len(lines)
    
    #split lines into entries
    values = [line.split() for line in lines]
    
    #convert strings into integers and remove negative integers
    values = [[int(y) for y in x if int(y)>-1] for x in values]
    
    #put them in order for each line
    values = [np.sort(x) for x in values]
    
    #how may entries per object?
    N = [1.0/len(x) for x in values]
    print "total number of unique objects:", np.sum(N) #doesn't agree with quoted value!
    
    #which value in each line gives the highest S/N?
    max_inds = [np.argmax(dset['SN_MEDIAN'][inds]) for inds in values]
    
    #get a list of the indices of the highest S/N objects per entry
    highest_sn_inds = [x[y] for x,y in zip(values,max_inds)]
    
    #remove duplicates
    unique_objects = np.unique(highest_sn_inds)
    
    #save indices as numpy array
    np.save(savepath + 'unique_objects', unique_objects)
    
    #save indices as ascii table
    from astropy.table import Table
    data = Table([unique_objects], names=['ind'])
    ascii.write(data, savepath + 'unique_objects.dat')
    ascii.write(data, './unique_objects.dat')
    
    #save a catalogue with only unique galaxies
    inds = np.arange(0,len(dset))
    keep = np.in1d(inds,unique_objects)
    data = dset[keep]
    filename = 'mpa_dr7_unique'
    f1 = h5py.File(savepath+filename+'.hdf5', 'w')
    dset1 = f1.create_dataset(filename, data=data)


if __name__ == '__main__':
  main()
