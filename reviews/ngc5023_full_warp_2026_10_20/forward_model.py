"""Deterministic optically-thin angular tilted-ring/spiral forward renderer.

This reconstructs the stated published model family; it is not TiRiFiC and
does not claim recovery of its preferred parameter file or fit posterior.
"""
import copy
import json
import math
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.ndimage import map_coordinates
from scipy.signal import fftconvolve

HERE=Path(__file__).resolve().parent
KPC_PER_ARCSEC=6.6e3*np.pi/648000  # only converts published lag units
BEAMS={'HR':(19.103587791336,13.422298617648,.383774966002),
       'LR':(35.515860468156,33.281349018228,8.65270614624),
       'WHISP':(18.114047893054,12.3021393772,0.),'C40':(40.,40.,0.)}


def load_preferred():
    disk=json.loads((HERE/'recovery/digitization_run002/ring_profiles.json').read_text())['profiles']
    arms=json.loads((HERE/'spiral/run002/profiles.json').read_text())
    p={'radius':np.maximum(disk['radius_arcsec'],0).tolist(),
       'inc_sw':disk['inclination_approaching_SW_deg'],'inc_ne':disk['inclination_receding_NE_deg'],
       'pa_sw':disk['PA_approaching_SW_deg'],'pa_ne':disk['PA_receding_NE_deg'],
       'v_sw':disk['VROT_both_sides_km_s'],'v_ne':disk['VROT_both_sides_km_s'],
       'sbr_sw':disk['SBR_both_sides_Jy_km_s_arcsec2'],'sbr_ne':disk['SBR_both_sides_Jy_km_s_arcsec2'],
       'h':[9.1,14.,9.], 'lag_km_s_arcsec':9.4*KPC_PER_ARCSEC,
       'dispersion_total_km_s':10.,'vsys_sw':404.8,'vsys_ne':404.8,
       'center_east_arcsec':.28451546,'center_north_arcsec':-.4286636,
       'vertical':'exponential','support_arcsec':360.,'interpolation':'linear',
       'arm_wedge_deg':360.,'clip_negative_rotation':False,
       'label':'published preferred disk+two arms+lag reconstructed from Figures11/12 and Table4',
       'exact_preferred_model_recovered':False}
    for key in ['inc_sw','inc_ne']:p[key]=[88.5 if i<10 else float(v) for i,v in enumerate(p[key])]
    for key in ['pa_sw','pa_ne']:p[key]=[28. if i<10 else float(v) for i,v in enumerate(p[key])]
    for j in [1,2]:
        ar=arms['arm'+str(j)]
        p['arm'+str(j)]={'width':ar['width_arcsec'],'phase':ar['phase_deg_approaching_CCW'],
            'sbr':ar['amplitude_Jy_km_s_arcsec2']}
    return p


def load_author_base():
    fields={}
    for line in (HERE/'recovery/pyHIARD_NGC_5023.def').read_text().splitlines():
        if '=' not in line:continue
        key,value=line.split('=',1)
        try:fields[key.strip()]=[float(s) for s in value.split()]
        except ValueError:pass
    p=load_preferred();p['label']='author public BaseModel-hr; actual parameters, not preferred spiral model'
    p['radius']=fields['RADI'];p['support_arcsec']=fields['RADI'][-1]
    for root,card in [('inc','INCL'),('pa','PA'),('v','VROT'),('sbr','SBR')]:
        p[root+'_sw']=fields[card];p[root+'_ne']=fields[card+'_2']
    p['h']=[fields['Z0'][0],1.,1.]
    for j in [1,2]:p['arm'+str(j)]['sbr']=[0.]*20
    p['vsys_sw']=fields['VSYS'][0];p['vsys_ne']=fields['VSYS_2'][0]
    p['lag_km_s_arcsec']=0.;p['dispersion_total_km_s']=fields['CONDISP'][0]
    p['center_east_arcsec']=(fields['XPOS'][0]-198.04918172867)*3600*np.cos(np.deg2rad(44.038146851))
    p['center_north_arcsec']=(fields['YPOS'][0]-44.038146851)*3600
    return p


