#!/usr/bin/env python3
"""N5 -- Torres-Gomez & Krasnov (arXiv:0911.3793) coupling relation, and the per-construction verdict table with lane D's bar applied.
TGK, AS PRINTED (eqs (199)-(203), read; the 57-page body is NOT read): L_YM = -(2/kappa)(F_munu)^2 => g_YM^2 = kappa/8 in their units; physical g_YM^2 = 4 pi G kappa (203),
with kappa a first derivative of the defining potential function of the theory (their (152), not read) and Lambda set to zero in their scheme.  => FREE (kappa = alpha/G would give alpha).
VERDICT TABLE (classes: TIED / FREE / MIXED / ABSENT-UNDEFINED), numbers from n1-n4 (re-derived here where cheap):
  C1 plain MacDowell-Mansouri SO(4,1) [lane M m3; Krasnov-Percacci (34)]: no gauge field; the only dimensionless coefficient is 3/(64 pi G Lambda): TIED to G Lambda (1e121)
  C2 MM-type extension to spin(1+N,3), constant compensator [n1]: ABSENT (kinetic coefficient identically 0; only the topological X=1 term)
  C3 Lisi-Smolin-Speziale spin(11,3) [n2]: TIED: alpha_G = (4/3) G Lambda; Riemann^2 coefficient = 1/(4 g_G^2); scale g free = G Lambda locked to the observed Lambda
  C4 Smolin extended Plebanski [n3]: MIXED with a free real: g_YM^2 = G_N Lambda h(gamma), h non-constant
  C5 Nesti-Percacci graviweak 0706.3307 [n4]: FREE (rank 3); forced 1:1:1 ratio of curvature-squared coefficients, overall 1/g2^2 free
  C6 Nesti-Percacci 0909.4537 SO(3,11) chirality: UNDEFINED (no bosonic action)  [source reading]
  C7 Torres-Gomez-Krasnov: FREE (g^2 = 4 pi G kappa)
LANE D BAR (declared there): (i) P_lookelsewhere < 1e-3, (ii) |miss| <= 5e-10 (or stated predicted precision), (iii) zero fitted reals, (iv) scale stated.
Row values computed here: predicted alpha at observed inputs (if the construction predicts one), miss relative to alpha_Thomson, number of fitted reals needed to reach alpha.
Run:    python3 n5_tgk_and_bar_summary.py           (exit 0)
MUTATE: python3 n5_tgk_and_bar_summary.py MUTATE   (declares the LSS value to sit at the required alpha; the internal-consistency check against the derived (4/3) x must FAIL -> exit 1)
"""
import sys
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok:
        fails.append(n)

mp.mp.dps = 30
Om, H0 = mp.mpf('0.6847'), mp.mpf('67.4') * 1000 / mp.mpf('3.0856775814913673e22')
cc, Gn_, hb = mp.mpf('299792458'), mp.mpf('6.67430e-11'), mp.mpf('1.054571817e-34')
x_obs = (3 * Om * H0**2 / cc**2) * (Gn_ * hb / cc**3)
aT = 1 / mp.mpf('137.035999177')

# --- TGK
G, kap = sp.symbols('G kappa', positive=True)
g2 = 4 * sp.pi * G * kap
chk("TGK: g_YM^2 = 4 pi G kappa; d g^2/d kappa != 0 and no Lambda anywhere -> kappa (a potential parameter) sets the coupling",
    sp.diff(g2, kap) != 0 and not g2.has(sp.Symbol('Lambda')))
print("   TGK: alpha = G kappa => kappa = alpha M_Pl^2 = %.6f M_Pl^2 would give alpha = 1/137.036 (kappa 'of order M_Pl^2' is their stated naturalness, no value derived)" % aT)

# --- LSS value
alpha_LSS = mp.mpf(4) / 3 * x_obs
claimed = aT if MUT else alpha_LSS
chk("LSS: the claimed value equals the derived (4/3) G Lambda at the observed inputs (%.3e)" % alpha_LSS,
    abs(claimed / alpha_LSS - 1) < mp.mpf('1e-9'), "claimed = %.3e" % claimed)
miss = abs(alpha_LSS / aT - 1)
decades = -mp.log10(alpha_LSS / aT)
print("   LSS: alpha_G(obs) = %.3e ; relative miss vs 1/137.036 = %.6f ; %.1f decades below alpha" % (alpha_LSS, miss, decades))

rows = [
    # name, class, fitted reals needed, predicted alpha or None, note
    ("C1 plain MacDowell-Mansouri", "TIED (to G Lambda)", 0, mp.mpf(16) / 3 * x_obs, "no gauge field; coefficient 3/(64 pi G Lambda); alpha_MM = (16/3) x / kN (lane M m3), kN = 1 shown"),
    ("C2 MM-type extension, constant X", "ABSENT", None, None, "spin(N) kinetic coefficient identically 0 (n1)"),
    ("C3 Lisi-Smolin-Speziale spin(11,3)", "TIED (ratio 4/3; scale g = G Lambda)", 0, alpha_LSS, "classical-vacuum scale; overall = observed Lambda"),
    ("C4 Smolin extended Plebanski", "MIXED (free gamma)", 1, None, "h(gamma) non-constant; printed chain: gamma to ~1e-59 near a pole, wrong sign; re-derived chains: bounded, alpha < ~1e-124"),
    ("C5 Nesti-Percacci graviweak", "FREE (+ forced 1:1:1 R^2:W^2:K^2)", 1, None, "g2 free; rank 3"),
    ("C6 Nesti-Percacci SO(3,11) chirality", "UNDEFINED", None, None, "no bosonic action (source reading)"),
    ("C7 Torres-Gomez & Krasnov", "FREE", 1, None, "kappa = alpha M_Pl^2 needed"),
]
print("%-38s %-38s %-7s %-10s %s" % ("construction", "class", "fitted", "alpha(obs)", "bar"))
ok_all_fail = True
for name, cls, fit, apred, note in rows:
    if apred is not None:
        m = abs(apred / aT - 1)
        passes = (m <= mp.mpf('5e-10')) and fit == 0
        why = "miss %.4f > 5e-10" % m
    else:
        passes = False
        why = "no value predicted" if fit is None else "needs %d fitted real(s)" % fit
    ok_all_fail &= (not passes)
    print("%-38s %-38s %-7s %-10s %s | %s" % (name, cls, "-" if fit is None else fit, ("%.2e" % apred) if apred is not None else "-",
                                              "PASS" if passes else "fail (" + why + ")", note))
chk("no construction clears lane D's bar", ok_all_fail)
chk("the only construction with zero fitted reals and a definite value (C3) misses by more than 100 decades", decades > 100)
print("READING: the branch produces forced RATIOS only (LSS: alpha_G/(G Lambda) = 4/3 and Riemann^2 coefficient : gauge coefficient = 1 : 4 in the normalisation of n2; graviweak: R^2 : W^2 : K^2 = 1 : 1 : 1;")
print("MM-type: none).  The overall scale is a free coefficient of the action (g, g2, kappa, gamma) or is locked to G Lambda ~ 3e-122 (LSS classical vacuum).  No forced principle fixes a gauge coupling.")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
