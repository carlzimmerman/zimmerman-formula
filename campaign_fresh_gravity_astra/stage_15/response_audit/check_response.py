"""Independent node5 hat support extension: one column, unchanged15 annuli."""
import json,sys,math,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from astropy.io import fits
from astropy.wcs import WCS

out=Path(sys.argv[1]); candidate_path=Path(sys.argv[2]); candidate_key=sys.argv[3]
base=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001')
geo=json.loads((base/'numeric_001/geometry.json').read_text())['ZW1215']
with np.load(candidate_path,allow_pickle=False) as a:
 new=np.asarray(a[candidate_key],float).copy()
assert new.shape==(15,),new.shape
candidate_geometry=json.loads(Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-028/fgf028_run_001/numeric_001/geometry.json').read_text())
N=512;P=1024;order=32
ra=geo['RA_deg'];dec=geo['DEC_deg'];z=geo['z'];rt=geo['target_radius_kpc']
DA=299792.458/70/(1+z)*quad(lambda t:1/math.sqrt(.315*(1+t)**3+.685),0,z,epsabs=1e-12)[0]
theta=rt/(1000*DA)
assert abs(DA/geo['DA_Mpc_fiducial']-1)<1e-13
assert abs(theta/(geo['theta_target_arcmin']*math.pi/(180*60))-1)<1e-13
with fits.open('deepseek_push/Z06_data/ilc_actplanck_ymap.fits',memmap=True) as fm, fits.open('deepseek_push/Z06_data/wide_mask_GAL070_apod_1.50_deg_wExtended.fits',memmap=True) as fk:
 assert fm[0].shape==fk[0].shape
 w=WCS(fm[0].header);wk=WCS(fk[0].header)
 cx,cy=map(float,w.world_to_pixel_values(ra,dec))
 x0=int(round(cx))-N//2;y0=int(round(cy))-N//2
 assert [x0,y0]==geo['patch_origin_zero_based']
 yy,xx=np.indices((N,N));rr,dd=w.pixel_to_world_values(xx+x0,yy+y0)
 im=np.asarray(fm[0].data[y0:y0+N,x0:x0+N],float).copy()
 mask=np.asarray(fk[0].data[y0:y0+N,x0:x0+N],float).copy()
 # WCS alignment tested at four corners and center, not only one pixel.
 tx=np.array([x0,x0+N-1,x0,x0+N-1,cx]);ty=np.array([y0,y0,y0+N-1,y0+N-1,cy])
 wr,wd=w.pixel_to_world_values(tx,ty);kx,ky=wk.world_to_pixel_values(wr,wd)
 alignment=float(max(np.max(abs(kx-tx)),np.max(abs(ky-ty))))
 assert alignment<1e-6
 dx=abs(float(fm[0].header['CDELT1']))*math.pi/180*math.cos(math.radians(dec))
 dy=abs(float(fm[0].header['CDELT2']))*math.pi/180
# Independent spherical atan2 of cross magnitude and dot product.
b=np.deg2rad(dd);b0=math.radians(dec);dra=np.deg2rad(rr-ra)
x=np.cos(b)*np.sin(dra)
y=math.cos(b0)*np.sin(b)-math.sin(b0)*np.cos(b)*np.cos(dra)
c=math.sin(b0)*np.sin(b)+math.cos(b0)*np.cos(b)*np.cos(dra)
radius=np.arctan2(np.hypot(x,y),c)/theta
edge_min=float(min(radius[0].min(),radius[-1].min(),radius[:,0].min(),radius[:,-1].min()))
assert edge_min>6
assert np.nanmin(mask)>=0 and np.nanmax(mask)<=1
# New hat index15: p=r-4 on [4,5], p=6-r on [5,6].
# Integrate directly over positive line-of-sight distance and double.
t=radius.ravel();proj=np.zeros_like(t)
gnodes,gweights=np.polynomial.legendre.leggauss(order)
for lower,upper,intercept,slope in [(4.,5.,-4.,1.),(5.,6.,6.,-1.)]:
 use=t<upper;v=t[use]
 lo=np.sqrt(np.maximum(lower*lower-v*v,0));hi=np.sqrt(upper*upper-v*v)
 total=np.zeros_like(v)
 for q,weight in zip(gnodes,gweights):
  line=(hi+lo)/2+(hi-lo)*q/2
  total+=weight*(intercept+slope*np.sqrt(v*v+line*line))
 proj[use]+=(hi-lo)*total
proj=proj.reshape(N,N)
assert np.max(abs(proj[radius>=6]))==0
# Repeat the declared finite FFT approximation, not a new physical beam model.
beam=np.loadtxt('deepseek_push/Z06_data/ilc_beam.txt')
assert beam.shape[1]==2 and beam[0,0]==0 and beam[0,1]==1 and np.all(np.diff(beam[:,0])>0)
f_y=np.fft.fftfreq(P,d=dy)[:,None];f_x=np.fft.rfftfreq(P,d=dx)[None,:]
ell=2*np.pi*np.hypot(f_x,f_y)
transfer=np.interp(ell,beam[:,0],beam[:,1],left=beam[0,1],right=0)
transfer[ell>17000]=0
padded=np.zeros((P,P));s=(P-N)//2;padded[s:s+N,s:s+N]=proj
blur=np.fft.irfft2(np.fft.rfft2(padded)*transfer,s=(P,P))[s:s+N,s:s+N]
edges=np.r_[np.linspace(0,2,13),3.,4.,5.]
valid=np.isfinite(im)&np.isfinite(mask)&(mask>0)
responses=[];coverage=[]
for j,(a,b) in enumerate(zip(edges[:-1],edges[1:])):
 ring=(radius>=a)&(radius<b);use=ring&valid
 den=float(np.sum(mask[use]));assert den>0
 weights=mask[use]/den
 fullweight=np.zeros_like(mask);fullweight[use]=weights
 whash=hashlib.sha256(np.ascontiguousarray(fullweight).tobytes()).hexdigest()
 cg=candidate_geometry['annuli'][j]
 assert int(ring.sum())==cg['pixels_total'] and int(use.sum())==cg['pixels_used']
 assert den==cg['weight_sum_before_normalization'] and whash==cg['normalized_weights_sha256']
 responses.append(float(np.dot(weights,blur[use])))
 coverage.append({'inner':float(a),'outer':float(b),'pixels_total':int(ring.sum()),'pixels_valid':int(use.sum()),'weight_sum_raw':den,'weight_sum_normalized':float(weights.sum()),'mask_min':float(mask[ring].min()),'mask_max':float(mask[ring].max()),'weight_sha256_matches_pinned_FGF028':True})
responses=np.array(responses);refs=new
errors=abs(responses-refs);tols=1e-10+2e-9*abs(refs)
assert np.all(errors<=tols),list(zip(errors,tols))
assert all(abs(c['weight_sum_normalized']-1)<1e-14 for c in coverage)
result={'claim':'independent node5 support-extension LOS/geometry/annulus response check','basis_index':15,'basis_node':5,'fixed_zero_endpoint':6,'quadrature_order':order,'N':N,'padding':P,'absolute_tolerance':1e-10,'relative_tolerance':2e-9,'distance_Mpc':DA,'angular_radius_rad':theta,'wcs_alignment_max_pixels':alignment,'patch_edge_min_target_radii':edge_min,'pixel_dx_rad':dx,'pixel_dy_rad':dy,'beam_zero_mode':float(beam[0,1]),'beam_lmax':17000,'responses':responses.tolist(),'reference_responses':refs.tolist(),'absolute_errors':errors.tolist(),'first12_max_absolute_error':float(errors[:12].max()),'last3_max_absolute_error':float(errors[12:].max()),'max_absolute_error':float(errors.max()),'coverage':coverage,'all_checks_passed':True,'limits':['only new node5 column; old15 columns not rebuilt','declared finite flat-sky/padding beam model only','no map fit/covariance/force','additional rows same cached map']}
Path(out).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['responses','reference_responses','absolute_errors','coverage']},sort_keys=True))
