#!/usr/bin/env python3
"""NPJ1 reported item R6 (lead's request after the result; REPORTED, not graded; criteria unchanged).

Questions (ROOT note, origin d4f8ac1563): for NPJ1's best candidates,
  (Q1) is there a fixed point whose universal amplitude ratio would fix kappa (the 1/2) without a fit?
  (Q2) does the sector's normalization run through 8 pi G (then the record's sqrt(pi) wall binds)?
Reads npj1.json (the graded fits); writes npj1_r6.out / npj1_r6.json. Natural units hbar = c = 1.
Any horizon-set mass below is an ASSUMPTION, labelled where used. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "npj1.json")))
OUT, LINES = {}, []


def say(*a):
    s = " ".join(str(v) for v in a)
    LINES.append(s)
    print(s, flush=True)


say("NPJ1 R6 (reported, not graded): fixed point, kappa, and 8 pi G")

# ---------------------------------------------------------------- c3 / b2: the A-native leaf pair
G, rho, K, nu, N, gB, mb0, cst, zeta, H = sp.symbols("G rho K nu N g_B m_b0 c_star zeta H", positive=True)
# (a) the amplitude tuning B = 1 (alpha = 2 at A = 0): B = K nu N g_B^2 m_b0/(4 pi), K = 4 pi G
tune = sp.solve(sp.Eq((K * nu * N * gB**2 * mb0 / (4 * sp.pi)).subs(K, 4 * sp.pi * G), 1), nu)[0]
say(f"(a) leaf pair, amplitude tuning B = 1 with K = 4 pi G: nu = {tune}, i.e. nu N g_B^2 m_b0 = 1/G "
    f"= M_Pl^2: the sector's normalization is fixed against GR's gradient term, i.e. by G.")
# (b) the crossover: s = g_B A/m_b0 = c_star x  ->  a0 = c_star m_b0/g_B; kappa = a0/sqrt(G rho_DE)
a0 = cst * mb0 / gB
kap_gen = sp.simplify(a0 / sp.sqrt(G * rho))
say(f"(b) kappa = a0/sqrt(G rho_DE) = {kap_gen}: needs m_b0 in units of sqrt(G rho_DE); m_b0 is a relevant coupling "
    f"(dimension 2 for m_b0^2), not a fixed-point number.")
# (c) ASSUMPTION: the horizon is the infrared cutoff, m_b0 = zeta H with H^2 = 8 pi G rho_DE/3
kap_h = sp.simplify(kap_gen.subs(mb0, zeta * sp.sqrt(8 * sp.pi * G * rho / 3)))
kap_over_sqrtpi = sp.simplify(kap_h / sp.sqrt(sp.pi))
say(f"(c) ASSUMPTION m_b0 = zeta H: kappa = {kap_h}; kappa/sqrt(pi) = {kap_over_sqrtpi} (no pi left): kappa carries "
    f"sqrt(pi) from 8 pi G unless g_B does.")
c_star = {f: 10 ** D["fits"][f]["c3 holographic leaf pair (G3 fields)"]["params"][2] for f in ("canonical", "alt")}
ZETAS = {"sqrt2 (4-d conformal coupling in dS: m^2 = R/6 = 2 H^2)": math.sqrt(2),
         "sqrt3/2 (3-d conformal coupling on a leaf S^3 of radius 1/H: m^2 = R_3/8 = 3 H^2/4)": math.sqrt(3) / 2}
R6 = {"tuning_nu": str(tune), "kappa_general": str(kap_gen), "kappa_horizon": str(kap_h),
      "kappa_over_sqrtpi": str(kap_over_sqrtpi), "rows": {}}
for f in ("canonical", "alt"):
    cg_loc = D["C_loc_A_gapped"][f]["c_g_needed"]             # g_F needed for locality (C-loc)
    for zn, zv in ZETAS.items():
        kfun = lambda g: c_star[f] * zv * math.sqrt(8 * math.pi / 3) / g
        g_half = c_star[f] * zv * math.sqrt(8 * math.pi / 3) / 0.5
        k_loc = kfun(2 * cg_loc)                              # g_B = 2 g_F at the locality bound
        R6["rows"][f"{f} | {zn}"] = {"c_star": c_star[f], "g_B_for_kappa_half": g_half,
                                     "kappa_at_locality_g_B": k_loc}
        say(f"   [{f}] zeta = {zn}: c_star = {c_star[f]:.4f}; kappa = 1/2 needs g_B = {g_half:.3f} (a choice, "
            f"not a fixed-point value: g_B is a marginal source coupling); at the locality bound g_B = 2 x "
            f"{cg_loc:.3e}: kappa = {k_loc:.2e}")

# (d) the fixed point actually reached at A -> 0: the free Cl(6) fermion; the interacting large-N O(N) point not selected
say(f"(d) fixed point at A -> 0 in c3/b2: the free massless Cl(6) leaf fermion (Gaussian). Its universal number is the "
    f"|A|^3 coefficient of V, 8/(12 pi) g_F^3 = {8/(12*math.pi):.6f} g_F^3 per leaf and flavor; the amplitude needed "
    f"is set by nu N (the tuning above), not by it.")
XG = np.logspace(-2, 2, 41)
MU = XG / (1 + XG)


def mhat(s, lh):
    r_ = 1 + lh + s * s
    return 2 * r_ / (lh + np.sqrt(lh * lh + 4 * r_))


# strong coupling, exact: completing the square in mhat^2 + l mhat = 1 + l + s^2 gives
#   mhat - s = -l/2 + (1 + l/2) [sqrt(1 + s'^2) - s'],  s' = s/(1 + l/2),
# so the large-N O(N) boson gives exactly G3's shape at every coupling l = lambda/(8 pi m_b0); the constant goes into
# alpha_t, the factor (1 + l/2) into B, and the crossover moves from m_b0 to m_b0 (1 + l/2) = m_b0 + lambda/(16 pi).
l_, s_ = sp.symbols("l s", positive=True)
mh = -l_ / 2 + sp.sqrt((1 + l_ / 2)**2 + s_**2)
root_ok = sp.simplify(mh**2 + l_ * mh - (1 + l_ + s_**2)) == 0
sp_ = s_ / (1 + l_ / 2)
ident_ok = sp.simplify((mh - s_) - (-l_ / 2 + (1 + l_ / 2) * (sp.sqrt(1 + sp_**2) - sp_))) == 0
say(f"   strong coupling (sympy, exact): mhat = -l/2 + sqrt((1 + l/2)^2 + s^2) solves the gap equation: {root_ok}; "
    f"mhat - s = -l/2 + (1 + l/2)[sqrt(1 + s'^2) - s'], s' = s/(1 + l/2): {ident_ok}. Same shape as the free pair at "
    f"every coupling; crossover scale m_b0 + lambda/(16 pi), i.e. lambda/(16 pi) at the critical point m_b0 -> 0.")
pc3 = D["fits"]["canonical"]["c3 holographic leaf pair (G3 fields)"]["params"]     # alpha_t, B, log10 c
mu_c3 = 1 - pc3[0] / 2 - pc3[1] * (np.sqrt(1 + (10 ** pc3[2] * XG)**2) - 10 ** pc3[2] * XG)
R6["b2_exact_identity"] = {"root_ok": bool(root_ok), "identity_ok": bool(ident_ok), "mapped": {}}
for lh in (1e-4, 1.0, 1e2, 1e3, 1e5):
    Bm = pc3[1] / (1 + lh / 2)                       # B (1 + l/2) = B_G3
    am = pc3[0] + Bm * lh                            # alpha_t/2 shifted by B l/2
    cm = 10 ** pc3[2] * (1 + lh / 2)                 # s' = s/(1 + l/2) = c_G3 x
    mu_m = 1 - am / 2 - Bm * (mhat(cm * XG, lh) - cm * XG)
    dev = float(np.max(np.abs(mu_m - mu_c3)))
    band = float(np.max(np.abs(mu_m - MU)))
    R6["b2_exact_identity"]["mapped"][str(lh)] = {"B": Bm, "alpha_t": am, "c": cm, "max_diff_to_c3": dev,
                                                  "max_dmu": band}
    say(f"   lambda_hat = {lh:g}: mapped (alpha_t {am:.4f}, B {Bm:.3e}, c {cm:.3e}) reproduces c3's mu to {dev:.1e}; "
        f"max dmu {band:.4f}")

# ---------------------------------------------------------------- a1 BK
al, Lam, MP, cbk, rh = sp.symbols("alpha Lambda M_Pl c_BK rho_DE", positive=True)
a0_bk = al**3 * Lam**2 / (8 * sp.pi * MP * cbk)              # law's crossover a0 = a0'/c_BK
kap_bk = sp.simplify(a0_bk / sp.sqrt(rh / MP**2))            # sqrt(G rho), G = 1/M_Pl^2
kap_bk_tied = sp.simplify(kap_bk.subs(Lam, rh**sp.Rational(1, 4)))
c_bk = {f: 10 ** D["fits"][f]["a1 BK superfluid"]["params"][0] for f in ("canonical", "alt")}
a_half = {f: float(sp.solve(sp.Eq(kap_bk_tied.subs(cbk, c_bk[f]), sp.Rational(1, 2)), al)[0]) for f in c_bk}
say(f"(e) a1 BK: kappa = {kap_bk} (alpha, Lambda free); ASSUMPTION Lambda^4 = rho_DE: kappa = {kap_bk_tied}; kappa = 1/2 "
    f"needs alpha = {a_half['canonical']:.4f} (c_BK = {c_bk['canonical']:.4f}; alt identical). alpha is a coupling, "
    f"not a fixed-point number; P proportional to X|X|^(1/2) is a three-body equation of state, not a fixed point. "
    f"Its normalization runs through 1/M_Pl (the baryon coupling alpha Lambda/M_Pl), i.e. G.")
R6["a1"] = {"kappa": str(kap_bk), "kappa_Lambda4_eq_rho": str(kap_bk_tied), "alpha_for_half": a_half, "c_BK": c_bk}

say("\nANSWERS (reported):")
say(" Q1: no. The leaf pair's A -> 0 fixed point is the free fermion; kappa = c_star m_b0/(g_B sqrt(G rho_DE)) needs a "
    "relevant mass and a marginal coupling, neither fixed by the fixed point. Even with the horizon as the infrared cutoff "
    "(assumed m_b0 = zeta H), kappa = c_star zeta sqrt(8 pi/3)/g_B: the fitted 1/2 becomes a fitted g_B (about 6.5 "
    "or 4.0 for the two zetas). Locality needs g_B >= 6.6e6, which gives kappa about 5e-7. The interacting "
    "large-N O(N) boson gives exactly the same shape at every coupling (an identity); at its critical point the crossover "
    "is lambda/(16 pi g_B), set by the dimensionful lambda. BK: kappa needs "
    "a chosen alpha (about 1.7 if Lambda^4 = rho_DE).")
say(" Q2: yes. The leaf pair is normalized against GR's gradient term (nu N g_B^2 m_b0 = 1/G), and a horizon-set "
    "crossover brings sqrt(8 pi/3): kappa/sqrt(pi) is free of pi, so the sqrt(pi) wall binds unless g_B carries "
    "1/sqrt(pi). BK's normalization runs through 1/M_Pl.")
OUT["R6"] = R6
with open(os.path.join(HERE, "npj1_r6.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "npj1_r6.out"), "w") as fh:
    fh.write("\n".join(LINES) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
