import hashlib,json,platform,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
inputs=[HERE/n for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']]+[HERE.parent/'AZ27_stable_cosmic_completion/RESULT.md',ROOT/'sol61_push/CANONICAL_CLOCK_RESULTS.md']
hashes=lambda:{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
before=hashes(); checks={}
def zero(k,e):checks[k]=s.simplify(e)==0
A,g,y,ell,k,B,Lambda,H=s.symbols('A g y ell k B Lambda H',positive=True)
lam=s.symbols('lambda',positive=True); c=s.symbols('cosine_squared',real=True)
f=4*A*g-4*A*A*s.log(1+g/A)
at=s.simplify(s.diff(f,g)/(2*g)); al=s.simplify(at+g*s.diff(at,g))
zero('transverse_Hessian',at-2/(1+g/A))
zero('longitudinal_Hessian',al-2/(1+g/A)**2)
ac=(at+(al-at)*c).subs(g,A*y)
zero('directional_Hessian',ac-2*(1+y*(1-c))/(1+y)**2)
zero('Hessian_lower_bound',ac-2/(1+y)**2-2*y*(1-c)/(1+y)**2)
zero('Hessian_upper_bound',2/(1+y)-ac-2*y*c/(1+y)**2)
zero('zero_gradient_Hessian',ac.subs(y,0)-2)
mu=s.simplify(1-at/2)
zero('static_constitutive_law',mu-g/(A+g))
zero('deep_MOND_coefficient',s.limit(mu/g,g,0)-1/A)
K=s.symbols('K',real=True)
zero('constant_trace_Jacobian',s.diff((1-3*lam)*K,K)-(1-3*lam))
zero('no_acceleration_trace_mixing',s.diff((1-3*lam)*K,g))
zd,z,n,b,alpha=s.symbols('zd z n shift_div alpha',real=True)
C=2*(3*lam-1)/(lam-1); G=2*(2-alpha)/alpha
L=-3*(3*lam-1)*zd**2+2*(3*lam-1)*zd*b+(1-lam)*b*b+k*k*(2*z*z+4*n*z+alpha*n*n)-16*ell**2*k**4*z*z
red=s.simplify(L.subs({b:(3*lam-1)*zd/(lam-1),n:-2*z/alpha}))
zero('constrained_angular_action',red-(C*zd*zd-(G*k*k+16*ell**2*k**4)*z*z))
omega=(G*k*k+16*ell**2*k**4)/C
zero('inherited_zero_gradient_k4_control',omega.subs(alpha,2)-8*ell**2*(lam-1)*k**4/(3*lam-1))
checks['mutate_k4_sign_rejected']=bool((-16*ell**2*k**4/C).subs(lam,2).is_negative)
checks['mutate_negative_Hessian_rejected']=bool(ac.subs({y:1,c:1})>0 and -ac.subs({y:1,c:1})<0)
# Weak-static, zero-background-acceleration Fourier source, alpha retained
# symbolically for an independent linear constraint check.
phi,psi,rho=s.symbols('phi psi rho',real=True)
Ls=B/2*(2*k*k*psi*psi-4*k*k*phi*psi+alpha*k*k*phi*phi-16*ell**2*k**4*psi*psi)-rho*phi
den=1-alpha/2+4*alpha*ell**2*k*k
psis=-rho/(2*B*k*k*den); phis=(1-8*ell**2*k*k)*psis
zero('static_lapse_constraint',s.diff(Ls,phi).subs({phi:phis,psi:psis}))
zero('static_spatial_constraint',s.diff(Ls,psi).subs({phi:phis,psi:psis}))
zero('zero_stabilizer_Newton_control',phis.subs({ell:0,alpha:0})+rho/(2*B*k*k))
zero('static_potential_zero',phis.subs(k,1/(s.sqrt(8)*ell)))
zero('vacuum_Friedmann', (3*(3*lam-1)*H*H-2*Lambda).subs(H*H,2*Lambda/(3*(3*lam-1))))
zero('width_absent_in_vacuum',s.diff(2*Lambda/(3*(3*lam-1)),A))
for name,expected in [('Certificate',0),('Mutate',1)]:
    proc=subprocess.run(['/opt/homebrew/bin/lean',str(HERE/(name+'.lean'))],capture_output=True,text=True)
    log=(proc.stdout+proc.stderr).replace(str(ROOT),'.'); (HERE/(name+'.log')).write_text(log)
    checks['lean_'+name]=proc.returncode==expected and (name!='Mutate' or 'false' in log.lower())
checks['inputs_unchanged']=before==hashes()
result={'label':'κ = ½ FITTED; not theory closed','checks':{key:bool(val) for key,val in checks.items()},'checks_passed':sum(bool(v) for v in checks.values()),'checks_total':len(checks),
 'assertion_tested':'Exact separable momentum Jacobian, angular lapse Hessian, frozen locally flat constrained principal action and weak-static source equations; not global nonlinear health.',
 'verdicts':{foot:{'specified_fold_removed':'PASS' if all(checks.values()) else 'FAIL','frozen_principal_stability':'PASS' if all(checks.values()) else 'FAIL','global_nonlinear_stability':'NO VERDICT','width_selection':'FAIL','physical_kappa':'NOT EVALUABLE','whole_requirement_rows_held':0,'whole_RQ3_rows_held':0} for foot in ['canonical','alt']},
 'expressions':{'angular_Hessian':str(s.factor(ac)),'dispersion':str(omega),'static_lapse_potential':str(phis),'vacuum_H_squared':str(2*Lambda/(3*(3*lam-1)))},
 'inputs_before':before,'inputs_after':hashes(),'versions':{'python':platform.python_version(),'sympy':s.__version__,'lean':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip()},
 'command':'python3 astra_goal_2026_11_03/P3/AZ28_separable_fold_repair/run.py','run_status':'completed' if all(checks.values()) else 'failed'}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['checks_passed'],'total':len(checks),'failed':[key for key,val in checks.items() if not val],'expressions':result['expressions']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
