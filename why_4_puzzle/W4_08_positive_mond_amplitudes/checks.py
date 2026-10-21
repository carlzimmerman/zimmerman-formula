#!/usr/bin/env python3
"""Bounded exact algebra for scoped response models. No parameter scan."""
import hashlib
import json
import os
from pathlib import Path
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
MUTATE=os.environ.get('W4_08_MUTATE','0')=='1'
rows=[]


def eq(a,b=0):
    return s.simplify(a-b)==0


def check(name,ok,value):
    passed=bool(ok)
    rows.append({'name':name,'passed':passed,'value':str(value)})
    print(f"{'PASS' if passed else 'FAIL'} {name}: {value}")


t,d,A,L,y,h=s.symbols('t d A L y h',positive=True)
mu=1+t-s.sqrt(1+t*t)
long=s.factor(mu+t*s.diff(mu,t))
energy=1+s.Rational(3,2)*t*t-(1+t*t)**s.Rational(3,2)+t**3
check('K01 band response derivative',eq(s.diff(energy,t),3*t*mu),s.diff(energy,t))
check('K02 band longitudinal Hessian',eq(s.diff(energy,t,2),3*long),long)
check('K03 transverse positive factor',eq((1+t)**2-(1+t*t),2*t),'1+t>sqrt(1+t^2)')
check('K04 longitudinal positive factor',eq((1+2*t)**2*(1+t*t)-(1+2*t*t)**2,4*t+t*t+4*t**3),'4t+t^2+4t^3>0')
check('K05 longitudinal upper factor',eq((1+2*t*t)**2-4*t*t*(1+t*t),1),'upper bound via difference of squares=1')
check('K06 band cubic IR',s.limit(energy/t**3,t,0)==1,s.limit(energy/t**3,t,0))
check('K07 band quadratic UV',s.limit(energy/t**2,t,s.oo)==s.Rational(3,2),s.limit(energy/t**2,t,s.oo))

r=s.sqrt(1+d*d)
b=1+d-r
f=(1+d*d)**s.Rational(3,2)-1-d**3
pair=(1+d*d+t*t)**s.Rational(3,2)-(d*d+t*t)**s.Rational(3,2)-(1+t*t)**s.Rational(3,2)+t**3
crit=s.Rational(3,2)*b
series=s.series(pair+crit*t*t,t,0,5).removeO().expand()
check('K08 paired baseline',eq(pair.subs(t,0),f),f)
check('K09 critical paired quadratic',eq(series.coeff(t,2)),series.coeff(t,2))
check('K10 paired cubic positive',eq(series.coeff(t,3),1),series.coeff(t,3))
w=s.symbols('w',positive=True)
uvbracket=(1+(1+d*d)*w*w)**s.Rational(3,2)-(1+d*d*w*w)**s.Rational(3,2)-(1+w*w)**s.Rational(3,2)+1
uv=s.series(uvbracket,w,0,6).removeO().expand()
check('K11 paired determinant UV decay',eq(uv.coeff(w,0)) and eq(uv.coeff(w,2)) and eq(uv.coeff(w,4),3*d*d/4),'D(t)~3d^2/(4t)')
C0=A*L**3*f
C2=s.Rational(3,2)*A*L*y*y*b
C3=A*y**3
R=s.factor(C0*C3*C3/C2**3)
check('K12 operational amplitude ratio',eq(R,s.Rational(8,27)*f/b**3),R)
check('K13 band factorization',eq(f,b*b*(1+d+2*r)/2),s.simplify(f-b*b*(1+d+2*r)/2))
u=r/(1+d)
Ru=s.Rational(4,27)*(1+2*u)/(1-u)
check('K14 closed amplitude expression',eq(R,Ru),Ru)
check('K15 reciprocal gap invariance',eq(R.subs(d,1/d),R),'R(d)=R(1/d)')
check('K16 unique minimum variable',eq(s.diff((1+d*d)/(1+d)**2,d),2*(d-1)/(d+1)**3),'sign(d-1)')
U=s.symbols('U',positive=True)
check('K17 monotone ratio function',eq(s.diff(s.Rational(4,27)*(1+2*U)/(1-U),U),s.Rational(4,9)/(1-U)**2),'4/[9(1-U)^2]>0')
Rmin=(16+12*s.sqrt(2))/27
check('K18 self-dual amplitude',eq(R.subs(d,1),Rmin),s.simplify(R.subs(d,1)))
active_d=s.Integer(2) if MUTATE else s.Integer(1)
check('K19 physical gap baseline',eq(R.subs(d,active_d),Rmin),s.simplify(R.subs(d,active_d)))
Z=s.symbols('Z',positive=True)
check('K20 common loop factor cancellation',eq((Z*C0)*(Z*C3)**2/(Z*C2)**3,R),'Z^(1+2-3)=1')
src,Omega=s.symbols('src Omega',positive=True)
G=src**2/(2*Omega*C2)
a0=2*src*C2/(3*C3)
xi=s.factor(a0*a0/(G*C0))
check('K21 actual source normalization',eq(xi,8*Omega/(9*R)),xi)
delta=s.symbols('delta',positive=True)
active_energy=energy+delta*t*t if MUTATE else energy
stiff=s.limit(s.diff(active_energy,t,2),t,0,dir='+')
check('K22 critical stiffness baseline',eq(stiff),stiff)
Mass,vel,rad=s.symbols('Mass vel rad',positive=True)
hprofile=s.sqrt(G*Mass*a0)/(src*rad)
check('K23 source adiabatic ratio',eq(vel/(y*hprofile*rad),vel*src/(y*s.sqrt(G*Mass*a0))),'independent of radius, depends on mass')
z,Delta,k=s.symbols('z Delta k',positive=True)
integrand=s.sqrt(k*k+z+Delta*Delta)-s.sqrt(k*k+z)
check('K24 paired integral derivative sign form',eq(s.diff(integrand,z),(1/s.sqrt(k*k+z+Delta*Delta)-1/s.sqrt(k*k+z))/2),'negative for Delta>0')
check('K25 paired integral convexity form',eq(s.diff(integrand,z,2),(1/(k*k+z)**s.Rational(3,2)-1/(k*k+z+Delta*Delta)**s.Rational(3,2))/4),'positive for Delta>0')
press_boundary=s.Rational(3,2)*A*L*L*(s.sqrt(L*L+Delta*Delta)-L)
boundary_k=s.Rational(3,2)*A*k*k*(s.sqrt(k*k+Delta*Delta)-k)
rho_integrand=3*A*k*(s.sqrt(k*k+Delta*Delta)-k)
p_integrand=s.Rational(3,2)*A*k*k*(k/s.sqrt(k*k+Delta*Delta)-1)
press_identity=eq(s.diff(boundary_k,k),rho_integrand+p_integrand) and eq(boundary_k.subs(k,0)) and eq(boundary_k.subs(k,L),press_boundary)
check('K26 pressure excludes vacuum',press_identity and eq((L*L+Delta*Delta)-L*L,Delta*Delta),'exact boundary identity; rho+p_parallel=(3A/2)L^2(sqrt(L^2+Delta^2)-L)>0')

