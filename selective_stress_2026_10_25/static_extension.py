"""Exact reciprocal-kinetic Schur complement, plus pinned prior static data."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output)
h,A=s.symbols('h A',positive=True);g=s.symbols('g',real=True)
H=s.Matrix([[h+g*g/A,-g/A],[-g/A,1/A]])
schur=s.simplify(H[0,0]-H[0,1]**2/H[1,1]);det=s.factor(H.det());assert schur==h and det==h/A
u,p=s.symbols('u p',real=True);assert s.expand((s.Matrix([u,p]).T*H*s.Matrix([u,p]))[0]-(h*u*u+(p-g*u)**2/A))==0
old=json.loads(Path('physical_completion_2026_10_25/run_two_field_audit/results.json').read_text())['audit'];r=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text())
out={'exact_identity':{'kinetic_extended_Hessian':str(H),'static_Schur_complement':str(schur),'determinant':str(det),'quadratic_form':'h u²+(p-g u)²/A'},'structural_claim':'For any positive static constrained Hessian H0 and positive scalar inertia A, the enlarged quadratic energy is delta_u^T H0 delta_u+(delta_Pi-G delta_u)^T A^-1(delta_Pi-G delta_u), plus nonnegative scalar-gradient/matter-kinetic terms. Relaxing the shifted momenta gives exactly H0. Passive outgoing damping cannot increase this energy.','inherited_radial_benchmark':{'radius_kpc':r['scaled_boundary_kpc'],'law_error_bound_percent':r['scaled_law_error_bound_percent'],'minimum_active_static_H':old['minimum_active_H'],'relaxed_boundary_stiffness_Eunit_per_kpc2':old['relaxed_boundary_stiffness_Eunit_per_kpc2'],'source':'PC-16 active radial discretization, not a new equilibrium solve'},'non_claims':['No formation or basin-of-attraction proof','No nonradial or continuum stability result','Static law-error and multi-mass failures are inherited unchanged','An outgoing field carries the shift charge; fixing it locally would be another constraint']}
dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['inherited_radial_benchmark'],indent=2),flush=True)
