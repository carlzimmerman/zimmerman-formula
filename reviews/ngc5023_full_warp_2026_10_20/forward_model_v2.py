"""Versioned renderer: resolve arbitrarily narrow arms by truncated-normal quadrature.

Fine-grid models are anchored on native image/channel centers, restricted
back to those centers, then passed through the same native-analysis sampler.
Version1 and all its evidence remain unchanged.
"""
import math
import numpy as np
from scipy.ndimage import gaussian_filter1d,map_coordinates
from scipy.signal import fftconvolve
from scipy.special import ndtr,ndtri
from forward_model import load_preferred,load_author_base,interp,vertical_nodes,NativeObservation,deposit_index


class Observation(NativeObservation):
    def __init__(self,beam,refinement):
        super().__init__(beam,refinement)
        self.sample_coords=(self.sample_coords+.5)/self.f-.5
        self.shape=tuple((n-1)*self.f+1 for n in (len(self.v),192,192))

    def observe(self,x,z,u,weight,sigma,compensate):
        a=np.deg2rad(28.)
        ra,dec=self.tangent(*self.ref,x*np.sin(a)+z*np.cos(a),x*np.cos(a)-z*np.sin(a))
        px,py=self.ncp(self.h,ra,dec);kk=(u+404.8-self.v[0])/self.native_dv
        coords=[kk*self.f,(py-self.y0)*self.f,(px-self.x0)*self.f]
        hist,kept=deposit_index(coords,weight,self.shape)
        cov=self.cov-(np.eye(2)/6 if compensate else 0)
        radius=int(np.ceil(5.5*np.sqrt(np.linalg.eigvalsh(cov).max())))
        gy,gx=np.mgrid[-radius:radius+1,-radius:radius+1]
        pts=np.stack([gx,gy],axis=-1)
        kernel=np.exp(-.5*np.einsum('...i,ij,...j->...',pts,np.linalg.inv(cov),pts));kernel/=kernel.sum()
        sv=np.sqrt(sigma**2-(self.dv**2/6 if compensate else 0))/self.dv
        hist=gaussian_filter1d(hist,sv,axis=0,mode='constant',truncate=5.5)
        for k in range(len(hist)):hist[k]=fftconvolve(hist[k],kernel,mode='same')
        self.last_postconvolution_flux=float(hist.sum())
        hist/=self.ds**2*self.dv
        if self.f>1:
            hist=hist[::self.f,::self.f,::self.f]
        result=map_coordinates(hist,self.sample_coords,order=1,mode='constant',cval=np.nan,prefilter=False)
        assert np.isfinite(result).all()
        return result.astype(np.float32),kept


def component_geometry(p,r,comp,nphi,narm):
    if comp==0:
        ph=(np.arange(nphi)+.5)*2*np.pi/nphi
        rr,phi=np.meshgrid(r,ph,indexing='ij')
        flat_r,flat_phi=rr.ravel(),phi.ravel()
        rec=np.cos(flat_phi)>=0
        s=np.where(rec,np.repeat(interp(p['sbr_ne'],r,p),nphi),np.repeat(interp(p['sbr_sw'],r,p),nphi))
        angular_weight=np.full(len(flat_r),2*np.pi/nphi)
    else:
        arm=p['arm'+str(comp)]
        # A zero-width arm with a finite peak has exactly zero angular flux.
        width=np.maximum(interp(arm['width'],r,p),0.)
        sigma=width/r
        phase=np.deg2rad(interp(arm['phase'],r,p))+np.pi
        g,w=np.polynomial.legendre.leggauss(narm)
        radii,phis,surfaces,weights=[],[],[],[]
        peaks=interp(arm['sbr'],r,p)
        half=np.deg2rad(p['arm_wedge_deg']/2)
        for ri,ph,sg,peak in zip(r,phase,sigma,peaks):
            if sg==0:
                radii.append(np.array([ri]));phis.append(np.array([ph]))
                surfaces.append(np.array([peak]));weights.append(np.array([0.]));continue
            lo,hi=ph-half,ph+half
            first=int(np.ceil((lo-np.pi/2)/np.pi))
            last=int(np.floor((hi-np.pi/2)/np.pi))
            # Split at every side boundary: half-disk geometry is discontinuous.
            cuts=[lo]+[np.pi/2+k*np.pi for k in range(first,last+1) if lo<np.pi/2+k*np.pi<hi]+[hi]
            for left,right in zip(cuts[:-1],cuts[1:]):
                c0,c1=ndtr((left-ph)/sg),ndtr((right-ph)/sg)
                probability=c1-c0
                if probability<=0:continue
                q=ndtri(np.clip(c0+(g+1)/2*probability,np.nextafter(0.,1.),np.nextafter(1.,0.)))
                radii.append(np.full(narm,ri));phis.append(ph+sg*q)
                surfaces.append(np.full(narm,peak))
                weights.append(sg*np.sqrt(2*np.pi)*probability*w/2)
        flat_r=np.concatenate(radii);flat_phi=np.concatenate(phis)
        s=np.concatenate(surfaces);angular_weight=np.concatenate(weights)
    return flat_r,flat_phi,s,angular_weight