def vertical_nodes(kind,n=12):
    if kind=='exponential':
        q,w=np.polynomial.laguerre.laggauss(n)
        return np.r_[-q[::-1],q],np.r_[w[::-1],w]/2
    # These are explicit alternative scale conventions, not source LTYPE recovery.
    if kind=='gaussian':
        q,w=np.polynomial.hermite.hermgauss(2*n)
        return np.sqrt(2)*q,w/np.sqrt(np.pi)  # scale is Gaussian sigma
    q,w=np.polynomial.legendre.leggauss(2*n)
    if kind=='sech2':return np.arctanh(q),w/2
    if kind=='uniform':return q,w/2  # scale is half-thickness
    raise ValueError(kind)


def interp(values,r,p):
    if p['interpolation']=='nearest':
        rr=np.asarray(p['radius']);ids=np.abs(r[:,None]-rr[None,:]).argmin(1)
        return np.asarray(values)[ids]
    return np.interp(r,p['radius'],values)


def deposit(x,z,u,weight,ds,dv,shape):
    coords=[u/dv+(shape[0]-1)/2,z/ds+(shape[1]-1)/2,x/ds+(shape[2]-1)/2]
    return deposit_index(coords,weight,shape)


def deposit_index(coords,weight,shape):
    ii=[np.floor(q).astype(np.int64) for q in coords]
    ff=[q-i for q,i in zip(coords,ii)]
    result=np.zeros(math.prod(shape),dtype=np.float64)
    valid_weight=0.
    for a in [0,1]:
        for b in [0,1]:
            for c in [0,1]:
                k,j,i=ii[0]+a,ii[1]+b,ii[2]+c
                w=weight*(ff[0] if a else 1-ff[0])*(ff[1] if b else 1-ff[1])*(ff[2] if c else 1-ff[2])
                ok=(k>=0)&(k<shape[0])&(j>=0)&(j<shape[1])&(i>=0)&(i<shape[2])
                index=(k[ok]*shape[1]+j[ok])*shape[2]+i[ok]
                result+=np.bincount(index,weights=w[ok],minlength=len(result))
                valid_weight+=w[ok].sum()
    return result.reshape(shape),valid_weight


