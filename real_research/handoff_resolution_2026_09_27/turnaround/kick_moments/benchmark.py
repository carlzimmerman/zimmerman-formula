import pathlib,sys,time,json,hashlib,platform
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent;COL=HERE.parents[1]/'collapse';sys.path.insert(0,str(COL/'mirror/campaign_fresh_gravity'));sys.dont_write_bytecode=True
import CFG5_common as C
import engine_exact as E
T=time.monotonic();sig=E.Sigma();p0=sig.Pk.copy();RG=np.geomspace(.2,3000,400);runs={}
sha=lambda a:hashlib.sha256(np.asarray(a).tobytes()).hexdigest()
for foot,a0 in C.FOOT.items():
 for cadence in [5,1]:
  cases=[(N,eta,0.) for N in [600,1000,2000] for eta in [.03,.015]]+[(600,.03,1e-7)]
  for N,eta,shift in cases:
   name=f'{foot}/cadence{cadence}/N{N}/eta{eta}/shift{shift}'
   if time.monotonic()-T>480:raise RuntimeError('bounded runtime guard reached; partial results preserved')
   sig.Pk=p0*(1+shift);print('START',name,flush=True);t=time.monotonic()
   r=E.run(sig,1e12,a0,trigger=True,cooling=False,Nc=N,nb=round(.04*N),eta=eta,seed=1,trigger_cadence=cadence)
   Md,Mdau,Mb=E.profiles(r,RG);r200=E.r200_of(RG,Md+Mb);md200=float(np.interp(r200,RG,Md));h=E.GK*Md/RG**2*1e6/C.KPC/a0
   runs[name]={'foot':foot,'a0':a0,'N':N,'nb':round(.04*N),'eta':eta,'cadence':cadence,'power_shift':shift,'hmax':float(h[RG<=r200].max()),'conversion_fraction':r['budget']['converted']/md200,'budget':r['budget'],'r200':r200,'nstep':r['nstep'],'runtime_seconds':time.monotonic()-t,'Md':Md.tolist(),'Mb':Mb.tolist(),'Md_sha256':sha(Md),'initial_profile_sha256':[sha(x) for x in E.initial_profile(sig,1e12,N)]}
   print('END',name,'h',runs[name]['hmax'],'fc',runs[name]['conversion_fraction'],'seconds',runs[name]['runtime_seconds'],flush=True)
   (HERE/'partial.json').write_text(json.dumps(runs,indent=2))
files=[HERE/'engine_exact.py',HERE/'exact_moments.py',HERE/'benchmark.py',COL/'engine_constant_j_force_refresh.py',COL/'mirror/campaign_fresh_gravity/CFG5_common.py']
out={'runs':runs,'runtime_seconds':time.monotonic()-T,'rgrid_kpc':RG.tolist(),'Pk_baseline_sha256':sha(p0),'sigma8':sig.sigma8,'sources':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'software':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform()},'limitations':['Exact angular moments only; same one-daughter moment closure','Fixed neighbor fraction .04, not fixed physical smoothing width','No event-time interpolation','constant spin .25 and no cooling benchmark, not main physical forecast']}
(HERE/'results.json').write_text(json.dumps(out,indent=2));print('FINISHED seconds',out['runtime_seconds'],flush=True)
