import sympy as s,json,math
n,r,C,kappa,Y,L,t=s.symbols('n r C kappa Y L t',positive=True)
HY=kappa*Y**(n-1)
Ybg=C**2/(2*r**2)
Hbg=HY.subs(Y,Ybg)
checks=[]
def check(name,e):
    assert s.simplify(s.expand_power_base(e,force=True))==0,name
    checks.append(name)
flux=r**2*Hbg*C/r
Up=C*(3-2*n)*Hbg/r**2
check('logarithmic profile field equation',s.diff(flux,r)/r**2-Up)
Upp=-2*n*(3-2*n)*Hbg/r**2
check('potential second derivative along profile',s.diff(Up,r)*r/C-Upp)
check('radial kinetic stiffness',(HY+2*Y*s.diff(HY,Y))/HY-(2*n-1))
b=n-s.Rational(3,2)
B=(2*n-1)*b*b-2*n*(3-2*n)
check('stability threshold factorization',B-(2*n-3)*(4*n*n+3)/4)
f=s.sin(s.pi*t/L)
q=s.integrate((2*n-1)*(s.diff(f,t)+b*f)**2-2*n*(3-2*n)*f**2,(t,0,L))
expected=L/2*((2*n-1)*(s.pi/L)**2+B)
check('trial form exact integral',q-expected)
check('canonical limit',expected.subs(n,1)-(s.pi**2/(2*L)-7*L/8))
check('cubic-gradient potential-free case',Up.subs(n,s.Rational(3,2)))
check('cubic-gradient constant flux',flux.subs(n,s.Rational(3,2))-kappa*C*C/s.sqrt(2))
qcouple,M,Ms,a0,E=s.symbols('q M Ms a0 E',positive=True)
C2=s.sqrt(2)*qcouple*Ms/(4*s.pi*kappa*M)
g2=qcouple*qcouple*C2/(M*M*r*r)
G=1/(8*s.pi*M*M)
a0expr=2*s.sqrt(2)*qcouple**3/(kappa*M)
check('source mass normalization',g2-G*Ms*a0expr/r**2)
check('vacuum ratio still independent',E/M**2/a0expr**2-E*kappa**2/(8*qcouple**6))
rows=[]
for nn in [.75,1.,1.25,1.4,1.5,2.]:
    bb=(2*nn-3)*(4*nn*nn+3)/4
    ellcrit=math.pi*math.sqrt((2*nn-1)/(-bb)) if bb<0 else None
    rows.append({'n':nn,'radial_speed_squared':2*nn-1,'long_shell_trial_coefficient':bb,'critical_log_radius_span':ellcrit,'trial_form_at_radius_ratio20':math.log(20)/2*((2*nn-1)*(math.pi/math.log(20))**2+bb)})
print(json.dumps({'symbolic_checks':checks,'parameter_samples':rows,'scope':'Flat spacetime spacelike-gradient power-law scalar family; prescribed logarithmic background, Dirichlet finite shells; no fully coupled gravity or UV completion'},indent=2))