def render(p,beam='HR',refinement=1,dr=6.,nphi=256,narm=64,nz=10,compensate=True):
    observation=Observation(beam,refinement)
    nr=int(np.ceil(p['support_arcsec']/dr));dr=p['support_arcsec']/nr
    r=(np.arange(nr)+.5)*dr
    q,wz=vertical_nodes(p['vertical'],nz)
    east,north=p['center_east_arcsec'],p['center_north_arcsec'];a0=np.deg2rad(28.)
    cx=east*np.sin(a0)+north*np.cos(a0);cz=east*np.cos(a0)-north*np.sin(a0)
    components=[];meta=[]
    for comp in range(3):
        rr,phi,s,angle_weight=component_geometry(p,r,comp,nphi,narm)
        rec=np.cos(phi)>=0
        def sides(key):return np.where(rec,interp(p[key+'_ne'],rr,p),interp(p[key+'_sw'],rr,p))
        inc=np.deg2rad(sides('inc'));beta=np.deg2rad(sides('pa')-28);vrot=sides('v')
        vsys=np.where(rec,p['vsys_ne'],p['vsys_sw'])-404.8
        h=p['h'][comp]*q[None,:]
        A=rr[:,None]*np.cos(phi)[:,None];B=rr[:,None]*np.sin(phi)[:,None]*np.cos(inc)[:,None]
        xx=A*np.cos(beta)[:,None]-B*np.sin(beta)[:,None]+h*np.sin(beta)[:,None]*np.sin(inc)[:,None]+cx
        zz=A*np.sin(beta)[:,None]+B*np.cos(beta)[:,None]-h*np.cos(beta)[:,None]*np.sin(inc)[:,None]+cz
        speed=vrot[:,None]-p['lag_km_s_arcsec']*abs(h)
        if p['clip_negative_rotation']:speed=np.maximum(speed,0)
        uu=vsys[:,None]+speed*np.sin(inc)[:,None]*np.cos(phi)[:,None]
        weight=(s*rr*dr*angle_weight)[:,None]*wz[None,:]
        target,kept=observation.observe(xx.ravel(),zz.ravel(),uu.ravel(),weight.ravel(),p['dispersion_total_km_s'],compensate)
        flux=float(weight.sum())
        meta.append({'component':comp,'intrinsic_integrated_flux_Jy_km_s':flux,
          'deposited_fraction_before_convolution':float(kept/max(flux,1e-30)),
          'postconvolution_nativeROI_flux_Jy_km_s':observation.last_postconvolution_flux,
          'sampled_aperture_flux_Jy_km_s':float(target.sum()*16*4.12),
          'negative_rotation_weight_fraction':float(weight[speed<0].sum()/max(flux,1e-30))})
        components.append(target)
    return np.array(components),{'components':meta,'native_shape':observation.shape,
        'radial_step_arcsec':dr,'uniform_disk_azimuth_points':nphi,'arm_truncated_normal_nodes_per_halfdisk_segment':narm,
        'vertical_nodes_each_side':nz,'refinement':refinement,'CIC_mean_variance_compensated':compensate,
        'native_analysis_interpolator_reapplied_after_refinement':True,
        'numerical_scope':'Finite quadrature/refinement comparisons, not a uniform certified integration bound.'}
