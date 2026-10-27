#!/usr/bin/env python3
"""Portable exact round-2 algebra. No repository imports, networking or data loads.
Usage: python3 checks.py --output /absolute/path/results.json
"""
import argparse
import json
import platform
from pathlib import Path
import sympy as s

ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
records={}
def check(name,ok,detail=''):
    records[name]={'passed':bool(ok),'detail':str(detail)}
    if not ok: raise AssertionError(name+': '+str(detail))
def zero(name,expr):
    result=s.factor(s.simplify(expr)); check(name,result==0,result)

K,beta,eta,gamma,H,a,p,k,a0,Lambda=s.symbols(
    'K beta eta gamma H a p k a0 Lambda',positive=True)
A=2+3*beta; B=K*A/beta; C=A/(K*beta)
N,ad,add,Nd=s.symbols('N adot addot Ndot',positive=True)
Lbg=-3*A*a*ad**2/(4*K*N)-Lambda*N*a**3/(2*K)
zero('background_lapse',s.diff(Lbg,N).subs({N:1,ad:a*H})-a**3*(3*A*H**2-2*Lambda)/(4*K))
ELa=s.diff(Lbg,a)-(s.diff(s.diff(Lbg,ad),a)*ad+s.diff(s.diff(Lbg,ad),ad)*add+s.diff(s.diff(Lbg,ad),N)*Nd)
zero('background_scale_factor',ELa.subs({N:1,Nd:0,ad:a*H,add:a*H**2})-3*a*a*(3*A*H*H-2*Lambda)/(4*K))
Lbeta=-9*beta*a*ad**2/(4*K*N)
rho_beta=-s.diff(Lbeta,N)/a**3
zero('beta_density',rho_beta.subs({N:1,ad:a*H})+9*beta*H*H/(4*K))
zero('S1_linked_background', (2*Lambda/(3*A)).subs(Lambda,32*s.pi*a0*a0)-64*s.pi*a0*a0/(3*A))

# Direct geometric expansion for a real x-directed scalar mode.
# Angle variables cc,ss stand for cos(kx),sin(kx). At second order only
# cc² and ss² survive the average; multiply by two for normalized mode action.
eps,z,zd,n,Y,cc,ss=s.symbols('eps z zd n Y cc ss',real=True)
zeta=eps*z*cc; lapse=1+eps*n*cc
q0=H+eps*zd*cc+eps**2*Y*z*ss**2
X=eps*Y*cc
kin=-3*A*q0*q0+2*A*q0*X-beta*X*X
Rpiece=(1+eps*n*cc)*s.exp(zeta)*(4*eps*p*p*z*cc-2*eps**2*p*p*z*z*ss**2)
Lgeo=s.exp(3*zeta)*kin/lapse-2*Lambda*lapse*s.exp(3*zeta)+Rpiece
second=s.expand(s.series(Lgeo,eps,0,3).removeO()).coeff(eps,2)
avg2=s.expand(second).subs({cc**2:s.Rational(1,2),ss**2:s.Rational(1,2),cc:0,ss:0})*2
avg2=s.expand(avg2.subs(Lambda,s.Rational(3,2)*A*H*H))
# Integrate the z*zd cross term with weight a³ at constant H.
cross=s.expand(avg2).coeff(z,1).coeff(zd,1)
after_ibp=s.expand(avg2-cross*z*zd-s.Rational(3,2)*H*cross*z*z)
expected=-3*A*(zd-H*n)**2+2*A*(zd-H*n)*Y-beta*Y*Y+2*p*p*z*z+4*p*p*n*z
zero('direct_ADM_quadratic',after_ibp-expected)

