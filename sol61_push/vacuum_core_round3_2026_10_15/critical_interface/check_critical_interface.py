#!/usr/bin/env python3
"""Exact reductions and assigned-scale certificates for the joined body."""
import json
import sys
from pathlib import Path
import sympy as s

checks=[]


def eq(name,expression):
    value=s.factor(s.cancel(expression))
    assert value==0,(name,value)
    checks.append(name)


def positive(name,expression):
    value=s.factor(expression)
    assert value>0,(name,value)
    checks.append(name)


r=s.symbols('r',positive=True)
G,c,zeta,D,Hpp=s.symbols('G c zeta D Hpp',positive=True)
rho_b=s.Function('rho_b')(r);rho_c=s.Function('rho_c')(r)
P_b=s.Function('P_b')(r);P_c=s.Function('P_c')(r)
xi_b=s.Function('xi_b')(r);xi_c=s.Function('xi_c')(r)
grav=s.Function('g')(r);electric=s.Function('E')(r)
div_b=s.diff(xi_b,r)+2*xi_b/r;div_c=s.diff(xi_c,r)+2*xi_c/r
dr_b=-rho_b*div_b-xi_b*s.diff(rho_b,r)
dr_c=-rho_c*div_c-xi_c*s.diff(rho_c,r)
dp_b=-2*P_b*div_b-xi_b*s.diff(P_b,r)
dp_c=-2*P_c*div_c-xi_c*s.diff(P_c,r)
dg=-4*s.pi*G*(rho_b*xi_b+rho_c*xi_c)
dD=-zeta*rho_c*xi_c
dE=Hpp*dD
force_b=-s.diff(dp_b,r)-grav*dr_b-rho_b*dg
force_c=-s.diff(dp_c,r)-(grav-zeta*electric)*dr_c-rho_c*dg+zeta*rho_c*dE


def background_reduce(expression):
    expression=expression.subs(s.diff(P_b,r,2),-s.diff(rho_b,r)*grav-rho_b*s.diff(grav,r))
    expression=expression.subs(s.diff(P_c,r,2),-s.diff(rho_c,r)*(grav-zeta*electric)-rho_c*(s.diff(grav,r)-zeta*s.diff(electric,r)))
    expression=expression.subs(s.diff(P_b,r),-rho_b*grav)
    expression=expression.subs(s.diff(P_c,r),-rho_c*(grav-zeta*electric))
    expression=expression.subs(s.diff(grav,r),4*s.pi*G*(rho_b+rho_c)-2*grav/r)
    expression=expression.subs(s.diff(electric,r),Hpp*(zeta*rho_c-2*D/r))
    return s.expand(expression).subs(zeta**2,4*s.pi*G)


target_b=s.diff(2*P_b*div_b,r)+4*rho_b*grav*xi_b/r-4*s.pi*G*rho_b*rho_c*(xi_b-xi_c)
target_c=(s.diff(2*P_c*div_c,r)+4*rho_c*grav*xi_c/r
          -4*s.pi*G*rho_b*rho_c*(xi_c-xi_b)-2*zeta*rho_c*(electric+Hpp*D)*xi_c/r)
eq('full baryon radial operator',background_reduce(force_b-target_b))
eq('full critical charged radial operator',background_reduce(force_c-target_c))
eq('symmetric positive gravity cross square',
   4*s.pi*G*rho_b*rho_c*((xi_b-xi_c)*xi_b+(xi_c-xi_b)*xi_c)
   -4*s.pi*G*rho_b*rho_c*(xi_b-xi_c)**2)

