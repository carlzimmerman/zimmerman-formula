"""Exact de Sitter quadratic reduction and bounded mode trajectory checks."""
import argparse
import json
import math
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
# One real periodic Fourier mode; cos(theta)=c, sin²(theta)=1-c².
eps,c=s.symbols('eps c',real=True)
z,zd,n,chi,Q,Qd,H,X=s.symbols('z zd n chi Q Qd H X',real=True)
B,t,t2,m0,kap,ms=s.symbols('B t t2 m0 kap ms',real=True)
S=3*B+2
lam=1+B+eps*t*Q*c+s.Rational(1,2)*eps**2*t2*Q**2*c**2
f=H+eps*zd*c+eps**2*chi*z*(1-c**2)
shift=eps*chi*c
volume=s.exp(3*eps*z*c)/(1+eps*n*c)
extrinsic=volume*((f-shift)**2+2*f**2-lam*(3*f-shift)**2)
potential=-(1+eps*n*c)*s.exp(3*eps*z*c)*(3*S*H**2-9*H**2*t*eps*Q*c+eps**2*m0*Q**2*c**2)
quadratic=s.expand(s.series(extrinsic+potential,eps,0,3).removeO().coeff(eps,2))
poly=s.Poly(quadratic,c)
averaged=0
for (power,),coef in poly.terms():
    if power==0: averaged+=coef
    elif power==2: averaged+=coef/2
    else: assert power==1
raw=s.expand(2*averaged+Qd**2-(X+m0)*Q**2+m0*Q**2+X*(2*z*z+4*n*z+2*n*n)-16*kap*X**2*z*z/ms**2)
# This is normalized by M²/2 and by the average cos²=1/2.
mfixed=m0+s.Rational(9,2)*H**2*t2
u=zd-H*n
expected=-3*S*u*u+2*S*u*chi-B*chi*chi-18*H*t*Q*u+6*H*t*Q*chi+Qd**2-(X+mfixed)*Q**2+X*(2*z*z+4*n*z+2*n*n)-16*kap*X**2*z*z/ms**2
boundary=-18*S*H*z*zd-27*S*H**2*z*z
check('direct periodic ADM quadratic expansion',s.simplify(raw-expected-boundary)==0)
chi_sol=(S*u+3*H*t*Q)/B
Ak=2*S/B
b=6*H*t/B
d=9*H**2*t*t/B
shift_reduced=s.simplify(expected.subs(chi,chi_sol))
target=Ak*u*u+2*b*Q*u+d*Q*Q+Qd**2-(X+mfixed)*Q**2+X*(2*z*z+4*n*z+2*n*n)-16*kap*X**2*z*z/ms**2
check('shift elimination',s.simplify(shift_reduced-target)==0)
D=Ak*H*H+2*X
nsol=(Ak*H*zd+b*H*Q-2*X*z)/D
lap=s.simplify(target.subs(n,nsol))
compact=Ak*zd*zd+2*b*Q*zd-(Ak*H*zd+b*H*Q-2*X*z)**2/D+Qd**2-(X+mfixed-d)*Q**2+2*X*z*z-16*kap*X**2*z*z/ms**2
check('lapse elimination',s.simplify(lap-compact)==0)
K=2*Ak*X/D
g=2*b*X/D
J=2*b*H*X*(Ak*H*H-2*X)/D**2
Vz=8*Ak*H*H*X*X/D**2+16*kap*X*X/ms**2
Nq=X+mfixed-d+b*b*H*H/D
Cself=4*Ak*H*X/D
selfdot=-2*H*X*s.diff(Cself,X)
check('redshifting self-boundary potential',s.simplify((2*X-4*X*X/D)-(3*H*Cself+selfdot)/2+Vz-16*kap*X*X/ms**2)==0)
gdot=-2*H*X*s.diff(g,X)
check('redshifting mixed-boundary potential',s.simplify(4*b*H*X/D-3*H*g-gdot-J)==0)
check('reduced kinetic coefficient',s.simplify(s.diff(compact,zd,2)/2-K)==0)
mhom=mfixed-d+b*b/Ak
check('homogeneous mass matches constraint reduction',s.simplify(mhom-(mfixed-27*H**2*t*t/S))==0)
zd2=-H*(3-2*Ak*H*H/D)*zd-(4*H*H*X/D+8*kap*X*D/(Ak*ms**2))*z-b/Ak*Qd-4*b*H*X/(Ak*D)*Q
qd2=-3*H*Qd+g*zd-Nq*Q+2*b*H*X/D*z
C=(zd+H*z+b/Ak*Q)/D
Cdot=s.diff(C,z)*zd+s.diff(C,zd)*zd2+s.diff(C,Q)*Qd-2*H*X*s.diff(C,X)
check('triangular clock first integral',s.simplify(Cdot+8*kap*X*z/(Ak*ms**2))==0)
check('triangular canonical scalar equation',s.simplify(qd2+3*H*Qd+(X+mhom)*Q-2*b*C*X)==0)
# Positive-potential determinant identity; independent free symbols.
aa,bb,hh,xx,mm=s.symbols('aa bb hh xx mm',positive=True)
tt=aa*hh**2; dd=tt+2*xx
nn=xx+mm+bb*bb*hh*hh/dd
vz=8*aa*hh*hh*xx*xx/dd**2
jj=2*bb*hh*xx*(tt-2*xx)/dd**2
factor=8*aa*xx*dd**2+(8*aa*mm-bb*bb)*dd**2+8*bb*bb*tt*(tt+3*xx)
check('positive determinant decomposition',s.simplify(vz*nn-jj*jj/4-hh*hh*xx*xx*factor/dd**4)==0)
check('linear coupling mixing margin identity',s.simplify(b*b/(8*Ak)-d/(4*S))==0)
q,A0,B0,Z=s.symbols('q A0 B0 Z',positive=True)
Up=-2*A0/q**3+2*B0*q
Up2=6*A0/q**4+2*B0
check('linear coupling positive mass floor',s.simplify((Up2+2*Up/q)/Z-(2*A0/q**4+6*B0)/Z)==0)

