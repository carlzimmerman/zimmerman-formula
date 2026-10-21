"""Conditional symplectic ell2,m0 coordinate from a CEPAIR1 snapshot.

No field evolution or automatic merger/mode-energy claim. Canonical order is
(u,s,chi,v,t), unit no-half mode K=1, and harmonic Y20 has unit angular norm.
"""
from pathlib import Path
import argparse
import json
import math
import struct

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import CubicHermiteSpline
from scipy.ndimage import map_coordinates, gaussian_filter1d
from scipy.signal import find_peaks

MAGIC = b'CEPAIR1\0'
HEADER = struct.Struct('<8siidd')
FIELD_NAMES = ('Psi_re','Psi_im','X_re','X_im','chi',
               'Psi_vel_re','Psi_vel_im','X_vel_re','X_vel_im','chi_vel')

def read_snapshot(path):
    path = Path(path)
    with path.open('rb') as stream:
        raw = stream.read(HEADER.size)
    if len(raw) != 32:
        raise ValueError('snapshot has no complete32-byte header')
    magic,nr,nz,dx,time = HEADER.unpack(raw)
    if magic != MAGIC or nr < 4 or nz < 8 or not (dx>0 and np.isfinite(dx) and np.isfinite(time)):
        raise ValueError('invalid CEPAIR1 little-endian header')
    expected = 32+10*nr*nz*8
    if path.stat().st_size != expected:
        raise ValueError('snapshot byte count does not match header')
    if nr*nz*8*40 > 750_000_000:
        raise ValueError('declared analysis workspace estimate exceeds750MB')
    fields = np.memmap(path,dtype='<f8',mode='r',offset=32,shape=(10,nz,nr))
    return {'path':str(path),'Nr':nr,'Nz':nz,'dx':dx,'time':time,'fields':fields,
            'rho':(np.arange(nr)+.5)*dx,
            'z':(np.arange(nz)+.5-nz/2)*dx}

def load_reference(mode_path, profile_path, Qref=None):
    with np.load(mode_path) as mode:
        r=mode['r'].copy(); Z=mode['mode'].copy()
        omega=float(mode['omega']); Omega=float(mode['Omega'])
        Q=float(mode['Q']); kappa=float(mode['K_normalization'])
        cache_fields=mode['background_fields'].copy()
    with np.load(profile_path) as profile:
        rp=profile['r'].copy(); yp=profile['y'].copy(); Qp=float(profile['Q'])
    if Qref is not None and abs(Q-float(Qref))>1e-8:
        raise ValueError('requested Qref differs from mode-cache charge')
    if abs(Q-Qp)>1e-8 or Z.shape!=(5,len(r)) or yp.shape!=(7,len(rp)):
        raise ValueError('reference/cache shape or charge mismatch')
    dr=float(np.median(np.diff(r)))
    if np.max(abs(np.diff(r)-dr))>1e-10 or r[0]<=0 or abs(kappa-1)>1e-7:
        raise ValueError('requires the uniform reduced radial unit-K mode cache')
    fs=CubicHermiteSpline(rp,yp[0],yp[1],extrapolate=False)
    bs=CubicHermiteSpline(rp,yp[2],yp[3],extrapolate=False)
    hs=CubicHermiteSpline(rp,yp[4],yp[5],extrapolate=False)
    def background(radius):
        radius=np.asarray(radius)
        safe=np.clip(radius,rp[0],rp[-1]); inside=(radius>=rp[0])&(radius<=rp[-1])
        return np.array([np.where(inside,spline(safe),0.) for spline in (fs,bs,hs)])
    mismatch=float(np.max(abs(background(r)-cache_fields)))
    return {'r':r,'dr':dr,'Z':Z,'omega':omega,'Omega':Omega,'Q':Q,'kappa':kappa,
            'background':background,'profile_L':float(rp[-1]),
            'profile_vs_mode_background_max_abs':mismatch,
            'mode_path':str(mode_path),'profile_path':str(profile_path)}

