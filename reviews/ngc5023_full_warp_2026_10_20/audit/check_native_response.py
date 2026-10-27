#!/usr/bin/env python3
"""Compare native renderer response to an independently evaluated analytic cloud."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
PACKET=HERE.parent
sys.path.insert(0,str(PACKET))
from forward_model import NativeObservation


def header(path):
    h={}
    with Path(path).open('rb') as f:
        end=False
        while not end:
            b=f.read(2880)
            for j in range(0,2880,80):
                c=b[j:j+80].decode('ascii');key=c[:8].strip()
                if key=='END':end=True;break
                if c[8:10]!='= ':continue
                v=c[10:].split('/')[0].strip()
                if v.startswith("'"):h[key]=v.strip(" '")
                elif v in ['T','F']:h[key]=v=='T'
                else:
                    try:h[key]=float(v.replace('D','E'))
                    except ValueError:pass
    return h


def sky_native(h,x0,y0):
    y,x=np.mgrid[0:192,0:192]
    xx=np.deg2rad((x+x0+1-h['CRPIX1'])*h['CDELT1'])
    yy=np.deg2rad((y+y0+1-h['CRPIX2'])*h['CDELT2'])
    ra0,dec0=np.deg2rad(h['CRVAL1']),np.deg2rad(h['CRVAL2'])
    c=np.cos(dec0)-yy*np.sin(dec0)
    ra=ra0+np.arctan2(xx,c);dec=np.arccos(np.sqrt(xx*xx+c*c))
    a,d=np.deg2rad(198.04918172867),np.deg2rad(44.038146851)
    den=np.sin(dec)*np.sin(d)+np.cos(dec)*np.cos(d)*np.cos(ra-a)
    e=np.cos(dec)*np.sin(ra-a)/den*648000/np.pi
    n=(np.sin(dec)*np.cos(d)-np.cos(dec)*np.sin(d)*np.cos(ra-a))/den*648000/np.pi
    return e,n


def sample_reference(a,observation):
    # This uses the actual native-analysis coordinates, but implements all
    # eight trilinear weights independently rather than scipy map_coordinates.
    coords=observation.sample_coords
    f=observation.f
    coords=(coords+.5)/f-.5
    low=np.floor(coords).astype(int);frac=coords-low
    out=np.zeros(coords.shape[1:])
    for k in [0,1]:
        for j in [0,1]:
            for i in [0,1]:
                w=(frac[0] if k else 1-frac[0])*(frac[1] if j else 1-frac[1])*(frac[2] if i else 1-frac[2])
                out+=w*a[low[0]+k,low[1]+j,low[2]+i]
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True)
    h=header(PACKET.parent/'ngc5023_cube_2026_10_20/data/NGC5023-HR-cube.fits')
    obs1,obs2=NativeObservation('HR',1),NativeObservation('HR',2)
    E,N=sky_native(h,obs1.x0,obs1.y0)
    a=np.deg2rad(h['BPA']);major=np.array([np.sin(a),np.cos(a)]);minor=np.array([np.cos(a),-np.sin(a)])
    cov=(h['BMAJ']*3600/2.354820045)**2*np.outer(major,major)+(h['BMIN']*3600/2.354820045)**2*np.outer(minor,minor)
    inv=np.linalg.inv(cov)
    v=(h['CRVAL3']+(np.arange(int(h['NAXIS3']))+1-h['CRPIX3'])*h['CDELT3'])/1000
    records=[]
    for x,z,u in [(0.,0.,0.),(.7,1.3,2.1),(13.7,-8.1,23.6),(170.3,57.4,38.2)]:
        pa=np.deg2rad(28);ce=x*np.sin(pa)+z*np.cos(pa);cn=x*np.cos(pa)-z*np.sin(pa)
        pos=np.stack([E-ce,N-cn],axis=-1)
        spatial=np.exp(-.5*np.einsum('...i,ij,...j->...',pos,inv,pos))/(2*np.pi*np.sqrt(np.linalg.det(cov)))
        spectral=np.exp(-.5*((v-404.8-u)/10)**2)/(np.sqrt(2*np.pi)*10)
        reference=.3*spectral[:,None,None]*spatial[None,:,:]
        expected=sample_reference(reference,obs1)
        one,k1=obs1.observe(np.array([x]),np.array([z]),np.array([u]),np.array([.3]),10,True)
        two,k2=obs2.observe(np.array([x]),np.array([z]),np.array([u]),np.array([.3]),10,True)
        val={'cloud_major_minor_u':[x,z,u],'deposited_flux_f1_f2':[float(k1),float(k2)],
            'reference_aperture_flux':float(expected.sum()*16*4.12),
            'f1_aperture_flux':float(one.sum()*16*4.12),'f2_aperture_flux':float(two.sum()*16*4.12),
            'f1_relative_L1_error_vs_analytic_native_observation':float(np.sum(abs(one-expected))/np.sum(abs(expected))),
            'f2_relative_L1_error_vs_analytic_native_observation':float(np.sum(abs(two-expected))/np.sum(abs(expected))),
            'f1_f2_relative_L1_difference':float(np.sum(abs(one-two))/np.sum(abs(expected)))}
        records.append(val)
    result={'records':records,'actual_intensity_data_read':False,
      'scope':'Independent analytic elliptical spatial/Gaussianvelocity cloud evaluated on actual native WCS, then independent trilinear native-analysis sampling. Compare productionNativeObservation finite deposition/response. Uses production targetcoordinate table only, not production deposition/convolution.',
      'interpretation':'Finite response accuracy/sensitivity, not a new observed residual. f2 directly samples fine model and therefore changes native-analysis response; see audit finding.'}
    (out/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
