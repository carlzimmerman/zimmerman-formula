import hashlib,json,platform,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
inputs=[HERE/n for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']]+[HERE.parent/'AZ28_separable_fold_repair/RESULT.md',HERE.parent/'AZ28_separable_fold_repair/CRITERIA.md']
hashes=lambda:{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
before=hashes(); checks={}
def zero(k,e):checks[k]=s.simplify(e)==0
a,N,B,M,R,e,Lambda,H,lam=s.symbols('a N B M R ell_squared Lambda H lambda',positive=True)
v,w,hd,r=s.symbols('adot addot Hdot rho_over_B',real=True)
S=3*lam-1; V=R-e*R**2-2*Lambda; D=s.diff(V,R)
L=B*N*a**3/2*(-3*S*v*v/(N*N*a*a)+V.subs(R,6/a**2))-N*M
lapse=s.diff(L,N)*2/(B*a**3)
zero('original_lapse_variation',lapse-(3*S*v*v/(N*N*a*a)+V.subs(R,6/a**2)-2*M/(B*a**3)))
L1=L.subs(N,1)
EL=s.diff(L1,a)-s.diff(s.diff(L1,v),a)*v-s.diff(s.diff(L1,v),v)*w
spatial=s.simplify(2*EL/(B*a*a)).subs({v:a*H,w:a*(hd+H*H)})
target=3*S*(3*H*H+2*hd)+3*V-2*R*D
zero('original_spatial_variation',spatial-target.subs(R,6/a**2))
Hsquared=(2*Lambda+2*r-R+e*R**2)/(3*S)
Hdot=(R*D-3*r)/(3*S)
zero('both_background_equations',target.subs({H*H:Hsquared,hd:Hdot}))
zero('constraint_conservation',6*S*H*Hdot-2*H*R*D+6*H*r)
zero('known_flat_background',Hsquared.subs(R,0)-(2*Lambda+2*r)/(3*S))
zero('known_GR_curved_background',Hsquared.subs({lam:1,e:0})-(Lambda+r)/3+R/6)
eps,dR,d2R=s.symbols('eps deltaR delta2R')
quadratic=s.expand(V.subs(R,R+eps*dR+eps**2*d2R)).coeff(eps,2)
zero('curvature_second_variation',quadratic-(D*d2R-e*dR*dR))
zero('TT_no_four_derivative_square',quadratic.subs(dR,0)-D*d2R)
zero('known_flat_tensor_speed',D.subs(R,0)-1)
zero('known_no_stabilizer_tensor_speed',D.subs(e,0)-1)
wit={lam:2,e:1,Lambda:1,r:1,R:1}
zero('on_shell_H_squared_witness',Hsquared.subs(wit)-s.Rational(4,15))
zero('on_shell_Hdot_witness',Hdot.subs(wit)+s.Rational(4,15))
checks['witness_real_expansion']=bool(Hsquared.subs(wit)>0)
checks['witness_negative_tensor_speed']=bool(D.subs(wit)<0)
checks['mutate_flat_coefficient_rejected']=bool(D.subs(wit)!=1)
zero('curvature_threshold',D.subs(R,1/(2*e)))
for name,expected in [('Certificate',0),('Mutate',1)]:
    proc=subprocess.run(['/opt/homebrew/bin/lean',str(HERE/(name+'.lean'))],capture_output=True,text=True)
    log=(proc.stdout+proc.stderr).replace(str(ROOT),'.'); (HERE/(name+'.log')).write_text(log)
    checks['lean_'+name]=proc.returncode==expected and (name!='Mutate' or 'false' in log.lower())
checks['inputs_unchanged']=before==hashes()
result={'label':'κ = ½ FITTED; not theory closed','checks':{k:bool(v) for k,v in checks.items()},'checks_passed':sum(bool(v) for v in checks.values()),'checks_total':len(checks),
 'assertion_tested':'Exact curved dust background equations and TT curvature-variation identities; principal-action proof and scope in RESULT.md.',
 'verdicts':{foot:{'unrestricted_curved_continuum_stability':'FAIL','tensor_gate_below_threshold':'PASS','curved_scalar_and_full_galaxy_evolution':'NO VERDICT','finite_cutoff_physics':'NOT EVALUABLE','physical_kappa':'NOT EVALUABLE','whole_requirement_rows_held':0,'whole_RQ3_rows_held':0} for foot in ['canonical','alt']},
 'expressions':{'H_squared':str(Hsquared),'Hdot':str(Hdot),'tensor_speed_squared':str(D),'curvature_quadratic':str(quadratic)},
 'inputs_before':before,'inputs_after':hashes(),'versions':{'python':platform.python_version(),'sympy':s.__version__,'lean':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip()},
 'command':'python3 astra_goal_2026_11_03/P3/AZ29_curved_tensor_gate/run.py','run_status':'completed' if all(checks.values()) else 'failed'}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['checks_passed'],'total':len(checks),'failed':[k for k,v in checks.items() if not v],'expressions':result['expressions']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
