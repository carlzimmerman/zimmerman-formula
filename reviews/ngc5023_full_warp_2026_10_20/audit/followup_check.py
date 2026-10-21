#!/usr/bin/env python3
"""Independent analytic clouds through the frozen older-cube adapter.

Only adapter evaluation imports production code. The reference uses own FITS
header reader, Cartesian tangent geometry, optical velocities and interpolation.
"""
import argparse
import json
from pathlib import Path
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
PACKET=HERE.parent
OLD=PACKET.parent/'ngc5023_cube_2026_10_20'
sys.path.insert(0,str(PACKET))
from followup_model import Observation


def header(path):
    h={}
    with Path(path).open('rb') as stream:
        done=False
        while not done:
            block=stream.read(2880)
            for j in range(0,2880,80):
                card=block[j:j+80].decode('ascii');key=card[:8].strip()
                if key=='END':done=True;break
                if card[8:10]!='= ':continue
                text=card[10:].split('/')[0].strip()
                if text.startswith("'"):h[key]=text.strip(" '")
                elif text in ['T','F']:h[key]=text=='T'
                else:
                    try:h[key]=float(text.replace('D','E'))
                    except ValueError:pass
    return h


def velocities(h):
    k=np.arange(int(h['NAXIS3']))+1-h['CRPIX3']
    if h['CTYPE3']=='VELO-HEL':return (h['CRVAL3']+k*h['CDELT3'])/1000
    frequency=h['CRVAL3']+k*h['CDELT3']
    return h['DRVAL3']+299792.458*1420405752.0*(1/frequency-1/h['CRVAL3'])


def ref(which):
    if which=='WHISP':
        return ((13+9/60+57.8503976860/3600)*15,44+18/60+11.510623991/3600)
    return 198.04918172867,44.038146851


def index_linear(v,desired):
    j=np.searchsorted(v,desired,side='right')-1
    j=np.clip(j,0,len(v)-2)
    return j+(desired-v[j])/(v[j+1]-v[j])


def world_cartesian(reference,east,north):
    a,d=np.deg2rad(reference)
    center=np.array([np.cos(d)*np.cos(a),np.cos(d)*np.sin(a),np.sin(d)])
    er=np.array([-np.sin(a),np.cos(a),0.])
    nr=np.array([-np.sin(d)*np.cos(a),-np.sin(d)*np.sin(a),np.cos(d)])
    s=center+np.asarray(east)[...,None]*np.pi/648000*er+np.asarray(north)[...,None]*np.pi/648000*nr
    s/=np.linalg.norm(s,axis=-1)[...,None]
    return np.arctan2(s[...,1],s[...,0]),np.arcsin(s[...,2])


def native_pixel(h,ra,dec):
    a,d=np.deg2rad([h['CRVAL1'],h['CRVAL2']])
    px=np.cos(dec)*np.sin(ra-a)*180/np.pi/h['CDELT1']+h['CRPIX1']-1
    py=(np.cos(d)-np.cos(dec)*np.cos(ra-a))/np.sin(d)*180/np.pi/h['CDELT2']+h['CRPIX2']-1
    return px,py


def independent_geometry(h,reference):
    a,d=np.deg2rad(reference)
    cx,cy=native_pixel(h,a,d)
    x0,y0=int(cx)-96,int(cy)-96
    y,x=np.mgrid[0:192,0:192]
    xi=np.deg2rad((x+x0+1-h['CRPIX1'])*h['CDELT1'])
    eta=np.deg2rad((y+y0+1-h['CRPIX2'])*h['CDELT2'])
    a0,d0=np.deg2rad([h['CRVAL1'],h['CRVAL2']])
    c=np.cos(d0)-eta*np.sin(d0)
    ra=a0+np.arctan2(xi,c);dec=np.arccos(np.sqrt(xi**2+c**2))
    den=np.sin(dec)*np.sin(d)+np.cos(dec)*np.cos(d)*np.cos(ra-a)
    east=np.cos(dec)*np.sin(ra-a)/den*648000/np.pi
    north=(np.sin(dec)*np.cos(d)-np.cos(dec)*np.sin(d)*np.cos(ra-a))/den*648000/np.pi
    xx,zz=np.meshgrid(np.arange(150)*4.-298.,np.arange(60)*4.-118.)
    angle=np.deg2rad(28.)
    ra,dec=world_cartesian(reference,xx*np.sin(angle)+zz*np.cos(angle),xx*np.cos(angle)-zz*np.sin(angle))
    px,py=native_pixel(h,ra,dec)
    vv=(np.arange(60)-29.5)*4.12+404.8
    kk=index_linear(velocities(h),vv)
    coords=np.array([np.broadcast_to(kk[:,None,None],(60,60,150)),
                     np.broadcast_to(py[None,:,:]-y0,(60,60,150)),
                     np.broadcast_to(px[None,:,:]-x0,(60,60,150))])
    return east,north,coords,x0,y0


