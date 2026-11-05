#!/usr/bin/env python3
"""Row-chunked V-image profile; fixed geometry and constant-M/L assumptions."""
import math,warnings
import numpy as np
from astropy.wcs import WCS,FITSFixedWarning
import io_beam as B
RA=(1+4/60+49.6/3600)*15;DEC=2+8/60+14.1/3600
class YieldRequested(Exception):pass

def profile(path,ring,row_chunk=32,stop=lambda:False):
    header,offset=B.metadata(path)
    # Preserve Astropy's original coordinate interpretation and record its repairs.
    with warnings.catch_warnings(record=True) as records:
        warnings.simplefilter('always',FITSFixedWarning)
        w=WCS(header)
    repairs=[str(item.message) for item in records]
    nring=int(math.ceil(1188/ring))
    values=[[] for _ in range(nring)];background=[];p=math.radians(73.7);ci=math.cos(math.radians(48.))
    for lo,image in B.rows(path,header,offset,row_chunk=row_chunk):
        if stop():raise YieldRequested('Stellar profile interrupted; restart this bounded stage')
        yy,xx=np.mgrid[lo:lo+len(image),0:header['NAXIS1']]
        sky=w.pixel_to_world(xx.ravel(),yy.ravel())
        east=((sky.ra.deg-RA)*math.cos(math.radians(DEC))*3600).reshape(image.shape)
        north=((sky.dec.deg-DEC)*3600).reshape(image.shape)
        major=east*math.sin(p)+north*math.cos(p);minor=(-east*math.cos(p)+north*math.sin(p))/ci
        radius=np.hypot(major,minor);finite=np.isfinite(image)
        background.append(image[finite&(radius>1500)])
        idx=np.floor(radius/ring).astype(int)
        for k in np.unique(idx[finite&(idx<nring)]):values[k].append(image[finite&(idx==k)])
    bg=np.concatenate(background)
    if len(bg)==0:raise ValueError('No background pixels outside1500arcsec')
    bkg=float(np.median(bg));counts=[];light=np.zeros(nring)
    for k,chunks in enumerate(values):
        v=np.concatenate(chunks) if chunks else np.empty(0);counts.append(len(v))
        if len(v)>20:light[k]=np.median(v)-bkg
    bad=np.flatnonzero(light<=0);cut=int(bad[0]) if len(bad) else nring
    light[cut:]=0.;r=(np.arange(nring)+.5)*ring;pc=.73e6*math.pi/(180*3600)
    norm=float(np.sum(light*2*math.pi*r*ring)*pc**2)
    if norm<=0:raise ValueError('No positive stellar profile after frozen truncation')
    half=float(np.interp(.5,np.cumsum(light*r)/np.sum(light*r),r))
    return dict(wcs_header_repairs=repairs,ring_arcsec=ring,radius_arcsec=r.tolist(),profile_counts=light.tolist(),normalization=norm,
                background=bkg,background_pixels=len(bg),annulus_pixels=counts,profile_cut_arcsec=cut*ring,
                half_light_arcsec=half,distance_Mpc=.73,geometry=dict(ra=RA,dec=DEC,pa=73.7,inc=48.),
                scope='Uncalibrated V-profile shape with constant M/L, normalized later to the two frozen stellar masses; both a0 footings share this input')
