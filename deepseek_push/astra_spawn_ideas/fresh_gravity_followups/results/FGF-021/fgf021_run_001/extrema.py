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
H=[[F(float(v)) for v in row] for row in x['H']]; L=[F(float(v)) for v in x['L']]
E=[[sum(row[:j+1],F(0)) for j in range(15)]+[row[15]] for row in H]
c=[sum(L[:j+1],F(0)) for j in range(15)]+[L[15]]
baseline=[F(float(v))/scale for v in x['baseline']];d=[dot(row,baseline) for row in H]
A=[[-F(i==j) for j in range(16)] for i in range(15)];zeros=[F(0)]*15
mn,u0=cert('min',c,E,d,A,zeros); mx,u1=cert('max',[-v for v in c],E,d,A,zeros)
glo=scale*dot(c,u0);ghi=scale*dot(c,u1);gbase=scale*dot(L,baseline)
# Exact fixture simplex x+y=1, x,y>=0.
fixture=[]
for sign in [1,-1]:
 rec,_=cert('simplex',[F(sign),F(0)],[[F(1),F(1)]],[F(1)],[[-F(1),F(0)],[F(0),-F(1)]],[F(0),F(0)]);fixture.append(rec)
assert fixture[0]['objective_exact']=='0' and fixture[1]['objective_exact']=='-1'
# Frozen nuisances exactly recover the inherited baseline, using H not E.
inner=[row[:12] for row in H]; frozen=[b-dot(row[12:],baseline[12:]) for row,b in zip(H,d)]
sol=solve(inner,frozen);assert sol==baseline[:12]
# Exact amplitude scaling certificates inherit unchanged dual multipliers.
scaling=all(dot(row,[10*v for v in u0])==10*b for row,b in zip(E,d)) and scale*dot(c,[10*v for v in u0])==10*glo
# Prior witness amplitudes have rounding errors; bracket gradient exactly anyway.
oldg=[dot(L,[F(float(v)) for v in x[key]]) for key in ['pressure_plus','pressure_minus']]
assert all(glo<v<ghi for v in oldg)
obs=[F(float(v))/scale for v in x['observed_annular_y']]
ineq=[row+[-F(1)] for row in E]+[[-v for v in row]+[-F(1)] for row in E]
bound=obs+[-v for v in obs]
ineq += [[-F(i==j) for j in range(17)] for i in list(range(15))+[16]];bound += [F(0)]*16
actual,uobs=cert('actual_minimax',[F(0)]*16+[F(1)],[],[],ineq,bound)
resid=scale*uobs[-1]
assert resid>=0
# LP witnesses restored to nodal pressure, without mistaking offset for node at 5.
def physical(u):return [float(scale*sum(u[i:15],F(0))) for i in range(15)]+[0.0]
res={'arithmetic':'Binary64 stored coefficients treated as exact binary rationals; Fraction certification','s':str(scale),'gradient_interval':{'min':float(glo),'max':float(ghi),'baseline':float(gbase),'width_fraction_abs_baseline':float((ghi-glo)/abs(gbase)),'prior_exhibited_width_fraction':float(abs(oldg[0]-oldg[1])/abs(gbase)),'min_exact':str(glo),'max_exact':str(ghi)},'min_certificate':mn,'max_certificate':mx,'minimum_pressure_nodes':physical(u0),'maximum_pressure_nodes':physical(u1),'minimum_offset_y':float(scale*u0[15]),'maximum_offset_y':float(scale*u1[15]),'fixture_certificates':fixture,'frozen_nuisance_exact_recovery':True,'exact_tenfold_scaling':bool(scaling),'prior_witness_gradients_strictly_inside':True,'actual_map':{'minimum_uniform_residual_y':float(resid),'minimum_uniform_residual_y_exact':str(resid),'certificate':actual,'pressure_nodes':physical(uobs),'offset_y':float(scale*uobs[15]),'residuals_y':[float(scale*(dot(row,uobs[:16])-v)) for row,v in zip(E,obs)],'not_a_confidence_or_noise_estimate':True},'strict_family':'Endpoints are limits by mixing either optimum with the strict baseline; gradients between endpoints achievable by convex mixing.'}
(OUT/'results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'gradient_interval':res['gradient_interval'],'minimum_uniform_residual_y':float(resid),'all_exact_certificates_pass':True}))
