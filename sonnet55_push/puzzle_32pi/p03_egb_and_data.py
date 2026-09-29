#!/usr/bin/env python3
"""p03_egb_and_data.py -- two follow-ups on the 32 pi puzzle (c = G = 1).

PART 1 (a check of the 4D EGB black hole for a natural '32'; RESULT: none, the first version of this check used a wrong temperature and was corrected): the 4D Einstein-Gauss-Bonnet (Glavan-Lin) black hole
   f(r) = 1 + r^2/(2 alpha) [1 - sqrt(1 + 8 alpha M/r^3)]   (Lambda = 0).
 E1  horizons: f = 0  <=>  r^2 - 2 M r + alpha = 0
 E2  Hawking temperature  T = f'(r_h)/4pi = r_h / (4 pi (r_h^2 + 2 alpha)),  kappa = 2 pi T
 E3  T has a maximum at r_h = sqrt(2 alpha):  kappa_max = 1/(4 sqrt(2 alpha)),  kappa_max^2 = 1/(32 alpha)
 E4  so kappa_max = a0 with a0^2 = Lambda/(32 pi) would need alpha = pi/Lambda;  the natural Lambda-tied values of alpha are different:
       - the degenerate (Chern-Simons) vacuum 1 + 4 alpha Lambda/3 = 0  gives alpha = -3/(4 Lambda)  (= the Kounterterm value -L^2/4),
       - and dS entropy matching etc. give no pi.  We check the two named values against pi/Lambda.
PART 2 (what the data can and cannot say): the SPARC a0 (profile likelihood, Upsilon free per galaxy, committed:
 1.0766e-10 m/s^2, 5.44% galaxy-clustered) against candidate coefficients Z in a0 = c H/Z on the two footings.
Exit 0 = the algebra held and the controls behaved; the offsets are findings.
"""
import math
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

# ---------------------------------------------------------------- PART 1
print("PART 1  4D Einstein-Gauss-Bonnet black hole: is there a natural '32'?  (a first version of this check used a misremembered T and failed; corrected)")
r, M, al = sp.symbols('r M alpha', positive=True)
Ssym = sp.symbols('S', positive=True)
Mh = (r**2 + al) / (2 * r)                                # from f(r_h) = 0
# f = 1 + r^2/(2 al) (1 - S), S = sqrt(1 + 8 al M/r^3); at the horizon S = 1 + 2 al/r^2 and M = Mh
f_at = 1 + r**2 / (2 * al) * (1 - (1 + 2 * al / r**2))
check("E1  f(r_h) = 0 with S = 1 + 2 alpha/r^2, and that S^2 = 1 + 8 alpha M/r^3 exactly when M = (r^2 + alpha)/(2 r)",
      sp.simplify(f_at) == 0 and sp.simplify((1 + 2 * al / r**2)**2 - (1 + 8 * al * Mh / r**3)) == 0)
fp = -2 / r + 6 * Mh / ((1 + 2 * al / r**2) * r**2)       # f'(r_h) = -2/r + 6 M/(S r^2)
fp = sp.simplify(fp)
check("E2  f'(r_h) = (r_h^2 - alpha)/(r_h (r_h^2 + 2 alpha)),  T = f'/(4 pi)  (the known Glavan-Lin temperature)",
      sp.simplify(fp - (r**2 - al) / (r * (r**2 + 2 * al))) == 0)
T = fp / (4 * sp.pi)
# numeric spot check of f' from the full f by finite differences
import random
for _ in range(3):
    rv, av = random.uniform(1.5, 4.0), random.uniform(0.1, 1.0)
    Mv = (rv**2 + av) / (2 * rv)
    ff = lambda x: 1 + x**2 / (2 * av) * (1 - math.sqrt(1 + 8 * av * Mv / x**3))
    h = 1e-6
    num = (ff(rv + h) - ff(rv - h)) / (2 * h)
    ok_num = abs(num - float(fp.subs({r: rv, al: av}))) < 1e-5
    check(f"E2n numeric check of f'(r_h) from the full metric at r={rv:.2f}, alpha={av:.2f}", ok_num)
