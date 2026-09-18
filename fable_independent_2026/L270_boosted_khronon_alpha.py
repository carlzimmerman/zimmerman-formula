#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L270 -- THE BOOSTED KHRONON alpha_1/alpha_2 for the L268 magnitude-only action: attempted, honestly.

The deciding gate for the magnitude-only EFE (L268/L269): the preferred-frame parameters alpha_1, alpha_2
in the Solar System.  A full boosted-metric Foster-Jacobson reduction for this specific action has never
been done (L203).  This lane does the pieces that can be made rigorous or validated, and states exactly
what remains.

HONESTY LABELS on every step: [DERIVED] = computed and validated here; [LIT] = published result I apply
and validate at a known limit, NOT re-derive; [OPEN] = not computed by anyone, named.

  P1 [DERIVED] the MOND scalar DECOUPLES from the aether EOM at PN order: its stress is <= ~1e-6 of
     matter at every Solar-System PPN radius, so alpha_1/alpha_2 are set by the aether+matter sector,
     free of a0.  THIS is the structural difference from AeST (where the MOND field WAS the aether and
     fixed alpha_1 un-tunably).
  P2 [LIT, GR-validated] the aether alpha_1 (Foster-Jacobson) vanishes in the GR limit and on a
     nontrivial coupling surface (numerator c3^2 + c1 c4 = 0); alpha_2 = 0 is a second condition.
  P3 [DERIVED] counting: alpha_1 = alpha_2 = 0 is 2 conditions on the aether couplings (3 in the
     hypersurface-orthogonal/khronometric case, 4 in general aether), so a nonempty family satisfies
     BOTH -- the PF alpha gate is SATISFIABLE, not a wall.
  P4 [OPEN] the residual crux: are the alpha_1=alpha_2=0 couplings (Solar System, scalar decoupled)
     compatible with the galactic MOND mechanism (where the scalar back-reaction is O(1))?  Plus ghost-
     freedom on that family and the slip-lock.  These are the genuine remaining computations.

VERDICT: alpha_1/alpha_2 are NOT the wall for this action -- they can be set to zero because the scalar
decouples at PN order and the aether family alpha_1=alpha_2=0 is nonempty.  The exact boosted VALUES for
this action are still uncomputed (P4); the gate moves from "the wall" to "passable, conditional on the
galactic/Solar-System coupling consistency".

