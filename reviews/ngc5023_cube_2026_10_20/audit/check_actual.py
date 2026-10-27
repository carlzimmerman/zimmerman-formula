#!/usr/bin/env python3
"""Independent saved-array checks and raw-FITS candidate reconstruction.

Does not import cube_io.py or cube_analysis.py. No source-region reselection.
"""
import argparse
import json
from pathlib import Path
import math
import numpy as np
from scipy.signal import convolve

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent


def primary(path):
    h = {}
    with path.open('rb') as f:
        done = False
        while not done:
            buf = f.read(2880)
            if len(buf) != 2880:
                raise ValueError('Header truncated')
            for start in range(0, 2880, 80):
                c = buf[start:start+80].decode('ascii')
                if c[:8].strip() == 'END':
                    done = True
                    break
                if c[8:10] != '= ':
                    continue
                v = c[10:].strip()
                if v.startswith("'"):
                    value = v[1:v.index("'", 1)].rstrip()
                else:
                    v = v.split('/')[0].strip()
                    if v in ('T', 'F'):
                        value = v == 'T'
                    else:
                        value = float(v.replace('D', 'E'))
                h[c[:8].strip()] = value
        offset = f.tell()
    shape = tuple(int(h['NAXIS'+str(i)]) for i in range(int(h['NAXIS']), 0, -1))
    dtype = {16:'>i2', -32:'>f4', -64:'>f8'}[int(h['BITPIX'])]
    return h, np.memmap(path, dtype=dtype, offset=offset, mode='r', shape=shape)


def pix(h, direction):
    # NCP projected Cartesian coordinates written directly in unit-vector terms.
    ra0, dec0 = np.deg2rad([h['CRVAL1'], h['CRVAL2']])
    xi = -direction[0]*np.sin(ra0)+direction[1]*np.cos(ra0)
    c = direction[0]*np.cos(ra0)+direction[1]*np.sin(ra0)
    eta = (np.cos(dec0)-c)/np.sin(dec0)
    return np.rad2deg(xi)/h['CDELT1']+h['CRPIX1']-1, np.rad2deg(eta)/h['CDELT2']+h['CRPIX2']-1


def direction(ra, dec, east=0, north=0):
    ar, dr = np.deg2rad([ra, dec])
    unit = np.array([np.cos(dr)*np.cos(ar), np.cos(dr)*np.sin(ar), np.sin(dr)])
    e = np.array([-np.sin(ar), np.cos(ar), 0.])
    n = np.array([-np.sin(dr)*np.cos(ar), -np.sin(dr)*np.sin(ar), np.cos(dr)])
    t = unit[:,None]+e[:,None]*np.asarray(east).reshape(1,-1)*np.pi/648000+n[:,None]*np.asarray(north).reshape(1,-1)*np.pi/648000
    return t/np.linalg.norm(t, axis=0)


