from pathlib import Path
from fractions import Fraction as F
import numpy as np,json,sys
P=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results');n=np.load(P/'FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz');r=json.loads((P/'FGF-022/fgf022_run_001/numeric_001/results.json').read_text());old=json.loads((P/'FGF-021/fgf021_run_001/numeric_001/results.json').read_text())
f=lambda x:F(float(x));dot=lambda a,b:sum((u*v for u,v in zip(a,b)),F(0));H=[[f(x) for x in row] for row in n['H']];L=list(map(f,n['L']));p=list(map(f,n['baseline']));s=F(r['scale_exact']);E=[[sum(row[:j+1]) for j in range(15)]+[row[15]] for row in H];c=[sum(L[:j+1]) for j in range(15)]+[L[15]];d=[dot(row,p)/s for row in H];e=[F(int(i==15)) for i in range(16)]
rows=[];last=None
for record in r['records']:
 beta=F(record['beta_exact']);eq=E+([e] if beta==0 else []);rhs=d+([F(0)] if beta==0 else []);A=[[-F(i==j) for j in range(16)] for i in range(15)];a=[F(0)]*15
 if beta: A +=[e,[-x for x in e]];a +=[beta/s,beta/s]
 vals=[]
 for side,sign in [('min',1),('max',-1)]:
  z=record[side];u=list(map(F,z['u_exact']));y=list(map(F,z['equality_dual_exact']));v=list(map(F,z['inequality_dual_exact']));cost=[sign*x for x in c]
  assert len(y)==len(eq) and len(v)==len(A)
  assert all(dot(row,u)==b for row,b in zip(eq,rhs));slack=[b-dot(row,u) for row,b in zip(A,a)];assert min(slack)>=0 and max(v)<=0
  assert all(cost[j]==dot([row[j] for row in eq],y)+dot([row[j] for row in A],v) for j in range(16))
  assert dot(cost,u)==dot(y,rhs)+dot(v,a) and dot(slack,v)==0
  pressure=[s*sum(u[j:15]) for j in range(15)]+[s*u[15]]
  assert all(dot(row,pressure)==dot(row,p) for row in H) and abs(pressure[-1]-p[-1])<=beta
  val=dot(L,pressure);assert val==F(z['gradient_exact']);vals.append(val)
  mutant=u.copy();mutant[-1]+=1;assert any(dot(row,mutant)!=b for row,b in zip(eq,rhs))
 if last: assert vals[0]<=last[0] and vals[1]>=last[1]
 last=vals;rows.append({'beta':float(beta),'min':float(vals[0]),'max':float(vals[1]),'width_fraction':float((vals[1]-vals[0])/abs(dot(L,p)))})
# Independently establish uniqueness of prior unrestricted vertices using exact rank.
def rank(a):
 a=[x[:] for x in a];k=0
 for j in range(16):
  idx=next((i for i in range(k,len(a)) if a[i][j]),None)
  if idx is None:continue
  a[k],a[idx]=a[idx],a[k];div=a[k][j];a[k]=[v/div for v in a[k]]
  for i in range(k+1,len(a)):
   fac=a[i][j];a[i]=[x-fac*y for x,y in zip(a[i],a[k])]
  k+=1
  if k==len(a):break
 return k
thresholds=[]
for side in ['min','max']:
 z=old[side+'_certificate'];dual=list(map(F,z['inequality_dual_exact']));active=[i for i,x in enumerate(dual) if x<0];mat=E+[[F(int(i==j)) for j in range(16)] for i in active];assert rank(mat)==16
 u=list(map(F,z['u_exact']));threshold=abs(s*u[-1]-p[-1]);assert threshold>0
 thresholds.append({'side':side,'unique_by_exact_rank':True,'necessary_sufficient_beta':float(threshold)})
out={'all_12_primal_dual_certificates_pass':True,'direct_H_and_offset_checks_pass':True,'mutants_rejected':True,'selected_intervals':rows,'unrestricted_recovery':thresholds,'scope':'Selected exact finite-model optima, not full breakpoint curve or calibrated observational uncertainty.'};Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
