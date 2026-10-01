"""Matched constant-spin numerical benchmark and bounded stale-force repair. Neither is a physical proposal."""
import pathlib,sys,time,json,hashlib,importlib.util
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'mirror/campaign_fresh_gravity'));sys.dont_write_bytecode=True
import CFG5_common as C
mods={}
for name,file in [('original_events','engine_constant_j.py'),('refresh_after_events','engine_constant_j_force_refresh.py')]:
 spec=importlib.util.spec_from_file_location(name,HERE/file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);mods[name]=m
T=time.monotonic();E=mods['original_events'];sig=E.Sigma();p0=sig.Pk.copy();RG=np.geomspace(.2,3000,400);runs={}
sha=lambda a:hashlib.sha256(np.asarray(a).tobytes()).hexdigest()
for method,E in mods.items():
 cases=[('600',600,24,.03,0.),('1000',1000,40,.03,0.),('2000',2000,80,.03,0.),('600_tiny_spectrum_shift',600,24,.03,1e-7)]
 if method=='refresh_after_events':cases.append(('2000_halfstep',2000,80,.015,0.))
 for label,N,nb,eta,shift in cases:
  name=method+'/'+label;sig.Pk=p0*(1+shift);print('START',name,flush=True);t=time.monotonic()
  r=E.run(sig,1e12,C.FOOT['canonical'],trigger=True,cooling=False,Nc=N,nb=nb,eta=eta,seed=1)
  Md,Mdau,Mb=E.profiles(r,RG);r200=E.r200_of(RG,Md+Mb);md200=float(np.interp(r200,RG,Md));h=E.GK*Md/RG**2*1e6/C.KPC/C.FOOT['canonical']
  runs[name]={'method':method,'N':N,'nb':nb,'eta':eta,'power_shift':shift,'hmax':float(h[RG<=r200].max()),'conversion_fraction':r['budget']['converted']/md200,'budget':r['budget'],'r200':r200,'nstep':r['nstep'],'runtime_seconds':time.monotonic()-t,'Md':Md.tolist(),'Mb':Mb.tolist(),'Md_sha256':sha(Md),'initial_profile_sha256':[sha(a) for a in E.initial_profile(sig,1e12,N)]}
  print('END',name,'h',runs[name]['hmax'],'fc',runs[name]['conversion_fraction'],'seconds',runs[name]['runtime_seconds'],flush=True)
  (HERE/'matched_partial.json').write_text(json.dumps(runs,indent=2))
out={'runs':runs,'runtime_seconds':time.monotonic()-T,'Pk_baseline_sha256':sha(p0),'sources':{str(HERE/f):hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in ['engine_constant_j.py','engine_constant_j_force_refresh.py','matched_benchmark.py']},'changes':['constant angular coefficient .25 everywhere, numerical benchmark','refresh clone recomputes enclosed mass and acceleration after event impulses; original source untouched'],'limitations':['Daughter directions remain original finite stochastic sampler; population/sample counts change with Nc','Fixed neighbour fraction is not fixed Eulerian physical width','No event-time interpolation added','No covariant action or physical parameter elimination claimed']}
(HERE/'matched_results.json').write_text(json.dumps(out,indent=2));print('Runtime',out['runtime_seconds'])
