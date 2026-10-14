"""Exact stress matching and finite shell perturbation surrogate."""
import json
import math
import sys
from pathlib import Path
import sympy as s

out=Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(label,expr):
    value=s.simplify(expr)
    assert value==0,(label,value)
    checks.append(label)

t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z)
b=s.Function('b')(x,y,z)
F=s.Function('A')(x,y,z)
g=s.Matrix([[-1+b*b,0,0,b],[0,1,0,0],[0,0,1,0],[b,0,0,1]])
gi=s.simplify(g.inv())
Gamma=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[q])+s.diff(g[d,q],coords[c])-s.diff(g[q,c],coords[d])) for d in range(4))/2) for c in range(4)] for q in range(4)] for a in range(4)]
Ric=s.zeros(4)
for a in range(4):
    for q in range(4):
        Ric[a,q]=s.simplify(sum(s.diff(Gamma[d][a][q],coords[d])-s.diff(Gamma[d][a][d],coords[q])+sum(Gamma[d][d][e]*Gamma[e][a][q]-Gamma[d][q][e]*Gamma[e][a][d] for e in range(4)) for d in range(4)))
scalar=s.simplify(sum(gi[a,q]*Ric[a,q] for a in range(4) for q in range(4)))
Ein=s.simplify(Ric-g*scalar/2)
n=s.Matrix([1,0,0,-b]); ez=s.Matrix([0,0,0,1])
zero('unit normal',(n.T*g*n)[0]+1)
zero('orthogonal z direction',(n.T*g*ez)[0])
Gnn=s.simplify((n.T*Ein*n)[0]); Gnz=s.simplify((n.T*Ein*ez)[0]); Gzz=s.simplify(Ein[3,3])
gradperp=s.diff(b,x)**2+s.diff(b,y)**2
zero('full Einstein density',Gnn+gradperp/4)
zero('full Einstein momentum',Gnz+(s.diff(b,x,2)+s.diff(b,y,2))/2)
zero('full Einstein z stress',Gzz+3*gradperp/4)
zero('two null contractions sum',2*(Gnn+Gzz)+2*gradperp)
shear=s.symbols('shear',positive=True)
planar_subs={s.diff(b,x):shear,s.diff(b,y):0,s.diff(b,z):0}
for a in (x,y,z):
    for q0 in (x,y,z):
        planar_subs[s.diff(b,a,q0)]=0
frame=s.Matrix.hstack(n,s.Matrix([0,1,0,0]),s.Matrix([0,0,1,0]),ez)
Gframe=s.simplify(frame.T*Ein*frame)
Gplanar=Gframe.subs(planar_subs,simultaneous=True).applyfunc(s.simplify)
eta=s.diag(-1,1,1,1)
mixed=s.simplify(eta*Gplanar*4/shear**2)
assert mixed==s.diag(1,1,-1,-3),mixed
checks.append('planar mixed stress eigenvalues')
for ev in (1,-1,-3):
    assert (mixed-ev*s.eye(4)).rank()>1
checks.append('planar stress cannot be pressure plus one rank-one scalar')
H=s.Matrix(4,4,lambda a,q:s.simplify(s.diff(F,coords[a],coords[q])-sum(Gamma[d][a][q]*s.diff(F,coords[d]) for d in range(4))))
Hnz=s.simplify((n.T*H*ez)[0])
zero('full Hessian normal z',Hnz-((s.diff(b,x)*s.diff(F,x)+s.diff(b,y)*s.diff(F,y))/2-b*s.diff(F,z,2)))

r=s.symbols('r',positive=True)
br,brr,Ar,Av,bv=s.symbols('br brr Ar Av bv',real=True)
equator={s.diff(b,x,2):brr,s.diff(b,y,2):br/r,s.diff(b,x):br,s.diff(b,y):0,b:bv,s.diff(F,x):Ar,s.diff(F,y):0,s.diff(F,z,2):Ar/r}
Geq=s.simplify(Gnz.subs(equator,simultaneous=True))
Heq=s.simplify(Hnz.subs(equator,simultaneous=True))
zero('equatorial source equation',-2*(Av*Geq-Heq)-(Av*(brr+br/r)+(br-2*bv/r)*Ar))

# A regular positive A turns the necessary equation into a nonsingular
# homogeneous linear second-order ODE for b; zero b,b' initial data are unique.
rad=s.Function('b')(r); af=s.Function('A')(r)
ode=af*(s.diff(rad,r,2)+s.diff(rad,r)/r)+(s.diff(rad,r)-2*rad/r)*s.diff(af,r)
normal=s.diff(rad,r,2)+(1/r+s.diff(af,r)/af)*s.diff(rad,r)-2*s.diff(af,r)*rad/(r*af)
zero('ODE normalization',ode/af-normal)
zero('ODE self adjoint form',ode-(s.diff(r*af*s.diff(rad,r),r)-2*rad*s.diff(af,r))/r)

