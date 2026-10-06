"""cm15: does the record's direction-blind EFE rule (SW01/SW05: g = nu(sqrt(x^2 + eta^2)) g_own, x = g_own/a0, eta = |g_ext|/a0 -- the magnitude of the external
field kept, its direction removed) survive the cluster-satellite lensing of cm14b? Same inputs and r_bg estimate as cm14b (Sifon+2018 table).
Readings: A no EFE (isolated: nu(x)); D SW01 quadrature rule nu(sqrt(x^2 + eta^2)); B cm14b's linear 1-D form nu(x + eta) for reference.
Verdict per reading: chi^2 over the 5 bins (5 dof), CONSISTENT if p > 0.01.
Run: python3 cm15_sw01_rule_vs_satellites.py | MUTATE=1 sets eta = 0 in D (D must then pass, i.e. check X fails)
"""
import os, sys, math, numpy as np
from scipy.stats import chi2
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cm14b_sifon_table.py")).read().split("rows = {")[0]
exec(src)
R_ = {"A": [], "D": [], "B": []}
for (lm, (lmb, elo, ehi), Rs) in zip(mstar, mbg, rsat):
    Mb = 1.2 * 10**lm; ret = 0.13 * (0.1200 / 0.02237) * Mb; mb = 10**lmb; sig = 0.5 * (elo + ehi)
    rbg = (mb / (4 * math.pi * rho_h(Rs)))**(1 / 3); x = G * Mb * Msun / (rbg * Mpc)**2 / a0; eta = 0.0 if MUTATE else G * Mh(Rs) * Msun / (Rs * Mpc)**2 / a0
    for k, nuv in (("A", nu(x)), ("D", nu(math.sqrt(x * x + eta * eta))), ("B", nu(x + eta))):
        R_[k].append((lmb - math.log10(nuv * Mb + ret)) / sig)
    print(f"   log M* {lm:5.2f}: x {x:.3f}, eta {eta:.2f}: nu A {nu(x):.2f}, D {nu(math.sqrt(x*x+eta*eta)):.2f}, B {nu(x+eta):.2f}")
out = {}
for k, lab in (("A", "no EFE"), ("D", "SW01 quadrature EFE"), ("B", "linear EFE")):
    z = np.array(R_[k]); X2 = float((z**2).sum()); p = float(chi2.sf(X2, 5)); out[k] = p
    print(f"   {k} {lab:20s}: chi2 {X2:6.1f}/5  p {p:.2g}  -> {'CONSISTENT' if p > 0.01 else 'EXCLUDED'}")
check("X the SW01 magnitude-EFE rule is excluded by the satellite lensing (MUTATE eta = 0 must fail)", out["D"] <= 0.01)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
