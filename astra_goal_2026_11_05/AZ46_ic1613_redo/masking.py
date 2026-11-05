#!/usr/bin/env python3
"""Frozen physical mask/noise/lattice operations, independent for each cube."""
import math
import numpy as np
from scipy import ndimage

def robust_std(a):
    a=np.asarray(a);a=a[np.isfinite(a)]
    if not len(a):raise ValueError('No finite noise samples')
    return float(1.4826*np.median(abs(a-np.median(a))))
def retain_components(binary):
    labels,count=ndimage.label(binary);sizes=np.bincount(labels.ravel());sizes[0]=0
    largest=int(sizes.max())
    if not largest:raise ValueError('No above-threshold emission component')
    keep=(sizes>=.01*largest);keep[0]=False
    return keep[labels],dict(components=count,largest=largest,retained_components=int(keep.sum()))
def dilation_kernel(pixel):
    nx=int(math.ceil(12/pixel[0]));ny=int(math.ceil(12/pixel[1]))
    y,x=np.mgrid[-ny:ny+1,-nx:nx+1]
    disk=(x*pixel[0])**2+(y*pixel[1])**2<=12**2
    return np.broadcast_to(disk,(5,*disk.shape)).copy()
def make_mask(cube,pixel,beam):
    if len(cube)<30:raise ValueError('First/last15 noise channels require at least30 channels')
    ends=np.r_[0:15,len(cube)-15:len(cube)]
    noise=robust_std(cube[ends]);smooth=ndimage.gaussian_filter(cube,(0,10.2/pixel[1],10.2/pixel[0]))
    smooth=ndimage.uniform_filter1d(smooth,3,axis=0);smoothed_noise=robust_std(smooth[ends])
    if min(noise,smoothed_noise)<=0:raise ValueError('Nonpositive measured noise')
    core,components=retain_components(smooth>3*smoothed_noise);del smooth
    mask=ndimage.binary_dilation(core,structure=dilation_kernel(pixel))
    indices=np.flatnonzero(mask.any(axis=(1,2)))
    area=math.pi/(4*math.log(2))*beam[0]*beam[1]
    stride=[max(1,int(np.rint(math.sqrt(area)/p))) for p in pixel]
    gy,gx=np.indices(cube.shape[1:]);spatial=(gx%stride[0]==0)&(gy%stride[1]==0)
    lattice=spatial[None]&((np.arange(len(cube))%2==0)[:,None,None])
    intensity=np.maximum(np.sum(cube*mask,axis=0),0.)
    science=dict(noise_Jy_per_beam=noise,smoothed_noise_Jy_per_beam=smoothed_noise,
                 components=components,mask_voxels=int(mask.sum()),sampled_mask_voxels=int((mask&lattice).sum()),
                 channels=[int(indices.min()),int(indices.max())],pixel_arcsec=list(pixel),
                 beam_arcsec_deg=list(beam),beam_area_arcsec2=area,lattice_stride_xy=stride,
                 smoothing_sigma_arcsec=10.2,spectral_box_channels=3,threshold_sigma=3,
                 dilation_radius_arcsec=12,dilation_half_channels=2,
                 lattice_origin='crop pixel0, native channel0',
                 caveat='Approximate beam-sampled chi-square; correlated interferometer pixels are not an exact independent likelihood')
    return dict(mask=mask,lattice=lattice,intensity=intensity),science
