import sympy as s,json
phi,M,xi,lam,v,r=s.symbols('phi M xi lam v r',positive=True)
F=M**2+xi*phi**2
E=lam*M**2*v**2/(4*xi)
U=M**4*(E+lam*phi**4/4)/F**2
K=M**2*(F+6*xi**2*phi**2)/F**2
f=xi*phi/s.sqrt(F+6*xi**2*phi**2)
checks=[]
def check(name,e):
    assert s.simplify(e)==0,name
    checks.append(name)
check('nonlinear potential derivative sign factor',s.diff(U,phi)-lam*M**6*phi*(phi**2-v**2)/F**3)
check('coupling increases with phi',s.diff(f,phi)-xi*M**2/(F+6*xi**2*phi**2)**s.Rational(3,2))
Q=s.Function('Q')(r);ff=s.Function('f')(r)
g=ff*Q/(M*r**2)
check('force envelope derivative',s.diff(r**2*g,r)-(s.diff(ff,r)*Q+ff*s.diff(Q,r))/M)
check('force logarithmic slope',r*s.diff(g,r)/g+2-r*s.diff(ff,r)/ff-r*s.diff(Q,r)/Q)
A=s.Function('A')(r)
w=r*s.diff(A,r)/A
# Exact circular geodesic speed in the conformally Minkowski diagnostic.
check('conformal circular-speed expression',s.diff(A**2,r)/(A**2)*A**2*r**2/s.diff(A**2*r**2,r)-w/(1+w))
print(json.dumps({'symbolic_checks':checks,'scope':'Nonlinear scalar exterior on flat Einstein-frame annulus with positive branch and vacuum outer boundary; controlled weak-metric interpretation only','non_claims':['No existence theorem for the boundary value problem','No full nonlinear Einstein solution','No general Jordan-frame no-go for large conformal potentials']},indent=2))
