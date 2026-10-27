import sympy as s,json,sys
from pathlib import Path
C,a0,g,u=s.symbols('C a0 g u',positive=True);checks=[]
def eq(n,a,b=0):
 d=s.simplify(a-b);assert d==0,(n,d);checks.append(n)
def positive(n,a):
 assert s.simplify(a).is_positive is True,(n,a);checks.append(n)
W=-a0/C*(u+a0*s.log(1-u/a0));U=W-u*u/(2*C)
Lraw=-g*g/(2*C)+u*g/C-W
Lcrit=-(g-u)**2/(2*C)-U
Lbad=-(g-u)**2/(2*C)-W
eq('actual_totalpotential_P_derivative',C*s.diff(W,u),u/(1-u/a0))
eq('actual_totalpotential_P_curvature',C*C*s.diff(W,u,2),C*a0*a0/(a0-u)**2)
eq('correct_raw_and_square_actions_identical',Lraw,Lcrit)
eq('naive_total_in_square_adds_quadratic',Lbad-Lraw,-u*u/(2*C))
eq('actual_correct_P_Euler',C*s.diff(Lcrit,u),g-u/(1-u/a0))
eq('actual_naive_P_Euler',C*s.diff(Lbad,u),g-u-u/(1-u/a0))
usol=a0*g/(a0+g)
eq('claimed_stationary_saturation',s.diff(Lcrit,u).subs(u,usol))
eq('claimed_Newton_relation',g-usol,g*g/(g+a0))
gn=s.symbols('gn',positive=True);ubad=a0*gn/(a0+gn)
eq('naive_branch_stationarity',s.diff(Lbad,u).subs({u:ubad,g:gn+ubad}))
eq('naive_deep_linear_not_square_root',s.limit((gn+ubad)/gn,gn,0,dir='+'),2)
# Derive the actual gravitational constraint from critical L, treating W independently.
r,x,y,z,R,w,gamma,p0=s.symbols('r x y z R w gamma p0',positive=True)
Phi=s.Function('Phi')(x,y,z);Ps=[s.Function('P'+str(i))(x,y,z) for i in range(3)];rho=s.symbols('rho',real=True)
L=-sum((s.diff(Phi,c)-C*Ps[i])**2 for i,c in enumerate((x,y,z)))/(2*C)-rho*Phi
EL=s.diff(L,Phi)-sum(s.diff(s.diff(L,s.diff(Phi,c)),c) for c in (x,y,z))
expected=sum(s.diff(Phi,c,2) for c in (x,y,z))/C-rho-sum(s.diff(Ps[i],c) for i,c in enumerate((x,y,z)))
eq('actual_gravity_source_is_divP',EL,expected)
p=s.Function('p')(r);div=s.diff(r*r*p,r)/(r*r)
eq('actual_radial_divergence',div,s.diff(p,r)+2*p/r)
# Vector radial Laplacian; componentwise derivative at an axis, obtained from actual 3D field.
rad=s.sqrt(x*x+y*y+z*z);f=s.Function('f');Pvec=[f(rad)*c/rad for c in (x,y,z)]
axis=sum(s.diff(Pvec[0],c,2) for c in (x,y,z)).subs({x:r,y:0,z:0}).doit()
eq('actual_vector_radial_laplacian',axis,s.diff(f(r),r,2)+2*s.diff(f(r),r)/r-2*f(r)/r**2)
ramp=p0*(R+w-r)/w
shellmass=4*s.pi*s.integrate(s.diff(r*r*ramp,r),(r,R,R+w))
eq('continuous_ramp_boundary_charge',shellmass,-4*s.pi*R*R*p0)
E=2*s.pi*gamma*s.integrate(r*r*s.diff(ramp,r)**2+2*ramp*ramp,(r,R,R+w))
eq('actual_affine_ramp_stiffness_energy',E,2*s.pi*gamma*p0*p0*(R*R/w+R+w))
eq('thin_ramp_divergence_coefficient',s.limit(w*E,w,0,dir='+'),2*s.pi*gamma*p0*p0*R*R)
assert s.limit(E,w,0,dir='+')==s.oo;checks.append('thin_ramp_energy_unbounded')
eq('zero_amplitude_no_shell_charge',shellmass.subs(p0,0))
eq('zero_amplitude_no_stiffness_cost',E.subs(p0,0))
tail=p0*R*R/r**2
eq('retained_tail_divergence_zero',(s.diff(p,r)+2*p/r).subs({s.diff(p,r):s.diff(tail,r),p:tail}))
eq('retained_tail_vector_laplacian_zero',s.diff(tail,r,2)+2*s.diff(tail,r)/r-2*tail/r**2)
eq('retained_tail_stiffness_finite',2*s.pi*gamma*s.integrate(r*r*s.diff(tail,r)**2+2*tail*tail,(r,R,s.oo)),4*s.pi*gamma*p0*p0*R)
eq('retained_tail_flux_matches_edge',(4*s.pi*r*r*tail).subs(r,R),4*s.pi*R*R*p0)
# Positive-source single-node masscap: u=B/r², q=(A+B)/r², gamma vectorLapP=0.
A,B=s.symbols('A B',positive=True);ut=B/r**2
res=A/r**2-ut**2/(a0-ut)
eq('actual_correct_masscap_Euler_residual',C*s.diff(Lcrit,u).subs({g:(A+B)/r**2,u:ut}),res)
eq('masscap_residual_monopole_at_infinity',s.limit(r*r*res,r,s.oo),A)
u0,t=s.symbols('u0 t',positive=True);Aedge=R*R*u0*u0/(a0-u0);Bedge=R*R*u0
red=s.factor(res.subs({A:Aedge,B:Bedge}))
eq('purekernel_matched_tail_residual',red,a0*R*R*u0*u0*(r*r-R*R)/(r*r*(a0-u0)*(a0*r*r-R*R*u0)))
eq('purekernel_tail_only_matches_at_edge',red.subs(r,R))
# Parameterize every declared branch a0=u0+d, r=R+t: all factors strictly positive.
d=s.symbols('d',positive=True)
positive_form=R**2*t*u0**2*(2*R+t)*(d+u0)/(d*(R+t)**2*(d*(R+t)**2+u0*t*(2*R+t)))
eq('exterior_positive_factor_identity',red.subs({a0:u0+d,r:R+t}),positive_form)
positive('actual_exterior_tail_residual_positive',positive_form)
result={'all_passed':True,'count':len(checks),'checks':checks,'W_total':str(W),'residual_potential':str(U),'shell_charge':str(shellmass),'ramp_energy':str(E),'masscap_EL_residual':str(red),'scope':'Exact per-node cutoff and retained-tail operators; host/parent total field, covariant completion and altered boundary/action terms remain outside'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
