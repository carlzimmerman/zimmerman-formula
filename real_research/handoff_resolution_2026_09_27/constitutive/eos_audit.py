#!/usr/bin/env python3
"""Conditional P2 equilibrium EOS: exact identities plus finite controls."""
import json, math, os, sys
from pathlib import Path
import numpy as np
import sympy as s

G=6.67430e-11; MS=1.98847e30
y,M,a,g=s.symbols('y M a g',positive=True)
r=s.sqrt(g*M/(a*y)); total=M*s.sqrt(1+1/y)
rho=a*M/(4*s.pi*g*r*total); pressure=a*a*y/(8*s.pi*g)
C=a**s.Rational(3,2)/(4*s.pi*g**s.Rational(3,2)*s.sqrt(M))
rho_y=C*y/s.sqrt(1+y)
cs=s.sqrt(g*M*a)/2*(1+y)**s.Rational(3,2)/(1+y/2)
checks={
 'density_reparameterization':s.simplify(rho-rho_y)==0,
 'effective_sound_derivative':s.simplify(s.diff(pressure,y)/s.diff(rho_y,y)-cs)==0,
 'hydrostatic_identity':s.simplify(s.diff(pressure,y)/s.diff(r,y)+rho*g*total/r**2)==0,
}
mut=os.environ.get('MUTATE')=='1'
rows=[]
for a0 in [9.3603e-11,1.1312e-10]:
 vals=[]
 for mb in [1e9,1e11]:
  mass=mb*MS; target=1e-23
  # Mutation erroneously removes host-mass dependence from the constitutive map.
  used_mass=1e9*MS if mut else mass
  cc=a0**1.5/(4*np.pi*G**1.5*np.sqrt(used_mass))
  q=target/cc; yy=.5*(q*q+q*np.sqrt(q*q+4))
  rr=np.sqrt(G*mass/(a0*yy)); mt=mass*np.sqrt(1+1/yy)
  actual_rho=a0*mass/(4*np.pi*G*rr*mt)
  pp=a0*a0*yy/(8*np.pi*G)
  vals.append({'Mb_solar':mb,'target_rho':target,'actual_rho':float(actual_rho),
               'y':float(yy),'r_kpc':float(rr/3.085677581491367e19),'P_Pa':float(pp)})
 checks[f'same_density_{a0}']=all(abs(v['actual_rho']/v['target_rho']-1)<1e-12 for v in vals)
 checks[f'distinct_pressure_{a0}']=vals[1]['P_Pa']/vals[0]['P_Pa']>1.01
 rows.append({'a0':a0,'points':vals,'pressure_ratio':vals[1]['P_Pa']/vals[0]['P_Pa']})
res={'mutation':mut,'checks':checks,'rows':rows,
 'scope':'Point-baryon, unshifted CFG2 hydrostatic family. Rules out a single-valued universal P(rho) reproducing this entire family. Does not rule out entropy/field/environment dependence or a broader covariant theory.',
 'identities':{'rho':'C_M*y/sqrt(1+y)','C_M':'a0^(3/2)/(4*pi*G^(3/2)*sqrt(Mb))',
 'P':'a0^2*y/(8*pi*G)','cs_equilibrium_squared':'sqrt(G*Mb*a0)/2*(1+y)^(3/2)/(1+y/2)'}}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
