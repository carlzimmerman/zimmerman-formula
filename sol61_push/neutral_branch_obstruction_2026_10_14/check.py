"""Exact algebra and numeric cross-checks of the coherent attractive branch."""
import json, math, sys
from pathlib import Path
import sympy as sp
from scipy.optimize import brentq
prior=json.loads(Path('sol61_push/explicit_neutral_medium_2026_10_14/run/results.json').read_text())
D,d,g,H=sp.symbols('D d g H',positive=True)
B=H-g*D;t=D-d
x=D*t/(2*B); r2=H*t*t/(4*B*B); mu=-t/2
n=2*x+2*r2
np=((2*D-d)*B+g*D*t)/B**2+H*t*(B+g*t)/B**3
# h*r = -H*x/D so h is not needed as a square root in symbolic identities.
E=d*r2-2*H*x*x/D+g*x*x
identities={'number_derivative':sp.diff(n,D)-np,'atomic_stationarity':mu-(g-H/D)*x,'mediator_number':r2-H*x*x/D**2,'pressure_identity':mu*n-E-mu*x,'energy_derivative':sp.diff(E,D)-mu*sp.diff(n,D)}
checks=[]
for name,expr in identities.items():
    assert sp.factor(expr)==0,name
    checks.append(dict(name=name,exact=True))
hc=1.973269804e-7;hv=.0005;gv=1e-6;dv=2e-9;Hv=hv*hv
nf=sp.lambdify((D,d,g,H),n,'math');npf=sp.lambdify((D,d,g,H),np,'math')
rows=[]
# Root uses y=D/delta-1, evaluated algebraically to avoid subtracting close D,d.
def n_y(y):
    q=dv*(1+y);t=dv*y;b=Hv-gv*q
    return q*t/b+Hv*t*t/(2*b*b)
for old in prior['rows']:
    target=old['total_conserved_number_density_per_m3']*hc**3
    y=math.exp(brentq(lambda z:math.log(n_y(math.exp(z))/target),-30,math.log((Hv/gv/dv-1)*.999),xtol=1e-13))
    q=dv*(1+y);b=Hv-gv*q;xx=q*dv*y/(2*b);chem=-dv*y/2
    slope=-1/(2*npf(q,dv,gv,Hv));pressure=chem*xx
    vals={'chemical_potential_eV':chem,'pressure_eV4':pressure,'compressibility_coefficient_n_dmu_dn_eV':target*slope}
    for k,v in vals.items():
        error=abs(v/old[k]-1)
        tol=2e-7 if 'compressibility' in k else 2e-9
        assert error<tol,(k,error)
        checks.append(dict(name=k,error=error,tolerance=tol))
    assert slope<0 and pressure<0
    rows.append(dict(density_per_m3=old['total_conserved_number_density_per_m3'],D_eV=q,**vals))
result=dict(scope='Exact sign obstruction for the coherent neutral minimum-composition branch of the assigned NR mean-field functional; not a finite-temperature or all-state exclusion',analytic_condition_H_over_gdelta=Hv/(gv*dv),formal_infinite_density_chemical_potential_eV=(dv-Hv/gv)/2,rows=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