def trilinear(a,coords):
    low=np.floor(coords).astype(int);fraction=coords-low
    out=np.zeros(coords.shape[1:])
    for k in [0,1]:
        for j in [0,1]:
            for i in [0,1]:
                w=(fraction[0] if k else 1-fraction[0])*(fraction[1] if j else 1-fraction[1])*(fraction[2] if i else 1-fraction[2])
                out+=w*a[low[0]+k,low[1]+j,low[2]+i]
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True)
    records=[];checks=[];observations={};summary={}
    for which,path in [('HR',OLD/'data/NGC5023-HR-cube.fits'),('LR',OLD/'data/NGC5023-LR-cube.fits'),('WHISP',OLD/'independent/UGC_08286cl_WHISP.fits')]:
        h=header(path);v=velocities(h);E,N,target,x0,y0=independent_geometry(h,ref(which))
        obs1=Observation(which+'40',1)
        checks.append({'name':which+' independently rebuilt sample coordinates','error':float(abs(target-obs1.sample_coords).max()),'tolerance':1e-6})
        checks.append({'name':which+' independently rebuilt velocity axis','error':float(abs(v-obs1.v).max()),'tolerance':1e-9})
        checks.append({'name':which+' positive channels and square pixels','error':int(not (np.all(np.diff(v)>0) and abs(abs(h['CDELT1'])-abs(h['CDELT2']))<1e-12)),'tolerance':0})
        summary[which]={'velocity_endpoints':v[[0,-1]].tolist(),'channel_width_min_max': [float(np.diff(v).min()),float(np.diff(v).max())],
                        'native_pixel_arcsec':abs(h['CDELT1'])*3600,'roi_origin':[x0,y0]}
        cases=[(0.,0.,0.,10.)]
        if which=='WHISP':cases=[(0.,0.,0.,10.),(.7,1.3,2.1,10.),(13.7,-8.1,23.6,10.),(170.3,57.4,38.2,10.),(0.,0.,0.,8.),(0.,0.,0.,12.)]
        for x,z,u,sigma in cases:
            angle=np.deg2rad(28.);e=x*np.sin(angle)+z*np.cos(angle);n=x*np.cos(angle)-z*np.sin(angle)
            spatial=np.exp(-.5*((E-e)**2+(N-n)**2)/(40/2.354820045)**2)/(2*np.pi*(40/2.354820045)**2)
            spectral=np.exp(-.5*((v-404.8-u)/sigma)**2)/(np.sqrt(2*np.pi)*sigma)
            expected=trilinear(.3*spectral[:,None,None]*spatial[None,:,:],target)
            one,k1=obs1.observe(np.array([x]),np.array([z]),np.array([u]),np.array([.3]),sigma,True)
            row={'dataset':which+'40','cloud_major_minor_u_sigma':[x,z,u,sigma],
                 'reference_aperture_flux_Jy_km_s':float(expected.sum()*16*4.12),
                 'f1_aperture_flux_Jy_km_s':float(one.sum()*16*4.12),
                 'f1_deposited_flux_Jy_km_s':float(k1),'f1_native_convolved_flux':obs1.last_postconvolution_flux,
                 'f1_relative_L1_vs_analytic':float(abs(one-expected).sum()/abs(expected).sum())}
            if which=='WHISP' and sigma==10:
                obs2=Observation(which+'40',2)
                two,k2=obs2.observe(np.array([x]),np.array([z]),np.array([u]),np.array([.3]),sigma,True)
                row.update({'f2_aperture_flux_Jy_km_s':float(two.sum()*16*4.12),'f2_deposited_flux_Jy_km_s':float(k2),
                            'f2_relative_L1_vs_analytic':float(abs(two-expected).sum()/abs(expected).sum()),
                            'f1_f2_relative_L1':float(abs(one-two).sum()/abs(expected).sum())})
                del obs2,two
            if which in ['HR','LR']:observations[which]=one
            records.append(row)
    checks.append({'name':'HR40 and LR40 identical native grids/40arcsec response','error':float(abs(observations['HR']-observations['LR']).max()),'tolerance':1e-12})
    for c in checks:c['passed']=bool(c['error']<=c['tolerance'])
    result={'all_coordinate_checks_passed':all(c['passed'] for c in checks),'checks':checks,'records':records,'headers_summary':summary,
            'actual_intensities_read':False,'scope':'Finite independent analytic circular40arcsec Gaussian clouds, actual native WCS/channel axes, own trilinear sampler. No astronomical fit or residual significance. WHISP reference uses optical velocity at every native frequency; adapter uses mean channel width only in convolution/normalization. Finite errors are quantified, not universally certified.'}
    (out/'checks.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))
    return 0 if result['all_coordinate_checks_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
