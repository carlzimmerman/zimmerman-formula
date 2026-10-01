from fractions import Fraction as F
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import linprog
OUT=Path(sys.argv[1]); OUT.mkdir(exist_ok=True)
SRC=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz')
x=np.load(SRC); scale=F(float(1e-5))
def dot(a,b): return sum((u*v for u,v in zip(a,b)),F(0))
def solve(a,b):
 m=[list(row)+[rhs] for row,rhs in zip(a,b)]; n=len(b)
 for i in range(n):
  j=next(j for j in range(i,n) if m[j][i]);m[i],m[j]=m[j],m[i]
  p=m[i][i];m[i]=[z/p for z in m[i]]
  for j in range(n):
   if i!=j:
    p=m[j][i]
    if p:m[j]=[z-p*w for z,w in zip(m[j],m[i])]
 return [row[-1] for row in m]
def trans(a):return list(map(list,zip(*a)))
def arr(a):return np.array(a,dtype=float)
def serial(a):return [str(z) for z in a]
def cert(name,c,eq,rhs,ineq,bound):
 n=len(c)
 r=linprog(arr(c),A_ub=arr(ineq) if ineq else None,b_ub=arr(bound) if ineq else None,A_eq=arr(eq) if eq else None,b_eq=arr(rhs) if eq else None,bounds=[(None,None)]*n,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
 assert r.success,(name,r.message)
 active=[i for i,row in enumerate(ineq) if abs(float(dot(row,list(map(F,r.x))))-float(bound[i]))<1e-7]
 rows=list(eq); vals=list(rhs); selected=[]
 for j in active:
  test=rows+[ineq[j]]
  if np.linalg.matrix_rank(arr(test),tol=1e-10)>len(rows):rows=test;vals.append(bound[j]);selected.append(j)
  if len(rows)==n:break
 assert len(rows)==n,(name,'not a full vertex',active)
 u=solve(rows,vals); lam=solve(trans(rows),c); y=lam[:len(eq)]; z=[F(0)]*len(ineq)
 for j,v in zip(selected,lam[len(eq):]):z[j]=v
 slack=[b-dot(row,u) for row,b in zip(ineq,bound)]
 stat=[dot(col,y)+dot(col2,z)-ci for col,col2,ci in zip(trans(eq) if eq else [[]]*n,trans(ineq) if ineq else [[]]*n,c)]
 checks={'primal_equalities_exact':all(dot(row,u)==b for row,b in zip(eq,rhs)),'primal_inequalities_exact':all(s>=0 for s in slack),'dual_nonpositive_exact':all(v<=0 for v in z),'dual_stationarity_exact':all(v==0 for v in stat),'complementarity_exact':all(s*v==0 for s,v in zip(slack,z)),'zero_gap_exact':dot(c,u)==dot(y,rhs)+dot(z,bound)}
 assert all(checks.values()),(name,checks)
 # Direct negative control: changing one cost coefficient cannot preserve stationarity.
 bad=c.copy();bad[0]+=F(1,1000)
 checks['damaged_cost_rejected']=bad[0]!=dot(trans(eq)[0],y)+dot(trans(ineq)[0],z) if eq else bad[0]!=dot(trans(ineq)[0],z)
 result={'objective_exact':str(dot(c,u)),'objective_float':float(dot(c,u)),'u_exact':serial(u),'u_float':list(map(float,u)),'equality_dual_exact':serial(y),'inequality_dual_exact':serial(z),'selected_active_inequalities':selected,'all_tight_inequalities':[i for i,s in enumerate(slack) if not s],'checks':checks,'float_candidate_objective':float(r.fun),'float_candidate_equality_residual_max':float(np.max(np.abs(arr(eq)@r.x-arr(rhs)))) if eq else 0,'float_candidate_min_slack':float(np.min(arr(bound)-arr(ineq)@r.x)) if ineq else 0,'active_matrix_condition_2':float(np.linalg.cond(arr(rows)))}
 return result,u

# Certificate helpers above copied unchanged from the pinned FGF-021 code.
H=[[F(float(v)) for v in row] for row in x['H']]; L=[F(float(v)) for v in x['L']]
E=[[sum(row[:j+1],F(0)) for j in range(15)]+[row[15]] for row in H]
c=[sum(L[:j+1],F(0)) for j in range(15)]+[L[15]]
baseline=[F(float(v))/scale for v in x['baseline']];d=[dot(row,baseline) for row in H]
qbase=[baseline[i]-(baseline[i+1] if i<14 else F(0)) for i in range(15)]+[baseline[15]]
assert all(v>0 for v in qbase[:15]) and qbase[15]==0 and all(dot(row,qbase)==di for row,di in zip(E,d))
A=[[-F(i==j) for j in range(16)] for i in range(15)];zeros=[F(0)]*15
brow=[F(0)]*15+[F(1)]
old=json.loads(Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-021/fgf021_run_001/numeric_001/results.json').read_text())
thresholds={}; unique=[]
for nm in ['min','max']:
 rec=old[nm+'_certificate'];u=list(map(F,rec['u_exact']));z=list(map(F,rec['inequality_dual_exact']));active=[i for i,v in enumerate(z) if v<0]
 assert len(active)==4
 rebuilt=solve(E+[A[i] for i in active],d+[F(0)]*4);assert rebuilt==u
 thresholds[nm]=abs(scale*u[-1]);unique.append({'side':nm,'nonzero_negative_dual_indices':active,'exact_unique_vertex_reconstruction':True,'threshold_beta_exact':str(thresholds[nm]),'threshold_beta_y':float(thresholds[nm]),'old_witness_fails_half_threshold':abs(scale*u[-1])>thresholds[nm]/2})
betas=sorted(set([F(0),F(1,1000000),thresholds['min']/2,thresholds['min'],thresholds['max']/2,thresholds['max']]))
records=[]
for beta in betas:
 eq=E+[brow] if beta==0 else E
 rhs=d+[F(0)] if beta==0 else d
 aq=A if beta==0 else A+[brow,[-v for v in brow]]
 bs=zeros if beta==0 else zeros+[beta/scale,beta/scale]
 rec={'beta_exact':str(beta),'beta_y':float(beta),'beta_scaled_exact':str(beta/scale),'definitions':'beta=0: equalities E u=d followed by b=0, inequalities -q_i<=0; beta>0: equalities E u=d, inequalities -q_i<=0 then b<=beta/s then -b<=beta/s','baseline_feasible_exact':all(dot(row,qbase)==v for row,v in zip(eq,rhs)) and all(dot(row,qbase)<=v for row,v in zip(aq,bs))}
 for name,cc in [('min',c),('max',[-v for v in c])]:
  certificate,u=cert(name+'_'+str(float(beta)),cc,eq,rhs,aq,bs)
  pressure=[sum(u[i:15],F(0)) for i in range(15)]+[u[15]]
  assert all(dot(row,pressure)==v for row,v in zip(H,d))
  gradient=scale*dot(c,u)
  certificate['gradient_exact']=str(gradient);certificate['gradient']=float(gradient)
  certificate['offset_y_exact']=str(scale*u[-1]);certificate['offset_y']=float(scale*u[-1]);certificate['direct_H_pressure_exact']=True
  rec[name]=certificate
 rec['width_fraction_baseline']=float((F(rec['max']['gradient_exact'])-F(rec['min']['gradient_exact']))/abs(scale*dot(L,baseline)))
 records.append(rec)
assert all(F(a['min']['gradient_exact'])>=F(b['min']['gradient_exact']) and F(a['max']['gradient_exact'])<=F(b['max']['gradient_exact']) for a,b in zip(records,records[1:]))
assert F(records[0]['min']['gradient_exact'])<F(records[0]['max']['gradient_exact'])
for rec in records:
 for name in ['min','max']:
  if F(rec['beta_exact'])>=thresholds[name]:assert F(rec[name]['gradient_exact'])==F(old['gradient_interval'][name+'_exact'])
result={'selected_beta_set_only':True,'not_a_complete_breakpoint_curve':True,'scale_exact':str(scale),'baseline_gradient_exact':str(scale*dot(L,baseline)),'coefficient_domain':'Stored binary64 rationalized exactly; selected beta values exact fractions','beta_range_y':[0,float(max(betas))],'records':records,'unrestricted_unique_optimum_thresholds':unique,'checks':{'baseline_strictly_positive_decreasing_exact':True,'zero_offset_nonzero_interval_exact':True,'nested_intervals_exact':True,'threshold_recovery_exact':True,'old_witness_rejected_at_half_thresholds':True},'structural_proof':'For all beta>=0 minimum is nonincreasing convex, maximum nondecreasing concave, feasible baseline always exists; selected certificates do not enumerate all kinks.'}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps([{'beta':v['beta_y'],'min':v['min']['gradient'],'max':v['max']['gradient'],'width_fraction':v['width_fraction_baseline']} for v in records]))
