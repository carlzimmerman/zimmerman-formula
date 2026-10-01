import sys
sys.dont_write_bytecode=True
from pathlib import Path
import math,json,csv,hashlib,importlib.util,itertools,argparse
from fractions import Fraction as F
import numpy as np
from scipy.fft import rfft2,irfft2,rfftfreq,fftfreq
from scipy.integrate import quad
from astropy.io import fits
from astropy.wcs import WCS
p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args();out=Path(args.out);out.mkdir(exist_ok=True)
B=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups');MAP=Path('deepseek_push/Z06_data');DATA=Path('real_research/data');N=512;PAD=1024
old=np.load(B/'results/FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz');nodes=old['nodes'];nb=15
checks=[]
def check(name,observed,pass_,tolerance=0):
 checks.append({'name':name,'observed':observed,'pass':bool(pass_),'tolerance':tolerance});assert pass_,(name,observed)
def arhash(a):return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def separation(ra,dec,ras,decs):
 d=np.deg2rad(decs);d0=math.radians(dec);q=np.sin((d-d0)/2)**2+np.cos(d)*math.cos(d0)*np.sin(np.deg2rad(ras-ra)/2)**2
 return 2*np.arctan2(np.sqrt(q),np.sqrt(np.maximum(0,1-q)))
def J(s,t):
 z=np.sqrt(np.maximum(s*s-t*t,0));ratio=np.divide(z,t,out=np.zeros_like(z),where=t>0)
 return z,.5*(s*z+t*t*np.arcsinh(ratio))
def project_segment(t,a,b,A,Bb):
 result=np.zeros_like(t);ok=t<b;v=t[ok];lo=np.maximum(a,v);j0b,j1b=J(b,v);j0a,j1a=J(lo,v);result[ok]=2*(A*(j0b-j0a)+Bb*(j1b-j1a));return result
def project_basis(t,i):
 result=np.zeros_like(t)
 if i>0:
  a,b=nodes[i-1:i+1];result+=project_segment(t,a,b,-a/(b-a),1/(b-a))
 a,b=nodes[i:i+2];result+=project_segment(t,a,b,b/(b-a),-1/(b-a));return result
# Arithmetic explicitly adapted from read parent; no top-level parent import.
cat={r['name']:r for r in csv.DictReader(Path('campaign_fresh_gravity_astra/stage_04/cluster_observables/run_002/catalogue_matches.csv').open())};row=cat['ZW1215'];ra=float(row['RA']);dec=float(row['DEC']);z=json.loads((DATA/'xcop/xcop_r500_ettori2019.json').read_text())['ZW1215']['z']
with fits.open(DATA/'erass1cl_primary_v3.2.fits') as f:
 er=f[1].data;match=np.where(np.char.strip(er['NAME'].astype(str))==row['erass_nearest_name'])[0];assert len(match)==1;rt=float(er[match[0]]['R500'])
DA=(299792.458/70.)/(1+z)*quad(lambda zz:1/math.sqrt(.315*(1+zz)**3+.685),0,z,epsabs=1e-12)[0];theta=rt/(1000*DA)
beam=np.loadtxt(MAP/'ilc_beam.txt');assert beam[0,0]==0 and np.all(np.diff(beam[:,0])>0)
with fits.open(MAP/'ilc_actplanck_ymap.fits',memmap=True) as hf,fits.open(MAP/'wide_mask_GAL070_apod_1.50_deg_wExtended.fits',memmap=True) as hm:
 w=WCS(hf[0].header);wm=WCS(hm[0].header);assert hf[0].shape==hm[0].shape
 xp,yp=map(float,w.world_to_pixel_values(ra,dec));x0=int(round(xp))-N//2;y0=int(round(yp))-N//2;assert 0<=x0 and x0+N<=hf[0].shape[1] and 0<=y0 and y0+N<=hf[0].shape[0]
 xx,yy=np.meshgrid(x0+np.arange(N),y0+np.arange(N));ras,decs=w.pixel_to_world_values(xx,yy);radius=separation(ra,dec,ras,decs)/theta
 patch=np.asarray(hf[0].data[y0:y0+N,x0:x0+N],float);mask=np.asarray(hm[0].data[y0:y0+N,x0:x0+N],float);header=hf[0].header.copy();xm,ym=wm.world_to_pixel_values(ra,dec)
 check('map mask center WCS agreement',abs(float(xm)-xp)+abs(float(ym)-yp),abs(float(xm)-xp)+abs(float(ym)-yp)<1e-9,1e-9)
 # Added stronger geometry control at patch corners, no changed response convention.
 mr,md=wm.pixel_to_world_values(xx[[0,0,-1,-1],[0,-1,0,-1]],yy[[0,0,-1,-1],[0,-1,0,-1]])
 wr,wd=w.pixel_to_world_values(xx[[0,0,-1,-1],[0,-1,0,-1]],yy[[0,0,-1,-1],[0,-1,0,-1]])
 ce=float(max(np.max(abs(mr-wr)),np.max(abs(md-wd))));check('map mask corner WCS agreement degrees',ce,ce<1e-12,1e-12)
