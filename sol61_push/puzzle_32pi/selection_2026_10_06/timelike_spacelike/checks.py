#!/usr/bin/env python3
"""Normalized P(X) branches, actual clock principal part and lapse control."""
import argparse,json,platform
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--mutate-drop-PXX',action='store_true');args=ap.parse_args()
out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,ok,detail):
 checks.append(dict(name=name,passed=bool(ok),detail=str(detail)));print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail))
X=s.symbols('X',negative=True); C,alpha,G,gamma,rho,M,r,u,q,kappa,Xt=s.symbols('C alpha G gamma rho M r u q kappa Xt',positive=True)
P=-C*(-X)**s.Rational(3,2)
PX=s.diff(P,X);PXX=s.diff(P,X,2)
check('spacelike_cubic_source_coefficient',s.simplify(PX.subs(X,-u*u/2)-3*C*u/(2*s.sqrt(2)))==0,'gamma=3 C/(2 sqrt2)')
check('spacelike_longitudinal_speed_squared',s.simplify((PX+2*X*PXX)/PX)==2,'time coefficient PX>0; longitudinal scalar speed squared 2')
a0=alpha**3/(4*s.pi*gamma*G)
uMOND=s.sqrt(alpha*M/(4*s.pi*gamma))/r
check('Gauss_source_flux',s.simplify(r*r*gamma*uMOND*uMOND-alpha*M/(4*s.pi))==0,'source div(PX gradphi)=alpha rho_b, attractive force alpha u')
check('actual_galaxy_a0',s.simplify((alpha*uMOND)**2-G*M*a0/r**2)==0,'scalar-dominated deep law with tensor G, not unnormalized P coefficient')
ratio=8*s.pi*G*rho/a0**2
check('vacuum_ratio',s.simplify(ratio-128*s.pi**3*gamma**2*G**3*rho/alpha**6)==0,'Lambda=8piG rho, rho=-P(Xt)')
check('target_requires_independent_density',s.simplify(ratio.subs(rho,4*a0*a0/G)-32*s.pi)==0,'32pi iff rho=4 a0 squared/G, not stationarity')
ss=s.symbols('normalization',positive=True)
check('field_rescaling_invariance',s.simplify(a0.subs({alpha:alpha/ss,gamma:gamma/ss**3})-a0)==0,'alpha cubed/gamma is invariant under phi_new=s phi')
# Full two-coordinate principal tensor, including clock/spatial mixing.
f,ff=s.symbols('PX PXX',real=True)
K=s.Matrix([[-f-q*q*ff,q*u*ff],[q*u*ff,f-u*u*ff]])
check('principal_determinant_general',s.simplify(K.det()+f*(f+(q*q-u*u)*ff))==0,'det(K_tr)=-PX(PX+2X PXX), X=(q squared-u squared)/2')
clockPX=gamma*u;clockPXX=-gamma/u
actual=s.simplify(K.det().subs({f:clockPX,ff:0 if args.mutate_drop_PXX else clockPXX}))
check('clock_MOND_principal_type',s.simplify(actual+gamma**2*(2*u*u-q*q))==0,'hyperbolic only u>q/sqrt2; drop-PXX control must fail')
clockP=-gamma*(q*q-2*X)**s.Rational(3,2)/3
check('clock_shifted_branch',s.simplify(s.diff(clockP,X)-gamma*s.sqrt(q*q-2*X))==0,'same clock requires shifted cubic, not pure spacelike P')
# Smooth healthy condensate, X=Xt+deltaX, P=-rho+kappa deltaX squared/2.
dx=s.symbols('deltaX',real=True)
Pc=-rho+kappa*dx**2/2
check('condensate_kinetic_and_vacuum',s.diff(Pc,dx).subs(dx,0)==0 and s.diff(Pc,dx,2)==kappa,'kinetic coefficient 2 Xt kappa>0; k-squared gradient coefficient zero')
check('healthy_condensate_static_flux_sign',s.diff(Pc,dx).subs(dx,-u*u/2)==-kappa*u*u/2,'flat fixed clock: PX<0 for small attractive u, opposite positive baryon source')
# Weak-lapse rescue: deltaX=q squared GM/r-u squared/2.
v=s.symbols('v',positive=True)
flux=s.expand(r*r*kappa*(q*q*G*M/r-v*v/(2*r*r))*(v/r))
check('lapse_asymptotic_mass_cancellation',s.limit(flux,r,s.oo)==kappa*v*q*q*G*M and s.simplify(s.solve(s.Eq(s.limit(flux,r,s.oo),alpha*M/(4*s.pi)),v)[0]-alpha/(4*s.pi*kappa*q*q*G))==0,'u=v/r; coefficient v independent of M, not MOND sqrtM')
t=s.symbols('t');B=10*t**3-15*t**4+6*t**5
check('fixed_offset_shape_deformation_jets',B.subs(t,0)==0 and B.subs(t,1)==1 and all(s.diff(B,t,j).subs(t,z)==0 for j in (1,2) for z in (0,1)),'polynomial leaves origin and endpoint first/second jets; changes endpoint vacuum value')
# Conformal test coupling changes physical cosmological clock/metric.
H,at,tt=s.symbols('H alphaq time',positive=True)
A=s.exp(at*tt);HJ=(H+at)/A
check('conformal_clock_not_physical_deSitter',s.diff(HJ,tt)!=0,'A=e^(alpha q t), H_J=(H_E+alpha q)/A not constant if alpha q nonzero')
# Concrete principal signatures spanning the physical obstruction.
signatures=[]
for uv in (s.Rational(1,4),s.Rational(3,5),1,2):
 mat=K.subs({f:uv,ff:-1/uv,q:1,u:uv})
 signatures.append(dict(u=float(uv),det=float(mat.det()),eigenvalues=[float(z) for z in mat.eigenvals()]))
check('finite_signature_control',signatures[0]['det']>0 and all(z>0 for z in signatures[0]['eigenvalues']) and signatures[-1]['det']<0,'q=gamma=1: small-u block positive definite; large-u Lorentzian')
result=dict(checks=checks,signatures=signatures,mutation=args.mutate_drop_PXX,software=dict(python=platform.python_version(),sympy=s.__version__))
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
