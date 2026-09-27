#!/usr/bin/env python3
"""Exact boosted weak-source response and independent local gyroscopic route."""
import argparse
import json
from pathlib import Path
import sympy as S

ap=S.ArgumentParser() if False else argparse.ArgumentParser()
ap.add_argument('--output',required=True)
args=ap.parse_args()
checks={}
def exact(name, value):
    value=S.factor(S.cancel(value))
    checks[name]={'residual':str(value),'passed':value==0}
    assert value==0,(name,value)
    print('PASS '+name,flush=True)

E,z,r,s,B,q,m,c,g,w,k,ka=S.symbols('E zeta r s B q v_squared cos_theta gamma omega k kappa',real=True)
kap=2*(2+3*B)/B
a=S.Matrix([1,s,r])
A=S.Matrix([[2,-2,0],[-2,E-z,-z],[0,-z,-z]])
Ai=A.inv()
ep=S.Matrix([1,0,0]);ef=S.Matrix([0,1,0])
delta=r-s
h=S.factor((a.T*Ai*a)[0])
src=kap*q*a/2-m*ep-ef
ax=S.factor((a.T*Ai*src)[0])
# R here already includes 16 pi G_bare.  The final two terms include shift and transverse-vector response.
H=S.factor(-((src.T*Ai*src)[0]-kap*q*ax**2/(1+kap*q*h))+q/B-2*(m-q))
H0=S.factor(H.subs({m:0,q:0}))
Hm=S.factor(S.diff(H,m).subs({m:0,q:0}))
Hq=S.factor(S.diff(H,q).subs({m:0,q:0}))
exact('static_normalization',H0-1/(2-E))
exact('transverse_order_v2',Hm-(2/(2-E)-2))
alpha1=S.factor(-2*(2+Hm/H0))
alpha2=S.factor(-1+Hq/H0)
target_a2=kap*((1-delta)**2/(2-E)-(1-delta))+(2-E)*(1/B+2)-1
exact('alpha1_independent_of_lapse_mixing',alpha1+4*E)
exact('alpha2_general_delta',alpha2-target_a2)
exact('alpha2_old_khronometric_limit',alpha2.subs({r:0,s:0})-E*(E-B+2*E*B)/(B*(2-E)))
# The exact boost: gamma^4/[1+(gamma^2-1)c^2]=1/[(1-m)(1-m+m c^2)].
boost_q=m*c*c/(1-m+m*c*c)
boost_H=H.subs(q,boost_q)
normalized=(2-E)*boost_H/((1-m)*(1-m+m*c*c))
exact('full_boost_static_limit',normalized.subs(m,0)-1)
exact('full_boost_order_v2',S.diff(normalized,m).subs(m,0)-(2*E+alpha2*c*c))
speed=2*E*(2-E)/(kap*(E-2*delta)**2)
exact('contact_free_PPN_speed_identity',alpha2-E*(1/speed-1)/2)
exact('completed_square_alpha2',alpha2-(kap*(E-2*delta)**2/(4*(2-E))-E/2))
exact('luminal_root_polynomial',(E-2*delta)**2-2*E*(2-E)/kap-4*((delta-E/2)**2-E*(2-E)/(2*kap)))

# A genuinely different local first-order term gamma(U V_N-lnN V_U) is gyroscopic.
# In the quadratic action it produces an antisymmetric phi/U block.
G=S.Matrix([[0,0,0],[0,0,1],[0,-1,0]])
D=E*(z-2*r*r)+2*r*r*z+4*r*r-4*r*(s+1)*z+2*z*s*s+4*z*s
detgyro=S.factor((k*k*A+ka*w*w*a*a.T+S.I*w*g*G).det())
pred=-ka*g*g*w**4-(ka*k**4*D+2*g*g*k*k)*w*w+2*z*(2-E)*k**6
exact('local_gyroscopic_two_pole_determinant',detgyro-pred)
exact('gyro_without_extension_recovers_one_pole',detgyro.subs(g,0)-k**4*(2*z*(2-E)*k*k-ka*D*w*w))
high_coefficient=S.expand(detgyro).coeff(w,4)
assert high_coefficient == -ka*g*g
checks['nonzero_gyro_second_pole']={'omega4_coefficient':str(high_coefficient),'passed':True}

# General single-mode-compatible gyro in coordinates (v,n1,n2).
C11,C12,C22,av,f1,f2,g1,g2=S.symbols('C11 C12 C22 av f1 f2 g1 g2',real=True)
C=S.Matrix([[C11,C12],[C12,C22]])
fv=S.Matrix([f1,f2]);gv=S.Matrix([g1,g2])
V=S.BlockMatrix([[S.Matrix([[av]]),fv.T],[fv,C]]).as_explicit()
Gdeg=S.Matrix([[0,g1,g2],[-g1,0,0],[-g2,0,0]])
detdeg=S.factor((k*k*V+ka*w*w*S.diag(1,0,0)+S.I*w*Gdeg).det())
gg=S.factor((gv.T*C.inv()*gv)[0])
stiff=S.factor(av-(fv.T*C.inv()*fv)[0])
preddeg=k**4*C.det()*((ka-gg/k**2)*w*w+k*k*stiff)
exact('single_mode_gyro_schur',detdeg-preddeg)
exact('single_mode_gyro_UV_kinetic',S.limit(ka-gg/k**2,k,S.oo)-ka)
negative_control=S.factor(alpha1.subs(E,1))
assert negative_control==-4
checks['large_preferred_frame_negative_control']={'E':1,'alpha1':str(negative_control),'passed':True}
result={
 'result':'The dynamic-lapse trace family changes alpha2 but not alpha1; a distinct local phi/U gyroscopic term adds a second scalar pole.',
 'checks':checks,
 'alpha1':str(alpha1),'alpha2':str(alpha2),
 'contact_free_identity':'alpha2=(E/2)(1/cs2-1)',
 'luminal_alpha2_zero':'delta=E/2 +/- sqrt(E(2-E)/(2*kappa))',
 'gyro_determinant':str(detgyro),
 'degenerate_gyro_kinetic':'kappa_eff(k)=kappa-g^T C^-1 g/k^2',
 'scope':'Frozen constant coefficients; conserved moving point-source boost through order v^2; unchanged Einstein vector sector and minimal matter metric. The source pipeline is checked against prior local L333 khronometric formula.',
 'non_claims':['No post-Newtonian nonlinear N-body calculation', 'No complete full-background constraint count', 'No universal exclusion of momentum-dependent higher-derivative architectures', 'No theorem that healthy waves imply causal response for arbitrary conserved sources']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
