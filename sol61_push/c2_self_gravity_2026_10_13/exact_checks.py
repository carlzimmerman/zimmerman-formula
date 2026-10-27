"""Bounded exact checks of a CONDITIONAL C2 + Einstein comparison."""
from pathlib import Path
import json
import sympy as s

OUT = Path(__file__).parent / 'exact_run' / 'results.json'
checks = []
def equal(name, value):
    value = s.simplify(value)
    assert value == 0, (name, value)
    checks.append({'name': name, 'passed': True})
def nonzero(name, value):
    value = s.factor(value)
    assert value != 0, name
    checks.append({'name': name, 'passed': True, 'mutation_residual': str(value)})

t,r,th,ph = s.symbols('t r th ph', real=True)
N, B = s.Function('N')(r), s.Function('B')(r)
coords=[t,r,th,ph]
metric=s.diag(N**2,-1/B,-r**2,-r**2*s.sin(th)**2)
inv=metric.inv()
# R^a_bcd = partial_c Gamma^a_db - partial_d Gamma^a_cb + ...
gam={}
for i in range(4):
    for j in range(4):
        for k in range(4):
            v=s.simplify(sum(inv[i,l]*(s.diff(metric[l,k],coords[j])+s.diff(metric[l,j],coords[k])-s.diff(metric[j,k],coords[l])) for l in range(4))/2)
            if v != 0: gam[i,j,k]=v
def C(i,j,k): return gam.get((i,j,k),s.S.Zero)
ric=[]
for i in range(4):
    ric.append(s.simplify(sum(s.diff(C(k,i,i),coords[k])-s.diff(C(k,i,k),coords[i])+sum(C(k,k,l)*C(l,i,i)-C(k,i,l)*C(l,i,k) for l in range(4)) for k in range(4))))
scalar=s.simplify(sum(inv[i,i]*ric[i] for i in range(4)))
G=[s.simplify(inv[i,i]*ric[i]-scalar/2) for i in range(4)]
equal('geometry_tt',G[0]-((1-B)/r**2-s.diff(B,r)/r))
equal('geometry_rr',G[1]-((1-B)/r**2-2*B*s.diff(N,r)/(r*N)))
expected_ang=-B*(s.diff(N,r,2)/N+s.diff(N,r)/(r*N))-s.diff(B,r)*(s.diff(N,r)/N+1/r)/2
equal('geometry_theta',G[2]-expected_ang)
equal('geometry_phi',G[3]-G[2])

grav,a,X0,rho0,d,R=s.symbols('G a X0 rho0 d R',positive=True)
X=s.symbols('X',positive=True)
P=-rho0+a*(X-X0)**2/2
px=s.diff(P,X); pxx=s.diff(P,X,2)
rho=rho0+2*a*X0*d+s.Rational(3,2)*a*d**2
p=-rho0+a*d**2/2
equal('C2_density', (2*X*px-P).subs(X,X0+d)-rho)
equal('C2_pressure',P.subs(X,X0+d)-p)
equal('C2_enthalpy',rho+p-2*a*d*(X0+d))
equal('C2_kinetic_coefficient',(px+2*X*pxx).subs(X,X0+d)-a*(2*X0+3*d))
equal('C2_sound_speed',(px/(px+2*X*pxx)).subs(X,X0+d)-d/(2*X0+3*d))
nuprime=s.symbols('nuprime')
dprime=-2*(X0+d)*nuprime
equal('phase_implies_hydrostatic',s.diff(p,d)*dprime+(rho+p)*nuprime)

m=s.symbols('m',real=True)
bb=1-2*grav*m/r
F=m+4*s.pi*r**3*p
nn=grav*F/(r**2*bb)
mp=4*s.pi*r**2*rho
dp=-2*(X0+d)*nn
bp=s.diff(bb,r)+s.diff(bb,m)*mp
np=s.diff(nn,r)+s.diff(nn,m)*mp+s.diff(nn,d)*dp
equal('Einstein_tt_mass', (1-bb)/r**2-bp/r-8*s.pi*grav*rho)
equal('Einstein_rr_pressure',(1-bb)/r**2-2*bb*nn/r+8*s.pi*grav*p)
equal('Einstein_angular_closure',-bb*(np+nn**2+nn/r)-bp*(nn+1/r)/2+8*s.pi*grav*p)

