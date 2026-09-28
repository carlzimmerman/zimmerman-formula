"""Finite spherical pressure projection on actual cached SZ geometry; no likelihood."""
import sys,math,json,csv,argparse
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.fft import rfft2,irfft2,rfftfreq,fftfreq
from scipy.integrate import quad
from astropy.io import fits
from astropy.wcs import WCS
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);O=ap.parse_args().out;O.mkdir(parents=True,exist_ok=True)
ROOT=Path.cwd();DATA=ROOT/'real_research/data';MAP=ROOT/'deepseek_push/Z06_data';N=512;PAD=1024
nodes=np.array([0,.18,.36,.54,.72,.90,1.10,1.28,1.46,1.64,1.82,2,2.5,3,4,5.]);nb=len(nodes)-1
checks=[]
def check(n,v,t,p):checks.append(dict(name=n,observed=v,tolerance=t,pass_=bool(p)))
def separation(ra,dec,ras,decs):
 d=np.deg2rad(decs);d0=math.radians(dec);q=np.sin((d-d0)/2)**2+np.cos(d)*math.cos(d0)*np.sin(np.deg2rad(ras-ra)/2)**2
 return 2*np.arctan2(np.sqrt(q),np.sqrt(np.maximum(0,1-q)))
def J(s,t):
 z=np.sqrt(np.maximum(s*s-t*t,0));ratio=np.divide(z,t,out=np.zeros_like(z),where=t>0)
 j1=.5*(s*z+t*t*np.arcsinh(ratio));return z,j1

def project_segment(t,a,b,A,B):
 out=np.zeros_like(t);ok=t<b;v=t[ok];lo=np.maximum(a,v);j0b,j1b=J(b,v);j0a,j1a=J(lo,v);out[ok]=2*(A*(j0b-j0a)+B*(j1b-j1a));return out

def project_basis(t,i):
 out=np.zeros_like(t)
 if i>0:
  a,b=nodes[i-1:i+1];out+=project_segment(t,a,b,-a/(b-a),1/(b-a))
 a,b=nodes[i:i+2];out+=project_segment(t,a,b,b/(b-a),-1/(b-a));return out
# Independent direct LOS quadrature at selected impact parameters.
errs=[]
for i,t in [(0,0.),(0,.1),(5,.7),(5,.95),(12,1.),(12,2.75),(14,3.9),(14,4.9)]:
 p=np.zeros(len(nodes));p[i]=1
 length=math.sqrt(max(0,nodes[-1]**2-t*t));points=[math.sqrt(x*x-t*t) for x in nodes if t<x<nodes[-1]]
 val=2*quad(lambda l:float(np.interp(math.sqrt(t*t+l*l),nodes,p)),0,length,points=points,epsabs=1e-11,epsrel=1e-11)[0]
 pred=float(project_basis(np.array([t]),i)[0]);errs.append(abs(pred-val))