sig,sd,Z,Zd=s.symbols('sigma sigmadot Z Zdot',real=True)
Lg=expected/(4*K)
LP=p*p*n*sig+eta*p*p*sd*sd/2-K*p*p*sig*sig/2-gamma*p**4*sig*sig/2
LY=Lg+LP
Ysol=s.solve(s.diff(LY,Y),Y)[0]
zero('scalar_shift_solution',Ysol-A*(zd-H*n)/beta)
L1=s.factor(LY.subs(Y,Ysol))
expected1=C*(zd-H*n)**2/2+p*p*z*z/(2*K)+p*p*n*(z/K+sig)+eta*p*p*sd*sd/2-K*p*p*sig*sig/2-gamma*p**4*sig*sig/2
zero('shift_reduced_scalar',L1-expected1)
nsol=s.solve(s.diff(L1,n),n)[0]
zero('scalar_lapse_solution',nsol-zd/H+p*p*(z/K+sig)/(C*H*H))
L2=s.expand(L1.subs(n,nsol).subs({z:K*(Z-sig),zd:K*(Zd-sd)}))
zzd=s.expand(L2).coeff(Z,1).coeff(Zd,1)
# coefficient is K*p²/H; derivative of a³p² is H a³p².
zero('ZZdot_coefficient',zzd-K*p*p/H)
L2ibp=s.expand(L2-zzd*Z*Zd-H*zzd*Z*Z/2)
expected2=eta*p*p*sd*sd/2-K*p*p*Z*(sd+H*sig)/H-gamma*p**4*sig*sig/2-p**4*Z*Z/(2*C*H*H)
zero('post_lapse_auxiliary_action',L2ibp-expected2)
Zsol=s.solve(s.diff(L2ibp,Z),Z)[0]
zero('remaining_auxiliary_solution',Zsol+C*K*H*(sd+H*sig)/p**2)
L3=s.factor(L2ibp.subs(Z,Zsol))
zero('deSitter_reduced_square_form',L3-(eta*p*p*sd*sd+B*(sd+H*sig)**2-gamma*p**4*sig*sig)/2)
Q=B+eta*p*p; V=gamma*p**4+2*B*H*H
Lstandard=s.expand(L3-B*H*sig*sd-s.Rational(3,2)*B*H*H*sig*sig)
zero('deSitter_reduced_standard_form',Lstandard-(Q*sd*sd-V*sig*sig)/2)
Qdot=s.diff(Q,p)*(-H*p); Vdot=s.diff(V,p)*(-H*p)
friction=s.factor(3*H*Q+Qdot)
zero('scalar_friction',friction-H*(3*B+eta*p*p))
sdd=-(friction*sd+V*sig)/Q
Edot=s.factor(Qdot*sd*sd/2+Q*sd*sdd+Vdot*sig*sig/2+V*sig*sd)
zero('scalar_Lyapunov_identity',Edot+H*(3*B+2*eta*p*p)*sd*sd+2*H*gamma*p**4*sig*sig)
check('scalar_positive_Q_and_V',Q.is_positive and V.is_positive,'All K,beta,eta,gamma,H,p positive; exact algebraic domain.')

# Frobenius endpoint controls: coefficients through the first nontrivial orders.
r=s.symbols('r',real=True)
indicial=s.factor(r*(r-1)-2*r+2)
zero('late_time_indicial',indicial-(r-1)*(r-2))
def ODEp(f): return s.expand((B+eta*p*p)*p*p*s.diff(f,p,2)-2*B*p*s.diff(f,p)+(2*B+gamma*p**4/(H*H))*f)
branch1=p*(1-gamma*p**4/(12*B*H*H))
branch2=p*p*(1-eta*p*p/(3*B))
zero('branch1_residual_through_p5',s.series(ODEp(branch1),p,0,7).removeO())
zero('branch2_residual_through_p4',s.series(ODEp(branch2),p,0,6).removeO())
zfrom=lambda f: -B*H*((-H*p*s.diff(f,p))+H*f)/(p*p)-K*f
zero('branch1_metric_decays',s.limit(zfrom(branch1),p,0))
zero('branch2_metric_finite',s.limit(zfrom(branch2),p,0)-B*H*H)

# Exactly k=0 metric scalar is rederived before any division by k.
Lhom=-3*A*(zd-H*n)**2/(4*K)
nhom=s.solve(s.diff(Lhom,n),n)[0]
zero('homogeneous_metric_lapse',nhom-zd/H)
zero('homogeneous_metric_on_constraint',Lhom.subs(n,nhom))
P0,Pd=s.symbols('P0 Pdot',real=True)
PTmass=K+gamma*p*p
Pdd=-H*Pd-PTmass*P0/eta
ETdot=s.factor(eta*Pd*Pdd+(-2*H*gamma*p*p)*P0*P0/2+PTmass*P0*Pd)
zero('transverse_and_homogeneous_energy',ETdot+eta*H*Pd*Pd+H*gamma*p*p*P0*P0)
zero('homogeneous_P_frequency',PTmass.subs(p,0)/eta-K/eta)

