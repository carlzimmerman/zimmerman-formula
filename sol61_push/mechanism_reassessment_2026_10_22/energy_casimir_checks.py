import sympy as s
import math,json,sys
q=s.symbols('q',positive=True)
V=-q-s.log(1-q)-q*q/2
checks={'potential_force':s.simplify(s.diff(V,q)-q*q/(1-q))==0,'potential_curvature':s.simplify(s.diff(V,q,2)-q*(2-q)/(1-q)**2)==0}
f,f0,F,A=s.symbols('f f0 F A',real=True)
checks['quadratic_remainder']=s.expand((f*f-f0*f0)/(2*F)-f0*(f-f0)/F-(f-f0)**2/(2*F))==0
checks['occupied_gap']=s.simplify(((f*f-f0*f0)/(2*F)+A*(f-f0)-(f-f0)**2/(2*F)).subs(f0,-F*A))==0
checks['empty_gap']=s.simplify(((f*f-f0*f0)/(2*F)+A*(f-f0)-f*f/(2*F)-A*f).subs(f0,0))==0
E,Ec,L2,ra=s.symbols('E Ec L2 ra',positive=True)
coef=0 if '--mutate' in sys.argv else 1
checks['anisotropic_stationarity']=s.simplify(E+(Ec-E-L2/(2*ra**2))+coef*L2/(2*ra**2)-Ec)==0
x=s.Matrix(s.symbols('x1:4',real=True));v=s.Matrix(s.symbols('v1:4',real=True));b=s.symbols('b',real=True)
ang=x.cross(v);lsq=ang.dot(ang)
der=sum(s.diff(lsq,x[i])*v[i]+s.diff(lsq,v[i])*(-b*x[i]) for i in range(3))
checks['central_L2']=s.simplify(der)==0
checks['liouville']=sum(s.diff(v[i],x[i])+s.diff(-b*x[i],v[i]) for i in range(3))==0
val=lambda z:-z-math.log1p(-z)-z*z/2
prime=lambda z:z*z/(1-z)
vals=[val(z)-val(y)-prime(y)*(z-y) for z in [0,.01,.1,.5,.9,.99] for y in [0,.01,.1,.5,.9,.99]]
checks['field_gap_examples']=min(vals)>=-1e-14
checks={k:bool(v) for k,v in checks.items()}
out=dict(checks=checks,all_pass=all(checks.values()),minimum_sampled_field_gap=min(vals),mutated='--mutate' in sys.argv,scope='algebra for conditional conserved-functional bound; not global PDE existence')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
