"""State-independent NR charge, local-flow and portal-force identities."""
import math,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
p=Path(__file__).parent
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
# Dimensionless hbar=m=1. Conversion vertex gamma(B* A^2+c.c.).
for A,B in [(1+.3j,.2-.7j),(.01+2j,-1+.4j),(3-2j,.5+.9j)]:
 gamma=.37;dA=-2j*gamma*B*A.conjugate();dB=-1j*gamma*A*A
 dn1=2*(A.conjugate()*dA).real;dn2=2*(B.conjugate()*dB).real
 check('pointwise conversion charge conservation',abs(dn1+2*dn2)<1e-13)
 for theta in [.1,1.,2.5]:
  r1=np.exp(-1j*theta);r2=np.exp(-2j*theta)
  check('conversion vector field phase covariance',abs(-2j*gamma*(r2*B)*(r1*A).conjugate()-r1*dA)<1e-13 and abs(-1j*gamma*(r1*A)**2-r2*dB)<1e-13)
  check('local conversion interaction invariant',abs((r2*B).conjugate()*(r1*A)**2-B.conjugate()*A*A)<1e-13)
# Exact portal momentum force, arbitrary fractions and common U'' grad S.
for n1,n2 in [(F(1),F(0)),(F(0),F(1)),(F(3,5),F(1,5))]:
 m=F(3,2);S=(n1+2*n2)/(2*m);Upp_gradS=F(2,7)
 force=-n1*Upp_gradS/(2*m)-n2*Upp_gradS/m
 check('portal force equals minus pressure gradient',force==-S*Upp_gradS)
# Cold two-fluid density acceleration matrix, with total restoring coefficient Ck2.
rows=[]
for f in [0.,.1,.3638167932,.5,.9,1.]:
 matrix=np.array([[1-f,f],[1-f,f]])*2.3
 ev=np.sort(np.linalg.eigvals(matrix).real)
 check('composition-independent cold density mode',np.max(abs(ev-[0.,2.3]))<1e-14)
 rows.append(dict(source_mass_fraction=f,eigenvalues=ev.tolist()))
# Independent analytic spatial profile checks P'(S)=S U''(S).
for s in [.01,.1,1.,10.,100.]:
 h=s*1e-4
 pressure=lambda x:1-1/math.hypot(1,x)
 fd=(pressure(s+h)-pressure(s-h))/(2*h)
 expected=s/(1+s*s)**1.5
 check('portal pressure chain rule',abs(fd/expected-1)<2e-7)
out=dict(all_pass=all(v['passed'] for v in checks),checks=checks,cold_two_fluid_rows=rows,
 non_claims=['Leading NR masses m and 2m; full relativistic density normalization differs',
 'Exact local portal-force identity is not a coarse-grained closure',
 'Cold two-fluid eigenvalues omit velocity dispersion, quantum stress and conversion pressure',
 'No evolving mixture, halo selector or acceleration normalization solved'])
(p/'portal_mixture_identity_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
