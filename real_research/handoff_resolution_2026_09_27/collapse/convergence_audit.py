"""Bounded one-host convergence and input-sensitivity discriminator for unchanged CFG5 engine."""
import pathlib,sys,os,json,time,hashlib,platform,subprocess
import numpy as np,scipy
HERE=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(HERE/'mirror/campaign_fresh_gravity'))
import CFG5_common as C, CFG5_collapse_engine as E
T=time.monotonic(); started=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
sig=E.Sigma();Pk0=sig.Pk.copy();RG=np.geomspace(.2,3000,400)
sha=lambda a:hashlib.sha256(np.asarray(a).tobytes()).hexdigest()
arrays={'k':sha(sig.k),'Pk':sha(Pk0)}
results={}
cases=[('N600_nb24',600,24,.03,0.),('repeat_N600_nb24',600,24,.03,0.),('N1000_nb24',1000,24,.03,0.),('N1000_nb40',1000,40,.03,0.),('N600_tighter_step',600,24,.015,0.),('N600_tiny_spectrum_shift',600,24,.03,1e-7)]
for name,n,nb,eta,shift in cases:
 sig.Pk=Pk0*(1+shift)
 init=E.initial_profile(sig,1e12,n)
 print('START',name,flush=True);t=time.monotonic()
 r=E.run(sig,1e12,C.FOOT['canonical'],trigger=True,cooling=False,Nc=n,nb=nb,eta=eta,seed=1)
 Md,Mdau,Mb=E.profiles(r,RG);R200=E.r200_of(RG,Md+Mb);inside=RG<=R200
 H=E.GK*Md/RG**2*1e6/C.KPC/C.FOOT['canonical'];md200=float(np.interp(R200,RG,Md))
 out={'Nc':n,'nb':nb,'eta':eta,'spectrum_fractional_shift':shift,'Pk_sha256':sha(sig.Pk),'initial_profile_sha256':[sha(a) for a in init],'hmax':float(H[inside].max()),'r200':R200,'dark_mass_r200':md200,'converted_fraction_same_CFG5_denominator':r['budget']['converted']/md200,'budget':r['budget'],'profile_sha256':{'Md':sha(Md),'Mb':sha(Mb),'daughter':sha(Mdau)},'nstep':r['nstep'],'seconds':time.monotonic()-t,'Md':Md.tolist(),'Mb':Mb.tolist(),'rgrid_kpc':RG.tolist()}
 # Same source denominator: each fossil run's surviving dark mass inside its own r200.
 results[name]=out
 print('END',name,'hmax',out['hmax'],'converted',r['budget']['converted'],'seconds',out['seconds'],flush=True)
 (HERE/'convergence_partial.json').write_text(json.dumps(results,indent=2))
base=results['N600_nb24'];repeat=results['repeat_N600_nb24']
# Tiny input perturbation must not be silently represented as same-input repetition: mutation deliberately does this.
MUT=os.environ.get('MUTATE')=='1';candidate=results['N600_tiny_spectrum_shift'] if MUT else repeat
checks={'same_input_profile_repeatability':{'passed':candidate['initial_profile_sha256']==base['initial_profile_sha256'] and candidate['profile_sha256']==base['profile_sha256'],'value':{'same_initial_arrays':candidate['initial_profile_sha256']==base['initial_profile_sha256'],'same_output_arrays':candidate['profile_sha256']==base['profile_sha256']}},'positive_finite_profiles':{'passed':all(np.isfinite(v['Md']).all() and min(v['Md'])>=0 for v in results.values()),'value':len(results)}}
comp={}
for k,v in results.items():
 comp[k]={'hmax_ratio_to_600':v['hmax']/base['hmax'],'converted_mass_ratio_to_600':v['budget']['converted']/base['budget']['converted'],'profile_max_fractional_difference':float(np.max(abs(np.array(v['Md'])-np.array(base['Md']))/np.maximum(np.array(base['Md']),1e8)))}
engine=pathlib.Path(E.__file__);common=pathlib.Path(C.__file__)
out={'base':'48905ae11213afcb9ff1b7726530bb5dd1933fe3','started':started,'runtime_seconds':time.monotonic()-T,'software':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()},'modules':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [engine,common,pathlib.Path(__file__)]},'spectrum':{'sigma8':sig.sigma8,'arrays_sha256':arrays,'class_build':'class_provenance.json'},'checks':checks,'comparisons':comp,'runs':results,'limits':'six sequential 1e12-solar-mass dark-only runs; source thread caps cooperative; no full cosmological box','non_claims':['No continuum convergence from two shell counts','Cannot infer original generation environment from original unmanifested output','Canonical footing only for numerical diagnosis; original full main covers both footings']}
path=HERE/('convergence_results_MUTATE.json' if MUT else 'convergence_results.json');path.write_text(json.dumps(out,indent=2))
print(json.dumps(comp,indent=2),flush=True)
sys.exit(0 if all(v['passed'] for v in checks.values()) else 1)
