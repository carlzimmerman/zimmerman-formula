import sys,json,math
import sympy as s
Y,l=s.symbols('Y l',positive=True)
mu=1-(1+Y)**(-l);integ=s.diff(mu,l)
assert s.simplify(integ-(1+Y)**(-l)*s.log(1+Y))==0
n=1
ser=s.series(integ,Y,0,3).removeO();primitive=s.integrate(ser,(Y,0,Y))
assert s.simplify(primitive-(Y*Y/2-(2*l+1)*Y**3/6))==0;n+=1
eta=.01;alpha=2.;out=[]
def src(y,ll):
 z=(ll-1)*math.log1p(y)
 return (-math.expm1(-z)-z*math.exp(-z))/(ll-1)**2
for eps in [1e-6,.001,1.]:
 A=alpha/(eps*math.sin(eta));roots=[]
 for yy in [.01,.1,1.,10.,1e3,1e6]:
  def f(delta):return eps*A*math.sin(delta)-alpha*src(yy,2+delta)
  assert f(0)<0 and f(eta)>0;n+=1
  lo,hi=0.,eta
  for _ in range(65):
   mid=(lo+hi)/2
   if f(mid)>0:hi=mid
   else:lo=mid
  d=(lo+hi)/2
  assert 0<d<eta and abs(f(d))<1e-12;n+=1
  roots.append(d)
 assert all(x<y for x,y in zip(roots,roots[1:]));n+=1
 out.append(dict(eps=eps,W_amplitude=A,delta_roots=roots))
assert max(abs(x-y) for row in out[1:] for x,y in zip(out[0]['delta_roots'],row['delta_roots']))<1e-12;n+=1
json.dump(dict(checks=n,eta=eta,controls=out,scope='Bounded restoring-potential countercontrol to kinetic-epsilon-only excursion estimate; not a full halo, stability or kappa derivation'),open(sys.argv[1],'w'),indent=2)
