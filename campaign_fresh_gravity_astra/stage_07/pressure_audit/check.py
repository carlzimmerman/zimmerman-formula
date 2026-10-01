import json,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
P=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results')
n=np.load(P/'FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz')
r=json.loads((P/'FGF-021/fgf021_run_001/numeric_001/results.json').read_text())
f=lambda x:F(float(x))
H=[[f(x) for x in row] for row in n['H']]; L=list(map(f,n['L'])); base=list(map(f,n['baseline'])); s=F(r['s'])
dot=lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))
E=[[sum(row[:j+1]) for j in range(15)]+[row[15]] for row in H]
c=[sum(L[:j+1]) for j in range(15)]+[L[15]]
d=[dot(row,base)/s for row in H]
checks={}; vals=[]
for key,sign in [('min_certificate',1),('max_certificate',-1)]:
 cert=r[key]; u=list(map(F,cert['u_exact'])); y=list(map(F,cert['equality_dual_exact']))
 w=[sign*c[j]-dot([row[j] for row in E],y) for j in range(16)]
 assert all(dot(row,u)==a for row,a in zip(E,d))
 assert all(x>=0 for x in u[:15]) and all(x>=0 for x in w[:15]) and w[15]==0
 assert dot(w,u)==0 and sign*dot(c,u)==dot(y,d)
 assert sign*dot(c,u)==F(cert['objective_exact'])
 p=[s*sum(u[j:15]) for j in range(15)]+[s*u[15]]
 assert all(dot(row,p)==s*a for row,a in zip(H,d))
 assert all(p[j]>=p[j+1] for j in range(14)) and p[14]>=0
 v=dot(L,p); vals.append(v)
 damaged=u.copy(); damaged[0]+=F(1,1000)
 assert any(dot(row,damaged)!=a for row,a in zip(E,d))
 bad_y=y.copy(); bad_y[0]+=1
 assert sign*c[15]-dot([row[15] for row in E],bad_y)!=0
 checks[key]={'primal_dual_exact':True,'damaged_primal_rejected':True,'damaged_dual_rejected':True,'gradient':float(v)}
u=list(map(F,r['actual_map']['certificate']['u_exact'])); assert u[-1]==0
assert all(x>=0 for x in u[:15])
obs=list(map(f,n['observed_annular_y']))
assert all(s*dot(row,u[:16])==v for row,v in zip(E,obs))
assert all(base[j]>base[j+1] for j in range(14)) and base[14]>0
out={'checks':checks,'actual_map_exact_feasible_residual':0,'residual_optimality':'t>=0 and exact feasible t=0','strict_baseline_verified':True,'width_fraction':float((vals[1]-vals[0])/abs(dot(L,base))),'scope':'Exact stored rational matrix only; no continuum/instrument accuracy or confidence claim; no worker implementation imported.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out))
