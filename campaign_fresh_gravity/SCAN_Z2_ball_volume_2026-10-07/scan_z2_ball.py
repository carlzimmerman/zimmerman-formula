#!/usr/bin/env python3
"""SCAN (10-07, owner question, a post-hoc check, labelled): Z^2 = (cH_Lambda/a0)^2 = (8 pi/3)/kappa^2 equals 32 pi/3 at kappa = 1/2, the volume of a
ball of radius 2 (it also appears as a coefficient in an OpenAI-math circle-packing paper).  How special is that?  Family of readings
'Z^2 = (n-ball volume or (n-1)-sphere area, n = 2..5) at radius r(kappa)', with r in {1/k, 2/k, 1/(2k), sqrt(1/k), 1/k^2}: count the solutions and how
many land in the measured kappa window 0.530 +- 0.037.  P(at least one hit) under a log-uniform spread of the solutions."""
import math, json, os
from scipy.optimize import brentq
from scipy.special import gamma
HERE = os.path.dirname(os.path.abspath(__file__))
V = lambda n, r: math.pi**(n / 2) / gamma(n / 2 + 1) * r**n
S = lambda n, r: n * math.pi**(n / 2) / gamma(n / 2 + 1) * r**(n - 1)
R = {"1/k": lambda k: 1 / k, "2/k": lambda k: 2 / k, "1/(2k)": lambda k: 1 / (2 * k), "sqrt(1/k)": lambda k: k**-0.5, "1/k^2": lambda k: k**-2}
SH = {**{f"V{n}": (lambda n: lambda r: V(n, r))(n) for n in range(2, 6)}, **{f"S{n}": (lambda n: lambda r: S(n, r))(n) for n in range(2, 6)}}
Z2 = lambda k: (8 * math.pi / 3) / k**2
sols = []
for sn, sf in SH.items():
    for rn, rf in R.items():
        f = lambda lk: math.log(Z2(math.exp(lk))) - math.log(sf(rf(math.exp(lk))))
        xs = [i * 0.01 for i in range(-700, 701)]
        for a, b in zip(xs, xs[1:]):
            if f(a) * f(b) < 0:
                sols.append((sn, rn, math.exp(brentq(f, a, b))))
lo, hi = 0.530 - 0.037, 0.530 + 0.037
hits = [s for s in sols if lo <= s[2] <= hi]
lk = [math.log10(s[2]) for s in sols]; spread = max(lk) - min(lk); p1 = math.log10(hi / lo) / spread
P_any = 1 - (1 - p1)**len(sols)
assert abs(Z2(0.5) - 32 * math.pi / 3) < 1e-12 and abs(V(3, 2) - 32 * math.pi / 3) < 1e-12
L = [f"readings {len(SH) * len(R)}, solutions {len(sols)}; in the measured window [{lo:.3f},{hi:.3f}]: {len(hits)} -> {hits}",
     f"per-solution chance {p1:.3f} (log-uniform over {spread:.2f} dex); P(at least one hit among {len(sols)}) = {P_any:.2f}",
     "verdict: the hit is the most natural reading (3-ball, radius 1/kappa, kappa = 1/2 exactly), but a family of this size yields a hit in the window by chance with the probability above -> COINCIDENCE-LEVEL unless a principle requires Z^2 to be that volume."]
print("\n".join(L)); open(os.path.join(HERE, "scan_z2_ball.out"), "w").write("\n".join(L) + "\n")
json.dump(dict(solutions=sols, hits=hits, p1=p1, P_any=P_any), open(os.path.join(HERE, "scan_z2_ball.json"), "w"), indent=1)