Lam,sv,muchem,l4,uv=s.symbols('Lam sv muchem l4 uv',positive=True)
Am=uv/(2*l4)
R2=Lam*sv
Kmicro=Am+R2-2*R2*muchem**2/sv**2
l4witness=uv/(8*Lam*(muchem**2/sv+sv))
check('K27 positive local kinetic region',eq(Kmicro.subs(l4,l4witness),2*Lam*muchem**2/sv+5*Lam*sv),'2Lambda mu^2/s+5Lambda s>0')
qp=s.symbols('qp',real=True)
B0=Lam*sv
Cphase=B0+Lam*qp**2/sv
Dphase=Am+B0
Keff=Am+B0-Lam*muchem**2/sv+muchem**2/l4
mix=2*Lam*muchem*qp/sv
P1=s.factor((B0-Cphase)*(Keff-Dphase)-mix**2/4)
check('K28 characteristic value at light cone',eq(P1,-Lam*muchem**2*qp**2/(sv*l4)),P1)
check('K29 relaxed kinetic dominance',eq(Keff-Kmicro,Lam*muchem**2/sv+muchem**2/l4),'positive')
m=s.symbols('m',positive=True)
smu=s.sqrt(qp**2-muchem**2+m*m)
ncharge=muchem*((muchem**2-m*m)/l4+2*Lam*smu)
chi_expected=(muchem**2-m*m+2*muchem**2)/l4+2*Lam*smu-2*Lam*muchem**2/smu
check('K30 charge susceptibility derivative',eq(s.diff(ncharge,muchem),chi_expected),chi_expected)
chi=(uv+2*muchem**2)/l4+2*Lam*sv-2*Lam*muchem**2/sv
check('K31 charge susceptibility positive form',eq(chi,2*Kmicro+2*muchem**2/l4+2*Lam*muchem**2/sv),'positive on K_micro>0 branch')
Tv,W,Cpar=s.symbols('Tv W Cpar',nonnegative=True)
F=(Tv-W)/2+Cpar*(Tv-W)**3
check('K32 parent velocity-space energy',eq(2*Tv*s.diff(F,Tv)-F,(Tv+W)/2+Cpar*(Tv-W)**2*(5*Tv+W)),'nonnegative for Tv,W,Cpar>=0')
aa,yy=s.symbols('aa yy',positive=True)
gap_eq=Lam**4*sv**4*yy**2*(yy-aa)-(yy+aa)**7
check('K33 parent saddle',eq(gap_eq.subs({aa:0,yy:Lam*sv})),0)
slope=-s.diff(gap_eq,aa)/s.diff(gap_eq,yy)
check('K34 parent finite-cutoff slope',eq(slope.subs({aa:0,yy:Lam*sv}),-2),-2)
ztime,rr=s.symbols('ztime rr',positive=True)
Ftime=ztime*rr**2/2+Lam**4*ztime**3/(6*rr**6)
check('K35 timelike radial grand-potential sign',eq(s.diff(Ftime,rr,2).subs(rr,s.sqrt(Lam*s.sqrt(ztime))),8*ztime),'L_rr=8Z>0, grand potential curvature negative')
coupling,GN=s.symbols('coupling GN',positive=True)
a_sf=coupling**3/(8*s.pi*GN*Lam)
active_c=2*coupling if MUTATE else coupling
check('K36 superfluid source baseline',eq(a_sf.subs(coupling,active_c),a_sf),s.factor(a_sf.subs(coupling,active_c)/a_sf))