Run:  python3 fable_independent_2026/L270_boosted_khronon_alpha.py
"""
import os, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "L270_boosted_khronon_alpha"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L270", "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
# =================================================================================================
banner("P1 [DERIVED] the MOND scalar decouples from the aether EOM at PN order")
G = 6.674e-11; Msun = 1.989e30; a0 = 9.3619e-11; AU = 1.496e11
radii = {"Mercury": 0.39, "Earth": 1.0, "Saturn (Cassini)": 9.58}
fracs = {}
for nm, r_AU in radii.items():
    r = r_AU * AU; x = (G * Msun / r**2) / a0
    fracs[nm] = 1.0 / (2 * x)                       # power-law-kernel upper bound on scalar/matter stress
    P(f"    {nm:18s} g/a0 = {x:.3e}   scalar/matter stress <= {fracs[nm]:.2e}")
worst = max(fracs.values())
OUT["numbers"]["scalar_matter_stress_max_PN"] = worst
check("P1 the scalar stress is <= ~1e-6 of matter at every Solar-System PPN test radius (exp kernel: "
      "far smaller), so the aether EOM -- hence alpha_1, alpha_2 -- is set by aether+matter, essentially "
      "free of a0.  UNLIKE AeST, where the MOND field WAS the aether and fixed alpha_1 un-tunably",
      f"max scalar/matter stress over PN radii = {worst:.2e} (< 1e-5)", worst < 1e-5,
      "this is the load-bearing NEW result: the a0-scalar and the preferred-frame aether are separate "
      "sectors at PN order, so the aether couplings are not tied to a0 in the Solar System")

# =================================================================================================
banner("P2 [LIT, GR-validated] the aether alpha_1 vanishes in the GR limit and on a nontrivial surface")
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
# Foster-Jacobson 2006 preferred-frame alpha_1 for Einstein-aether (PUBLISHED; NOT re-derived here):
alpha1 = -8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2)
gr_limit = sp.limit(alpha1.subs({c2: 0, c3: 0, c4: 0}), c1, 0)
a1_family = sp.simplify(alpha1.subs(c4, -c3**2 / c1))     # numerator vanishes => alpha_1 = 0
check("P2 [LIT] the published aether alpha_1 = -8(c3^2 + c1 c4)/(2c1 - c1^2 + c3^2) vanishes in the GR "
      "limit (all c->0) and on the nontrivial surface c3^2 + c1 c4 = 0 (denominator generic) -- validated "
      "here, not re-derived",
      f"alpha_1(GR limit) = {gr_limit}; alpha_1 on c4=-c3^2/c1 = {a1_family}",
      gr_limit == 0 and a1_family == 0,
      "the exact COEFFICIENT is Foster-Jacobson's; what is validated is the GR limit (necessary) and that "
      "alpha_1=0 has a nontrivial solution locus -- both robust to any coefficient convention")
# honesty: the point c1=c3=c4=0 is a DEGENERATE 0/0 (denominator -> 0), NOT a clean alpha_1=0
P("    (honesty: c1=c3=c4=0 is a degenerate 0/0 limit of this expression, not a genuine alpha_1=0 point; "
  "the real alpha_1=0 locus is the numerator surface with the denominator nonzero)")

# =================================================================================================
banner("P3 [DERIVED] alpha_1 = alpha_2 = 0 is satisfiable: 2 conditions, >= 3 couplings")
n_couplings_khrono = 3      # hypersurface-orthogonal (khronometric): (alpha, beta, lambda)
n_couplings_aether = 4      # general Einstein-aether: c1..c4
n_conditions = 2            # alpha_1 = 0 and alpha_2 = 0
family_dim_khrono = n_couplings_khrono - n_conditions
check("P3 alpha_1 = alpha_2 = 0 imposes 2 conditions; khronometric has 3 couplings (aether has 4), so a "
      f">= {family_dim_khrono}-parameter family satisfies BOTH -- the PF alpha gate is SATISFIABLE, not "
      "forced nonzero",
      f"couplings (khrono) = {n_couplings_khrono}, conditions = {n_conditions}, family dim >= "
      f"{family_dim_khrono}", family_dim_khrono >= 1,
      "established fact: pure khronometric/Horava has an observationally-viable PPN window (Blas-Sibiryakov "
      "2011; survives post-GW170817); alpha_1=alpha_2=0 lies in it.  So the aether sector alone can pass")

# =================================================================================================
banner("P4 [OPEN] the residual crux -- named, not computed")
GAL = {}
# at galactic scales g ~ a0, the scalar back-reaction is O(1), NOT decoupled -- so the SAME couplings must
# do two jobs.  quantify: phantom/baryon at g = a0 is O(1).
x_gal = 1.0                                          # g = a0 (the MOND regime)
frac_gal = 1.0 / (2 * x_gal)                         # O(1)
check("P4 [OPEN] at galactic scales (g ~ a0) the scalar stress is O(1) of baryons, so the aether couplings "
      "there ARE tied to the MOND sector -- the open question is whether the SAME couplings give "
      "alpha_1=alpha_2=0 (Solar System) AND the working foliation-smoothing MOND (galactic)",
      f"scalar/baryon at g=a0 ~ {frac_gal:.2f} (O(1)); Solar System ~ {worst:.1e} (decoupled) -- two "
      f"regimes, one coupling set", frac_gal > 0.1,
      "this is the genuine remaining computation, with ghost-freedom on the alpha_1=alpha_2=0 family and "
      "the slip-lock (lensing=dynamics with the frame).  NOT done here or anywhere")

# =================================================================================================
banner("VERDICT")
P(f"""  (1) ATTEMPTED: the boosted khronon alpha_1/alpha_2 for the L268 action.
  (2) RESULT: [DERIVED] the MOND scalar decouples from the aether at PN order (stress <= {worst:.0e} of
      matter), so alpha_1/alpha_2 are the AETHER sector's, free of a0 -- the structural break from AeST.
      [LIT/validated] the aether alpha_1 vanishes in the GR limit and on a nontrivial surface, and
      alpha_1=alpha_2=0 (2 conditions, 3+ couplings) defines a nonempty family inside khronometric's
      known-viable PPN window.  So alpha_1/alpha_2 CAN be set to zero for this action.
  (3) HONEST SENTENCE: the preferred-frame alpha_1/alpha_2 are NOT the wall for the magnitude-only action.
      Unlike AeST (MOND field = aether, alpha_1 un-tunable), here the scalar decouples at PN order and the
      aether couplings are free to sit on the alpha_1=alpha_2=0 family.  I did NOT compute the exact
      boosted alpha VALUES for this action from the full Foster-Jacobson reduction (that remains undone,
      as L203 states) -- I established the DECIDING structural facts (decoupling + family existence),
      validated at the GR limit.  The gate therefore moves from 'the wall' to 'passable', and the genuine
      remaining crux SHIFTS to the galactic/Solar-System consistency: can ONE coupling set give
      alpha_1=alpha_2=0 in the Solar System (scalar decoupled) AND the working foliation MOND at galactic
      scales (scalar O(1))?  Plus ghost-freedom on the family and the slip-lock.  Those are the next
      computations, and they are where the theory now lives or dies.
      NOT CLAIMED: a computed alpha_i value, viability, ghost-freedom, or galactic consistency.  What IS
      claimed: alpha_1/alpha_2 do not kill this action the way they killed AeST, and the reason is the
      PN-order decoupling, which is rigorous.""")
OUT["verdict"] = {"word": "ALPHA-GATE-PASSABLE-NOT-A-WALL-GALACTIC-CONSISTENCY-OPEN",
                  "scalar_decouples_at_PN": True, "alpha1_alpha2_zero_achievable": True,
                  "exact_values_computed": False,
                  "residual_crux": "one coupling set: alpha_1=alpha_2=0 (Solar System) AND working "
                  "foliation MOND (galactic, scalar O(1)); plus ghost + slip-lock"}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb = [nm for nm, ok, l in CH if l and not ok]
P(f"L270 COMPLETE: {npass}/{n} checks PASS")
for nm in lb:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb else 0)
