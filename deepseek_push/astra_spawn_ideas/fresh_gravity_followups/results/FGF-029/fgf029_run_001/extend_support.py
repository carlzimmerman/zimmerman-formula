import sys
sys.dont_write_bytecode=True
from pathlib import Path
import math,json,hashlib,argparse
from fractions import Fraction as F
import numpy as np
from scipy.fft import rfft2,irfft2,rfftfreq,fftfreq
from scipy.integrate import quad
from astropy.io import fits
from astropy.wcs import WCS
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out);out.mkdir(exist_ok=True)
B=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups');P=B/'results/FGF-028/fgf028_run_001/numeric_001';MAP=Path('deepseek_push/Z06_data');old=np.load(P/'response_rows.npz');geo=json.loads((P/'geometry.json').read_text());N=512;PAD=1024
checks=[]
def check(name,observed,passed,tol=0):
 checks.append({'name':name,'observed':observed,'pass':bool(passed),'tolerance':tol});assert passed,(name,observed)
def ah(a):return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def trans(a):return list(map(list,zip(*a)))
def mul(a,b):return [[dot(row,col) for col in trans(b)] for row in a]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def inverse(a):
 n=len(a);rows=[row+i for row,i in zip(a,eye(n))]
 for j in range(n):
  pivot=next(k for k in range(j,n) if rows[k][j]);rows[j],rows[pivot]=rows[pivot],rows[j];v=rows[j][j];rows[j]=[q/v for q in rows[j]]
  for k in range(n):
   if k!=j:
    v=rows[k][j]
    if v:rows[k]=[q-v*r for q,r in zip(rows[k],rows[j])]
 return [row[n:] for row in rows]
def enc(x):return [enc(v) for v in x] if isinstance(x,list) else str(x)
def separation(ra,dec,ras,decs):
 d=np.deg2rad(decs);d0=math.radians(dec);q=np.sin((d-d0)/2)**2+np.cos(d)*math.cos(d0)*np.sin(np.deg2rad(ras-ra)/2)**2
 return 2*np.arctan2(np.sqrt(q),np.sqrt(np.maximum(0,1-q)))
def J(s,t):
 z=np.sqrt(np.maximum(s*s-t*t,0));ratio=np.divide(z,t,out=np.zeros_like(z),where=t>0)
 return z,.5*(s*z+t*t*np.arcsinh(ratio))
def segment(t,a,b,A,C):
 result=np.zeros_like(t);ok=t<b;v=t[ok];lo=np.maximum(a,v);j0b,j1b=J(b,v);j0a,j1a=J(lo,v);result[ok]=2*(A*(j0b-j0a)+C*(j1b-j1a));return result
def new_projection(t):return segment(t,4.,5.,-4.,1.)+segment(t,5.,6.,6.,-1.)
ra=geo['ra_deg'];dec=geo['dec_deg'];theta=geo['theta_target_rad'];x0,y0=geo['patch_origin_zero_based']
with fits.open(MAP/'ilc_actplanck_ymap.fits',memmap=True) as hf,fits.open(MAP/'wide_mask_GAL070_apod_1.50_deg_wExtended.fits',memmap=True) as hm:
 w=WCS(hf[0].header);wm=WCS(hm[0].header);check('map mask shapes',list(hf[0].shape),hf[0].shape==hm[0].shape)
 xp,yp=map(float,w.world_to_pixel_values(ra,dec));check('center pixels fixed',[xp,yp],[xp,yp]==geo['center_pixel'])
 xm,ym=map(float,wm.world_to_pixel_values(ra,dec));check('mask center WCS',abs(xm-xp)+abs(ym-yp),abs(xm-xp)+abs(ym-yp)<1e-9,1e-9)
 xx,yy=np.meshgrid(x0+np.arange(N),y0+np.arange(N));ras,decs=w.pixel_to_world_values(xx,yy);radius=separation(ra,dec,ras,decs)/theta
 patch=np.asarray(hf[0].data[y0:y0+N,x0:x0+N],float);mask=np.asarray(hm[0].data[y0:y0+N,x0:x0+N],float);header=hf[0].header.copy()
