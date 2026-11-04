from pathlib import Path
import sympy as S
import subprocess,json,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
b,xi,M,Q,s,g,chi,d,R=S.symbols('b xi M Q s g chi d R',positive=True);C=S.symbols('C',real=True)
f=1-xi*b*b;F=M**(d-2)*f;V=Q*f/b**2
trace=2*d*V/((d-2)*F);scalar=S.diff(F,b)*R/2-S.diff(V,b)
joint=S.factor(scalar.subs(R,trace));P=(d-2)-d*xi*b*b
bstar2=(d-2)/(d*xi);einstein_log=S.diff(S.log(Q/b**2),b)-S.Rational(2,1)/(d-2)*S.diff(f,b)/f
U4=Q/(b*b*f);K4=M*M*(1/f+S.Rational(3,2)*(S.diff(f,b)/f)**2);root=S.sqrt(1/(2*xi))
curv=S.simplify(S.diff(U4,b,2).subs(b,root));ks=S.simplify(K4.subs(b,root));us=S.simplify(U4.subs(b,root))
ratio=S.simplify((curv/ks)/(us/(3*M*M)))
alpha2=S.simplify((M*M*(S.diff(f,b)/(2*f))**2/K4).subs(b,root))
calibration=S.factor(1+2*alpha2)
U=2*S.log(chi)-4*chi+chi*chi+C
E=M*M*f*((1-chi*chi)*g*g+s*s*U/b**2)
chi_root=s/(s+b*g)
chi_check=S.simplify(S.diff(E,chi).subs(chi,chi_root))
Gtensor=1/(8*S.pi*M*M*f);rho=M*M*f*s*s*(C-3)/b**2;a0fixed=s/(2*b)
kap2=S.simplify(a0fixed**2/(Gtensor*rho))
checks={'Jordan_common_action_identity':S.simplify(joint-2*Q*P/(b**3*(d-2)))==0,'Einstein_stationarity_identity':S.simplify(einstein_log+2*P/((d-2)*b*f))==0,'stationary_root':S.simplify(P.subs(b*b,bstar2))==0,'effective_Planck_factor':S.simplify(f.subs(b*b,bstar2)-2/d)==0,'static_chi_variation':chi_check==0,'static_flux_normalization':S.simplify(1/(2*M*M*f)-4*S.pi*Gtensor)==0,'dictionary_invariant':S.simplify(kap2-2*S.pi/(C-3))==0,'positive_kinetic_identity':S.simplify(ks-2*M*M*(1+6*xi))==0,'positive_curvature_identity':S.simplify(curv-64*Q*xi*xi)==0,'canonical_mass_ratio':S.simplify(ratio-24*xi/(1+6*xi))==0,'scalar_charge':S.simplify(alpha2-xi/(1+6*xi))==0,'MUTATE_old_vacuum_root':S.simplify(P.subs(d,4).subs(b*b,1/(3*xi)))==S.Rational(2,3),'MUTATE_zero_charge_fails':S.simplify(alpha2)!=0,'unselected_vacuum_offset':S.diff(kap2,C)!=0}
runs={}
for name in ['Certificate','Mutate']:
 p=subprocess.run(['lean',str((D/(name+'.lean')).relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 log=p.stdout+p.stderr;(D/(name+'.log')).write_text(log);runs[name]={'exit':p.returncode,'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
checks.update(Lean_controls=runs['Certificate']['exit']==0,Lean_MUTATE=runs['Mutate']['exit']!=0 and 'false' in (D/'Mutate.log').read_text().lower(),no_sorry='sorryAx' not in (D/'Certificate.log').read_text())
checks={k:bool(v) for k,v in checks.items()};label='FAIL' if all(checks.values()) else 'NO VERDICT'
r={'label':label,'disclaimer':'κ = ½ FITTED; not theory closed','scope':'Common-action matching does not select invariant vacuum/response ratio','footings':{k:{'stabilization':'PASS' if all(checks.values()) else 'NO VERDICT','selection':label,'full_physical_kappa':'NOT EVALUABLE'} for k in ['canonical','alt']},'checks':checks,'symbolic':{'b_squared':str(bstar2),'potential_4d_at_vacuum':str(us),'kinetic_4d_at_vacuum':str(ks),'potential_curvature':str(curv),'mass_squared_over_H_squared':str(ratio),'scalar_charge_squared':str(alpha2),'unscreened_scalar_tensor_G_ratio':str(calibration),'frozen_b_tensor_kappa_squared':str(kap2),'derivative_kappa_squared_wrt_C':str(S.diff(kap2,C))},'free_parameters':['C vacuum offset FITTED/unselected','xi curvature coupling FITTED/unselected','s response scale symbolic','preferred timelike response structure posited'], 'limits':['Fixed-b static aligned-vector response is conditional, not a solved full source','Scalar-tensor weak-source calibration omits possible vector dynamics and nonlinear screening','Need solve b,u,chi and metric with same boundary state for a physical MOND prediction','No stability claim for all preferred-frame perturbations'], 'runs':runs,'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'inputs':{str((D/n).relative_to(ROOT)):hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']}}
(D/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(not all(checks.values()))
