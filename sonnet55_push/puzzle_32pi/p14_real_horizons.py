"""p14: is the 'actual' horizon the wrong one? Compare A Lambda = 32 pi^2 with the real horizons of a LambdaCDM universe.

Pure de Sitter: r = sqrt(3/Lambda), A Lambda = 12 pi exactly (metric identity, not an approximation).
Our universe is not pure de Sitter, so test its three horizons (Hubble/apparent, event, particle) at z = 0, 0.5, 1, 2.5:
  ratio = Lambda A / (32 pi^2)  and the a0 implied by a Schwarzschild horizon of that area, a0 = c^2/(2R).
Cosmology: Planck 2018 (H0 67.66, Om 0.3111, Or 9e-5, flat). a0 footings: 9.36e-11 (framework) / 1.13e-10 (SPARC).

Run: python3 p14_real_horizons.py   |   MUTATE=1: use the event horizon in check B (must fail)
"""
import os, sys
import numpy as np
from scipy.integrate import quad

MUTATE = os.environ.get("MUTATE") == "1"
c = 2.99792458e8; Mpc = 3.0857e22; Gly = 9.4607e24
H0 = 67.66e3 / Mpc; Om = 0.3111; Or = 9.0e-5; OL = 1 - Om - Or
H = lambda a: H0 * np.sqrt(Or / a**4 + Om / a**3 + OL)
Lam = 3 * OL * H0**2 / c**2
res = []
def check(n, ok): res.append(ok); print(("PASS  " if ok else "FAIL  ") + n)

def horizons(a):
    return dict(Hubble=c / H(a),
                event=a * quad(lambda x: c / (x * x * H(x)), a, np.inf, limit=500)[0],
                particle=a * quad(lambda x: c / (x * x * H(x)), 1e-12, a, limit=500)[0])

ratio = lambda R: Lam * 4 * np.pi * R * R / (32 * np.pi**2)
RdS = np.sqrt(3 / Lam)
print(f"de Sitter radius {RdS/Gly:.2f} Gly; radius needed for 32 pi^2: sqrt(8 pi/Lambda) = {np.sqrt(8*np.pi/Lam)/Gly:.2f} Gly")
tab = {}
for z in (0, 0.5, 1, 2.5):
    h = horizons(1 / (1 + z)); tab[z] = h
    for k, R in h.items():
        print(f"z={z:<4} {k:9s} R={R/Gly:6.2f} Gly  Lambda A/32pi^2={ratio(R):6.3f}  a0=c^2/2R={c*c/(2*R):.3g}")

check("A pure de Sitter horizon: Lambda A = 12 pi (ratio 3/(8 pi))", abs(ratio(RdS) - 3 / (8 * np.pi)) < 1e-12)
Rb = tab[0]["event" if MUTATE else "particle"]
check(f"B today's particle horizon lands within 20% of 32 pi^2 (ratio {ratio(Rb):.3f}); its a0 {c*c/(2*Rb):.3g} sits between the footings",
      abs(ratio(Rb) - 1) < 0.2 and 9.36e-11 < c * c / (2 * Rb) < 1.13e-10)
check("C Hubble and event horizons miss by a factor 9-12 today", ratio(tab[0]["Hubble"]) < 0.12 and ratio(tab[0]["event"]) < 0.12)
g = tab[2.5]["particle"]; g0 = tab[0]["particle"]
check(f"D but the particle horizon grows: implied a0(z=2.5)/a0(0) = {g0/g:.2f}, not FLAT (and above the a0~H(z) rival's {H(1/3.5)/H0:.2f})",
      g0 / g > H(1 / 3.5) / H0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
