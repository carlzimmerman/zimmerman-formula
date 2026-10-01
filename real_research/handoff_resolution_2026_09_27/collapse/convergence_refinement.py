"""Higher-resolution fixed-neighbour-fraction and half-step discriminator, unchanged CFG5 engine."""
import pathlib,sys,time,json,hashlib,platform
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'mirror/campaign_fresh_gravity'));sys.dont_write_bytecode=True
import CFG5_common as C,CFG5_collapse_engine as E
T=time.monotonic();sig=E.Sigma();RG=np.geomspace(.2,3000,400);rows={}
sha=lambda a:hashlib.sha256(np.asarray(a).tobytes()).hexdigest()
for name,N,nb,eta in [('N1000_nb40_halfstep',1000,40,.015),('N2000_nb80',2000,80,.03),('N2000_nb80_halfstep',2000,80,.015)]:
 print('START',name,flush=True);t=time.monotonic();r=E.run(sig,1e12,C.FOOT['canonical'],trigger=True,cooling=False,Nc=N,nb=nb,eta=eta,seed=1)
 Md,Mdau,Mb=E.profiles(r,RG);R200=E.r200_of(RG,Md+Mb);md200=float(np.interp(R200,RG,Md));h=E.GK*Md/RG**2*1e6/C.KPC/C.FOOT['canonical']
 rows[name]={'N':N,'nb':nb,'eta':eta,'hmax':float(h[RG<=R200].max()),'converted_fraction':r['budget']['converted']/md200,'budget':r['budget'],'nstep':r['nstep'],'seconds':time.monotonic()-t,'Md':Md.tolist(),'Mb':Mb.tolist(),'rgrid_kpc':RG.tolist(),'r200':R200,'initial_profile_hashes':[sha(a) for a in E.initial_profile(sig,1e12,N)]}
 print('END',name,'h',rows[name]['hmax'],'fraction',rows[name]['converted_fraction'],'seconds',rows[name]['seconds'],flush=True)
 (HERE/'refinement_partial.json').write_text(json.dumps(rows,indent=2))
out={'runs':rows,'runtime_seconds':time.monotonic()-T,'sigma8':sig.sigma8,'Pk_sha256':sha(sig.Pk),'python':sys.version,'numpy':np.__version__,'source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [pathlib.Path(E.__file__),pathlib.Path(C.__file__),pathlib.Path(__file__)]},'limitations':['Same seed is not same angular momentum realization when shell count changes','Neighbour fraction fixed in index, not exact Eulerian physical width as collapse changes','No claim of continuum convergence or physical model repair'],'checks':{'finite_nonnegative_mass_profiles':all(np.isfinite(r['Md']).all() and min(r['Md'])>=0 for r in rows.values())}}
(HERE/'refinement_results.json').write_text(json.dumps(out,indent=2));print('Runtime',out['runtime_seconds'],flush=True)
