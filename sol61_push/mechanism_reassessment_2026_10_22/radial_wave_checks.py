import sympy as s
import numpy as np
from scipy.integrate import quad
import json,sys
r=s.symbols('r',positive=True); u=s.Function('u')(r); h=s.Function('h')(r)
B,eta,gamma,w,k,H=s.symbols('B eta gamma omega k H',positive=True)
f=u/r
lap=lambda x:s.diff(x,r,2)+2*s.diff(x,r)/r
original=r*(gamma*lap(lap(f))+eta*w*w*lap(f)-s.diff(r*r*h*s.diff(f,r),r)/r**2-B*w*w*f)
expected=gamma*s.diff(u,r,4)+(eta*w*w-h)*s.diff(u,r,2)-s.diff(h,r)*s.diff(u,r)+(s.diff(h,r)/r-B*w*w)*u
checks={'radial_operator':s.simplify(original-expected)==0}
# Independent Euler variation of the radial quadratic spatial energy.
z0,z1,z2=s.symbols('z0 z1 z2')
energy=(h*(z1-z0/r)**2+gamma*z2**2)/2
sub={z0:u,z1:s.diff(u,r),z2:s.diff(u,r,2)}
euler=s.diff(energy,z0).subs(sub)-s.diff(s.diff(energy,z1).subs(sub),r)+s.diff(s.diff(energy,z2).subs(sub),r,2)
checks['radial_quadratic_form']=s.simplify(euler-(expected-eta*w*w*s.diff(u,r,2)+B*w*w*u))==0
h0=s.symbols('h0',positive=True)
checks['constant_stiffness']=s.simplify(expected.subs(h,h0).doit()-(gamma*s.diff(u,r,4)+(eta*w*w-h0)*s.diff(u,r,2)-B*w*w*u))==0
# For u=e^(ikr) r^(i alpha), derivative ratios obtained recursively.
a=s.symbols('alpha',real=True); D=s.I*k+s.I*a/r
rat=[s.Integer(1)]
for n in range(4):rat.append(s.diff(rat[-1],r)+D*rat[-1])
res=gamma*rat[4]+(eta*w*w-H/r)*rat[2]+H/r**2*rat[1]-H/r**3-B*w*w
constant=gamma*k**4-eta*w*w*k*k-B*w*w
coeff=s.simplify(s.limit(r*(res-constant),r,s.oo))
alpha=-H*k/(2*(2*gamma*k*k-eta*w*w))
mutate='--mutate' in sys.argv
checks['log_phase']=s.simplify(coeff.subs(a,-alpha if mutate else alpha))==0
# Positive k root and group velocity on the asymptotic tail.
b=(2+3*.02798)/.02798; gv=.01; ev=.01/b
rows=[]
for om in [.01,.03,.1,.3,1.]:
    cross=2/(np.sqrt(gv)*om)
    def kval(rad):
        hv=2/rad; z=2*om*om/(hv-ev*om*om+np.sqrt((hv-ev*om*om)**2+4*gv*om*om))
        return np.sqrt(z)
    def group(rad):
        kk=kval(rad); hv=2/rad
        return kk*(hv+2*gv*kk*kk-ev*om*om)/(om*(1+ev*kk*kk))
    grid=np.geomspace(10,cross,300)
    kvals=np.array([kval(t) for t in grid]); groups=np.array([group(t) for t in grid])
    # implicit derivative dk/dr = -h' k/[2(h+2 gamma k²-eta omega²)]
    WKB=np.array([(2/t**2)/(2*kval(t)*(2/t+2*gv*kval(t)**2-ev*om*om)) for t in grid])
    errs=[]
    for t in [10,cross]:
        kk=kval(t); dk=kk*1e-5; hv=2/t
        disp=lambda x:np.sqrt((hv*x*x+gv*x**4)/(1+ev*x*x))
        errs.append(abs((disp(kk+dk)-disp(kk-dk))/(2*dk)/group(t)-1))
    travel=quad(lambda t:1/group(t),10,cross,epsabs=1e-8)[0]
    kv=kval(1e100); al=-2*kv/(2*(2*gv*kv*kv-ev*om*om))
    rows.append(dict(omega=om,crossover_radius=cross,travel_time=travel,travel_angular_cycles=om*travel/(2*np.pi),max_WKB=float(WKB.max()),min_k=float(kvals.min()),min_group=float(groups.min()),group_derivative_error=max(errs),log_phase_coefficient=al))
checks['positive_root']=all(x['min_k']>0 for x in rows)
checks['positive_group']=all(x['min_group']>0 for x in rows)
checks['group_derivative']=all(x['group_derivative_error']<1e-7 for x in rows)
result=dict(checks=checks,all_pass=all(checks.values()),coefficient=str(coeff),alpha=str(alpha),rows=rows,mutated=mutate,scope='radial formal reduced model and idealized 1/r tail; WKB travel is not damping')
with open(sys.argv[1],'w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2));sys.exit(0 if result['all_pass'] else 1)
