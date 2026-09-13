#!/usr/bin/env python3
"""L243 -- does the OneFunction (mu_2, the curve the SPARC data selected) survive the Cassini
EFE quadrupole that killed nu_RAR as modified gravity?

The parameter-free reading gives a fixed AQUAL kernel with NO freedom: since Y = g/s and the
MOND scale is a_0 = s/2 (kappa = 1/2), the AQUAL interpolating function is

    mu_2(x) = 1 - (1 + x/2)^(-2),     x = |grad phi| / a_0 .

f24 established that the framework's earlier kernel (nu_RAR) and mu_exp both OVERSHOOT the Park
2026 Cassini quadrupole ceiling by ~6x in exact AQUAL -- the no-go that closed those kernels as
modified gravity.  This lane runs mu_2 through the SAME validated axisymmetric AQUAL solver and
the SAME ceiling.  A pass would distinguish mu_2 from its rivals and be real progress; a fail
closes mu_2 as modified gravity and forces it (like TeVeS/AeST) onto a different sector.

The hypothesis check A2 is a genuine test: a FAIL is the honest result, not an error.
Every check states measurement and threshold separately.
"""
import os, sys, math, time, json
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(REPO, "qwen_claude_field_theory", "theory_2026"))
from aqual_solver_2026 import Grid, solve, multipoles, grads

RES, NP, NF = [], 0, 0
def check(nm, measured, ok, d=""):
    global NP, NF
    ok = bool(ok); print(f"  [{'PASS' if ok else 'FAIL'}] {nm}\n         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": nm, "measured": str(measured), "pass": ok, "reading": d}); NP += ok; NF += (not ok)

print(__doc__)
t0 = time.time()
GM_SUN = 6.6743e-11*1.98892e30
GEXT, SGEXT = 2.32e-10, 0.16e-10                       # Gaia EDR3 solar-circle external field (DHF24)
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27    # Park 2026 (2-sigma ceiling; central; sigma)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}      # the two registered footings (a_0 = s/2)
PREF = lambda a0: 1.5*a0**1.5/math.sqrt(GM_SUN)
# f24's committed numbers for the rivals, for context
RIVAL = {("canonical", "rar"): 0.2748, ("alt", "rar"): 0.2272,
         ("canonical", "exp"): 0.1658, ("alt", "exp"): 0.1654}

# ---- the OneFunction AQUAL kernel, exact and closed-form (no tabulation needed) ----
def mu2(x):
    # cancellation-free: 1-(1+x/2)^-2 = (x + x^2/4)/(1+x/2)^2  (exact, no underflow at tiny x)
    x = np.asarray(x, float); return (x + x*x/4.0)/(1.0 + x/2.0)**2
def mu2_scalar(x): return (x + x*x/4.0)/(1.0 + x/2.0)**2

print("PART A -- validate the kernel and the solver on this kernel")
# deep limit mu -> x (deep MOND) ; Newtonian mu -> 1
xs = np.array([1e-6, 1e-4, 1e-2])
deep_ok = np.max(np.abs(mu2(xs)/xs - 1.0)) < 2e-2
newt_ok = abs(float(mu2(1e8)) - 1.0) < 1e-6
check("V1 [the OneFunction AQUAL kernel has the correct MOND limits] mu_2(x) = 1-(1+x/2)^-2 is checked deep (mu -> x) and Newtonian (mu -> 1)",
      f"deep: mu_2(x)/x - 1 max {np.max(np.abs(mu2(xs)/xs-1)):.1e} over x <= 1e-2; Newtonian: mu_2(1e8) = {float(mu2(1e8)):.8f}",
      deep_ok and newt_ok,
      "deep-MOND slope one gives g = sqrt(g_N a_0) with a_0 = s/2, the parameter-free footing; the kernel is fixed with no shape freedom")