rows=[]
GRID=np.linspace(0,16,801)
for ell in (1.,10.):
    qs=brentq(lambda q:-2/q**3+2*q+3*ell*(q**-2+q*q)/(2+3*ell*q),3**(-0.25),1)
    SS=2+3*ell*qs; BB=ell*qs
    HH=math.sqrt(2*(qs**-2+qs*qs)/(3*SS))
    AA=2*SS/BB; bb=6*HH*ell/BB; dd=9*HH*HH*ell*ell/BB
    mf=6/qs**4+2; mh=mf-dd+bb*bb/AA
    check('positive all-momentum mixing margin ell='+str(ell),mf-dd>bb*bb/(8*AA))
    for ratio in (0.1,1.,10.):
        X0=(ratio*HH)**2
        for kk in (0.,0.01):
            label=str((ell,ratio,kk))
            # Initial zeta=1,zeta_dot=0,Q=0.1,Qdot=0.
            C0=(HH+bb/AA*0.1)/(AA*HH*HH+2*X0)
            def triangular(n,y):
                zz,cc,qq,ww=y
                x=X0*math.exp(-2*n); den=AA*HH*HH+2*x
                return [(cc*den-bb/AA*qq)/HH-zz,-8*kk*x*zz/(AA*HH),ww,-3*ww-(x+mh)*qq/(HH*HH)+2*bb*cc*x/(HH*HH)]
            sol=solve_ivp(triangular,(0,16),[1.,C0,0.1,0.],method='DOP853',rtol=1e-9,atol=1e-11,max_step=0.05,t_eval=GRID)
            check('mode integration completed '+label,sol.success and sol.t[-1]==16)
            zz,cc,qq,ww=sol.y
            derivatives=np.array([triangular(n,y) for n,y in zip(GRID,sol.y.T)])
            check('late scalar decay and finite metric '+label,abs(qq[-1])<1e-7 and abs(ww[-1])<1e-6 and abs(derivatives[-1,0])<1e-6 and np.all(np.isfinite(zz)))
            row={'ell':ell,'initial_k_over_H':ratio,'kappa':kk,'Q_final':float(qq[-1]),'zeta_final':float(zz[-1]),'zeta_prime_final':float(derivatives[-1,0]),'largest_sampled_abs_zeta':float(np.max(np.abs(zz))),'largest_sampled_abs_Q':float(np.max(np.abs(qq))),'C_initial':C0,'C_final':float(cc[-1])}
            if kk==0:
                def direct(n,y):
                    z,v,q,w=y
                    x=X0*math.exp(-2*n); den=AA*HH*HH+2*x
                    gg=2*bb*x/den; nq=x+mf-dd+bb*bb*HH*HH/den
                    return [v,-(3-2*AA*HH*HH/den)*v-4*x/den*z-bb/(AA*HH)*w-4*bb*x/(AA*HH*den)*q,w,-3*w+gg/HH*v-nq/(HH*HH)*q+2*bb*x/(HH*den)*z]
                alt=solve_ivp(direct,(0,16),[1.,0.,0.1,0.],method='DOP853',rtol=2e-10,atol=2e-12,max_step=0.05,t_eval=GRID)
                difference=float(max(np.max(np.abs(alt.y[0]-zz)),np.max(np.abs(alt.y[2]-qq))))
                check('direct-equation comparison '+label,alt.success and difference<1e-7)
                check('conserved C without stabilizer '+label,float(np.max(np.abs(cc-C0)))<1e-12)
                row['direct_equation_max_absolute_field_difference']=difference
            rows.append(row)
result={'passed':all(c['passed'] for c in checks),'checks':checks,'mode_samples':rows}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
for c in checks:
    if not c['passed']: print(c)
for row in rows: print(json.dumps(row))
raise SystemExit(0 if result['passed'] else 1)
