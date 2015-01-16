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
    
    filename = catalogues[2]
    hdulist3 = fits.open(filepath+filename, memmap=True)
    data3 = hdulist3[1].data
    print 'saving as:', savepath+filename[:-5]+'.hdf5'
    f3 = h5py.File(savepath+filename[:-5]+'.hdf5', 'w')
    dset3 = f3.create_dataset(filename[:-5], data=data3)

    dtype1 = dset1.dtype.descr
    dtype2 = dset2.dtype.descr
    
    dtype12 = dtype2+dtype1
    dtype12 = np.dtype(dtype12)

    print dtype12
    print len(dset1), len(dset2)

    data12 = np.recarray((len(dset2),), dtype=dtype12)
    for name in dset2.dtype.descr:
        name = name[0]
        print name
        data12[name]=dset2[name]
    for name in dset1.dtype.descr:
        name = name[0]
        print name
        data12[name]=dset1[name]

    filename = 'gal_info_gal_totspecsfr_dr7_v5_2'
    print savepath+filename+'.hdf5'
    f12 = h5py.File(savepath+filename+'.hdf5', 'w')
    dset12 = f12.create_dataset(filename, data=data12)

    dtype3 = dset3.dtype.descr
    dtype2 = dset2.dtype.descr
    
    print dtype3
    print dtype2
    
    dtype32 = dtype2+dtype3
    dtype32 = np.dtype(dtype32)

    print dtype32
    print len(dset3), len(dset2)

    data32 = np.recarray((len(dset2),), dtype=dtype32)
    for name in dset2.dtype.descr:
        name = name[0]
        print name
        data32[name]=dset2[name]
    for name in dset3.dtype.descr:
        name = name[0]
        print name
        data32[name]=dset3[name]

    filename = 'gal_info_totlgm_dr7_v5_2'
    print savepath+filename+'.hdf5'
    f32 = h5py.File(savepath+filename+'.hdf5', 'w')
    dset32 = f32.create_dataset(filename, data=data32)
    
    
    print "making combined master catalogue"
    
    #alter column names for these two
    dtype1_c = []
    dtype3_c = []
    for i in range(len(dtype1)):
        dtype1_c.append(('sfr_'+dtype1[i][0],dtype1[i][1]))
    for i in range(len(dtype3)):
        dtype3_c.append(('sm_'+dtype3[i][0], dtype3[i][1]))
        
    dtype1 = np.dtype(dtype1_c)
    dtype3 = np.dtype(dtype3_c)
    
    dtype123 = dtype2 + dtype3_c + dtype1_c
    dtype123 = np.dtype(dtype123)

    print dtype123
    print len(dset3), len(dset2), len(dset1) 

    data123 = np.recarray((len(dset2),), dtype=dtype123)
    for name in dset2.dtype.descr:
        name = name[0]
        print name
        data123[name]=dset2[name]
    original_descr = dset1.dtype.descr
    for i,name in enumerate(dtype1.descr):
        name = name[0]
        original_name = original_descr[i][0]
        print name, original_name
        data123[name]=dset1[original_name]
    original_descr = dset3.dtype.descr
    for i,name in enumerate(dtype3.descr):
        name = name[0]
        original_name = original_descr[i][0]
        print name, original_name
        data123[name]=dset3[original_name]
    
    filename = 'mpa_dr7'
    print savepath+filename+'.hdf5'
    f123 = h5py.File(savepath+filename+'.hdf5', 'w')
    dset123 = f123.create_dataset(filename, data=data123)
    

    


    

if __name__ == '__main__':
  main()
