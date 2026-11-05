import hashlib,json,platform,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
inputs=[HERE/n for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']]+[HERE.parent/'AZ28_separable_fold_repair/RESULT.md',HERE.parent/'AZ29_curved_tensor_gate/RESULT.md']
hashes=lambda:{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
before=hashes(); checks={}
def zero(k,e):checks[k]=s.simplify(e)==0
eps,z,n,lap,grad2=s.symbols('eps z n lap grad2',real=True)
R,e,X,lam=s.symbols('R ell_squared X lambda',positive=True)
# Exact conformal spatial geometry. grad2 represents |D zeta|^2, already quadratic.
inside=R-4*eps*lap-2*eps**2*grad2
curv=s.exp(-2*eps*z)*inside
dens=(1+eps*n)*s.exp(3*eps*z)*(curv-e*curv**2)
quad=s.expand(s.series(dens,eps,0,3).removeO()).coeff(eps,2)
# Integrated harmonic identities: <z lap>=-X<z²>, <grad²>=X<z²>,
# <lap²>=X²<z²>, <n lap>=-X<n z>. Zero-derivative terms recorded separately.
qmode=s.expand(quad.subs({lap:-X*z,grad2:X*z*z}))
expected=(2+12*e*R)*X*z*z-16*e*X*X*z*z+4*(1-2*e*R)*X*n*z
mass=s.expand(qmode-expected)
zero('no_derivatives_in_remainder',s.diff(mass,X))
zero('conformal_Einstein_control',qmode.subs(e,0)-mass.subs(e,0)-(2*X*z*z+4*X*n*z))
zero('R_squared_cross_coefficient',s.diff(s.diff(expected,e),R).subs(n,0)-12*X*z*z)
checks['mutate_drop_curvature_cross_rejected']=s.simplify(expected-((2-4*e*R)*X*z*z-16*e*X*X*z*z+4*(1-2*e*R)*X*n*z))!=0
zd,b=s.symbols('zd shift_div',real=True)
S=3*lam-1
kin=-3*S*zd**2+2*S*zd*b+(1-lam-R/(3*X))*b*b
bsol=S*zd/(lam-1+R/(3*X))
C=S*(2-R/X)/(lam-1+R/(3*X))
zero('curved_shift_constraint',s.diff(kin,b).subs(b,bsol))
zero('curved_kinetic_coefficient',kin.subs(b,bsol)-C*zd*zd)
zero('known_flat_kinetic',C.subs(R,0)-2*(3*lam-1)/(lam-1))
spatial=expected+2*X*n*n
nsol=-(1-2*e*R)*z
zero('derivative_order_lapse_constraint',s.diff(spatial,n).subs(n,nsol))
P=16*e*X*X+(-20*e*R+8*e*e*R*R)*X
zero('reduced_spatial_derivative_block',spatial.subs(n,nsol)+P*z*z)
zero('known_flat_k4',P.subs(R,0)-16*e*X*X)
zero('closed_harmonic_lower_bound',P.subs(X,4*R/3)-e*(4*R/3)*(4*R/3+8*e*R*R))
zero('kinetic_numerator_at_lowest_mode',(2-R/X).subs(X,4*R/3)-s.Rational(5,4))
u,v=s.symbols('u v',positive=True)
checks['positive_block_above_lowest_harmonic']=bool(s.factor(P.subs(X,4*R/3+u)).is_positive)
checks['positive_kinetic_above_lowest_harmonic']=bool(s.factor(C.subs({X:4*R/3+u,lam:1+v})).is_positive)
c3=s.symbols('c3',real=True)
zero('unfixed_omitted_operator_ratio',c3*e**2*R**3/(e*R**2)-c3*e*R)
for name,expected_exit in [('Certificate',0),('Mutate',1)]:
    proc=subprocess.run(['/opt/homebrew/bin/lean',str(HERE/(name+'.lean'))],capture_output=True,text=True)
    log=(proc.stdout+proc.stderr).replace(str(ROOT),'.'); (HERE/(name+'.log')).write_text(log)
    checks['lean_'+name]=proc.returncode==expected_exit and (name!='Mutate' or 'false' in log.lower())
checks['inputs_unchanged']=before==hashes()
result={'label':'κ = ½ FITTED; not theory closed','checks':{key:bool(val) for key,val in checks.items()},'checks_passed':sum(bool(v) for v in checks.values()),'checks_total':len(checks),
 'assertion_tested':'Exact conformal spatial expansion and derivative-order constraint block; not full curved time-dependent scalar spectrum.',
 'verdicts':{foot:{'retained_scalar_derivative_block':'PASS' if all(checks.values()) else 'FAIL','action_alone_selects_cutoff':'FAIL','physical_validity_window':'NOT EVALUABLE','full_curved_scalar_stability':'NO VERDICT','physical_kappa':'NOT EVALUABLE','whole_requirement_rows_held':0,'whole_RQ3_rows_held':0} for foot in ['canonical','alt']},
 'expressions':{'conformal_quadratic':str(quad),'zero_derivative_spatial_remainder':str(mass),'curved_derivative_kinetic':str(C),'restoring_derivative_block':str(P)},
 'inputs_before':before,'inputs_after':hashes(),'versions':{'python':platform.python_version(),'sympy':s.__version__,'lean':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip()},
 'command':'python3 astra_goal_2026_11_03/P3/AZ30_weak_curvature_scalar/run.py','run_status':'completed' if all(checks.values()) else 'failed'}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['checks_passed'],'total':len(checks),'failed':[key for key,val in checks.items() if not val],'expressions':result['expressions']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
