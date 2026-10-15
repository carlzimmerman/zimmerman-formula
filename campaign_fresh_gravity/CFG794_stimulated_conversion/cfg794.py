"""CFG794 -- theory-only: enhancement classes for cold-energy -> light conversion vs the CFG792 gap.
Criteria: FROZEN_CRITERIA.md (e6e2f236b).  Run: python3 cfg794.py  (CFG794_MUTATE=1: tau = 1 us).  Seconds.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG794_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


c, hbar, kB, eV, YR = 2.99792458e8, 1.054571817e-34, 1.380649e-23, 1.602176634e-19, 3.156e7
uc = 6.084e-5
sig = 2.3e5
Ew = 2.5 * eV
w = Ew / hbar
tau = 1e-6 if MUT else 4.4e15 * YR
P("CFG794  enhancement classes for cold-energy -> light (theory only)" + ("  [MUTATE tau=1us]" if MUT else ""))

# K1 mode density x Planck -> a T^4
T = 5800.0
f = lambda x: (x ** 2 / (math.pi ** 2 * c ** 3)) * hbar * x / math.expm1(hbar * x / (kB * T))
uP = integrate.quad(f, 1e10, 60 * kB * T / hbar, limit=400)[0]
aT4 = 4 * 5.670374e-8 / c * T ** 4
k1 = abs(uP / aT4 - 1) < 0.01
P(f"  K1 mode count x Planck {uP:.4e} vs aT^4 {aT4:.4e}: {'PASS' if k1 else 'FAIL'}")

# K2 S
S = 4.4e15 * YR / ((1e-3 / 2000.0) / sig)
k2 = abs(S / 6.4e34 - 1) < 0.05
P(f"  K2 S = {S:.2e} (CFG792 6.4e34): {'PASS' if k2 else 'FAIL'}")

# (a)
Qf = (c / sig) ** 2
Ea = min(1e11, Qf)
P(f"\n(a) resonant: Q_field (c/sigma)^2 = {Qf:.2e}; Q_cavity <= 1e11 -> enhancement <= {Ea:.2e} (field-bandwidth limited)")

# (b) laser threshold
dw = w / Qf
rho_m = w ** 2 * dw / (math.pi ** 2 * c ** 3)
r = uc / (tau * Ew * rho_m)
loss = w / 1e11
short_b = loss / r
P(f"(b) stimulated: mode density {rho_m:.2e} /m^3; spontaneous rate into one mode r = {r:.2e} /s; best cavity loss w/Q = {loss:.2e} /s")
P(f"    -> {'ABOVE' if r > loss else 'BELOW'} laser threshold by x{short_b:.1e}  (seeded stimulation without threshold costs more seed energy than it extracts)")

# (c) coherent volume
lc = hbar * c / (Ew * sig / c)
Ec = (lc / 0.5e-6) ** 2
P(f"(c) coherent volume: l_c = {lc * 1e3:.3f} mm (m = 2.5 eV, conditional) -> gain <= (l_c/d)^2 = {Ec:.1e}")
P("(d) parametric: pump supplies the photons; cold-energy draw remains the stimulated term -> reduces to (b)")

passive = Ea * Ec
gap = S / passive
cls = "GAP CLOSABLE" if (passive >= S or r > loss) else "NOT CLOSABLE"
P(f"\n  best passive (a)x(c) = {passive:.1e} vs needed {S:.1e} -> short x{gap:.1e} ({math.log10(gap):.0f} orders); laser short x{short_b:.0e}")
P(f"  CLASS: {cls}" if not MUT else f"  MUTATE: r {r:.1e} vs loss {loss:.1e} -> {'bites' if r > loss else 'DID NOT BITE'}")
R = dict(lane="CFG794", mutate=MUT, K1=bool(k1), K2=bool(k2), S=S, Ea=Ea, r=r, loss=loss, laser_short=short_b, lc=lc, Ec=Ec,
         passive=passive, gap=gap, cls=cls)
sfx = "_MUTATE" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"cfg794_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg794{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
