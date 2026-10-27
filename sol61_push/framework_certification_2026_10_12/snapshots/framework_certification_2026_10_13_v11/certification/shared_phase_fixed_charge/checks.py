import sympy as s,json,sys
from pathlib import Path
r,R,a,m,f,X0,rho0,u,y,v=s.symbols('r R a m f X0 rho0 u y v',positive=True)
checks=[]
def eq(name,lhs,rhs=0):
 z=s.factor(lhs-rhs);assert z==0,(name,z);checks.append(name)
def positive(name,z):
 assert s.simplify(z).is_positive is True,(name,z);checks.append(name)
X=s.Symbol('X',real=True);P=-rho0+a*(X-X0)**2/2;PX=s.diff(P,X);U=m**2*(r-f)**2/2
energy=v**2/2+r**2*X+2*X*PX-P+U
pressure=v**2/2+r**2*X+P-U
Xq=X0-r**2/a
Veff=rho0+U-X0*r**2+r**4/(2*a)
eq('total_charge_zero',r**2+PX.subs(X,Xq))
eq('fixed_charge_energy',energy.subs(X,Xq),v**2/2+Veff)
eq('fixed_charge_pressure',pressure.subs(X,Xq),v**2/2-Veff)
eq('fixed_charge_enthalpy', (energy+pressure).subs(X,Xq),v**2)
eq('effective_radial_gradient',s.diff(Veff,r),m**2*(r-f)-2*r*Xq)
# Stationary relations are substitutes, not inferred unconstrained identities.
relations={f:R*(1-u**2/m**2),X0:u**2/2+R**2/a,r:R}
eq('stationary_effective_gradient',s.diff(Veff,r).subs(relations,simultaneous=True))
eq('stationary_energy_height',Veff.subs(relations,simultaneous=True),rho0-R**2*u**2*(1-u**2/m**2)/2-R**4/(2*a))
eq('stationary_curvature',s.diff(Veff,r,2).subs(relations,simultaneous=True),m**2-u**2+4*R**2/a)
eq('gap_curvature_match',m**2-u**2+(2*R*u)**2/(a*u**2),m**2-u**2+4*R**2/a)
g=y/2+f**2*m**4/(a*(m**2-y)**2)
eq('branch_equilibrium_equation',m**2*(f*m**2/(m**2-y)-f),f*m**2*y/(m**2-y))
eq('branch_initial_endpoint',g.subs(y,0),f**2/a)
t=s.Symbol('t',positive=True)
positive('branch_monotone_for_y_below_m2',s.diff(g,y).subs(y,m**2-t))
assert s.limit(g,y,m**2,dir='-')==s.oo;checks.append('branch_upper_endpoint_infinite')
EP=(2*X*PX-P).subs(X,Xq);Ec=(r**2*X+U).subs(X,Xq)
eq('component_energy_sum',EP+Ec,Veff)
eq('component_exchange_equal_opposite_at_stationary', (s.diff(EP,r)+s.diff(Ec,r)).subs(relations,simultaneous=True))
rdot,uddot,udd=s.symbols('rdot uddot udd',real=True)
# Total qdot=0 implies Xdot=-2r rdot/a; P-component power u pidot.
Pidot=s.diff((PX).subs(X,Xq)*s.sqrt(2*Xq),r)*rdot
Ppower=s.diff(EP,r)*rdot
eq('P_component_exchange_current',Ppower,s.sqrt(2*Xq)*Pidot)
eq('radial_energy_ODE_conservation',v*(-s.diff(Veff,r))+s.diff(Veff,r)*v)
# Exact stationary healthy leading-time-kinetic, gradient-degenerate witness.
w={m:s.Integer(2),f:s.Integer(1),u:s.Integer(1),a:s.Integer(4),R:s.Rational(4,3),X0:s.Rational(17,18),rho0:s.Integer(2)}
eq('witness_stationary', (m**2*(R-f)-R*u**2).subs(w))
positive('witness_radial_curvature', (m**2-u**2+4*R**2/a).subs(w))
positive('witness_positive_total_vacuum_energy', Veff.subs(r,R).subs(w))
positive('witness_positive_time_kinetic',(a*u**2).subs(w))
# Same dynamical branch at rho0=0 is mathematically possible but negative energy.
assert Veff.subs(r,R).subs({**w,rho0:s.Integer(0)})<0;checks.append('counter_witness_offset_not_selected')
assert s.diff(EP,r).subs(r,R).subs(w)!=0;checks.append('nonzero_component_exchange_derivative_witness')
result={'all_passed':True,'checks':checks,'count':len(checks),'scope':'Exact algebra of prospective shared-phase homogeneous zero-total-shift-charge branch; no irreversible cold settling or new-framework admission','witness_total_energy':str(Veff.subs(r,R).subs(w)),'witness_curvature':str((m**2-u**2+4*R**2/a).subs(w))}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
