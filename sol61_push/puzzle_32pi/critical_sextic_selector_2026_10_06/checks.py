import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','critical_selects_mass','stable_positive_cubic','BMB_equals_UV'],default='none');a=ap.parse_args();checks=[]
def ck(n,b,e=''):checks.append(dict(name=n,passed=bool(b),detail=str(e)))
def eq(n,e):e=s.simplify(e);ck(n,e==0,e)
N,eta,g6,m,hbar=s.symbols('N eta g6 m hbar',positive=True);pi=s.pi
eta_norm=g6*120/N**2;bar=g6/(16*pi*pi)
eq('canonical_sextic_coefficient',eta_norm/s.factorial(6)-g6/(6*N**2))
eq('eta_bar_normalization',eta_norm*N**2/(16*pi*pi*120)-bar)
beta=(24*bar**2-2*pi*pi*bar**3)/N
eq('BMB_beta_not_UV_zero',beta.subs(g6,16*pi*pi)-(24-2*pi*pi)/N)
eq('UV_beta_zero',beta.subs(g6,192))
ck('distinct_critical_points',192>16*pi*pi)
# Independent subtracted tadpole, radial momentum p=m u; elementary convergent integral.
u=s.symbols('u',positive=True);rho=-hbar*m/(2*pi*pi)*s.integrate(1/(1+u*u),(u,0,s.oo))
eq('subtracted_tadpole',rho+hbar*m/(4*pi))
eq('LO_gap_coefficient',g6*rho**2-m*m*(g6*hbar*hbar/(16*pi*pi)))
crit=16*pi*pi/hbar**2;gap=m*m-g6*rho*rho
eq('critical_gap_all_masses',gap.subs(g6,crit))
# hbar=1: composite auxiliary potential U=g6rho³/6-m²rho/2+1/2Trln.
rho1=rho.subs(hbar,1);logterm=-m**3/(12*pi)
energy=N*(g6*rho1**3/6-m*m*rho1/2+logterm)
eq('LO_composite_energy',energy-N*m**3/(24*pi)*(1-bar))
eq('LO_flat_energy',energy.subs(g6,16*pi*pi))
eq('LO_flat_mass_curvature',s.diff(energy,m,2).subs(g6,16*pi*pi))
C=s.symbols('C');eq('additive_offset_does_not_gap',s.diff(energy+C,m)-s.diff(energy,m))
eq('offset_at_critical_remains_free',(energy+C).subs(g6,16*pi*pi)-C)
D=s.symbols('D');dim=D-6*(D-2)/2
eq('sextic_dimension',dim-(6-2*D));eq('marginal_only_D3',dim.subs(D,3));eq('D4_dimension_minus2',dim.subs(D,4)+2)
psi,g,h,z,k=s.symbols('psi g h z k',positive=True);q=s.symbols('q',nonnegative=True)
E=k*(g*psi**6/6-h*z*psi**2/2);ps=(h*z/g)**s.Rational(1,4);emin=s.simplify(E.subs(psi,ps));curv=s.diff(E,psi,2).subs(psi,ps)
eq('classical_stationary',s.diff(E,psi).subs(psi,ps));eq('classical_min_energy',emin+k*h**s.Rational(3,2)*z**s.Rational(3,2)/(3*s.sqrt(g)))
eq('classical_source_gap',curv-4*k*h*z)
ck('classical_stable_minimum',curv.is_positive)
eq('classical_vacuum_gap_zero',s.diff(E,psi,2).subs({psi:0,z:0}))
ck('stable_eliminated_cubic_negative',emin.is_negative)
ck('source_normalization_still_free',s.diff(emin,h).is_negative)
eq('reverse_energy_is_positive_cubic',(-E).subs(psi,ps)+emin)
ck('reverse_stationary_point_not_minimum',(-curv).is_negative)
# Explicit Legendre conjugate changes the controlled variable; not same energy minimum.
Q=s.sqrt(h*z/g);dual=k*(h*z*q/2-g*q**3/6)
eq('positive_dual_value',dual.subs(q,Q)+emin);ck('dual_is_supremum',s.diff(dual,q,2).subs(q,Q).is_negative)
eq('at_BMB_classical_coefficient_free',emin.subs(g,16*pi*pi)+k*h**s.Rational(3,2)*z**s.Rational(3,2)/(12*pi))
if a.control=='critical_selects_mass':ck('false_nonzero_critical_gap_mass_curvature',s.diff(energy,m,2).subs(g6,16*pi*pi)!=0)
if a.control=='stable_positive_cubic':ck('false_positive_stable_minimum',emin.is_positive)
if a.control=='BMB_equals_UV':eq('false_BMB_equals_UV',16*pi*pi-192)
out=dict(passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,control=a.control,scope='exact LO/canonical normalization and stable classical source diagnostic; no QFT NLO recomputation or gravity dictionary')
p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps(dict(passed=out['passed'],total=out['total'],failures=[c for c in checks if not c['passed']])));sys.exit(out['passed']!=out['total'])
