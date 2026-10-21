#!/usr/bin/env python3
"""Exploratory paired-cube asymmetry, with real-blank and frozen replication controls."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.ndimage import map_coordinates, gaussian_filter1d
from scipy.signal import fftconvolve
from cube_io import read_fits, physical_image, ncp_pixel, tangent_world, velocity_axis, beam_covariance_pixels

HERE = Path(__file__).resolve().parent
X = np.arange(150) * 4.0 - 298.0
Z = np.arange(60) * 4.0 - 118.0
U = (np.arange(60) - 29.5) * 4.12
XC = X.reshape(15, 10).mean(1)
ZC = Z.reshape(6, 10).mean(1)
UC = U.reshape(10, 6).mean(1)
YY, ZZ, XX = np.meshgrid(UC, ZC, XC, indexing='ij')
HALF = XX > 0
KNOWN = [(-72., 80., -24.8, 56.), (112., 92., 39.2, 40.), (120., -76., 39.2, 52.)]
BLANK_CENTERS = [(x, z) for x in [-600., -300., 0., 300., 600.]
                 for z in [-500., -300., 300., 500.]]


def dataset(which):
    if which in ['HR', 'LR']:
        return {'name': which, 'path': HERE/'data'/('NGC5023-'+which+'-cube.fits'),
                'ra': 198.04918172867, 'dec': 44.038146851,
                'unit_to_jy_beam': 1., 'frame': 'ICRS/J2000'}
    return {'name': 'WHISP', 'path': HERE/'independent/UGC_08286cl_WHISP.fits',
            'ra': (13+9/60+57.8503976860/3600)*15,
            'dec': 44+18/60+11.510623991/3600,
            'unit_to_jy_beam': .005, 'frame': 'FK4 B1950'}


class Cube:
    def __init__(self, which, target_fwhm=40.):
        self.spec = dataset(which)
        self.h, raw, self.info = read_fits(self.spec['path'])
        if which == 'WHISP':
            self.h['BMAJ'], self.h['BMIN'], self.h['BPA'] = self.h['BMMAJ']/3600, self.h['BMMIN']/3600, self.h['BMPA']
        self.v = velocity_axis(self.h)
        self.cx, self.cy = ncp_pixel(self.h, self.spec['ra'], self.spec['dec'])
        self.x0, self.y0 = max(0, int(self.cx)-384), max(0, int(self.cy)-384)
        x1, y1 = min(raw.shape[2], int(self.cx)+385), min(raw.shape[1], int(self.cy)+385)
        self.a = physical_image(self.h, raw, (slice(None), slice(self.y0,y1), slice(self.x0,x1)))
        area = math.pi/(4*math.log(2)) * self.h['BMAJ']*self.h['BMIN']*3600**2
        self.a *= self.spec['unit_to_jy_beam']/area  # Jy / square arcsec
        # Per-channel robust spatial baseline from outside the galaxy, retained in metadata.
        sy, sx = np.indices(self.a.shape[1:])
        outside = ((sx+self.x0-self.cx)**2 + (sy+self.y0-self.cy)**2) > (400/(abs(self.h['CDELT1'])*3600))**2
        sample = self.a[:, ::4, ::4][:, outside[::4, ::4]]
        self.baseline = np.nanmedian(sample, axis=1)
        self.a -= self.baseline[:,None,None]
        self.original_fwhm = [self.h['BMAJ']*3600, self.h['BMIN']*3600, self.h['BPA']]
        self.target_fwhm = target_fwhm
        if target_fwhm:
            native_cov = beam_covariance_pixels(self.h)
            target_cov = np.diag([(target_fwhm/(2.354820045*abs(self.h[k])*3600))**2 for k in ['CDELT1','CDELT2']])
            extra = target_cov-native_cov
            assert np.linalg.eigvalsh(extra).min() > 0
            radius = int(math.ceil(5.5*math.sqrt(np.linalg.eigvalsh(extra).max())))
            gy, gx = np.mgrid[-radius:radius+1, -radius:radius+1]
            pts = np.stack([gx,gy],axis=-1)
            kernel = np.exp(-.5*np.einsum('...i,ij,...j->...',pts,np.linalg.inv(extra),pts))
            kernel /= kernel.sum()
            for k in range(len(self.a)):
                finite = np.isfinite(self.a[k])
                weight = fftconvolve(finite.astype(float),kernel,mode='same')
                smoothed = fftconvolve(np.nan_to_num(self.a[k]),kernel,mode='same')
                self.a[k] = np.where(weight > .99999, smoothed/np.maximum(weight,1e-30), np.nan)
        self.metadata = {'source': str(self.spec['path'].relative_to(HERE)),
            'shape': list(raw.shape), 'frame': self.spec['frame'],
            'center_world_deg': [self.spec['ra'],self.spec['dec']],
            'center_native_pixel_zero_based': [float(self.cx),float(self.cy)],
            'native_beam_major_minor_PA': self.original_fwhm,
            'target_circular_fwhm_arcsec': target_fwhm,
            'velocity_range_km_s': [float(self.v.min()),float(self.v.max())],
            'unit_to_Jy_per_native_beam': self.spec['unit_to_jy_beam'],
            'native_baseline_Jy_per_arcsec2': self.baseline.tolist(),
            'native_header_rms': self.h.get('RMS',self.h.get('NOISE')),
            'spectral_response': 'native channel response retained; 24.72 km/s integrated bins; channel covariance calibrated with real blank apertures',
            'interpretation': 'HI brightness and kinematics only; no gravity law or cosmology'}

    def sample(self, dx=0., dz=0., dv=0., pa=28., order=1, warp=None):
        xx, zz = np.meshgrid(X+dx, Z+dz)
        if warp is not None:
            zz = zz + np.interp(X, warp['x'], warp['z'])[None,:]
        p = np.deg2rad(pa)
        east, north = xx*np.sin(p)+zz*np.cos(p), xx*np.cos(p)-zz*np.sin(p)
        ra, dec = tangent_world(self.spec['ra'],self.spec['dec'],east,north)
        px, py = ncp_pixel(self.h,ra,dec)
        px,py = px-self.x0,py-self.y0
        kz = np.interp(U+404.8+dv,self.v,np.arange(len(self.v)))
        assert (U+404.8+dv).min() >= self.v.min() and (U+404.8+dv).max() <= self.v.max()
        coords = np.array([np.broadcast_to(kz[:,None,None],(60,60,150)),
                           np.broadcast_to(py[None,:,:],(60,60,150)),
                           np.broadcast_to(px[None,:,:],(60,60,150))])
        lo = np.floor(coords.reshape(3,-1).min(1)).astype(int)-4
        hi = np.ceil(coords.reshape(3,-1).max(1)).astype(int)+5
        lo = np.maximum(lo,0); hi = np.minimum(hi,self.a.shape)
        local = self.a[lo[0]:hi[0],lo[1]:hi[1],lo[2]:hi[2]]
        return map_coordinates(local,coords-lo[:,None,None,None],order=order,
                               mode='constant',cval=np.nan,prefilter=(order>1))


def bins(a):
    return a.reshape(10,6,6,10,15,10).sum(axis=(1,3,5))*16*4.12


def pair(b):
    return b-b[::-1,::-1,::-1], b+b[::-1,::-1,::-1]


def support(kind):
    m = np.ones(XX.shape,dtype=bool)
    if kind in ['inner','known_removed','candidate_search']:
        m &= abs(XX) <= 175
    if kind in ['known_removed','candidate_search']:
        for x,z,u,w in KNOWN:
            for s in [-1,1]:
                # Conservative rectangular known-feature mask: center within
                # 40arcsec spatially and FWZI/2 + one spectral-bin halfwidth.
                m &= ~((abs(XX-s*x)<=40)&(abs(ZZ-s*z)<=40)&(abs(YY-s*u)<=w/2+12.36))
    if kind == 'candidate_search':
        m &= abs(ZZ) >= 60
    return m


def metrics(b, blanks, mask):
    d,s = pair(b)
    db = blanks-blanks[:,::-1,::-1,::-1]
    sb = blanks+blanks[:,::-1,::-1,::-1]
    m = mask & HALF
    d0,s0 = d[m],s[m]
    bd,bs = db[:,m],sb[:,m]
    d2,s2 = float(np.sum(d0*d0)),float(np.sum(s0*s0))
    noise_d2,noise_s2 = np.mean(np.sum(bd*bd,axis=1)),np.mean(np.sum(bs*bs,axis=1))
    denom = s2-noise_s2
    flux = float(s0.sum())
    return {'paired_bins':int(m.sum()), 'paired_total_flux_Jy_km_s':flux,
      'absolute_asymmetry_raw':float(np.abs(d0).sum()/flux) if flux>0 else None,
      'absolute_blank_subtracted_diagnostic':float((np.abs(d0).sum()-np.mean(np.abs(bd).sum(1)))/flux) if flux>0 else None,
      'squared_asymmetry_noise_corrected':float((d2-noise_d2)/denom) if denom>0 else None,
      'difference_power':d2,'sum_power':s2,
      'blank_difference_power_mean':float(noise_d2),'blank_sum_power_mean':float(noise_s2),
      'blank_power_range':np.quantile(np.sum(bd*bd,axis=1),[0,.5,1]).tolist()}


def blank_samples(cube):
    out,centers = [],[]
    for x,z in BLANK_CENTERS:
        a = cube.sample(dx=x,dz=z)
        if np.isfinite(a).all():
            out.append(bins(a));centers.append([x,z])
    assert len(out)>=8
    return np.array(out),centers


def centroid_warp(a):
    moment = a.sum(0)
    # Data-derived sensitivity control, not an independent model fit.
    use = abs(Z)<=60
    weights = np.maximum(moment[use],0)
    c = (weights*Z[use,None]).sum(0)/np.maximum(weights.sum(0),1e-30)
    c = np.clip(gaussian_filter1d(c,10,mode='nearest'),-30,30)
    return {'x':X.tolist(),'z':c.tolist(),
      'method':'positive-weight centroid within projected |z|<=60arcsec, Gaussian sigma40arcsec along major axis, clipped±30arcsec; exploratory nuisance diagnostic',
      'limitation':'Not published 20-ring warp/spiral forward model; can absorb real emission asymmetry and does not remove line-of-sight mixing.'}


def candidate_value(b,blanks,index):
    d,s = pair(b);db = blanks-blanks[:,::-1,::-1,::-1]
    k,j,i = index
    vals = db[:,k,j,i]
    return {'signed_difference_Jy_km_s':float(d[k,j,i]),
            'paired_sum_Jy_km_s':float(s[k,j,i]),
            'blank_mean':float(vals.mean()),'blank_scatter':float(vals.std(ddof=1)),
            'blank_scatter_units':float((d[k,j,i]-vals.mean())/vals.std(ddof=1)),
            'blank_range':[float(vals.min()),float(vals.max())]}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['discovery','replication'],required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--candidate')
    args=ap.parse_args();out=Path(args.output);out.mkdir(exist_ok=True)
    names=['HR','LR'] if args.phase=='discovery' else ['WHISP']
    result={'phase':args.phase,'exploratory':True,'null':'centrosymmetric source/observation operator',
       'new_physical_parameters':0,'cosmology_used':False,'gravity_law_used':False,
       'bin_widths_arcsec_arcsec_km_s':[40,40,24.72],
       'blank_note':'Overlapping translated real-sky apertures; empirical correlated-noise/processing controls, not independent trials or a formal discovery p-value.',
       'datasets':{}}
    archive={}
    frozen=json.loads(Path(args.candidate).read_text()) if args.candidate else None
    for name in names:
        c=Cube(name,40.)
        a=c.sample();b=bins(a);blanks,bc=blank_samples(c)
        assert np.isfinite(a).all()
        if frozen is None:
            d,s=pair(b);db=blanks-blanks[:,::-1,::-1,::-1]
            sd=db.std(0,ddof=1)
            allowed=support('candidate_search')&HALF
            score=np.where(allowed,abs(d-db.mean(0))/np.maximum(sd,1e-30),-np.inf)
            index=list(np.unravel_index(np.argmax(score),score.shape))
            frozen={'selected_from':'HALOGAS HR only; fixed before opening WHISP intensities',
              'selection':'largest absolute residual in40x40arcsec x24.72km/s bins; x>0,|x|<=175arcsec,|z|>=60arcsec; known features masked',
              'searched_bins':int(allowed.sum()),'index':[int(v) for v in index],
              'x_arcsec':float(XC[index[2]]),'z_arcsec':float(ZC[index[1]]),'u_km_s':float(UC[index[0]]),
              'widths':[40,40,24.72],'vsys_km_s':404.8,'PA_deg':28.,'sign':int(np.sign(d[tuple(index)])),
              'warp_control':centroid_warp(a),
              'replication_rule':'Same frozen signed bin and mirror, at40arcsec beam and same velocity/sky box; no region reselection or sign change. Compare amplitude uncertainty and sensitivity, not merely whether independent map looks similar.'}
            (out/'candidate.json').write_text(json.dumps(frozen,indent=2)+'\n')
        index=frozen['index']
        rec={'metadata':c.metadata,'blank_centers_major_minor_arcsec':bc,
            'baseline':{k:metrics(b,blanks,support(k)) for k in ['all','inner','known_removed','candidate_search']},
            'candidate':candidate_value(b,blanks,index),'controls':[]}
        archive[name+'_aligned40']=a;archive[name+'_binned40']=b;archive[name+'_blanks40']=blanks
        # Nuisance grid; do not reinterpret its minimum as an independently known center.
        for dx in [-8.,-4.,0.,4.,8.]:
            for dz in [-8.,-4.,0.,4.,8.]:
                for dv in [-4.,0.,4.]:
                    bb=bins(c.sample(dx,dz,dv))
                    rec['controls'].append({'kind':'center_vsys','dx_arcsec':dx,'dz_arcsec':dz,'dv_km_s':dv,
                       'candidate':candidate_value(bb,blanks,index),
                       'all':metrics(bb,blanks,support('all')),
                       'masked_inner':metrics(bb,blanks,support('known_removed'))})
        for sign in [-1,1]:
            east=sign*46.37;p=np.deg2rad(28)
            bb=bins(c.sample(dx=east*np.sin(p),dz=east*np.cos(p)))
            rec['controls'].append({'kind':'literal_published_RA_stress','east_arcsec':east,
              'candidate':candidate_value(bb,blanks,index),'all':metrics(bb,blanks,support('all'))})
        for pa in [27.,29.]:
            bb=bins(c.sample(pa=pa))
            rec['controls'].append({'kind':'global_PA_aperture_only','PA_deg':pa,
               'candidate':candidate_value(bb,blanks,index),'all':metrics(bb,blanks,support('all'))})
        cubic=c.sample(order=3);bb=bins(cubic)
        rec['controls'].append({'kind':'cubic_interpolation','candidate':candidate_value(bb,blanks,index),
           'all':metrics(bb,blanks,support('all')),
           'linear_cubic_binned_max_abs_difference':float(np.max(abs(bb-b)))})
        warped=c.sample(warp=frozen['warp_control']);wb=bins(warped)
        rec['controls'].append({'kind':'empirical_dewarp_diagnostic','candidate':candidate_value(wb,blanks,index),
          'all':metrics(wb,blanks,support('all')),'masked_inner':metrics(wb,blanks,support('known_removed'))})
        archive[name+'_dewarped40']=warped
        # Paired moment0 masks from the discovery source; raw signed flux retained.
        signal_map=b.sum(0); noise_maps=blanks.sum(1)
        map_sd=noise_maps.std(0,ddof=1)
        for t in [2.,3.,5.]:
            mask2=signal_map>t*map_sd
            mask2=mask2|mask2[::-1,::-1]
            mask3=np.broadcast_to(mask2,b.shape)
            rec['controls'].append({'kind':'paired_moment0_mask','threshold_blank_scatter':t,
              'all':metrics(b,blanks,mask3),'candidate_included':bool(mask3[tuple(index)])})
        del c
        c_native=Cube(name,0.)
        an=c_native.sample();bn=bins(an);blankn,bcn=blank_samples(c_native)
        rec['controls'].append({'kind':'native_elliptical_beam','candidate':candidate_value(bn,blankn,index),
           'all':metrics(bn,blankn,support('all')),'metadata':c_native.metadata})
        archive[name+'_binned_native']=bn
        del c_native
        result['datasets'][name]=rec
        print(name,'candidate',rec['candidate'],'A2',rec['baseline']['all']['squared_asymmetry_noise_corrected'],flush=True)
    result['frozen_candidate']=frozen
    np.savez_compressed(out/'arrays.npz',**archive)
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':
    main()