def _inventory_and_fit(snap,ref,fit_radius,apertures,center_z):
    rho=snap['rho']; zz=snap['z']-center_z; dx=snap['dx']; data=snap['fields']
    total_q=0.; positive_q=0.; negative_q=0.; total_weight=0.
    q_ap=np.zeros(len(apertures)); w_ap=np.zeros(len(apertures))
    cpsi=0j; cx=0j; phase_den=0.; phase_norm=0.
    frequency_num=0.; frequency_den=0.; fit_volume=0.
    for first in range(0,snap['Nz'],32):
        sl=slice(first,min(first+32,snap['Nz']))
        d=np.asarray(data[:,sl,:])
        if not np.all(np.isfinite(d)):
            raise ValueError('nonfinite snapshot field')
        rad=np.sqrt(rho[None,:]**2+zz[sl,None]**2)
        vol=2*math.pi*rho[None,:]*dx*dx
        psi=d[0]+1j*d[1]; xx=d[2]+1j*d[3]
        psit=d[5]+1j*d[6]; xt=d[7]+1j*d[8]
        charge=2*np.imag(psi.conj()*psit)+4*np.imag(xx.conj()*xt)
        weight=abs(psi)**2+4*abs(xx)**2
        total_q+=float(np.sum(vol*charge)); total_weight+=float(np.sum(vol*weight))
        positive_q+=float(np.sum(vol*np.maximum(charge,0.)))
        negative_q+=float(np.sum(vol*np.minimum(charge,0.)))
        for k,ap in enumerate(apertures):
            mask=rad<=ap
            q_ap[k]+=float(np.sum(vol*charge*mask)); w_ap[k]+=float(np.sum(vol*weight*mask))
        mask=rad<=fit_radius
        f,b,h=ref['background'](rad)
        vv=vol*mask
        cpsi+=np.sum(vv*f*psi); cx+=np.sum(vv*b*xx)
        phase_den+=float(np.sum(vv*f*f)); phase_norm+=float(np.sum(vv*abs(psi)**2))
        frequency_num+=float(np.sum(vv*(np.imag(psi.conj()*psit)+2*np.imag(xx.conj()*xt))))
        frequency_den+=float(np.sum(vv*(abs(psi)**2+4*abs(xx)**2)))
        fit_volume+=float(np.sum(np.broadcast_to(vol,rad.shape)*mask))
    if frequency_den<=0 or abs(cpsi)==0:
        raise ValueError('core overlap does not define a carrier phase/frequency')
    phase=float(np.angle(cpsi)); omega_fit=frequency_num/frequency_den
    coherence=float(abs(cpsi)**2/max(phase_den*phase_norm,1e-300))
    x_lock=float(np.angle(cx*np.exp(-2j*phase))) if abs(cx)>0 else None
    line=abs(np.asarray(data[0,:,0])+1j*np.asarray(data[1,:,0]))**2
    line+=4*abs(np.asarray(data[2,:,0])+1j*np.asarray(data[3,:,0]))**2
    smooth=gaussian_filter1d(line,max(.25,.5/dx),mode='nearest')
    peaks,_=find_peaks(smooth,prominence=.1*float(smooth.max()),distance=max(1,int(1/dx)))
    return {'total_Noether_Q_in_box':total_q,'positive_Q_in_box':positive_q,
            'negative_Q_in_box':negative_q,'positive_carrier_weight_in_box':total_weight,
            'aperture_charge':[{'radius':float(ap),'Q':float(q),
                              'Q_fraction_of_box':float(q/total_q) if total_q else None,
                              'positive_carrier_weight_fraction':float(w/total_weight) if total_weight else None}
                             for ap,q,w in zip(apertures,q_ap,w_ap)],
            'phase_fit':phase,'omega_fit':float(omega_fit),'Psi_reference_overlap_coherence':coherence,
            'X_shared_phase_lock_residual_radians':x_lock,'fit_volume':fit_volume,
            'axis_carrier_density_peak_count':int(len(peaks)),
            'axis_carrier_density_peak_z':[float(snap['z'][p]) for p in peaks],
            'morphology_definition':'Near-axis |Psi|²+4|X|²; Gaussian width0.5,10% prominence, minimum separation1. Diagnostic only; aperture charge is not automatically bound stock.'}

