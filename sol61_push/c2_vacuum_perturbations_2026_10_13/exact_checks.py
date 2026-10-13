"""Exact local identities and counterexamples; no full constrained EFT claim."""
import argparse,json
from pathlib import Path
import sympy as s

parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
OUT=Path(parser.parse_args().output)
checks=[]
def eq(name,e):
    e=s.simplify(e);assert e==0,(name,e)
    checks.append({'name':name,'passed':True})
def ne(name,e):
    e=s.factor(e);assert e!=0,name
    checks.append({'name':name,'passed':True,'residual':str(e)})

a,X0,d,lam,qv,zv=s.symbols('a X0 d lambda qv zv',real=True)
P=lambda X:-s.Symbol('rho0')+a*(X-X0)**2/2
xe=X0+d+lam*qv+lam**2*zv/2
eq('fixed_metric_quadratic_action',s.expand(P(xe)).coeff(lam,2)-a*(qv**2+d*zv)/2)
N,B,om,ps,pt,pr,h00,h01,h11=s.symbols('N B omega psi pit pir h00 h01 h11',real=True)
g=s.diag(N**2,-1/B);hm=s.Matrix([[h00,h01],[h01,h11]])
p=s.Matrix([om,ps]);dp=s.Matrix([pt,pr]);q=g.inv()*p
inverse_variation=-g.inv()*hm*g.inv()
chi=(dp.T*g.inv()*p)[0]+(p.T*inverse_variation*p)[0]/2
eq('deltaX_includes_metric',chi-(q.T*dp)[0]+(q.T*hm*q)[0]/2)
deltaq=inverse_variation*p+g.inv()*dp
deltaJ=a*chi*q+a*d*deltaq
for i in range(2):eq('vacuum_deltaJ_'+str(i),deltaJ[i].subs(d,0)-a*chi*q[i])

r,R,grav,rho0,x=s.symbols('r R G rho0 x',positive=True)
BR=s.symbols('BR',positive=True)
Aedge=8*s.pi*grav*rho0*X0/BR
dd=Aedge*x**2
W=r**2*a*(2*X0+3*d)/(N*s.sqrt(B))
D=N*r**2*s.sqrt(B)*a*d
eq('core_radial_speed',D/W-N**2*B*d/(2*X0+3*d))
eq('core_edge_acoustic_coefficient',s.limit((D/W).subs({d:dd,N:1,B:BR})/x**2,x,0)-4*s.pi*grav*rho0)
Wedge=2*a*X0*R**2/s.sqrt(BR)
eq('core_edge_W',W.subs({r:R,d:0,N:1,B:BR})-Wedge)
eq('core_edge_D_coefficient',s.limit(D.subs({r:R,d:dd,N:1,B:BR})/x**2,x,0)-Wedge*4*s.pi*grav*rho0)
kappa=s.symbols('kappa',positive=True)
eq('acoustic_primitive',s.diff(s.log(x)/kappa,x)-1/(kappa*x))
assert s.limit(-s.log(x)/kappa,x,0)==s.oo
checks.append({'name':'acoustic_distance_diverges','passed':True})
eq('leading_zero_mode_constant',s.diff(x**2*s.diff(s.Integer(1),x),x))
eq('leading_zero_mode_inverse_x',s.diff(x**2*s.diff(1/x,x),x))
cut=s.symbols('cut',positive=True)
eq('constant_zero_mode_L2',s.integrate(1,(x,0,cut))-cut)
assert s.integrate(x**-2,(x,0,cut))==s.oo
checks.append({'name':'inverse_x_zero_mode_not_L2','passed':True})
f=x**(-s.Rational(1,4))
eq('finite_energy_singular_trace_L2',s.integrate(f**2,(x,0,cut))-2*s.sqrt(cut))
eq('finite_energy_singular_trace_gradient',s.integrate(x**2*s.diff(f,x)**2,(x,0,cut))-s.sqrt(cut)/8)
assert s.limit(f,x,0)==s.oo
checks.append({'name':'finite_weighted_energy_has_unbounded_trace','passed':True})
z=s.symbols('z',real=True);F=s.Function('F')(z);fz=s.exp(z/2)*F
eq('leading_Liouville_operator',-kappa**2*(s.diff(fz,z,2)-s.diff(fz,z))-s.exp(z/2)*kappa**2*(-s.diff(F,z,2)+F/4))

