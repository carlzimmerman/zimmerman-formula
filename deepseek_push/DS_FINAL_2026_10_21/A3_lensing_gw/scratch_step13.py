#!/usr/bin/env python3
"""Step 13: rational parametrisation f = W^2 (W = sqrt(f)). Fast + exact."""
import sympy as s, time

r = s.symbols('r', positive=True)
K, gamma, a0 = s.symbols('K gamma a0', positive=True)
NV, NP, NPP = s.symbols('NV NP NPP', positive=True)
WV, WP, WPP = s.symbols('WV WP WPP', positive=True)
PV, PP, PPP = s.symbols('PV PP PPP', positive=True)
rho = s.Function('rho')(r)

R3 = 2*WP**2/WV**4 - 4*WPP/WV**3 - 8*WP/(r*WV**3)
u = K*PV/WV
W = a0**2/K*(-u/a0 - s.log(1 - u/a0))
d = (1/WV**3)*(1/r**2)*s.diff(r**2*WV*PV, r)
Lag = 4*s.pi*r**2*(NV*WV**3*(R3/(4*K) - W - (gamma/2)*d**2) + WV*PV*NP - rho*NV)


def Dt(e):
    out = s.diff(e, r)
    for v, dv, ddv in ((NV, NP, NPP), (WV, WP, WPP), (PV, PP, PPP)):
        out += s.diff(e, v)*dv + s.diff(e, ddv)*ddv
    return out


t0 = time.time()
EN = s.cancel((Dt(s.diff(Lag, NP)) - s.diff(Lag, NV))/(4*s.pi*r**2))
EF = s.cancel((s.diff(Lag, WV) - Dt(s.diff(Lag, WP)) + Dt(Dt(s.diff(Lag, WPP))))
              / (4*s.pi*r**2))
EP = s.cancel((s.diff(Lag, PV) - Dt(s.diff(Lag, PP)))/(4*s.pi*r**2))
print('built', round(time.time()-t0, 2), [len(str(e)) for e in (EN, EF, EP)])

m = s.symbols('m', positive=True)
Ns = (1 - m/r)/(1 + m/r); Ws = (1 + m/r)**2
sub = {PV: 0, PP: 0, PPP: 0, rho: 0, NV: Ns, NP: s.diff(Ns, r), NPP: s.diff(Ns, r, 2),
       WV: Ws, WP: s.diff(Ws, r), WPP: s.diff(Ws, r, 2)}
t0 = time.time()
print('EN(Schw)=', s.simplify(EN.subs(sub)), ' EF(Schw)=', s.simplify(EF.subs(sub)),
      ' EP(Schw)=', s.simplify(EP.subs(sub)))
print('check time', round(time.time()-t0, 2))
