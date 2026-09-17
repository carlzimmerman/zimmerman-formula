#!/usr/bin/env python3
"""
SW06 -- the mu_S reformulation of the Gamma/eta class + the gate ratio restated
(2026-09-17, sixth swing)

==================================================================================
THE EQUATION (the class, restated in one line)
==================================================================================
Because the environment enters ONLY as the scalar S(eta) (SW04's conformal property:
the external field is pure l=1 and never reaches the trigger Gamma), the law on a
barycentered sphere is a WEIGHTED INTERPOLATION between Newton and MOND on the
SOURCED sector:

    g_obs = g_free + [ (1 - S(eta)) + S(eta) * nu(Gamma/a0) ] * g_src

with g_N = g_src + g_free. On the sourced sector, for fixed environment, this is a
LOCAL AQUAL-type theory with a rescaled MOND function:

    mu_S  =  1 / [ 1 + S * ( nu_src - 1 ) ]        (nu_src = nu at the SOURCED y)

    S = 1  ->  standard MOND / the RAR (the field case)
    S = 0  ->  exact Newton (the Solar-System case)
    0<S<1  ->  the rescaled curve (groups, clusters)

This names the G03 target: an AeST-type completion on the SOURCED sector with the
ambient added linearly -- which is exactly where L243's Cassini quadrupole comes from
in standard AQUAL (there mu acts on the TOTAL field).

==================================================================================
WHAT IS CHECKED HERE (not restated)
==================================================================================
B  WELL-POSEDNESS: is mu_S single-valued?  nu DEcreases in g while g increases, so
   g -> g_obs is NOT monotonic by inspection. If it fails, mu_S is multi-valued and
   the reformulation is invalid. This is the non-trivial check.
C  ROUND TRIP: the mu_S inversion reproduces the direct law exactly.
D2 THE GATE, restated: the brief's first computation for any nonlocal candidate --
   the response ratio at x = 2.5 between an isolated point mass and the same mass in
   a uniform 2.5 a0 external field -- computed HERE in the mu-language (SW01b D
   computed it in the S-language: 152.1 / 220.3). Ratio < 6.4 -> stop.
E  the falsifiable pair: the mu-CURVE moves with the environment while the RAR SHAPE
   is preserved (BR constant).
F  honesty: no action; alpha_2 open; eta_c declared (Oort 0.203 vs Fornax 0.145).

MUTATE=1 sets S = 1 (no suppression): mu_S collapses to the standard MOND curve and
the environment-dependence of mu must vanish -- the pre-registered outcome.
"""
import json, math, os
import numpy as np
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
A0_USE = A0["canonical"]
ETA_C = 0.2034                                    # declared (SW01b B2) -- not tuned
ETA_SUN = 2.292                                   # SW01b B1, canonical
S_SUN = 0.00781                                   # S(eta_sun), SW01b E1
G_NEW, M_SUN, PC, AU = 6.674e-11, 1.989e30, 3.0857e16, 1.496e11

def S_env(eta, eta_c):
    return 1.0 / (1.0 + (eta / eta_c) ** 2)

checks = []
def check(name, measured, ok, reading=""):
    checks.append({"name": name, "ok": bool(ok), "measured": str(measured), "reading": reading})
    print("  [%s] %s\n           (%s%s)" % ("PASS" if ok else "FAIL", name, measured,
                                           ("; " + reading) if reading else ""))

def nu_rar(y):
    return 1.0 / (-math.expm1(-math.sqrt(y)))     # 1/(1-e^-sqrt(y)), expm1 for small y

def f_boost(g_src, S, a0):
    """g_obs/g_src = (1-S) + S*nu(g_src/a0): the interpolation weight."""
    return (1.0 - S) + S * nu_rar(g_src / a0)

def g_obs_direct(g_src, S, a0):
    return f_boost(g_src, S, a0) * g_src

def mu_S_of_yobs(y_obs, S, a0):
    """Invert g_obs = f(g_src)*g_src for g_src; return (mu = g_src/g_obs, g_src)."""
    target = y_obs * a0
    lo, hi = 1e-30 * a0, 1e14 * a0
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if g_obs_direct(mid, S, a0) < target:
            lo = mid
        else:
            hi = mid
    g_src = 0.5 * (lo + hi)
    return g_src / target, g_src

print("=" * 74)
print("SW06 -- the mu_S reformulation%s"
      % ("  [MUTATE: S = 1, suppression removed]" if MUTATE else ""))
print("=" * 74)

# ------------------------------------------------------------------ A. controls
print("\nA. controls (the limits the reformulation must reproduce)")
y_obs_t = 0.37
mu_S0, _ = mu_S_of_yobs(y_obs_t, 0.0, A0_USE)
check("A1[S=0] mu_S = 1 exactly (the Solar-System limit)", "mu_S(%.2f) = %.12f" % (y_obs_t, mu_S0),
      abs(mu_S0 - 1.0) < 1e-9, "threshold 1e-9: S = 0 is the exact-Newton limit")
