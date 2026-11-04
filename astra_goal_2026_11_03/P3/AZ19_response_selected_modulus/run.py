from pathlib import Path
import sympy as S
import json,hashlib,subprocess
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
b,g,s,x=S.symbols('b g s chi',positive=True);C=S.symbols('C',real=True)
U=2*S.log(x)-4*x+x*x+C
E=(1-x*x)*g*g+s*s*U/b**2
Eb=S.diff(E,b);Ex=S.diff(E,x)
branch=s/(s+b*g)
reduce=lambda e:S.simplify(e.subs(x,branch))
Eeff=reduce(E)
chi_res=reduce(Ex)
chain_res=S.simplify(S.diff(Eeff,b)-reduce(Eb))
rootC=-2*S.log(x)+4*x-x*x
stat={C:rootC,g**2:s**2*(1-x)**2/(b*b*x*x)}
Exx=S.factor(S.diff(E,x,2).subs(stat))
Ebb=S.factor(S.diff(E,b,2).subs(stat))
Ebx=S.factor(S.diff(E,b,x).subs(stat))
curvature=S.factor(Ebb-Ebx**2/Exx)
expected=4*s*s*(1-x)**3/b**4
Uprime=S.factor(S.diff(U,x))
# Strictly increasing U except at chi=1; physical branch uses 0<chi<1.
checks={'chi_equation_known_branch':chi_res==0,'reduced_derivative_chain_rule':chain_res==0,'b_stationarity_exact':S.simplify(Eb+2*s*s*U/b**3)==0,'potential_monotonicity_identity':S.simplify(Uprime-2*(1-x)**2/x)==0,'reduced_curvature_identity':S.simplify(curvature-expected)==0,'MUTATE_omitted_b_variation_detected':S.simplify(S.diff(Eb,C))==-2*s*s/b**3,'source_dependent_branch_identity':S.simplify((s*(1-x)/(x*g))*g-s*(1-x)/x)==0}
runs={}
for name in ['Certificate','Mutate']:
 p=subprocess.run(['lean',str((D/(name+'.lean')).relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 log=p.stdout+p.stderr;(D/(name+'.log')).write_text(log);runs[name]={'exit':p.returncode,'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
checks['Lean_known_and_source_controls']=runs['Certificate']['exit']==0
checks['Lean_MUTATE_rejected']=runs['Mutate']['exit']!=0 and 'false' in (D/'Mutate.log').read_text().lower()
checks['no_sorry_axiom']='sorryAx' not in (D/'Certificate.log').read_text()
checks={k:bool(v) for k,v in checks.items()};label='FAIL' if all(checks.values()) else 'NO VERDICT'
paths=[D/'CRITERIA.md',D/'run.py',D/'Certificate.lean',D/'Mutate.lean']
result={'label':label,'disclaimer':'κ = ½ FITTED; not theory closed','scope':'Response-driven modulus fails universal-normalization/nonlinear-force selection; no physical kappa derived','footings':{k:{'mechanism':label,'physical_kappa':'NOT EVALUABLE'} for k in ['canonical','alt']},'checks':checks,'symbolic':{'E_b':str(Eb),'E_chi':str(Ex),'U_prime':str(Uprime),'on_branch_E_chichi':str(Exx),'on_branch_reduced_b_curvature':str(curvature),'b_stationary':'s*(1-chi_root)/(chi_root*g)','mu_stationary':'1-chi_root**2; independent of g','physical_root_condition':'C>3; C=3 has chi_root=1, incompatible with g>0 and finite b>0'},'runs':runs,'free_parameters':['C vacuum offset FITTED/unselected','Zb positive kinetic coefficient FITTED/unselected','s=c sqrt(G rho), symbolic; no numerical density'],'limits':['Constant stationary local patches only','No no-go for spatial gradients, time-dependent fields or additional dynamics','Schur curvature is not full covariant stability','Lean certifies branch witnesses, not the Sympy variational derivation or physical normalization'],'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(D/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(not all(checks.values()))