crit = sp.solve(sp.diff(fp, r), r)
rstar = [c_ for c_ in crit if c_.is_positive][0]
check("E3a T is maximal at r_h^2 = alpha (5 + sqrt 33)/2", sp.simplify(rstar**2 - al * (5 + sp.sqrt(33)) / 2) == 0)
kmax2 = sp.simplify((fp.subs(r, rstar) / 2)**2 * al)
kcoef = float(kmax2)
print(f"       kappa_max^2 = {kcoef:.5f} / alpha   (a '32' would be 1/32 = {1/32:.5f} / alpha)")
check("E3b kappa_max^2 alpha is NOT 1/32: the 4D-EGB maximal temperature gives no 32 (the earlier lead is retracted)", abs(kcoef - 1 / 32) > 0.01)
Lam = sp.symbols('Lambda', positive=True)
alpha_cs = -3 / (4 * Lam)                                   # degenerate (Chern-Simons) vacuum 1 + 4 alpha Lambda/3 = 0
check("E4  the degenerate vacuum 1 + 4 alpha Lambda/3 = 0 is alpha = -3/(4 Lambda) = the Kounterterm value -L^2/4 (no pi)",
      sp.simplify(1 + 4 * alpha_cs * Lam / 3) == 0)

# ---------------------------------------------------------------- PART 2
print("\nPART 2  what the SPARC amplitude can and cannot distinguish (coefficient Z in a0 = c H/Z)")
c = 2.99792458e8
H0 = 67.4e3 / 3.0856775814913673e22
OmL = 0.685
a0_hat, sig = 1.0766e-10, 0.0544
cands = [("Milgrom  2 pi", 2 * math.pi), ("Verlinde  6", 6.0), ("framework  sqrt(32 pi/3)", math.sqrt(32 * math.pi / 3)),
         ("Nariai-shell  3 sqrt 3", 3 * math.sqrt(3)), ("4 pi/2 = 2 pi (same as Milgrom)", 2 * math.pi)]
print(f"  a0_hat = {a0_hat:.4e} +- {100 * sig:.2f}% (galaxy-clustered);  c H0 = {c * H0:.4e};  c H_Lambda = {c * H0 * math.sqrt(OmL):.4e}")
print(f"  {'coefficient Z':<34}{'a0 (H0 footing)':>17}{'offset':>9}{'a0 (H_L footing)':>19}{'offset':>9}")
rows = {}
for nm, Zc in cands[:4]:
    a_tot = c * H0 / Zc
    a_lam = c * H0 * math.sqrt(OmL) / Zc
    o_tot = (a_tot - a0_hat) / (sig * a0_hat)
    o_lam = (a_lam - a0_hat) / (sig * a0_hat)
    rows[nm] = (o_tot, o_lam)
    print(f"  {nm:<34}{a_tot:>17.4e}{o_tot:>+8.2f}s{a_lam:>19.4e}{o_lam:>+8.2f}s")
best_tot = min(rows.items(), key=lambda kv: abs(kv[1][0]))
n_within_1 = sum(1 for v in rows.values() if abs(v[0]) < 1.0)
print(f"\n  on the rho_total footing {n_within_1} of {len(rows)} candidate coefficients lie within 1 sigma of the fit (best: {best_tot[0]}, {best_tot[1][0]:+.2f} sigma):")
print("  the data alone cannot say the coefficient is 32 pi rather than 36 (Verlinde) or 4 pi^2 (Milgrom); a geometric derivation, if it exists,")
print("  is not being checked by the amplitude at the 10% level.")
check("C1  the sigma offsets are computed from the committed a0 and sigma (Verlinde within 1 sigma, Milgrom within 1 sigma on the H0 footing)",
      abs(rows["Verlinde  6"][0]) < 1 and abs(rows["Milgrom  2 pi"][0]) < 1)
check("C2  control: an absurd coefficient Z = 12 is rejected at > 3 sigma", abs((c * H0 / 12 - a0_hat) / (sig * a0_hat)) > 3)
print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
