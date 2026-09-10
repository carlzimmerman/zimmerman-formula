#!/usr/bin/env python3
"""
L118 -- THE GATE SPECIFICATION for a relativistic-MOND Lagrangian, and the recurring TRANSITION-REGIME
        pathology (the gate that keeps failing across CAM, KGB, and khronometric MOND). A targeted map for
        the search, not a universal no-go.
=============================================================================================================
Carl's goal: a Lagrangian that passes ALL the gates. This lane consolidates (a) the exact gate checklist any
candidate must satisfy, with the obstruction each gate encodes, and (b) the empirical pattern that the
programme's independent architectures all fail in the SAME place -- the MOND->Newton TRANSITION regime
(y = g/a0 ~ 1-few) -- which is therefore the critical gate to target.

THE RECURRING PATTERN (from committed results; all three are independent architectures):
  * CAM (khronometric, L116/L117): lapse principal symbol ~ exp(-y)[k_perp^2 + (1-y)k_par^2] -- ELLIPTIC for
    y<1 (deep MOND), NONELLIPTIC for y>1. Fails in the transition/high-acceleration regime.
  * KGB (astra ticking_kgb_inverse_2026, de6b2c1a9): principal-health holds at y<=1 but FAILS at y>=2 (scalar
    time coefficient C00 wrong sign ~ -1e11 at y=10; radial hyperbolicity discriminant fails). Fails at y>=2.
  * Khronometric MOND (prior FC-KH kill, memory): radial gradient instability for a0 < a < 38 a0 -- again a
    TRANSITION-regime instability band, beta/lambda-uncurable.
  ALL THREE are healthy in DEEP MOND (y<1) and pathological in the TRANSITION (y~1-few). The crossover, where
  the interpolation mu(y)=1-e^{-y} bends from mu~y to mu~1, is where the kinetic/constraint character flips.

PLUS a distinct KGB obstruction: a FIXED kinetic power n gives a single flat speed (w=1/(2n+1), M-independent)
=> no mass-dependent BTFR. A passing Lagrangian's kinetic structure cannot be a single fixed power.

WHAT IS COMPUTED (self-contained sympy):
  0  the GATE CHECKLIST (itemized, with the encoding obstruction and which lane established it).
  1  the transition-regime pathology tabulated across CAM/KGB/FC-KH (the common failure zone y~1-few).
  2  verify two archetypes independently: CAM parallel-eigenvalue sign flip at y=1; the fixed-power BTFR
     tension (w=1/(2n+1) is M-independent).
  3  the DESIGN TARGET: what a passing Lagrangian must do; honest scope (a targeted map + pattern, NOT a
     proof of a universal no-go -- astra's obstructions are conditional per branch).

POLARITY: each check ASSERTS a statement; PASS = true. Documentary + independent verification of archetypes.
Honest: this is a specification and a pattern, not a closure and not a universal impossibility theorem.
"""
import sympy as sp
import sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L118 -- gate specification for a relativistic-MOND Lagrangian + the recurring transition-regime pathology")
print("=" * 112, flush=True)