finite=np.isfinite(patch)&np.isfinite(mask);assert np.nanmin(mask)>=0 and np.nanmax(mask)<=1
edges=np.r_[np.linspace(0,2,13),3.,4.,5.];weights=[];rings=[]
for j,(a,b) in enumerate(zip(edges[:-1],edges[1:])):
 ring=(radius>=a)&(radius<b);use=ring&finite&(mask>0);den=float(mask[use].sum());nring=int(ring.sum());nuse=int(use.sum())
 rings.append({'row':j,'edges_target_radii':[float(a),float(b)],'pixels_total':nring,'pixels_used':nuse,'weight_sum_before_normalization':den,'mask_min':float(mask[ring].min()) if nring else None,'mask_max':float(mask[ring].max()) if nring else None,'usable_fraction':nuse/nring if nring else None})
 if den<=0:
  (out/'empty_annulus_failure.json').write_text(json.dumps(rings,indent=2));raise ValueError('Empty or fully masked annulus')
 weight=np.where(use,mask,0)/den;weights.append(weight);rings[-1]['normalized_weights_sha256']=arhash(weight)
weights=np.asarray(weights);normerr=float(np.max(abs(weights.sum(axis=(1,2))-1)));check('normalized ring weights',normerr,normerr<1e-14,1e-14)
edge_radius=float(min(radius[0,:].min(),radius[-1,:].min(),radius[:,0].min(),radius[:,-1].min()));check('source support contained',edge_radius,edge_radius>5)
dx=abs(header['CDELT1'])*math.pi/180*math.cos(math.radians(dec));dy=abs(header['CDELT2'])*math.pi/180
ell=2*math.pi*np.sqrt(fftfreq(PAD,d=dy)[:,None]**2+rfftfreq(PAD,d=dx)[None,:]**2);transfer=np.interp(ell,beam[:,0],beam[:,1],left=beam[0,1],right=0.);transfer[ell>17000]=0.
check('beam zero',float(beam[0,1]),beam[0,1]==1.)
def convolve(image):
 pad=np.pad(image,((N//2,N//2),(N//2,N//2)));blur=irfft2(rfft2(pad,workers=1)*transfer,s=pad.shape,workers=1);return blur[N//2:N//2+N,N//2:N//2+N]
responses=np.zeros((15,15));unblurred=np.zeros_like(responses)
for i in range(15):
 image=project_basis(radius,i);blur=convolve(image);responses[:,i]=np.sum(weights*blur,axis=(1,2));unblurred[:,i]=np.sum(weights*image,axis=(1,2))
oldP=old['H'][:,:15];delta=responses[:12]-oldP;relative=float(np.linalg.norm(delta)/np.linalg.norm(oldP));check('old twelve rows reproduced relative',relative,relative<=1e-12,1e-12)
qerrs=[]
for i,t in [(12,2.2),(12,2.75),(13,3.2),(14,4.2),(14,4.9)]:
 vals=np.zeros(16);vals[i]=1;length=math.sqrt(25-t*t);points=[math.sqrt(a*a-t*t) for a in nodes if t<a<5]
 direct=2*quad(lambda ll:float(np.interp(math.sqrt(t*t+ll*ll),nodes,vals)),0,length,points=points,epsabs=1e-11,epsrel=1e-11)[0];qerrs.append(abs(direct-float(project_basis(np.array([t]),i)[0])))
check('outer LOS quadrature',max(qerrs),max(qerrs)<1e-9,1e-9)
C=responses[12:];combined=np.vstack([oldP,C]);np.savez_compressed(out/'response_rows.npz',nodes=nodes,old_pressure=oldP,reproduced_inner=responses[:12],outer_rows=C,combined_pressure=combined,offset_column=np.ones(15),row_edges_target_radii=np.column_stack([edges[:-1],edges[1:]]),unblurred_response=unblurred,L=old['L'][:15],baseline=old['baseline'][:15])
geometry={'cluster':'ZW1215','ra_deg':ra,'dec_deg':dec,'redshift':z,'Rtarget_kpc':rt,'fiducial_DA_Mpc':DA,'theta_target_rad':theta,'theta_target_arcmin':theta*180/math.pi*60,'patch_origin_zero_based':[x0,y0],'center_pixel':[xp,yp],'patch_shape':[N,N],'pad_shape':[PAD,PAD],'dx_rad':dx,'dy_rad':dy,'CDELT_deg':[float(header['CDELT1']),float(header['CDELT2'])],'minimum_patch_edge_target_radius':edge_radius,'radius_float64_sha256':arhash(radius),'map_patch_float64_sha256':arhash(patch),'mask_patch_float64_sha256':arhash(mask),'transfer_float64_sha256':arhash(transfer),'ell_cutoff':17000,'annuli':rings,'source_hashes':json.loads((Path(__file__).parent/'source_hash_check.json').read_text())['inputs']}
(out/'geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
# Reviewed validator is import-safe main-guarded code; no old project.py import.
vp=B/'results/FGF-024/fgf024_run_001/missing_functional.py';spec=importlib.util.spec_from_file_location('fgf024_validator',vp);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);model=v.build()
sourcepins=geometry['source_hashes'];payload={'operator_sha256':v.SHA,'coefficient_encoding':'rational_strings','pressure_column_count':15,'offset_fixed_y':'0','response_derived_not_calibrated':True,'rows':[]}
for j,row in enumerate(C):
 payload['rows'].append({'pressure_coefficients':[str(F(float(q))) for q in row],'offset_coefficient':'1','provenance':{'annulus_edges_target_radius':[j+2,j+3],'mask_weight_rule':'finite map and mask, mask>0; normalized mask pixel weight','beam_transfer_source':'cached ilc_beam.txt; ell>17000 zero','convolution_convention':'512 source zero padded to1024, tangent-plane FFT, cropped central512','geometry_distance':{'DA_Mpc':DA,'H0':70,'Omega_m':.315,'Omega_Lambda':.685,'center_deg':[ra,dec]},'outer_support':'p(5)=0; zero outside 5 target radii','basis_nodes':nodes.tolist(),'post_convolution_offset':'fixed and subtracted; separately declared offset coefficient','source_hashes':sourcepins}})
(out/'candidate_rows.json').write_text(json.dumps(payload,indent=2)+'\n')
subsets={}
for k in [1,2,3]:
 for subset in itertools.combinations(range(3),k):
  sub=dict(payload);sub['rows']=[payload['rows'][i] for i in subset];res=v.validate(sub,model);subsets[','.join(map(str,subset))]=res
allres=subsets['0,1,2'];D=np.array([[float(F(q)) for q in row] for row in allres['residual_rows_exact']]);sv=np.linalg.svd(D,compute_uv=False);normD=D/np.linalg.norm(D,axis=1)[:,None];svnorm=np.linalg.svd(normD,compute_uv=False);svfull=np.linalg.svd(combined,compute_uv=False)
control=dict(payload);control['rows']=[payload['rows'][0],payload['rows'][1],payload['rows'][0]];duplicate=v.validate(control,model);check('duplicate third row retains ambiguity',duplicate['target_identifiable'],not duplicate['target_identifiable'])
sensitivity={}
if allres['target_identifiable']:
 coeff=list(map(F,allres['old_bin_coefficients_exact']))+list(map(F,allres['extra_row_coefficients_alpha_exact']));eps=F(1,100000000);pert=[eps*(1 if c>0 else -1 if c<0 else 0) for c in coeff];pred=v.dot(coeff,pert);bound=eps*sum(map(abs,coeff));check('uniform perturbation reaches exact dual l1 bound',str(pred-bound),pred==bound)
 base=list(map(lambda q:F(float(q)),old['baseline'][:15]));M=[[F(float(q)) for q in row] for row in combined];data=[v.dot(row,base) for row in M];g0=v.dot(list(map(lambda q:F(float(q)),old['L'][:15])),base);gpert=v.dot(coeff,[a+b for a,b in zip(data,pert)]);check('perturbed reconstruction exact',str(gpert-g0-pred),gpert-g0==pred)
 sensitivity={'coefficient_weights_float':list(map(float,coeff)),'l1_amplification':float(sum(map(abs,coeff))),'l2_amplification':float(np.linalg.norm(list(map(float,coeff)))),'synthetic_epsilon_y_exact':str(eps),'synthetic_perturbation_exact':list(map(str,pert)),'gradient_change_exact':str(pred),'gradient_change':float(pred),'relative_to_synthetic_baseline':float(abs(pred/g0)),'not_observed_noise':True}
result={'checks':checks,'old_row_max_abs_difference':float(np.max(abs(delta))),'old_row_relative_difference':relative,'old_rows_bitwise_equal':bool(np.array_equal(responses[:12],oldP)),'outer_rows_float':C.tolist(),'subsets':subsets,'duplicate_control':duplicate,'residual_D_float':D.tolist(),'conditioning':{'residual_singular_values':sv.tolist(),'residual_condition2':float(sv[0]/sv[-1]),'row_normalized_residual_singular_values':svnorm.tolist(),'row_normalized_residual_condition2':float(svnorm[0]/svnorm[-1]),'combined_pressure_singular_values':svfull.tolist(),'combined_pressure_condition2':float(svfull[0]/svfull[-1]),'units':'bin rows: Compton-y per dimensionless p; target g=dp/dx; row normalization explicitly separate'},'sensitivity':sensitivity,'limitations':['Exact rank concerns stored binary64 coefficients only','Response-derived rows not independently calibrated','Finite basis/support and FFT approximation inherited','No noise, covariance, confidence, data fit or force inference','Same map bins are not independent instruments']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'old_rows_bitwise_equal':result['old_rows_bitwise_equal'],'subsets':{k:z['target_identifiable'] for k,z in subsets.items()},'condition_D':result['conditioning']['residual_condition2'],'sensitivity':sensitivity}))
