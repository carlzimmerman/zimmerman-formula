"""Actual normal-stress coefficients and exact arbitrary-spectrum time-power obstruction."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['coordinate_weight','expansion_is_density','dust_pressure']);args=ap.parse_args();rows=[]
def eq(name,e):rows.append({'name':name,'passed':s.simplify(e)==0})
def ck(name,e):rows.append({'name':name,'passed':bool(e)})
K,H,a,b,eta,P,k2=s.symbols('K H a b eta P k2',positive=True);D,C=s.symbols('D C',real=True)
d=D/a;u=C*k2/(b*H*H*a*a);z=C-d-u;nu=d+u
zd=H*d+2*H*u;A=-b
# Independent lapse reconstruction, with mode physical P=k²/a².
sol=(A*H*zd+k2/a**2*z)/(A*H*H-k2/a**2)
eq('actual_lapse_reconstructed',sol-nu)
eq('actual_relative_f',zd-H*nu-H*u)
e=2*(d+u)-3*C;eq('relative_volume_constraint',nu+3*z+e)
# Tensor-projector trace square, including each-metric half relative shear.
T=s.diag(s.Rational(2,3),-s.Rational(1,3),-s.Rational(1,3));eq('tracefree_projector_squared',s.trace(T*T)-s.Rational(2,3))
eq('each_metric_shear_square',s.trace(((-3*H*u/(2*eta))*T)**2)-3*H*H*u*u/(2*eta**2))
# Direct own-lapse and conformal-spatial variation of shear, at fixed shift/velocities.
N,Vsig,Qsig,phi=s.symbols('N Vsig Qsig phi',positive=True)
Lshear=-eta*K*N*Vsig*Qsig/N**2
rhoS=-s.diff(Lshear,N)/Vsig;eq('actual_shear_normal_energy',rhoS+eta*K*Qsig/N**2)
pS=s.diff(Lshear*s.exp(3*phi),phi).subs(phi,0)/(3*N*Vsig);eq('actual_shear_spatial_pressure',pS-rhoS)
# Own conformal variation: delta v/v=3phi/2; delta I=-phi I; M=-A0+I/2.
I,A0,a0,v,Vg=s.symbols('I A0 a0 v Vg',positive=True)
Lgrad=2*K*a0*a0*v*s.exp(3*phi/2)*(-A0+I*s.exp(-phi)/2)
pint=s.diff(Lgrad,phi).subs(phi,0)/(3*Vg)
eq('actual_interaction_pressure',pint-K*a0*a0*v/Vg*(-A0+I/6))
# Actual proper-volume IBP: -K/2 gradient direct plus +K gradient divergence.
Sq=s.symbols('S_gradient',nonnegative=True);rhoGrad=(-s.Rational(1,2)+1)*K*Sq/a**2
if args.control=='coordinate_weight':rhoGrad=-K*Sq/(2*a*a)
eq('proper_volume_divergence_weight',rhoGrad-K*Sq/(2*a*a))
# Parseval sums over ALL k; input symbols are convergent moments, not finite samples.
SD,SC4,SC6=s.symbols('S_D S_C4 S_C6',nonnegative=True);SX=s.symbols('S_cross',real=True)
grad=K/s.Integer(2)*(SD/a**4+2*SX/(b*H**2*a**5)+SC6/(b*b*H**4*a**6))
shear=-3*K*SC4/(2*eta*b*b*H*H*a**4)
rho=s.expand(grad+shear);press=s.expand(grad/3+shear)
R4=K*SD/2-3*K*SC4/(2*eta*b*b*H*H);R5=K*SX/(b*H*H);R6=K*SC6/(2*b*b*H**4)
eq('actual_density_three_powers',rho-(R4/a**4+R5/a**5+R6/a**6))
eq('actual_pressure_three_powers',press-((K*SD/6-3*K*SC4/(2*eta*b*b*H*H))/a**4+R5/(3*a**5)+R6/(3*a**6)))
# Independent polynomial coefficient extraction; an identity on an open a interval
# forces every coefficient to vanish, so the positive highest coefficient kills C.
x=s.symbols('inverse_a',positive=True);pol=s.Poly(press.subs(a,1/x),x)
eq('positive_pressure_six_coefficient',pol.coeff_monomial(x**6)-K*SC6/(6*b*b*H**4))
ck('highest_pressure_prefactor_strict_positive',K/(6*b*b*H**4)>0)
eq('pressure_after_momentum_zero',press.subs({SC4:0,SC6:0,SX:0})-K*SD/(6*a**4))
ck('remaining_pressure_prefactor_strict_positive',K/(6*a**4)>0)
eq('no_actual_density_dust_power',s.Poly(rho.subs(a,1/x),x).coeff_monomial(x**3))
if args.control=='dust_pressure':eq('false_nonzero_decay_pressureless',press.subs({SC4:0,SC6:0,SX:0,SD:1}))
# Same-shell geometric cross is real but cancels from averaged Hamiltonian density.
dd,uu,CC=s.symbols('d u C',real=True);deltaH=P*CC*dd/(24*H);Rcross=-P*CC*dd/2
candidate=6*H*deltaH+Rcross/2
if args.control=='expansion_is_density':candidate=6*H*deltaH
eq('actual_geometric_dust_cross_cancellation',candidate)
res={'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'conditional actualpropernormalstress toformalorder2 scalarvacuum spectra; all-spectrum theorem analytic positivity and summability, not finite simulation or matter-era no-go'}
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':res['passed'],'total':res['total'],'failed':[r['name'] for r in rows if not r['passed']]}));raise SystemExit(not all(r['passed'] for r in rows))