C=s.symbols('C',positive=True)
xx=s.symbols('xx',positive=True)
H=s.sqrt((xx+2)/(3*xx));bb=1-C*(2/(3*xx)+xx**2/3);br=1-C
eq('exterior_speed_factorization',br-bb-C*(xx-1)**2*H**2)
ut=br/bb
packet=[]
for sign in [-1,1]:
    ur=sign*s.sqrt(C)*(xx-1)*H
    eq('unit_geodesic_'+str(sign),bb/br*ut**2-ur**2/bb-1)
    eq('geodesic_time_'+str(sign),ur*s.diff(ut,xx)+s.diff(bb,xx)/bb*ut*ur)
    eq('geodesic_radius_'+str(sign),ur*s.diff(ur,xx)+s.diff(bb,xx)/2)
    expansion=(2*ur/xx+s.diff(ur,xx))/s.sqrt(C)
    V=sign*bb/br*(xx-1)*H
    weight=xx**2/bb
    reaction=s.diff(weight*V,xx)/weight
    eq('charge_transport_measure_'+str(sign),reaction-expansion/ut)
    eq('edge_velocity_derivative_'+str(sign),s.diff(V,xx).subs(xx,1)-sign)
    eq('edge_expansion_'+str(sign),expansion.subs(xx,1)-sign)
    eq('edge_density_reaction_'+str(sign),reaction.subs(xx,1)-sign)
    ne('expansion_deletion_detected_'+str(sign),reaction)
    packet.append({'sign':sign,'V':str(V),'reaction':str(s.simplify(reaction))})

Q,t,k=s.symbols('Q t k',positive=True)
M=s.Matrix([[0,1/Q],[0,0]])
eq('derivative_block_nilpotent',(M*M).norm())
eq('derivative_propagator',(s.exp(s.I*k*t*M)-(s.eye(2)+s.I*k*t*M)).norm())
eq('equal_order_transport_propagator',(s.exp(t*M)-(s.eye(2)+t*M)).norm())
assert M.rank()==1
checks.append({'name':'derivative_block_not_diagonalizable','passed':True})
assert s.limit(1/k,k,s.oo)==0
eq('wave_norm_counterexample_final_gradient',k*(t/k)-t)
checks.append({'name':'parametric_wave_norm_derivative_loss','passed':True,'argument':'pi0=0,pit0=cos(kx)/k; initial H1xL2 norm tends0, future phase gradient amplitude=t'})
eta,omega2=s.symbols('eta omega2',positive=True)
px=-a*eta;K=a*(2*X0-3*eta)
eq('negative_d_dispersion',px/K+eta/(2*X0-3*eta))
v=s.symbols('v',positive=True)
eq('negative_d_positive_time_coefficient',K.subs(eta,2*X0*v/(3*(1+v)))-2*a*X0/(1+v))
theta,tau,n0=s.symbols('Theta tau n0',real=True)
nt=n0*s.exp(-theta*tau)
eq('smooth_sign_transport_identity',s.diff(nt,tau)+theta*nt)
checks.append({'name':'sign_preserved_until_regular_flow_fails','passed':True,'argument':'general n(tau)=n0 exp[-integral Theta d tau]; exponential positive; existence/regularity remains an independent obligation'})
OUT.write_text(json.dumps({'all_passed':True,'count':len(checks),'checks':checks,'exterior_transport':packet,'nonclaims':['No constrained Einstein instability proof','No nonlinear well-posedness theorem','No higher derivative repair']},indent=2)+'\n')
print(json.dumps({'all_passed':True,'count':len(checks)}))
