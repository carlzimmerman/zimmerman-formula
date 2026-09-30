"""Exact local weak-action reduction plus finite illustrative annuli.

The expansion is frozen only at leading order under the conditions in
EXPANSION_BRIDGE_MOND_RESULTS.md; no complete ADM solution is asserted.
"""
import argparse
import json
from pathlib import Path
import sympy as s
import numpy as np

parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
eps,r,M2,H,beta,G,Mass,a0=s.symbols('eps r M2 H beta G Mass a0',positive=True)
phi,phip,psi,P,b=s.symbols('phi phip psi P b',real=True)
Lcurv=M2*((1+eps*phi)*(s.exp(eps*psi)+s.exp(-eps*psi))+2*r*eps*phip*s.exp(-eps*psi))
L2=s.expand(s.series(Lcurv,eps,0,3).removeO()).coeff(eps,2)
C=beta*M2/(3*H)
Lred=-M2*r**2*(phip-P)**2-C*r**2*P**3
a0bridge=2*H/beta
g=b+s.sqrt(a0*b)
checks={
 'curvature_second_order':L2-M2*(psi**2-2*r*psi*phip),
 'metric_constraint':s.diff(L2,psi)-2*M2*(psi-r*phip),
 'metric_elimination':L2.subs(psi,r*phip)+M2*r**2*phip**2,
 'reduced_polarization':s.diff(Lred,P)-2*M2*r**2*(phip-P-P**2/a0bridge),
 'potential_flux':s.diff(Lred,phip)+2*M2*r**2*(phip-P),
 'Gauss_mass_normalization':Mass/(8*s.pi*M2*r**2)-(G*Mass/r**2).subs(G,1/(8*s.pi*M2)),
 'exact_reduced_force':(g-b)**2/a0-b,
 'deep_BTFR':(r*s.sqrt(a0*G*Mass/r**2))**2-G*Mass*a0,
 'coefficient_ratio':3*H**2/a0bridge**2-3*beta**2/4,
}
results={key:s.simplify(value)==0 for key,value in checks.items()}
assert all(results.values()),results
rr=np.geomspace(1e-6,1e-5,32);GM=1e-16
samples=[]
for betaval in [2.,10.,20.]:
 scale=2/betaval;flux=GM/rr**2;polar=np.sqrt(scale*flux);acc=flux+polar
 samples.append({'beta':betaval,'a0':scale,'Lambda_over_a0_squared':3/scale**2,
 'max_Hr_over_g_over_H':float(np.max(rr/acc)),
 'max_g_over_H':float(np.max(acc)),
 'max_deep_BTFR_fractional_correction':float(np.max((rr*acc)**2/(GM*scale)-1)),
 'max_beta_P_over_H_cubed':float(np.max(betaval*polar**3))})
assert all(v['max_g_over_H']<.011 for v in samples)
assert all(v['max_beta_P_over_H_cubed']<3e-6 for v in samples)
out={'passed_symbolic':len(results),'checks':results,'annulus':{'H':1,'GM':GM,'r_min':1e-6,'r_max':1e-5,'points':32},
 'samples':samples,'scope':'Exact reduced-action identities and illustrative reduced field profiles; no coupled ADM solve, error theorem, source equilibrium or observational fit.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
