#!/usr/bin/env python3
"""
ADVERSARIAL VERIFIER script 3 -- the "saturation gives precisely mu(a/a0)" claim, taken
BEYOND the gauntlet's asymptotic argument to a DATA-GRADE test (the gauntlet's kill was
exponents-only; a critic could say "SPARC never reaches g->0, maybe it fits in-window").

X1  Target identities re-verified: m_eff/m = sqrt(g/(g+a0)) == the mu_fw form
    (mu(x)=(sqrt(1+4x^2)-1)/(2x), x=g_obs/a0, g_obs=sqrt(g^2+g a0)); deep-MOND exponent 1/2;
    Newtonian tail -a0/(2g).
X2  STRUCTURAL theorem: EVERY intensity-saturation family 1 - c/(1+(g/gs)^2)^q (any q>0)
    has deep-MOND exponent 2 (with c=1) or a floor (c<1). The target's 1/2 is unreachable:
    the failure is structural, not parametric.
X3  DATA-GRADE fit: best 2-parameter (c, gs) homogeneous and inhomogeneous saturation vs the
    target over the OBSERVED SPARC window g_bar in [1e-12, 1e-8] m/s^2 (Lelli+ 2017):
    max |Delta log10 g_obs| (identically |Delta log10 mu| at fixed g_bar) reported against
    the RAR total scatter 0.11 dex and intrinsic <= 0.057 dex.
X4  The floor escape (c<1 fits better in-window by faking the low end) PREDICTS mu -> 1-c:
    at dSph accelerations (g ~ 1e-13, McGaugh-Wolf) it overshoots the target mu by >~0.3 dex
    => killed by the deepest-MOND objects. And c=1-exact versions fail in-window outright.
X5  Required saturation variable s_req = mu_T/(1-mu_T): ~sqrt(g/a0) at low g, ~2g/a0 at high g
    (sqrt-to-linear in amplitude; physical saturation is quadratic/intensity).
X6  Scale: even the best fits need c*gs ~ a0/2 with gs an I_sat-type medium constant:
    a0 = cH_L/Z is INSERTED, not delivered (no assertion possible -- bookkeeping statement).
Exit 0 = all assertions hold.
"""
import numpy as np
import sympy as sp

ok = []

# --- X1 target identities (sympy, independent forms)
g, a0s, gss, cs, q = sp.symbols('g a0 gs c q', positive=True)
target = sp.sqrt(g/(g + a0s))
g_obs = sp.sqrt(g**2 + g*a0s)
x = g_obs/a0s
mu_fw = (sp.sqrt(1 + 4*x**2) - 1)/(2*x)
for gv, av in [(3.0, 7.0), (0.01, 1.0), (250.0, 1.0)]:
    lhs = float(mu_fw.subs({g: gv, a0s: av}))
    rhs = float((g/g_obs).subs({g: gv, a0s: av}))
    tgt = float(target.subs({g: gv, a0s: av}))
    assert abs(lhs - rhs) < 1e-12 and abs(lhs - tgt) < 1e-12
assert sp.limit(target/sp.sqrt(g/a0s), g, 0, '+') == 1                 # deep exponent 1/2
assert sp.simplify(sp.series(target, a0s, 0, 2).removeO() - 1 + a0s/(2*g)) == 0  # tail -a0/(2g)
ok.append("X1: m_eff/m = sqrt(g/(g+a0)) == mu_fw(g_obs/a0) verified; deep-MOND exponent 1/2; "
          "Newtonian tail -a0/(2g)")

# --- X2 structural theorem: intensity saturation always gives deep exponent 2 (c=1)
X = (g/gss)**2
for qv in [sp.Rational(1, 2), 1, 2, 3]:
    fam = 1 - (1 + X)**(-qv)
    lead = sp.limit(fam/X, g, 0, '+')
    assert sp.simplify(lead - qv) == 0                                  # fam ~ q*(g/gs)^2
ok.append("X2: 1-(1+(g/gs)^2)^(-q) ~ q (g/gs)^2 as g->0 for EVERY q: deep-MOND exponent 2, "
          "never 1/2 -- structural failure of all intensity-saturation shapes (c=1); c<1 => floor")

