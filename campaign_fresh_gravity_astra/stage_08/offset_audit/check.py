from fractions import Fraction as F
from pathlib import Path
import numpy as np,json,sys
src=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz')
n=np.load(src);toF=lambda z:F(float(z));H=[[toF(x) for x in row] for row in n['H']];L=list(map(toF,n['L']));p=list(map(toF,n['baseline']));dot=lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))
C=H+[[F(int(i==15)) for i in range(16)]];A=[row[:] for row in C]; piv=[]; r=0
for j in range(16):
 found=next((i for i in range(r,len(A)) if A[i][j]),None)
 if found is None:continue
 A[r],A[found]=A[found],A[r]; div=A[r][j];A[r]=[x/div for x in A[r]]
 for i in range(len(A)):
  if i!=r:
   mul=A[i][j];A[i]=[x-mul*y for x,y in zip(A[i],A[r])]
 piv.append(j);r+=1
 if r==len(A):break
V=[]
for j in set(range(16))-set(piv):
 v=[F(0)]*16;v[j]=1
 for i,col in enumerate(piv):v[col]=-A[i][j]
 V.append(v)
v=next(v for v in V if dot(L,v)!=0);assert all(dot(row,v)==0 for row in C)
margin=[p[i]-p[i+1] for i in range(14)]+[p[14]];dv=[v[i]-v[i+1] for i in range(14)]+[v[14]];assert min(margin)>0
eps=min(m/abs(d) for m,d in zip(margin,dv) if d)/2
pm=[[x+sign*eps*y for x,y in zip(p,v)] for sign in [-1,1]]
for z in pm:
 assert all(dot(row,z)==dot(row,p) for row in C)
 assert all(z[i]>z[i+1] for i in range(14)) and z[14]>0
assert dot(L,pm[0])!=dot(L,pm[1])
bad=v[:];bad[15]+=1;assert dot(C[-1],bad)!=0
out={'rank_C_exact':len(piv),'nullity':16-len(piv),'null_vector_exact':list(map(str,v)),'epsilon_exact':str(eps),'witnesses_exact':[list(map(str,z)) for z in pm],'gradients':[float(dot(L,z)) for z in pm],'width_fraction_abs_baseline':float(abs(dot(L,pm[1])-dot(L,pm[0]))/abs(dot(L,p))),'all_exact_checks':True,'wrong_offset_mutant_rejected':True,'claim':'Fixing offset alone fails to identify finite-model target at strict baseline; exhibited width not sharp.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['null_vector_exact','epsilon_exact','witnesses_exact']}))
