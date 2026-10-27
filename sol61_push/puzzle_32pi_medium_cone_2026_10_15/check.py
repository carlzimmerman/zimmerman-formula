import json
import sympy as s
import numpy as np
v,A,b,m,rho,cN,c=s.symbols('v A b m rho cN c', real=True)
K=s.Matrix([[A-b/v,A*v],[A*v,rho+A*v**2]])
G=s.diag(b*v*(1+c**2)/m**2,rho*cN**2)
C=s.diag(b*c/m,0)
Q=K-2*C-G
q=Q.subs(c,1)
assert s.simplify(Q[0,0]-q[0,0]-b*(1-c)*(2*m+v*(1+c))/m**2)==0
assert s.simplify((K+2*C-G)-Q.subs(c,-c))==s.zeros(2)
r=rho*(1-cN**2)
assert s.simplify(q.det()-((A-b/v-2*b/m-2*b*v/m**2)*(r+A*v**2)-A**2*v**2))==0
p=-200*v**4-200*v**3-298*v**2+9702*v-99
assert s.simplify(v*q.det().subs({A:100,b:1,m:1,rho:100,cN:s.Rational(1,10)})-p)==0
assert s.expand(s.diff(p,v,2)+2400*v**2+1200*v+596)==0
roots=s.polys.polytools.intervals(p,eps=s.Rational(1,10**12))
positive=[]
for (lo,hi),multiplicity in roots:
    if lo>0:
        assert multiplicity==1
        assert p.subs(v,lo)*p.subs(v,hi)<0
        positive.append({'lower_exact':str(lo),'upper_exact':str(hi),'approximation':float((lo+hi)/2)})
assert len(positive)==2
rows=[]
for vv in [.0101,.011,.02,.1,1.,2.,3.,3.3,10.]:
    kk=np.array([[100-1/vv,100*vv],[100*vv,100+100*vv**2]])
    assert np.linalg.eigvalsh(kk).min()>0
    maximum=0.;imaginary=0.
    for angle in np.linspace(-1,1,401):
        gg=np.diag([vv*(1+angle**2),1.]);cc=np.diag([angle,0.])
        matrix=np.block([[np.zeros((2,2)),np.eye(2)],[np.linalg.solve(kk,gg),2*np.linalg.solve(kk,cc)]])
        eig=np.linalg.eigvals(matrix)
        maximum=max(maximum,float(abs(eig.real).max()))
        imaginary=max(imaginary,float(abs(eig.imag).max()))
    analytic=float(p.subs(v,vv))>=0
    assert imaginary<1e-9
    assert (maximum<=1)==analytic
    rows.append({'v':vv,'analytic_cone_bound':analytic,'sampled_maximum_absolute_phase_speed':maximum})
print(json.dumps({'exact_symbolic_identities':5,'positive_root_isolation':positive,'samples':rows,'angles_per_sample':401,'claim':'All-direction characteristic normal-speed bound from endpoint PSD; finite eigenvalue grid is cross-check only','non_claim':'No UV causality, microscopic coefficient selection, or global nonlinear stability'},indent=2))
