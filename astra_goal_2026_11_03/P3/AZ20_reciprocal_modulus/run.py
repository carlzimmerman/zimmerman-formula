from pathlib import Path
import sympy as S
import json,hashlib,subprocess
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
B,y,eta,x=S.symbols('B y eta x',positive=True);q,C=S.symbols('q C',real=True);chi=S.symbols('chi',positive=True)
U=2*S.log(chi)-4*chi+chi**2+C
E=y*y+(C-1-2/(1+B*y)-2*S.log(1+B*y))/B**2
unreduced=(1-chi**2)*y*y+U/B**2
Eplus=E.subs(B,eta*S.exp(q));Eminus=E.subs(B,eta*S.exp(-q));pair=(Eplus+Eminus)/2
stationary=S.simplify(S.diff(pair,q).subs(q,0))
H=S.simplify(S.diff(pair,q,2).subs(q,0))
h=S.simplify((eta**2*H).subs(y,x/eta))
h0=S.limit(h,x,0,dir='+');high=S.limit(h+8*S.log(x),x,S.oo)
fixedchi=4*U.subs(chi,1/(1+x))
mutation=S.simplify((h-fixedchi).subs(x,1))
unequal=S.simplify(S.diff(Eplus/3+2*Eminus/3,q).subs(q,0))
mu=(1-(1+eta*S.exp(q)*y)**(-2)+1-(1+eta*S.exp(-q)*y)**(-2))/2
slope=S.simplify(S.diff(mu,y).subs(y,0))
vacuum_ratio=(C-3)/(8*S.pi*eta**2)
checks={'exact_auxiliary_elimination':S.simplify(unreduced.subs(chi,1/(1+B*y))-E)==0,'equal_point_energy':S.simplify(pair.subs(q,0)-E.subs(B,eta))==0,'exchange_stationarity':stationary==0,'vacuum_curvature':S.simplify(h0-4*(C-3))==0,'large_source_asymptotic':S.simplify(high-(4*C+4))==0,'MUTATE_fixed_auxiliary_discrepancy':mutation==S.Rational(1,2),'MUTATE_unequal_weights_break_stationarity':S.diff(unequal,C)!=0,'low_source_slope':S.simplify(slope-eta*(S.exp(q)+S.exp(-q)))==0,'common_scale_not_selected':S.diff(vacuum_ratio,C)!=0}
runs={}
for name in ['Certificate','Mutate']:
 p=subprocess.run(['lean',str((D/(name+'.lean')).relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 log=p.stdout+p.stderr;(D/(name+'.log')).write_text(log);runs[name]={'exit':p.returncode,'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
checks.update(Lean_known_answer=runs['Certificate']['exit']==0,Lean_MUTATE=runs['Mutate']['exit']!=0 and 'false' in (D/'Mutate.log').read_text().lower(),no_sorry_axiom='sorryAx' not in (D/'Certificate.log').read_text())
checks={k:bool(v) for k,v in checks.items()};label='FAIL' if all(checks.values()) else 'NO VERDICT'
result={'label':label,'scope':'Reciprocal-sector stabilization is locally possible but not universal and does not fix common physical normalization','disclaimer':'κ = ½ FITTED; not theory closed','footings':{f:{'mechanism':label,'physical_kappa':'NOT EVALUABLE'} for f in ['canonical','alt']},'checks':checks,'symbolic':{'h':str(h),'h_at_zero':str(h0),'limit_h_plus_8_log_x':str(high),'fixed_chi_MUTATE_error_at_x1':str(mutation),'unequal_weight_derivative':str(unequal),'mu_low_field_slope':str(slope),'vacuum_density_ratio':str(vacuum_ratio),'conditional_kappa_at_symmetric_point':'1/(2 eta); eta remains free','conclusion':'For every finite C, h(x) tends to negative infinity. Vacuum q=0 is stable only if C>3; symmetry is not a global source-stability principle.'},'free_parameters':['eta common normalization FITTED/unselected','C vacuum offset FITTED/unselected','positive q kinetic coefficient FITTED/unselected','two exchanged auxiliary sectors are a model hypothesis, not independently derived'], 'limits':['Constant local response patches','Large-source limit is of this unrestricted action; an independently derived cutoff could change applicability','Vacuum consistency calculation conditional on same-sector density identification','No full covariant completion, independent second prediction or physical kappa certificate'], 'runs':runs,'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'inputs':{str((D/n).relative_to(ROOT)):hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']}}
(D/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(not all(checks.values()))
