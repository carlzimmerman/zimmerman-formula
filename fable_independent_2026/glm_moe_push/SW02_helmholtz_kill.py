#!/usr/bin/env python3
"""
SW02_helmholtz_kill.py -- the barycenter Gauss projector, pre-registered kill (2026-09-17)

THE CONSTRUCTION (attacked before code, per the loop's ATTACK step): drop SW01's declared
environmental suppression and keep only the structural idea -- a Helmholtz split on each
barycentered Gauss sphere,

    g_N = g_src + g_free,   div g_src = -4 pi G rho,   g_free = curl-free residual,

    g_obs = nu_RAR(|g_src|/a0) * g_src + g_free.

Isolated point mass: g_free = 0 -> exactly the RAR (the internal branch is untouched).
Pure uniform field: g_src = 0 -> exactly Newton, departure 0 (and the free piece is never
modified, so no anisotropy either).  The construction is therefore direction-blind for free
and has NO declared number -- the cleanest possible competitor to SW01-B.

PRE-REGISTERED KILL (stated BEFORE the computation, per the brief):
    if the SOURCED piece is left unsuppressed in the Galactic environment (eta_sun ~ 2), the
    solar phantom is uncapped: the deep two-body force g = sqrt(G M a0)/r applies to the
    Sun-neighbour pair at 1 pc, reproducing L263 C1's phantom -> rho_dark >= 128x the
    0.015 Msun/pc^3 budget -> KILLED.  A PASS would require rho_dark < 3x the budget on
    both a0 footings.  If it dies here, it is NOT fixed by re-inserting S(eta): that is
    SW01 again, and it is not written.

Correction record: the first run's verdict block recomputed rho_dark with the SOLAR r_M
(no sqrt(0.5) for the 0.5-Msun star) and printed 90.0x/99.1x, inconsistent with check A
(130.3x/143.1x).  The checks were right; the verdict constants were wrong.  Fixed by
storing the per-footing over-budget factors from check A itself.
"""
import json, math, os
import numpy as np
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
G_NEW, M_SUN, AU, PC = 6.674e-11, 1.989e30, 1.496e11, 3.0857e16
R_M_SUN_AU = {"canonical": 7960.0, "alt": 7252.0}     # solar r_M per footing (L263)
M_STAR = 0.5                                          # Msun, the L263 C1 configuration
N_STAR = 0.1                                          # pc^-3, stellar number density
R_CUT_PC = 1.08                                       # min(r_J, half-separation) from L263 C
OORT_BUDGET = 0.015                                   # Msun/pc^3
R_SATURN = 9.5 * AU

checks = []
def check(name, measured, ok, reading=""):
    checks.append({"name": name, "ok": bool(ok), "measured": str(measured), "reading": reading})
    print("  [%s] %s\n           (%s%s)" % ("PASS" if ok else "FAIL", name, measured,
                                           ("; " + reading) if reading else ""))

def nu_rar(y):
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))

print("=" * 72)
print("SW02 -- the barycenter Gauss projector (Helmholtz split, no suppression)%s"
      % ("  [MUTATE]" if MUTATE else ""))
print("=" * 72)
print("\nPRE-REGISTERED KILL: unsuppressed sourced piece in eta_sun ~ 2 environment")
print("-> uncapped solar phantom -> rho_dark >= 128x the 0.015 budget -> KILLED.")
print("   A PASS requires rho_dark < 3x the budget on BOTH footings. Stated before the numbers.\n")

# ---------------------------------------------------------------- A. the rule on the pair
print("A. the rule on the Sun-neighbour pair at the cut radius %.2f pc" % R_CUT_PC)
GM = G_NEW * M_STAR * M_SUN
r_cut = R_CUT_PC * PC
g_src = GM / r_cut ** 2
over_by_foot = {}
for f in ("canonical", "alt"):
    y = g_src / A0[f]
    nu = nu_rar(y)
    g_obs = nu * g_src
    M_dyn = g_obs * r_cut ** 2 / G_NEW
    M_ph = M_dyn / M_SUN - M_STAR
    rho = N_STAR * M_ph
    over = rho / OORT_BUDGET
    over_by_foot[f] = {"M_ph": M_ph, "rho": rho, "over": over}
    check("A[%s] M_ph(<%.2f pc) = %.2f Msun -> rho_dark = %.3f = %.1fx the budget"
          % (f, R_CUT_PC, M_ph, rho, over),
          "g_src = %.3e (y = %.2e), nu = %.2f; need < 3x" % (g_src, y, nu),
          over < 3.0,
          "the uncapped deep force sqrt(GMa0)/r: the L263 C1 phantom reproduced by the rule")

# ---------------------------------------------------------------- B. the other horn
print("\nB. the Cassini horn (for the record: which horn kills it)")
g_10au = GM / R_SATURN ** 2
y_10 = g_10au / A0["canonical"]
excess = nu_rar(y_10) - 1.0
check("B1 solar modification at 9.5 AU: nu(%.2e) - 1 = %.2e" % (y_10, excess),
      "the Helmholtz free piece is never modified: no quadrupole at any order",
      excess < 1e-100,
      "Cassini-safe -- the pincer horn this construction dies on is the OORT horn, not Cassini")
# sympy: the deep two-body force and the identity behind M_dyn = g r^2 / G
G_, M_, a0_, r_ = sp.symbols("G M a0 r", positive=True)
g_deep = sp.sqrt(G_ * M_ * a0_) / r_
rM_expr = sp.sqrt(G_ * M_ / a0_)
check("B2 sympy: the rule's deep force g = sqrt(GMa0)/r implies M_dyn = M r / r_M (L263 B1)",
      "M_dyn/M - r/r_M = %s" % sp.simplify((g_deep * r_ ** 2 / G_) / M_ - r_ / rM_expr),
      sp.simplify((g_deep * r_ ** 2 / G_) / M_ - r_ / rM_expr) == 0,
      "the phantom grows linearly in r with no environment term anywhere in the rule")

# ---------------------------------------------------------------- verdict
n_pass = sum(1 for c in checks if c["ok"])
print("\nSW02 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
verdict = ("SW02 (barycenter Gauss projector, no environmental suppression) -- KILLED as "
           "pre-registered: Oort %.1fx/%.1fx the budget (canonical/alt); Cassini-safe, so it "
           "dies on the OORT horn only.  Re-inserting S(eta) is SW01 again -- not written."
           % (over_by_foot["canonical"]["over"], over_by_foot["alt"]["over"]))
print(verdict)

out = {"lane": "SW02_helmholtz_kill", "mutate": MUTATE,
       "n_pass": n_pass, "n_total": len(checks), "checks": checks, "verdict": verdict,
       "constants": {"a0": A0,
                     "over_budget": {f: over_by_foot[f]["over"] for f in over_by_foot},
                     "rho_dark": {f: over_by_foot[f]["rho"] for f in over_by_foot}}}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "SW02_helmholtz_kill.json"), "w") as f:
    json.dump(out, f, indent=1)
print("\n(json written: SW02_helmholtz_kill.json)")
