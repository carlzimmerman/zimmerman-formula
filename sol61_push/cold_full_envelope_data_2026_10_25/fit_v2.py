"""Conditional-position Jeans likelihood and complete-envelope screens."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,math,pathlib,resource,subprocess,sys,time
import numpy as np,scipy
from scipy.optimize import minimize
from scipy.special import logsumexp
from physics import *
from data import load,ROOT,P
NAMES=['Draco','Sextans','Fornax','Leo I']
PREV=ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json'
PROFILES={
 'Draco_initial':('sol61_push/cold_envelope_formation_2026_10_24/runs/draco_escape_long','initial'),
 'Sextans_initial':('sol61_push/cold_envelope_formation_2026_10_24/runs/sextans_escape_long','initial'),
 'Fornax_initial':('sol61_push/cold_material_transport_2026_10_24/runs/fornax_matched_L8','initial'),
 'Leo I_initial':('sol61_push/cold_material_transport_2026_10_24/runs/leoi_matched_L8','initial'),
 'Sextans_legacy_late':('sol61_push/cold_envelope_formation_2026_10_24/runs/sextans_escape_long','final')}
DRACO='sol61_push/cold_core_binding_2026_10_25/late_runs/late_dt005'
def artifacts():
 PathSelf=pathlib.Path(__file__).resolve()
 fs=[PathSelf,P/'data.py',P/'physics.py',P/'test_physics.py',P/'CONTRACT.md',PREV,ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv',ROOT/'real_research/data/walker2023/ReadMe',ROOT/'real_research/data/walker2023/hectocat.dat.gz',ROOT/'real_research/data/walker2023/m2fshi.dat.gz',ROOT/'sol61_push/cold_survey_capture_2026_10_24/survey.py',ROOT/'sol61_push/cold_survey_capture_2026_10_24/data/members.tsv',ROOT/'sol61_push/cold_survey_capture_2026_10_24/data/ReadMe.txt',ROOT/'sol61_push/cold_core_binding_2026_10_25/binding_phase_runs/dt005.json']
 for base,field in PROFILES.values():fs.extend([ROOT/(base+'.json'),ROOT/(base+'_fields.npz')])
 fs.extend([ROOT/(DRACO+'.json'),ROOT/(DRACO+'.npz'),ROOT/'sol61_push/cold_resolved_pulse_2026_10_25/runs/draco_joint_s05.npz'])
 return sorted(set(fs))
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in artifacts()}
def profiles(name):
 rows=[]
 for tag,(base,field) in PROFILES.items():
  if not tag.startswith(name+'_'):continue
  meta=json.loads((ROOT/(base+'.json')).read_text());z=np.load(ROOT/(base+'_fields.npz'));r=z['r']*meta['physical']['Runit_pc'];dm=np.sum(abs(z[field])**2,axis=1)*meta['physical']['Munit_Msun'];z.close()
  rows.append(dict(tag=tag,r=r,dm=dm,parent_status=meta['status'],kind='initial condition' if field=='initial' else 'coarse legacy endpoint; not converged core proof'))
 if name=='Draco':
  meta=json.loads((ROOT/(DRACO+'.json')).read_text());z=np.load(ROOT/(DRACO+'.npz'));dm=np.sum(abs(z['u'])**2,axis=(1,2))*meta['physical']['Munit_Msun'];z.close()
  grid=np.load(ROOT/'sol61_push/cold_resolved_pulse_2026_10_25/runs/draco_joint_s05.npz');r=grid['r']*meta['physical']['Runit_pc'];grid.close()
  assert len(dm)==len(r)
  rows.append(dict(tag='Draco_fine_late',r=r,dm=dm,parent_status=meta['status'],kind='clean fine short endpoint; full-state convergence not established'))
 return rows

def prior(d):
 if d['name']!='Sextans':return np.zeros((len(d['R']),1))
 R=d['R']; phot=np.array([-math.log(math.pi*a*a)-2*np.log1p((R/a)**2) for a in d['aa']]).T
 met=np.array([-.5*np.log(2*math.pi*(d['efe']**2+s*s))-.5*(d['fe']-m)**2/(d['efe']**2+s*s) for m,s in [(-2.09,.30),(-2.81,.13)]]).T
 return phot+met

def nll(d,var,mu,logit=0.,contam=0.):
 var=var+d['ev'][:,None]**2;logv=window_logpdf(d['v'][:,None],mu,var,d['lo'][:,None],d['hi'][:,None])
 if var.shape[1]==1:ll=logv[:,0]
 else:
  f=1/(1+np.exp(-logit));lp=d['logprior']+np.log([f,1-f]);lp-=logsumexp(lp,axis=1)[:,None]
  logz=np.log(np.maximum(ndtr((d['hi'][:,None]-mu)/np.sqrt(var))-ndtr((d['lo'][:,None]-mu)/np.sqrt(var)),1e-300))
  ll=logsumexp(lp+logv+logz,axis=1)-logsumexp(lp+logz,axis=1)
 if contam:ll=np.logaddexp(np.log1p(-contam)+ll,np.log(contam/(d['hi']-d['lo'])))
 return -float(ll.sum())

def rms_sigma(d,var,mu,logit):
 if var.shape[1]==1:return float(np.sqrt(np.mean(var)))
 vv=var+d['ev'][:,None]**2;f=1/(1+np.exp(-logit));lp=d['logprior']+np.log([f,1-f]);lz=np.log(np.maximum(ndtr((d['hi'][:,None]-mu)/np.sqrt(vv))-ndtr((d['lo'][:,None]-mu)/np.sqrt(vv)),1e-300));lp=lp+lz;lp-=logsumexp(lp,axis=1)[:,None]
 return float(np.sqrt(np.mean(np.sum(np.exp(lp)*var,axis=1))))

def constant_fit(d):
 def obj(x):return -float(np.sum(window_logpdf(d['v'],x[0],np.exp(2*x[1])+d['ev']**2,d['lo'],d['hi'])))
 vs=float(d['cat']['vlos_systemic']);s=minimize(obj,[np.median(d['v']),math.log(9.)],bounds=[(vs-15,vs+15),(math.log(.1),math.log(50.))],method='L-BFGS-B')
 return dict(nll=float(s.fun),intrinsic_sigma_kms=float(np.exp(s.x[1])),mu=float(s.x[0]),optimizer_success=bool(s.success))

def nuisance(d,var,contam=0.):
 vs=float(d['cat']['vlos_systemic']);two=var.shape[1]>1
 def obj(x):return nll(d,var,x[0],x[1] if two else 0.,contam)
 opt=minimize(obj,[np.median(d['v'])]+([.5] if two else []),bounds=[(vs-15,vs+15)]+([(-4,4)] if two else []),method='L-BFGS-B')
 return dict(nll=float(opt.fun),mu=float(opt.x[0]),logit=float(opt.x[1]) if two else 0.,optimizer_success=bool(opt.success))

def interpolate(kernels,lb,logb):
 j=min(len(lb)-2,max(0,int(np.searchsorted(lb,logb)-1)));f=(logb-lb[j])/(lb[j+1]-lb[j]);return np.exp((1-f)*np.log(kernels[j])+f*np.log(kernels[j+1]))

def family_fit(d,base,kernels,lb,mass=None,contam=0.):
 # The envelope mass is in Msun; kernel has 1e8 Msun normalization.
 two=len(d['aa'])==2;vs=float(d['cat']['vlos_systemic']);a=float(d['cat']['rhalf_sph_physical'])
 bounds=[(float(lb[0]),float(lb[-1])),(vs-15,vs+15)]+([(-4,4)] if two else [])+([(math.log(1e4),math.log(1e13))] if mass is None else [])
 def unpack(x):return (float(np.exp(x[-1])) if mass is None else mass,x[0],x[1],x[2] if two else 0.)
 def obj(x):
  m,b,mu,l=unpack(x);return nll(d,base+m/1e8*interpolate(kernels,lb,b),mu,l,contam)
 sols=[]
 for ratio in [.5,2.,8.,32.,100.]:
  x=[float(np.clip(math.log(a*ratio),lb[0],lb[-1])),float(np.median(d['v']))]+([.5] if two else [])+([math.log(1e8 if ratio<8 else 1e10)] if mass is None else [])
  sols.append(minimize(obj,x,bounds=bounds,method='L-BFGS-B',options={'ftol':1e-11,'maxiter':300}))
 opt=min(sols,key=lambda s:s.fun);m,b,mu,l=unpack(opt.x)
 return dict(nll=float(opt.fun),cold_mass_Msun=m,scale_pc=float(np.exp(b)),mu=mu,logit=l,optimizer_success=bool(opt.success),scale_at_grid_edge=bool(min(b-lb[0],lb[-1]-b)<.001),mass_at_bound=bool(mass is None and (m<1.01e4 or m>9.9e12)))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--sensitivity',action='store_true');args=ap.parse_args();outdir=pathlib.Path(args.out);outdir.mkdir(parents=True,exist_ok=True);assert not (outdir/'result.json').exists()
 before=hashes();start=time.time();revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();prev=json.loads(PREV.read_text());rows=[];datasets={};cache={};checks={};shared=[]
 for name in NAMES:
  d=load(name);d['logprior']=prior(d);a=float(d['cat']['rhalf_sph_physical']);ms=5e5 if name=='Sextans' else prev['galaxies'][name]['populations'][0]['stellar_mass'];formed=ms/.59 if name=='Sextans' else prev['galaxies'][name]['populations'][0]['formed_mass'];supply=5.364*200*formed
  datasets[name]=dict(counts=d['counts'],coverage=d['coverage'],ids=d['ids'],source_rows=d.get('source_rows'),selection=d.get('selection'),R_pc=d['R'].tolist(),vel_kms=d['v'].tolist(),error_kms=d['ev'].tolist(),tracer_scales_pc=d['aa'].tolist(),stellar_mass_Msun=ms,formed_mass_Msun=formed,supply_Msun=supply,selected_constant_sigma_fit=constant_fit(d),observed_global_sigma_kms=float(d['cat']['vlos_sigma']),observed_sigma_errors_kms=[float(d['cat']['vlos_sigma_em']),float(d['cat']['vlos_sigma_ep'])],observed_rhalf_pc=a,observed_rhalf_errors_pc=[float(d['cat']['rhalf_sph_physical_em']),float(d['cat']['rhalf_sph_physical_ep'])])
  pp=profiles(name);bs=a*np.geomspace(.125,512,121);lb=np.log(bs)
  for beta in [-.5,0.,.5]:
   kernels=np.array([[project(d['R'],ar,lambda r,b=b:plummer_g(r,1e8,b),beta) for ar in d['aa']] for b in bs]).transpose(0,2,1)
   for foot in A0:
    base=np.array([project(d['R'],ar,lambda r:baryon_g(r,ms,d['aa'],foot),beta) for ar in d['aa']]).T
    free=family_fit(d,base,kernels,lb);fixed=[];trials=[]
    for f in [.25,.5,1.]:
     fit=family_fit(d,base,kernels,lb,supply*f);b=fit['scale_pc'];m=fit['cold_mass_Msun'];rad=np.array([a,d['coverage']['R_pc_percentiles'][3],3000.,10000.]);fit.update(retention=f,b_over_a=b/a,M_at_radii_pc=rad.tolist(),enclosed_Msun=(m*rad**3/(rad*rad+b*b)**1.5).tolist(),central_escape_speed_kms=math.sqrt(2*G*m/b),two_delta_nll=2*(fit['nll']-free['nll']));fixed.append(fit)
    for prof in pp:
     r,dm=prof['r'],prof['dm'];cv=np.array([project(d['R'],ar,lambda q:g_cold(q,r,dm),beta) for ar in d['aa']]).T
     fit=nuisance(d,base+cv);rad=np.array([a,d['coverage']['R_pc_percentiles'][3],3000.,10000.]);fit.update(tag=prof['tag'],kind=prof['kind'],parent_status=prof['parent_status'],total_Msun=float(dm.sum()),enclosed_at_radii_pc=rad.tolist(),enclosed_Msun=np.cumsum(dm)[np.minimum(len(dm)-1,np.searchsorted(r,rad,side='right')-1)].tolist(),selected_position_rms_sigma_kms=rms_sigma(d,base+cv,fit['mu'],fit['logit']),cold_component_position_rms_sigma_kms=np.sqrt(np.mean(cv,axis=0)).tolist(),two_delta_nll=2*(fit['nll']-free['nll']));trials.append(fit)
     if beta==0 and foot=='canonical':
      fine=np.array([project(d['R'],ar,lambda q:g_cold(q,r,dm),beta,nr=16384,nz=256) for ar in d['aa']]).T
      checks[prof['tag']+'_projection_relative_refine']=float(np.max(abs(cv/fine-1)))
    row=dict(name=name,footing=foot,beta=beta,beta_DF_warning=('positive constant anisotropy with cored tracer/finite potential is not a physical equilibrium DF' if beta>0 else 'DF positivity not demonstrated'),free_Plummer=free,fixed_supply_envelopes=fixed,trial_profiles=trials,baryon_only=nuisance(d,base))
    if beta==0 and foot=='canonical':
     row['contamination_5percent']=family_fit(d,base,kernels,lb,supply*.5,.05)
     if name!='Sextans':
      sens=[]
      for label,kw in [('window35',{'halfwindow':35.}),('pmfloor02',{'pmfloor':.02}),('include_velocity_variables',{'variables':True})]:
       ds=load(name,**kw);ds['logprior']=prior(ds);bb=np.array([project(ds['R'],ar,lambda r:baryon_g(r,ms,ds['aa'],foot),beta) for ar in ds['aa']]).T
       kk=np.array([[project(ds['R'],ar,lambda r,b=b:plummer_g(r,1e8,b),beta) for ar in ds['aa']] for b in bs]).transpose(0,2,1)
       fit=family_fit(ds,bb,kk,lb,supply*.5);fit.update(label=label,n=len(ds['R']),ids=ds['ids']);sens.append(fit)
      row['selection_sensitivities']=sens
     b=free['scale_pc'];direct=np.array([project(d['R'],ar,lambda r:plummer_g(r,1e8,b),beta,nr=8192,nz=256) for ar in d['aa']]).T
     checks[name+'_Plummer_interpolation_and_refine']=float(np.max(abs(interpolate(kernels,lb,math.log(b))/direct-1)))
    rows.append(row);cache[(name,foot,beta)]=(d,base,kernels,lb,supply,a)
    print(name,foot,beta,'free',round(free['cold_mass_Msun']/1e6,2),round(free['scale_pc'],1),'fixed half',round(fixed[1]['scale_pc'],1),round(fixed[1]['two_delta_nll'],2),flush=True)
  if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>750_000_000:raise RuntimeError('memory headroom')
 # Joint fits of a COMMON relative scale, without pooling footings or beta.
 for foot in A0:
  for beta in [-.5,0.,.5]:
   for f in [.25,.5,1.]:
    two_index=1+len(NAMES)
    def objective(x):
     ans=0.
     for j,name in enumerate(NAMES):
      d,base,kern,lb,supply,a=cache[(name,foot,beta)];b=np.log(a)+x[0]
      ans+=nll(d,base+f*supply/1e8*interpolate(kern,lb,b),x[1+j],x[two_index] if name=='Sextans' else 0.)
     return ans
    bounds=[(math.log(.125),math.log(512))]+[(float(cache[(n,foot,beta)][0]['cat']['vlos_systemic'])-15,float(cache[(n,foot,beta)][0]['cat']['vlos_systemic'])+15) for n in NAMES]+[(-4,4)]
    sols=[minimize(objective,[math.log(q)]+[float(np.median(cache[(n,foot,beta)][0]['v'])) for n in NAMES]+[.5],method='L-BFGS-B',bounds=bounds,options={'ftol':1e-11,'maxiter':500}) for q in [.5,2.,8.,32.,100.]];s=min(sols,key=lambda x:x.fun)
    comps=[]
    for j,name in enumerate(NAMES):
     d,base,kern,lb,supply,a=cache[(name,foot,beta)];var=base+f*supply/1e8*interpolate(kern,lb,math.log(a)+s.x[0]);own=next(r for r in rows if r['name']==name and r['footing']==foot and r['beta']==beta);fit=next(z for z in own['fixed_supply_envelopes'] if z['retention']==f)
     comps.append(dict(name=name,nll=nll(d,var,s.x[1+j],s.x[two_index] if name=='Sextans' else 0.),independent_scale_nll=fit['nll'],position_rms_sigma=rms_sigma(d,var,s.x[1+j],s.x[two_index] if name=='Sextans' else 0.)))
    shared.append(dict(footing=foot,beta=beta,retention=f,b_over_a=float(np.exp(s.x[0])),nll=float(s.fun),two_delta_nll_vs_separate_scales=2*(float(s.fun)-sum(c['independent_scale_nll'] for c in comps)),components=comps,optimizer_success=bool(s.success)))
 result=dict(scope='conditional spherical Jeans screens and inverse full-envelope constructions; not a supported cold solution, retained material mass or stellar survival certificate',datasets=datasets,rows=rows,shared_scale_tests=shared,checks=checks,seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,inputs_before=before,inputs_after=hashes(),revision_before=revision,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),software=dict(Python=sys.version,numpy=np.__version__,scipy=scipy.__version__))
 assert before==result['inputs_after'];(outdir/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('DONE',result['seconds'],result['peak_RSS_bytes'],checks,flush=True)
if __name__=='__main__':main()
