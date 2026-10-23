import json,sys
from equilibrium import solve
from spectrum import modes
case=sys.argv[1];out=sys.argv[2];records=[]
if case=='family':
 for K in [.01,.025,.05,.1]:
  last=None
  for mult in [.5,1,2,4]:
   s,r=solve(M=.08408132497418408*mult,K=K,guess=last);last=s if s.success else None;records.append(r);print(K,mult,r['success'],r['r50'],r['residual'],flush=True)
elif case=='refinement':
 for R,n,tol in [(24,600,1e-6),(36,1200,2e-7),(48,1600,1e-7)]:
  s,r=solve(R=R,n=n,tol=tol);records.append(r);print(R,r['success'],r['r50'],flush=True)
elif case=='spectrum':
 s,r=solve(R=36,n=1000,tol=1e-7)
 for n in [300,600,900]:
  q=modes(s,.05,R=36,n=n,lmax=8);records.append(q);print(n,[(m['l'],m['eigenvalues'][0]) for m in q['modes']],flush=True)
json.dump(records,open(out,'w'),indent=2)
