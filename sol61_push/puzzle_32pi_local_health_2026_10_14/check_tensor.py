import sympy as s,json
x,e,n=s.symbols('x eps nu',positive=True)
U=3*x*x+(e+6)*n*(x-1)**2/2
Ux=s.diff(U,x); h2=U/3; fx=1/(4*x**3)
up=(-Ux+24*fx*h2**2)/(e+96*fx**2*h2**2)
ft=1+8*fx*up
formula=(e*x**6+2*U**2-2*Ux*x**3)/(e*x**6+s.Rational(2,3)*U**2)
assert s.factor(ft-formula)==0
value=s.factor(ft.subs({e:0,n:10,x:s.Rational(11,10)}))
assert value==-s.Rational(4419,17161)
finite=s.factor(ft.subs({e:s.Rational(1,10**6),n:10,x:s.Rational(11,10)}))
assert finite<0
slope=s.factor(s.diff(ft,x).subs({e:0,x:1}))
assert slope==-2*n
print(json.dumps({'checks':4,'limit_counterexample':str(value),'positive_eps_counterexample':str(finite),'small_displacement_gradient_slope':str(slope),'scope':'exact initial-rest tensor coefficient after homogeneous constraints'},indent=2))