fi,baux,gam,Y,H=s.symbols('fi baux gam Y H',positive=True)
faux=fi*Y/(Y+baux)
hY=s.sqrt(gam/(fi*baux))*Y*(Y+baux)
Uaux=faux*H**2/2-gam*Y**3/6
Caux=s.diff(Uaux,Y)
check('K37 auxiliary stationarity',eq(Caux.subs(H,hY)),0)
Eaux=s.factor(Uaux.subs(H,hY))
check('K38 positive reduced energy',eq(Eaux,gam*Y**3*(3*Y+2*baux)/(6*baux)),Eaux)
Dp=s.factor(s.diff(Eaux,Y)/s.diff(hY,Y))
trans=s.factor(Dp/hY)
longaux=s.factor(s.diff(Dp,Y)/s.diff(hY,Y))
check('K39 constrained transverse Hessian',eq(trans,fi*Y/(Y+baux)),trans)
check('K40 constrained longitudinal Hessian',eq(longaux,fi*2*Y/(2*Y+baux)),longaux)
C3aux=s.limit(Eaux/hY**3,Y,0)
C2aux=s.limit(Eaux/hY**2,Y,s.oo)
check('K41 constrained IR cubic',eq(C3aux,fi**s.Rational(3,2)/(3*s.sqrt(gam)*baux**s.Rational(3,2))),C3aux)
check('K42 constrained UV quadratic',eq(C2aux,fi/2),C2aux)
Ac=s.factor(-s.diff(Caux,Y).subs(H,hY))
check('K43 second-class curvature',eq(Ac,gam*Y*(2*Y+baux)/(Y+baux)),Ac)
eta=s.symbols('eta',positive=True)
check('K44 positive regulator tachyon',s.ask(s.Q.negative(-Ac/eta)) is True,-Ac/eta)
check('K45 source displacement',eq(Dp,s.sqrt(gam*fi/baux)*Y**2),Dp)
D=s.symbols('D',positive=True)
hinv=D/fi+(gam*baux**3/fi**3)**s.Rational(1,4)*s.sqrt(D)
check('K46 source inverse exact',eq(hinv.subs(D,Dp),hY),s.simplify(hinv.subs(D,Dp)-hY))
Gaux=src**2/(Omega*fi)
aaux=src*s.sqrt(gam*baux**3/fi)
check('K47 attractive MOND source',eq(src*hinv.subs(D,src*Mass/(Omega*rad**2)),Gaux*Mass/rad**2+s.sqrt(aaux*Gaux*Mass/rad**2)),'g=gN+sqrt(a0 gN)')
ep0=s.symbols('ep0',positive=True)
Raux=s.factor(ep0*C3aux**2/C2aux**3)
check('K48 constrained amplitude',eq(Raux,8*ep0/(9*gam*baux**3)),Raux)
Y0,J=s.symbols('Y0 J',positive=True)
vac=(Uaux+J*Y).subs({H:0,Y:Y0,J:gam*Y0**2/2},simultaneous=True)
check('K49 FI same-sector vacuum',eq(vac,gam*Y0**3/3),vac)
f0=fi*Y0/(Y0+baux)
active_Y0=baux if MUTATE else s.Integer(0)
check('K50 FI infrared stiffness baseline',eq(f0.subs(Y0,active_Y0)),f0.subs(Y0,active_Y0))
Rnom=s.factor(Raux.subs(ep0,vac))
check('K51 FI nominal ratio',eq(Rnom,s.Rational(8,27)*(Y0/baux)**3),Rnom)
check('K52 nominal target loses cubic window',48*3>125,'pi>3 implies (48pi)^(1/3)>5; true IR already quadratic')
p,mgap=s.symbols('p mgap',positive=True)
bubble_sub=(p*p+4*mgap*mgap)/(4*s.pi*p)*s.atan(p/(2*mgap))-mgap/(2*s.pi)
check('K53 continuum nonlocal bubble limit',eq(s.limit(bubble_sub,mgap,0,dir='+'),p/8),'Pi(p,0)-Pi(0,0)=p/8; continuum infrared only')

files=['FROZEN_CRITERIA.md','VERIFICATION_SCOPE.md','PROOF.md','checks.py']
hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in files}
failed=[row['name'] for row in rows if not row['passed']]
print(f"{len(rows)-len(failed)}/{len(rows)} PASS; failures={failed}; mode={'MUTATE' if MUTATE else 'normal'}")
result={'mode':'MUTATE' if MUTATE else 'normal','checks':rows,'input_sha256':hashes,'sympy':s.__version__,
        'non_claims':['No forced amplitude ratio','No full healthy microscopic completion','No numerical target search']}
(ROOT/sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
sys.exit(1 if failed else 0)