class NativeObservation:
    """Project/deposit/convolve/sample in the real native HALOGAS WCS."""
    def __init__(self,beam,refinement):
        import sys
        old=HERE.parent/'ngc5023_cube_2026_10_20'
        if str(old) not in sys.path:sys.path.insert(0,str(old))
        from cube_io import read_fits,ncp_pixel,tangent_world,velocity_axis,beam_covariance_pixels
        self.ncp,self.tangent=ncp_pixel,tangent_world
        self.h,raw,_=read_fits(old/'data'/('NGC5023-'+beam+'-cube.fits'))
        self.v=velocity_axis(self.h);self.f=refinement
        self.ref=(198.04918172867,44.038146851)
        cx,cy=ncp_pixel(self.h,*self.ref)
        self.x0,self.y0=int(cx)-96,int(cy)-96
        self.shape=(len(self.v)*refinement,192*refinement,192*refinement)
        self.native_dv=float(np.diff(self.v).mean());self.dv=self.native_dv/refinement
        self.ds=abs(self.h['CDELT1'])*3600/refinement
        self.cov=beam_covariance_pixels(self.h)*refinement**2
        xx,zz=np.meshgrid(np.arange(150)*4.-298.,np.arange(60)*4.-118.)
        angle=np.deg2rad(28.)
        e,n=xx*np.sin(angle)+zz*np.cos(angle),xx*np.cos(angle)-zz*np.sin(angle)
        ra,dec=tangent_world(*self.ref,e,n);px,py=ncp_pixel(self.h,ra,dec)
        vv=(np.arange(60)-29.5)*4.12+404.8
        kk=(vv-self.v[0])/self.native_dv
        self.sample_coords=np.array([np.broadcast_to((kk[:,None,None]+.5)*refinement-.5,(60,60,150)),
           np.broadcast_to(((py[None,:,:]-self.y0)+.5)*refinement-.5,(60,60,150)),
           np.broadcast_to(((px[None,:,:]-self.x0)+.5)*refinement-.5,(60,60,150))])

    def observe(self,x,z,u,weight,sigma,compensate):
        a=np.deg2rad(28.)
        e,n=x*np.sin(a)+z*np.cos(a),x*np.cos(a)-z*np.sin(a)
        ra,dec=self.tangent(*self.ref,e,n);px,py=self.ncp(self.h,ra,dec)
        kk=(u+404.8-self.v[0])/self.native_dv
        coords=[(kk+.5)*self.f-.5,((py-self.y0)+.5)*self.f-.5,((px-self.x0)+.5)*self.f-.5]
        hist,kept=deposit_index(coords,weight,self.shape)
        cov=self.cov-(np.eye(2)/6 if compensate else 0)
        radius=int(np.ceil(5.5*np.sqrt(np.linalg.eigvalsh(cov).max())))
        gy,gx=np.mgrid[-radius:radius+1,-radius:radius+1]
        pts=np.stack([gx,gy],axis=-1)
        kernel=np.exp(-.5*np.einsum('...i,ij,...j->...',pts,np.linalg.inv(cov),pts));kernel/=kernel.sum()
        sv=np.sqrt(sigma**2-(self.dv**2/6 if compensate else 0))/self.dv
        hist=gaussian_filter1d(hist,sv,axis=0,mode='constant',truncate=5.5)
        for k in range(len(hist)):hist[k]=fftconvolve(hist[k],kernel,mode='same')
        hist/=self.ds**2*self.dv
        target=map_coordinates(hist,self.sample_coords,order=1,mode='constant',cval=np.nan,prefilter=False)
        assert np.isfinite(target).all()
        return target.astype(np.float32),kept


def beam_kernel(beam,ds,compensate=True):
    major,minor,pa=beam;angle=np.deg2rad(pa-28.)
    a=np.array([np.cos(angle),np.sin(angle)]);b=np.array([-np.sin(angle),np.cos(angle)])
    cov=(major/2.354820045)**2*np.outer(a,a)+(minor/2.354820045)**2*np.outer(b,b)
    if compensate:cov-=np.eye(2)*ds**2/6
    assert np.linalg.eigvalsh(cov).min()>0
    radius=int(np.ceil(5.5*np.sqrt(np.linalg.eigvalsh(cov).max())/ds))
    zz,xx=np.mgrid[-radius:radius+1,-radius:radius+1]*ds
    pt=np.stack([xx,zz],axis=-1)
    k=np.exp(-.5*np.einsum('...i,ij,...j->...',pt,np.linalg.inv(cov),pt));k/=k.sum()
    return k


