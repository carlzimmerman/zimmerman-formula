"""CE-FM-015: a varied clock changes the longitudinal independent-P wave."""
import json,sys
from pathlib import Path
import sympy as s

I,gamma,k=s.symbols('I gamma k',positive=True)
P,pi,pP,ppi,mult=s.symbols('P pi pP ppi lambda',real=True)
pd,td=s.symbols('Pdot pidot',real=True)
L=I*pd*pd/2-gamma*k*k*P*P/2-k*P*td
H=pP*pP/(2*I)+gamma*k*k*P*P/2
C=ppi+k*P
HT=H+mult*C
checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)
def PB(a,b):
    return sum(s.diff(a,q)*s.diff(b,p)-s.diff(a,p)*s.diff(b,q) for q,p in ((P,pP),(pi,ppi)))
check('primary clock constraint',s.simplify(s.diff(L,td)+k*P)==0,'p_pi=-kP')
secondary=s.factor(PB(C,HT))
check('constraint consistency kills Pdot',s.simplify(secondary-k*pP/I)==0,str(secondary))
check('secondclass bracket',PB(C,pP)==k,'nonzero fornonzerok')
multiplier=s.solve(s.Eq(PB(pP,HT),0),mult)[0]
check('determined clock velocity',s.simplify(multiplier+gamma*k*P)==0,str(multiplier))
reduced=s.simplify(H.subs({pP:0,P:-ppi/k}))
check('nonnegative reduced clock Hamiltonian',s.simplify(reduced-gamma*ppi*ppi/2)==0,str(reduced))
check('zero restoring gradient forclock',s.diff(reduced,pi)==0,'p_pi_dot=0,pi_dot=gamma*p_pi')
omega=s.symbols('omega',real=True)
# P equation (-Iomega^2+gamma k^2)P-ikomega*pi=0; clockconstraint ikomega*P=0.
matrix=s.Matrix([[gamma*k*k-I*omega*omega,-s.I*k*omega],[s.I*k*omega,0]])
check('covariant longitudinal normalmode determinant',s.simplify(matrix.det()+k*k*omega*omega)==0,str(matrix.det()))
check('fixedclock has a different propagating branch',s.solve(s.Eq(gamma*k*k-I*omega*omega,0),omega)!=[],
      'fixedclockomega^2=gamma k^2/I; variedclockonlyomega0 inthisslowvacuumblock')
result=dict(checks=checks,reduced_H=str(reduced),normalmode_matrix=str(matrix),
            scope='Nonzero-k slowvacuum longitudinalblock; positiveHamiltonian zero-frequency mode, not a ghost/nonlinearwellposedness verdict or fullDiracproof.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
