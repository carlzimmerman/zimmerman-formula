import sympy as s, json
H,M,b,p,F,z,e,A=s.symbols('H M b p F z e A',positive=True)
d,v,n=s.symbols('d v n',real=True)
U,U1,U2=s.symbols('U U1 U2',real=True)
checks=[]
def ck(name,expr):
    assert s.simplify(expr)==0,(name,s.simplify(expr))
    checks.append(name)
# Signature -+++, R_deS=12H^2. M denotes M_Pl^2.
# Spatially flat gauge, lapse=1+n. WZ cubic/quartic terms do not contribute here.
N=1+n
L=-3*M*H**2/N+v*v/(2*N)-N*(U+U1*d+U2*d*d/2)-8*b*v*H**3/((p+d)*N**3)-12*b*H**2*v*v/((p+d)**2*N**3)
K=s.hessian(L,(d,v,n)).subs({d:0,v:0,n:0,U1:24*b*H**4/p})
E=s.simplify(K[:2,:2]-K[:2,2:3]*K[2:3,:2]/K[2,2])
D=1-24*b*H**2/p**2+96*b*b*H**4/(M*p*p)
mass=U2+24*b*H**4/p**2-384*b*b*H**6/(M*p*p)
ck('lapse eliminated kinetic',E[1,1]-D)
ck('integrated mixed term mass',-E[0,0]+3*H*E[0,1]-mass)
subs={H:s.sqrt(M*z/(4*b)),p:F*s.sqrt(z),U2:(2+4*z)*3*M*M*z/(4*b*F*F)}
Ds=s.simplify(D.subs(subs).subs(F*F,e*M))
Ns=s.simplify(mass.subs(subs).subs(F*F,e*M))
ck('WZ kinetic on branch',Ds-(e-6+6*z)/e)
ck('WZ mass on branch',Ns-3*M*z*(1-z)/(b*e))
ck('physical squared mass ratio',Ns/Ds/(M*z/(4*b))-12*(1-z)/(e-6+6*z))
ck('continuously variable healthy family',Ds.subs({e:12,z:s.Rational(1,2)})-s.Rational(3,4))
ck('family mass ratio',(12*(1-z)/(e-6+6*z)).subs({e:12,z:s.Rational(1,2)})-s.Rational(2,3))
ck('anomaly normalization', (3/(4*(A/(16*s.pi**2))*e)).subs(e,3*s.pi/(8*A))-32*s.pi)
q=s.symbols('q',positive=True)
ck('Planck ratio health polynomial', (Ds.subs(z,q/e)*e**2)-(e*e-6*e+6*q))
xi=s.symbols('xi',real=True)
B=M-xi*p*p
hh=p*p/(4*b)*(B/F**2+2*xi)
ck('nonminimal vacuum equation', (2*p*(3*B*hh)/F**2+12*xi*p*hh-24*b*hh**2/p))
ck('nonminimal changed ratio', 3*hh/p**2-3/(4*b)*(M/F**2+xi*(2-p*p/F**2)))
print(json.dumps({'count':len(checks),'checks':checks,'scope':'Declared WZ-completed minimal action; homogeneous lapse-eliminated quadratic sector only',
 'examples':[{'Delta_a':float(av),'epsilon_at_target':float(3*s.pi/(8*av)), 'z_lower_bound':float(1-s.pi/(16*av)), 'phi_squared_over_M_squared_lower_bound':float(3*s.pi/(8*av)-(3*s.pi/(8*av))**2/6)} for av in [s.Rational(1,4),s.Rational(3,4)]]},indent=2))
