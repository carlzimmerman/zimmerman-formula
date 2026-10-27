import sympy as s,json,math
v,psi,psi0,B,h,ss=s.symbols('v psi psi0 B h ss',positive=True)
# h>0 is the stiffness of the auxiliary field, not a scalar mass squared in a covariant action.
E=B*v**3/psi+h*(psi-psi0)**2/2
checks=[]
def check(name,e):
    assert s.factor(e)==0,name
    checks.append(name)
check('auxiliary stationarity',s.diff(E,psi)-(h*(psi-psi0)-B*v**3/psi**2))
branch={B:v**(-3)*h*(psi-psi0)*psi**2}
J=s.diff(E,v)
Epp=s.diff(E,psi,2)
relaxed=s.diff(E,v,2)-s.diff(E,v,psi)**2/Epp
check('positive auxiliary stiffness',Epp.subs(branch)-h*(3-2*psi0/psi))
check('relaxed slope factor',s.factor((v*relaxed/J).subs(branch))-(3*psi-psi0)/(3*psi-2*psi0))
check('all-gradient speed bound numerator',ss*(3*ss-2)**3-(ss-1)*(3*ss-1)**3-(2*ss-1))
# Parameterize interpolation by mu in [0,1).
mu=s.symbols('mu',positive=True)
t=mu/(1-mu**3);sc=1/(1-mu**3)
check('implicit interpolating relation',sc**2*(sc-1)-t**3)
check('speed expression from elimination',(t/sc)*(3*sc-1)/(3*sc-2)-mu*(2+mu**3)/(1+2*mu**3))
check('direct radial subunit factor',1-mu*(2+mu**3)/(1+2*mu**3)-(1-mu)**3*(1+mu)/(1+2*mu**3))
check('absolute force residual',t*(1-mu)-mu/(1+mu+mu**2))
check('limiting residual',s.limit(t*(1-mu),mu,1,dir='-')-s.Rational(1,3))
check('unrelaxed stiffness',s.diff(E,v,2)/(J/v)-2)
check('deficit derivative in mu',s.diff(mu/(1+mu+mu**2),mu)-(1-mu**2)/(1+mu+mu**2)**2)
# The time kinetic K0=3 B^(2/3) h^(1/3), choosing preferred-frame limiting speed1.
rows=[]
for mm in [.001,.01,.1,.5,.9,.99,.999]:
    tt=mm/(1-mm**3)
    p=(2+mm**3)/(1+2*mm**3)
    rows.append({'mu':mm,'gradient_over_transition':tt,'radial_speed_squared':mm*p,'transverse_speed_squared':mm,'log_flux_slope':p})
print(json.dumps({'symbolic_checks':checks,'samples':rows,'scope':'Auxiliary field eliminated algebraically in an explicitly preferred-frame scalar theory; no dynamical aether or relativistic completion','non_claims':['No originality claim','No zero-gradient strong-coupling resolution','No solar-system fit','No32pi selection']},indent=2))