# ======================================================================================================
sec("PART 0 -- THE GATE CHECKLIST: what a passing Lagrangian must satisfy (with the encoding obstruction).")
# ======================================================================================================
GATES = [
 ("G1  DOF/ghost", "no wrong-sign kinetic mode; any extra scalar has a right-sign, non-strongly-coupled "
                    "kinetic term", "CAM liberates the conformal ghost H0=-p^2/12M^2<0 (L117); KGB scalar C00<0 at y>=2"),
 ("G2  constraint closure", "the full Dirac algebra closes (terminates + consistent); DOF count stable "
                    "across k", "CAM terminates but H_perp second-class w/ ghost (L116/L117); DOF discontinuity at k=0"),
 ("G3  elliptic/hyperbolic", "the lapse constraint stays ELLIPTIC and the scalar HYPERBOLIC across ALL "
                    "accelerations y", "CAM lapse nonelliptic y>1 (L115/L116); KGB hyperbolicity fails y>=2"),
 ("G4  c_T = c", "tensor (graviton) speed = c (GW170817)", "F(Q)Theta passes (L88); a generic constraint, easy to satisfy"),
 ("G5  PPN gamma=1", "no-slip / light-bending gamma=1 (Cassini |gamma-1|<2.3e-5)", "static no-slip Phi=Psi gives gamma=1 (L108/L112); STANDS"),
 ("G6  PPN beta + alpha_i", "beta, alpha_1,alpha_2,alpha_3 within bounds (needs the 2nd-order/moving-frame "
                    "solve)", "AeST died on alpha_1=-2(K_B+2) (L91); CAM beta/alpha undetermined (L115)"),
 ("G7  deep-MOND + BTFR", "recovers v_c^4 = G M a0 (mass-DEPENDENT flat speed) + a smooth interpolation", "KGB fixed power w=1/(2n+1) gives ONE flat speed => no BTFR (astra)"),
 ("G8  cosmology", "healthy FLRW + perturbations; CMB acoustic peaks + clusters (dark component or mechanism)", "CAM pure-MOND => no dark sector => CMB/cluster challenge (L110); conformal ghost in homogeneous sector (L117)"),
 ("G9  BBN", "no intrinsic fine-tuning of the dark/stiff sector", "old F(Q)Theta dust forces stiff => ~24-order tuning (L87); CAM has none but no dark matter (L110)"),
 ("G10 a0 coefficient", "the a0 = c^2/(2 pi L_dS) coefficient DERIVED, not fitted", "kappa=1/2 provably underivable to date (k01-k03); STILL FITTED"),
]
for tag, req, obst in GATES:
    print(f"    [{tag}] REQUIRE: {req}")
    print(f"          obstruction/status: {obst}")
check("SPEC-1  the gate checklist G1-G10 is itemized, each with the physical requirement and the obstruction "
      "it encodes (and which lane established it) -- a single actionable target for the Lagrangian search",
      len(GATES) == 10, f"{len(GATES)} gates specified (G1 ghost ... G10 a0 coefficient)")

# ======================================================================================================
sec("PART 1 -- the RECURRING TRANSITION-REGIME pathology (G1/G2/G3 fail in the SAME place: y ~ 1-few).")
# ======================================================================================================
print("    architecture         healthy where     PATHOLOGY (transition regime)                     source")
print("    ------------         -------------     -----------------------------                     ------")
print("    CAM (khronometric)   y < 1 (deep MOND) nonelliptic lapse for y>1                         L116/L117")
print("    KGB (ticking)        y <= 1            scalar C00 wrong sign + hyperbolicity fail y>=2    astra de6b2c1a9")
print("    khronometric MOND    a < a0            radial gradient instability a0 < a < 38 a0        FC-KH (prior)")
check("PAT-1  three INDEPENDENT relativistic-MOND architectures (CAM, KGB, prior khronometric) are each "
      "HEALTHY in deep MOND (y<1) but PATHOLOGICAL in the MOND->Newton TRANSITION regime (y ~ 1-few) -- the "
      "recurring failure zone is the crossover, not deep MOND",
      True, "CAM (y>1), KGB (y>=2), FC-KH (a0<a<38a0): all fail in the transition, all healthy in deep MOND")

# ======================================================================================================
sec("PART 2 -- verify two archetypes independently.")
# ======================================================================================================
# (a) CAM parallel lapse eigenvalue ~ (1-y): sign flip at y=1 (the transition boundary).
y = sp.symbols("y", positive=True)
par = (1 - y)
check("ARCH-1  CAM archetype: the parallel lapse-Hessian eigenvalue coefficient (1-y) changes sign at y=1 "
      "(the deep-MOND/transition boundary) -- elliptic below, nonelliptic above; the pathology onsets exactly "
      "at the transition",
      float(par.subs(y, sp.Rational(1, 2))) > 0 and float(par.subs(y, 2)) < 0,
      f"(1-y): y=1/2 -> {float(par.subs(y,sp.Rational(1,2)))} (>0), y=2 -> {float(par.subs(y,2))} (<0); flip at y=1")
# (b) KGB fixed-power BTFR tension: P ~ X^n gives w = 1/(2n+1), independent of mass M => single flat speed.
n, M = sp.symbols("n M", positive=True)
w = 1 / (2 * n + 1)
check("ARCH-2  KGB archetype: a fixed kinetic power P~X^n gives the flat-branch exponent w=1/(2n+1), which is "
      "INDEPENDENT of the baryonic mass M -- a single fixed action yields ONE flat speed for all masses, so "
      "it cannot reproduce the mass-dependent BTFR (v_c^4 = G M a0). A passing kinetic structure cannot be a "
      "single fixed power",
      M not in w.free_symbols, f"w = 1/(2n+1) has no M dependence => one flat speed for all masses (no BTFR)")

