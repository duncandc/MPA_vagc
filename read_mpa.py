#!/usr/bin/python

#Author: Duncan Campbell
#Written: July 9, 2013
#Yale University
#Description: Read in fits mpa catalogues and save as HDF5 files.

###packages###
import numpy as np
from astropy.io import fits
from astropy.io import ascii
import h5py
import gc
import custom_utilities as cu


def main():

    filepath = cu.get_data_path() + 'mpa_DR7_catalogue/'
    savepath = cu.get_output_path() + 'processed_data/mpa_dr7/'
    #################################################################

    catalogues=['gal_totspecsfr_dr7_v5_2.fits','gal_info_dr7_v5_2.fits','totlgm_dr7_v5_2.fits']

    filename = catalogues[0]
    hdulist1 = fits.open(filepath+filename, memmap=True)
    data1 = hdulist1[1].data
    print 'saving as:', savepath+filename[:-5]+'.hdf5'
    f1 = h5py.File(savepath+filename[:-5]+'.hdf5', 'w')
    dset1 = f1.create_dataset(filename[:-5], data=data1)
    
    filename = catalogues[1]
    hdulist2 = fits.open(filepath+filename, memmap=True)
    data2 = hdulist2[1].data
    print 'saving as:', savepath+filename[:-5]+'.hdf5'
    f2 = h5py.File(savepath+filename[:-5]+'.hdf5', 'w')
    dset2 = f2.create_dataset(filename[:-5], data=data2)

    dtype1 = dset1.dtype.descr
    dtype2 = dset2.dtype.descr
    
    dtype3 = dtype2+dtype1
    dtype3 = np.dtype(dtype3)

    print dtype3
    print len(dset1), len(dset2)

    data3 = np.recarray((len(dset2),), dtype=dtype3)
    for name in dset2.dtype.descr:
        name = name[0]
        print name
        data3[name]=dset2[name]
    for name in dset1.dtype.descr:
        name = name[0]
        print name
        data3[name]=dset1[name]

    filename = 'gal_info_gal_totspecsfr_dr7_v5_2'
    print savepath+filename+'.hdf5'
    f3 = h5py.File(savepath+filename+'.hdf5', 'w')
    dset3 = f3.create_dataset(filename, data=data3)
    
    print "reading total stellar mass catalogue now."
    
    filename = catalogues[2]
    hdulist1 = fits.open(filepath+filename, memmap=True)
    data1 = hdulist1[1].data
    print 'saving as:', savepath+filename[:-5]+'.hdf5'
    f1 = h5py.File(savepath+filename[:-5]+'.hdf5', 'w')
    dset1 = f1.create_dataset(filename[:-5], data=data1)

    dtype1 = dset1.dtype.descr
    dtype2 = dset2.dtype.descr
    
    print dtype1
    print dtype2
    
    dtype3 = dtype2+dtype1
    dtype3 = np.dtype(dtype3)

    print dtype3
    print len(dset1), len(dset2)

    data3 = np.recarray((len(dset2),), dtype=dtype3)
    for name in dset2.dtype.descr:
        name = name[0]
        print name
        data3[name]=dset2[name]
    for name in dset1.dtype.descr:
        name = name[0]
        print name
        data3[name]=dset1[name]

    filename = 'gal_info_totlgm_dr7_v5_2'
    print savepath+filename+'.hdf5'
    f3 = h5py.File(savepath+filename+'.hdf5', 'w')
    dset3 = f3.create_dataset(filename, data=data3)

    


    

if __name__ == '__main__':
  main()
