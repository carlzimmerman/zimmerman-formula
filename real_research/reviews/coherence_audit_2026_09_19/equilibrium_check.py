import sympy as s
r,A,sig,w2 = s.symbols('r A sig w2', positive=True)
xi=s.Function('xi')(r)
rho=A/r**2
drho=-s.diff(r*r*rho*xi,r)/(r*r)
dp=sig*drho
dphi=-2*sig*xi/r**2
full=s.simplify((-s.diff(dp,r)-drho*2*sig/r-rho*dphi)/rho)
old=s.simplify((-s.diff(dp,r)-rho*dphi)/rho)
assert s.simplify(full-(sig*s.diff(xi,r,2)+2*sig*xi/r**2))==0
print('full force per rho:',full)
print('omitted term:',s.simplify(full-old))
for z in [r,r*r]: print('mode',z,'residual:',s.simplify(full.subs(xi,z).doit()))
z=(r-1)*(64-r)/r
q=s.integrate(s.expand(s.diff(z,r)**2-2*z*z/r**2),(r,1,64))
q=s.expand_log(q,force=True)
assert s.simplify(q-(-s.Rational(115605,64)+1560*s.log(2)))==0
print('annulus [1,64] exact energy / sigma^2:',q)
print('using log(2)<=1, energy <=',-s.Rational(115605,64)+1560)
