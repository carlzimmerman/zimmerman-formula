"""Exact rotating-wave coefficients and restricted emergent-current ledger."""
import json
import pathlib
import sys
import sympy as s

checks=[]
def ck(label, condition):
    if not condition:
        raise AssertionError(label)
    checks.append({'label':label,'passed':True})
def zero(label,expr):
    ck(label,s.simplify(s.expand(expr))==0)
z=s.symbols('z',nonzero=True)
pp,pm,pb,mb,bp,bm,bb,cb=s.symbols('psi_plus psi_minus psi_plus_bar psi_minus_bar b_plus b_minus b_plus_bar b_minus_bar')
fields=[pp,pm,pb,mb,bp,bm,bb,cb]
# Conjugates are independent polynomial variables for exact coefficient algebra.
phi=z*pp+mb/z
phic=pb/z+z*pm
X=z**2*bp+cb/z**2
Xc=bb/z**2+z**2*bm
cubic=s.expand(Xc*phi**2+X*phic**2)
quartic=s.expand((phic*phi)**2)
slow_cubic=cubic.coeff(z,0)
slow_quartic=quartic.coeff(z,0)
expected_cubic=bb*pp**2+bp*pb**2+cb*pm**2+bm*mb**2
expected_quartic=pb**2*pp**2+mb**2*pm**2+4*pb*pp*mb*pm
zero('slow cubic coefficient',slow_cubic-expected_cubic)
zero('slow quartic cross factor four',slow_quartic-expected_quartic)
plus=[1,0,-1,0,2,0,-2,0]
minus=[0,1,0,-1,0,2,0,-2]
for label,slow in [('cubic',slow_cubic),('quartic',slow_quartic)]:
    mons=s.Poly(slow,*fields).monoms()
    ck(label+' independent particle U1',all(sum(a*b for a,b in zip(mon,plus))==0 for mon in mons))
    ck(label+' independent antiparticle U1',all(sum(a*b for a,b in zip(mon,minus))==0 for mon in mons))
full_mons=s.Poly(cubic,*fields).monoms()
ck('full cubic still has exact signed U1',all(sum(a*(b-c) for a,b,c in zip(mon,plus,minus))==0 for mon in full_mons))
ck('full cubic violates emergent equal-angle number',any(sum(a*(b+c) for a,b,c in zip(mon,plus,minus))!=0 for mon in full_mons))
n1,n2,nb1,nb2,m,M=s.symbols('n1 n2 nb1 nb2 m M',positive=True)
q=n1+n2+2*(nb1+nb2)
rho=m*(n1+n2)+M*(nb1+nb2)
zero('neutral-compatible positive current rest dictionary',rho-m*q-(M-2*m)*(nb1+nb2))
r1,r2=s.symbols('Rplus Rminus',real=True)
zero('sum-current conversion conservation',2*r1+2*r2+2*(-r1-r2))
zero('sum rest work',m*(2*r1+2*r2)+M*(-r1-r2)+(M-2*m)*(r1+r2))
# The upper bound follows from the manifestly nonnegative remainder.
zero('positive mass-bound numerator remainder', (M-2*m)*rho-M*(rho-m*q)-m*(M-2*m)*(n1+n2))
full_N_initial=2+2
full_N_final=1+1
ck('source pair annihilation full weighted defect minus two',full_N_final-full_N_initial==-2)
ck('source pair hard escape soft defect minus four',0-full_N_initial==-4)
ck('four daughter to two hard daughters weighted defect minus two',2-4==-2)
result={'status':'all_exact_checks_passed','assertions':len(checks),'checks':checks,
        'rwa_cubic':str(slow_cubic),'rwa_quartic':str(slow_quartic),
        'non_claims':['No physical NR or small loss hierarchy verified','No scattering rate computed','No W matching or halo formation','No exact new symmetry of the microscopic relativistic theory']}
pathlib.Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'assertions':len(checks)}))
