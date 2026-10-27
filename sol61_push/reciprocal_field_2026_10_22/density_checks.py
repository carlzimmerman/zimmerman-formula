import argparse,json
from pathlib import Path
import sympy as s
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--mutate',action='store_true');args=pa.parse_args()
x,rho0,g0,chi,V=s.symbols('x rho0 g0 chi V',positive=True);y=s.symbols('y',real=True)
p,n=s.symbols('p n',real=True)
r=s.sqrt(x*x+y*y);rho=rho0*r**(-n);gg=g0*s.sqrt(rho)
vb=s.Matrix([-V*y*r**(p-1),V*x*r**(p-1)])
omega=s.diff(vb[1],x)-s.diff(vb[0],y)
Xz=gg*omega/chi
Q=s.Matrix([s.diff(gg*Xz,y)/rho,-s.diff(gg*Xz,x)/rho]);mom=vb+Q
coords=[x,y]
lie=sum(vb[j]*s.diff(mom[0],coords[j])+mom[j]*s.diff(vb[j],x) for j in range(2))
chem=gg*Xz*omega/(2*rho)
if args.mutate:chem=s.Integer(0)
force=s.simplify((s.diff(vb.dot(vb)/2+chem,x)-lie).subs(y,0))
expected=V*V*x**(2*p-1)*(1+g0*g0*(n-2*p)*(1-p*p)/(chi*x*x))
checks=[]
def ck(name,ok,value):
    checks.append(dict(name=name,passed=bool(ok),value=str(value)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(value))
ck('full_material_force',s.simplify(force-expected)==0,force)
ck('flat_force',s.simplify(force.subs(p,0)-(V*V/x)*(1+n*g0*g0/(chi*x*x)))==0,s.simplify(force.subs(p,0)))
ck('rigid_force',s.simplify(force.subs(p,1)-V*V*x)==0,s.simplify(force.subs(p,1)))
ck('zero_vorticity_force',s.simplify(force.subs(p,-1)-V*V/x**3)==0,s.simplify(force.subs(p,-1)))
ck('constant_density_force',s.simplify(force.subs(n,0)-V*V*x**(2*p-1)*(1-2*p*(1-p*p)*g0*g0/(chi*x*x)))==0,s.simplify(force.subs(n,0)))
rr,alpha=s.symbols('rr alpha',positive=True)
feedback=g0*g0*rr**(2*alpha-1)
ck('uniform_density_speed_power',s.solve(s.Eq(2*alpha-1,0),alpha)==[s.Rational(1,2)],feedback)
ck('density_independent_speed',s.simplify(feedback.subs(alpha,s.Rational(1,2))-g0*g0)==0,g0*g0)
res=dict(status='checks_passed' if all(c['passed'] for c in checks) else 'checks_failed',checks=checks,
         non_claims=['No full nonlinear field stability','No observed rotation-curve test','No pressure-system selector'])
path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(res,indent=2)+'\n')
print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)}")
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