# Arbitrary-angle complete shift elimination in the static principal system.
PL,PT1,PT2,qd=s.symbols('PL PT1 PT2 qdot',real=True)
pv=s.Matrix([PL,PT1,PT2]); S0=s.diag(-beta/(2*K),1/(4*K),1/(4*K))
Delta=1-2*K*eta*PL*PL/beta+4*K*eta*(PT1*PT1+PT2*PT2)
SM=S0+eta*pv*pv.T
ysol=eta*S0.inv()*pv*qd/Delta
for i in range(3): zero('oblique_shift_equation_'+str(i),(SM*ysol-eta*pv*qd)[i])
zero('oblique_shift_determinant',s.det(SM)-s.det(S0)*Delta)
Lob=s.factor(eta*(qd-(pv.T*ysol)[0])**2/2+(ysol.T*S0*ysol)[0]/2)
zero('oblique_reduced_kinetic',Lob-eta*qd*qd/(2*Delta))
nullvec=S0.inv()*pv
# Matrix applied to this vector equals Delta*P exactly: zero at Delta=0.
for i in range(3): zero('rank_locus_null_vector_'+str(i),(SM*nullvec)[i]-Delta*pv[i])
zero('rank_locus_compatibility', (nullvec.T*(eta*pv*qd))[0]-(Delta-1)*qd)
u,ssq=s.symbols('u sin_squared_theta',nonnegative=True)
Dangle=s.expand(Delta.subs({PL*PL:u*u*(1-ssq)/(K*K),PT1*PT1:u*u*ssq/(K*K),PT2:0}))
r0=2*eta*u*u/(K*beta)
zero('angular_margin_formula',Dangle-(1-r0+(1+2*beta)*r0*ssq))
check('forbidden_principal_example',Delta.subs({K:1,eta:1,beta:1,PL:1,PT1:0,PT2:0})==-1,'a0=2, u=1 is inside cap; beta=eta=K=gamma=1.')
zero('maximum_nontensor_speed', ((gamma/eta)*Delta).subs({PL:0,PT1:u/K,PT2:0})-(gamma/eta)*(1+4*eta*u*u/K))

# Critical quadratic and direct cubic, independent of quadratic reduction.
Wu=a0*a0*(-u/a0-s.log(1-u/a0))/K
series=s.series(Wu,u,0,4).removeO()
zero('W_quadratic_and_cubic',series-u*u/(2*K)-u**3/(3*K*a0))
amp=s.symbols('u_amplitude',positive=True)
RW=2*K*p*p*amp/(3*a0*(gamma*p**4+2*B*H*H))
peak=(2*B*H*H/gamma)**s.Rational(1,4)
zero('direct_cubic_envelope_peak',s.diff(RW,p).subs(p,peak))
zero('direct_cubic_envelope_max',RW.subs(p,peak)-K*amp/(3*a0*H*s.sqrt(2*B*gamma)))
check('negative_eta_mutation_detected',Q.subs({K:1,beta:1,eta:-1,p:3})<0,'Wrong electric sign makes scalar Q=5-9<0.')
check('negative_gamma_mutation_detected',V.subs({K:1,beta:1,H:1,gamma:-1,p:3})<0,'Wrong stiffness sign makes V=10-81<0.')

result={'status':'scoped exact identities verified; complete four-gate theory remains open',
 'software':{'python':platform.python_version(),'sympy':s.__version__},'checks_passed':len(records),'checks':records,
 'formulae':{'deSitter_H_squared':str(2*Lambda/(3*A)),'scalar_Q':str(Q),'scalar_V':str(V),
  'scalar_energy_derivative':str(Edot),'oblique_Delta':str(Delta),'oblique_Q':str(eta/Delta),
  'direct_cubic_envelope_bound':str(K*amp/(3*a0*H*s.sqrt(2*B*gamma)))},
 'domains':{'deSitter':'Exact P=0 pure-Lambda expanding solution; positive coefficients; nonzero Fourier k with physical p=k/a, plus separately derived homogeneous sector.',
  'polarized':'Frozen regular static clock-aligned principal system, fixed finite potential curvature, arbitrary angle; high-frequency limit only.'},
 'nonclaims':['No S3 mass/current embedding','No full nonlinear degree count or well-posedness','No quantum strong-coupling cutoff',
  'No low-frequency polarized halo stability','No arbitrary evolving-background principal theorem','No PPN/Solar-System test pass']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks_passed':len(records),'status':result['status']},indent=2))
