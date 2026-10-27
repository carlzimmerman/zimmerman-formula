import sympy as s,json
phi,M,xi,lam,r,ms,GN,MB=s.symbols('phi M xi lam r ms GN MB',positive=True)
F=M**2+xi*phi**2
K=M**2*(F+6*xi**2*phi**2)/F**2
logA=s.log(M)-s.log(F)/2
alpha2=s.factor(M**2*s.diff(logA,phi)**2/K)
checks=[]
def check(name,e):
    assert s.simplify(e)==0,name
    checks.append(name)
check('canonical matter coupling',alpha2-xi**2*phi**2/(F+6*xi**2*phi**2))
B=2*alpha2
check('strict one-third bound margin',s.Rational(1,3)-B-F/(3*(F+6*xi**2*phi**2)))
mass2=2*lam*M**4*phi**2/(F*(F+6*xi**2*phi**2))
HE2=M**2*lam*phi**2/(12*xi*F)
check('mass versus cosmological scale',mass2/HE2-24*xi*M**2/(F+6*xi**2*phi**2))
check('coupling-mass identity',mass2/HE2+12*(1+6*xi)*B-24*xi)
q=s.symbols('q',positive=True)
potential=-GN*MB*(1+q*s.exp(-ms*r))/r
force=GN*MB*(1+q*(1+ms*r)*s.exp(-ms*r))/r**2
check('differentiate Yukawa potential',s.diff(potential,r)-force)
check('log slope steeper than inverse square',r*s.diff(force,r)/force+2+q*(ms*r)**2*s.exp(-ms*r)/(1+q*(1+ms*r)*s.exp(-ms*r)))
x=s.symbols('x',nonnegative=True)
check('Yukawa enhancement decreases',s.diff((1+x)*s.exp(-x),x)+x*s.exp(-x))
print(json.dumps({'symbolic_checks':checks,'coupling_squared':str(alpha2),'force_enhancement_bound':'1 <= g/g_tensor < 4/3','radial_logarithmic_slope':'<= -2, for the source-induced linear force','scope':'Weak-source linearization, unscreened point source, r much less than H^-1; homogeneous cosmological acceleration excluded'},indent=2))
