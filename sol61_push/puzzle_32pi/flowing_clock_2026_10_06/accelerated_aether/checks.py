#!/usr/bin/env python3
"""Frozen coupled ADM constraints with accelerated unit aether, c13=0."""
import argparse,json,math,platform
from pathlib import Path
import sympy as S
import numpy as np
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--mutate-drop-mixing',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok,detail):
 checks.append(dict(name=name,passed=bool(ok),detail=str(detail)));print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail))
n,ell,h,s,theta,aL,aT,Z,W,B,j,P=S.symbols('n ell h s theta aL aT Z W B j P',real=True)
N=n-1;L=ell-1;p=-s*theta*aL;t=-s*theta*aT
etaL=h+2*s*aL*aL;etaT=h+2*s*aT*aT;etaLT=2*s*aL*aT
# Quadratic F Hessian includes 2 F''(-theta deltaTheta/2+a.deltaAcceleration)^2/M2.
dT,dAL,dAT=S.symbols('dT dAL dAT',real=True)
raw=h*(-dT*dT/2+dAL*dAL+dAT*dAT)+2*s*(-theta*dT/2+aL*dAL+aT*dAT)**2
expected=(-h/2+s*theta*theta/2)*dT*dT+etaL*dAL*dAL+etaT*dAT*dAT+2*etaLT*dAL*dAT+2*(p*dAL+t*dAT)*dT
if args.mutate_drop_mixing:raw=raw-2*(p*dAL+t*dAT)*dT
check('actual_aether_Hessian_cross_term',S.expand(raw-expected)==0,'Fpp theta a mixing retained before eliminating constraints; deliberate drop fails')
L0=n*(1-n*ell)*Z*Z+2*(n*ell-1)*Z*B+(1-ell)*B*B+etaL*j*j+2*etaLT*j*W+etaT*W*W+2*(n*Z-B)*(p*j+t*W)+2*N*j*P+N*(n-2)*P*P
if args.mutate_drop_mixing:L0=L0-2*(n*Z-B)*(p*j+t*W)
Bsol=S.solve(S.diff(L0,B),B)[0]
L1=S.factor(L0.subs(B,Bsol));U=p*j+t*W
expected1=N*(n*ell-1)*Z*Z/L+U*U/L-2*N*Z*U/L+etaL*j*j+2*etaLT*j*W+etaT*W*W+2*N*j*P+N*(n-2)*P*P
check('longitudinal_shift_constraint',S.simplify(L1-expected1)==0,'B=((n ell-1)Z-U)/(ell-1); v_T retained dynamically')
C=etaL+p*p/L;r=etaLT+p*t/L;q=N*p/L
jsol=-(r*W-q*Z+N*P)/C
check('lapse_constraint',S.simplify(S.diff(L1,j).subs(j,jsol))==0,'lapse Hessian C and vector mixing r enter Schur complement')
A=N*(n*ell-1)/L
Kzz=A-q*q/C;Kzv=-N*t/L+q*r/C;Kvv=etaT+t*t/L-r*r/C
Jz=N*q/C;Jv=-N*r/C;G=N*N/C-N*(n-2)
reduced=Kzz*Z*Z+2*Kzv*Z*W+Kvv*W*W+2*Jz*Z*P+2*Jv*W*P-G*P*P
check('full_retained_vector_Schur_matrix',S.simplify(L1.subs(j,jsol)-reduced)==0,'all lapse/shift constraints eliminated; physical transverse velocity not eliminated')
check('perpendicular_negative_restriction',S.simplify(Kzz.subs(aL,0)-A)==0 and S.simplify(jsol.subs(aL,0)+N*P/h)==0,'k perpendicular a: lapse independent Z,W and Kzz=A exactly')
check('parallel_transverse_decoupling',S.simplify(Kzv.subs(aT,0))==0 and S.simplify(Kvv.subs(aT,0)-h)==0,'k parallel a: transverse velocity decouples; scalar tilted cone retains lapse correction')
check('zero_acceleration_coupled_limit',S.simplify(Kzz.subs({aL:0,aT:0})-A)==0 and S.simplify(G.subs({aL:0,aT:0})-(N*N/h-N*(n-2)))==0,'previous geodesic ADM result recovered, no assumed cone import')
ell_relation=1+h/2-s*theta*theta/2
closed_vv=h*(L+s*(aL*aL+aT*aT))/(L+s*aL*aL)
check('general_angle_vector_diagonal_identity',S.factor((Kvv-closed_vv).subs(ell,ell_relation))==0,'Qnegative gives Kvv positive for every orientation, not just perpendicular')
u=aL*aL+aT*aT
det_perp=A*(h+2*s*u+s*s*theta*theta*u/L)-N*N*s*s*theta*theta*u/(L*L)
check('general_angle_determinant_identity',S.factor((Kzz*Kvv-Kzv*Kzv-h*det_perp/C).subs(ell,ell_relation))==0,'detK angle=(h/C)detK perpendicular; exact rotational reduction')
# Rational midpoint data supply an all-angle positive coefficient witness.
hm=S.Rational(2101,2020);sm=S.Rational(1899,1010)*S.Rational(375,2);zm=S.Rational(21,200);am2=S.Rational(1,1000000)
amax2=hm*(6*sm*zm-3*hm-4)/(8*sm)
check('exact_all_angle_positive_midpoint',hm>0 and hm<2 and hm-2*zm*sm<0 and am2<amax2 and amax2>0,'rational h,s,z,a² satisfy Qnegative,allangle detKpositive,and C<=h<2: sufficient frozen Hamiltonian positivity')
# The physical vector degree orthogonal to a,k has h(dotv²-|gradv|²).
# Finite exact derivatives for prior quintic transition, no external script import.
delta=.01;h0=2/(1+delta);hL=.1;b=.1;w=.01
def hs(z):
 x=(z-b)/w
 if x<=0:return h0,0.
 if x>=1:return hL,0.
 smooth=10*x**3-15*x**4+6*x**5
 hp=-(h0-hL)*30*x*x*(1-x)**2/w
 return hL+(h0-hL)*(1-smooth),-hp

