import sympy as s,json
x,f,A=s.symbols('x f A',positive=True)
e=s.symbols('e',real=True)
V=A*f**4/(e*(e+4))*((x/f)**(e+4)-(e+4)*(x/f)**4/4)
checks=[]
def ck(n,z):
 assert s.simplify(z)==0,(n,z)
 checks.append(n)
v0=s.simplify(V.subs(x,f)); jets=[s.simplify(s.diff(V,x,k).subs(x,f)) for k in range(1,5)]
ck('stationary',jets[0]);ck('energy',v0+A*f**4/(4*(e+4)))
ck('mass',jets[1]-A*f**2);ck('cubic',jets[2]-A*f*(e+5));ck('quartic',jets[3]-A*(e*e+6*e+11))
R=s.factor(-v0*jets[2]**2/jets[1]**3);S=s.factor(jets[3]*jets[1]/jets[2]**2)
ck('energy_ratio',R-(e+5)**2/(4*(e+4)))
ck('shape_ratio',S-(e*e+6*e+11)/(e+5)**2)
ck('unitarity_shape_gap',1-S-(4*e+14)/(e+5)**2)
ck('CW_limit',s.limit(V,e,0)-A*x**4/4*(s.log(x/f)-s.Rational(1,4)))
ck('CW_energy_ratio',s.limit(R,e,0)-s.Rational(25,16))
ck('CW_shape_ratio',s.limit(S,e,0)-s.Rational(11,25))
Rvar=s.symbols('R',real=True)
res=s.resultant(e*e+18*e+53,(e+5)**2-4*Rvar*(e+4),e)
ck('joint_elimination',res+16*(3*Rvar**2+2*Rvar-9))
roots=s.solve((e+5)**2-256*s.pi*(e+4),e)
shapeRoots=s.solve(e*e+18*e+53,e)
# Two sectors with an independently adjustable spectator vacuum energy can fit R,
# but cannot change the shape of this one-field potential.
print(json.dumps({'count':len(checks),'checks':checks,'energy_target_roots':[{'epsilon':float(v),'Delta':float(v+4),'shape_ratio':float(S.subs(e,v))} for v in roots],'shape_target_roots':[{'epsilon':float(v),'Delta':float(v+4),'energy_ratio':float(R.subs(e,v))} for v in shapeRoots],'scope':'Single-deformation leading potential with linear polarization dictionary. No full gravity or multi-field exclusion.'},indent=2))
