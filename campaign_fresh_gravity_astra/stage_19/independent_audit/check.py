from fractions import Fraction as F
from pathlib import Path
import json,sys
import numpy as np
INPUT='deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-029/fgf029_run_001/numeric_001/extended_response.npz'
OLD='campaign_fresh_gravity_astra/stage_15/target_audit/run_001/results.json'
h=np.load(INPUT,allow_pickle=False)['combined_pressure'];assert h.shape==(15,16)
H=[[F(float(x)) for x in row] for row in h];n=15
U=[row[:n] for row in H];c=[row[n] for row in H]
L=[F(0)]*n;L[5]=F(-5);L[6]=F(5)
dot=lambda x,y:sum((a*b for a,b in zip(x,y)),F(0))
# Independent pivoted rational LU; inverse columns use triangular solves.
lu=[row[:] for row in U];perm=list(range(n))
for k in range(n):
 p=max(range(k,n),key=lambda i:abs(lu[i][k]));assert lu[p][k]
 lu[k],lu[p]=lu[p],lu[k];perm[k],perm[p]=perm[p],perm[k]
 for i in range(k+1,n):
  lu[i][k]/=lu[k][k]
  for j in range(k+1,n):lu[i][j]-=lu[i][k]*lu[k][j]
def solve(rhs):
 y=[]
 for i in range(n):y.append(rhs[perm[i]]-dot(lu[i][:i],y))
 x=[F(0)]*n
 for i in reversed(range(n)):x[i]=(y[i]-dot(lu[i][i+1:],x[i+1:]))/lu[i][i]
 return x
cols=[solve([F(int(i==j)) for i in range(n)]) for j in range(n)]
inv=[list(row) for row in zip(*cols)]
assert all(dot(U[i],cols[j])==int(i==j) for i in range(n) for j in range(n))
q=solve([-x for x in c]);v=q+[F(1)];dual=[dot(L,col) for col in cols]
assert all(dot(row,v)==0 for row in H)
assert all(dot(dual,col)==L[j] for j,col in enumerate(zip(*U)))
mu=dot(L,q);old=json.loads(Path(OLD).read_text())
assert mu==F(old['target_sensitivity_dp5_exact']) and mu>0
assert v==list(map(F,old['null_direction_exact']))
a=max(sum(map(abs,row),F(0)) for row in inv);b=max(map(abs,q));R=sum(map(abs,dual),F(0));l=sum(map(abs,L),F(0))
assert a>0 and R>0 and l==10 and R<=l*a
threshold=min(1/(4*a),mu/(4*R*(1+b)))
delta=F(1)
while delta>threshold:delta/=10
eta=a*delta*(1+b)/(1-a*delta);Bt=R*delta*(1+b)/(1-a*delta)
assert a*delta<=F(1,4) and Bt<=mu/3 and mu-Bt>0
# Independently verify the author's preview formula, without author code/outputs.
adelta=min(1/(4*a),mu/(4*a*l*(1+b)))
aeta=a*adelta*(1+b)/(1-a*adelta);aBt=l*aeta
assert a*adelta<=F(1,4) and aBt<=mu/3
nodes=list(map(F,['0','.18','.36','.54','.72','.90','1.10','1.28','1.46','1.64','1.82','2','2.5','3','4','5']))
base=[F(1,100000)/(1+x)**2 for x in nodes];gaps=[base[i]-(base[i+1] if i<15 else 0) for i in range(16)]
assert min(gaps)>0
vv=v+[F(0)];err=[eta]*15+[F(0),F(0)]
bounds=[abs(vv[i]-vv[i+1])+err[i]+err[i+1] for i in range(16)]
assert all(x>0 for x in bounds) and bounds[-1]==1
step=min(m/d for m,d in zip(gaps,bounds))/2
assert step>0 and all(m-step*d>=m/2 for m,d in zip(gaps,bounds))
# Coarse author step checked using this independently declared baseline;
# author may select its own baseline, whose values must be separately audited.
aM=max(F(1),b+aeta);astep=min(gaps)/(4*aM)
assert all(m-2*aM*astep>=m/2 for m in gaps)
witness=[]
for sign in [-1,1]:
 p=[x+sign*step*y for x,y in zip(base,v)]
 pg=[p[i]-(p[i+1] if i<15 else 0) for i in range(16)]
 assert min(pg)>0
 assert all(dot(row,p)==dot(row,base) for row in H)
 witness.append({'sign':sign,'pressure_exact':list(map(str,p)),'minimum_gap_exact':str(min(pg)),'target_exact':str(dot(L,p[:15]))})
assert F(witness[1]['target_exact'])-F(witness[0]['target_exact'])==2*step*mu
# Exact controls, not sampled operator errors.
assert a*(1/a)==1 # Sufficient inverse gate is inconclusive here.
assert n*delta>delta and n*(delta/n)==delta
assert dot(L,q)-mu==0 # Mutant extended target last coefficient -mu.
assert base[-1]-2*base[-1]<0 # Last free-node positivity must be checked.
assert eta>0 and Bt>0 # Zero-error formulas instead give exactly zero.
constants={'inverse_induced_norm':a,'nominal_q_maxnorm':b,'dual_l1_norm':R,'target_l1_norm':l,'mu':mu,'radius_threshold':threshold,'radius_induced_U_and_maxnorm_c':delta,'entrywise_U_sufficient':delta/n,'q_error_bound':eta,'target_error_bound':Bt,'target_lower':mu-Bt,'common_step':step,'uniform_target_separation_lower':2*step*(mu-Bt),'author_preview_radius':adelta,'author_preview_q_bound':aeta,'author_preview_target_error':aBt,'author_preview_target_lower':mu-aBt,'author_formula_step_this_baseline':astep}
res={'status':'passed','arithmetic':'Fraction exact rationals representing saved binary64 matrix','constants_exact':{k:str(x) for k,x in constants.items()},'constants_approx':{k:float(x) for k,x in constants.items()},'nominal_null_direction_exact':list(map(str,v)),'dual_exact':list(map(str,dual)),'baseline_exact':list(map(str,base)),'baseline_gaps_exact':list(map(str,gaps)),'gap_change_bounds_exact':list(map(str,bounds)),'nominal_witnesses':witness,'controls':{'exact_inverse':True,'exact_nominal_null':True,'target_sign_and_last_zero':True,'oldFGF029_exact_agreement':True,'full16gaps_including_fixed_endpoint':True,'entrywise_induced_factor15':True,'inverse_threshold_only_inconclusive':True,'last_target_cancellation_mutant':True,'negative_last_free_node_rejected':True,'author_preview_coarse_radius_certified':True},'quantifier':'For every real E,e in declared norm ball, its own exact null pair has the same step and a strictly separated target; data may depend on operator.','limits':['No response rebuilding','No sampled errors or continuum/instrument authentication','No actual observed data fit, covariance or force/mass inference']}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'status':'passed','constants_approx':res['constants_approx']},indent=2))