edge={r:R,m:4*s.pi*rho0*R**3,d:0}
br=1-8*s.pi*grav*rho0*R**2
equal('edge_B',bb.subs(edge)-br)
equal('edge_nuprime',nn.subs(edge))
equal('edge_Bprime',bp.subs(edge))
equal('edge_nusecond',np.subs(edge)+8*s.pi*grav*rho0/br)
ddp=s.diff(dp,r)+s.diff(dp,m)*mp+s.diff(dp,d)*dp
equal('edge_dsecond',ddp.subs(edge)-16*s.pi*grav*rho0*X0/br)
fp=s.diff(F,r)+s.diff(F,m)*mp+s.diff(F,d)*dp
equal('edge_active_mass_derivative',fp.subs(edge)+8*s.pi*rho0*R**2)
M=8*s.pi*rho0*R**3/3
equal('areal_mean_excess_density',M/(4*s.pi*R**3/3)-2*rho0)
be=1-2*grav*M/r-8*s.pi*grav*rho0*r**2/3
equal('vacuum_tt',(1-be)/r**2-s.diff(be,r)/r-8*s.pi*grav*rho0)
equal('vacuum_rr',(1-be)/r**2-s.diff(be,r)/r-8*s.pi*grav*rho0)
equal('vacuum_angular',-s.diff(be,r,2)/2-s.diff(be,r)/r-8*s.pi*grav*rho0)
equal('exterior_B_match',be.subs(r,R)-br)
equal('exterior_Bprime_match',s.diff(be,r).subs(r,R))
equal('exterior_Bsecond',s.diff(be,r,2).subs(r,R)+16*s.pi*grav*rho0)
psi2=2*X0/be*(br/be-1)
equal('exterior_phase_X',((2*X0*br/be-be*psi2)/2)-X0)
nonzero('wrong_gradient_sign_detected',((2*X0*br/be+be*psi2)/2)-X0)
nonzero('omit_vacuum_active_pressure_detected',nn.subs(edge).subs(rho0,rho0)+grav*(4*s.pi*R**3*rho0)/(R**2*br))
nonzero('identify_total_as_excess_mass_detected',4*s.pi*rho0*R**3-M)

eps,uc,y,Y=s.symbols('epsilon uc y Y',real=True)
u,w=s.symbols('u w',real=True)
rhob=1+2*u+s.Rational(3,2)*eps*u**2
pb=-1+eps*u**2/2
bc=1-eps*w/(2*y)
up=-(1+eps*u)*(w+y**3*pb)/(2*y**2*bc)
wp=y**2*rhob
upp=s.diff(up,y)+s.diff(up,u)*up+s.diff(up,w)*wp
equal('dimensionless_edge_u_second',upp.subs({u:0,w:y**3})-1/(1-eps*y**2/2))
u0=1+(uc-1)*s.sin(y)/y
w0=y**3-2*y**2*s.diff(u0,y)
equal('weak_u_equation',s.diff(u0,y)+(w0-y**3)/(2*y**2))
equal('weak_w_equation',s.diff(w0,y)-y**2*(1+2*u0))
equal('weak_center_limit',s.limit(u0,y,0)-uc)
# At tanY=Y, sinY=Y cosY; uc=1-1/cosY.
at={s.sin(Y):Y*s.cos(Y),uc:1-1/s.cos(Y)}
equal('weak_endpoint_u',u0.subs(y,Y).subs(at))
equal('weak_endpoint_uprime',s.diff(u0,y).subs(y,Y).subs(at))
equal('weak_endpoint_u_second',s.diff(u0,y,2).subs(y,Y).subs(at)-1)
equal('weak_endpoint_jacobian_11',s.diff(u0,uc).subs(y,Y).subs(at)-s.cos(Y))
equal('weak_endpoint_jacobian_21',s.diff(u0,y,uc).subs(y,Y).subs(at))

lam=s.symbols('lambda',positive=True)
theta=lam+(1-lam)*s.sin(y)/y
iu=s.integrate(s.expand(theta**2*y**2),(y,0,Y))
i4=s.integrate(s.expand(theta*y**4),(y,0,Y))
# Critical lambda=-cosY/(1-cosY) => cosY=-lambda/(1-lambda).
crit={s.sin(Y):Y*s.cos(Y),s.sin(2*Y):2*Y*s.cos(Y)**2,s.cos(Y):-lam/(1-lam)}
def reduce_crit(v):
    v=v.subs(crit,simultaneous=False)
    # cos²Y=1/(1+Y²), combined with cosY=-lam/(1-lam).
    # Equivalent polynomial relation lam² Y²=1-2lam.
    num,den=s.fraction(s.factor(v))
    remainder=s.rem(s.Poly(num,Y),s.Poly(lam**2*Y**2+2*lam-1,Y)).as_expr()
    return s.factor(remainder/den)
equal('weak_internal_energy_integral',reduce_crit(iu-5*lam**2*Y**3/6))
equal('weak_vacuum_work_integral',reduce_crit(i4-lam*Y**3*(Y**2/5-2)))
equal('weak_homologous_stiffness_factor',5*lam**2*Y**3/6-lam*(lam*Y**3*(Y**2/5-2))/3-lam**2*Y**3*(s.Rational(3,2)-Y**2/15))
scale,U,W,V=s.symbols('scale U W V',real=True)
energy=U/scale**3+W/scale+V*scale**2
equal('homologous_virial',s.diff(energy,scale).subs({scale:1,W:-3*U+2*V}))
equal('homologous_second_variation',s.diff(energy,scale,2).subs({scale:1,W:-3*U+2*V})-6*(U+V))
OUT.write_text(json.dumps({'all_passed':True,'count':len(checks),'checks':checks,'geometry':{'mixed_Einstein_components':[str(v) for v in G]},'scope':'exact identities, not physical postulate validation'},indent=2)+'\n')
print(json.dumps({'all_passed':True,'count':len(checks)}))
