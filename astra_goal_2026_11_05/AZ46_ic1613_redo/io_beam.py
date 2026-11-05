#!/usr/bin/env python3
"""Bounded FITS metadata/row reads and physical beam kernels for AZ46."""
import json,math,os,re
from pathlib import Path
import numpy as np
from astropy.io import fits

def atomic(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def metadata(path):
    with fits.open(path,memmap=True,lazy_load_hdus=True) as h:
        header=h[0].header.copy();offset=h.fileinfo(0)['datLoc']
    if header['BITPIX']!=-32 or header.get('BSCALE',1)!=1 or header.get('BZERO',0)!=0:
        raise ValueError('Only unscaled32-bit float primary images supported')
    if any(header.get('NAXIS'+str(i),1)!=1 for i in range(4,header['NAXIS']+1)):
        raise ValueError('Unexpected non-singleton additional FITS axis')
    return header,offset

def clean_beam(header):
    lines=[x for x in header.get('HISTORY',[]) if 'CLEAN BMAJ=' in x]
    if not lines:raise ValueError('Missing CLEAN beam record')
    match=re.search(r'BMAJ=\s*([\d.E+-]+) BMIN=\s*([\d.E+-]+) BPA=\s*([\d.E+-]+)',lines[-1])
    if match is None:raise ValueError('Malformed CLEAN beam record')
    beam=np.array([float(x) for x in match.groups()]);beam[:2]*=3600
    if not np.all(np.isfinite(beam)) or np.min(beam[:2])<=0:raise ValueError('Invalid beam')
    return beam

def rows(path,header,offset,plane=0,row_chunk=32):
    """Yield full-width float64 row chunks, never loading the full cube."""
    if row_chunk<1:raise ValueError('Positive row chunk required')
    nx,ny=header['NAXIS1'],header['NAXIS2'];nz=header.get('NAXIS3',1)
    if not 0<=plane<nz:raise ValueError('Plane outside image')
    with Path(path).open('rb') as f:
        f.seek(offset+plane*nx*ny*4)
        for lo in range(0,ny,row_chunk):
            count=min(row_chunk,ny-lo);raw=f.read(count*nx*4)
            if len(raw)!=count*nx*4:raise ValueError('Truncated FITS payload')
            yield lo,np.frombuffer(raw,dtype='>f4').reshape(count,nx).astype('f8')

def beam_kernel(ny,nx,pixel_arcsec,beam,sub=5):
    """Pixel-integrated CLEAN Gaussian, normalized for discrete convolution.

    Subpixel quadrature performs the spatial box averaging once. Do not add
    a second Gaussian pixel-box variance before this integration. Index x
    runs west, y north; beam PA is east of north. Kernel origin is FFT zero.
    """
    if min(ny,nx,sub)<1 or pixel_arcsec<=0:raise ValueError('Invalid beam grid')
    bmaj,bmin,pa=beam;sigmas=np.array([bmaj,bmin])/math.sqrt(8*math.log(2))
    if np.min(sigmas)<=0:raise ValueError('Invalid beam width')
    p=math.radians(pa);yy,xx=np.meshgrid(np.fft.fftfreq(ny)*ny,np.fft.fftfreq(nx)*nx,indexing='ij')
    kernel=np.zeros((ny,nx))
    for oy in (np.arange(sub)+.5)/sub-.5:
        for ox in (np.arange(sub)+.5)/sub-.5:
            east=-(xx+ox)*pixel_arcsec;north=(yy+oy)*pixel_arcsec
            u=east*math.sin(p)+north*math.cos(p);v=-east*math.cos(p)+north*math.sin(p)
            kernel+=np.exp(-.5*((u/sigmas[0])**2+(v/sigmas[1])**2))
    return kernel/kernel.sum()