def raw_candidate(name, meta, candidate):
    h, a = primary(PACKET/meta['source'])
    ra, dec = meta['center_world_deg']
    cx, cy = (float(v[0]) for v in pix(h, direction(ra, dec)))
    # Reconstruct exact frozen 6x10x10 quadrature cells on both sides.
    u = candidate['u_km_s']+(np.arange(6)-2.5)*4.12
    z = candidate['z_arcsec']+(np.arange(10)-4.5)*4
    x = candidate['x_arcsec']+(np.arange(10)-4.5)*4
    uu, zz, xx = np.meshgrid(u, z, x, indexing='ij')
    xx, zz, vv = np.concatenate([xx.ravel(),-xx.ravel()]), np.concatenate([zz.ravel(),-zz.ravel()]), np.concatenate([uu.ravel(),-uu.ravel()])+candidate['vsys_km_s']
    pa = np.deg2rad(candidate['PA_deg'])
    east = xx*np.sin(pa)+zz*np.cos(pa)
    north = xx*np.cos(pa)-zz*np.sin(pa)
    px, py = pix(h, direction(ra, dec, east, north))
    grid = np.arange(a.shape[0])+1-h['CRPIX3']
    if h['CTYPE3'] == 'VELO-HEL':
        vel = (h['CRVAL3']+grid*h['CDELT3'])/1000
        maj, minor, angle = h['BMAJ']*3600, h['BMIN']*3600, h['BPA']
    else:
        freq = h['CRVAL3']+grid*h['CDELT3']
        vel = h['DRVAL3']+299792.458*1420405752*(1/freq-1/h['CRVAL3'])
        maj, minor, angle = h['BMMAJ'], h['BMMIN'], h['BMPA']
    assert np.all(np.diff(vel)>0)
    spectral = np.interp(vv, vel, np.arange(len(vel)))
    base = np.floor(spectral).astype(int)
    frac = spectral-base
    # Same physical Gaussian target, covariance derived in east/north first.
    theta = np.deg2rad(angle)
    rot = np.array([[np.sin(theta),np.cos(theta)],[np.cos(theta),-np.sin(theta)]])
    native_sky = rot @ np.diag([(maj/2.3548200450309493)**2,(minor/2.3548200450309493)**2]) @ rot.T
    scale = np.diag([1/(h['CDELT1']*3600),1/(h['CDELT2']*3600)])
    # The production target uses its documented rounded Gaussian conversion.
    target = np.diag([(40/(2.354820045*abs(h[k])*3600))**2 for k in ['CDELT1','CDELT2']])
    extra = target-scale@native_sky@scale
    radius = int(np.ceil(5.5*np.sqrt(np.linalg.eigvalsh(extra).max())))
    yy, xxk = np.mgrid[-radius:radius+1,-radius:radius+1]
    precision = np.linalg.inv(extra)
    kernel = np.exp(-.5*(precision[0,0]*xxk**2+2*precision[0,1]*xxk*yy+precision[1,1]*yy**2))
    kernel /= kernel.sum()
    # Bounded native patch covering the paired bins plus the complete kernel.
    x0 = int(np.floor(px.min()))-radius-2
    y0 = int(np.floor(py.min()))-radius-2
    x1 = int(np.ceil(px.max()))+radius+3
    y1 = int(np.ceil(py.max()))+radius+3
    assert 0<=x0<x1<=a.shape[2] and 0<=y0<y1<=a.shape[1]
    fx, fy = px-x0, py-y0
    ix, iy = np.floor(fx).astype(int),np.floor(fy).astype(int)
    tx, ty = fx-ix,fy-iy
    area = np.pi/(4*np.log(2))*maj*minor
    unit = meta['unit_to_Jy_per_native_beam']/area
    # Independently recompute per-channel background in the production crop.
    ox0, oy0 = max(0,int(cx)-384),max(0,int(cy)-384)
    ox1, oy1 = min(a.shape[2],int(cx)+385),min(a.shape[1],int(cy)+385)
    gy,gx = np.mgrid[oy0:oy1:4,ox0:ox1:4]
    outside = (gx-cx)**2+(gy-cy)**2 > (400/(abs(h['CDELT1'])*3600))**2
    values = np.zeros(len(vv),dtype=float)
    background_errors=[]
    channels = np.unique(np.concatenate([base,base+1]))
    for k in channels:
        # Preserve signed data and the native int16 sentinel before scaling.
        image = np.array(a[k,y0:y1,x0:x1],dtype=np.float32)
        blank = image == h['BLANK'] if 'BLANK' in h else ~np.isfinite(image)
        image *= h.get('BSCALE',1); image += h.get('BZERO',0);image[blank]=np.nan
        image *= unit
        bg = np.array(a[k,oy0:oy1:4,ox0:ox1:4],dtype=np.float32)
        bad = bg == h['BLANK'] if 'BLANK' in h else ~np.isfinite(bg)
        bg *= h.get('BSCALE',1);bg += h.get('BZERO',0);bg[bad]=np.nan;bg *= unit
        median = np.nanmedian(bg[outside])
        background_errors.append(float(median-meta['native_baseline_Jy_per_arcsec2'][k]))
        image -= median
        valid = np.isfinite(image)
        weighted = convolve(np.nan_to_num(image),kernel,mode='same',method='fft')
        norm = convolve(valid.astype(float),kernel,mode='same',method='fft')
        smooth = np.asarray(np.where(norm>.99999,weighted/np.maximum(norm,1e-30),np.nan),dtype=np.float32)
        # Explicit bilinear sky interpolation then independent linear spectrum.
        interp=((1-tx)*(1-ty)*smooth[iy,ix]+tx*(1-ty)*smooth[iy,ix+1]
                +(1-tx)*ty*smooth[iy+1,ix]+tx*ty*smooth[iy+1,ix+1])
        w=np.where(base==k,1-frac,0)+np.where(base+1==k,frac,0)
        values+=w*interp
    assert np.isfinite(values).all()
    vplus,vminus = values.reshape(2,-1).sum(axis=1)*16*4.12
    return {'positive_bin_flux_Jy_km_s':float(vplus),'mirror_bin_flux_Jy_km_s':float(vminus),
            'signed_difference_Jy_km_s':float(vplus-vminus),'paired_sum_Jy_km_s':float(vplus+vminus),
            'center_pixels':[cx,cy],'native_channels':channels.tolist(),
            'maximum_background_discrepancy_Jy_arcsec2':max(map(abs,background_errors)),
            'notes':'Independent FITS parsing, Cartesian-vector sky projection, Gaussian patch convolution, explicit bilinear plus spectral interpolation. No production module imported.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    records=[];raw=[]
    frozen=json.loads((PACKET/'discovery_run001/candidate.json').read_text())
    for run in ['discovery_run001','replication_run001']:
        saved=json.loads((PACKET/run/'results.json').read_text())
        arrays=np.load(PACKET/run/'arrays.npz')
        assert saved['frozen_candidate']==frozen
        for name,rec in saved['datasets'].items():
            b=arrays[name+'_binned40'].astype(float)
            blank=arrays[name+'_blanks40'].astype(float)
            d=b-np.flip(b);s=b+np.flip(b)
            db=blank-np.flip(blank,axis=(1,2,3));sb=blank+np.flip(blank,axis=(1,2,3))
            index=tuple(frozen['index'])
            check={'dataset':name,'candidate_difference_error':float(d[index]-rec['candidate']['signed_difference_Jy_km_s']),
                   'candidate_blank_scatter_error':float(np.std(db[(slice(None),)+index],ddof=1)-rec['candidate']['blank_scatter']),
                   'candidate_blank_mean_error':float(np.mean(db[(slice(None),)+index])-rec['candidate']['blank_mean']),
                   'blank_count':len(blank)}
            x=np.arange(15)*40-280
            half=np.broadcast_to((x>0)[None,None,:],b.shape)
            nd=np.sum(db[:,half]**2,axis=1).mean();ns=np.sum(sb[:,half]**2,axis=1).mean()
            a2=(np.sum(d[half]**2)-nd)/(np.sum(s[half]**2)-ns)
            check['all_squared_asymmetry_error']=float(a2-rec['baseline']['all']['squared_asymmetry_noise_corrected'])
            check['central_major_axis_bin_excluded']=True
            check['passed']=all(abs(check[k])<1e-6 for k in ['candidate_difference_error','candidate_blank_scatter_error','candidate_blank_mean_error','all_squared_asymmetry_error'])
            records.append(check)
            direct=raw_candidate(name,rec['metadata'],frozen)
            direct['dataset']=name
            direct['difference_from_saved']=direct['signed_difference_Jy_km_s']-rec['candidate']['signed_difference_Jy_km_s']
            direct['passed']=abs(direct['difference_from_saved'])<2e-6
            raw.append(direct)
    output={'outcome':'saved-array quantities and raw candidate reconstruction independently checked in stated finite range',
            'checks':records,'raw_candidate_checks':raw,'all_passed':all(v['passed'] for v in records+raw),
            'non_claims':['No formal real-data discovery significance','No complete independent reprocessing of all nuisance grid cases','No exact instrumental LSF matching or asymmetric warp/spiral fit','Not a gravity or memory detection']}
    Path(args.output).write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'all_passed':output['all_passed'],'datasets':len(records),'raw_checks':len(raw)}))
    return 0 if output['all_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