R,xi_R=s.symbols('R xi_R',positive=True)
eq('moving finite-density Gauss trace',-zeta*rho_c*xi_R+xi_R*(zeta*rho_c-2*D/R)+2*D*xi_R/R)
mass_c,mass_b,D0=s.symbols('mass_c mass_b D0',positive=True)
x=s.symbols('x',positive=True)
critical_force=(zeta*(zeta*mass_c/(4*s.pi*r**2))/(1-x)).subs(zeta**2,4*s.pi*G)
eq('actual critical Gauss force',critical_force-G*mass_c/(r**2*(1-x)))
a=s.symbols('a',positive=True)
eq('dark mass nonlinear Lipschitz derivative',s.diff(mass_c*(a*mass_c)/(1-a*mass_c),mass_c)-((1-a*mass_c)**-2-1))
gap=D0**2*(-x-s.log(1-x)-x**2/2)
gap_up=D0**2*x**3/(3*(1-x))
eq('electric load positive derivative',s.diff(gap,x)-D0**2*x**2/(1-x))
eq('electric load upper derivative',s.diff(gap_up-gap,x)-D0**2*x**3/(3*(1-x)**2))
eq('electric load zero origin',s.limit(gap,x,0))
eq('electric upper bound zero origin',s.limit(gap_up-gap,x,0))
eq('electric pressure D derivative',s.diff(gap.subs(x,D/D0),D)-(D/(1-D/D0)-D))
q=s.symbols('q',positive=True)
eq('fixed total charge phase derivative',s.diff(gap.subs(x,q/(D0*R**2)),R)+2*(q/R**2)*(q/R**2/(1-q/(D0*R**2))-q/R**2)/R)
sigma=s.symbols('sigma',positive=True)
mw=4*s.pi*sigma*R**2/c**2
Vw=4*s.pi*sigma*R**2-G*mw*(mass_b+mass_c)/R-G*mw**2/(2*R)
wall_load=2*sigma/R-G*sigma*(mass_b+mass_c)/(c**2*R**2)-6*s.pi*G*sigma**2/c**4
eq('complete wall energy derivative',s.diff(Vw,R)/(4*s.pi*R**2)-wall_load)
eq('wall load derivative',s.diff(wall_load,R)+2*sigma/R**2-2*G*sigma*(mass_b+mass_c)/(c**2*R**3))
z=s.symbols('z',positive=True)
eq('Hardy Tonelli kernel',s.integrate(r/3,(r,z,R))-(R**2-z**2)/6)
rho0=s.symbols('rho0',positive=True)
eq('finite ball mass kernel',s.integrate((4*s.pi*rho0*r**3/3)/r**2,(r,0,R))-2*s.pi*rho0*R**2/3)
P,rho=s.symbols('P rho',positive=True)
eq('Gamma2 exact effective inertia',(rho*c**2+2*P)*(1-2*P/(rho*c**2+2*P))-rho*c**2)

