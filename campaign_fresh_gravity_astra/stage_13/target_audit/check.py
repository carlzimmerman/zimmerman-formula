from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import numpy as np,json,argparse
p=argparse.ArgumentParser();p.add_argument('--matrix',required=True);p.add_argument('--key',required=True);p.add_argument('--output',required=True);args=p.parse_args()
old=np.load('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz',allow_pickle=False)
new=np.load(args.matrix,allow_pickle=False);uf=np.asarray(new[args.key]);assert uf.shape in [(15,15),(15,16)]
if uf.shape[1]==16:assert np.array_equal(uf[:,15],np.ones(15));uf=uf[:,:15]
assert np.array_equal(uf[:12],old['H'][:,:15])
U=[[F(float(x)) for x in row] for row in uf];L=[F(float(x)) for x in old['L'][:15]];baseline=[F(float(x)) for x in old['baseline'][:15]]
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
A,piv=rr([list(col)+[v] for col,v in zip(zip(*U),L)]);assert piv==list(range(15));r=[row[-1] for row in A];assert [dot(r,col) for col in zip(*U)]==L
rank=lambda rows:len(rr(rows)[1]);subsets=[]
for k in [1,2,3]:
 for inds in combinations(range(12,15),k):
  rows=U[:12]+[U[i] for i in inds];R,piv=rr(rows);rank0=len(piv);rank1=rank(rows+[L]);entry={'new_indices':[i-12 for i in inds],'rank':rank0,'rank_with_target':rank1,'identified':rank0==rank1}
  if rank0!=rank1:
   for j in range(15):
    if j in piv:continue
    v=[F(0)]*15;v[j]=1
    for i,c in enumerate(piv):v[c]=-R[i][j]
    if dot(L,v):break
   assert all(dot(row,v)==0 for row in rows)
   margins=[baseline[i]-(baseline[i+1] if i<14 else 0) for i in range(15)]
   dv=[v[i]-(v[i+1] if i<14 else 0) for i in range(15)]
   assert min(margins)>0;eps=min(m/abs(d) for m,d in zip(margins,dv) if d)/2
   for sign in [-1,1]:
    z=[x+sign*eps*y for x,y in zip(baseline,v)];assert all(dot(row,z)==dot(row,baseline) for row in rows);assert min([z[i]-(z[i+1] if i<14 else 0) for i in range(15)])>0
   entry.update(null_direction_exact=list(map(str,v)),step_exact=str(eps),target_change_exact=str(dot(L,v)),strict_feasible_both_signs=True)
  subsets.append(entry)
l1=sum(map(abs,r));offset=sum(r);ey=F(1,10**9);err=[ey*(1 if x>=0 else -1) for x in r];assert dot(r,err)==ey*l1
assert dot(r,[ey]*15)==ey*offset
rfloat=np.array(list(map(float,r)));rnp=np.linalg.solve(uf.T,np.array(list(map(float,L))))
assert np.allclose(rfloat,rnp,rtol=1e-8,atol=1e-10)
# Negative control: release the assumed offset, keeping all fifteen bins fixed.
R,piv=rr([row+[F(-1)] for row in U]);assert piv==list(range(15));v=[row[-1] for row in R]
assert all(dot(row,v)==-1 for row in U) and dot(L,v)==-offset
margins=[baseline[i]-(baseline[i+1] if i<14 else 0) for i in range(15)]
dv=[v[i]-(v[i+1] if i<14 else 0) for i in range(15)]
epsb=min(m/abs(d) for m,d in zip(margins,dv) if d)/2
for sign in [-1,1]:
 z=[x+sign*epsb*y for x,y in zip(baseline,v)];b=sign*epsb
 assert all(dot(row,z)+b==dot(row,baseline) for row in U)
 assert min([z[i]-(z[i+1] if i<14 else 0) for i in range(15)])>0
assert offset!=0
baseg=dot(L,baseline)
output={'relaxed_offset_control':{'pressure_direction_exact':list(map(str,v)),'offset_direction':1,'step_exact':str(epsb),'target_direction_exact':str(dot(L,v)),'strict_positive_two_sided_witness':True,'all_fifteen_bins_unchanged_exact':True,'scope':'Negative control relaxing fixed-offset premise; no actual offset inferred'},'exact_dual_weights':list(map(str,r)),'dual_weights_float':list(map(float,r)),'target_identity_exact':True,'all_inner_rows_bitwise_match':True,'subsets':subsets,'l1_gain_exact':str(l1),'l1_gain':float(l1),'offset_gain_exact':str(offset),'offset_gain':float(offset),'raw_matrix_condition_2':float(np.linalg.cond(uf)),'epsilon_y':str(ey),'worst_case_error_exact':str(ey*l1),'worst_case_error':float(ey*l1),'common_offset_error':float(ey*offset),'synthetic_baseline_gradient':float(baseg),'relative_worst_case_to_baseline':float(ey*l1/abs(baseg)),'numeric_weights_max_abs_difference':float(np.max(abs(rfloat-rnp))),'non_claims':['epsilon is a declared algebraic control, not measured noise','No calibrated response or covariance','No actual data fit','No MOND mass/source inference']}
Path(args.output).write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ['relaxed_offset_control','subsets','exact_dual_weights','dual_weights_float','l1_gain_exact','offset_gain_exact','worst_case_error_exact']}))
