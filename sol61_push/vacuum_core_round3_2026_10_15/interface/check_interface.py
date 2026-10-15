#!/usr/bin/env python3
"""Exact constants/identities for the global fixed-core interface control."""
import json
import sys
from pathlib import Path
import sympy as s

checks=[]


def eq(name, expression):
    value=s.factor(s.cancel(expression))
    assert value==0,(name,value)
    checks.append(name)


def positive(name, expression):
    value=s.factor(expression)
    assert value>0,(name,value)
    checks.append(name)


r,R,Rc,Mc,Ms,G,c,sigma,rho0,w0,D0,D=s.symbols(
    'r R Rc Mc Ms G c sigma rho0 w0 D0 D',positive=True)
x=s.symbols('x',positive=True)
mwall=4*s.pi*sigma*R**2/c**2
Vwall=4*s.pi*sigma*R**2-G*mwall*(Mc+Ms)/R-G*mwall**2/(2*R)
wall_load=2*sigma/R-G*sigma*(Mc+Ms)/(c**2*R**2)-6*s.pi*G*sigma**2/c**4
eq('all wall gravitational work',s.diff(Vwall,R)/(4*s.pi*R**2)-wall_load)
eq('wall pressure derivative',s.diff(wall_load,R)+2*sigma/R**2-2*G*sigma*(Mc+Ms)/(c**2*R**3))
gap=D0**2*(-x-s.log(1-x)-x**2/2)
eq('positive electric jump derivative',s.diff(gap,x)-D0**2*x**2/(1-x))
upper=D0**2*x**3/(3*(1-x))
eq('electric jump upper derivative',(s.diff(upper-gap,x)-D0**2*x**3/(3*(1-x)**2)))
eq('electric jump zero limit',s.limit(gap,x,0))
eq('electric jump bound zero limit',s.limit(upper-gap,x,0))
eq('electric pressure D derivative',s.diff(gap.subs(x,D/D0),D)-(D/(1-D/D0)-D))
qcharge=s.symbols('qcharge',positive=True)
eq('fixed charge boundary derivative',s.diff(gap.subs(x,qcharge/(D0*R**2)),R)
   +2*(qcharge/R**2)*(qcharge/R**2/(1-qcharge/(D0*R**2))-qcharge/R**2)/R)
core_integral=s.integrate(Mc*r/Rc**3,(r,0,Rc))+s.integrate(Mc/r**2,(r,Rc,R))
eq('compact source enthalpy integral',core_integral-Mc/Rc*(s.Rational(3,2)-Rc/R))
eq('uniform density Volterra kernel',s.integrate((4*s.pi*rho0*r**3/3)/r**2,(r,0,R))-2*s.pi*rho0*R**2/3)
w=s.symbols('w',positive=True)
eq('neutral EOS derivative',s.diff(rho0*(w/w0)**5,w)-5*rho0*w**4/w0**5)

# Euler/Poisson identity with the fixed central density retained.
rh=s.Function('rho')(r);P=s.Function('P')(r);xi=s.Function('xi')(r);g=s.Function('g')(r)
rhoc=s.Function('rhoc')(r);Gamma=s.symbols('Gamma',positive=True)
divxi=s.diff(xi,r)+2*xi/r
dp=-Gamma*P*divxi-xi*s.diff(P,r)
drho=-rh*divxi-xi*s.diff(rh,r)
dg=-4*s.pi*G*rh*xi
force=-s.diff(dp,r)-g*drho-rh*dg
force=force.subs(s.diff(P,r,2),-s.diff(rh,r)*g-rh*s.diff(g,r))
force=force.subs(s.diff(P,r),-rh*g)
force=force.subs(s.diff(g,r),4*s.pi*G*(rh+rhoc)-2*g/r)
target=s.diff(Gamma*P*divxi,r)+rh*(4*g/r-4*s.pi*G*rhoc)*xi
target=target.subs(s.diff(P,r),-rh*g)
eq('full radial Euler Poisson operator',force-target)
z=s.symbols('z',positive=True)
eq('Hardy Tonelli kernel',s.integrate(r/3,(r,z,R))-(R**2-z**2)/6)