for name,array in [('radius',radius),('map_patch',patch),('mask_patch',mask)]:check(name+' hash unchanged',ah(array),ah(array)==geo[name+'_float64_sha256'])
edge=float(min(radius[0,:].min(),radius[-1,:].min(),radius[:,0].min(),radius[:,-1].min()));check('extended support contained',edge,edge>6)
finite=np.isfinite(patch)&np.isfinite(mask);weights=[];rings=[]
for j,(a,b) in enumerate(old['row_edges_target_radii']):
 ring=(radius>=a)&(radius<b);use=ring&finite&(mask>0);den=float(mask[use].sum())
 if den<=0:
  (out/'empty_annulus_failure.json').write_text(json.dumps({'row':j,'edges':[float(a),float(b)]}));raise ValueError('Empty annulus')
 weight=np.where(use,mask,0)/den;weights.append(weight);h=ah(weight);check('ring_'+str(j)+' weights unchanged',h,h==geo['annuli'][j]['normalized_weights_sha256']);rings.append({'row':j,'edges':[float(a),float(b)],'count':int(use.sum()),'normalized_weights_sha256':h})
weights=np.asarray(weights);beam=np.loadtxt(MAP/'ilc_beam.txt');dx=abs(header['CDELT1'])*math.pi/180*math.cos(math.radians(dec));dy=abs(header['CDELT2'])*math.pi/180
check('FFT spacing unchanged',[dx,dy],dx==geo['dx_rad'] and dy==geo['dy_rad'])
ell=2*math.pi*np.sqrt(fftfreq(PAD,d=dy)[:,None]**2+rfftfreq(PAD,d=dx)[None,:]**2);transfer=np.interp(ell,beam[:,0],beam[:,1],left=beam[0,1],right=0.);transfer[ell>17000]=0.;check('beam transfer unchanged',ah(transfer),ah(transfer)==geo['transfer_float64_sha256'])
image=new_projection(radius);pad=np.pad(image,((N//2,N//2),(N//2,N//2)));convolved=irfft2(rfft2(pad,workers=1)*transfer,s=pad.shape,workers=1);blur=convolved[N//2:N//2+N,N//2:N//2+N];column=np.sum(weights*blur,axis=(1,2));unblurred=np.sum(weights*image,axis=(1,2))
qerr=[]
for t in [0.,1.,3.5,4.,4.5,5.,5.5,5.99,6.]:
 bound=math.sqrt(max(0.,36-t*t));points=[math.sqrt(r*r-t*t) for r in [4.,5.] if t<r<6.]
 def hat(r):return max(0.,min(r-4.,6.-r))
 direct=2*quad(lambda ll:hat(math.sqrt(t*t+ll*ll)),0,bound,points=points,epsabs=1e-11,epsrel=1e-11)[0] if bound else 0.
 qerr.append(abs(direct-float(new_projection(np.array([t]))[0])))
check('new hat direct LOS quadrature',max(qerr),max(qerr)<1e-9,1e-9)
Mfloat=old['combined_pressure'];combined=np.column_stack([Mfloat,column]);check('old15 columns unchanged',ah(combined[:,:15]),np.array_equal(combined[:,:15],Mfloat));check('old zero-new-coefficient model exact',True,np.array_equal(combined[:,:15],Mfloat))
nodes=np.r_[old['nodes'],6.];L=np.r_[old['L'],0.];baseline=1e-5*np.exp(-nodes[:-1]);np.savez_compressed(out/'extended_response.npz',new_column=column,combined_pressure=combined,old_pressure=Mfloat,baseline16=baseline,L16=L,nodes17=nodes,offset_column=np.ones(15),row_edges_target_radii=old['row_edges_target_radii'],unblurred_new_column=unblurred)
M=[[F(float(q)) for q in row] for row in Mfloat];k=[F(float(q)) for q in column];inv=inverse(M);I=eye(15);check('M left inverse',True,mul(inv,M)==I);check('M right inverse',True,mul(M,inv)==I)
h=[row[0] for row in mul(inv,[[q] for q in k])];l=[F(float(q)) for q in L];w=mul([l[:15]],inv)[0];mu=-dot(l[:15],h);null=[-q for q in h]+[F(1)];A=[row+[ki] for row,ki in zip(M,k)]
check('extended null exact',True,all(dot(row,null)==0 for row in A));check('target response nonzero',float(mu),mu!=0);check('target null equals coefficient',True,dot(l,null)==mu)
reconstructed=[a+b for a,b in zip(mul([w],A)[0],[F(0)]*15+[mu])];check('target decomposition exact',True,reconstructed==l)
b=[F(float(q)) for q in baseline];gaps=[b[i]-(b[i+1] if i<15 else F(0)) for i in range(16)];ngaps=[null[i]-(null[i+1] if i<15 else F(0)) for i in range(16)];eps=min(g/(4*abs(v)) for g,v in zip(gaps,ngaps) if v)
plus=[q+eps*v for q,v in zip(b,null)];minus=[q-eps*v for q,v in zip(b,null)];data=[dot(row,b) for row in A]
for name,pvals in [('plus',plus),('minus',minus)]:
 check(name+' strict pressure gaps',True,all(pvals[i]>(pvals[i+1] if i<15 else F(0)) for i in range(16)));check(name+' exact observations',True,all(dot(row,pvals)==d for row,d in zip(A,data)))
check('nonzero exact witness gradient separation',float(dot(l,plus)-dot(l,minus)),dot(l,plus)!=dot(l,minus));bad=null[:];bad[0]+=F(1,1000);check('damaged null rejected',True,any(dot(row,bad)!=0 for row in A))
positive=[F(0)]*15+[F(1)];negative=A[0];check('new coefficient observation identifies algebraic control',str(dot(positive,null)),dot(positive,null)==1);check('old row extra observation fails algebraic control',str(dot(negative,null)),dot(negative,null)==0)
result={'checks':checks,'new_column_float':column.tolist(),'matrix_rank_exact':15,'augmented_target_rank_exact':16,'nullity_exact':1,'inverse_M_exact':enc(inv),'h_M_exact':enc(h),'old_bin_target_weights_exact':enc(w),'missing_coefficient_mu_exact':str(mu),'missing_coefficient_mu_float':float(mu),'null_direction_exact':enc(null),'baseline_exact':enc(b),'synthetic_data_exact':enc(data),'epsilon_exact':str(eps),'epsilon_float':float(eps),'witness_plus_exact':enc(plus),'witness_minus_exact':enc(minus),'gradient_plus':float(dot(l,plus)),'gradient_minus':float(dot(l,minus)),'gradient_baseline':float(dot(l,b)),'relative_exhibited_gradient_width':float(abs((dot(l,plus)-dot(l,minus))/dot(l,b))),'new_pressure_baseline':float(b[-1]),'new_pressure_witnesses':[float(plus[-1]),float(minus[-1])],'extra_row_criterion':'r_new-r_old h_M != 0, for the fixed old observations and strict feasible interior','old_matrix_condition2':float(np.linalg.cond(Mfloat)),'limitations':['One added synthetic pressure degree of freedom; no measured support extension','Stored rational response and finite basis only','Fixed offset and inherited instrument approximations','Witnesses fit synthetic extended-baseline bins, not observed map','No noise/covariance, continuum, force or mass inference']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');newgeo={'parent_geometry_sha256':hashlib.sha256((P/'geometry.json').read_bytes()).hexdigest(),'inherited_geometry':geo,'extended_support_target_radius':6,'source_patch_edge_min_target_radius':edge,'new_hat':'x-4 on[4,5];6-x on[5,6];zero elsewhere','annuli':rings,'new_projection_sha256':ah(image),'convolved_new_projection_sha256':ah(blur)};(out/'geometry.json').write_text(json.dumps(newgeo,indent=2)+'\n');print(json.dumps({'missing_mu':float(mu),'new_pressure_baseline':float(b[-1]),'witness_gradient_plus':result['gradient_plus'],'witness_gradient_minus':result['gradient_minus'],'relative_width':result['relative_exhibited_gradient_width'],'edge_radius':edge,'checks':len(checks)}))
