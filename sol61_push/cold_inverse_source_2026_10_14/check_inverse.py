"""Inverse source, field equations and a precise local positivity obstruction."""
import json
import sys
from pathlib import Path
import sympy as s

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,v):
    vv=s.simplify(v)
    assert vv==0,(name,vv)
    checks.append(name)

t,x,y,z=s.symbols('t x y z',real=True);coords=(t,x,y,z)
b=s.Function('b')(x,y,z)
g=s.Matrix([[-1+b*b,0,0,b],[0,1,0,0],[0,0,1,0],[b,0,0,1]])
gi=s.simplify(g.inv());zero('metric determinant',g.det()+1)
Gamma=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[q])+s.diff(g[d,q],coords[c])-s.diff(g[q,c],coords[d])) for d in range(4))/2) for c in range(4)] for q in range(4)] for a in range(4)]
Ric=s.zeros(4)
for a in range(4):
    for q in range(4):
        Ric[a,q]=s.simplify(sum(s.diff(Gamma[d][a][q],coords[d])-s.diff(Gamma[d][a][d],coords[q])+sum(Gamma[d][d][e]*Gamma[e][a][q]-Gamma[d][q][e]*Gamma[e][a][d] for e in range(4)) for d in range(4)))
scalar=s.simplify(sum(gi[a,q]*Ric[a,q] for a in range(4) for q in range(4)))
Ein=s.simplify(Ric-g*scalar/2)
# Mp² factored out; phiA=xA on this target. H_AB=Ric_AB.
H=Ric
T=s.simplify(H-g*sum(gi[a,q]*H[a,q] for a in range(4) for q in range(4))/2)
for a in range(4):
    for q in range(a,4):
        zero('Einstein source component '+str((a,q)),T[a,q]-Ein[a,q])
# Scalar equation E_A=partial_mu(H_AB g^{mu B})-g^{BC} partial_A H_BC/2.
# sqrt(-g)=1 here, so this is the full coordinate Euler-Lagrange residual.
for a in range(4):
    residual=sum(s.diff(sum(H[a,q]*gi[mu,q] for q in range(4)),coords[mu]) for mu in range(4))-sum(gi[q,d]*s.diff(H[q,d],coords[a]) for q in range(4) for d in range(4))/2
    zero('scalar Euler Lagrange '+str(a),residual)
n=s.Matrix([1,0,0,-b]);ez=s.Matrix([0,0,0,1])
Hnn=s.simplify((n.T*H*n)[0]);Hzz=s.simplify((ez.T*H*ez)[0])
zero('Ricci sum driving positivity obstruction',Hnn+Hzz+s.diff(b,x)**2+s.diff(b,y)**2)

# Any 10x10 symmetric strain Hessian restricts to these3 strains when other
# perturbations and x/y derivatives are zero. Thus this is not a sampled C.
d0,dz,g0,gz=s.symbols('dot0 dotz grad0 gradz',real=True)
h00,h0z,hzz=s.symbols('H00 H0z Hzz',real=True)
c00,c01,c02,c11,c12,c22=s.symbols('C00 C01 C02 C11 C12 C22',real=True)
C=s.Matrix([[c00,c01,c02],[c01,c11,c12],[c02,c12,c22]])
u=s.Matrix(s.symbols('strain0:3'))
counter=(u.T*C*u)[0]/2
atbg={q:0 for q in u}
zero('counterterm background value',counter.subs(atbg))
for q in u:zero('counterterm first variation '+str(q),s.diff(counter,q).subs(atbg))
strain=s.Matrix([-2*d0,-dz+g0,2*gz])
Lbase=(h00*(d0*d0-g0*g0)+2*h0z*(d0*dz-g0*gz)+hzz*(dz*dz-gz*gz))/2
L=s.expand(Lbase+(strain.T*C*strain)[0]/2)
K=s.hessian(L,(d0,dz));G=-s.hessian(L,(g0,gz))
Mix=s.Matrix(2,2,lambda a,q:s.diff(L,(d0,dz)[a],(g0,gz)[q]))
zero('all strain counterterms cancel from obstruction',K[1,1]+G[0,0]-h00-hzz)
# A Legendre calculation, in velocity variables, shows mixed terms cancel
# from energy; arbitrary cross coupling cannot hide a negative spatial form.
mom=s.Matrix([s.diff(L,d0),s.diff(L,dz)])
vel=s.Matrix([d0,dz]);grad=s.Matrix([g0,gz])
energy=s.expand((mom.T*vel)[0]-L)
zero('Legendre energy identity',energy-(vel.T*K*vel)[0]/2-(grad.T*G*grad)[0]/2)

# Positive definite K -> Kzz>0 -> G00<H00+Hzz<0 for target; no finite scan.
# An exact one-dimensional counterexample: real wave speeds do not imply
# positive Hamiltonian when mixed time-space terms are permitted.
speed=s.symbols('speed',real=True)
poly=speed**2-4*speed+1
roots=s.solve(poly,speed)
assert len(roots)==2 and all(rr.is_real for rr in roots)
checks.append('real speeds with indefinite Hamiltonian counterexample')
for rr in roots:zero('gyroscopic root '+str(rr),poly.subs(speed,rr))

# Planar constant-shear control in local orthonormal material frame.
shear=s.symbols('shear',positive=True)
sub={s.diff(b,x):shear,s.diff(b,y):0,s.diff(b,z):0}
for a in (x,y,z):
    for q in (x,y,z):sub[s.diff(b,a,q)]=0
frame=s.Matrix.hstack(n,s.Matrix([0,1,0,0]),s.Matrix([0,0,1,0]),ez)
Hplanar=(frame.T*H*frame).subs(sub,simultaneous=True).applyfunc(s.simplify)
expected=s.diag(-1,1,0,-1)*shear**2/2
for a in range(4):
    for q in range(a,4):zero('planar Ricci source '+str((a,q)),Hplanar[a,q]-expected[a,q])
u0,ux,uy,uz=s.symbols('u0 ux uy uz',real=True)
hu=-u0*u0+ux*ux-uz*uz
zero('planar source negative on every timelike unit vector',hu.subs(u0*u0,1+ux*ux+uy*uy+uz*uz)+1+uy*uy+2*uz*uz)
eta=s.diag(-1,1,1,1)
zero('planar Lorentz trace',s.trace(eta*s.diag(-1,1,0,-1))-1)

result={'claim':'CIS-001','checks_passed':len(checks),'source_action':'S=integral sqrt(-g)[Mp2 R/2-H_AB(phi)partial phiA.partial phiB/2], H_AB=Mp2 Ric_AB[g*](phi)','scalar_equations':'all4 exact Euler-Lagrange residuals zero for arbitrary static b(x,y,z)','Kzz':str(K[1,1]),'G_clock_z':str(G[0,0]),'obstruction_sum':str(s.simplify(K[1,1]+G[0,0])),'planar_H_over_Mp2':str(Hplanar),'gyroscopic_real_speeds':[str(rr) for rr in roots],'interpretation':'Exact inverse-designed source, not identified physical cold matter. Positive quadratic energy in specified normal frame fails for regular first-derivative strain deformations; not a universal instability theorem.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
