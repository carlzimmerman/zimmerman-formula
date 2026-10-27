import sympy as s,json
phi,M,xi,lam,E,z=s.symbols('phi M xi lam E z',positive=True)
h=s.symbols('h',real=True) # h denotes a mass-squared coefficient, not necessarily positive
F=M**2+xi*phi**2
V=E+h*phi**2/2+lam*phi**4/4
U=M**4*V/F**2
D=lam*M**2-xi*h
station=phi*(D*phi**2+h*M**2-4*xi*E)
checks=[]
def check(name,expression):
    assert s.factor(expression)==0,name
    checks.append(name)
check('full constant scalar equation',F*s.diff(V,phi)-2*s.diff(F,phi)*V-station)
check('Einstein potential derivative',s.diff(U,phi)-M**4*station/F**3)
Ebranch=(D*phi**2+h*M**2)/(4*xi)
check('metric and scalar give same Lambda', (V/F).subs(E,Ebranch)-(h+lam*phi**2)/(4*xi))
K=M**2/F+s.Rational(3,2)*M**2*(s.diff(F,phi)/F)**2
check('positive Einstein kinetic form',K-M**2*(F+6*xi**2*phi**2)/F**2)
mass2=2*M**2*phi**2*D/(F*(F+6*xi**2*phi**2))
check('canonical scalar mass with metric mixing',s.diff(U,phi,2).subs(E,Ebranch)/K-mass2)
zbranch=(4*xi*E-h*M**2)/D
ratio=lam/(4*xi)+h/(4*xi*zbranch)
check('vacuum shift sensitivity',s.diff(ratio,E)+h*D/(4*xi*E-h*M**2)**2)
check('quartic branch scale',zbranch.subs(h,0)-4*xi*E/(lam*M**2))
check('quartic branch ratio independent of E',ratio.subs(h,0)-lam/(4*xi))
rows=[]
for hh in [0,s.Rational(1,10)]:
    for ee in [1,2]:
        sub={M:1,xi:1,lam:4,h:hh,E:ee}
        zz=s.factor(zbranch.subs(sub))
        rr=s.factor(ratio.subs(sub))
        rows.append({'mass_squared_coefficient':str(hh),'vacuum_offset':ee,'phi_squared':str(zz),'Lambda_over_phi_squared':str(rr)})
print(json.dumps({'symbolic_checks':checks,'exact_examples':rows,'scope':'Classical constant-field scalar-tensor vacuum and local linear scalar mass; no operational a0 matching or radiative protection'},indent=2))
