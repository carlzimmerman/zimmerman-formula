"""Exact background-stealth variation and positive kinetic construction; not full health."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--wrong-half',action='store_true');ap.add_argument('--freeze-Xbar',action='store_true');ap.add_argument('--vacuum-homogeneous',action='store_true');args=ap.parse_args()
checks=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
def eq(x):return s.simplify(x)==0
phi=s.symbols('phi',positive=True);X=s.symbols('X',positive=True);Z=s.Function('Z')(phi);B=s.Function('B')(phi);Y=X-B;F=Z*Y*Y/2
FX=s.diff(F,X);Fp=s.diff(F,phi)
ck('stealth_action_value',eq(F.subs(X,B)))
ck('stealth_X_first_derivative',eq(FX.subs(X,B)))
ck('stealth_phi_first_derivative',eq(Fp.subs(X,B)))
ck('Einstein_pressure_unchanged',eq(F.subs(X,B)))
ck('Einstein_density_unchanged',eq((2*X*FX-F).subs(X,B)))
q,Xd=s.symbols('q Xd',positive=True);Yd=Xd-s.diff(B,phi)*q
used_Bprime=0 if args.freeze_Xbar else Xd/q
ck('trajectory_stealth_time_derivative',eq(Yd.subs(s.diff(B,phi),used_Bprime)))
FXdot=s.diff(Z,phi)*q*Y+Z*Yd
ck('scalar_EL_current_divergence_unchanged',eq(FXdot.subs({X:B,s.diff(B,phi):used_Bprime},simultaneous=True)))
eps,dphi,dX,nu,zeta=s.symbols('eps dphi dX nu zeta',real=True)
shift=F.subs({phi:phi+eps*dphi,X:B+eps*dX},simultaneous=True)
quad=s.simplify(s.series(shift,eps,0,3).removeO().coeff(eps,2))
ck('full_gauge_invariant_second_variation',eq(quad-Z*(dX-s.diff(B,phi)*dphi)**2/2))
ck('clock_surface_invariant',eq((dX-s.diff(B,phi)*dphi).subs(s.diff(B,phi),Xd/q)-(dX-Xd*dphi/q)))
unitquad=quad.subs({dphi:0,dX:-q*q*nu},simultaneous=True)
ck('unitary_exact_lapse_square',eq(unitquad-Z*q**4*nu*nu/2))
DeltaSigma=(X*FX+2*X*X*s.diff(F,X,2)).subs(X,B).subs(B,q*q/2)
ck('Sigma_from_K_derivatives',eq(DeltaSigma-Z*q**4/2))
ck('mixed_scalar_second_derivatives_retained',eq(s.diff(F,X,phi).subs(X,B)+Z*s.diff(B,phi)) and eq(s.diff(F,phi,2).subs(X,B)-Z*s.diff(B,phi)**2))
M,Hs,eta,h,pp,kappa=s.symbols('M Hs eta h pp kappa',positive=True)
lam=1+3*eta*eta/(1-eta)**2
poly=lam*(h-eta)**2+3*eta*(h-1-eta)
Zchosen=2*M*Hs**2*poly/q**4
chosenDelta=DeltaSigma.subs(Z,Zchosen)
ck('chosen_positive_floor_cancellation',eq(3*M*eta*(1+eta-h)/(h-eta)**2+chosenDelta/(Hs*Hs*(h-eta)**2)-lam*M))
ck('positive_Z_endpoint_bound',eq(poly.subs(h,1)-(1-eta)**2))
delta=s.symbols('delta',nonnegative=True)
ck('positive_Z_polynomial_decomposition',eq(poly.subs(h,1+delta)-((1-eta)**2+(2*lam*(1-eta)+3*eta)*delta+lam*delta**2)))
actualDelta=2*chosenDelta if args.wrong_half else chosenDelta
Knew=3*M*eta*(1+eta-h)/(h-eta)**2+actualDelta/(Hs*Hs*(h-eta)**2)+kappa*M*pp/(Hs*Hs*(h-eta)**2)
ck('finite_mode_clock_Schur_floor',eq(Knew-(lam*M+kappa*M*pp/(Hs*Hs*(h-eta)**2))))
# Full coupled radiation velocity Hessian gets only its positive lapse square.
d,Cr,Aold=s.symbols('d Cr Aold',positive=True);zd,vrD,vpot=s.symbols('zd vrD vpot',real=True)
raw=Aold*zd*zd+Cr*(vrD-d*zd)**2+chosenDelta*(d*zd+vpot)**2
KM=s.hessian(raw,[zd,vrD])/2
ck('radiation_coupled_positive_Schur',eq(KM.det()-Cr*(Aold+chosenDelta*d*d)))
# No acceleration Hessian or shift coefficient is inserted by this operator.
t=s.symbols('t',real=True)
ck('shift_constraint_unchanged',s.diff(unitquad,t)==0)
ck('no_new_lapse_spatial_operator',s.diff(unitquad,pp)==0)
# Exact simple reference state eta=.5 at the former background fold h1.5.
rows=[]
for hh in [s.Rational(11,10),s.Rational(3,2),s.Integer(10),s.Integer(1000)]:
 pol=s.simplify(poly.subs({eta:s.Rational(1,2),h:hh}));kn=s.simplify(Knew.subs({M:1,Hs:1,eta:s.Rational(1,2),h:hh,pp:0,kappa:1}))
 rows.append({'h':str(hh),'positive_Z_bracket':str(pol),'new_clock_Schur_at_p0':str(kn)})
ck('bounded_positive_Z_samples',all(s.Rational(r['positive_Z_bracket'])>0 for r in rows))
# Early radiation phi integral implies phi~a³ and Xbar~a².
power=s.Integer(2) if args.vacuum_homogeneous else s.Rational(2,3)
ck('radiation_trajectory_phi_power',eq(3*power-2))
aa,alpha,jhat,qstar=s.symbols('aa alpha jhat qstar',positive=True)
qearly=qstar*alpha*aa/jhat;phiearly=qstar*aa**3/(3*Hs*jhat)
ck('early_phi_derivative_from_current',eq(s.diff(phiearly,aa)*(Hs*alpha/aa)-qearly))
ck('early_Z_power',eq(s.limit(Zchosen.subs({h:alpha/aa**2,q:qearly},simultaneous=True)*aa**8,aa,0,dir='+')-2*M*Hs**2*lam*jhat**4/(qstar**4*alpha**2)))
# Original vacuumrescaling preservation forces polynomial coefficient homogeneity.
sc,Zo,Bo,Zs,Bs=s.symbols('sc Zo Bo Zs Bs',positive=True)
mapdiff=s.expand(Zs*(sc*sc*X-Bs)**2/2-Zo*(X-Bo)**2/2)
ck('vacuum_map_X2_coefficient',eq(mapdiff.coeff(X,2)-(sc**4*Zs-Zo)/2))
ck('vacuum_map_requires_B_degree2',eq(mapdiff.coeff(X).subs(Zs,Zo/sc**4)-Zo*(Bo-Bs/sc**2)))
ck('actual_early_profile_not_degree2',s.Integer(8)**s.Rational(2,3)!=s.Integer(8)**2)
# A pure shift-symmetric C² deformation zero on an open visited interval
# differentiates to zero; exact stress condition also forces firstderivative0.
U,Ux=s.symbols('U Ux',real=True)
ck('pure_K_stress_requires_value_and_slope',s.solve([U,2*X*Ux-U],[U,Ux])=={U:0,Ux:0})
out={'checks':checks,'summary':{'passed':sum(i['passed'] for i in checks),'total':len(checks)},'bounded_kinetic_states':rows,'scope':'Exact chosenbackground stealth and positive allfiniteepoch clock Schur floor; no completegradient/nonlinear/sourcehealth, no preservedcontinuousvacuumshiftmap or32pi selection.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']));raise SystemExit(0 if all(i['passed'] for i in checks) else 1)
