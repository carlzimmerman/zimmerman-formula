"""Bounded L017819 aperture-Jeans experiments; see contracts and derivation."""
import argparse,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from axisymmetric_jeans_v2 import JeansMoments,plummer_benchmark
HERE=Path(__file__).resolve().parent
TARGET=HERE.parent
ROOT=TARGET.parents[1]
sys.path.insert(0,str(ROOT/'euclid_for_j0332_fit_2026_11_13'))
from aqual_lensing import spherical_density_table,geometry,G,fv
from scipy.interpolate import RegularGridInterpolator


def make_model(field_file,nodes=440,extent=300.):
    a=np.load(field_file)
    # Loader is finalized against the producer's explicit array schema.
    required=['xc','tc','gr','gt','logmass','light','zl','zs','a0']
    assert all(k in a for k in required),list(a)
    xc,tc=a['xc'],a['tc'];light=a['light'];scale,_=geometry(float(a['zl']),float(a['zs']));re=float(np.exp(light[2])*scale);q=float(light[4]);n=float(np.exp(light[3]));mass=float(10**a['logmass'])
    lr,ld=spherical_density_table(n)
    def density(R,z):
        m=np.sqrt(R*R+(z/q)**2)/re
        return np.exp(np.interp(np.log(np.maximum(m,1e-100)),lr,ld,right=-1000))/(q*re**3)
    angles=np.r_[0,tc,np.pi/2]
    gr=np.column_stack((a['gr'][:,0],a['gr'],a['gr'][:,-1]))
    gt=np.column_stack((np.zeros(len(xc)),a['gt'],np.zeros(len(xc))))
    rg=RegularGridInterpolator((xc,angles),gr)
    tg=RegularGridInterpolator((xc,angles),gt)
    def force(R,z):
        R,z=np.broadcast_arrays(R,z);r=np.hypot(R,z);theta=np.arctan2(R,abs(z))
        co=np.column_stack((np.clip(np.log(np.maximum(r,1e-100)).ravel(),xc[0],xc[-1]),theta.ravel()))
        grv=rg(co).reshape(r.shape);gtv=tg(co).reshape(r.shape)
        out=r>np.exp(xc[-2]);gn=G*mass/np.maximum(r[out],1e-100)**2
        grv[out]=gn if ('mu_one' in a and bool(a['mu_one'])) else .5*(gn+np.sqrt(gn*gn+4*fv.a0_kpc(float(a['a0']))*gn));gtv[out]=0.
        return grv*np.sin(theta)+gtv*np.cos(theta),(grv*np.cos(theta)-gtv*np.sin(theta))*np.sign(z)
    return JeansMoments(density,force,re,nodes=nodes,extent=extent)


def astrometry(light):
    from astropy.io import fits
    from astropy.wcs import WCS
    fm=json.loads((TARGET/'desi_spectrum/target_fibermap.json').read_text())
    data=TARGET/'inputs/dataset/Tile102140883RA2311901412524DEC0441637579847.fits'
    wcs=WCS(fits.getheader(data,'VIS_BGSUB'))
    sky=np.array([[fm['MEAN_FIBER_RA'],fm['MEAN_FIBER_DEC']]])
    pix=wcs.all_world2pix(sky,0)[0]
    back=wcs.all_pix2world([pix],0)[0]
    assert np.max(abs(back-sky[0]))<1e-9
    fiber=(pix-49.5)*.1
    offset=fiber-np.array([light['center_west_arcsec'],light['center_north_arcsec']])
    phi=np.deg2rad(light['PA_from_west_deg'])
    uv=np.array([np.cos(phi)*offset[0]+np.sin(phi)*offset[1],
                 -np.sin(phi)*offset[0]+np.cos(phi)*offset[1]])
    return dict(fiber_pixel=pix.tolist(),fiber_west_north_arcsec=fiber.tolist(),
                relative_west_north_arcsec=offset.tolist(),relative_major_minor_arcsec=uv.tolist(),
                sky_roundtrip_max_deg=float(np.max(abs(back-sky[0]))))


def main(args):
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    if args.mode=='benchmark':
        r={'benchmark':plummer_benchmark()}
        (out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True);return
    specs=json.loads(Path(args.fields).read_text())
    scale,ratio=geometry(.32022095721117494,1.210)
    records=[]
    for s in specs:
        light=s['physical_light']
        fieldfile=ROOT/s['field_path']
        check=np.load(fieldfile)
        assert abs(float(check['zl'])-.32022095721117494)<1e-12 and abs(float(check['zs'])-1.210)<1e-12
        assert abs(float(np.exp(check['light'][2]))-light['Re_major_arcsec'])<1e-10
        assert abs(float(check['light'][4])-light['q'])<1e-10
        model=make_model(fieldfile,nodes=args.nodes,extent=args.extent)
        astro=astrometry(light);offset=np.array(astro['relative_major_minor_arcsec'])*scale
        rows=[]
        for seeing in [.8,1.2,1.6]:
            value=model.aperture(.75*scale,seeing/2.354820045*scale,offset=offset,
                                 nrad=args.nrad,nphi=args.nphi,nlos=args.nlos)
            value['seeing_fwhm_arcsec']=seeing;rows.append(value)
        centered=model.aperture(.75*scale,1.2/2.354820045*scale,offset=(0,0),
                               nrad=args.nrad,nphi=args.nphi,nlos=args.nlos)
        record=dict(specification=s,astrometry=astro,scenarios=rows,centered_control=centered)
        records.append(record);print(json.dumps(record),flush=True)
    r=dict(records=records,scale_kpc_arcsec=scale,geometry_ratio=ratio,
           non_claims=['Finite cylindrically aligned constant-b Jeans model; no positive DF certification.',
                       'Seeing, anisotropy, inclination, Satoh split are scenarios, not inferred priors.',
                       'No black hole, gas, stellar M/L gradient, full screened action or external field.',
                       'No full observational uncertainty or calibrated theory exclusion.'])
    (out/'result.json').write_text(json.dumps(r,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    p.add_argument('--mode',choices=['benchmark','fields'],default='benchmark');p.add_argument('--fields')
    p.add_argument('--nodes',type=int,default=440);p.add_argument('--extent',type=float,default=300.)
    p.add_argument('--nrad',type=int,default=200);p.add_argument('--nphi',type=int,default=64);p.add_argument('--nlos',type=int,default=160)
    main(p.parse_args())