def _sample_spheres(snap,r,mu,center_z,order):
    if order not in (1,3):
        raise ValueError('interpolation_order must be1 or3')
    rho=r[:,None]*np.sqrt(1-mu[None,:]**2)
    zz=center_z+r[:,None]*mu[None,:]
    pad=2 if order==3 else 1
    coords=np.array([zz/snap['dx']+snap['Nz']/2-.5,
                     rho/snap['dx']-.5+pad])
    sampled=[]
    for field in snap['fields']:
        # Even reflection across the regular rho=0 axis; no outer/z clamping.
        padded=np.concatenate([field[:,:pad][:,::-1],field],axis=1)
        val=map_coordinates(padded,coords,order=order,mode='constant',cval=np.nan,
                            prefilter=(order==3))
        if not np.all(np.isfinite(val)):
            raise ValueError('projection sphere left available snapshot cells')
        sampled.append(val)
    return np.array(sampled)

def analyze_snapshot(path,mode_path,profile_path,Qref=None,*,fit_radius=12.,
                     apertures=(8.,12.,16.,24.,32.),center_z=0.,angular_nodes=48,
                     interpolation_order=3,carrier_frequency=None,carrier_phase=None):
    """Return conditional coordinates/diagnostics; write nothing and evolve nothing.

    omega_fit includes the correct charge-two X weight. An override is explicit
    and reported. The gyro projection always uses the pinned mode-reference
    omega; a frame/reference mismatch is reported, never silently retuned.
    """
    snap=read_snapshot(path); ref=load_reference(mode_path,profile_path,Qref)
    if fit_radius<=0 or fit_radius>=ref['profile_L'] or angular_nodes<12:
        raise ValueError('invalid fit radius/angular quadrature')
    inv=_inventory_and_fit(snap,ref,fit_radius,apertures,center_z)
    theta=inv['phase_fit'] if carrier_phase is None else float(carrier_phase)
    omega_used=inv['omega_fit'] if carrier_frequency is None else float(carrier_frequency)
    margin=2.1*snap['dx'] if interpolation_order==3 else 1.1*snap['dx']
    cap=min(snap['rho'][-1]-margin,
            snap['z'][-1]-center_z-margin,center_z-snap['z'][0]-margin,
            ref['r'][-1])
    keep=ref['r']<=cap
    if np.count_nonzero(keep)<20:
        raise ValueError('snapshot too small for a modal coordinate')
    r=ref['r'][keep]; Z=ref['Z'][:,keep]; dr=ref['dr']; Om=ref['Omega']
    mu,weights=leggauss(angular_nodes)
    sample=_sample_spheres(snap,r,mu,center_z,interpolation_order)
    psi=(sample[0]+1j*sample[1])*np.exp(-1j*theta)
    xx=(sample[2]+1j*sample[3])*np.exp(-2j*theta)
    psit=(sample[5]+1j*sample[6])*np.exp(-1j*theta)-1j*omega_used*psi
    xt=(sample[7]+1j*sample[8])*np.exp(-2j*theta)-2j*omega_used*xx
    f,b,h=ref['background'](r)
    canonical=np.array([math.sqrt(2)*(psi.real-f[:,None]),
                        math.sqrt(2)*(xx.real-b[:,None]),sample[4]-h[:,None],
                        math.sqrt(2)*psi.imag,math.sqrt(2)*xx.imag])
    velocity=np.array([math.sqrt(2)*psit.real,math.sqrt(2)*xt.real,sample[9],
                       math.sqrt(2)*psit.imag,math.sqrt(2)*xt.imag])
    Y20=math.sqrt(5/(16*math.pi))*(3*mu*mu-1)
    factor=2*math.pi*weights*Y20
    q=r[None,:]*np.sum(canonical*factor[None,None,:],axis=2)
    v=r[None,:]*np.sum(velocity*factor[None,None,:],axis=2)
    Gq=np.zeros_like(q); om=ref['omega']
    Gq[0]=-2*om*q[3];Gq[1]=-4*om*q[4]
    Gq[3]=2*om*q[0];Gq[4]=4*om*q[1]
    c=-1j*Om/ref['kappa']*dr*np.sum(Z.conj()*(v+Gq+1j*Om*q))
    qrec=2*np.real(c*Z); vrec=2*np.real(1j*Om*c*Z)
    norm=float(dr*np.sum(Om*Om*q*q+v*v))
    residual=float(dr*np.sum(Om*Om*(q-qrec)**2+(v-vrec)**2))
    support=float(np.sum(abs(Z)**2)/np.sum(abs(ref['Z'])**2))
    mismatch=float(2*math.pi*dr*np.sum(r[:,None]**2*weights[None,:]
                                     *np.sum(canonical**2,axis=0)))
    background_norm=float(4*math.pi*dr*np.sum(r*r*(2*f*f+2*b*b+h*h)))
    return {'scope':'Conditional canonical ell2,m0 coordinate about the supplied reference; not automatically persistent mode energy or proof of merger/capture.',
            'snapshot':str(path),'time':snap['time'],'Nr':snap['Nr'],'Nz':snap['Nz'],'dx':snap['dx'],
            'Q_reference':ref['Q'],'omega_reference':om,'Omega_reference':Om,
            'carrier_phase_used':theta,'carrier_frequency_used':omega_used,
            'carrier_frequency_minus_mode_reference':omega_used-om,
            'carrier_phase_override':carrier_phase is not None,
            'carrier_frequency_override':carrier_frequency is not None,
            'core_fit_radius':fit_radius,'center_z_used':center_z,
            'projection_radius_max':float(r[-1]),'radial_nodes_used':len(r),
            'angular_nodes':angular_nodes,'interpolation_order':interpolation_order,
            'mode_canonical_L2_fraction_inside_projection':support,
            'profile_vs_mode_background_max_abs':ref['profile_vs_mode_background_max_abs'],
            'coordinate_real':float(c.real),'coordinate_imag':float(c.imag),
            'conditional_K_coordinate':float(abs(c)**2),
            'ell2_positive_state_norm':norm,'ell2_reconstruction_state_residual':residual,
            'ell2_reconstruction_state_residual_fraction':residual/max(norm,1e-300),
            'full_canonical_field_mismatch_relative_L2':math.sqrt(mismatch/max(background_norm,1e-300)),
            'inventory_and_carrier_fit':inv,
            'limits':['No one-core or stationary-reference acceptance is imposed automatically',
                      'Aperture Q is not automatically bound charge or physical mass',
                      'Coordinate modulus squared is mode K only for a valid matched linear reference',
                      'Residual is a positive q/velocity state norm, not an unassigned energy',
                      'Static and nonlinear harmonics can contaminate an instantaneous coordinate',
                      'No merger excitation, radiative efficiency or orbital-J claim from one snapshot']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot');parser.add_argument('mode');parser.add_argument('profile')
    parser.add_argument('--output');parser.add_argument('--Qref',type=float)
    parser.add_argument('--fit-radius',type=float,default=12.)
    parser.add_argument('--interpolation-order',type=int,default=3)
    args=parser.parse_args()
    result=analyze_snapshot(args.snapshot,args.mode,args.profile,Qref=args.Qref,
                            fit_radius=args.fit_radius,interpolation_order=args.interpolation_order)
    encoded=json.dumps(result,indent=2)+'\n'
    if args.output:Path(args.output).write_text(encoded)
    else:print(encoded,end='')
