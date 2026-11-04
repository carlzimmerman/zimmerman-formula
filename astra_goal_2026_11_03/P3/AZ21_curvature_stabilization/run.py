from pathlib import Path
import sympy as S
import subprocess,json,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
b,xi,M,V0,d,R=S.symbols('b xi M V0 d R',positive=True)
f=1-xi*b*b;V=V0/b**2;F=M**(d-2)*f
trace=2*d*V/((d-2)*F)
scalar=S.diff(F,b)*R/2-S.diff(V,b)
joint=S.factor(scalar.subs(R,trace))
P=(d-2)-2*(d-1)*xi*b*b
U=V*f**(-d/(d-2))
log_deriv=S.simplify(S.diff(S.log(U),b))
# Independent logarithmic derivative avoids assumptions about arbitrary powers.
expected_log=-2*P/((d-2)*b*f)
jordan_check=S.simplify(joint-2*V0*P/(b**3*(d-2)*f))
b2star=(d-2)/(2*(d-1)*xi)
fstar=S.simplify(f.subs(b*b,b2star))
xic=(d-2)/(4*(d-1))
benchmark=S.simplify(b2star.subs(xi,xic))
U4=V/f**2;K4=M*M*(1/f+S.Rational(3,2)*(S.diff(f,b)/f)**2)
b4=S.sqrt(1/(3*xi));u4star=S.simplify(U4.subs(b,b4));k4star=S.simplify(K4.subs(b,b4))
hessian=S.simplify(S.diff(U4,b,2).subs(b,b4))
mass2=S.simplify(hessian/k4star);H2=u4star/(3*M*M);ratio=S.simplify(mass2/H2)
fake_ratio=S.simplify(hessian/(M*M/f.subs(b,b4))/H2)
checks={'Jordan_equations_elimination':jordan_check==0,'Einstein_log_derivative_agrees':S.simplify(log_deriv-expected_log)==0,'stationary_polynomial':S.simplify(P.subs(b*b,b2star))==0,'positive_Planck_factor_identity':S.simplify(fstar-d/(2*(d-1)))==0,'conformal_benchmark_field_squared':benchmark==2,'four_dim_stationarity':S.simplify(S.diff(U4,b).subs(b,b4))==0,'canonical_kinetic_identity':S.simplify(k4star-S.Rational(3,2)*M*M*(1+3*xi))==0,'positive_hessian_identity':S.simplify(hessian-S.Rational(243,2)*V0*xi*xi)==0,'mass_Hubble_ratio':S.simplify(ratio-36*xi/(1+3*xi))==0,'MUTATE_fixed_flat_metric_no_stationary':S.simplify(scalar.subs(R,0)-2*V0/b**3)==0,'MUTATE_missing_kinetic_term_bites':S.simplify(fake_ratio-ratio-108*xi**2/(1+3*xi))==0}
runs={}
for name in ['Certificate','Mutate']:
 p=subprocess.run(['lean',str((D/(name+'.lean')).relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 log=p.stdout+p.stderr;(D/(name+'.log')).write_text(log);runs[name]={'exit':p.returncode,'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
checks.update(Lean_known_answers=runs['Certificate']['exit']==0,Lean_MUTATE=runs['Mutate']['exit']!=0 and 'false' in (D/'Mutate.log').read_text().lower(),no_sorry_axiom='sorryAx' not in (D/'Certificate.log').read_text())
checks={k:bool(v) for k,v in checks.items()};label='FAIL' if all(checks.values()) else 'NO VERDICT'
result={'label':label,'scope':'Vacuum stabilization exists but unit physical normalization is not selected','disclaimer':'κ = ½ FITTED; not theory closed','footings':{k:{'stabilization':'PASS' if all(checks.values()) else 'NO VERDICT','normalization_selection':label,'physical_kappa':'NOT EVALUABLE'} for k in ['canonical','alt']},'checks':checks,'symbolic':{'joint_scalar_equation':str(joint),'stationary_b_squared':str(b2star),'effective_Planck_factor':str(fstar),'conformal_benchmark_b_squared':str(benchmark),'Einstein_kinetic_at_vacuum_4d':str(k4star),'potential_Hessian_4d':str(hessian),'scalar_mass_squared_4d':str(mass2),'scalar_mass_over_H_squared':str(ratio),'MUTATE_without_mixing_ratio':str(fake_ratio),'unit_field_requires_xi':str((d-2)/(2*(d-1)))},'free_parameters':['xi nonminimal curvature coupling FITTED/unselected','V0 inverse-square potential scale FITTED/unselected','M canonical Einstein/scalar normalization','force-portal coupling not supplied'], 'limits':['Constant-field vacuum and scalar perturbation, not a sourced MOND solution','Conformal coefficient benchmark not enforced by the full action','Newton constant and operational a0 map absent; no kappa value inferred','No observational second prediction without fixing xi and source coupling'],'runs':runs,'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'inputs':{str((D/n).relative_to(ROOT)):hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']}}
(D/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(not all(checks.values()))
