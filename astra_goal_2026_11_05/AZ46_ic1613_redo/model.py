#!/usr/bin/env python3
"""AZ46 beam-aware FN4a model family, with physical domains fixed across rungs."""
import importlib.util,json,math
from pathlib import Path
import numpy as np
from scipy import ndimage
import io_beam as B
import raw_cube as R
OLD=R.ROOT/'finish_2026_11_04/FN4_galaxy_rows_data/FN4a_ic1613_cube_model/fn4a_core.py'
spec=importlib.util.spec_from_file_location('az46_readonly_fn4a_core',OLD);C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
A0={'canonical':9.3603e-11,'alt':1.1312e-10}

def load_prepared(relative):
    directory=R.HERE/relative;manifest=json.loads((directory/'prep_manifest.json').read_text())
    for name,h in manifest['identity']['hashes'].items():
        if R.sha(R.ROOT/name)!=h:raise RuntimeError('Changed preparation source/input')
    stages={}
    for name,item in manifest['stages'].items():
        path=directory/(name+'.json')
        if R.sha(path)!=item['sha256']:raise RuntimeError('Changed stage manifest')
        obj=json.loads(path.read_text());stages[name]=obj['scientific']
        if obj['identity']!=manifest['identity']:raise RuntimeError('Mixed preparation identities')
        for file,h in obj['outputs'].items():
            if R.sha(directory/file)!=h:raise RuntimeError('Changed prepared array')
    raw=R.HERE/manifest['raw_source'];rm=json.loads((raw/'raw_manifest.json').read_text())
    if R.sha(raw/'raw_manifest.json')!=manifest['identity']['raw_manifest_sha256']:raise RuntimeError('Changed raw manifest')
    for path,h in rm['identity']['hashes'].items():
        if R.sha(R.ROOT/path)!=h:raise RuntimeError('Changed raw source/input')
    for path,h in rm['output_hashes'].items():
        if R.sha(raw/path)!=h:raise RuntimeError('Changed raw output')
    load=lambda root,name:np.load(root/name,mmap_mode='r',allow_pickle=False)
    lo,hi=stages['mask']['channels'];sl=slice(lo,hi+1)
    stars=stages['stars'];rings=stages['rings']
    return dict(cube=load(raw,'cube.npy')[sl],v=load(raw,'velocity.npy')[sl],mask=load(directory,'mask_mask.npy')[sl],
                grid=load(directory,'mask_lattice.npy')[sl],mom0=load(directory,'mask_intensity.npy'),
                XE=load(raw,'east.npy'),YN=load(raw,'north.npy'),gas_sky=load(directory,'maps_gas_sky.npy'),
                star_R=np.array(stars['radius_arcsec']),star_prof=np.array(stars['profile_counts']),star_norm=stars['normalization'],
                R_out=rings['R_out_arcsec'],nring=rings['nring'],ring_width=rings['ring_width_arcsec'],
                initial_ring_R=load(directory,'rings_radius.npy'),initial_ring_V=load(directory,'rings_rotation.npy'),
                noise=stages['mask']['noise_Jy_per_beam'],beam=stages['mask']['beam_arcsec_deg'],pixel=stages['mask']['pixel_arcsec'],
                native_channel_range=[lo,hi],native_shape=rm['scientific']['shape'],binning=manifest['binning'],weight=manifest['weight'],
                manifest_sha256=R.sha(directory/'prep_manifest.json'))

class Cube:
    def __init__(self,P,data=None,sub=5):
        self.D=np.asarray(P['cube'] if data is None else data);self.v=np.asarray(P['v']);self.mask=np.asarray(P['mask']);self.grid=np.asarray(P['grid'])
        self.XE=np.asarray(P['XE']);self.YN=np.asarray(P['YN']);self.sig=float(P['noise']);self.pixel=np.array(P['pixel']);self.beam=P['beam']
        if not math.isclose(self.pixel[0],self.pixel[1],rel_tol=1e-10):raise ValueError('Square pixels required by the inherited model')
        self.nk,self.ny,self.nx=self.D.shape;self.I=np.maximum(np.asarray(P['mom0']),0).copy()
        # Fixed24arcsec border equals the old four6arcsec pixels.
        border=max(1,int(math.ceil(24/self.pixel[0])));self.I[:border]=0;self.I[-border:]=0;self.I[:,:border]=0;self.I[:,-border:]=0
        self.otf=np.fft.rfft2(B.beam_kernel(self.ny,self.nx,float(self.pixel[0]),self.beam,sub))
        self.Sobs=(self.D*self.mask).sum(0);self.sel=self.grid&self.mask;self.ndat=int(self.sel.sum())
        # Original Gaussian instrumental-width convention at the native channel spacing.
        self.sig_inst=2*float(np.median(abs(np.diff(self.v))))/2.355
    def model(self,vlos,sigma):
        effective=np.sqrt(sigma**2+self.sig_inst**2)
        line=self.I[None]*np.exp(-.5*((self.v[:,None,None]-vlos[None])/effective[None])**2)
        convolved=np.fft.irfft2(np.fft.rfft2(line)*self.otf[None],s=(self.ny,self.nx))
        summed=(convolved*self.mask).sum(0);factor=np.zeros_like(summed)
        np.divide(self.Sobs,summed,out=factor,where=(self.Sobs>0)&(summed>0))
        return convolved*factor[None]
    def residual(self,vlos,sigma):return ((self.D-self.model(vlos,sigma))/self.sig)[self.sel]

