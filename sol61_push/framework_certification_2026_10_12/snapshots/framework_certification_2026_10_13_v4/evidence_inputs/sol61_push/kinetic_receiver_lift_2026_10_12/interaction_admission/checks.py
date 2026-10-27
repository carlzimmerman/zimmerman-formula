"""Exact source-only interaction obligations, not a microscopic derivation."""
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
checks=[]
def check(name,assertion):
    assert assertion,name
    checks.append({'name':name,'passed':True})

P1,P2,g1,g2,D,p,gamma,R=s.symbols('P1 P2 g1 g2 D p gamma R',real=True)
h=P2*g1-P1*g2
r=s.Matrix([D*g2+p*P2,-D*g1-p*P1])
J=gamma*h*h*R;S=gamma*h*r*R
reverse={P1:-P1,P2:-P2,p:-p}
JT=J.subs(reverse,simultaneous=True)
ST=S.subs(reverse,simultaneous=True)
check('time reversal rate is even, rather than required odd',s.expand(JT-J)==0)
check('time reversal receiver source is odd, rather than required even',
      all(s.expand(x)==0 for x in ST+S))
fixture={P1:1,P2:0,g1:0,g2:1,D:1,p:0,gamma:1,R:1}
check('nonzero reversed-equation discrepancy',
      J.subs(fixture)==1 and S.subs(fixture)==s.Matrix([-1,0]) and
      (JT+J).subs(fixture)==2 and (ST-S).subs(fixture)==s.Matrix([2,0]))

# Literal real/imaginary components of the complex carrier fields.
# u=qdot is velocity; canonical momentum is 2u, not u.
q=s.Matrix(s.symbols('q1:5',real=True))
u=s.Matrix(s.symbols('u1:5',real=True))
acc=s.Matrix(s.symbols('source1:5',real=True))
def ell(z):return s.Matrix([-z[1],z[0],-2*z[3],2*z[2]])
Q=-2*ell(q).dot(u)  # i(phi*dotphi-phi dotphi*) + twice chi current
Qdot=sum(s.diff(Q,q[i])*u[i]+s.diff(Q,u[i])*acc[i] for i in range(4))
check('original-normalization charge acceleration source',
      s.expand(Qdot+2*ell(q).dot(acc))==0)

# A rows u,Gx,Gy,Gz; D,p below are one half of physical cold costs.
# Alternatively rows 2u,2G give the same physical equations without rescaling t.
A=s.Matrix(4,4,s.symbols('a0:16',real=True))
target=s.Matrix(s.symbols('target0:4',real=True))
extent=s.symbols('extent',real=True)
adj=A.adjugate();det=A.det()
residual=(adj*A-det*s.eye(4)).applyfunc(s.expand)
dual_residual=(A*adj-det*s.eye(4)).applyfunc(s.expand)
check('full-rank compatibility and source inverse identities',
      residual==s.zeros(4) and dual_residual==s.zeros(4))

ell0=ell(s.Matrix([1,0,0,0]));A0=s.eye(4)
badtarget=s.Matrix([0,1,0,0]);badsource=A0.inv()*badtarget
check('energy-momentum balance alone misses charge, omission mutation detected',
      A0*badsource==badtarget and ell0.dot(badsource)==1)
goodtarget=s.Matrix([1,0,0,0]);goodsource=A0.inv()*goodtarget
check('compatible full-rank neutral source exists',
      A0*goodsource==goodtarget and ell0.dot(goodsource)==0)
check('source-sign mutation detected',A0*(-badsource)!=badtarget)

result={'checks':checks,'passed':len(checks),'failures':0,
        'normalization':'q literal real/imag components, u=qdot, canonical momentum=2u; A rows u,G and target costs physical/2; charge source=-2 ell(q).s',
        'time_reversal_scope':'Standard neutral real fields with reversed velocities; no coarse-graining or extra variables included',
        'compatibility':'det(A)!=0 implies neutral solution iff ell.adj(A).target*J=0; source=adj(A).target*J/det(A)',
        'non_claims':['No new derived coupling or rate','No universal action no-go','No cold f / underlying phi identification','No target profile or gravity completion']}
(HERE/'run/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
