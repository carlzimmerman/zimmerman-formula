"""Local parent operator, slow-sheet response, and domain-wall stress obstruction."""
import argparse
import json
import math
from pathlib import Path
import sympy as s
from scipy.integrate import quad

checks=[]
def check(name,ok,detail=None):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
    print(('PASS ' if ok else 'FAIL ')+name)

sx=s.Matrix([[0,1],[1,0]]);sy=s.Matrix([[0,-s.I],[s.I,0]]);sz=s.diag(1,-1);I=s.eye(2)
kp=s.kronecker_product
gam=[kp(sx,I,I),kp(sy,I,I),kp(sz,sx,I),kp(sz,sy,I),kp(sz,sz,sx),kp(sz,sz,sy),kp(sz,sz,sz)]
check('seven Hermitian Clifford generators',all(a.H==a for a in gam) and all(a*b+b*a==(2*s.eye(8) if i==j else s.zeros(8)) for i,a in enumerate(gam) for j,b in enumerate(gam)))
C=s.I*gam[2]*gam[3];projector=(s.eye(8)+C)/2
check('normalizable wall projector rank four',C.H==C and C*C==s.eye(8) and projector.rank()==4 and projector*projector==projector)
surface=[gam[i] for i in (0,1,4,5,6)]
check('five surface generators preserve wall subspace',all(a*C==C*a for a in surface))
v,vz,g,f,L,z,P,y,ell,G=s.symbols('v vz g f L z P y ell G',positive=True)
profile=s.cosh(z/L)**(-g*f*L/vz)
check('bound envelope solves normal Dirac equation',s.simplify(vz*s.diff(profile,z)+g*f*s.tanh(z/L)*profile)==0)
check('positive Yukawa gives exponentially decaying tails',s.limit(s.diff(s.log(profile),z),z,s.oo)==-g*f/vz)
kx,ky,p1,p2,p3=s.symbols('kx ky p1 p2 p3',real=True)
H=v*kx*gam[0]+v*ky*gam[1]+y*(p1*gam[4]+p2*gam[5]+p3*gam[6])
check('projected isotropic spectrum exact',s.simplify(H*H-(v*v*(kx*kx+ky*ky)+y*y*(p1*p1+p2*p2+p3*p3))*s.eye(8))==s.zeros(8))
# A mass allowed by internal rotations alone: gap protection needs more symmetry.
singlet=s.I*gam[0]*gam[1]
rotations=[gam[i]*gam[j] for i in (4,5,6) for j in (4,5,6) if i<j]
check('internal rotation singlet mass remains allowed',all(singlet*a==a*singlet for a in rotations) and all(singlet*a+a*singlet==s.zeros(8) for a in gam[:2]) and singlet*C==C*singlet)

lam=s.symbols('lam',positive=True)
chi=f*s.tanh(z/L);potential=lam*(chi*chi-f*f)**2/4
L0=s.sqrt(2)/(s.sqrt(lam)*f)
check('tree scalar kink equation',s.simplify((s.diff(chi,z,2)-lam*chi*(chi*chi-f*f)).subs(L,L0))==0)
# First integral makes gradient energy equal potential. Integral sech^4 x=4/3.
check('kink first integral',s.simplify((s.diff(chi,z)**2/2-potential).subs(L,L0))==0)
u=s.symbols('u',real=True)
sech_integral=s.integrate(1-u*u,(u,-1,1))
sigma=s.simplify(f*f/L0*sech_integral)
check('positive tree wall tension',s.simplify(sigma-2*s.sqrt(2)*s.sqrt(lam)*f**3/3)==0)

