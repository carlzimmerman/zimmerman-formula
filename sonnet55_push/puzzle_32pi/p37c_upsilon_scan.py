"""p37c: fine global Upsilon_disk scan (bulge 1.4x) on SPARC MLS16 cuts (153 galaxies, sigma_int 0.11): for each Upsilon, chi2_min and a0 for the framework kernel (n = 1),
the best n in nu_n, and RAR's Delta chi2. Then the gas/star split (p16 classes T >= 8 vs T <= 5, RAR -> framework kernel) at the chi2-preferred Upsilon.
Footings: 9.3603e-11 (rho_Lambda, kappa = 1/2) and 1.1312e-10 (rho_crit: the original a0 = c sqrt(G rho_c)/2).
Run: python3 p37c_upsilon_scan.py  |  MUTATE=1: sigma_int 0.03 (chi2 scale changes; the preferred Upsilon must still be reported; check U uses the 0.11 calibration -> fails)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
SIG = 0.03 if MUTATE else 0.11
IFn = lambda n: (lambda gb, a: gb * (1 + (gb / a)**(-n))**(1 / (2 * n)))
gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
A = np.exp(np.linspace(math.log(0.5e-10), math.log(2.2e-10), 81))
U = np.round(np.arange(0.50, 0.761, 0.02), 2)
N = [0.7, 0.85, 1.0, 1.15, 1.3]
rows = []
for u in U:
    ch = V.Profile(gals, V.IF_alpha1, ufixed=u).scan(A, SIG); c1 = ch.min(); a1 = V.parabola_min(A, ch, k=6)[0]
    nb = min(N, key=lambda n: V.Profile(gals, IFn(n), ufixed=u).scan(A, SIG).min())
    rar = V.Profile(gals, V.IF_rar, ufixed=u).scan(A, SIG).min() - c1
    rows.append((u, c1, a1, nb, rar))
    print(f"   Upsilon {u:.2f}: chi2(n=1) {c1:8.1f}  a0 {a1:.3e}  best n {nb:<5g} RAR {rar:+7.1f}")
ub = min(rows, key=lambda r: r[1])
print(f"   chi2-preferred Upsilon_disk = {ub[0]:.2f}: a0 = {ub[2]:.3e} (rho_crit footing 1.1312e-10: {100*(ub[2]/1.1312e-10-1):+.1f}%; rho_Lambda footing 9.3603e-11: {100*(ub[2]/9.3603e-11-1):+.1f}%); best n {ub[3]}; RAR {ub[4]:+.1f}")
# gas/star split at the preferred Upsilon, framework kernel
gas = [g for g in gals if g["T"] >= 8]; star = [g for g in gals if g["T"] <= 5]
ag = V.parabola_min(A, V.Profile(gas, V.IF_alpha1, ufixed=ub[0]).scan(A, SIG), k=6); as_ = V.parabola_min(A, V.Profile(star, V.IF_alpha1, ufixed=ub[0]).scan(A, SIG), k=6)
ratio = as_[0] / ag[0]; sr = math.hypot(ag[1], as_[1])
print(f"   gas/star split at Upsilon {ub[0]:.2f} (framework kernel): gas {ag[0]:.3e}, star {as_[0]:.3e}, ratio {ratio:.2f} +- {ratio*sr:.2f}")
check("U the chi2-preferred global Upsilon_disk lies in 0.56-0.66 (stellar-population range), not at the conventional 0.5", 0.56 <= ub[0] <= 0.66)
check("K at that Upsilon the framework kernel is the best member of the nu_n family (n = 1)", ub[3] == 1.0)
check(f"G at that Upsilon the gas/star split is closed within 2 sigma (ratio {ratio:.2f})", abs(math.log(ratio)) < 2 * sr)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
