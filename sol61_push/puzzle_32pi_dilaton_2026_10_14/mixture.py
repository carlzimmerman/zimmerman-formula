import sympy as s,json
D,mu=s.symbols('D mu',real=True)
checks=[]
def ck(n,z):
 assert s.simplify(z)==0,(n,z)
 checks.append(n)
ck('dimension_second_moment_chord',5*D-4-D**2-(D-1)*(4-D))
ck('inverse_dimension_chord',(5-D)/4-1/D-(D-1)*(4-D)/(4*D))
ck('shape_bound_square',9*(mu+1)**2-16*(3*mu-1)-(3*mu-5)**2)
ck('energy_bound_factor',32-(mu+1)**2*(5-mu)-(mu-3)**2*(mu+3))
w=s.symbols('w',real=True)
mean=1+3*w;second=1+15*w;inv=1-s.Rational(3,4)*w
R=inv*(mean+1)**2/4;S=(second-2*mean+3)/(mean+1)**2
ck('sharp_energy',R.subs(w,s.Rational(2,3))-2)
ck('sharp_shape',S.subs(w,s.Rational(2,9))-s.Rational(9,16))
print(json.dumps({'count':len(checks),'checks':checks,'scope':'Arbitrary finite positive mixture, common minimum f, individual scalar dimensions in [1,4]. Bounds use moment inequalities; no parameter scan.'},indent=2))