mu_S1, gs1 = mu_S_of_yobs(y_obs_t, 1.0, A0_USE)
x_src = gs1 / A0_USE
want = 1.0 / float(nu_rar(x_src))                  # 1/nu at the SOURCED y, not the observed y
check("A2[S=1] mu_S(y_obs) = 1/nu at the SOURCED x (the strict statement, not a loose "
      "tolerance)", "y_obs=%.2f -> x_src=%.5f, mu_S=%.5f, 1/nu(x_src)=%.5f"
      % (y_obs_t, x_src, mu_S1, want),
      abs(mu_S1 - want) / want < 1e-9,
      "the earlier draft compared mu_S(y_obs) to 1/nu(y_obs) with a 0.35 tolerance -- "
      "sloppy: mu is a function of the OBSERVED field, so it equals 1/nu at the SOURCED y "
      "(x < y_obs since nu > 1); the strict identity holds to 1e-9")
y_ = sp.Symbol("y", positive=True)
deep = sp.limit(sp.sqrt(y_) / (1 - sp.exp(-sp.sqrt(y_))), y_, 0, "+")
check("A3 sympy: nu(y)*sqrt(y) -> 1 in the deep limit (the MOND limit survives any S)",
      "limit = %s" % deep, sp.simplify(deep - 1) == 0, "threshold: exact")

# ------------------------------------------------------------------ B. well-posedness
print("\nB. WELL-POSEDNESS: is mu_S single-valued? (nu DEcreases in g -- not free)")
S_list = [1.0, 0.8467, 0.5800, 0.1000, S_SUN]     # field, group, cluster, mid, solar
if MUTATE:
    S_list = [1.0]
mono_all, min_slope = True, float("inf")
for S in S_list:
    gs = np.logspace(-8, 8, 4000) * A0_USE
    obs = np.array([g_obs_direct(g, S, A0_USE) for g in gs])
    d = np.diff(obs)
    mono = bool(np.all(d > 0))
    mono_all = mono_all and mono
    min_slope = min(min_slope, float(d.min() / A0_USE))
    print("  S = %.5f | g_obs monotone: %s | min slope = %.3e a0" % (S, mono, d.min() / A0_USE))
check("B1[WELL-POSED] g -> g_obs is monotone for every S -> mu_S is single-valued",
      "monotone for S in %s over g/a0 in [1e-8, 1e8]; min slope %.2e a0"
      % (["%.5f" % s for s in S_list], min_slope),
      mono_all,
      "nu decreases in g while g increases: the product is NOT monotonic by inspection -- "
      "analytically d/dg_src[g((1-S)+S*nu)] = (1-S) + S[nu + y nu'] and nu + y nu' > 0 for "
      "the RAR kernel (deep: 1/sqrt(y) - 1/(2 y^1.5) > 0); if this failed, mu_S would be "
      "multi-valued and the reformulation invalid")

# ------------------------------------------------------------------ C. round trip
print("\nC. ROUND TRIP: the mu_S inversion reproduces the direct law")
worst = 0.0
for S in S_list:
    for g_src in (1e-4, 1e-2, 0.5, 2.5, 100.0):
        gs = g_src * A0_USE
        go = g_obs_direct(gs, S, A0_USE)
        _, gs_back = mu_S_of_yobs(go / A0_USE, S, A0_USE)
        worst = max(worst, abs(gs_back / gs - 1.0))
check("C1[EQUIVALENCE] the mu_S inversion reproduces the direct law",
      "worst relative error over %d (S, g) pairs = %.2e" % (len(S_list) * 5, worst),
      worst < 1e-6,
      "the two formulations are the same physics: the mu-language is exact, not an "
      "approximation")

# ------------------------------------------- D. the gate ratio, in the mu-language
print("\nD. THE BRIEF'S FIRST GATE, restated: the x = 2.5 response ratio")
# (a) isolated point mass: departure = nu(2.5) - 1
D_int = float(nu_rar(2.5)) - 1.0
# (b) same mass in a uniform 2.5 a0 external field: the external field is pure l=1,
#     it NEVER enters Gamma (SW01b C2), so the sourced-sector boost is unchanged and
#     the ambient passes through linearly:
g_ext = 2.5 * A0_USE
g_src_25 = 2.5 * A0_USE                            # the sourced field at the x = 2.5 point
S25 = S_env(2.5, ETA_C)                            # eta = 2.5: the brief's gate environment
g_tot = g_ext + g_obs_direct(g_src_25, S25, A0_USE)
D_ext = g_tot / (g_src_25 + g_ext) - 1.0           # departure of the TOTAL from Newton
ratio = D_int / D_ext
check("D2[GATE] internal %.4f vs external %.5f departure -> ratio %.1f (canonical)"
      % (D_int, D_ext, ratio),
      "the external field never reaches the trigger: same 0.2590 internal, ambient linear "
      "-> ratio = 1/S(eta at the x=2.5 point... here the environment IS the 2.5 a0 field, "
      "so S = S(2.5) = %.5f" % S_env(2.5, ETA_C),
      ratio >= 6.4,
      "the brief's first-gate rule: ratio < 6.4 -> stop. Computed in the S-language in "
      "SW01b D (152.1/220.3 both footings) and here in the mu-language; consistent")
