#!/usr/bin/env python3
"""Independent local constitutive/current-action audit, exact symbolic identities only."""
from pathlib import Path
import sympy as s,json
p=Path(__file__).resolve().parent
y,V,Pc,c2,E0=s.symbols('y V Pc c2 E0',positive=True)
rho=Pc/V*y/s.sqrt(1+y);F=s.sqrt(1+y)+s.log((s.sqrt(1+y)-1)/(s.sqrt(1+y)+1));energy=rho*(c2+E0+V*F)
h=s.simplify(s.diff(energy,y)/s.diff(rho,y));dpdr=s.simplify(Pc/s.diff(rho,y));P=s.simplify(rho*h-energy)
checks={
'pressure':s.simplify(P-Pc*y)==0,
'enthalpy_explicit':s.simplify(h-(c2+E0+V*(2*s.sqrt(1+y)+s.log((s.sqrt(1+y)-1)/(s.sqrt(1+y)+1)))))==0,
'dP_drho':s.simplify(dpdr-V*(1+y)**s.Rational(3,2)/(1+y/2))==0,
'F_prime':s.simplify(s.diff(F,y)-(y+2)/(2*y*s.sqrt(1+y)))==0,
'low_density_enthalpy_log':s.simplify(s.limit((h-c2-E0)/V-s.log(y),y,0)-(2-s.log(4)))==0,
'positive_density_map':s.simplify(s.diff(rho,y)-(Pc/V)*(1+y/2)/(1+y)**s.Rational(3,2))==0}
# At one local Lorentz frame, vary inverse metric while holding contravariant J fixed.
# Since this is tensorial, arbitrary J and arbitrary symmetric delta g^{-1} test all tensor components.
jt,jx,htt,htx,hxx,eps,er,L=s.symbols('jt jx htt htx hxx eps er L',real=True)
r=s.sqrt(jt**2-jx**2);eta=s.diag(-1,1);J=s.Matrix([jt,jx]);H=s.Matrix([[htt,htx],[htx,hxx]]);dg=-eta*H*eta
rho_var=s.simplify(-(J.T*dg*J)[0]/(2*r));ul=eta*J/r
checks['metric_variation_fixed_contravariant_current']=s.simplify(rho_var-r*(ul.T*H*ul)[0]/2)==0
# delta(sqrt(-g)L)/sqrt(-g)=-er delta rho -L/2 trace(g delta g^{-1}).
T=r*er*(ul*ul.T)+L*eta
checks['stress_variation']=s.simplify(-er*rho_var-L*s.trace(eta*H)/2+s.trace(T*H)/2)==0
checks['on_shell_L_pressure']=s.simplify(-eps-r*er*(ul.T*J/r)[0]-(r*er-eps))==0
out={'checks':{k:bool(v) for k,v in checks.items()},'pressure':str(P),'enthalpy_denergy_drho':str(h),'sound_speed_SI':'c_s^2 = c^2 * (dP/drho)/(d epsilon/drho), epsilon and P both SI energy density; no extra c^2 in denominator','scope':'local tensor variation and exact constitutive identities only; no global health, boundary selection or host-label derivation'}
(p/'current_action_review_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