# --- X3 data-grade fit over the observed SPARC window
a0 = 9.3624e-11
gw = np.logspace(-12, -8, 240)                                          # observed window (SI)
mu_T = np.sqrt(gw/(gw + a0))
def maxdev(mu_model):
    m = np.where(mu_model > 1e-12, mu_model, 1e-12)
    return np.max(np.abs(np.log10(m) - np.log10(mu_T)))
gs_grid = np.logspace(-13.5, -8.5, 320)
c_grid = np.linspace(0.50, 1.00, 201)
best = {}
for name, form in [("hom", lambda c_, s_: 1 - c_/(1 + s_)),
                   ("inh", lambda c_, s_: 1 - c_/np.sqrt(1 + s_))]:
    e_free, arg_free, e_c1 = np.inf, None, np.inf
    for gs in gs_grid:
        s = (gw/gs)**2
        for c_ in c_grid:
            e = maxdev(form(c_, s))
            if e < e_free:
                e_free, arg_free = e, (c_, gs)
            if c_ == 1.0 and e < e_c1:
                e_c1 = e
    best[name] = (e_free, arg_free, e_c1)
(eh, argh, eh1), (ei, argi, ei1) = best["hom"], best["inh"]
print(f"  [X3] hom  best free-(c,gs): max|dlog g_obs| = {eh:.3f} dex at c={argh[0]:.3f}, "
      f"gs={argh[1]:.2e} ({argh[1]/a0:.3f} a0); c=1-exact best = {eh1:.3f} dex")
print(f"  [X3] inh  best free-(c,gs): max|dlog g_obs| = {ei:.3f} dex at c={argi[0]:.3f}, "
      f"gs={argi[1]:.2e} ({argi[1]/a0:.3f} a0); c=1-exact best = {ei1:.3f} dex")
assert eh > 0.057 and ei > 0.057                       # both exceed the RAR INTRINSIC budget
assert eh1 > 0.30 and ei1 > 0.30                       # c=1-exact versions fail outright
ok.append(f"X3: best physical-saturation fits over the OBSERVED window: homogeneous "
          f"{eh:.3f} dex (c=1: {eh1:.3f}), inhomogeneous {ei:.3f} dex (c=1: {ei1:.3f}) "
          f"max systematic vs RAR intrinsic scatter 0.057 dex / total 0.11 dex: the mu shape "
          "is NOT reproduced at data grade even inside the window")

# --- X4 the floor escape dies at dSph depth
g_dsph = 1e-13
for name, form in [("hom", lambda c_, s_: 1 - c_/(1 + s_)),
                   ("inh", lambda c_, s_: 1 - c_/np.sqrt(1 + s_))]:
    c_, gs = best[name][1]
    mu_m = form(c_, (g_dsph/gs)**2)
    mu_t = np.sqrt(g_dsph/(g_dsph + a0))
    dev = abs(np.log10(mu_m) - np.log10(mu_t))
    print(f"  [X4] {name} best-fit extended to dSph g=1e-13: mu_model={mu_m:.4f} vs "
          f"mu_target={mu_t:.4f} -> {dev:.2f} dex")
    assert dev > 0.25, (name, dev)
ok.append("X4: the in-window best fits (floors 1-c) overshoot the deep-MOND target at dSph "
          "accelerations by >0.25 dex (g_obs underpredicted ~2x): killed by the deepest-MOND "
          "objects (McGaugh-Wolf dSphs); and reaching m_eff->0 at all needs c=1 EXACT, which "
          "X3 shows fails in-window by >0.30 dex")

# --- X5 required saturation variable
s_req = sp.simplify(target/(1 - target))
assert sp.limit(s_req/sp.sqrt(g/a0s), g, 0, '+') == 1                   # ~ sqrt(g/a0)
assert sp.simplify(sp.limit(s_req/g, g, sp.oo) - 2/a0s) == 0            # ~ 2g/a0
ok.append("X5: s_req(g) = mu_T/(1-mu_T) ~ sqrt(g/a0) (g->0), ~ 2g/a0 (g->inf): sqrt-to-linear "
          "in amplitude where physical saturation is quadratic (intensity): the mu shape must "
          "be inserted by hand")

ok.append("X6: even the best fits sit at c*gs ~ a0/2 with gs an I_sat-derived medium constant "
          "(pump rate, linewidth, dipole): nothing delivers a0 = cH_L/Z; the scale is set, "
          "not derived")

print("ALL ASSERTIONS PASSED (verifier 3: saturation-shape kill upgraded to data grade)")
for line in ok:
    print(" *", line)
