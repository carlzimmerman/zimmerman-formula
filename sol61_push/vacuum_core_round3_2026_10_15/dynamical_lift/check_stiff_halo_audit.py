#!/usr/bin/env python3
"""Independent mass integration and reconstruction of the supplied certificate."""
import hashlib
import json
from pathlib import Path
import sys
import sympy as s

root=Path(__file__).resolve().parents[3]
b=root/'sol61_push/vacuum_core_round3_2026_10_15/stiff_halo'
old=json.loads((b/'run_v1/results.json').read_text())
r,t=s.symbols('r t',nonnegative=True)
rho0=s.Rational(105,776)/s.pi
rho=rho0*(1-r*r)*(1+s.Rational(9,10)*r*r)
m=s.integrate(4*s.pi*t*t*rho.subs(r,t),(t,0,r))
u=m/r**2
k=s.Rational(101,50958); gamma=k/rho0
Fmatter=u*u/(1-u)
gb=Fmatter-gamma*s.diff(rho,r)
mb=r*r*gb
q=s.cancel((1-u)**2*s.diff(mb,r)/r**2)
checks=[]
def exact(name,expr):
    z=s.factor(expr)
    assert z==0,(name,z)
    checks.append(name)
exact('independent density-integral mass',m-r**3*(350-21*r*r-135*r**4)/1940)
exact('independent source from full force equation',gb-(u*u/(1-u)+k*(r/s.Integer(5)+s.Rational(18,5)*r**3)))
exact('actual cold inventory',m.subs(r,1)-s.Rational(1,10))
exact('actual baryon inventory',mb.subs(r,1)-s.Rational(25,1341))
exact('ratio of actual counted inventories',m.subs(r,1)/mb.subs(r,1)-s.Rational(1341,250))
cert=old['bernstein_partition']; assert len(cert)==1 and cert[0]['left']=='0' and cert[0]['right']=='1'
coeff=[s.Rational(v) for v in cert[0]['coefficients']]
assert len(coeff)==15 and all(v>0 for v in coeff)
reconstructed=sum(c*s.binomial(14,i)*r**i*(1-r)**(14-i) for i,c in enumerate(coeff))
exact('source polynomial reconstructed from the stored Bernstein certificate',q-reconstructed)
assert min(coeff)==s.Rational(101,84930)
checks.append('all 15 reconstructed Bernstein coefficients positive with exact stated minimum')
P=m/(4*s.pi*r*r); Pout=s.Rational(1,10)/(4*s.pi*r*r)
exact('Gauss at all occupied radii',s.diff(r*r*P,r)/r**2-rho)
exact('continuous edge flux',P.subs(r,1)-Pout.subs(r,1))
exact('continuous normal derivative at edge',s.diff(P,r).subs(r,1)-s.diff(Pout,r).subs(r,1))
exact('zero Hodge boundary term at center',s.limit(r*P*P,r,0))
exact('zero Hodge boundary term at infinity',s.limit(r*Pout*Pout,r,s.oo))
Fout=(s.Rational(1,10)/r**2)**2/(1-s.Rational(1,10)/r**2)-s.Rational(25,1341)/r**2
exact('negative exterior force at boundary',Fout.subs(r,1)+s.Rational(101,13410))
exact('outside force-envelope derivative has negative sign',s.diff(r*r*Fout,r)+2*s.Rational(1,100)*r/(r*r-s.Rational(1,10))**2)
exact('occupied chemical-potential gradient vanishes',-(Fmatter-gb)+gamma*s.diff(rho,r))
exact('finite positive central baryon density',s.limit(s.diff(mb,r)/(4*s.pi*r*r),r,0)-k/(20*s.pi))
expected={
 'PROOF.md':'db363953a1199748c668e71c65911db17992c7e7868f6591bfc36fe43f7e01ca',
 'check_stiff_halo.py':'8e1ad0c4d22564dc1dfec95d9a668ae0d18ac570b6766cb4052b0602ccec767b',
 'run_v1/results.json':'306b90af861818289edded99eb0ed17c1290c58fc9a1730745f6a3e590f7ece0'}
for rel,h in expected.items():
 assert hashlib.sha256((b/rel).read_bytes()).hexdigest()==h
checks.append('audited proof, code and raw-result hashes unchanged')
Path(sys.argv[1]).write_text(json.dumps({'exact_check_count':len(checks),'exact_checks':checks,'certificate_coefficient_count':len(coeff),'minimum_certificate_coefficient':str(min(coeff)),'scope':'counted NR electrostatic/current model with fixed inverse-constructed baryon source; no relativistic interface theorem'},indent=2)+'\n')
print(str(len(checks))+' independent integration, force, interface and certificate checks passed.')
