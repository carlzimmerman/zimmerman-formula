#!/usr/bin/env python3
"""Separate rectangular-Q-band necessary pressure bound; no dynamics fit."""
import json
import sys
from pathlib import Path
import mpmath as mp
import sympy as s

mp.mp.dps=70
here=Path(__file__).resolve().parent
source=here.parents[1]/'static_gate/matching/run01/results.json'
data=json.loads(source.read_text())
t=s.symbols('t',positive=True)
f=(1-s.exp(-t))/t
checks={'derivative_identity':s.simplify(s.diff(f,t)-((t+1)*s.exp(-t)-1)/t**2)==0,
        'zero_limit':s.limit(f,t,0)==1}
assert all(checks.values())
rows=[]
for mu in sorted({r['mu_Mpc_inverse'] for r in data['rows']}):
    selected=[r for r in data['rows'] if r['mu_Mpc_inverse']==mu]
    X=max(mp.mpf(str(abs(r['phi_geo']))) for r in selected);Qmax=1+X
    delta=mp.mpf(str(selected[0]['dust_fraction_ceiling_delta']))
    aa=-mp.log1p(-delta);C_times_K=mp.mpf(str(mu))**2/2
    KBmin=C_times_K*X**2/Qmax*delta/aa
    for factor in [1,2,10,1000000]:
        L2=factor*X**2/(Qmax*aa);T=X**2/(L2*Qmax)
        actual=C_times_K*L2*(-mp.expm1(-T))
        assert actual>=KBmin*(1-mp.mpf('1e-65'))
    outer=max(selected,key=lambda r:r['r_Mpc']);U=mp.mpf(str(outer['Pi_over_Pic']))
    Q=1+mp.mpf(str(abs(outer['phi_geo'])))
    moment=3*mp.exp(-mp.mpf(2)/3)-(3*U**3+1)*mp.exp(-U**3)
    Kpressure=Q*KBmin*moment
    rows.append(dict(mu_Mpc_inverse=mu,qmax=float(Qmax),delta=float(delta),
                     K_Bband_min_Mpc_inverse2=float(KBmin),
                     outer_K_pressure_min_Mpc_inverse2=float(Kpressure),
                     outer_pressure_over_Pi=float(Kpressure/mp.mpf(str(outer['KPi_Mpc_inverse2']))),
                     coefficient_bound_witnesses=4))
result=dict(status='PASS; rectangular-domain necessary bound only',checks=checks,rows=rows,
            scope='Same perspective QGamma repair,1<=Q<=qmax andPi>=0 independently; no correlated-domain or global dynamical conclusion')
output=Path(sys.argv[1]);output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
