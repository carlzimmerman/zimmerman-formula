import sympy as s,json
phi=s.symbols('phi',real=True)
M,xi,lam,E=s.symbols('M xi lam E',positive=True)
h=s.symbols('h',nonnegative=True)
z=phi**2;F=M**2+xi*z;D=F+6*xi**2*z
U=M**4*(E+h*z/2+lam*z*z/4)/F**2
W=U+xi*phi*F/D*s.diff(U,phi)
P=E*(M**2+xi*(1+2*xi)*z)+h*z/2*(M**2*(1+2*xi)+xi*(1+4*xi)*z)+lam*z*z/4*(M**2*(1+4*xi)+xi*(1+6*xi)*z)
assert s.factor(W-M**4*P/(F**2*D))==0
assert s.factor(s.diff(P,h)-z/2*(M**2*(1+2*xi)+xi*(1+4*xi)*z))==0
print(json.dumps({'checks':2,'result':'Nonnegative mass-squared preserves positive feedback polynomial for all real phi','limits':'Negative mass-squared is not classified by this positivity proof'},indent=2))
