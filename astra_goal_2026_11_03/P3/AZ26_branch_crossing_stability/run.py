import hashlib,json,platform,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
inputs=[HERE/n for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']]+[HERE.parent/'AZ24_nonlinear_cusp_constraints/RESULT.md',HERE.parent/'AZ25_nonlinear_cosmic_attractor/RESULT.md',ROOT/'why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant/SINGLE_FUNCTION.md']
hashes=lambda:{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
before=hashes(); checks={}
def zero(k,e):checks[k]=s.simplify(e)==0
C1,C2,A,H0,m,K0,g,u=s.symbols('C1 C2 A H0 m K0 g u',positive=True)
q,J=s.symbols('q J',real=True)
S=C1*g*g+C2*(K0*K0-J*J)
Pplus=C1*A*A*q*q+C2*J*J*(1+q)**2-C2*K0*K0-C1*g*g
Pminus=-C1*A*A*q*q+C2*J*J*(1+q)**2-C2*K0*K0-C1*g*g
zero('crossing_value_continuity',(Pplus-Pminus).subs(q,0))
zero('crossing_derivative_continuity',s.diff(Pplus-Pminus,q).subs(q,0))
zero('left_boundary_negative',Pminus.subs(q,-1)+C1*A*A+C2*K0*K0+C1*g*g)
zero('left_derivative_positive_decomposition',s.diff(Pminus,q)-(-2*C1*A*A*q+2*C2*J*J*(1+q)))
zero('right_derivative_positive_decomposition',s.diff(Pplus,q)-(2*C1*A*A*q+2*C2*J*J*(1+q)))
zero('crossing_condition',Pplus.subs(q,0)+S)
zero('crossing_jacobian',s.diff(Pplus,q).subs(q,0).subs(J*J,K0*K0+C1*g*g/C2)-2*(C2*K0*K0+C1*g*g))
zero('width_absent_at_crossing',s.diff(Pplus.subs(q,0),A))
# Direct scalar principal action, obtained by expanding the original trace
# kinetic term and spatial Ricci/lapse-gradient terms at a homogeneous jet.
lam,alpha,X=s.symbols('lambda alpha X',positive=True)
zd,z,n,b=s.symbols('zd z n shift_div',real=True)
Sp=3*lam-1
L=-3*Sp*zd**2+2*Sp*zd*b+(1-lam)*b*b+X*(2*z*z+4*n*z+alpha*n*n)
bsol=Sp*zd/(lam-1); nsol=-2*z/alpha
zero('shift_constraint',s.diff(L,b).subs(b,bsol))
zero('lapse_constraint',s.diff(L,n).subs(n,nsol))
Lred=s.factor(L.subs({b:bsol,n:nsol}))
C=2*(3*lam-1)/(lam-1); G=2*(2-alpha)/alpha
zero('constrained_principal_action',Lred-(C*zd*zd-G*X*z*z))
cs=G/C
zero('known_sound_speed',cs-(lam-1)*(2-alpha)/(alpha*(3*lam-1)))
zero('positive_gradient_control',cs.subs({lam:2,alpha:1})-s.Rational(1,5))
zero('negative_gradient_control',cs.subs({lam:2,alpha:4})+s.Rational(1,10))
checks['mutate_gradient_sign_rejected']=s.simplify(Lred-(C*zd*zd+G*X*z*z))!=0
# AZ25 negative-q background, with all widths still symbolic.
xa=C1*A*A/m**2; I0=-9*C2*H0*H0/m**2; I=I0-xa*q*q
fp=2/(C1*(1+q)); fpp=s.diff(fp,q)/s.diff(I,q)
Q= s.factor(fp+2*I*fpp)
lamleft=1+C2*Q
zero('negative_branch_Q',Q-2*(I0+xa*q)/(C1*xa*q*(1+q)**2))
mapped=s.factor(Q.subs(q,-u/(1+u)))
checks['Q_positive_on_entire_negative_branch']=bool(mapped.is_positive)
csleft=s.factor(cs.subs({lam:lamleft,alpha:2/(1+q)}))
zero('width_independent_sign_factor',csleft-q*(lamleft-1)/(3*lamleft-1))
checks['speed_negative_on_entire_negative_branch']=bool((-s.factor(csleft.subs(q,-u/(1+u)))).is_positive)
zero('near_cusp_speed',s.limit(csleft/q,q,0,dir='-')-s.Rational(1,3))
t,k,qa=s.symbols('t k qa',positive=True)
growth=k*s.sqrt(qa/3)*s.exp(-5*H0*t/2)
integral=2*k*s.sqrt(qa/3)/(5*H0)*(1-s.exp(-5*H0*t/2))
zero('late_time_WKB_integral',s.diff(integral,t)-growth)
zero('late_time_integral_linear_in_k',s.diff(integral,k,2))
for name,expected in [('Certificate',0),('Mutate',1)]:
    p=subprocess.run(['/opt/homebrew/bin/lean',str(HERE/(name+'.lean'))],capture_output=True,text=True)
    log=(p.stdout+p.stderr).replace(str(ROOT),'.'); (HERE/(name+'.log')).write_text(log)
    checks['lean_'+name]=p.returncode==expected and (name!='Mutate' or 'false' in log.lower())
checks['inputs_unchanged']=before==hashes()
result={'label':'κ = ½ FITTED; not theory closed','checks':{k:bool(v) for k,v in checks.items()},'checks_passed':sum(bool(v) for v in checks.values()),'checks_total':len(checks),
 'assertion_tested':'Nonlinear algebraic crossing and exact constrained principal-symbol identities for the AZ25 cosmic branch; no galaxy simulation.',
 'verdicts':{f:{'algebraic_crossing':'PASS' if all(checks.values()) else 'FAIL','declared_continuum_inhomogeneous_stability':'FAIL','width_selection_by_health':'FAIL','finite_cutoff_physics':'NOT EVALUABLE','physical_kappa':'NOT EVALUABLE','whole_requirement_rows_held':0,'whole_RQ3_rows_held':0} for f in ['canonical','alt']},
 'expressions':{'reduced_principal_action':str(Lred),'Q_left':str(Q),'Q_positive_reparameterization':str(mapped),'sound_speed_squared_left':str(csleft),'negative_speed_positive_reparameterization':str(s.factor(-csleft.subs(q,-u/(1+u)))),'late_time_WKB_exponent':str(integral)},
 'inputs_before':before,'inputs_after':hashes(),'versions':{'python':platform.python_version(),'sympy':s.__version__,'lean':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip()},
 'command':'python3 astra_goal_2026_11_03/P3/AZ26_branch_crossing_stability/run.py','run_status':'completed' if all(checks.values()) else 'failed'}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['checks_passed'],'total':len(checks),'failed':[k for k,v in checks.items() if not v],'expressions':result['expressions']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
