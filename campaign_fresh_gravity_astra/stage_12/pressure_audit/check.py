from fractions import Fraction as F
from pathlib import Path
import numpy as np,json,sys
src=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz')
a=np.load(src);H=[[F(float(x)) for x in row] for row in a['H']];L=[F(float(x)) for x in a['L']];p=[F(float(x)) for x in a['baseline']]
dot=lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))
def rr(rows):
 a=[r[:] for r in rows];piv=[];k=0
 for j in range(len(a[0])):
  i=next((i for i in range(k,len(a)) if a[i][j]),None)
  if i is None:continue
  a[k],a[i]=a[i],a[k];d=a[k][j];a[k]=[x/d for x in a[k]]
  for i in range(len(a)):
   if i!=k:
    d=a[i][j];a[i]=[x-d*y for x,y in zip(a[i],a[k])]
  piv.append(j);k+=1
  if k==len(a):break
 return a,piv
C=H+[[F(i==15) for i in range(16)]];A,piv=rr(C);assert piv==list(range(12))+[15]
N=[]
for j in [12,13,14]:
 v=[F(0)]*16;v[j]=1
 for k,c in enumerate(piv):v[c]=-A[k][j]
 assert all(dot(r,v)==0 for r in C);N.append(v)
ell=[dot(L,v) for v in N];assert all(ell)
wp=[F(0)]*12+ell+[F(0)];wm=[F(0)]*12+[F(1),F(0),F(0),F(0)]
orth=[ell[1],-ell[0],F(0)];wo=[F(0)]*12+orth+[F(0)]
rank=lambda rows:len(rr(rows)[1])
assert rank(C)==13 and rank(C+[wp])==14 and rank(C+[wp,L])==14
assert rank(C+[wm])==14 and rank(C+[wm,L])==15
assert rank(C+[wo])==14 and rank(C+[wo,L])==15
assert rank(C+[wp,wm])==15 and rank(C+[wp,wm,L])==15
assert rank(C+[[F(i==j) for i in range(16)] for j in [12,13,14]])==16
v=N[1];marg=[p[i]-p[i+1] for i in range(14)]+[p[14]];dm=[v[i]-v[i+1] for i in range(14)]+[v[14]]
assert min(marg)>0;eps=min(m/abs(d) for m,d in zip(marg,dm) if d)/2
witness=[[x+sign*eps*y for x,y in zip(p,v)] for sign in [-1,1]]
for z in witness:
 assert all(dot(r,z)==dot(r,p) for r in C+[wm]);assert min([z[i]-z[i+1] for i in range(14)]+[z[14]])>0
assert dot(L,witness[0])!=dot(L,witness[1])
# Equality of target and aligned outer row on the null space, independently
# of measured-bin particular solution. A mutant row must fail.
assert [dot(wp,v) for v in N]==ell
bad=wp[:];bad[12]+=1;assert rank(C+[bad,L])>rank(C+[bad])
out={'coefficient_domain':'exact rationals of stored binary64','pivots':piv,'null_basis_exact':[list(map(str,v)) for v in N],'ell_exact':list(map(str,ell)),'ell_float':[float(x) for x in ell],'rank_C':13,'positive_rank':14,'positive_augmented_target_rank':14,'positive_remaining_nullity':2,'negative_rank':14,'negative_augmented_target_rank':15,'orthogonal_control_failed_identification':True,'damaged_aligned_row_rejected':True,'negative_witness_epsilon':str(eps),'negative_witnesses_exact':[list(map(str,z)) for z in witness],'negative_gradients':[float(dot(L,z)) for z in witness],'checks_passed':True,'non_claims':['Instrument observation','Continuum identifiability','Mass inference','Noise robustness']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if 'exact' not in k and 'epsilon' not in k}))
