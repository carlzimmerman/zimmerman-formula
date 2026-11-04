import hashlib,json,platform,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
inputs=[HERE/n for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']]+[HERE.parent/'AZ24_nonlinear_cusp_constraints/RESULT.md',ROOT/'why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant/SINGLE_FUNCTION.md']
hashes=lambda:{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
before=hashes(); checks={}
def zero(k,e):checks[k]=s.simplify(e)==0
q=s.symbols('q',real=True); C1,C2,A,H0,m,B=s.symbols('C1 C2 A H0 m B',positive=True)
I0=-9*C2*H0**2/m**2; xa=C1*A*A/m**2
F0=4*I0/C1-6*H0**2/m**2
Fminus=F0-4*xa/C1*(q-s.log(1+q))
Fplus=F0+4*xa/C1*(q-s.log(1+q))
I=I0-xa*q*q
fp=2/(C1*(1+q))
Y=H0**2+C1*A*A*q*q/(9*C2)
r=s.simplify(3*Y-m*m*(2*I*fp-Fminus)/2) # r=rho/B
rp=s.diff(r,q)
rp_claim=2*C1*A*A*q/(3*C2)+2*A*A*q/(1+q)-18*C2*Y/(C1*(1+q)**2)
zero('original_Friedmann_constraint',3*Y-r-m*m*(2*I*fp-Fminus)/2)
zero('invariant_H_relation',I+9*C2*Y/m**2)
zero('left_branch_derivative',s.diff(Fminus,q)/s.diff(I,q)-fp)
zero('right_branch_derivative',s.diff(Fplus,q)/(2*xa*q)-fp)
zero('continuous_cusp_value',Fminus.subs(q,0)-Fplus.subs(q,0))
zero('known_vacuum_density',r.subs(q,0))
zero('density_derivative_decomposition',rp-rp_claim)
zero('density_slope_at_vacuum',rp.subs(q,0)+18*C2*H0**2/C1)
# The displayed rp decomposition has three strictly negative terms on -1<q<0.
# Verify the only nontrivial factor Y is explicitly a positive sum.
zero('positive_H_squared_decomposition',Y-(H0**2+C1*A*A*q*q/(9*C2)))
checks['density_infinite_at_left_boundary']=s.limit(r,q,-1,dir='+')==s.oo
qdot=-3*s.sqrt(Y)*r/rp
zero('nonlinear_conservation',rp*qdot+3*s.sqrt(Y)*r)
fpp=s.diff(fp,q)/s.diff(I,q)
Qkin=fp+2*I*fpp
Hdot=s.diff(Y,q)*qdot/(2*s.sqrt(Y))
zero('independent_spatial_metric_equation',(2+3*C2*Qkin)*Hdot+r)
zero('late_time_relaxation_rate',s.limit(qdot/q,q,0,dir='-')+3*H0)
coefficient=s.limit((Y-H0**2)/r**2,q,0,dir='-')
expected=C1**3*A**2/(2916*C2**3*H0**4)
zero('late_time_width_coefficient',coefficient-expected)
zero('zero_linear_homogeneous_susceptibility',s.limit(s.diff(Y,q)/rp,q,0,dir='-'))
zero('width_retained',s.diff(coefficient,A)-2*coefficient/A)
rwrong=3*Y+m*m*Fminus/2
checks['mutate_missing_stress_term_rejected']=s.simplify(rwrong.subs(q,0))!=0
for name,expected_exit in [('Certificate',0),('Mutate',1)]:
    p=subprocess.run(['/opt/homebrew/bin/lean',str(HERE/(name+'.lean'))],capture_output=True,text=True)
    log=(p.stdout+p.stderr).replace(str(ROOT),'.'); (HERE/(name+'.log')).write_text(log)
    checks['lean_'+name]=p.returncode==expected_exit and (name!='Mutate' or 'false' in log.lower())
checks['inputs_unchanged']=before==hashes()
result={'label':'κ = ½ FITTED; not theory closed','checks':{k:bool(v) for k,v in checks.items()},'checks_passed':sum(bool(v) for v in checks.values()),'checks_total':len(checks),
 'assertion_tested':'Exact homogeneous nonlinear signed-cusp constraint, conservation law and asymptotic identities; monotonicity/convergence proof in RESULT.md.',
 'verdicts':{f:{'homogeneous_attractor':'PASS' if all(checks.values()) else 'FAIL','homogeneous_normalization_selection':'FAIL','galaxy_evolution':'NO VERDICT','all_mode_health':'NO VERDICT','physical_kappa':'NOT EVALUABLE','whole_requirement_rows_held':0,'whole_RQ3_rows_held':0} for f in ['canonical','alt']},
 'expressions':{'rho_over_B':str(r),'density_derivative':str(s.factor(rp)),'late_time_H_squared_coefficient':str(coefficient),'wrong_vacuum_density':str(s.simplify(rwrong.subs(q,0)))},
 'inputs_before':before,'inputs_after':hashes(),'versions':{'python':platform.python_version(),'sympy':s.__version__,'lean':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip()},
 'command':'python3 astra_goal_2026_11_03/P3/AZ25_nonlinear_cosmic_attractor/run.py','run_status':'completed' if all(checks.values()) else 'failed'}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['checks_passed'],'total':len(checks),'failed':[k for k,v in checks.items() if not v],'expressions':result['expressions']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
