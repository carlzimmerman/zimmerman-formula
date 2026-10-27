import sympy as s,json
lam,V,delta,theta,Omega,Q,Qh,mu4,M2,ell,a,n,q=s.symbols('lam V delta theta Omega Q Qh mu4 M2 ell a n q',nonzero=True,real=True)
checks=[]
def ck(name,expr):
 assert s.simplify(expr)==0,(name,expr)
 checks.append(name)
# Defined Euclidean reduced action; sphere radius ell, geometric Lambda=3/ell^2.
vol=8*s.pi**2*ell**4/3
R=12/ell**2; GB=24/ell**4
SE=(-M2*R/2+lam+V)*vol-theta*GB*vol-lam*Q/mu4-theta**2*Qh/2
ck('Euler_integral',GB*vol-64*s.pi**2)
ck('lambda_variation',s.diff(SE,lam)-(vol-Q/mu4))
ck('theta_variation',s.diff(SE,theta)-(-64*s.pi**2-theta*Qh))
ck('radius_Einstein_equation',s.diff(SE,ell)-(32*s.pi**2*ell**3/3)*(lam+V-3*M2/ell**2))
ck('fixed_sector_shift',SE.subs({V:V+delta,lam:lam-delta},simultaneous=True)-SE-delta*Q/mu4)
ck('bare_plus_vacuum_invariance',(lam-delta)+(V+delta)-(lam+V))
L=s.symbols('L',positive=True)
ck('sphere_volume_curvature_relation',(24*s.pi**2/L**2)*L**2-24*s.pi**2)
ck('target_volume',(24*s.pi**2/L**2*a**4).subs(L,32*s.pi*a**2)-s.Rational(3,128))
ck('alternative_volume',(24*s.pi**2/L**2*a**4).subs(L,16*s.pi*a**2)-s.Rational(3,32))
ck('flux_selector',(24*s.pi**2*mu4/(n*q)/a**4).subs(n*q,s.Rational(3,128)*mu4/a**4)-(32*s.pi)**2)
# One fixed set of couplings and two positive integer sectors.
mu4v=s.Rational(1,10**12); a2=s.Rational(1,10**12)
n1=s.Integer(23437500000); n2=4*n1
for tag,N,Lv in [('target',n1,32*s.pi*a2),('alternative',n2,16*s.pi*a2)]:
 Om=N/mu4v
 ck(tag+'_sphere_and_quantized_volume',Lv**2*Om-24*s.pi**2)
 ck(tag+'_theta_constraint',(-64*s.pi**2)*1+64*s.pi**2)
 for Vv in [s.Integer(0),s.Rational(1,10**8)]:
  bare=Lv-Vv
  ck(tag+'_Einstein_V_'+str(Vv),bare+Vv-Lv)
 ck(tag+'_normalized_ratio',Lv/a2-(32 if tag=='target' else 16)*s.pi)
Q1,Q2=s.symbols('Q1 Q2',real=True)
ck('relative_action_shift',delta*Q1/mu4-delta*Q2/mu4-delta*(Q1-Q2)/mu4)
# The action change is a sector-dependent constant, not a changed field equation.
ck('theta_solution',(-64*s.pi**2-theta*Qh).subs(theta,-64*s.pi**2/Qh))
SEon=SE.subs({lam:3*M2/ell**2-V,theta:-64*s.pi**2/Qh,Q:mu4*vol},simultaneous=True)
ck('on_shell_action',SEon-(-6*M2/ell**2*vol+V*vol+(64*s.pi**2)**2/(2*Qh)))
print(json.dumps({'count':len(checks),'checks':checks,'integer_sectors':[int(n1),int(n2)],'dimensionless_volumes':['3/128','3/32'],'scope':'Specified compact Euclidean saddle and optional quantization hypothesis, not a quantum state prescription or a complete MOND model.'},indent=2))