q,m,K,nu=s.symbols('q m K nu',positive=True)
# Scale l=v k in the two-dimensional loop measure.
energy=-nu*((v*v*K*K+m*m)**s.Rational(3,2)-(v*K)**3-m**3)/(6*s.pi*v*v)+nu*K*m*m/(4*s.pi*v)
check('sheet cubic enhanced by inverse speed squared',s.limit(energy,K,s.oo)==nu*m**3/(6*s.pi*v*v))
bubble=s.atan(v*q/(2*m))/(4*s.pi*v*q)
DL=y*y/v**2*2*((v*v*q*q+4*m*m)*bubble-4*m*m/(8*s.pi*m))
DT=y*y/v**2*2*v*v*q*q*bubble
check('local longitudinal stiffness speed independent',s.limit(DL/q**2,q,0)==y*y/(6*s.pi*m))
check('local transverse stiffness speed independent',s.limit(DT/q**2,q,0)==y*y/(4*s.pi*m))
check('massless nonlocal kernel scales as inverse speed',s.limit(DT,m,0)==y*y*q/(4*v))
rows=[]
for speed in (.1,.01):
    for momentum in (.01,.1,1.,10.):
        num=quad(lambda x:1/(8*math.pi*math.sqrt(1+x*(1-x)*(speed*momentum)**2)),0,1,epsabs=1e-12,epsrel=1e-12)[0]
        ex=math.atan(speed*momentum/2)/(4*math.pi*speed*momentum)
        check('rescaled bubble v=%g q/m=%g'%(speed,momentum),abs(num-ex)<1e-11)
        rows.append(dict(v=speed,q_over_m=momentum,error=abs(num-ex)))

# Mean in-plane momentum squared: <1-(n dot qhat)^2>=2/3.
check('isotropic plane projection factor',s.integrate((1-u*u)/2,(u,-1,1))==s.Rational(2,3))
AL=4*G*y/(9*ell);AT=2*G*y/(3*ell) # nu=2, bulk normalization 4pi G.
r,A,a0,Mass=s.symbols('r A a0 Mass',positive=True)
radP=A/r
grad_force=s.simplify(AL*s.diff(radP,r)**2/(2*radP**2)-AL*(s.diff(radP,r,2)+2*s.diff(radP,r)/r)/radP+AT/r**2)
check('leading derivative force gives constant mass offset',s.simplify(grad_force-8*G*y/(9*ell*r*r))==0)
alpha=2*G*nu*y**3/(3*ell*v*v);scale=1/(3*alpha)
check('response acceleration dictionary with speed',s.simplify(scale-ell*v*v/(2*G*nu*y**3))==0)
check('nu-two derivative relative correction',s.simplify((grad_force/(radP**2/scale)).subs(nu,2)-2*v*v/(9*y*y*A*A))==0)
mass_offset=8*y/(9*ell)
check('formal far-field amplitude branch',s.simplify((radP**2/scale+grad_force-G*Mass/r**2).subs(A*A,scale*G*(Mass-mass_offset)))==0)

# Normal boost of a positive-tension wall followed by isotropic orientation mean.
b=s.symbols('b',real=True)
gamma2=1/(1-b*b)
wall_w=s.simplify((-2/gamma2+b*b)/3)
check('wall equation of state exact',s.simplify(wall_w-(-s.Rational(2,3)+b*b))==0)
check('vacuum equation of state has no real wall velocity',s.solve(s.Eq(wall_w,-1),b)==[])
sigma_symbol=s.symbols('sigma',positive=True)
density=sigma_symbol/ell
ratio=s.simplify(8*s.pi*G*density/scale**2)
check('density-scale ratio retains independent inputs',s.simplify(ratio-32*s.pi*G**3*nu**2*y**6*sigma_symbol/(ell**3*v**4))==0)
check('ratio changes with wall separation',s.diff(ratio,ell)!=0)
aa,ell0=s.symbols('aa ell0',positive=True)
check('frozen comoving wall density redshifts as a inverse',s.simplify(density.subs(ell,ell0*aa)*aa-sigma_symbol/ell0)==0)
check('same frozen population makes a0 grow with a',s.simplify(scale.subs(ell,ell0*aa)/aa-scale.subs(ell,ell0))==0)
check('density acceleration ratio drifts as a inverse cubed',s.simplify(ratio.subs(ell,ell0*aa)*aa**3-ratio.subs(ell,ell0))==0)

galA=(200000/299792458)**2;eps=1e-9/galA
check('hypothetical slow speed admits local hierarchy',eps<.01,eps)
example=dict(galactic_A=galA,mode_speed_over_c=1e-9,y=1,derivative_parameter=eps,leading_gradient_fraction=2*eps*eps/9)
result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,rows=rows,example=example,non_claims=['Preferred-frame local probe parent, not covariant gravity theory','No dynamically selected mode velocity or sheet density','No protection against the allowed singlet mass or critical quadratic detuning','Tree kink ignores fermion backreaction','Derivative expansion, not full nonuniform determinant','Wall stress is not cosmological-constant stress','No 32pi selection'])
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print('%s %d/%d'%(result['status'],result['passed'],result['total']))
raise SystemExit(result['status']!='PASS')
