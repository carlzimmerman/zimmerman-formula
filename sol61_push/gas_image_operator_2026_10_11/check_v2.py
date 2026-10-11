import json,sys
from pathlib import Path
import numpy as np
from scipy.ndimage import map_coordinates
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord,FK5
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
P=Path('sol61_push'); D=P/'gas_map_2026_10_11/sources'; N=P/'native_lensing_2026_10_11/run_v2'
prior=json.loads((N/'results.json').read_text()); rows=prior['gold_rows']; origin=prior['tangent_origin_degrees']
old=np.load(N/'operator.npz'); H=old['helmert']; theta=old['theta_arcsec']
header=fits.getheader(D/'xray_alpha1_dsdls1.fits'); wc=WCS(header); spacing=abs(header['CDELT1'])*3600
ax=fits.getdata(D/'xray_alpha1_dsdls1.fits').astype(float); ay=fits.getdata(D/'xray_alpha2_dsdls1.fits').astype(float)
sky=SkyCoord([r['ra'] for r in rows]*u.deg,[r['dec'] for r in rows]*u.deg,frame='icrs')
def hm(x):
 return np.einsum('ij,j...->i...',H,x,optimize=False)
checks=[]
def ck(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
def tangent(ra,dec,centre=origin):
 a,d=np.deg2rad(ra),np.deg2rad(dec); a0,d0=np.deg2rad(centre); da=a-a0
 den=np.sin(d0)*np.sin(d)+np.cos(d0)*np.cos(d)*np.cos(da)
 return np.stack([np.cos(d)*np.sin(da)/den,(np.cos(d0)*np.sin(d)-np.sin(d0)*np.cos(d)*np.cos(da))/den],axis=-1)*206264.80624709636
fkframe=FK5(equinox='J2000')
def chart(p,frame,centre=origin):
 world=wc.all_pix2world(p,0)
 s=SkyCoord(world[:,0]*u.deg,world[:,1]*u.deg,frame='icrs' if frame=='ICRS' else fkframe).icrs
 return tangent(s.ra.deg,s.dec.deg,centre)
def jac(p,frame,step,centre=origin):
 return np.stack([(chart(p+np.eye(2)[k]*step,frame,centre)-chart(p-np.eye(2)[k]*step,frame,centre))/(2*step) for k in range(2)],axis=-1)/spacing
ck('target_theta_reproduction',np.max(abs(tangent(sky.ra.deg,sky.dec.deg)-theta))<1e-6)
ck('Helmert_orthonormal',np.max(abs(hm(H.T)-np.eye(len(H))))<1e-12)
for f in sorted(set(r['feature'] for r in rows)):
 mask=np.array([r['feature']==f for r in rows],float)
 ck('source_constant_'+f,np.max(abs(hm(mask)))<1e-12)
# Orthogonal known chart origin control, independent of observed deflection values.
p0=np.array([[header['CRPIX1']-1,header['CRPIX2']-1]])
J0=jac(p0,'ICRS',.01,[header['CRVAL1'],header['CRVAL2']])[0]
ck('known_basis',np.max(abs(J0-np.diag([-1.,1.])))<1e-6,J0.tolist())
ck('MUTATE_omit_west_flip',np.max(abs(J0-np.eye(2)))>1)
ck('MUTATE_degree_arcsec',np.linalg.norm(J0*3600)/np.linalg.norm(J0)>100)
yy,xx=np.mgrid[:256,:256]; test=.3*xx-.7*yy+5; pts=np.array([[12.4,73.8],[100.9,120.1]])
ck('affine_bilinear',np.max(abs(map_coordinates(test,pts.T[::-1],order=1)-(.3*pts[:,0]-.7*pts[:,1]+5)))<1e-10)
cosmo=FlatLambdaCDM(H0=70,Om0=.3); zs=np.array([r['zsys'] for r in rows]); zl=.296
w=np.array((cosmo.angular_diameter_distance_z1z2(zl,zs)/cosmo.angular_diameter_distance(zs)).value)
ck('source_weights',np.all((w>0)&(w<1)) and all(np.ptp(w[[r['feature']==f for r in rows]])<1e-14 for f in set(r['feature'] for r in rows)))
arrays={'helmert':H,'theta_arcsec':theta,'source_weight_author_context':w}; metrics={}
for frame in ['ICRS','FK5J2000']:
 pos=sky if frame=='ICRS' else sky.transform_to(fkframe)
 pix=wc.all_world2pix(np.column_stack([pos.ra.deg,pos.dec.deg]),0)
 ck('interior_'+frame,np.all((pix>2)&(pix<253)))
 world=wc.all_pix2world(pix,0); back=wc.all_world2pix(world,0)
 ck('inverse_'+frame,np.max(abs(back-pix))<1e-6,float(np.max(abs(back-pix))))
 ck('chart_'+frame,np.max(abs(chart(pix,frame)-theta))<1e-6)
 J=jac(pix,frame,.005); Jwide=jac(pix,frame,.01)
 vals={}
 for name,order in [('linear',1),('cubic',3)]:
  v=np.column_stack([map_coordinates(a,pix.T[::-1],order=order,mode='nearest') for a in [ax,ay]])
  alpha=np.einsum('nij,nj->ni',J,v); alt=np.einsum('nij,nj->ni',Jwide,v)
  ck('jacobian_refinement_'+frame+'_'+name,np.max(abs(alpha-alt))<1e-5,float(np.max(abs(alpha-alt))))
  contrast=hm(w[:,None]*alpha)
  ck('target_gauge_'+frame+'_'+name,np.max(abs(hm(w[:,None]*(alpha+np.array([3.,-7.]))) - contrast))<1e-10)
  ck('finite_'+frame+'_'+name,np.isfinite(alpha).all() and np.isfinite(contrast).all())
  tag=frame+'_'+name
  arrays[tag+'_alpha_infinity_arcsec']=alpha
  arrays[tag+'_H_alpha_infinity_arcsec']=hm(alpha)
  arrays[tag+'_H_reduced_author_context_arcsec']=contrast
  vals[name]=alpha
  metrics[tag]={'max_alpha_infinity_arcsec':float(np.max(np.linalg.norm(alpha,axis=1))),'max_reduced_contrast_component_arcsec':float(np.max(abs(contrast)))}
 arrays[frame+'_pixel']=pix
 metrics[frame+'_interpolation']={'max_vector_difference_arcsec':float(np.max(np.linalg.norm(vals['linear']-vals['cubic'],axis=1))),'max_context_contrast_difference_arcsec':float(np.max(abs(hm(w[:,None]*(vals['linear']-vals['cubic'])))))}
for name in ['linear','cubic']:
 delta=arrays['ICRS_'+name+'_alpha_infinity_arcsec']-arrays['FK5J2000_'+name+'_alpha_infinity_arcsec']
 metrics['frame_difference_'+name]={'max_vector_arcsec':float(np.max(np.linalg.norm(delta,axis=1))),'max_context_contrast_component_arcsec':float(np.max(abs(hm(w[:,None]*delta))))}
previous=np.load(P/'gas_image_operator_2026_10_11/run/operator.npz')
for key,value in arrays.items():
 ck('independent_sum_'+key,np.all(np.isfinite(value)) and np.max(abs(value-previous[key]))<1e-10)
out=Path(sys.argv[1]);np.savez_compressed(out/'operator.npz',**arrays)
result=dict(checks=checks,metrics=metrics,image_ids=[r['id'] for r in rows],source_normalization='Dls/Ds=1; author gas calibration unchanged',context_background={'H0':70,'Om0':.3,'z_lens':zl},scientific_verdict=None)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks');print(json.dumps(metrics,indent=2))
assert all(c['passed'] for c in checks)
