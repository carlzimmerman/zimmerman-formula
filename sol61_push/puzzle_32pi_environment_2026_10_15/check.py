import sympy as s,json
phi=s.symbols('phi',real=True)
M,xi,lam,E=s.symbols('M xi lam E',positive=True)
F=M**2+xi*phi**2
D=F+6*xi**2*phi**2
K=M**2*D/F**2
U=M**4*(E+lam*phi**4/4)/F**2
f=xi*phi/s.sqrt(D)
checks=[]
def check(name,v):
    assert s.simplify(v)==0,name
    checks.append(name)
fchi=xi*M*F/D**2
check('canonical derivative positive for either field sign',s.diff(f,phi)/s.sqrt(K)-fchi)
W=U+M*f*s.diff(U,phi)/s.sqrt(K)
P=E*(M**2+xi*(1+2*xi)*phi**2)+lam*phi**4/4*(M**2*(1+4*xi)+xi*(1+6*xi)*phi**2)
check('potential plus matter feedback positive polynomial',W-M**4*P/(F**2*D))
x,e=s.symbols('x e',positive=True)
p=e*(1+(1+2*xi)*x)+x**2*(1+4*xi+(1+6*xi)*x)
d=1+(1+6*xi)*x
c=p/((e+x*x)*d)
check('dimensionless independent derivative check',c-1-2*xi*x*(1+x)/d*(2*x/(e+x*x)-2/(1+x)))
check('rejected candidate actual sign',c.subs({xi:s.Rational(1,10),x:1,e:10})-s.Rational(125,143))
# No dividing by f: valid also at phi=0.
r,N,cp=s.symbols('r N cp',positive=True)
a,w,S,u=s.symbols('a w S u',real=True)
T=r**2*fchi*cp**2/M+r**2*W/(M**2*N)
check('combination of potential and charge source',T-(r**2*fchi*cp**2/M+r**2*f*s.diff(U,phi)/(M*N*s.sqrt(K))+r**2*U/(M**2*N)))
print(json.dumps({'symbolic_checks':checks,'positive_polynomial':str(P),'candidate_feedback_exact':'125/143','scope':'Exact algebra supporting static spherical no-flat-interval result for this action, with arbitrary scalar boundary values','non_claims':['No general scalar-tensor no-go','No exclusion of all approximate plateaus in strong geometry','No coefficient selection']},indent=2))
