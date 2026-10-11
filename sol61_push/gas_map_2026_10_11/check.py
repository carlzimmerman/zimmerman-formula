"""Gas-only released map convention audit; no theory fit or gas rescaling."""
from pathlib import Path
import itertools,json,hashlib
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord,FK5
import astropy.units as u
P=Path(__file__).resolve().parent

def derivative(a,axis,h,order):
    if order==2:return (np.roll(a,-1,axis)-np.roll(a,1,axis))/(2*h)
    return (-np.roll(a,-2,axis)+8*np.roll(a,-1,axis)-8*np.roll(a,1,axis)+np.roll(a,2,axis))/(12*h)

def fields(ax,ay,h,order):
    return ((derivative(ax,1,h,order)+derivative(ay,0,h,order))/2,
            (derivative(ay,1,h,order)-derivative(ax,0,h,order))/2)

def main():
    checks=[]
    def ck(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    names=['xray_alpha1_dsdls1.fits','xray_alpha2_dsdls1.fits','xray_kappa_dsdls1.fits']
    arrays=[np.array(fits.getdata(P/'sources'/n),float) for n in names]
    headers=[fits.getheader(P/'sources'/n) for n in names]
    h=abs(headers[0]['CDELT1'])*3600
    ck('finite_matching_arrays',all(a.shape==(256,256) and np.isfinite(a).all() for a in arrays))
    ck('positive_square_pixel',h>0 and abs(abs(headers[0]['CDELT2'])*3600-h)<1e-10)
    wkeys=['CTYPE1','CTYPE2','CRPIX1','CRPIX2','CRVAL1','CRVAL2','CDELT1','CDELT2']
    ck('common_WCS',all(all(q[k]==headers[0][k] for k in wkeys) for q in headers))
    YY,XX=np.mgrid[:256,:256]*h
    ax=.3*XX+.2*YY;ay=.2*XX+.7*YY
    sl=np.s_[8:-8,8:-8]
    for order in (2,4):
        dv,cu=fields(ax,ay,h,order)
        ck('quadratic_potential_'+str(order),np.max(np.abs(dv[sl]-.5))<5e-11 and np.max(np.abs(cu[sl]))<5e-11)
        ds,cs=fields(ax+12,ay-7,h,order)
        ck('constant_deflection_gauge_'+str(order),np.max(np.abs(ds[sl]-dv[sl]))<5e-11 and np.max(np.abs(cs[sl]-cu[sl]))<5e-11)
        dm,_=fields(ax,-ay,h,order)
        ck('MUTATE_component_sign_'+str(order),np.mean(np.abs(dm[sl]-.5))>.1)
        dm,_=fields(ax,ay,h/3600,order)
        ck('MUTATE_angular_units_'+str(order),np.mean(np.abs(dm[sl]-.5))>100)
    a,b,kappa=arrays; kk=kappa[sl].ravel();std=float(np.std(kk)); out=[]; preferred=[]
    for order in (2,4):
        cases=[]
        for swap,sx,sy in itertools.product((False,True),(1,-1),(1,-1)):
            xx,yy=(b,a) if swap else (a,b)
            dv,cu=fields(sx*xx,sy*yy,h,order); dd=dv[sl].ravel()
            slope,offset=np.linalg.lstsq(np.column_stack([kk,np.ones(len(kk))]),dd,rcond=None)[0]
            resid=float(np.sqrt(np.mean((dd-slope*kk-offset)**2))/std)
            curl=float(np.sqrt(np.mean(cu[sl]**2))/std)
            cases.append(dict(order=order,swap=swap,sx=sx,sy=sy,slope=float(slope),offset=float(offset),residual_over_std_kappa=resid,curl_over_std_kappa=curl,raw_difference_over_std_kappa=float(np.sqrt(np.mean((dd-kk)**2))/std)))
        # Global sign ambiguity resolved diagnostically by the positive-divergence convention.
        best=min([v for v in cases if v['slope']>0],key=lambda v:v['residual_over_std_kappa']+v['curl_over_std_kappa'])
        passed=abs(abs(best['slope'])-1)<.02 and best['residual_over_std_kappa']<.02 and best['curl_over_std_kappa']<.02
        ck('differential_gate_'+str(order),passed,best)
        preferred.append(best);out.extend(cases)
    ck('derivative_order_convention_agreement',[(x['swap'],x['sx'],x['sy']) for x in preferred][0]==[(x['swap'],x['sx'],x['sy']) for x in preferred][1])
    gold=json.loads((P.parent/'native_lensing_2026_10_11/run_v2/results.json').read_text())['gold_rows']
    coords=SkyCoord([r['ra'] for r in gold]*u.deg,[r['dec'] for r in gold]*u.deg,frame='icrs')
    fk=coords.transform_to(FK5(equinox='J2000'))
    wc=WCS(headers[0]); pi=wc.all_world2pix(np.column_stack([coords.ra.deg,coords.dec.deg]),0)
    pf=wc.all_world2pix(np.column_stack([fk.ra.deg,fk.dec.deg]),0)
    outside=[]
    for frame,px in [('ICRS',pi),('FK5J2000',pf)]:
        bad=[gold[j]['id'] for j in range(len(gold)) if not np.all((px[j]>=0)&(px[j]<=255))]
        ck('all_images_inside_'+frame,not bad,bad);outside.append(dict(frame=frame,outside=bad))
    output=dict(status='differential_gate_pass_normalization_still_requires_metadata' if all(q['passed'] for q in checks) else 'UNRESOLVED_preserve_source_do_not_import',passed=sum(q['passed'] for q in checks),total=len(checks),checks=checks,pixel_arcsec=h,preferred=preferred,all_conventions=out,map_stats=[dict(file=n,min=float(a.min()),max=float(a.max()),mean=float(a.mean())) for n,a in zip(names,arrays)],interior_std_kappa=std,frame_shift_pixels_max=float(np.linalg.norm(pi-pf,axis=1).max()),outside=outside,header_notes='BUNIT and RADESYS absent. No image deflections evaluated and no normalization changed.')
    (P/'run/results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(output['status'],output['passed'],output['total']);print(json.dumps(preferred));print(json.dumps(output['map_stats']));print('frame shift pixels',output['frame_shift_pixels_max'])
    # A diagnostic fail is retained as a nonzero run, never relabelled.
    assert all(q['passed'] for q in checks)
if __name__=='__main__':main()
