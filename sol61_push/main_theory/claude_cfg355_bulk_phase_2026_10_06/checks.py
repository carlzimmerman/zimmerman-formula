import argparse, json
import sympy as s
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--forget-relative-bulk',action='store_true');args=p.parse_args()
delta=s.Rational(1,5); bulk=s.Matrix([2,0,0]); H=s.Rational(1,10);mu=s.Integer(1);r0=s.Integer(1)
vel=[]
for j in range(3):
 for sign in [-1,1]:
  v=s.zeros(3,1);v[j]=sign*delta;vel.append(v)
shift=[v+bulk for v in vel]
def mean(vs):return sum(vs,s.zeros(3,1))/len(vs)
def cov(vs):
 m=mean(vs)
 return sum([(v-m)*(v-m).T for v in vs],s.zeros(3,3))/len(vs)
def central(vs,indices):
 m=mean(vs)
 return s.simplify(sum(s.prod((v-m)[j] for j in indices) for v in vs)/len(vs))
rs=(mu/H**2)**s.Rational(1,3);Us=-s.Rational(3,2)*(mu*H)**s.Rational(2,3)
U0=-mu/r0-H**2*r0**2/2
def energy(v):return s.simplify(v.dot(v)/2+U0)
actual_shift=vel if args.forget_relative_bulk else shift
es=[energy(v) for v in actual_shift]
Ls=[s.simplify(r0**2*(v[1]**2+v[2]**2)) for v in actual_shift]
checks=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
ck('covariance_translation_exact',cov(vel)==cov(shift)==s.eye(3)/75)
ck('rank_three_both',cov(vel).det()>0 and cov(shift).rank()==3)
ck('central_third_fourth_translation',all(central(vel,ix)==central(shift,ix) for ix in [(0,0,0),(0,1,2),(0,0,0,0),(0,0,1,1)]))
ck('host_relative_mean_changed',mean(shift)-mean(vel)==bulk)
ck('inside_outer_barrier',rs>r0)
ck('all_unshifted_confined',all(energy(v)<Us for v in vel))
ck('all_shifted_outward',all(v[0]>0 for v in actual_shift))
ck('global_outward_effective_potential_bound',all(E>Us+L/(2*r0**2) for E,L in zip(es,Ls)))
ck('least_shifted_energy',min(es)==s.Rational(123,200))
out={'checks':checks,'summary':{'passed':sum(x['passed'] for x in checks),'total':len(checks)},'Us':float(Us),'rs':float(rs),'unshifted_energy':str(energy(vel[0])),'shifted_energies':[str(E) for E in es],'max_L_squared':str(max(Ls)),'control':args.forget_relative_bulk,'scope':'Exact six-stream test-host witness; no finite self-gravitating halo or GR initial-data equality'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']))
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
