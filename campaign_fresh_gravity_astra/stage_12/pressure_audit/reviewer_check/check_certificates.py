import json,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
p=Path('campaign_fresh_gravity_astra/stage_12/pressure_audit')
r=json.loads((p/'run_001/results.json').read_text())
m=json.loads((p/'run_001/manifest.json').read_text())
checks=[]
for x in m['input_artifacts']:
 h=hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()
 assert h==x['sha256']==x['sha256_after']
 checks.append({'path':x['path'],'match':True})
for x in m['outputs']:
 assert hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256']
 checks.append({'path':x['path'],'match':True})
a=np.load('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz',allow_pickle=False)
H=[[F(float(t)) for t in row] for row in a['H']]
L=[F(float(t)) for t in a['L']]
p0=[F(float(t)) for t in a['baseline']]
N=[[F(t) for t in v] for v in r['null_basis_exact']]
ell=[F(t) for t in r['ell_exact']]
witnesses=[[F(t) for t in v] for v in r['negative_witnesses_exact']]
dot=lambda x,y:sum((a*b for a,b in zip(x,y)),F(0))
assert len(N)==3 and all(len(v)==16 for v in N)
for j,v in enumerate(N):
 assert all(dot(h,v)==0 for h in H) and v[15]==0
 assert [v[k] for k in (12,13,14)]==[F(i==j) for i in range(3)]
 assert dot(L,v)==ell[j] and ell[j]!=0
prime=65537
A=[[int(t.numerator%prime)*pow(int(t.denominator%prime),-1,prime)%prime for t in row[:12]] for row in H]
det=1
for k in range(12):
 j=next(j for j in range(k,12) if A[j][k])
 if j!=k:A[j],A[k]=A[k],A[j];det=-det
 pivot=A[k][k];det=det*pivot%prime;inv=pow(pivot,-1,prime)
 for i in range(k+1,12):
  mult=A[i][k]*inv%prime
  for t in range(k,12):A[i][t]=(A[i][t]-mult*A[k][t])%prime
assert det%prime!=0
wp=[F(0)]*12+ell+[F(0)]
wm=[F(0)]*12+[F(1),F(0),F(0),F(0)]
orth=[ell[1],-ell[0],F(0)]
assert [dot(wp,v) for v in N]==ell
assert [dot(wm,v) for v in N]==[1,0,0]
assert dot(orth,ell)==0 and any(orth)
assert ell[1]!=0 and ell[2]!=0
bad=ell[:];bad[0]+=1
assert bad[0]*ell[1]-bad[1]*ell[0]==ell[1]!=0
minimum_margins=[]
for v in [p0]+witnesses:
 margins=[v[i]-v[i+1] for i in range(14)]+[v[14]]
 assert min(margins)>0;minimum_margins.append(float(min(margins)))
for v in witnesses:
 assert all(dot(h,v)==dot(h,p0) for h in H)
 assert v[15]==p0[15] and dot(wm,v)==dot(wm,p0)
assert dot(L,witnesses[0])!=dot(L,witnesses[1])
out={'claim':'exact saved-operator certificate verification','coefficient_domain':'exact rationals of binary64 entries; one prime-field determinant certificate','manifest_hash_checks':checks,'exact_null_and_witness_certificates':'passed','inner_block_determinant_mod_prime':int(det%prime),'prime':prime,'baseline_and_two_witness_minimum_margins':minimum_margins,'target_values':[float(dot(L,v)) for v in witnesses],'target_gap_exact':str(dot(L,witnesses[1])-dot(L,witnesses[0])),'aligned_wrong_orthogonal_mutant_controls':'passed','worker_code_read':False,'limitations':['no instrument calibration','no continuum or noise-robustness inference','no force or missing-mass inference']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['manifest_hash_checks','target_gap_exact']},sort_keys=True))