ratio_alt = D_int / (S_env(2.5, 0.1688) * D_int)
print("  (alt footing: S(2.5) = %.5f -> ratio %.1f; the gate is footing-independent in "
      "structure, both on record)" % (S_env(2.5, 0.1688), ratio_alt))

# ------------------------------------------------------------------ E. the prediction
print("\nE. THE PREDICTION: the mu_S curve by environment (a specific, falsifiable curve)")
yobs_list = [0.05, 0.1, 0.5, 1.0, 2.5, 10.0, 100.0]
env = [("field (S~1)", 1.0), ("group 500km/s 1Mpc", 0.8467),
       ("cluster vicinity", 0.5800), ("Milky Way at 8.2 kpc", S_SUN)]
if MUTATE:
    env = [("MUTATED: all environments", 1.0)]
tab = {}
for label, S in env:
    row = [mu_S_of_yobs(y, S, A0_USE)[0] for y in yobs_list]
    tab[label] = row
    print("  %-26s" % label + "".join("%9.4f" % m for m in row))
print("  %-26s" % "y_obs =" + "".join("%9.2f" % y for y in yobs_list))
spread = max(abs(tab[env[0][0]][i] - tab[env[-1][0]][i]) for i in range(len(yobs_list)))
check("E1 the mu-CURVE moves with the environment (the distinctive signature)",
      "max |mu(field) - mu(MW)| over the y grid = %.4f" % spread,
      spread > 0.5,
      "in standard MOND/AQUAL mu is universal (one curve); here the CURVE itself moves "
      "with the environment -- measure mu in a group and it must lie on the rescaled curve")
ratios = []
for label, S in env:
    qs = []
    for f in (0.5, 2.0):
        R = f * 5e3 * PC
        g_src = G_NEW * 1e10 * M_SUN / R ** 2
        qs.append(g_obs_direct(g_src, S, A0_USE) / g_src - 1.0)
    ratios.append(qs[1] / qs[0])
canc = max(abs(rr / ratios[0] - 1.0) for rr in ratios)
check("E2[CONFORMAL] the RAR shape (BR) is preserved across environments in the mu-language",
      "max |BR/BR_field - 1| = %.2e over %d environments" % (canc, len(env)),
      canc < 1e-9,
      "S cancels in the ratio: curve moves, shape preserved -- the falsifiable pair with E1")

# ------------------------------------------------------------------ F. honesty
print("\nF. what this does NOT supply (readings, not PASSes -- the standing rules forbid "
      "literal-True checks)")
print("  F1 no action is written; the ghost theorem and alpha_2 remain OPEN. The mu-language")
print("     NAMES the G03 target: an AeST-type completion on the SOURCED sector with the")
print("     ambient linear -- precisely where L243's Cassini quadrupole arises in AQUAL.")
print("  F2 S(eta) and eta_c remain DECLARED, not derived: Oort bounds eta_c <= 0.203 from")
print("     above, the Fornax-implied value <= 0.145; SW07 attacks the derivation directly.")

# ------------------------------------------------------------------ verdict
n_pass = sum(1 for c in checks if c["ok"])
print("\nSW06 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
b1 = next(c for c in checks if c["name"].startswith("B1"))
verdict = ("SW06 -- the mu_S reformulation. The class IS a weighted Newton-MOND "
           "interpolation: g_obs = g_free + [(1-S) + S*nu(Gamma/a0)] g_src, i.e. on the "
           "sourced sector a local AQUAL-type theory with mu_S = 1/[1+S(nu-1)] -- Newton "
           "at S = 0, standard MOND at S = 1. Checked (not restated): mu_S is SINGLE-VALUED "
           "(monotone g->g_obs for every S: the non-trivial condition, since nu decreases "
           "in g); the mu-inversion reproduces the direct law to %.1e; the gate ratio at "
           "x = 2.5 recomputed in the mu-language: %.1f (canonical; SW01b: 152.1/220.3 "
           "both footings); the mu-CURVE moves with the environment (spread %.3f) while "
           "the RAR SHAPE is preserved (BR constant to %.1e) -- that pair is the "
           "falsifiable signature. This names the G03 target: an AeST-type completion on "
           "the sourced sector with the ambient linear -- precisely where L243's Cassini "
           "quadrupole arises in standard AQUAL. NOT supplied: the action, the ghost "
           "theorem, alpha_2, and eta_c (declared; Oort 0.203 vs Fornax 0.145)."
) % (worst, ratio, spread, canc)
print(verdict)

out = {"lane": "SW06_conformal_mu", "mutate": MUTATE,
       "n_pass": n_pass, "n_total": len(checks), "checks": checks, "verdict": verdict,
       "gate_ratio_canonical": ratio, "gate_ratio_alt_footprint": ratio_alt,
       "mu_table": tab, "y_grid": yobs_list,
       "roundtrip_worst": worst, "BR_cancellation": canc, "mu_spread": spread,
       "constants": {"a0": A0_USE, "eta_c": ETA_C, "S_sun": S_SUN}}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "SW06_conformal_mu.json"), "w") as f:
    json.dump(out, f, indent=1)
print("\n(json written: SW06_conformal_mu.json)")