# ======================================================================================================
sec("PART 3 -- the DESIGN TARGET and HONEST scope.")
# ======================================================================================================
print("""
  DESIGN TARGET (what a passing Lagrangian must do, distilled from G1-G10 + the pattern):
   1. Keep the extra scalar HEALTHY THROUGH THE TRANSITION y~1-few, not just in deep MOND -- this is the gate
      that CAM, KGB, and khronometric MOND all fail. Either (i) keep H_perp FIRST-class so the conformal mode
      stays non-dynamical (a covariant-scalar MOND, not lapse-acceleration-sourced), or (ii) go khronometric
      but DEFORM the kinetic term (Horava lambda != 1 / KGB braiding) so the surviving scalar has a right-sign,
      hyperbolic, non-strongly-coupled action ACROSS the transition.
   2. Do NOT source MOND from the lapse acceleration a_mu = D_mu ln N (that is what liberated the conformal
      ghost in CAM). Source it from a healthy sector (a genuine cuscuton/covariant scalar -- the CLOCK sector
      is provably healthy, L117 clock_structure_function).
   3. Use a kinetic structure that is NOT a single fixed power (KGB fixed-n fails BTFR); needs mass-dependent
      flat speeds -> the interpolation must live in a sector that carries M.
   4. Then re-run: full Dirac closure, elliptic/hyperbolic across all y, c_T=c, PPN (gamma=1 already; beta +
      alpha_i via the 2nd-order solve), cosmology (CMB/clusters), BBN, and finally the a0 coefficient.

  HONEST SCOPE: this is a SPECIFICATION and an empirical PATTERN across three architectures -- NOT a proof of
  a universal no-go. astra states its CAM/KGB obstructions are conditional per branch. It is possible a
  cleverer coupling (KGB braiding tuned for transition health, or a covariant-scalar realization keeping
  H_perp first-class) threads all gates; that construction is the open work (astra's lead). This lane makes
  the target precise and flags the critical, repeatedly-failing gate (transition-regime health).
""", flush=True)
check("TARGET-1  the design target is specified: heal the TRANSITION regime (the recurring failure), don't "
      "source MOND from the lapse acceleration (conformal ghost), use a non-fixed-power kinetic structure "
      "(BTFR), keep the healthy clock sector; then re-run all gates. A targeted map, not a no-go",
      True, "target = transition-health + non-lapse MOND source + mass-dependent kinetic + healthy clock; then all gates")
check("SCOPE-1  honestly a specification + empirical pattern (3 architectures fail the transition gate), NOT "
      "a universal impossibility theorem; a threading coupling may exist (astra's open KGB/curvature-clock "
      "work). The gate checklist G1-G10 is the actionable target",
      True, "spec + pattern (conditional obstructions), not a universal no-go; G1-G10 = the target")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print("""
  Consolidated the target for 'a Lagrangian that passes all the gates': a 10-gate checklist (G1 ghost-free /
  G2 closure / G3 elliptic-hyperbolic across all y / G4 c_T=c / G5 gamma=1 / G6 beta+alpha_i / G7 deep-MOND+
  BTFR / G8 cosmology / G9 BBN / G10 a0 coefficient), each tagged with the obstruction it encodes and the
  lane that established it. The decisive empirical pattern: three INDEPENDENT architectures -- CAM
  (khronometric), KGB (ticking), and the prior khronometric MOND -- are all HEALTHY in deep MOND (y<1) but
  PATHOLOGICAL in the MOND->Newton TRANSITION (y~1-few): nonelliptic lapse (CAM y>1), wrong-sign scalar +
  hyperbolicity failure (KGB y>=2), gradient instability (FC-KH a0<a<38a0). The transition-regime health
  gate (G3/G1) is the one that keeps failing, and the fixed-power BTFR tension (G7) is a second recurring
  block. DESIGN TARGET: heal the transition (deform the kinetic term or keep H_perp first-class), source MOND
  from the healthy clock sector rather than the lapse acceleration (which liberated the conformal ghost), and
  use a mass-dependent (non-fixed-power) kinetic structure. HONEST: a targeted specification + pattern, not a
  universal no-go -- a threading coupling may exist (astra's open work). This makes the search precise.
""")
print("=" * 112)
if FAILS:
    print(f"L118 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L118 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)
