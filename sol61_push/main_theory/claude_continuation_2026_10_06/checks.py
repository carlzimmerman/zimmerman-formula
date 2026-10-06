#!/usr/bin/env python3
"""Exact restricted curvature-mass cold-bridge discrimination; own action, not Claude execution."""
import argparse,json,sys,math
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['omit_metric_variation','call_stiff_dust']);args=ap.parse_args()
rows=[]
def ck(n,v,detail=''):
 rows.append(dict(name=n,pass_=bool(v),detail=str(detail)))
def zero(e):return s.simplify(s.expand(e))==0
t,xi,A=s.symbols('t xi A',positive=True);u=s.symbols('u',real=True)
f=A/t;H=s.Rational(2,3)/t;R=6*(s.diff(H,t)+2*H**2)
omega2=4*xi/3-s.Rational(1,4)
kin=A*(s.Rational(1,4)+omega2)/t**3
fac=0 if args.mutation=='omit_metric_variation' else 2
rho=kin+fac*xi*(3*H**2*f+3*H*s.diff(f,t))
p=kin+fac*xi*(-(2*s.diff(H,t)+3*H**2)*f-s.diff(f,t,2)-2*H*s.diff(f,t))
ck('EdS_R_from_metric',zero(R-4/(3*t**2)))
pol=u*(u-1)+2*u+4*xi/3
ck('scalar_Euler_power_polynomial',zero(pol-(u**2+u+4*xi/3)))
ck('oscillatory_pair_root',zero(pol.subs(u,-s.Rational(1,2)+s.I*s.sqrt(omega2))))
ck('full_EdS_density_zero',zero(rho),rho)
ck('full_EdS_pressure_zero',zero(p),p)
ck('EdS_full_stress_conservation',zero(s.diff(rho,t)+3*H*(rho+p)))
# A real mode: vary before treating the curvature term as a mass.
xi_s=-s.Rational(3,4)*u*(u+1)
rhoc=s.factor((s.Rational(1,2)*u**2+xi*(s.Rational(4,3)+4*u)).subs(xi,xi_s))
pc=s.factor((s.Rational(1,2)*u**2+xi*(-2*u*(2*u-1)-s.Rational(8,3)*u)).subs(xi,xi_s))
ck('real_mode_density_coefficient',zero(rhoc+s.Rational(1,2)*u*(3*u+2)*(2*u+1)),rhoc)
ck('real_mode_equation_of_state',zero(pc+u*rhoc))
ck('real_mode_conservation_exact',zero((2*u-2)*rhoc+2*(rhoc+pc)))
ck('real_dust_exponent_implies_zero_mass_and_stress',zero(rhoc.subs(u,0)) and zero(xi_s.subs(u,0)))
# Radiation decaying mode, R=0, same massless field equation irrespective of xi.
Hr=1/(2*t);Rr=6*(s.diff(Hr,t)+2*Hr**2);kr=A/(4*t**3)
rhor=s.simplify(kr+fac*xi*(3*Hr**2*f+3*Hr*s.diff(f,t)))
pr=s.simplify(kr+fac*xi*(-(2*s.diff(Hr,t)+3*Hr**2)*f-s.diff(f,t,2)-2*Hr*s.diff(f,t)))
ck('radiation_curvature_mass_zero',zero(Rr))
ck('radiation_decaying_scalar_Euler',zero(s.diff(t**(-s.Rational(1,2)),t,2)+3*Hr*s.diff(t**(-s.Rational(1,2)),t)))
ck('radiation_full_density_coefficient',zero(rhor-(s.Rational(1,4)-3*xi/2)*A/t**3))
ck('radiation_decaying_w_is_stiff',zero(pr-rhor) if args.mutation!='call_stiff_dust' else zero(pr))
ck('radiation_full_conservation',zero(s.diff(rhor,t)+3*Hr*(rhor+pr)))
# Nonoscillating radiation constant branch is gravity renormalization, radiation-like.
f0=A;k0=0
r0=2*xi*3*Hr**2*f0;p0=2*xi*(-(2*s.diff(Hr,t)+3*Hr**2)*f0)
ck('constant_radiation_mode_w_one_third',zero(p0-r0/3))
ck('constant_radiation_mode_as_Planck_shift',zero(r0-2*xi*f0*3*Hr**2))
# General power-law FRW complex circular oscillatory pair requires Re(s)=(1-3p)/2.
v=s.symbols('v',positive=True);l=(1-3*v)/2;Rcoef=6*v*(2*v-1)
om2=xi*Rcoef-l**2
kincoef=l**2+om2
rhogen=s.factor(kincoef+2*xi*(3*v**2+6*v*l))
ck('general_powerlaw_circular_density_zero',zero(rhogen))
pcgen=s.factor(kincoef+2*xi*((2*v-3*v**2)-2*l*(2*l-1)-4*v*l))
ck('general_powerlaw_circular_pressure_zero',zero(pcgen))
C0,C1=s.symbols('C0 C1',real=True)
ch=C0+C1/s.sqrt(t);ff=ch**2;kk=s.diff(ch,t)**2
rr=kk+2*xi*(3*Hr**2*ff+3*Hr*s.diff(ff,t))
pp=kk+2*xi*(-(2*s.diff(Hr,t)+3*Hr**2)*ff-s.diff(ff,t,2)-2*Hr*s.diff(ff,t))
ck('general_radiation_no_cross_density',zero(rr-(3*xi*C0**2/(2*t**2)+(s.Rational(1,4)-3*xi/2)*C1**2/t**3)))
ck('general_radiation_pressure_components',zero(pp-(xi*C0**2/(2*t**2)+(s.Rational(1,4)-3*xi/2)*C1**2/t**3)))
# Independent numerical magnitude only: not applying constant-m transfer function.
hbar_eVs=6.582119569e-16;Hvac=1.8e-18;mneed=2.29e-20
xi_need=(mneed/(math.sqrt(12)*hbar_eVs*Hvac))**2
ck('declared_dS_mass_link_requires_large_dimensionless_xi',xi_need>1e24,xi_need)
Hd=s.symbols('Hd',positive=True);fd=A*s.exp(-3*Hd*t);kd=12*xi*Hd**2*fd
rd=kd+2*xi*(3*Hd**2*fd+3*Hd*s.diff(fd,t))
pd=kd+2*xi*(-3*Hd**2*fd-s.diff(fd,t,2)-2*Hd*s.diff(fd,t))
ck('deSitter_circular_density_zero',zero(rd))
ck('deSitter_circular_pressure_zero',zero(pd))
ck('EdS_U1_number_charge_nonzero_constant',zero(s.diff(t**2*f/t,t)))
# Bare massive positive control has adiabatic conserved dust in external FRW, unlike varied R coupling.
m,n=s.symbols('m n',positive=True);rhob=m*n;pb=0
ck('constant_mass_number_current_dust_control',zero(-3*H*rhob+3*H*(rhob+pb)))
out={'scope':'exact own-action FRW identities; no full stability or source existence','mutation':args.mutation,'checks':rows,'summary':{'passed':sum(r['pass_'] for r in rows),'total':len(rows)},'xi_dS_control':xi_need,'software':{'sympy':s.__version__}}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));sys.exit(0 if all(r['pass_'] for r in rows) else 1)