u=s.symbols('u',real=True)
rise=10*u**3-15*u**4+6*u**5
D=s.expand((u+1)*s.diff(rise,u)-2*rise)
Q=9*u**3-25*u+15
zero('quintic obstruction denominator factor',D-2*u**2*Q)
N=s.expand((u+1)*s.diff(rise,u,2)+s.diff(rise,u))
zero('quintic obstruction numerator factor',N-30*u*(1-u)*(2-u-5*u**2))
lo=s.Rational(3,4); hi=s.Rational(19,25)
assert Q.subs(u,lo)>0 and Q.subs(u,hi)<0
checks.append('exact root bracket')
assert s.Poly(Q,u).count_roots(0,1)==1
checks.append('one exact interior obstruction root')
assert (2-u-5*u*u).subs(u,lo)<0
checks.append('negative numerator throughout bracket by negative derivative')
roots=[v for v in s.nroots(Q,maxsteps=100) if abs(s.im(v))<s.Float('1e-14') and 0<float(s.re(v))<1]
assert len(roots)==1
root=float(s.re(roots[0]))

# P(X) action quadratic principal term, independent Taylor expansion.
q,eps,pdot,g2,Px,Pxx=s.symbols('q eps pdot g2 Px Pxx',real=True)
dX=eps*q*pdot+eps**2*(pdot**2-g2)/2
Pexp=Px*dX+Pxx*dX*dX/2
quadratic=s.expand(Pexp).coeff(eps,2)
zero('timelike principal quadratic',quadratic-((Px+q*q*Pxx)*pdot**2-Px*g2)/2)
# Spacelike background phi=q*x has time coefficient PX and x-gradient PX-q²PXX.
dx,dy,dz=s.symbols('dx dy dz',real=True)
dXs=-eps*q*dx+eps**2*(pdot**2-dx*dx-dy*dy-dz*dz)/2
spacequad=s.expand(Px*dXs+Pxx*dXs*dXs/2).coeff(eps,2)
zero('spacelike time kinetic coefficient',s.diff(spacequad,pdot,2)-Px)

X,M,delta=s.symbols('X M delta',positive=True)
P=-X+X**2/M**4+M**4/4
X0=(1-delta)*M**4/2
rho=s.simplify((2*X*s.diff(P,X)-P).subs(X,X0))
px=s.simplify(s.diff(P,X).subs(X,X0))
Akin=s.simplify((s.diff(P,X)+2*X*s.diff(P,X,2)).subs(X,X0))
zero('negative-density branch',rho-M**4*(-delta+3*delta**2/4))
zero('branch NEC coefficient',px+delta)
zero('branch kinetic coefficient',Akin-(2-3*delta))
zero('zero-density reference state',rho.subs(delta,0))

# Ideal spherical shell eigenfunction, squared Dirichlet Laplacian boundaries.
aa,dd=s.symbols('a d',positive=True)
psi=s.sin(s.pi*(r-aa)/dd)/r
lap=s.diff(psi,r,2)+2*s.diff(psi,r)/r
zero('shell ground-state Laplacian',lap+(s.pi/dd)**2*psi)
zero('inner Dirichlet',psi.subs(r,aa))
zero('outer Dirichlet',psi.subs(r,aa+dd))
zero('inner Laplacian boundary',lap.subs(r,aa))
zero('outer Laplacian boundary',lap.subs(r,aa+dd))
k,kap=s.symbols('k kappa',positive=True)
w2=k**4/M**2-kap*k**2
zero('continuum fastest instability stationary point',s.diff(-w2,k).subs(k,M*s.sqrt(kap/2)))
zero('continuum growth maximum',(-w2).subs(k,M*s.sqrt(kap/2))-kap**2*M**2/4)

rows=[]
for de in (1e-6,1e-4,1e-2):
    ka=de/(2-3*de)
    for ell in (40,100,300,1000,10000):
        nmax=math.floor(0.1*ell/math.pi)
        values=[(j*math.pi/ell)**4-ka*(j*math.pi/ell)**2 for j in range(1,nmax+1)]
        assert values
        stable=ell<=math.pi/math.sqrt(ka)
        assert stable==all(vv>=0 for vv in values)
        checks.append('gap vs enumerated radial modes '+str((de,ell)))
        rows.append({'delta':de,'Md':ell,'kappa':ka,'max_radial_n_under_k_over_M_0_1':nmax,'radial_modes_unstable':sum(vv<0 for vv in values),'gap_predicts_stable':stable,'omega1_squared_over_M2':values[0]})
result={'claim':'CWS-001/002','checks_passed':len(checks),'Gnn':str(Gnn),'Gnz':str(Gnz),'Gzz':str(Gzz),'Hnz':str(Hnz),'root_u':root,'root_radius_over_R':(1+root)/2,'rho_branch':str(rho),'kinetic_branch':str(Akin),'spectral_rows':rows,'nonclaim':'No actual cold medium, complete wall stress realization, physical boundary controller or full gravitational stability.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