# Assigned scales and exact rational upper/lower bounds; only pi<4 is used.
fv=s.Rational(1341,250);Gv=s.Rational(1,10**8);cv=s.Integer(100)
Kcv=s.Rational(1,100);Kbv=Kcv*fv*(1+fv)
rhob0=s.Integer(1);rhoc0=fv;Rv=s.Integer(1);D0v=s.Integer(1)
wb0=2*Kbv;wc0=2*Kcv*fv;Pb0=Kbv;Pc0=Kcv*fv**2;P0=Pb0+Pc0
X=s.Rational(1,1000);eps=s.Rational(1,100)
positive('exact central pressure ordering',Pb0-Pc0)
eq('zeta rational upper square',s.Rational(1,2500)**2-16*Gv)
positive('uniform electric domain',X-fv/7500)
positive('charged inward force throughout box',(1-eps)*rhob0-rhoc0*X/(1-X))
Bb=s.Rational(8,3)*Gv*(1+fv);Bc=s.Rational(8,3)*Gv
positive('baryon map self margin',eps*wb0-Bb)
positive('charged map self margin',eps*wc0-Bc)
qb=s.Rational(8,3)*Gv*(1+fv)/wb0
qc=s.Rational(8,3)*Gv*(1+fv*((1-X)**-2-1))/wc0
positive('baryon contraction margin',s.Rational(1,10**6)-qb)
positive('charged contraction margin',s.Rational(1,10**6)-qc)
positive('pressure squared lower bound',(1-eps)**2-s.Rational(49,50))
Mupper=s.Rational(16,3)*(1+fv)
gapupper=X**3/(3*(1-X))
positive('total wall load positive',s.Rational(49,50)*P0-gapupper)
positive('electric load below nanounit',s.Rational(1,10**9)-gapupper)
sigma_test=s.Rational(51,100)*P0
Alower=2-Gv*Mupper/cv**2
Bupper=24*Gv/cv**4
positive('actual weak wall root exists',Alower*sigma_test-Bupper*sigma_test**2-P0)
positive('weak wall root on rising branch',Alower-2*Bupper*sigma_test)
omega_upper=s.Rational(16,3)*Gv*(1+fv)
boundary_electric=X**3/(1-X)
Cb=2*s.Rational(49,50)*Pb0-s.Rational(2,3)*rhob0*omega_upper-(boundary_electric+sigma_test)/3
Cc=2*s.Rational(49,50)*Pc0-s.Rational(2,3)*rhoc0*omega_upper-(boundary_electric+sigma_test)/3
positive('all radial baryon coercivity margin',Cb-s.Rational(14,25))
positive('all radial cold coercivity margin',Cc-s.Rational(9,20))
Hb_upper=rhob0+2*Pb0/cv**2;Hc_upper=rhoc0+2*Pc0/cv**2
positive('current inertia maximum is cold',Hc_upper-Hb_upper)
inertia_cap=(Hc_upper+sigma_test/cv**2)/6
positive('complete radial Rayleigh bound',s.Rational(9,20)/inertia_cap-s.Rational(1,2))
hc_upper=X**3/(1-X)**2
positive('principal critical inertia upper',s.Rational(2,10**9)-hc_upper)
positive('full interior cold principal gate',(1-eps)*fv*cv**2-hc_upper)
positive('baryon current sound below metric speed',cv**2-2*Kbv*rhob0)

result={
    'claim_id':'VC3-CRITICAL-INTERFACE-001','exact_checks':len(checks),'check_names':checks,
    'parameters':{'R':1,'D0':1,'rho_b0':1,'rho_c0':str(fv),'c':100,'G':str(Gv),'Kc':str(Kcv),'Kb':str(Kbv)},
    'critical_charge':'q_c/m_c=sqrt(4*pi*G); q_b=0',
    'relative_enthalpy_contraction_bounds':{'b':str(qb),'c':str(qc),'uniform_bound':'1/1000000'},
    'relative_first_iterate_error_upper':str(s.Rational(1,10**6)/(1-s.Rational(1,10**6))*max(Bb/wb0,Bc/wc0)),
    'central_pressures':{'b':str(Pb0),'c':str(Pc0),'total':str(P0)},
    'actual_wall_sigma_interval':['0',str(sigma_test)],
    'wall_rest_mass_upper':str(16*sigma_test/cv**2),
    'all_radial_Cb_lower':str(Cb),'all_radial_Cc_lower':str(Cc),
    'all_radial_Cb_decimal':str(s.N(Cb,30)),'all_radial_Cc_decimal':str(s.N(Cc,30)),
    'full_current_plus_wall_inertia_cap':str(inertia_cap),
    'Rayleigh_lower':str(s.Rational(9,20)/inertia_cap),
    'principal_hcrit_upper':str(hc_upper),
    'interpretation':'Actual no-held-source finite-ball critical charged/baryonic equilibrium with counted moving Maxwell wall and positive complete radial comparison energy in the defined hybrid.',
    'non_claims':['No EOS/phase/wall microphysics or production.','No nonspherical or magnetic-background stability.','No full Einstein or nonlinear free-boundary theorem.','No canonical pressureless galaxy law or empirical pass.']
}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ('claim_id','exact_checks','all_radial_Cb_decimal','all_radial_Cc_decimal')}))