def render(p,beam='HR',refinement=1,dr=6.,nphi=256,nz=10,compensate=True,native=True):
    ds,dv=4./refinement,4.12/refinement
    shape=(90*refinement,110*refinement,210*refinement)
    nr=int(np.ceil(p['support_arcsec']/dr));dr=p['support_arcsec']/nr
    r=(np.arange(nr)+.5)*dr
    phi=(np.arange(nphi)+.5)*2*np.pi/nphi
    rr,pp=np.meshgrid(r,phi,indexing='ij');flat_r,flat_phi=rr.ravel(),pp.ravel()
    rec=np.cos(flat_phi)>=0
    sw=lambda k:np.repeat(interp(p[k+'_sw'],r,p),nphi)
    ne=lambda k:np.repeat(interp(p[k+'_ne'],r,p),nphi)
    inc=np.deg2rad(np.where(rec,ne('inc'),sw('inc')))
    beta=np.deg2rad(np.where(rec,ne('pa'),sw('pa'))-28)
    vrot=np.where(rec,ne('v'),sw('v'))
    vsys=np.where(rec,p['vsys_ne'],p['vsys_sw'])-404.8
    surface=np.where(rec,ne('sbr'),sw('sbr'))
    q,wz=vertical_nodes(p['vertical'],nz)
    area=flat_r*dr*(2*np.pi/nphi)
    east,north=p['center_east_arcsec'],p['center_north_arcsec']
    a0=np.deg2rad(28.);cx=east*np.sin(a0)+north*np.cos(a0);cz=east*np.cos(a0)-north*np.sin(a0)
    kernel=beam_kernel(BEAMS[beam],ds,compensate)
    observation=NativeObservation(beam,refinement) if native else None
    total_sigma=p['dispersion_total_km_s']
    sig=np.sqrt(total_sigma**2-(dv**2/6 if compensate else 0))/dv
    components=[];meta=[]
    for comp in range(3):
        s=surface.copy()
        if comp:
            arm=p['arm'+str(comp)]
            width=np.repeat(interp(arm['width'],r,p),nphi)
            phase=np.deg2rad(np.repeat(interp(arm['phase'],r,p),nphi))+np.pi
            delta=(flat_phi-phase+np.pi)%(2*np.pi)-np.pi
            sigma=np.maximum(width,1e-6)/flat_r
            s=np.repeat(interp(arm['sbr'],r,p),nphi)*np.exp(-.5*(delta/sigma)**2)
            if p['arm_wedge_deg']<360:s*=abs(delta)<=np.deg2rad(p['arm_wedge_deg']/2)
        h=p['h'][comp]*q[None,:]
        A=flat_r[:,None]*np.cos(flat_phi)[:,None]
        B=flat_r[:,None]*np.sin(flat_phi)[:,None]*np.cos(inc)[:,None]
        xx=A*np.cos(beta)[:,None]-B*np.sin(beta)[:,None]+h*np.sin(beta)[:,None]*np.sin(inc)[:,None]+cx
        zz=A*np.sin(beta)[:,None]+B*np.cos(beta)[:,None]-h*np.cos(beta)[:,None]*np.sin(inc)[:,None]+cz
        speed=vrot[:,None]-p['lag_km_s_arcsec']*abs(h)
        if p['clip_negative_rotation']:speed=np.maximum(speed,0)
        uu=vsys[:,None]+speed*np.sin(inc)[:,None]*np.cos(flat_phi)[:,None]
        weight=(s*area)[:,None]*wz[None,:]
        if native:
            target,kept=observation.observe(xx.ravel(),zz.ravel(),uu.ravel(),weight.ravel(),total_sigma,compensate)
        else:
            hist,kept=deposit(xx.ravel(),zz.ravel(),uu.ravel(),weight.ravel(),ds,dv,shape)
            hist=gaussian_filter1d(hist,sig,axis=0,mode='constant',truncate=5.5)
            for k in range(shape[0]):hist[k]=fftconvolve(hist[k],kernel,mode='same')
            if refinement>1:
                f=refinement
                hist=hist.reshape(90,f,110,f,210,f).sum((1,3,5))
            hist=hist/(4.**2*4.12)
            target=hist[15:75,25:85,30:180].astype(np.float32)
        components.append(target)
        meta.append({'component':comp,'intrinsic_integrated_flux_Jy_km_s':float(weight.sum()),
          'deposited_fraction':float(kept/max(weight.sum(),1e-30)),
          'sampled_aperture_flux_Jy_km_s':float(target.sum()*16*4.12),
          'negative_rotation_weight_fraction':float(weight[speed<0].sum()/max(weight.sum(),1e-30))})
    return np.array(components),{'components':meta,'internal_shape':observation.shape if native else shape,'ds_arcsec':ds,'dv_km_s':dv,
        'radial_step_arcsec':dr,'azimuth_points':nphi,'vertical_nodes_each_side':nz,
        'CIC_variance_compensated':compensate,'dispersion_includes_instrument_once':True,
        'native_WCS_beam_sampling':native}


def perturb(p,**kwargs):
    p=copy.deepcopy(p)
    for key,value in kwargs.items():p[key]=value
    return p
