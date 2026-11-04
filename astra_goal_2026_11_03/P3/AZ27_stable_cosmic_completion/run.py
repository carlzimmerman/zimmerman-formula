import hashlib,json,platform,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
inputs=[HERE/n for n in ['CRITERIA.md','run.py','Certificate.lean','Mutate.lean']]+[HERE.parent/'AZ24_nonlinear_cusp_constraints/RESULT.md',HERE.parent/'AZ26_branch_crossing_stability/RESULT.md',ROOT/'why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant/SINGLE_FUNCTION.md']
hashes=lambda:{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
before=hashes(); checks={}
def zero(k,e):checks[k]=s.simplify(e)==0
z,p,C1,C2,H0,m,A,J0=s.symbols('z p C1 C2 H0 m A J0',positive=True)
F0=-4*J0/C1-6*H0**2/m**2
F=F0-2*J0/C1*(z**(1-p)-1)/(1-p)
fp=2*z**(-p)/C1
fpp=s.diff(fp,z)/(-J0)
Q=s.simplify(fp+2*(-J0*z)*fpp)
zero('integrated_derivative',s.diff(F,z)/(-J0)-fp)
zero('continuous_value',F.subs(z,1)-F0)
zero('continuous_slope',fp.subs(z,1)-2/C1)
zero('trace_hessian',Q-(1-2*p)*fp)
rho=3*H0**2*z-m*m*(2*(-J0*z)*fp-F)/2
rho_target=3*H0**2*(z-1)+m*m*J0/C1*(1-2*p)/(1-p)*(z**(1-p)-1)
zero('exact_density_constraint',rho-rho_target)
zero('vacuum_density',rho.subs(z,1))
rp=s.diff(rho,z)
zero('monotone_density_derivative',rp-(3*H0**2+m*m*J0/C1*(1-2*p)*z**(-p)))
zdot=-3*H0*s.sqrt(z)*rho/rp
zero('nonlinear_dust_conservation',rp*zdot+3*H0*s.sqrt(z)*rho)
zero('width_absent_cosmology',s.diff(rho,A))
lam=1+C2*Q; alpha=C1*fp
C=2*(3*lam-1)/(lam-1)
cs=(lam-1)*(2-alpha)/(alpha*(3*lam-1))
zero('stable_speed_factor',cs-(z**p-1)*(lam-1)/(3*lam-1))
zero('positive_kinetic_decomposition',C-(6+4/(lam-1)))
zero('stable_finite_control',cs.subs({p:s.Rational(1,4),z:16,C1:1,C2:1})-s.Rational(1,7))
zero('endpoint_speed',cs.subs(z,1))
zero('endpoint_kinetic_jump',C.subs(z,1)-6-2*C1/(C2*(1-2*p)))
zero('linear_cosmic_response',H0**2/rp.subs(z,1).subs(J0,9*C2*H0**2/m**2)-1/(3+9*C2*(1-2*p)/C1))
# Nonlinear fixed-acceleration momentum Jacobian, normalized by F'.
K,g=s.symbols('K g',positive=True)
Inon=(-C2*K*K+C1*g*g)/m**2
fpnon=2/C1*((-Inon)/J0)**(-p)
jac=s.simplify(s.diff(fpnon*K,K)/fpnon)
target=1-2*p*C2*K*K/(C2*K*K-C1*g*g)
zero('nonlinear_momentum_jacobian',jac-target)
zero('fold_location',target.subs(g*g,(1-2*p)*C2*K*K/C1))
zero('fold_invariant',Inon.subs(g*g,(1-2*p)*C2*K*K/C1)+2*p*C2*K*K/m**2)
zero('fold_witness',target.subs({p:s.Rational(1,4),C1:1,C2:1,K:2,g:s.sqrt(2)}))
checks['fold_witness_inside_left_domain']=bool(Inon.subs({C1:1,C2:1,K:2,g:s.sqrt(2),m:1}) < -1)
checks['mutate_exponent_range_rejected']=bool(Q.subs({p:s.Rational(3,4),z:16,C1:1})<0)
for name,expected in [('Certificate',0),('Mutate',1)]:
    proc=subprocess.run(['/opt/homebrew/bin/lean',str(HERE/(name+'.lean'))],capture_output=True,text=True)
    log=(proc.stdout+proc.stderr).replace(str(ROOT),'.'); (HERE/(name+'.log')).write_text(log)
    checks['lean_'+name]=proc.returncode==expected and (name!='Mutate' or 'false' in log.lower())
checks['inputs_unchanged']=before==hashes()
result={'label':'κ = ½ FITTED; not theory closed','checks':{k:bool(v) for k,v in checks.items()},'checks_passed':sum(bool(v) for v in checks.values()),'checks_total':len(checks),
 'assertion_tested':'Exact power-law completion identities, cosmic principal stability factors, and nonlinear momentum fold; interval proofs in RESULT.md.',
 'verdicts':{f:{'cosmic_gradient_repair':'PASS' if all(checks.values()) else 'FAIL','uniform_momentum_invertibility':'FAIL','full_nonlinear_stability':'NO VERDICT','width_selection':'FAIL','physical_kappa':'NOT EVALUABLE','whole_requirement_rows_held':0,'whole_RQ3_rows_held':0} for f in ['canonical','alt']},
 'expressions':{'Q':str(Q),'density':str(rho_target),'sound_speed_squared':str(s.factor(cs)),'nonlinear_Jacobian_over_Fprime':str(target),'endpoint_kinetic_jump':str(2*C1/(C2*(1-2*p)))},
 'inputs_before':before,'inputs_after':hashes(),'versions':{'python':platform.python_version(),'sympy':s.__version__,'lean':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip()},
 'command':'python3 astra_goal_2026_11_03/P3/AZ27_stable_cosmic_completion/run.py','run_status':'completed' if all(checks.values()) else 'failed'}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['checks_passed'],'total':len(checks),'failed':[k for k,v in checks.items() if not v],'expressions':result['expressions']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