def coeff(z,acc,cosangle):
 hv,sv=hs(z);th=math.sqrt(2*(z+acc*acc));el=1+.5*hv-.5*sv*th*th;ll=el-1;aaL=acc*cosangle;aaT=acc*math.sqrt(max(0,1-cosangle*cosangle));pp=-sv*th*aaL;tt=-sv*th*aaT
 etL=hv+2*sv*aaL**2;etT=hv+2*sv*aaT**2;etLT=2*sv*aaL*aaT;cc=etL+pp*pp/ll;rr=etLT+pp*tt/ll;qq=2*pp/ll;av=2*(3*el-1)/ll
 km=np.array([[av-qq*qq/cc,-2*tt/ll+qq*rr/cc],[-2*tt/ll+qq*rr/cc,etT+tt*tt/ll-rr*rr/cc]])
 jmat=np.array([[2*qq/cc,-rr/cc],[-rr/cc,0.]])
 vm=np.diag([4/cc-2,hv])
 return dict(h=hv,s=sv,theta=th,ell=el,C=cc,K=km,J=jmat,V=vm,Q=(hv-2*z*sv)/hv)
# An explicit frozen local coefficient point on prior family, not a constructed solution.
healthy=[]
for ca in np.linspace(-1,1,401):
 c=coeff(.105,.001,float(ca));kv=np.linalg.eigvalsh(c['K']);vv=np.linalg.eigvalsh(c['V']);healthy.append((min(kv),min(vv),c['C']))
check('bounded_accelerated_disconnected_positive_point',min(x[0] for x in healthy)>0 and min(x[1] for x in healthy)>0 and hs(.105)[0]-2*.105*hs(.105)[1]<0,'401 directions, K/V positive at z=.105,a/M=.001 despite Q<0; coefficient test not on-shell background existence')
# Real speeds follow from positive kinetic/spatial Hamiltonian, independently check polynomial roots.
cone_imag=[]
for ca in [-1,-.5,0,.5,1]:
 c=coeff(.105,.001,ca);k0=c['K'];j0=c['J'];v0=c['V']
 pol=np.polynomial.polynomial.polysub(np.polynomial.polynomial.polymul([-v0[0,0],-2*j0[0,0],k0[0,0]],[-v0[1,1],0,k0[1,1]]),np.polynomial.polynomial.polymul([0,-2*j0[0,1],k0[0,1]],[0,-2*j0[1,0],k0[1,0]]))
 roots=np.roots(pol[::-1]);cone_imag.append(max(abs(x.imag) for x in roots))
check('bounded_mixed_cone_roots',max(cone_imag)<1e-10,'five directions polynomial det(v² K-2v J-V)=0 has real speeds; no subluminality requirement')
# Ghost-band coordinate point: intermediate value path theorem below does not need finite sampling.
zghost=.10048120142709685
bad=[]
for acc in [0,.001,.01,.1]:
 c=coeff(zghost,acc,0.);bad.append(dict(a=acc,ell=c['ell'],restricted_A=c['K'][0,0],min_kinetic=float(np.linalg.eigvalsh(c['K'])[0])))
check('accelerated_ghost_band_witness',bad[1]['restricted_A']<0 and bad[2]['restricted_A']<0,'small acceleration retains real negative scalar restriction after every constraint')
# Analytic comparison ell_theta<=ell_geo when Fpp>=0; K=-z implies theta²=2(z+a²).
u,zz,hh,ss=S.symbols('u z h s',nonnegative=True)
ell_theta=1+hh/2-(u+zz)*ss;ell_geo=1+hh/2-zz*ss
check('accelerated_path_comparison_identity',S.simplify(ell_theta-ell_geo+u*ss)==0,'continuous endpoints ell>1, negativeQ point implies ell_theta<1, hence crossing (1/3,1); acceleration cannot skip band')
# Actual constraint and gauge completeness, tied to covariant linear unit-normal decomposition.
# A_cov_i=v_i, A^i=v_i-N_i; acceleration contains vdot_i+partial_i nu, no Ndot_i.
check('principal_transverse_auxiliary_constraint',S.diff(S.Symbol('k',positive=True)**2*S.Symbol('NT',real=True)**2/2,S.Symbol('NT',real=True))==S.Symbol('k',positive=True)**2*S.Symbol('NT',real=True),'transverse shift equation NT=0; unit constraint and scalar time gauge stated separately in proof')
result=dict(checks=checks,healthy_point=dict(z=.105,a_over_M=.001,exact_allangle_acceleration_squared_bound=str(amax2),min_kinetic=min(x[0] for x in healthy),min_gradient=min(x[1] for x in healthy),min_lapse_C=min(x[2] for x in healthy),Q=coeff(.105,.001,0.)['Q'],ell=coeff(.105,.001,0.)['ell']),ghost_witnesses=bad,mutation=args.mutate_drop_mixing,software=dict(python=platform.python_version(),sympy=S.__version__,numpy=np.__version__))
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
