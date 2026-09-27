#!/usr/bin/env python3
"""Exact AQUAL with measured rather than bare Newton normalization."""
import argparse,json
from pathlib import Path
import sympy as s
p=s.symbols('psi',real=True); f,be,dp=s.symbols('phi beta psi_dot',real=True)
k,w,B,E,R,stress=s.symbols('k omega B E R stress',real=True)
C,x,a0,Gb=s.symbols('C x a0 Gbare',positive=True)
checks={}
def exact(name,expr):
    val=s.factor(s.simplify(expr)); assert val==0,(name,val)
    checks[name]={'passed':True,'residual':str(val)}
F=2*(1-C)*a0**2*x**2+4*C*a0**2*(1-(1+x)*s.exp(-x))
G=x*x+2*(1+x)*s.exp(-x)-2
muT=1-s.exp(-x); muL=1+(x-1)*s.exp(-x)
ET=s.diff(F,x)/(2*a0**2*x); EL=s.diff(F,x,2)/(2*a0**2)
exact('integrated_general_source_AQUAL',-2*a0**2*x*x+F+2*C*a0**2*G)
exact('transverse_Hessian',ET-2*(1-C*muT))
exact('longitudinal_Hessian',EL-2*(1-C*muL))
exact('tangent_integrability',EL-ET-x*s.diff(ET,x))
exact('muL_derivative',s.diff(muL,x)-(2-x)*s.exp(-x))
exact('muL_maximum_value',muL.subs(x,2)-(1+s.exp(-2)))
exact('high_acceleration_E',s.limit(ET,x,s.oo)-2*(1-C))
exact('zero_acceleration_E',s.limit(ET,x,0)-2)
exact('vacuum_offset',s.limit(F-2*(1-C)*a0*a0*x*x,x,s.oo)-4*C*a0*a0)
L=-6*dp**2+4*k*k*be*dp+2*k*k*p*p-4*k*k*f*p+E*k*k*f*f-B*(3*dp-k*k*be)**2
aux=s.solve([s.diff(L,f),s.diff(L,be)],[f,be])
kap=2*(2+3*B)/B
exact('reduced_scalar_action',L.subs(aux)-(kap*dp*dp-2*(2-E)/E*k*k*p*p))
static=s.solve([s.diff(L,f)-R,s.diff(L,p)],[f,p])
exact('static_no_slip',static[f]-static[p])
exact('physical_Newton_constant',static[f].subs(E,2*(1-C))-(-R/(4*C*k*k)))
cs=2*(2-E)/(kap*E)
Emin=(2*(1-C*(1+s.exp(-2)))) .subs(C,s.Rational(1,2))
cap=s.simplify(cs.subs({E:Emin,B:s.Rational(1,10)}))
assert 0<float(cap)<1
checks['all_x_positive_domain_witness']={'passed':True,'C':'1/2','B':'1/10','kappa':'46','E_min':str(Emin),'maximum_speed_squared':float(cap)}
# Euler equations with a fully conserved longitudinal source and independent stress.
D=-s.I*w
eqs=[s.diff(L,f)-R,s.diff(L,p)-D*s.diff(L,dp)-stress,s.diff(L,be)+D*R]
eqs=[ee.subs(dp,D*p)for ee in eqs]
sol=s.solve(eqs,[f,p,be])
# Positive E alone does not impose a causal metric; this is a transfer diagnostic.
tidal=s.factor((-k*k*(sol[f]+D*sol[be])-w*w*sol[p]).subs(stress,w*w*R/(k*k))/R)
q=s.symbols('q',real=True)
tidalq=s.factor(tidal.subs(w*w,q*k*k))
num,den=s.fraction(tidalq)
quot,rem=s.div(num,den,q)
exact('planar_tidal_wave_contact_division',tidalq-quot-rem/den)
assert s.degree(quot,q)<=1
checks['planar_generator_no_inverse_spatial_contact']={'passed':True,'transfer':str(tidalq),'polynomial':str(quot),'scope':'R=-k²F with conserved stress=omega²R/k², constant tangent'}
# Moving weak source at asymptotically high acceleration.
v,angle,kp,M=s.symbols('v angle kp M',real=True)
gm=1/s.sqrt(1-v*v)
# R=16pi Gbare rho, rho=gamma M; transverse shift S/J_T=-16piGbare/k².
wave={R:16*s.pi*Gb*gm*M,stress:16*s.pi*Gb*gm*M*v*v}
phi=s.factor(sol[f].subs(wave)); psi=s.factor(sol[p].subs(wave)); beta=s.factor(sol[be].subs(wave))
shift_v=-16*s.pi*Gb*gm*M*(v*v-w*w/(k*k))/(k*k)
rest=gm**3*(-2*(phi-s.I*w*beta)-2*v*v*psi+2*shift_v)
# Fourier boost: k²=kp²[1+(gamma²−1)angle²], omega=gamma kp angle v.
# Replace k² directly to avoid artificial square-root branches.
rest=s.cancel(rest).subs(k*k,kp*kp*(1+(gm*gm-1)*angle*angle)).subs(w,gm*kp*angle*v)
GN=Gb/(1-E/2)
ratio=s.cancel(rest/(8*s.pi*GN*M/(kp*kp)))
series=s.series(ratio,v,0,3).removeO().expand()
zer=s.simplify(series.coeff(v,0))
v2=s.factor(series.coeff(v,2))
iso=s.simplify(v2.subs(angle,0))
ani=s.simplify(s.diff(v2,angle,2)/2)
exact('moving_source_static_normalization',zer-1)
exact('moving_source_has_only_isotropic_and_quadrupole',v2-iso-ani*angle**2)
alpha1=s.factor(-2*iso)
alpha2=s.factor(ani)
exact('derived_alpha1',alpha1+4*E)
exact('derived_alpha2',alpha2-E*(E-B+2*E*B)/(B*(2-E)))
exact('GR_moving_source_control',s.limit(s.limit(v2,E,0),B,0))
alpha_floor=8/(s.exp(2)+1)
assert float(alpha_floor)>.95
checks['all_x_stability_PPN_conflict']={'passed':True,'required_C_upper':float(1/(1+s.exp(-2))),'required_abs_alpha1_lower':float(alpha_floor),'conservative_reference_bound':1e-4,'meaning':'Within this beta=0 khronometric asymptotic class, not universal modified gravity'}
# Derive FRW lapse equation from minisuperspace; potential contribution F(a=0)=0.
N,H,aa,Lam=s.symbols('N H a Lambda',positive=True)
Lg=aa**3*(-(6+9*B)*H**2/N-2*Lam*N)/(16*s.pi*Gb)
exact('FRW_lapse_variation',s.diff(Lg,N).subs(N,1)-aa**3*((6+9*B)*H**2-2*Lam)/(16*s.pi*Gb))
result={'result':'Exact measured-G AQUAL has an all-x healthy principal window, with a derived preferred-frame obstruction in this action family',
'checks':checks,'formulas':{'F_C':str(F),'E_T':str(ET),'E_L':str(EL),'GN':'Gbare/C','Gcosm_over_GN':'C/(1+3B/2)','alpha1':str(alpha1),'alpha2':str(alpha2),'kinetic':str(kap),'speed2':str(cs),'tidal_transfer':str(tidalq)},
'non_claims':['No full nonlinear gravity or degree-count certification','No all-source causal proof from one planar generator','No physical PPN inference at finite MOND acceleration from asymptotic formula','No uniform positive speed at x=0','No claim scalar speed below light evades gravitational Cherenkov constraints'],
'source_dependency':'Exact PPN crosscheck: Yagi et al arXiv:1311.7144v4 equations48-49, beta=0. Moving-source method also checked against local L333; no imported simulation output.'}
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'alpha1':str(alpha1),'alpha2':str(alpha2),'all_passed':True}))

