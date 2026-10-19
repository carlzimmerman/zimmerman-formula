#!/usr/bin/env python3
"""A declared Abelian screened-exterior calculation; not a full monopole determinant."""
import json
import pathlib
import platform
import sys

import mpmath as mp
import sympy as s

out=pathlib.Path(sys.argv[1])
r,rc,R,m,kappa,psi0,v=s.symbols("r rc R m kappa psi0 v",positive=True)
psi=psi0*rc*s.sinh(m*(R-r))/(r*s.sinh(m*(R-rc)))
checks={}
checks["Yukawa_radial_equation"] = s.simplify(s.diff(psi,r,2)+2*s.diff(psi,r)/r-m**2*psi)==0
checks["core_boundary"] = s.simplify(psi.subs(r,rc)-psi0)==0
checks["wall_boundary"] = psi.subs(r,R)==0
onshell=2*s.pi*kappa*psi0**2*rc*(1+m*rc*s.coth(m*(R-rc)))
boundary=-2*s.pi*kappa*rc**2*psi0*s.diff(psi,r).subs(r,rc)
checks["on_shell_scalar_action"] = s.simplify(onshell-boundary)==0
# Integration by parts is checked directly at the density level.
checks["action_total_derivative"] = s.simplify(s.diff(r**2*psi*s.diff(psi,r),r)-r**2*(s.diff(psi,r)**2+m**2*psi**2))==0
Sinfinity=2*s.pi*kappa*psi0**2*rc*(1+m*rc)
deltaS=2*s.pi*kappa*psi0**2*rc**2*m*(s.coth(m*(R-rc))-1)
checks["finite_minus_infinite"] = s.simplify(onshell-Sinfinity-deltaS)==0
massless=s.limit(onshell,m,0,dir="+")
checks["massless_fixed_wall"] = s.simplify(massless-2*s.pi*kappa*psi0**2*rc*R/(R-rc))==0
Smag=2*s.pi*kappa*(1/rc-1/R)
checks["magnetic_tail_integral"] = s.simplify(s.diff(Smag,R)-2*s.pi*kappa/R**2)==0
logweight_correction=2*s.pi*kappa/R-deltaS
checks["charged_weight_sign"] = s.simplify(logweight_correction-(-(onshell+Smag)+(Sinfinity+2*s.pi*kappa/rc)))==0
# BPS core and unit scalar-charge Yukawa outer region in v^-1 << rc << m^-1.
matched_core=4*s.pi*kappa*(v+m-1/rc)
matched_scalar=2*s.pi*kappa*s.exp(-2*m*rc)*(m+1/rc)
matched_total=matched_core+2*s.pi*kappa/rc+matched_scalar
checks["matched_massless_action"] = s.simplify(matched_total.subs(m,0)-4*s.pi*kappa*v)==0
checks["matched_first_mass_correction"] = s.simplify(s.diff(matched_total,m).subs(m,0)-2*s.pi*kappa)==0
checks["fixed_core_cloud_increment"] = s.simplify(Sinfinity-Sinfinity.subs(m,0)-2*s.pi*kappa*psi0**2*rc**2*m)==0
assert all(checks.values()), checks
mp.mp.dps=60
rows=[]
for mn,rn in [(mp.mpf("0.1"),mp.mpf("5")),(mp.mpf("0.1"),mp.mpf("20")),(mp.mpf("0.3"),mp.mpf("20"))]:
    rcn=mp.mpf("2"); psin=-1/rcn; kn=mp.mpf(1)
    fn=lambda rr: psin*rcn*mp.sinh(mn*(rn-rr))/(rr*mp.sinh(mn*(rn-rcn)))
    df=lambda rr: psin*rcn*(-mn*rr*mp.cosh(mn*(rn-rr))-mp.sinh(mn*(rn-rr)))/(rr**2*mp.sinh(mn*(rn-rcn)))
    val=2*mp.pi*kn*mp.quad(lambda rr: rr**2*(df(rr)**2+mn**2*fn(rr)**2),[rcn,rn])
    formula=2*mp.pi*kn*psin**2*rcn*(1+mn*rcn*mp.coth(mn*(rn-rcn)))
    rel=abs(val-formula)/max(1,abs(formula))
    assert rel<mp.mpf("1e-50")
    rows.append({"m":str(mn),"R":str(rn),"rc":str(rcn),"scalar_action":str(formula),"quadrature_relative_discrepancy":str(rel)})
result={"assertion_tested":"Twelve exact exterior-field/action identities and three finite high-precision independent action quadratures for the declared linear Abelian model.","checks":checks,"symbolic":{"psi":str(psi),"scalar_action":str(onshell),"scalar_finite_correction":str(deltaS),"magnetic_action":str(Smag),"charged_log_weight_correction":str(logweight_correction),"matched_first_order_cloud_action":"2*pi*kappa*m"},"finite_quadratures":rows,"software":{"python":platform.python_version(),"sympy":s.__version__,"mpmath":mp.__version__},"limitations":["Core determinant, fluctuations, boundary functional and magnetic screening are omitted.","The matched BPS core calculation is conditional asymptotic matching, not an exact nonlinear solution.","The finite-wall formula fixes the core Dirichlet value; a dynamical core is a further matching problem.","No vacuum ensemble or stress insertion is evaluated."]}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
