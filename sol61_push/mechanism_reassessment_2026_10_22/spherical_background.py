import json,sys
import numpy as np
from scipy.integrate import solve_bvp
mutate='--mutate' in sys.argv

def solve(eps,end,tol):
    r=np.geomspace(1e-5,end,700)
    n=r/(1+r*r)**1.5
    q=(np.sqrt(n*n+4*n)-n)/2
    def fun(s,y):
        q,d=y
        return np.array([d,(q*q/(1-q)-s/(1+s*s)**1.5)/eps**2-2*d/s+(0 if mutate else 2)*q/s**2])
    def bc(a,b): return np.array([a[1]-a[0]/1e-5,b[1]+b[0]/end])
    return solve_bvp(fun,bc,r,np.array([q,np.gradient(q,r)]),tol=tol,max_nodes=15000)
rows=[]
for eps in [.03,.1,.3]:
    a=solve(eps,100,1e-6); b=solve(eps,100,2e-8); c=solve(eps,200,2e-8)
    s=np.geomspace(1e-4,50,1500); q,d=b.sol(s); dd=b.sol(s,1)[1]
    residual=eps**2*(dd+2*d/s-2*q/s**2)-q*q/(1-q)+s/(1+s*s)**1.5
    n=s/(1+s*s)**1.5; algebra=(np.sqrt(n*n+4*n)-n)/2
    rows.append(dict(epsilon=eps,statuses=[a.status,b.status,c.status],nodes=[a.x.size,b.x.size,c.x.size],min_q=float(q.min()),max_q=float(q.max()),refinement=float(np.max(np.abs(a.sol(s)[0]-q))),domain_change=float(np.max(np.abs(c.sol(s)[0]-q))),residual=float(np.max(np.abs(residual))),central_slope=float(b.sol(1e-5)[0]/1e-5),predicted_core_scale=eps**.8,profile=[dict(r=float(t),q=float(b.sol(t)[0]),q_algebra=float((np.sqrt((t/(1+t*t)**1.5)**2+4*t/(1+t*t)**1.5)-t/(1+t*t)**1.5)/2)) for t in [.001,.01,.1,1,10,50]]))
checks=dict(converged=all(all(s==0 for s in r['statuses']) for r in rows),admissible=all(0<r['min_q']<r['max_q']<1 for r in rows),refined=all(r['refinement']<1e-4 for r in rows),outer_domain=all(r['domain_change']<1e-4 for r in rows),original_equation=all(r['residual']<1e-4 for r in rows))
out=dict(rows=rows,checks=checks,all_pass=all(checks.values()),mutated=mutate)
with open(sys.argv[1],'w') as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
