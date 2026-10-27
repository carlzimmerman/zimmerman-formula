import sympy as s,json
r,C,kap,mu,S,K,k=s.symbols('r C kap mu S K k',positive=True)
checks=[]
def ck(name,expr):
    assert s.simplify(expr)==0,(name,s.simplify(expr))
    checks.append(name)
A=-mu**2/(2*kap*S**2)
B=-A*A/(2*C)
g=C/r+A/r**2+B/r**3
flux=2*kap*r*r*g*g/mu**2-r*r*(s.diff(g,r,2)+2*s.diff(g,r)/r-2*g/r**2)/S**2
Q=2*kap*C*C/mu**2
t=s.symbols('t',positive=True)
res=s.expand((flux-Q).subs(r,1/t))
ck('large radius flux order one',res.coeff(t,1))
ck('large radius flux order two',res.coeff(t,2))
ck('leading large radius force',s.limit(r*g,r,s.oo)-C)
ck('Laplacian squared log profile',s.diff(C/r,r,2)+2*s.diff(C/r,r)/r-2*(C/r)/r**2+2*C/r**3)
sx,sy,sz=s.symbols('sx sy sz',real=True)
v=s.symbols('v',positive=True)
energy=2*kap*(sx*sx+sy*sy+sz*sz)**s.Rational(3,2)/(3*mu**2)
hes=s.hessian(energy,(sx,sy,sz)).subs({sx:v,sy:0,sz:0})
ck('radial stiffness',hes[0,0]-4*kap*v/mu**2)
ck('transverse stiffness',hes[1,1]-2*kap*v/mu**2)
ck('vacuum dispersion',(k*k/(s.sqrt(K)*S))**2-k**4/(K*S*S))
alpha,M,ms=s.symbols('alpha M ms',positive=True)
C2=alpha*ms*mu**2/(8*s.pi*kap*M)
a0=alpha**3*mu**2/(kap*M)
ck('emergent MOND coefficient',alpha**2*C2/M**2-a0*ms/(8*s.pi*M*M))
lam=s.symbols('lam',positive=True)
ck('unselected ratio',(lam*mu**4/M**2)/a0**2-lam*kap**2/alpha**6)
print(json.dumps({'count':len(checks),'checks':checks,'flux_remainder':str(s.factor(res)),
 'scope':'Fixed preferred frame scalar theory; formal large-radius expansion, not global boundary-value existence'},indent=2))
