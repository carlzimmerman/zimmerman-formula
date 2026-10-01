"""Exact C2 polynomial controls for PF1; no instrument kernels or data."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sys

def integral(coeffs, symmetric=False):
    return sum((Q(c, k+1) * (2 if symmetric else 1)
                for k,c in enumerate(coeffs) if not symmetric or k % 2 == 0), Q(0))

# phi(t) = t - 3 t^3 + 3 t^5 - t^7.
phi = [0,1,0,-3,0,3,0,-1]
i0 = integral(phi, True)
i1 = integral([0]+phi, True)
assert i0 == 0 and i1 == Q(32,315)
# h(t) = 140 t^3 (1-t)^3, t=x-1 in [0,1].
h = [0,0,0,140,-420,420,-140]
h0 = integral(h)
h1 = h0 + integral([0]+h)
assert h0 == 1 and h1 == Q(3,2)
det = -2*h0*h1
assert det == -3
rows=[]
for n in [2,8,32]:
    delta=Q(1,n*n)
    amp=Q(1,n)
    v0=amp*delta*i0
    v1=amp*delta**2*i1
    cp=v1/(2*h1); cm=-cp
    residual0=v0-cp*h0-cm*h0
    residual1=v1-cp*h1+cm*h1
    slope=amp/delta
    lower=10-amp-Q(140,64)*abs(cp)
    assert residual0==0 and residual1==0 and slope==n and lower>0
    assert v1 != 0 and v1+cp*h1-cm*h1 == 2*v1
    rows.append({k:str(v) for k,v in dict(n=n,delta=delta,slope=slope,
                 first_moment_local=v1,c_plus=cp,c_minus=cm,
                 residual0=residual0,residual1=residual1,pressure_lower_bound=lower).items()})
duplicate_rank_det=h0*h1-h0*h1
assert duplicate_rank_det==0
out={"arithmetic":"exact rational", "observations":"integrals against 1 and x; toy only",
     "regularity":"C2 compact polynomial pieces, not C-infinity",
     "witnesses":rows,"controls":{"omitted_compensation":"rejected at every n",
     "reversed_compensation":"rejected at every n", "duplicate_compensators":"rank deficient"},
     "nonclaims":["No empirical response", "No proof by finite sampling", "No global hydrostatic construction"]}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print('3 exact positive witnesses; 3 negative-control types verified')