check('analytic piecewise-linear Abel projection versus independent LOS quadrature',max(errs),1e-9,max(errs)<1e-9)
beam=np.loadtxt(MAP/'ilc_beam.txt');assert beam.shape[1]==2 and beam[0,0]==0 and np.all(np.diff(beam[:,0])>0)
check('cached beam preserves zero mode',float(beam[0,1]),1.,beam[0,1]==1.)
cat=list(csv.DictReader((ROOT/'campaign_fresh_gravity_astra/stage_04/cluster_observables/run_002/catalogue_matches.csv').open()));cat={r['name']:r for r in cat}
zdata=json.loads((DATA/'xcop/xcop_r500_ettori2019.json').read_text())
with fits.open(DATA/'erass1cl_primary_v3.2.fits') as f:er=f[1].data.copy()
coverage=[];geometry={};profile_support=[];rows=[]
with fits.open(MAP/'ilc_actplanck_ymap.fits',memmap=True) as hf, fits.open(MAP/'wide_mask_GAL070_apod_1.50_deg_wExtended.fits',memmap=True) as hm:
 w=WCS(hf[0].header);wm=WCS(hm[0].header);assert hf[0].shape==hm[0].shape
 for name in ['A644','ZW1215']:
  ra=float(cat[name]['RA']);dec=float(cat[name]['DEC']);z=zdata[name]['z'];match=np.where(np.char.strip(er['NAME'].astype(str))==cat[name]['erass_nearest_name'])[0];assert len(match)==1;rt=float(er[match[0]]['R500'])
  DA=(299792.458/70.)/(1+z)*quad(lambda zz:1/math.sqrt(.315*(1+zz)**3+.685),0,z,epsabs=1e-12)[0]
  theta=rt/(1000*DA);xp,yp=[float(v) for v in w.world_to_pixel_values(ra,dec)];x0=int(round(xp))-N//2;y0=int(round(yp))-N//2
  assert 0<=x0 and x0+N<=hf[0].shape[1] and 0<=y0 and y0+N<=hf[0].shape[0]
  xx,yy=np.meshgrid(x0+np.arange(N),y0+np.arange(N));ras,decs=w.pixel_to_world_values(xx,yy);radius=separation(ra,dec,ras,decs)/theta
  patch=np.asarray(hf[0].data[y0:y0+N,x0:x0+N],float);mask=np.asarray(hm[0].data[y0:y0+N,x0:x0+N],float)
  xmask,ymask=wm.world_to_pixel_values(ra,dec);assert abs(float(xmask)-xp)+abs(float(ymask)-yp)<1e-9
  finite=np.isfinite(patch)&np.isfinite(mask);assert np.nanmin(mask)>=0 and np.nanmax(mask)<=1
  edges=np.r_[np.linspace(0,2,13),3.,4.,5.];weights=[];dat=[]
  for j,(a,b) in enumerate(zip(edges[:-1],edges[1:])):
   ring=(radius>=a)&(radius<b);use=ring&finite&(mask>0);den=float(mask[use].sum());nring=int(ring.sum());nuse=int(use.sum());mean=float(np.sum(mask[use]*patch[use])/den) if den>0 else None
   row=dict(name=name,annulus_index=j,inner_target_radii=float(a),outer_target_radii=float(b),inner_arcmin=float(a*theta*180/math.pi*60),outer_arcmin=float(b*theta*180/math.pi*60),pixels_total=nring,pixels_mask_positive=nuse,usable_fraction=nuse/nring if nring else None,mask_weight_sum=den,mask_min=float(mask[ring].min()),mask_max=float(mask[ring].max()),mask_mean=float(mask[ring].mean()),weighted_y_mean=mean)
   coverage.append(row)
   if j<12:weights.append(np.where(use,mask,0)/den if den>0 else np.zeros_like(mask));dat.append(mean)
  geom=dict(RA_deg=ra,DEC_deg=dec,z=z,target_radius_kpc=rt,DA_Mpc_fiducial=DA,theta_target_arcmin=theta*180/math.pi*60,patch_origin_zero_based=[x0,y0],patch_shape=[N,N],center_xy=[xp,yp],center_mask=float(mask[N//2,N//2]),pressure_support_radius_arcmin=5*theta*180/math.pi*60,min_patch_edge_radius_target_units=float(min(radius[0,:].min(),radius[-1,:].min(),radius[:,0].min(),radius[:,-1].min())))
  geometry[name]=geom
  for kind,ext in [('fgas_profile',1),('hydro_mass',1),('mstar',2)]:
   with fits.open(DATA/'xcop'/name/(name+'_'+kind+'.fits')) as fp:
    hh=fp[ext];unit=hh.columns['RADIUS'].unit;fac=1 if unit=='kpc' else (1000 if unit=='Mpc' else hh.header['R500']);r=np.asarray(hh.data['RADIUS'],float)*fac;assert r[0]<rt<r[-1];profile_support.append(dict(name=name,profile=kind,min_kpc=float(r[0]),max_kpc=float(r[-1]),target_in_support=True))
  if name=='ZW1215':target=dict(radius=radius,weights=np.asarray(weights),data=np.asarray(dat),dec=dec,theta=theta,header=hf[0].header.copy(),rt=rt)
assert all(np.isfinite(target['data']))
check('ZW1215 all twelve analysis annuli have usable pixels',sum(x['pixels_mask_positive']>0 for x in coverage if x['name']=='ZW1215' and x['annulus_index']<12),12,all(x['pixels_mask_positive']>0 for x in coverage if x['name']=='ZW1215' and x['annulus_index']<12))
check('A644 masked center reproduced',geometry['A644']['center_mask'],0,geometry['A644']['center_mask']==0)
check('pressure support contained inside source patch',geometry['ZW1215']['min_patch_edge_radius_target_units'],5,geometry['ZW1215']['min_patch_edge_radius_target_units']>5)
dx=abs(target['header']['CDELT1'])*math.pi/180*math.cos(math.radians(target['dec']));dy=abs(target['header']['CDELT2'])*math.pi/180
ell=2*math.pi*np.sqrt(fftfreq(PAD,d=dy)[:,None]**2+rfftfreq(PAD,d=dx)[None,:]**2);transfer=np.interp(ell,beam[:,0],beam[:,1],left=beam[0,1],right=0.);transfer[ell>17000]=0.
def convolve(im):
 pad=np.pad(im,((N//2,N//2),(N//2,N//2)));out=irfft2(rfft2(pad,workers=1)*transfer,s=pad.shape,workers=1);return out[N//2:N//2+N,N//2:N//2+N]
A=np.zeros((12,nb));unblurred=np.zeros_like(A)
for i in range(nb):
 proj=project_basis(target['radius'],i);blur=convolve(proj)
 A[:,i]=np.sum(target['weights']*blur,axis=(1,2));unblurred[:,i]=np.sum(target['weights']*proj,axis=(1,2))
H=np.column_stack([A,np.ones(12)]);inner=A[:,:12];nu=H[:,12:];sv=np.linalg.svd(H,compute_uv=False);si=np.linalg.svd(inner,compute_uv=False);cond=float(si[0]/si[-1]);L=np.zeros(nb+1);L[6]=5.;L[5]=-5.
check('closed finite inner model full rank',int(np.linalg.matrix_rank(inner)),12,np.linalg.matrix_rank(inner)==12)
check('full observation matrix row rank',int(np.linalg.matrix_rank(H)),12,np.linalg.matrix_rank(H)==12)
base=1e-5*np.exp(-nodes[:-1]);theta0=np.r_[base,0.];d0=H@theta0
# Recover inner amplitudes with correct known outer/background values, not a zero-boundary substitution.
rec=np.linalg.solve(inner,d0-H[:,12:]@theta0[12:]);recovery=float(np.max(abs(rec/base[:12]-1)))
check('noiseless recovery with frozen correct nuisance amplitudes',recovery,1e-10,recovery<1e-10)
mode_info=[];modes=[]
for j in range(4):
 v=np.r_[-np.linalg.solve(inner,nu[:,j]),np.eye(4)[j]];v/=np.max(abs(v));diff=np.diff(np.r_[base,0.]);vdiff=np.diff(np.r_[v[:nb],0.]);bounds=[np.min(base[np.abs(v[:nb])>1e-15]/np.abs(v[:nb][np.abs(v[:nb])>1e-15]))]
 use=abs(vdiff)>1e-15;bounds.append(np.min((-diff[use])/abs(vdiff[use])));step=.25*min(bounds)
 plus=theta0+step*v;minus=theta0-step*v
 assert np.all(plus[:nb]>0) and np.all(minus[:nb]>0) and np.all(np.diff(np.r_[plus[:nb],0.])<0) and np.all(np.diff(np.r_[minus[:nb],0.])<0)
 nullres=float(np.linalg.norm(H@v)/(np.linalg.norm(H)*np.linalg.norm(v)));shift=float(L@(plus-minus));relshift=abs(shift/float(L@theta0))
 mode_info.append(dict(nuisance=['pressure_node_2.5','pressure_node_3','pressure_node_4','constant_background'][j],relative_null_residual=nullres,gradient_difference=shift,relative_gradient_difference=relshift,step=step));modes.append((v,plus,minus))
j=max(range(4),key=lambda i:mode_info[i]['relative_gradient_difference']);v,plus,minus=modes[j];dp=H@plus;dm=H@minus
rowres=L-H.T@np.linalg.lstsq(H.T,L,rcond=None)[0];relative_rowres=float(np.linalg.norm(rowres)/np.linalg.norm(L));pred_diff=float(np.max(abs(dp-dm)));pred_rel=float(np.linalg.norm(dp-dm)/np.linalg.norm(d0));gradient_diff=float(L@(plus-minus))
check('free nuisance model target outside row space',relative_rowres,1e-8,relative_rowres>1e-8)
check('explicit null modes',max(x['relative_null_residual'] for x in mode_info),1e-12,max(x['relative_null_residual'] for x in mode_info)<1e-12)
check('positive monotone witnesses have equal model bins',pred_rel,1e-11,pred_rel<1e-11)
check('positive monotone witnesses change target gradient',abs(gradient_diff),1e-15,abs(gradient_diff)>1e-15)
# Background mean is exactly preserved by normalized binning; FFT beam zero mode checked above.
check('annular weights preserve a constant',float(np.max(abs(target['weights'].sum(axis=(1,2))-1))),1e-14,float(np.max(abs(target['weights'].sum(axis=(1,2))-1)))<1e-14)
# The photon/instrument data are not used to manufacture a confidence level.
RT=target['rt']*3.085677581491367e19;C=6.6524587321e-29/(9.1093837139e-31*299792458.**2)
result=dict(checks=checks,all_checks_pass=all(x['pass_'] for x in checks),pressure_free_nodes=nb,observed_annuli=12,free_nuisance_count=4,closed_inner_condition_number=cond,full_singular_values=sv.tolist(),closed_singular_values=si.tolist(),target_row_space_relative_residual=relative_rowres,modes=mode_info,selected_mode=mode_info[j],synthetic_gradient_plus=float(L@plus),synthetic_gradient_minus=float(L@minus),synthetic_physical_electron_pressure_gradient_plus_Pa_per_m=float(L@plus)/(C*RT**2),synthetic_physical_electron_pressure_gradient_minus_Pa_per_m=float(L@minus)/(C*RT**2),max_synthetic_bin_difference=pred_diff,relative_synthetic_bin_difference=pred_rel,beam_lmax=17000,beam_zero=beam[0].tolist(),beam_at_17000=float(np.interp(17000,beam[:,0],beam[:,1])),data_used_for='Real mask and geometry operator; observed annular y retained descriptively, synthetic identifiability witnesses are not real-data fits.',gravity='No force evaluated: projection identifiability is independent of Q/R/M and both a0/vacuum-H choices.',shared_covariance_status='Unavailable; ACT+Planck and X-COP Planck dependence not authenticated.')
np.savez_compressed(O/'operator_and_witness.npz',nodes=nodes,A=A,H=H,A_unblurred=unblurred,L=L,baseline=theta0,null_vector=v,pressure_plus=plus,pressure_minus=minus,synthetic_data_plus=dp,synthetic_data_minus=dm,observed_annular_y=target['data'])
for filename,obj in [('checks.json',result),('geometry.json',geometry),('annular_coverage.json',coverage),('xcop_support.json',profile_support)]: (O/filename).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(result,indent=2));assert result['all_checks_pass']
