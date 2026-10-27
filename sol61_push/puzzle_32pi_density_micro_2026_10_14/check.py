import sympy as s,json
n,g,X,m,v,chem,E0=s.symbols('n g X m v chem E0',positive=True)
checks=[]
def ck(name,expr):
    assert s.simplify(expr)==0,(name,expr)
    checks.append(name)
U=g*n**3/3+E0
ne=s.sqrt(X/g)
P=2*X**s.Rational(3,2)/(3*s.sqrt(g))-E0
ck('density stationary equation',(X-s.diff(U,n)).subs(n,ne))
ck('pressure Legendre value',(n*X-U).subs(n,ne)-P)
ck('density from pressure',s.diff(P,X)-ne)
ck('positive compressibility',s.diff(P,X,2)-1/(2*s.sqrt(g*X)))
ck('nonrel internal energy and pressure',(U+2*g*n**3/3-E0)-g*n**3)
nn=s.Function('nn')
xx=chem-v*v/(2*m)
J=nn(xx)*v/m
ck('general static slope',v*s.diff(J,v)/J-(1-v*v*s.diff(nn(X),X).subs(X,xx)/(m*nn(xx))))
z=s.symbols('z',positive=True)
# Negative branch: P(-z)=-2 z^(3/2)/(3sqrt(g))-E0.
Pm=-2*z**s.Rational(3,2)/(3*s.sqrt(g))-E0
ck('negative branch curvature',s.diff(Pm,z,2)+1/(2*s.sqrt(g*z)))
ck('exact convexity witness coordinates',s.Rational(5,8)*(-1)+s.Rational(3,8)*(-9)+4)
ck('exact convexity violation',-8-(s.Rational(5,8)*(-1)+s.Rational(3,8)*(-27))-s.Rational(11,4))
# A shifted energy baseline changes no density equation or stiffness.
shift=s.symbols('shift',real=True)
ck('baseline response invariance',s.diff(U+shift,n)-s.diff(U,n))
print(json.dumps({'checks':checks,'count':len(checks),'scope':'Local equilibrium nonrelativistic density-phase model; density gradient energy neglected; positive compressibility single-component class'},indent=2))
