#!/usr/bin/env python3
"""Finite Dirac benchmark matching; never a QCD counterterm."""
import json,sys
from pathlib import Path
import sympy as sp
import mpmath as mp
p=Path(__file__).resolve().parent
out=Path(sys.argv[1])
source=json.loads((p/'run_001/RESULTS.json').read_text())
x=sp.symbols('x',real=True)
eps=sp.symbols('epsilon')
d=4-2*eps
assert sp.expand(d+(2-d)*x-(4-2*x+eps*(2*x-2)))==0
pole=sp.integrate(4-2*x,(x,0,1))
evan=sp.integrate(2*x-2,(x,0,1))
log=sp.integrate(-2*(4-2*x)*sp.log(1-x),(x,0,1))
assert (pole,evan,log)==(3,-1,5)
assert evan+log==4
cPV=(sp.Rational(3,2)-6*sp.log(2))/(16*sp.pi**2)
cCT=(sp.Rational(5,2)+6*sp.log(2))/(16*sp.pi**2)
assert sp.simplify(cPV+cCT-1/(4*sp.pi**2))==0
mp.mp.dps=55
target=1/(4*mp.pi**2)
vals=[]
for row in source['PV_results']:
 ll=mp.mpf(row['Lambda_over_m'])
 dd=mp.mpf(row['M_u_over_m'])
 ct=(-3*mp.log(ll*ll)+mp.mpf('2.5')+6*mp.log(2))/(16*mp.pi**2)
 matched=dd+ct
 # Exact algebraic translation of the independently derived residual.
 err=abs((matched-target)-mp.mpf(row['difference_from_proved_asymptotic_constant']))
 assert err<mp.mpf('1e-46')
 vals.append({'Lambda_over_m':str(ll),'matched_at_mu_equals_m':mp.nstr(matched,45),'finite_cutoff_difference_from_exact_limit':mp.nstr(matched-target,45),'algebraic_translation_error':mp.nstr(err,12)})
r={'schema':'fsp008.dirac_MSbar_matching.v1','exact_pole_coefficient':str(pole),'exact_evanescent_contribution':str(evan),'exact_log_integral':str(log),'exact_MSbar_finite_constant':'4/(16*pi^2)','exact_PV_to_MSbar_finite_counterterm':'(5/2+6*log(2))/(16*pi^2)','fixed_MSbar_m_mu_equals_m_limit':mp.nstr(target,45),'finite_PV_translation':vals,'domain':'One elementary Dirac field, first derivative at u=e^2=0; not a QCD proton matching calculation.','assertion_count':6,'limitations':['Finite cutoff results are not the asymptotic limit.','No alpha value, QCD parameter, or cosmological datum is input.','Numerical translations use saved 48-digit run_001 data; not interval certified.']}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'assertions':6,'PV_cases_translated':len(vals),'MSbar_slope_mu_equals_m':mp.nstr(target,40)},indent=2))
