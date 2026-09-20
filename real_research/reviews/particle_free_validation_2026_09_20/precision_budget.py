#!/usr/bin/env python3
"""Planning arithmetic, NOT an observational forecast or detection.
Exact local sensitivities of the conditional orbital and field tests.
"""
import json
from pathlib import Path
import sys
import sympy as S

HERE=Path(__file__).resolve().parent
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE/'run'
OUT.mkdir(exist_ok=True)
q,m=S.symbols('q m',real=True)
beta=S.Rational(1,2)-(1+q)/(1+q+2*q*q)
mass_ratio=1/(1-q*q)
qstar=S.Rational(1,2)
dD_dbeta=S.simplify((S.diff(mass_ratio,q)/S.diff(beta,q)).subs(q,qstar))
assert dD_dbeta==S.Rational(128,45)
beta_extended=S.Rational(1,2)+(m-2)*(1+q)/(2*(1+q+2*q*q))
assert S.simplify(beta_extended.subs(q,qstar)-(3*m/S.Integer(8)-S.Rational(1,4)))==0
dD_dm=S.simplify((-S.diff(mass_ratio,q)*S.diff(beta_extended,m)/S.diff(beta_extended,q)).subs({q:qstar,m:0}))
assert dD_dm==-S.Rational(16,15)

target=S.Rational(4,3)
gap_standard=target-S.sqrt(S.Rational(3,2))
gap_simple=S.Rational(3,2)-target
sigma_D_ideal=gap_standard/3
sigma_beta_ideal=sigma_D_ideal/dD_dbeta
gap_anisotropy=S.sqrt(2)-S.Rational(4,3)
sigma_E_ideal=gap_anisotropy/3

# Correct covariance propagation. Independent errors are only one example.
D,b,E=S.symbols('D beta E',real=True)
R=E*E*(1-2*b)-2
assert S.diff(R,E)==2*E*(1-2*b)
assert S.diff(R,b)==-2*E*E
assert S.diff(R,E).subs({E:S.sqrt(2),b:0})==2*S.sqrt(2)
assert S.diff(R,b).subs({E:S.sqrt(2),b:0})==-4
example_sigma_D=S.Rational(1,50)
example_sigma_beta=S.Rational(1,100)
sigma_R_example=S.sqrt(example_sigma_D**2+(dD_dbeta*example_sigma_beta)**2)
result={
 'status':'exact sensitivities checked; precision numbers are planning-only',
 'orbital':{
  'dD_dbeta_at_quarter':str(dD_dbeta),
  'dD_dm_at_fixed_beta_quarter':str(dD_dm),
  'gap_to_standard':float(gap_standard),'gap_to_simple':float(gap_simple),
  'ideal_3sigma_sigma_D_max':float(sigma_D_ideal),
  'ideal_3sigma_fractional_sigma_D_max':float(sigma_D_ideal/target),
  'ideal_3sigma_sigma_beta_max_if_only_error':float(sigma_beta_ideal),
  'example_independent_sigma_D_0_02_sigma_beta_0_01_residual_sigma':float(sigma_R_example),
  'example_first_order_mass_gradient_0_03_bias_D':float(dD_dm*S.Rational(3,100)),
  'residual_variance':'sigma_D^2+(128/45)^2 sigma_beta^2-2(128/45)Cov(D,beta), plus modeled nuisance terms'},
 'field':{
  'deep_force_ratio_gap':float(gap_anisotropy),
  'ideal_3sigma_sigma_E_max':float(sigma_E_ideal),
  'ideal_3sigma_fractional_sigma_E_max':float(sigma_E_ideal/S.sqrt(2)),
  'residual_variance_at_deep':'8 sigma_E^2+16 sigma_beta^2-16 sqrt(2)Cov(E,beta), plus modeled nuisance terms'},
 'non_claims':['No sample size or date promised','No data were fitted',
 'Gaussian three-sigma separation of two fixed predictions is not model evidence or discovery significance',
 'Systematics, covariance, selection, geometry and finite-field corrections require measurement or validated simulation',
 'Local first-order sensitivities are not uniform error bounds']}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
