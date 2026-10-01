#!/usr/bin/env python3
"""Exact conditional causal-branch identities and named mutation."""
import json,os,sys
from pathlib import Path
import sympy as s
y,ye,V,Pc,c2=s.symbols('y ye V Pc c2',positive=True)
F=lambda z:s.sqrt(1+z)+s.log((s.sqrt(1+z)-1)/(s.sqrt(1+z)+1))
rho=Pc/V*y/s.sqrt(1+y);re=Pc/V*ye/s.sqrt(1+ye)
mut=os.environ.get('MUTATE')=='1'
energy=rho*(c2+V*(F(y)-F(ye)))+(0 if mut else Pc*ye)
h=s.diff(energy,y)/s.diff(rho,y);P=s.simplify(rho*h-energy)
Q=V*(1+y)**s.Rational(3,2)/(1+y/2);gap=s.simplify(h-Q)
checks={
 'constitutive_finite_pressure':s.simplify(P-Pc*(y-ye))==0,
 'zero_edge_pressure':s.simplify(P.subs(y,ye))==0,
 'positive_pressure_derivative_identity':s.simplify(s.diff(P,y)/s.diff(rho,y)-Q)==0,
 'gap_increases_identity':s.simplify(s.diff(gap,y)-4*V*s.sqrt(1+y)/(y*(y+2)**2))==0,
 'edge_gap_identity':s.simplify(gap.subs(y,ye)-(c2-V*ye*s.sqrt(1+ye)/(ye+2)))==0,
 'edge_energy_identity':s.simplify(energy.subs(y,ye)-(re*c2+Pc*ye))==0,
 'dominant_energy_derivative_identity':s.simplify(s.diff(energy-P,y)/s.diff(rho,y)-gap)==0}
out={'mutation':mut,'checks':checks,'pressure':str(P),
 'universal_hypotheses':'Positive Pc,V,ye,c2; y>=ye; c2>V*ye*sqrt(1+ye)/(ye+2)',
 'proof_steps_not_replaced_by_sampling':['Displayed positive rho derivative and gap derivative','Boundary gap and energy positive under hypotheses','Monotonicity extends inequalities to all y>=ye'],
 'non_claims':['No formation or boundary selection','No gravitational or nonlinear free-boundary stability','No joint data pass or unique EOS normalization']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