# Exact assigned scales. Pi<4 is used only as a rigorous upper bound.
Rval=cval=rhoval=D0val=s.Integer(1)
Gval=s.Rational(1,10**6);Mcval=s.Rational(1,1000);Rcval=s.Rational(1,2)
Kval=s.Rational(1,100);Gammaval=s.Rational(6,5);Dbval=s.Rational(1,1000)
w0val=6*Kval;P0=Kval;epsilon=s.Rational(1,100)
B0upper=Gval*(Mcval/Rcval*(s.Rational(3,2)-Rcval/Rval)+8*rhoval*Rval**2/3)
qupper=40*Gval*rhoval*Rval**2/(3*w0val)
eq('contraction upper constant',qupper-s.Rational(1,4500))
positive('self map strict margin',epsilon*w0val-B0upper)
positive('contraction strict margin',1-qupper)
rho_lower=(1-epsilon)**5
P_lower=P0*(1-epsilon)**6
positive('effective inertia lower bound',rho_lower-s.Rational(19,20))
positive('pressure lower bound',P_lower-s.Rational(47,5000))
Mtotupper=Mcval+s.Rational(16,3)*rhoval*Rval**3
eq('counted interior mass upper',Mtotupper-s.Rational(16003,3000))
gapupper=Dbval**3/(3*(1-Dbval))
positive('positive wall load',P_lower-gapupper)
positive('electric load bound',s.Rational(1,10**9)-gapupper)
sigma_test=s.Rational(51,10000)
Alower=2-Gval*Mtotupper;Bupper=24*Gval
positive('wall equation crosses load',Alower*sigma_test-Bupper*sigma_test**2-P0)
positive('wall weak branch derivative',Alower-2*Bupper*sigma_test)
eq('wall inertia finite mass bound',s.Rational(816,10000)-16*sigma_test)
omega_upper=Gval*(Mcval/Rcval**3+s.Rational(16,3))
electric_derivative=2*Dbval*(Dbval/(1-Dbval)-Dbval)
eq('electric boundary derivative value',electric_derivative-s.Rational(2,999*10**6))
gravity_loss=s.Rational(2,3)*omega_upper
eq('gravity form bound value',gravity_loss-s.Rational(4006,1125*10**6))
C_lower=Gammaval*s.Rational(47,5000)-gravity_loss-(electric_derivative+2*sigma_test)/3
positive('full radial energy strict margin',C_lower-s.Rational(39,5000))
J_to_inertia=s.Rational(1,6)+sigma_test/3
positive('positive radial Rayleigh lower bound',s.Rational(39,5000)/J_to_inertia-s.Rational(46,1000))
xmax=Dbval/Rcval**2
eq('occupied maximum D',xmax-s.Rational(1,250))
hcmax=xmax**3/(1-xmax)**2
eq('occupied maximum critical inertia',hcmax-1/(s.Integer(250)*249**2))
positive('uniform occupied gate',rho_lower-hcmax)
Pvar=s.symbols('Pvar',positive=True)
eq('full polytropic effective inertia',(rho0+6*Pvar)*(1-Gammaval*Pvar/(rho0+6*Pvar))-(rho0+s.Rational(24,5)*Pvar))

result={
    'claim_id':'VC3-INTERFACE-001','exact_checks':len(checks),'check_names':checks,
    'assigned_parameters':{'c':1,'R':1,'rho0':1,'D0':1,'G':'1/1000000','Gamma':'6/5','K':'1/100','Mc':'1/1000','Rc':'1/2','Db':'1/1000'},
    'contraction_upper':str(qupper),'enthalpy_drop_upper':str(B0upper),
    'first_iterate_error_upper':str(qupper*B0upper/(1-qupper)),
    'actual_wall_sigma_interval':['0',str(sigma_test)],
    'actual_wall_mass_upper':str(16*sigma_test),
    'full_radial_C_lower':str(C_lower),'full_radial_C_lower_decimal':str(s.N(C_lower,25)),
    'radial_Rayleigh_lower':str(s.Rational(39,5000)/J_to_inertia),
    'occupied_hcrit_upper':str(hcmax),
    'interpretation':'Constructive existence plus positive all-radial fluid/wall energy in the specified fixed-core Newtonian rest-mass-gravity model; not full theory closure.',
    'non_claims':['No dynamical charged-core equilibrium or stability.','No nonspherical interface or magnetic-background stability.','No wall microphysics, production, empirical pass or full Einstein junction.','No numerical ODE profile is used as proof.']
}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ('claim_id','exact_checks','contraction_upper','full_radial_C_lower_decimal')}))
