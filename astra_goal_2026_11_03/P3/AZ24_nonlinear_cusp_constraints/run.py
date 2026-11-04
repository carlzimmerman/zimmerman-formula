import hashlib, json, platform, subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
inputs=[HERE/'CRITERIA.md',HERE/'run.py',HERE/'Certificate.lean',HERE/'Mutate.lean',HERE.parent/'AZ23_causal_critical_response/RESULT.md',ROOT/'why_4_puzzle/W4_08_positive_mond_amplitudes/formal/critical_endpoint/RESULT.md',ROOT/'why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant/SINGLE_FUNCTION.md']
hashes=lambda:{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
before=hashes(); checks={}
def zero(k,e): checks[k]=s.simplify(e)==0
N,Nx,Nxx,z,zx,zxx,zt,ztx,v,vx,vxx,P,Px,f=s.symbols('N Nx Nxx z zx zxx zt ztx v vx vxx P Px f',real=True)
a,H,m,C1,C2,K0,A,q,g,E=s.symbols('a H m C1 C2 K0 A q g E',positive=True)
c1,c2=-C1,-C2
T=(H+zt-v*zx)/N; w=vx/N; K=3*T-w
ginv=s.exp(-2*z)/a**2
acc2=ginv*(Nx/N)**2
R3=ginv*(-4*zxx-2*zx*zx)
Qkin=-6*T*T+4*T*w
I=(c2*K*K-c1*acc2)/m**2
F=s.Function('F'); u=s.Symbol('u')
fp=s.diff(F(u),u).subs(u,I)
L=N*s.exp(3*z)*(R3+Qkin+m*m*F(I))
def reduce(e):
    # SymPy canonicalizes I during differentiation; structural subs(fp,P)
    # misses that equivalent argument. Check equality before replacing it.
    replacements={}
    for atom in e.atoms(s.Subs):
        assert isinstance(atom.expr,s.Derivative) and atom.expr.expr.func==F
        assert s.simplify(atom.point[0]-I)==0
        replacements[atom]=P
    e=e.xreplace(replacements)
    for atom in e.atoms(s.Function):
        if atom.func==F:
            assert s.simplify(atom.args[0]-I)==0
            e=e.xreplace({atom:f})
    return s.simplify(e)
dx=lambda e:sum(s.diff(e,k)*val for k,val in {N:Nx,Nx:Nxx,z:zx,zx:zxx,zt:ztx,v:vx,vx:vxx,P:Px}.items())
dLv=reduce(s.diff(L,v)); dLvx=reduce(s.diff(L,vx))
momentum=dx(c2*P*K-2*T)-2*zx*w
zero('exact_shift_variation',s.exp(-3*z)*(dLv-dx(dLvx))/2-momentum)
ham=R3-Qkin+m*m*f-2*c2*P*K*K+2*c1*P*acc2+2*c1*s.exp(-3*z)*dx(s.exp(3*z)*P*ginv*Nx/N)
zero('exact_lapse_variation',s.exp(-3*z)*(reduce(s.diff(L,N))-dx(reduce(s.diff(L,Nx))))-ham)
checks['mutate_missing_connection_rejected']=s.simplify(momentum-dx(c2*P*K-2*T))!=0
I0=-C2*K0*K0/m**2
F0=4*I0/C1-2*K0*K0/(3*m*m)
h0=ham.subs({Nx:0,Nxx:0,zx:0,zxx:0,zt:0,ztx:0,v:0,vx:0,vxx:0,N:1,P:2/C1,Px:0,f:F0.subs(K0,3*H)})
zero('known_homogeneous_vacuum',h0)
xa=C1*A*A/(m*m)
Fq=F0+4*xa/C1*(q-s.log(1+q))
zero('integrated_cusp_derivative',s.diff(Fq,q)/(2*xa*q)-2/(C1*(1+q)))
J=K0-C1*E/C2
Kbranch=J*(1+q)
zero('integrated_momentum',c2*(2*Kbranch/(C1*(1+q))-2*K0/C1)-2*E)
poly=(C1*A*A+C2*J*J)*q*q+2*C2*J*J*q+C2*(J*J-K0*K0)-C1*g*g
zero('branch_polynomial',poly-(m*m*xa*q*q+C2*(Kbranch*Kbranch-K0*K0)-C1*g*g))
zero('known_zero_source_root',poly.subs({E:0,g:0,q:0}))
S=C1*g*g+C2*(K0*K0-J*J)
eps,e1,g1=s.symbols('eps e1 g1',real=True)
zero('domain_first_order',s.diff(S.subs({E:eps*e1,g:eps*g1}),eps).subs(eps,0)-2*C1*K0*e1)
zero('width_absent_at_vacuum',s.diff(Fq.subs(q,0),A))
zero('width_absent_in_vacuum_slope',s.diff(2/(C1*(1+q)),A))
# Negative E is allowed as a test substitution although the symbolic E was
# declared positive only to simplify some other exact expressions.
bad=s.factor(poly.subs({C1:1,C2:1,K0:1,A:1,E:-s.Rational(1,10),g:0}))
checks['negative_domain_all_coefficients_positive']=all(c>0 for c in s.Poly(bad,q).all_coeffs())
y,B,Q=s.symbols('y B Q',positive=True)
zp=Q*y**3/12; np=-zp
U=-H*y*s.diff(zp,y)-H*np
zero('AZ23_source_U',U+H*Q*y**3/6)
checks['AZ23_particular_negative_U']=bool((-U).is_positive)
for name,expected in [('Certificate',0),('Mutate',1)]:
    p=subprocess.run(['/opt/homebrew/bin/lean',str(HERE/(name+'.lean'))],capture_output=True,text=True)
    log=(p.stdout+p.stderr).replace(str(ROOT),'.'); (HERE/(name+'.log')).write_text(log)
    checks['lean_'+name]=p.returncode==expected and (name!='Mutate' or 'false' in log.lower())
checks['inputs_unchanged']=before==hashes()
result={'label':'κ = ½ FITTED; not theory closed','checks':{k:bool(v) for k,v in checks.items()},'checks_passed':sum(bool(v) for v in checks.values()),'checks_total':len(checks),
 'assertion_tested':'Exact plane ADM constraint identities and one-sided nonlinear cusp admissibility; not full PDE evolution.',
 'verdicts':{f:{'constraint_derivation':'PASS' if all(checks.values()) else 'FAIL','unrestricted_AZ23_nonlinear_extrapolation':'FAIL','late_time_selection':'NO VERDICT','physical_kappa':'NOT EVALUABLE','whole_requirement_rows_held':0,'whole_RQ3_rows_held':0} for f in ['canonical','alt']},
 'expressions':{'branch_polynomial':str(s.expand(poly)),'domain_S':str(s.factor(S)),'negative_domain_witness':str(bad),'AZ23_particular_U':str(U),'connection_mutant_residual':str(-2*zx*w)},
 'inputs_before':before,'inputs_after':hashes(),'versions':{'python':platform.python_version(),'sympy':s.__version__,'lean':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip()},
 'command':'python3 astra_goal_2026_11_03/P3/AZ24_nonlinear_cusp_constraints/run.py','run_status':'completed' if all(checks.values()) else 'failed'}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['checks_passed'],'total':len(checks),'failed':[k for k,v in checks.items() if not v],'expressions':result['expressions']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
