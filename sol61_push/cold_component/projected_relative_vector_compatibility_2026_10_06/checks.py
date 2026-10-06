import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','longitudinal_as_vector','erase_scalar_time','unweighted_only'],default='none');args=ap.parse_args();rows=[]
def eq(n,x):x=s.factor(s.simplify(x));rows.append(dict(name=n,passed=x==0,residual=str(x)))
def ck(n,x):rows.append(dict(name=n,passed=bool(x)))
K,a,H,k=s.symbols('K a H k',positive=True);Fd,V,dxW=s.symbols('Fd V dxW',real=True)
# Actual EH vector principal: tracefree symmetric offdiagonalextrinsic variation.
dK=s.Matrix([[0,dxW/2,0],[dxW/2,0,0],[0,0,0]])
eq('vector_extrinsic_trace_zero',s.trace(dK))
eq('single_EH_vector_square',s.trace(dK*dK)-s.trace(dK)**2-dxW**2/2)
Lrel=K*a**3*k*k*(Fd-V)**2/4
eq('relative_two_EH_normalization',Lrel-2*(K*a**3*k*k*(Fd-V)**2/8))
eq('actual_transverse_shift_constraint',s.diff(Lrel,V)-K*a**3*k*k*(V-Fd)/2)
eq('on_constraint_vector_action_zero',Lrel.subs(V,Fd))
# Purevector plane spatialpullback has unitJacobian andflatmetric; lapse1=>I0.
f=s.symbols('f',real=True);J=s.Matrix([[1,0,0],[f,1,0],[0,0,1]]);gam=J.T*J
eq('plane_vector_pullback_volume',gam.det()-1)
eq('pure_vector_geometric_mean_volume_difference',(s.sqrt(gam.det())-s.sqrt(gam.subs(f,-f).det()))**2)
# Eigenshell maxpoint formula: div((lapnu)V) = -k²(gradnu·V+nu divV).
nu,g1,g2,g3,V1,V2,V3,divV=s.symbols('nu g1 g2 g3 V1 V2 V3 divV',real=True)
vector_term=-k*k*(g1*V1+g2*V2+g3*V3+nu*divV)
eq('smooth_transverse_at_scalar_extremum',vector_term.subs({g1:0,g2:0,g3:0,divV:0}))
# scalarcurrent divergenceatmax = -3Hnu lapnu, E=2Ka timescurrent.
Emax=6*K*a*H*k*k*nu*nu
ck('clock_residual_nonzero_at_nonzero_extremum',Emax.subs(nu,1)>0)
# An inadmissiblelongitudinal shift can cancel, showing constraint matters.
x=s.symbols('x',real=True);amp=s.symbols('amp',positive=True);field=amp*s.cos(k*x);Vlong=-3*H*s.diff(field,x)/k**2
candidateshift=Vlong if args.control=='longitudinal_as_vector' else 0
eq('candidate_shift_is_transverse',s.diff(candidateshift,x))
current=-3*H*field*s.diff(field,x)+s.diff(field,x,2)*Vlong
eq('inadmissible_longitudinal_formally_cancels_clock',s.diff(current,x))
eq('longitudinal_divergence_not_free_vector',s.diff(Vlong,x)-3*H*field)
# Actualtimecomponent cannotbe erased.
scalarcurrent=s.diff(field,x,2)*(2*H*s.diff(field,x)/k**2)-H*field*s.diff(field,x)
if args.control=='erase_scalar_time':scalarcurrent=s.diff(field,x,2)*(2*H*s.diff(field,x)/k**2)
eq('actual_eigenshell_scalar_current',scalarcurrent+3*H*field*s.diff(field,x))
# Weighted necessarycondition for ANY weak divergencefreevector on torus.
# f=cosx+alpha cos2x, -u''=f, w=f''; required V·gradw=H R.
alpha=s.symbols('alpha',real=True);f2=s.cos(x)+alpha*s.cos(2*x);u=s.cos(x)+alpha*s.cos(2*x)/4;w=s.diff(f2,x,2);R=s.diff(f2*s.diff(f2,x)-2*w*s.diff(u,x),x)
eq('inverse_Laplacian_two_shells',s.diff(u,x,2)+f2)
weight=1 if args.control=='unweighted_only' else w*w
moment=s.integrate(s.expand_trig(weight*R),(x,0,2*s.pi))
expected=-3*s.pi*(64*alpha**4+40*alpha*alpha+1)/2
eq('two_shell_weighted_obstruction',moment-expected)
ck('weighted_obstruction_strict_every_real_alpha',s.Poly(64*alpha**4+40*alpha*alpha+1,alpha).all_coeffs()==[64,0,40,0,1])
eq('unweighted_compatibility_blind',s.integrate(R,(x,0,2*s.pi)))
# Testfunctions: G=w² and antiderivativew³/3 makevectorweightedmomentzero bydivV0.
wfun=s.Function('w')(x)
eq('weak_vector_weighted_chainrule',s.diff(wfun**3/3,x)-wfun*wfun*s.diff(wfun,x))
# Allowedfrozen/homflatterms have independent timepowers atfixednonzerofmax.
t,nu3,Z0lap,peak=s.symbols('t nu3 Z0lap peak',real=True);at=s.exp(H*t)
flat_piece=k*k*peak*Z0lap/(H*at**3)
hom_piece=3*H*k*k*nu3*peak/at**4
pure_piece=3*H*k*k*peak*peak/at**2
q=s.symbols('q',positive=True);poly=s.expand((pure_piece+flat_piece+hom_piece).subs(at,q)*q**4)
eq('independent_leading_timepower',s.Poly(poly,q).coeff_monomial(q*q)-3*H*k*k*peak*peak)
# Homogeneousactualr=nζ∞+2asinh(p/m0a³) hasconstant+decaya^-3 atlinearorder.
p,m0,zinf=s.symbols('p m0 zinf',real=True);eps=s.symbols('eps');rhom=3*eps*zinf+2*s.asinh(eps*p/(m0*at**3))
eq('allowed_homogeneous_lapse_time_dependence',s.diff(rhom,eps).subs(eps,0)-3*zinf-2*p/(m0*at**3))
out={'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'actualfirstorderEHtransversevectors, realcompacteigenshell extremumgate, explicit1+2cosmultishellweightedtest; noallmultishellclassification'}
p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[r for r in rows if not r['passed']]}));sys.exit(out['passed']!=out['total'])