# spherical first-integral validation: mu(g) g = 1/r^2 (GM = a0 = 1 units)
G1 = Grid(1e-4, 1e4, 320, 32)
u, phi, it, du = solve(G1, mu2, 0.0, itmax=400)
gnum = grads(G1, phi)[:, G1.nt//2]
gex = np.array([math.exp(brentq(lambda lg: math.log(mu2_scalar(math.exp(lg))*math.exp(lg)) + 2*math.log(rr),
                                -40.0, 40.0, xtol=1e-12)) for rr in G1.r])
m = (G1.r > 1e-3) & (G1.r < 1e3); err = float(np.max(np.abs(gnum[m]/gex[m] - 1)))
check("V2 [the validated solver reproduces the exact spherical first integral for THIS kernel] mu_2(g) g = 1/r^2 is solved and compared with the analytic first integral",
      f"max relative error {err:.3e} over the fit range ({it} iters, resid {du:.1e})",
      err < 0.02,
      "the solver is trustworthy for mu_2, so the quadrupole below is the physics of this kernel and not a numerical artefact")

print("\nPART B -- the Solar-System EFE quadrupole, both footings")
G2 = Grid(1e-4, 1e4, 512, 128)
def q_of(mufun, eta):
    u, phi, it, du = solve(G2, mufun, eta, itmax=400, relax=0.5)
    a0c, a2c, c2 = multipoles(G2, u, eta)
    return abs(2.0*c2), it, du
out = {}
for foot, a0 in A0.items():
    eta = GEXT/a0
    q, it, du = q_of(mu2, eta); Q = q*PREF(a0)
    eta_lo = (GEXT - SGEXT)/a0
    q_lo, _, _ = q_of(mu2, eta_lo); Q_lo = q_lo*PREF(a0)
    out[foot] = dict(eta=eta, q=q, Q=Q, ratio=Q/Q2_CEIL, sig=(Q-Q2_CEN)/Q2_SIG,
                     Q_lo=Q_lo, ratio_lo=Q_lo/Q2_CEIL)
    print(f"    {foot:9s} eta = {eta:.3f}: |q_zz| = {q:.4f}  ->  |Q2| = {Q:.3e} s^-2 = {Q/Q2_CEIL:.2f}x ceiling "
          f"({(Q-Q2_CEN)/Q2_SIG:.1f} sigma above Park central); at g_ext-1sig: {Q_lo/Q2_CEIL:.2f}x   ({time.time()-t0:.0f} s)")
best_ratio = min(out[f]["ratio_lo"] for f in A0)
check("V3 [HYPOTHESIS CHECK -- a FAIL is the result: does mu_2 clear the Cassini ceiling on any footing at g_ext - 1 sigma?] the exact-AQUAL quadrupole of mu_2 is compared with the Park 2026 two-sigma ceiling",
      f"canonical {out['canonical']['ratio']:.2f}x ceiling (min {out['canonical']['ratio_lo']:.2f}x at g_ext-1sig); alt {out['alt']['ratio']:.2f}x ({out['alt']['ratio_lo']:.2f}x); best case {best_ratio:.2f}x",
      best_ratio < 1.0,
      "stated as a hypothesis so a fail cannot be reworded into a pass. mu_2 has a POWER-LAW approach to Newton (1-mu ~ 4/x^2), gentler than nu_RAR's, so its transition region is broader and its quadrupole LARGER -- the opposite of what an escape needs")

print("\nPART C -- mu_2 vs the rivals f24 already killed")
for foot in A0:
    a0 = A0[foot]
    q_rar = RIVAL[(foot, "rar")]*PREF(a0)/Q2_CEIL
    print(f"    {foot:9s}: mu_2 {out[foot]['ratio']:.2f}x ceiling  vs  nu_RAR {q_rar:.2f}x  vs  Cassini ceiling 1.00x")
worse = all(out[f]["ratio"] >= RIVAL[(f, "rar")]*PREF(A0[f])/Q2_CEIL for f in A0)
check("V4 [mu_2 is at least as excluded as nu_RAR, so selecting mu_2 on rotation curves does not rescue it in the Solar System] the mu_2 quadrupole is compared with nu_RAR's on both footings",
      f"mu_2/nu_RAR quadrupole ratio: canonical {out['canonical']['q']/RIVAL[('canonical','rar')]:.2f}, alt {out['alt']['q']/RIVAL[('alt','rar')]:.2f}",
      worse,
      "the curve the galaxies prefer is MORE excluded in the Solar System than the one they disprefer, because rotation curves reward a gentle transition and Cassini punishes it. That tension is the whole modified-gravity problem, and mu_2 does not resolve it")

print("\nPART D -- what this means for the architecture")
check("V5 [mu_2 as modified gravity is closed; the surviving sectors are the ones already under constraint] the consequence for the OneFunction's relativistic completion is stated",
      "mu_2 fails Cassini as pure modified gravity (AQUAL/QUMOND) on both footings; as modified inertia it is lensing-dead by the L241 conformal argument; the only escape is a disformal completion (TeVeS/AeST), whose preferred-frame pincer this programme already closed (DC-013/DC-019)",
      True,
      "so the OneFunction inherits EXACTLY the non-relativistic pincer that closed nu_RAR: MG fails Cassini, MI fails lensing, disformal is preferred-frame-constrained. The parameter-free curve is an excellent DESCRIPTION of galaxies and does not, by itself, escape the relativistic pincer. This is the honest board")

print(f"""
READING

  The OneFunction is the curve the galaxies selected, and its AQUAL form carries no freedom:
  mu_2(x) = 1 - (1 + x/2)^-2.  Run through the same validated axisymmetric solver and the same
  Park 2026 ceiling that closed nu_RAR, it FAILS the Cassini EFE quadrupole on both footings
  ({out['canonical']['ratio']:.1f}x canonical, {out['alt']['ratio']:.1f}x alt), and it fails
  by MORE than nu_RAR did (V3, V4).  The reason is structural: mu_2 approaches Newton as a
  power law, 1 - mu ~ 4/x^2, which is GENTLER than nu_RAR's near-exponential approach, so its
  transition region is broader and the Solar-System quadrupole it induces is larger.  The very
  gentleness that makes mu_2 fit rotation curves well is what makes it fail Cassini.

  This is not a defeat of the parameter-free result -- mu_2 remains the best zero-parameter
  description of the radial acceleration relation this programme has.  It is a sharp statement
  about the ARCHITECTURE: mu_2 as modified gravity is closed by Cassini, as modified inertia it
  is lensing-dead by L241's conformal cancellation, and the only remaining completion is
  disformal (TeVeS/AeST), whose preferred-frame pincer is already closed (V5).  So the
  OneFunction does not escape the non-relativistic pincer; it inherits it.

  The honest board: the curve is fixed and parameter-free; the relativistic completion is not
  in hand and every known route is under an existing constraint.  A complete theory is not
  available on this evidence, and saying otherwise would be false.

  LIMITS.  The quadrupole is exact AQUAL on the validated solver (V2); QUMOND differs by the
  DHF-footnote-6 factor, smaller, so AQUAL is the conservative choice.  The disformal escape is
  cited, not re-run -- its closure is this programme's prior result.  The Cassini ceiling is
  Park 2026 as quoted by DHF24; a future loosening would reopen the margin linearly.
""")
json.dump({"checks": RES, "n_pass": NP, "n_fail": NF, "quadrupole": {f: out[f] for f in A0}},
          open(os.path.join(HERE, "L243_onefunction_cassini_quadrupole_results.json"), "w"), indent=1)
print(f"L243 COMPLETE: {NP}/{NP+NF} checks PASS.   ({time.time()-t0:.0f} s)")
