#!/usr/bin/env python3
"""Exact pressure/enthalpy identities for the stated conditional current action."""
import json,os,sys
from pathlib import Path
import sympy as s
y,V,Pc,Pe,E0,c2=s.symbols('y V Pc Pe E0 c2',positive=True)
rho=(Pc/V)*y/s.sqrt(1+y)
F=s.sqrt(1+y)+s.log((s.sqrt(1+y)-1)/(s.sqrt(1+y)+1))
mut=os.environ.get('MUTATE')=='1'
if mut:F=s.sqrt(1+y)  # dropping the internal-energy logarithm changes the EOS
energy=rho*(c2+V*F+E0)
dedrho=s.diff(energy,y)/s.diff(rho,y)
pressure=s.simplify(rho*dedrho-energy)
checks={'constitutive_pressure':s.simplify(pressure-Pc*y)==0,
        'enthalpy_identity':s.simplify(dedrho-(energy+Pc*y)/rho)==0,
        'rest_and_label_zero_cancel':s.diff(pressure,E0)==0 and s.diff(pressure,c2)==0,
        'physical_pressure_offset':s.simplify(rho*dedrho-(energy+Pe)-(pressure-Pe))==0}
out={'mutation':mut,'checks':checks,'pressure':str(pressure),
     'scope':'Exact constitutive identities only. Does not derive the material label, vacuum completion, boundary or full stability.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