class Baryons:
    """FN4a in-plane FFT and azimuthal average, parameterized by actual pixel size."""
    def __init__(self,P,mstar):
        self.gas=np.asarray(P['gas_sky']);self.XE=np.asarray(P['XE']);self.YN=np.asarray(P['YN']);self.pixel=float(P['pixel'][0])
        self.sR=np.asarray(P['star_R']);self.sprof=np.asarray(P['star_prof'])*(mstar/P['star_norm'])
        self.n=int(2000/self.pixel)|1;axis=(np.arange(self.n)-self.n//2)*self.pixel;self.FX,self.FY=np.meshgrid(axis,axis,indexing='xy')
        self.pad=1<<int(math.ceil(math.log2(2*self.n)));self.kernels={}
    def kernel(self,thickness):
        if thickness not in self.kernels:
            d=C.arcsec_to_pc(self.pixel);axis=np.fft.fftfreq(self.pad)*self.pad;y,x=np.meshgrid(axis,axis,indexing='ij');rx=x*d;ry=y*d
            r3=(rx**2+ry**2+thickness**2)**1.5
            self.kernels[thickness]=(np.fft.rfft2(-rx/r3),np.fft.rfft2(-ry/r3))
        return self.kernels[thickness]
    def face_on(self,x0,y0,pa,inc):
        p=math.radians(pa);ci=math.cos(math.radians(inc));a=self.FX;b=self.FY*ci
        east=x0+a*math.sin(p)-b*math.cos(p);north=y0+a*math.cos(p)+b*math.sin(p)
        ix=(east-self.XE[0,0])/(self.XE[0,1]-self.XE[0,0]);iy=(north-self.YN[0,0])/(self.YN[1,0]-self.YN[0,0])
        gas=ndimage.map_coordinates(self.gas,[iy,ix],order=1,mode='constant',cval=0)*ci
        radius=np.hypot(self.FX,self.FY);stars=np.interp(radius,self.sR,self.sprof,right=0.)
        return gas,stars,radius
    def vc2(self,x0,y0,pa,inc,a0,modified=True,thickness=200.,radii=None):
        gas,stars,radius=self.face_on(x0,y0,pa,inc);density=gas+stars;d=C.arcsec_to_pc(self.pixel)
        kx,ky=self.kernel(thickness);fourier=np.fft.rfft2(density,s=(self.pad,self.pad))
        gx=np.fft.irfft2(fourier*kx,s=(self.pad,self.pad))[:self.n,:self.n]*C.GPC*d*d
        gy=np.fft.irfft2(fourier*ky,s=(self.pad,self.pad))[:self.n,:self.n]*C.GPC*d*d
        inward=-(gx*self.FX+gy*self.FY)/np.maximum(radius,1e-9)
        # Fixed960arcsec physical range;160 radial bins at the original6arcsec rung.
        if radii is None:radii=(np.arange(int(math.ceil(960/self.pixel)))+.5)*self.pixel
        edges=np.r_[0,.5*(radii[1:]+radii[:-1]),radii[-1]+.5*(radii[-1]-radii[-2])]
        idx=np.digitize(radius.ravel(),edges)-1;ok=(idx>=0)&(idx<len(radii));counts=np.bincount(idx[ok],minlength=len(radii))
        mean=np.bincount(idx[ok],weights=inward.ravel()[ok],minlength=len(radii))/np.maximum(counts,1)
        gsum=np.bincount(idx[ok],weights=gas.ravel()[ok],minlength=len(radii))/np.maximum(counts,1)
        gN=np.maximum(mean,0)*C.KMS2_PC_TO_SI;g=C.law_g(gN,a0) if modified else gN
        return radii,g/C.KMS2_PC_TO_SI*C.arcsec_to_pc(radii),gsum
