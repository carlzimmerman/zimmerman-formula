"""p20b: branch B -- the khronon's universal horizon (UH) in Schwarzschild-de Sitter. Criteria: SETUP.md (frozen first).
Framework core: khronon with beta = 0 and alpha_c <= 3.2e-9 (FP2), so the khronon is a test field on SdS (decoupling limit). Infinite-speed limit:
the khronon foliation is constant-mean-curvature, K = div u = (1/r^2) d(r^2 u^r)/dr = K0, matched to cosmic time at large r (K0 = 3H, flat dS slicing).
So u^r = H r + C/r^2 and (u.chi)^2 = u_t^2 = f + (u^r)^2 =: F(r). The UH is where F has a DOUBLE zero (the slices pile up; regularity fixes C).
Surface gravity kappa_UH = (1/2) |u^r| sqrt(F''/2) at r_UH (= (1/2) u^a d_a (u.chi), Berglund-Bhattacharyya-Mattingly definition).
G = c = 1, f = 1 - 2M/r - H^2 r^2, Lambda = 3H^2. Target (puzzle): kappa r = 1/2 AND Lambda r^2 = 8 pi.
Run: python3 p20b_khronon_universal_horizon.py  |  MUTATE=1: u^r = 2 H r + C/r^2 (wrong CMC value); checks S1 and S3 must fail
"""
import os, sys
import numpy as np
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
r, M, H = sp.symbols("r M H", positive=True); C = sp.symbols("C", real=True)
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
kH = 2 if MUTATE else 1
f = 1 - 2 * M / r - H**2 * r**2
ur = kH * H * r + C / r**2
F = sp.expand(f + ur**2)
print(f"   F(r) = f + (u^r)^2 = {sp.simplify(F)}")
check("S1 the cosmological term cancels: F = 1 - 2(M - H C)/r + C^2/r^4 (Schwarzschild form with M_eff = M - H C)",
      sp.simplify(F - (1 - 2 * (M - H * C) / r + C**2 / r**4)) == 0)
# Schwarzschild limit (H = 0): classic maximal-slice limit r = 3M/2, kappa = sqrt(2/27)/M
F0 = F.subs(H, 0)
sol = sp.solve([F0, sp.diff(F0, r)], [r, C], dict=True)
s0 = [s for s in sol if s[r].is_positive and s[C].is_negative][0]
k0 = sp.simplify(sp.Rational(1, 2) * sp.Abs(ur.subs(H, 0).subs(s0)) * sp.sqrt(sp.diff(F0, r, 2).subs(s0) / 2))
print(f"   H = 0: r_UH = {s0[r]}, C = {s0[C]}, kappa_UH = {k0}, kappa r = {sp.simplify(k0 * s0[r])}")
check("S2 Schwarzschild limit: r_UH = 3M/2 and kappa_UH = sqrt(2/27)/M (the known maximal-slicing values)",
      sp.simplify(s0[r] - 3 * M / 2) == 0 and sp.simplify(k0 - sp.sqrt(sp.Rational(2, 27)) / M) == 0)

# SdS family: x = H M from 0 to Nariai (x_N = 1/(3 sqrt 3)); numeric double root of F; compare with the BH Killing horizon r_b
rows = []
for x in np.linspace(1e-4, 1 / (3 * np.sqrt(3)) * 0.999, 300):
    Mv, Hv = 1.0, x
    Fn = sp.lambdify((r, C), F.subs({M: Mv, H: Hv}))
    dF = sp.lambdify((r, C), sp.diff(F, r).subs({M: Mv, H: Hv}))
    d2F = sp.lambdify((r, C), sp.diff(F, r, 2).subs({M: Mv, H: Hv}))
    # M_eff = M - H C with C = -(sqrt27/4) M_eff^2  =>  (sqrt27/4) H M_eff^2 - M_eff + M = 0 (smaller root -> Schwarzschild as H -> 0)
    a = np.sqrt(27) / 4 * Hv * kH**0
    Meff = (1 - np.sqrt(1 - 4 * a * Mv)) / (2 * a) if 4 * a * Mv <= 1 else np.nan
    if not np.isfinite(Meff): continue
    Cv = -np.sqrt(27) / 4 * Meff**2; ru = 1.5 * Meff
    ok = abs(Fn(ru, Cv)) < 1e-9 and abs(dF(ru, Cv)) < 1e-9
    kap = 0.5 * abs(Hv * kH * ru + Cv / ru**2) * np.sqrt(d2F(ru, Cv) / 2)
    rts = np.roots([-Hv**2, 0, 1, -2 * Mv]); rb = np.sort(rts[(abs(rts.imag) < 1e-12) & (rts.real > 0)].real)[0]
    rows.append((x, ru, rb, kap * ru, 3 * Hv**2 * ru**2, ok))
rows = np.array(rows)
print(f"   SdS family ({len(rows)} masses up to Nariai): kappa_UH r_UH in [{rows[:,3].min():.4f}, {rows[:,3].max():.4f}];"
      f" Lambda r_UH^2 in [{rows[:,4].min():.2e}, {rows[:,4].max():.4f}]; r_UH/r_b in [{(rows[:,1]/rows[:,2]).min():.3f}, {(rows[:,1]/rows[:,2]).max():.3f}]")
check("S3 every UH is a genuine double root of F (regular foliation) and lies inside the black-hole Killing horizon", rows[:, 5].all() and (rows[:, 1] < rows[:, 2]).all())
check(f"B1 Lambda r_UH^2 <= {rows[:,4].max():.3f} < 1 for every mass: the area condition Lambda r^2 = 8 pi (= 25.1) is unreachable (the UH sits inside r_b, and Lambda r_b^2 <= 1)",
      rows[:, 4].max() < 1)
check(f"B2 kappa_UH r_UH stays in [{rows[:,3].min():.3f}, {rows[:,3].max():.3f}] (1/sqrt 6 = 0.408 at H = 0), never 1/2 -> branch B FAILS criterion 1",
      not ((rows[:, 3].min() <= 0.5) and (rows[:, 3].max() >= 0.5)))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
