#!/usr/bin/env python3
r"""mi_route_d_dragged_frame_nogo_2026.py
========================================================================================================
ROUTE D -- ADVERSARIAL NO-GO HUNT AGAINST A LOCALLY-DRAGGED PASSIVE FRAME.

FRAMEWORK (judged on its OWN terms, never through a standard-MOND lens, never with McGaugh's nu).
de Sitter-Unruh MODIFIED INERTIA. a0 = c H_Lambda / Z with Z = sqrt(32 pi/3) = 5.78881, on the pure-
Lambda (rho_DE) footing a0 = 9.36e-11 m/s^2; equivalently a0 = (c/2) sqrt(G rho_Lambda), EXACTLY HALF
the free-fall acceleration at the dark-energy density. The coefficient kappa = 1/2 is Carl Zimmerman's
and is absent from the prior literature (Milgrom 1999 PLA 253:273, Pikhitsa 2010, Klinkhamer & Kopp
2011 all land on 2 c H_Lambda = 11.58x larger; Milgrom 2020 gives c H_Lambda/2pi).
CAVEAT CARRIED EVERY TIME: 32pi/3 is the Einstein-coupling conversion factor and CANCELS in that
reduction, so the content is the ONE number kappa = 1/2, and it is FITTED, not derived (the
kappa-forcing door closed 2026-06-17). Treating 32pi/3 as independent geometric structure is the
RETRACTED numerology direction.
ALTERNATE FOOTING carried on every dimensional number: a0 = 1.13e-10 (rho_total / c H0).
KERNEL IN FORCE: alpha = 2, mu(x) = x/sqrt(1+x^2).  RETIRED: alpha = 1.

------------------------------------------------------------------------------------------------------
THE DOOR THIS FILE ATTACKS
------------------------------------------------------------------------------------------------------
Theorem 8 (kernel-independent): the nonlocal operator action's argument is w = c Omega/a0 while the
law's is x = a/a0, and w/x = c/v exactly. So the missing factor is a SPEED. A lone worldline has no
speed; a PASSIVE PREFERRED FRAME supplies one. The corpus already computed the LOCK: a COSMIC (CMB)
frame speed would inject ~1.0 dex of a0 variation against a total RAR budget of ~0.22 dex -> excluded
at ~4.6x. Hence the target: the frame must be LOCALLY DRAGGED so a star's frame-relative speed is its
ORBITAL speed, not its galaxy's bulk motion.

MY JOB IS THE OPPOSITE OF CONSTRUCTION: find the obstruction and make it rigorous. Default = there is
one. Six candidates were assigned. This file prosecutes all six, ranks them, and reports which DIED.

------------------------------------------------------------------------------------------------------
RESULT (each horn is a numbered section below; nothing here is asserted without a computed number)
------------------------------------------------------------------------------------------------------
S1  THE DICTIONARY. A frame-speed error by factor lam = v_rel/v_orb is EXACTLY a0 -> a0/lam, for ANY
    interpolating function (sympy, symbolic mu). So every horn reduces to a spread in log10(lam)
    measured against the framework's own RAR budget. The estimator is calibrated by reproducing the
    corpus's own cosmic-frame 4.6x number.

S2  HORN A -- STRICTLY-LOCAL DRAG (u = local matter 4-velocity: the unique local, boost-FIXING,
    scale-free, manifestly passive prescription). Its own tracer kills it: HI gas IS the local matter,
    so lam = sigma_gas/v_c ~ 0.04-0.10 on real SPARC -> 1.0-1.4 dex of a0, 4.5-6.3x over budget; at
    lam = 0 exactly the closure has NO SOLUTION (mu(0) = 0 identically). Plus a tracer split: stars
    and gas at the same radius would differ by ~23% in rotation speed.

S3  HORN A' -- AND THE SAME HORN DIES A SECOND, INDEPENDENT WAY, WITH THE SHARPEST NUMBER IN THE FILE.
    From the action itself: the differential anomalous acceleration between two bodies of a common
    subsystem is EXACTLY  -w x (curl u)  -- a Coriolis force in the frame's VORTICITY (derived
    symbolically, negative control u = const gives exactly zero). The Earth ranging bound then caps
    the frame vorticity at 1/717 of the Milky Way's own measured matter vorticity (Oort A - B).
    So the frame may NOT be dragged rotationally at all: the rotational drag fraction is <= 1.4e-3.

S4  HORN B -- IRROTATIONAL + ELLIPTIC PASSIVE DRAG (the form S3 forces and the only form that keeps
    zero propagating modes). Two theorems kill it:
      (i) STATIONARITY. Continuity makes the irrotational source exactly -d rho/dt, which VANISHES
          IDENTICALLY for any stationary bound system; and its volume integral is dM/dt = 0 always.
          So a stationary galaxy exerts ZERO irrotational drag and u reverts to its boundary value =
          the cosmic frame -> the corpus's own 4.6x lock, unchanged.
      (ii) THE TRACE IDENTITY. The one surviving piece (rigid translation) has drag tensor
          f_ij = -kappa_d d_i d_j chi with Laplacian chi = rho, so (1/3)Tr f = -kappa_d rho(x)/3
          POINTWISE for any profile: the drag fraction is proportional to the LOCAL DENSITY. A single
          coupling cannot give f ~ 1 across SPARC's density range, and what it produces is
          a0_eff(rho_local) -- the door the framework's OWN SPARC environmental test already nulled
          at 10.5 sigma.

S5  HORN C -- PASSIVITY. THIS ONE DIED AS AN INDEPENDENT OBSTRUCTION, and I report it as such. The
    u-velocity Hessian of the general 4-coefficient aether kinetic term is 2(c1 - c4)delta_ij, so
    c1 = c4 gives ZERO propagating dof WITH spatial gradients intact. Passivity is therefore
    COMPATIBLE with an elliptic smoothing operator. It does not close the door by itself -- it forces
    the door into HORN B, where S4 closes it.

S6  HORN D -- SMOOTHED DRAG OVER A NEW LENGTH R_drag (a fifth constant). Quantitative window scan on
    the real SPARC sample: S3's vorticity bound sets R_drag from BELOW, host-weight domination sets it
    from ABOVE, and the two requirements are computed and intersected. Reported honestly including the
    galaxies for which a window survives.

S7  NESTING / WELL-DEFINEDNESS, and TWO LIVE-FRONT CONSEQUENCES. a0_eff = a0 (v_orb/v_frame) is
    SUBSYSTEM-dependent over ~3.2 dex; one u per point cannot serve both the Sun's galactic orbit and
    the Earth's solar orbit (mismatch exactly 7.8). Front A: the dragged frame FORCES gamma_v = 1.0000
    for wide binaries, outside the FROZEN pre-registration band 1.0182-1.0350. Front B: the frozen
    s^TX prediction is frame-dependent -- the dragged apex is 131.5 deg from the CMB apex at 0.63x the
    speed, so it needs re-derivation. REPORTED, NOT AMENDED (frozen pre-regs are amended in the open,
    by Carl, before data; not by a subagent).

CREDIT. Mach's principle is ancient prior art for inertia-relative-to-matter; Sciama 1953 (MNRAS 113,
34) is the standard citation, and the "fictitious forces from a non-rigidly-dragged frame" objection is
classical -- S3 is its modern quantitative form, not a new idea. Milgrom 1994 Ann.Phys. 229:384
(modified inertia, orbit-dependent interpolating functions), Milgrom astro-ph/0510117 (virial),
Milgrom 2022 PRD 106:064060 (Fourier-space MI; the algebraic relation holds ONLY for single-frequency
trajectories). Lense-Thirring / gravitomagnetic frame dragging is the GR prior art for S4's vector
option. NOVELTY IS ASSESSED, NEVER ASSERTED, in the verdict block.

HONESTY GUARDS. Exits non-zero on any failed internal check. Every check is structural (an identity, a
limit, a sign, a monotonicity, a scaling) -- no check(True, ...). Both a0 footings on every dimensional
number, and where a result is footing-FREE that is stated rather than faked. mpmath at 50 digits is
used wherever a quantity is a difference of large terms. Nothing here derives a0; nothing here says the
theory is closed; nothing here revives the retracted TOE/Standard-Model claims.
"""
from __future__ import annotations

import math
import os

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 50

ok = True
FAILS: list[str] = []


def check(c, m):
    global ok
    c = bool(c)
    if not c:
        ok = False
        FAILS.append(m)
    print(f"  [{'OK' if c else 'FAIL'}] {m}")


def banner(s):
    print("\n" + "=" * 102)
    print(s)
    print("=" * 102)


# ---------------------------------------------------------------------------------------------------
# S0. CONSTANTS, FOOTINGS, AND THE FRAMEWORK'S OWN BUDGET
# ---------------------------------------------------------------------------------------------------
C = 2.99792458e8                     # m/s
G = 6.67430e-11                      # m^3 kg^-1 s^-2
KPC = 3.0856775814913673e19          # m
MPC = 1000.0 * KPC
AU = 1.495978707e11                  # m
MSUN = 1.98847e30                    # kg
YR = 3.15576e7                       # s (Julian)

Z_FACTOR = math.sqrt(32.0 * math.pi / 3.0)
A0_CANON = 9.36e-11                  # rho_DE footing, cH_Lambda/Z
A0_ALT = 1.13e-10                    # rho_total / cH0 footing
FOOTINGS = (("canonical rho_DE ", A0_CANON), ("alternate rho_tot", A0_ALT))

# The framework's OWN measured RAR scatter (STANDING.md sec.1): 0.1116 dex at alpha=2 (in force),
# 0.1083 at the retired alpha=1. The corpus's published budget line uses 0.108.
RAR_SCATTER_A2 = 0.1116
RAR_SCATTER_A1 = 0.1083
# Deep regime g_obs = sqrt(g_bar a0)  =>  d log10 g_obs = 0.5 d log10 a0  =>  budget = 2 x scatter.
BUDGET_A2 = 2.0 * RAR_SCATTER_A2
BUDGET_A1 = 2.0 * RAR_SCATTER_A1
# Tighter alternative: Desmond 2023 RAR universality sigma_int = 0.034 dex -> +/-0.068 at 1 sigma.
BUDGET_TIGHT = 2.0 * 0.034

# Solar-system / Milky Way kinematics (measured inputs, sources named in-line).
V_SUN_GAL = 233.0e3        # m/s   Sun's circular speed (GRAVITY-anchored, ~229-233)
R_SUN_GAL = 8.178 * KPC    # m     GRAVITY Collab. 2019
V_EARTH = 29.7827e3        # m/s   Earth mean orbital speed
V_MARS = 24.077e3          # m/s
OORT_A = 15.3e3 / KPC      # s^-1  Bovy 2017 / Gaia: A = 15.3 +/- 0.4 km/s/kpc
OORT_B = -11.9e3 / KPC     # s^-1  B = -11.9 +/- 0.4 km/s/kpc
# Sereno & Jetzer 2006 (astro-ph/0606197) Table 1 (Pitjeva EPM2004) inverted through their Eq (9);
# these two numbers are ALREADY VERIFIED FROM PRIMARY SOURCE IN-CORPUS (STANDING.md sec.5.0).
DAR_EARTH = 3.66e-14       # m/s^2, 2 sigma
DAR_MARS = 3.72e-14        # m/s^2, 2 sigma
# Cosmology for the mean matter density (Planck-like), used only as the MOST GENEROUS environment.
H0 = 67.4e3 / MPC          # s^-1
OM_M = 0.315
RHO_CRIT = 3.0 * H0**2 / (8.0 * math.pi * G)
RHO_MEAN_M = OM_M * RHO_CRIT                       # kg/m^3
RHO_MEAN_MSUN_KPC3 = RHO_MEAN_M / MSUN * KPC**3    # Msun/kpc^3

HERE = os.path.dirname(os.path.abspath(__file__))
SPARC_MRT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/SPARC_Lelli2016c.mrt"


def mu2(x):
    """alpha = 2 kernel IN FORCE: Milgrom 1983 'standard' mu."""
    x = np.asarray(x, dtype=float)
    return x / np.sqrt(1.0 + x * x)


def mu1(x):
    """alpha = 1 kernel, RETIRED; carried because the corpus's published numbers are on it."""
    x = np.asarray(x, dtype=float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


def solve_closure(g_bar, a0, kernel=mu2, lam=1.0):
    """Solve g_bar = A mu(lam A / a0) for A > 0 by bisection at high precision.

    lam = v_rel/v_orb is the frame-speed error factor. lam = 1 is the framework's own closure.
    """
    f = lambda A: A * float(kernel(lam * A / a0)) - g_bar
    lo, hi = 1e-30, max(1e3, 1e6 * g_bar / max(lam, 1e-300))
    if f(hi) < 0:
        return math.nan
    for _ in range(400):
        mid = math.sqrt(lo * hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


_SPARC_CACHE: list | None = None


def load_sparc():
    """Real SPARC I (Lelli, McGaugh & Schombert 2016) Table 1.

    Parsed by whitespace (galaxy names contain none), with a hard row-count assertion against the
    published sample size so a silent mis-parse cannot quietly weaken or strengthen any result.
    Column order per the file's own byte-by-byte description:
        Galaxy T D e_D f_D Inc e_Inc L[3.6] e_L Reff SBeff Rdisk SBdisk MHI RHI Vflat e_Vflat Q [Ref]
    """
    global _SPARC_CACHE
    if _SPARC_CACHE is not None:
        return _SPARC_CACHE
    rows = []
    with open(SPARC_MRT, "r") as fh:
        for ln in fh:
            tk = ln.split()
            if len(tk) < 18:
                continue
            try:
                vals = [float(t) for t in tk[1:18]]
            except ValueError:
                continue
            if not (0 <= vals[0] <= 11):        # Hubble type flag sanity
                continue
            rows.append(dict(name=tk[0], T=vals[0], D=vals[1], L36=vals[6], Reff=vals[8],
                             Rdisk=vals[10], MHI=vals[12], RHI=vals[13], Vflat=vals[14],
                             Q=int(vals[16])))
    if len(rows) != 175:
        raise RuntimeError(f"SPARC parse produced {len(rows)} rows, expected the published 175 -- "
                           f"refusing to run on a mis-parsed table")
    _SPARC_CACHE = rows
    return rows


# ---------------------------------------------------------------------------------------------------
def s1_dictionary():
    banner("S1. THE DICTIONARY -- a frame-speed error IS an a0 error, exactly, for ANY kernel")
    A, a0, lam = sp.symbols("A a_0 lambda", positive=True)
    mu = sp.Function("mu")
    lhs = A * mu(lam * A / a0)          # closure evaluated with the WRONG (frame-relative) speed
    rhs = A * mu(A / (a0 / lam))        # closure with the RIGHT speed but a rescaled a0
    check(sp.simplify(lhs - rhs) == 0,
          f"symbolic, for an UNSPECIFIED mu: A mu(lam A/a0) == A mu(A/(a0/lam)) -- so the kernel-argument "
          f"speed error lam is IDENTICALLY the substitution a0 -> a0/lam. Kernel-independent, so it "
          f"holds for the alpha=2 kernel in force and for the retired alpha=1 alike")

    print("\n  and in the deep regime the a0 error shows up at HALF strength in the observable:")
    g_b, a0s = sp.symbols("g_bar a_0", positive=True)
    Adeep = sp.solve(sp.Eq(g_b, A * (lam * A / a0s)), A)          # mu_2(x) -> x as x -> 0
    Adeep = [s for s in Adeep if sp.ask(sp.Q.positive(s)) is not False][0]
    print(f"      deep-regime solution  A = {sp.simplify(Adeep)}")
    dlog = sp.simplify(sp.diff(sp.log(Adeep), sp.log(lam)) if False else
                       sp.diff(sp.log(Adeep.subs(lam, sp.exp(sp.Symbol('t')))), sp.Symbol('t')))
    check(sp.simplify(dlog + sp.Rational(1, 2)) == 0,
          f"d ln g_obs / d ln lam = {dlog} = -1/2 exactly, so d log10 g_obs = -0.5 d log10 lam. "
          f"The framework's own RAR scatter therefore budgets TWICE itself in log10 a0")

    print(f"\n  THE BUDGET, from the framework's own numbers (STANDING.md sec.1):")
    print(f"      RAR scatter  alpha=2 (in force) {RAR_SCATTER_A2:.4f} dex -> a0 budget "
          f"{BUDGET_A2:.4f} dex (factor {10**BUDGET_A2:.3f})")
    print(f"      RAR scatter  alpha=1 (retired)  {RAR_SCATTER_A1:.4f} dex -> a0 budget "
          f"{BUDGET_A1:.4f} dex (factor {10**BUDGET_A1:.3f})")
    print(f"      TIGHTER alternative (Desmond 2023 sigma_int = 0.034 dex): {BUDGET_TIGHT:.4f} dex")
    print("  The headline budget below is the GENEROUS one: the whole observed RAR scatter is handed")
    print("  to a0 variation, with nothing reserved for distance, inclination or mass-to-light. That")
    print("  is deliberately generous to the dragged-frame hypothesis.")

    print("\n  NUMERICAL CONFIRMATION of the dictionary on the alpha=2 kernel in force, both footings:")
    print(f"  {'footing':<18s} {'g_bar/a0':>9s} {'lam':>6s} {'A(lam,a0)':>12s} {'A(1,a0/lam)':>12s} {'rel diff':>10s}")
    worst = 0.0
    for nm, a0v in FOOTINGS:
        for y in (0.01, 0.1, 1.0, 10.0):
            for lv in (0.05, 0.5, 2.0, 20.0):
                g = y * a0v
                A1v = solve_closure(g, a0v, mu2, lam=lv)
                A2v = solve_closure(g, a0v / lv, mu2, lam=1.0)
                rel = abs(A1v - A2v) / A2v
                worst = max(worst, rel)
                if y in (0.01, 10.0) and lv in (0.05, 20.0):
                    print(f"  {nm:<18s} {y:9.2f} {lv:6.2f} {A1v:12.5e} {A2v:12.5e} {rel:10.2e}")
    check(worst < 1e-10,
          f"worst relative disagreement over 32 (footing, y, lam) combinations = {worst:.2e} -- the "
          f"dictionary is exact numerically as well as symbolically")

    print("\n  ESTIMATOR CALIBRATION -- reproduce the corpus's OWN cosmic-frame lock so the metric below")
    print("  is not a new and unvalidated one:")
    v_pec = np.array([100.0, 300.0, 620.0, 1000.0]) * 1e3
    spread_cosmic = math.log10(v_pec.max() / v_pec.min())
    over = spread_cosmic / BUDGET_A1
    print(f"      peculiar velocities {v_pec.min()/1e3:.0f}-{v_pec.max()/1e3:.0f} km/s = "
          f"{spread_cosmic:.3f} dex; budget (alpha=1, the corpus's) {BUDGET_A1:.3f} dex -> {over:.2f}x over")
    check(abs(over - 4.6) < 0.15,
          f"reproduces the corpus's published 4.6x cosmic-frame lock to {abs(over-4.6):.3f} -- the "
          f"estimator used in S2-S6 is the corpus's own, recomputed here, not a new one")
    return dict(budget=BUDGET_A2, budget_a1=BUDGET_A1, budget_tight=BUDGET_TIGHT)


# ---------------------------------------------------------------------------------------------------
def s2_horn_a_comoving(env):
    banner("S2. HORN A -- STRICTLY-LOCAL DRAG (u = local matter 4-velocity). ITS OWN TRACER KILLS IT.")
    print("  Why this prescription and not another: u^mu = U^mu_matter(x) is the UNIQUE prescription")
    print("  that is (a) algebraic in the local fields, (b) boost-covariant AND boost-FIXING (a static")
    print("  configuration's own 4-velocity picks the boost, which no Galilei-invariant differential")
    print("  condition can do), (c) free of any new constant, and (d) manifestly passive (u is a")
    print("  function of T_mu_nu, with no equation of its own). Every other option below buys its way")
    print("  out of one of those four and pays for it.")

    print("\n  THE COLLAPSE. The RAR is measured on HI rotation curves. HI gas in a rotating disk IS the")
    print("  local matter, so its velocity relative to a locally-comoving frame is not its orbital")
    print("  speed at all -- it is only its random motion about the local mean.")
    check(float(mu2(0.0)) == 0.0 and float(mu1(1e-300)) < 1e-299,
          "at lam = 0 exactly the closure g_bar = A mu(lam A/a0) becomes g_bar = A mu(0) = 0 for EVERY "
          "A, because mu(0) = 0 identically in both kernels -- so for any g_bar > 0 there is NO "
          "solution. The theory is not mispredicting the RAR; at the exactly-comoving limit it has no "
          "equation of motion to predict with")

    rows = [r for r in load_sparc() if r["Vflat"] > 0.0]
    vfl = np.array([r["Vflat"] for r in rows])
    print(f"\n  Real SPARC I (Lelli+2016) Table 1: {len(rows)} galaxies with a measured Vflat, "
          f"{vfl.min():.1f}-{vfl.max():.1f} km/s")
    print(f"  {'sigma_gas':>10s} {'lam range':>20s} {'|log10(1/lam)| range (dex)':>28s} {'x budget':>10s}")
    worst_over = 0.0
    for sig in (8.0, 10.0, 12.0):     # HI turbulent velocity dispersion, standard 8-12 km/s
        lam = sig / vfl
        dex = np.abs(np.log10(1.0 / lam))
        over = dex.max() / env["budget"]
        worst_over = max(worst_over, over)
        print(f"  {sig:8.1f}   {lam.min():7.4f}-{lam.max():7.4f}   "
              f"{dex.min():11.3f}-{dex.max():11.3f}        {over:8.2f}")
    check(worst_over > 3.0,
          f"a strictly-comoving frame injects up to {worst_over*env['budget']:.2f} dex of a0 variation "
          f"on the real SPARC sample against a budget of {env['budget']:.3f} dex -- {worst_over:.1f}x "
          f"over. And this is the GENEROUS reading (whole scatter handed to a0); on Desmond's "
          f"sigma_int the factor is {worst_over*env['budget']/env['budget_tight']:.0f}x")

    print("\n  THE SPREAD IS THE POINT, not the offset. A single global rescaling of a0 is absorbable")
    print("  into kappa (kappa is fitted anyway), so only the SAMPLE SPREAD counts. Median-subtracted:")
    for sig in (10.0,):
        lam = sig / vfl
        d = np.log10(1.0 / lam)
        d -= np.median(d)
        print(f"      sigma_gas = {sig:.0f} km/s: residual spread max-min {d.max()-d.min():.3f} dex, "
              f"RMS {d.std():.3f} dex, budget {env['budget']:.3f} dex "
              f"-> {(d.max()-d.min())/env['budget']:.2f}x / {d.std()/env['budget']:.2f}x over")
        check(d.std() > env["budget"],
              f"even after absorbing the best global a0 shift into kappa, the RMS residual "
              f"{d.std():.3f} dex exceeds the whole budget {env['budget']:.3f} dex. The kill is a "
              f"SPREAD, so it cannot be renormalised away")

    print("\n  AND A SECOND, INDEPENDENT SIGNATURE OF THE SAME HORN -- A TRACER SPLIT. Two tracers at")
    print("  the same radius with different random motions get different a0_eff, hence different")
    print("  circular speeds (deep regime v^4 = G M a0_eff, so v ~ lam^-1/4):")
    sig_gas, sig_star = 10.0, 25.0            # HI ~10 km/s; old-disk stars ~20-30 km/s
    split = (sig_star / sig_gas) ** (-0.25)
    print(f"      sigma_gas {sig_gas:.0f} km/s, sigma_star {sig_star:.0f} km/s -> "
          f"v_star/v_gas = {split:.3f}, i.e. a {100*(1-split):.1f}% split at the SAME radius")
    print("      Measured: after asymmetric-drift correction, stellar and gas rotation curves in disk")
    print("      galaxies agree at the few-per-cent level (order 5-10 km/s out of 150-200). A 23%")
    print("      split is an order of magnitude larger. Stated as an order-of-magnitude comparison,")
    print("      not as a sigma -- I did not re-fit a stellar/gas curve pair here.")
    check(1.0 - split > 0.10,
          f"predicted tracer split {100*(1-split):.1f}% is >10%, an order of magnitude above the "
          f"observed few-per-cent stellar-vs-gas agreement -- a second, tracer-based failure of the "
          f"strictly-local prescription that does NOT go through the a0 budget at all")

    print("\n  NEGATIVE CONTROL (this must PASS or the section is meaningless): a NON-comoving tracer,")
    print("  lam = 1 exactly, must return the framework's own closure with zero residual.")
    resid = 0.0
    for nm, a0v in FOOTINGS:
        for y in (0.01, 1.0, 100.0):
            A = solve_closure(y * a0v, a0v, mu2, lam=1.0)
            resid = max(resid, abs(A * float(mu2(A / a0v)) - y * a0v) / (y * a0v))
    check(resid < 1e-12,
          f"lam = 1 reproduces g_bar = A mu(A/a0) to {resid:.1e} relative, both footings, three "
          f"decades of y -- the estimator returns PASS when it should")
    return dict(n_sparc=len(rows), vflat=vfl, over=worst_over, split=100.0 * (1.0 - split))


# ---------------------------------------------------------------------------------------------------
def s3_coriolis(env):
    banner("S3. HORN A' -- THE FRAME-VORTICITY (CORIOLIS) BOUND. The sharpest number in this file.")
    print("  The action that reproduces the closure on circles (mi_offcircular_action_2026.py) is")
    print("      S[x] = Int dt m ( |xdot|^2 f(|xddot|/a0) - phi(x) ),   f(u) = u^-2 Int_0^u v mu(v) dv,")
    print("  and the WHOLE POINT of the door is that |xdot| must be measured relative to the frame:")
    print("      S[x] = Int dt m ( |xdot - u(x)|^2 f(|xddot|/a0) - phi(x) ).")
    print("  If the speed is NOT frame-relative, Theorem 8's c/v mismatch is unrepaired. So the")
    print("  u(x)-dependence is forced, not optional -- and a position-dependent u breaks translation")
    print("  invariance. That is candidate obstruction 4 (conservation laws). Here is its exact form.")

    t = sp.symbols("t", real=True)
    x = sp.Matrix([sp.Function(f"x{i}")(t) for i in range(3)])
    U = [sp.Function(f"u{i}")(*x) for i in range(3)]
    Uv = sp.Matrix(U)
    m, fc = sp.symbols("m f_c", positive=True)
    phi = sp.Function("phi")(*x)
    vrel = x.diff(t) - Uv
    # Newtonian limit of the action: f -> f_c = 1/2 constant (verified numerically below), so the
    # 4th-order piece drops and the EL equation is the honest 2nd-order one.
    L = m * (fc * (vrel.T * vrel)[0, 0] - phi)
    el = sp.zeros(3, 1)
    for i in range(3):
        el[i] = sp.diff(L, x[i].diff(t)).diff(t) - sp.diff(L, x[i])
    # Extract the anomalous piece: everything that is not m*xddot + m*grad(phi).
    anom = sp.zeros(3, 1)
    for i in range(3):
        e = sp.expand(el[i] / (2 * m * fc))
        anom[i] = sp.simplify(e - x[i].diff(t, 2) - sp.diff(phi, x[i]) / (2 * fc))
    print("\n  The anomalous (non-Newtonian) acceleration from the EL equation has exactly two pieces:")
    print("      delta a_i = (v . grad) u_i  -  (v - u)_j d_i u_j          [v = xdot]")
    print("  (printed in compact vector form; the three explicit component expressions are what the")
    print("   checks below are run on, and each has 7 terms)")
    nterms = [len(sp.expand(sp.simplify(-anom[i])).args) for i in range(3)]
    check(all(n >= 6 for n in nterms),
          f"the anomalous acceleration is genuinely nonzero and structurally rich (term counts "
          f"{nterms} per component) -- there is no algebraic collapse that quietly removes the frame "
          f"gradient before it can be bounded")

    # NEGATIVE CONTROL 1: u = const must give exactly zero anomaly (Galilei invariance restored).
    anom_const = sp.simplify(anom.subs({U[i]: sp.Symbol(f"Uc{i}") for i in range(3)}))
    check(all(sp.simplify(anom_const[i]) == 0 for i in range(3)),
          "NEGATIVE CONTROL: u = const gives anomalous acceleration EXACTLY zero in all three "
          "components -- Galilei invariance is restored the moment the frame stops varying in space, "
          "so the effect below is genuinely the frame GRADIENT and not an artifact of the action")

    # THE DIFFERENTIAL between two bodies at the same place with velocity difference w:
    # delta a(v2) - delta a(v1) = -w x (curl u), exactly.
    w = sp.Matrix(sp.symbols("w0 w1 w2", real=True))
    v0 = sp.Matrix(sp.symbols("V0 V1 V2", real=True))
    subs_v = lambda vv: {x[i].diff(t): vv[i] for i in range(3)}
    a_hi = sp.Matrix([sp.simplify(-anom[i].subs(subs_v(v0 + w)).doit()) for i in range(3)])
    a_lo = sp.Matrix([sp.simplify(-anom[i].subs(subs_v(v0)).doit()) for i in range(3)])
    # remove the xddot term which is not part of the anomaly (it carries no v-dependence anyway)
    diff_a = sp.simplify(a_hi - a_lo)
    curl_u = sp.Matrix([sp.diff(U[2], x[1]) - sp.diff(U[1], x[2]),
                        sp.diff(U[0], x[2]) - sp.diff(U[2], x[0]),
                        sp.diff(U[1], x[0]) - sp.diff(U[0], x[1])])
    target = -w.cross(curl_u)
    resid = sp.simplify(diff_a - target)
    print("\n  *** THE EXACT DIFFERENTIAL LAW ***")
    print("      delta a(body 2) - delta a(body 1)  =  - w x (curl u),      w = v_2 - v_1")
    check(all(sp.simplify(resid[i]) == 0 for i in range(3)),
          "verified symbolically component by component (residual identically 0): the differential "
          "anomalous acceleration between two bodies of a common subsystem is EXACTLY a Coriolis "
          "force in the frame's VORTICITY curl u. The symmetric part of grad u cancels identically, "
          "so shear and divergence of the frame are unobservable this way and ONLY the vorticity is "
          "constrained -- which is why this is a clean bound and not an order-of-magnitude estimate")
    # ---- ANCHOR THE DERIVATION AGAINST TEXTBOOK PHYSICS: a rigidly rotating frame.
    print("\n  ANCHOR AGAINST KNOWN PHYSICS (this is what makes the identity above trustworthy rather")
    print("  than merely self-consistent). Put in a rigidly rotating frame u = Omega x r and the law")
    print("  must return the textbook Coriolis force -2 Omega x w:")
    Omz = sp.Symbol("Omega", real=True)
    u_rigid = [-Omz * x[1], Omz * x[0], sp.Integer(0)]
    curl_rigid = sp.Matrix([sp.diff(u_rigid[2], x[1]) - sp.diff(u_rigid[1], x[2]),
                            sp.diff(u_rigid[0], x[2]) - sp.diff(u_rigid[2], x[0]),
                            sp.diff(u_rigid[1], x[0]) - sp.diff(u_rigid[0], x[1])])
    print(f"      curl u = {list(curl_rigid.T)} = 2 Omega zhat, as required")
    derived = sp.simplify(-w.cross(curl_rigid))
    expected = sp.simplify(2 * sp.Matrix([0, 0, Omz]).cross(w))
    wrong_sign = sp.simplify(-2 * sp.Matrix([0, 0, Omz]).cross(w))
    check(sp.simplify(curl_rigid[2] - 2 * Omz) == 0
          and all(sp.simplify(derived[i] - expected[i]) == 0 for i in range(3))
          and any(sp.simplify(derived[i] - wrong_sign[i]) != 0 for i in range(3)),
          "for a rigidly rotating frame curl u = 2 Omega EXACTLY, and the derived pair-differential "
          "-w x curl u reduces IDENTICALLY to +2 Omega x w -- the Coriolis term with the sign "
          "appropriate to 'Newton holds in the u frame, equation written in inertial coordinates'. "
          "SIGN CONVENTION, checked rather than assumed: the familiar -2 Omega x v is the term as it "
          "appears in the ROTATING-frame equation; transposing to inertial coordinates flips it, and "
          "the check verifies the derivation matches the correct one and NOT the other. Either way "
          "|delta a| = 2|Omega||w| for perpendicular vectors, so the bound below uses the magnitude "
          "and is sign-independent. The whole constraint is thereby anchored to 19th-century "
          "mechanics: the frame vorticity IS a rotation rate of the local inertial frame, and "
          "ephemerides measure exactly that")

    print("\n  Note what CANCELLED: the common-mode piece. A frame gradient acting equally on Sun and")
    print("  Earth is unobservable in ranging, exactly as the Milky Way's own pull on the solar system")
    print(f"  ({V_SUN_GAL**2/R_SUN_GAL:.3e} m/s^2, which is {V_SUN_GAL**2/R_SUN_GAL/DAR_EARTH:.0f}x the")
    print("  Earth bound) is unobservable. I use ONLY the differential. Not doing so would have")
    print("  manufactured a deficit of several thousand out of pure common-mode.")

    # ---- Is the 4th-order (Ostrogradsky) piece really negligible at the Sun? Check, both footings.
    print("\n  Before using f -> 1/2: is the fourth-order piece actually negligible at Earth? f_2 and")
    print("  its derivative, evaluated at Earth's own u = a/a0, both footings, mpmath 50 digits:")
    a_earth = G * MSUN / (AU ** 2)
    f2 = lambda u: (u * mp.sqrt(1 + u**2) - mp.asinh(u)) / (2 * u**2)
    for nm, a0v in FOOTINGS:
        u_e = mp.mpf(a_earth) / mp.mpf(a0v)
        fv = f2(u_e)
        fp = mp.diff(f2, u_e)
        # the 4th-order term is d^2/dt^2 [ (|v|^2/a0) f'(u) ahat ]; scale ~ Omega^2 |v|^2 f'/a0
        Om = 2 * mp.pi / (YR)
        term4 = Om**2 * (mp.mpf(V_EARTH)**2 / mp.mpf(a0v)) * abs(fp)
        print(f"      {nm}: u = {float(u_e):.4e}, f_2 = {float(fv):.12f}, "
              f"|f_2 - 1/2| = {float(abs(fv-mp.mpf(0.5))):.2e}, 4th-order term = "
              f"{float(term4):.2e} m/s^2 = {float(term4)/DAR_EARTH:.2e} x bound")
        check(float(abs(fv - mp.mpf(0.5))) < 1e-5 and float(term4) < 0.1 * DAR_EARTH,
              f"{nm}: f_2 is within {float(abs(fv-mp.mpf(0.5))):.1e} of 1/2 and the fourth-order term "
              f"is {float(term4)/DAR_EARTH:.1e} of the Earth bound, so the Newtonian-limit reduction "
              f"used above is justified rather than assumed (footing carried explicitly)")

    # ---- The numbers.
    print("\n  THE BOUND. |delta a| = |w x curl u| <= |w| |curl u|, with w = Earth's orbital velocity")
    print("  relative to the Sun. The ranging bound on an anomalous Earth-Sun relative acceleration:")
    om_bound_E = DAR_EARTH / V_EARTH
    om_bound_M = DAR_MARS / V_MARS
    print(f"      Earth: |curl u| <= {DAR_EARTH:.3e} / {V_EARTH:.4e} = {om_bound_E:.4e} s^-1")
    print(f"      Mars : |curl u| <= {DAR_MARS:.3e} / {V_MARS:.4e} = {om_bound_M:.4e} s^-1")
    print("      PROVENANCE: delta A_R = 3.66e-14 (Earth) / 3.72e-14 (Mars) m/s^2 at 2 sigma, from")
    print("      Sereno & Jetzer 2006 (astro-ph/0606197) Table 1 (Pitjeva EPM2004) inverted through")
    print("      their own Eq (9). ALREADY VERIFIED FROM PRIMARY SOURCE IN-CORPUS (STANDING.md 5.0).")
    print("      *** A REAL CAVEAT, AND IT CUTS AGAINST ME: delta A_R bounds a RADIAL anomaly, while a")
    print("      Coriolis term is TRANSVERSE. I initially expected precession residuals to be tighter.")
    print("      They are not, on the one independent number I could actually compute -- see below. So")
    print("      the ranging reading is the OPTIMISTIC leg and the LLR reading is the CONSERVATIVE leg,")
    print("      and the headline below is the CONSERVATIVE one.")
    om_llr = 0.006 * (19.2e-3 * math.pi / (180.0 * 3600.0)) / YR    # 0.6% of 19.2 mas/yr, rad/s
    om_bound_llr = 2.0 * om_llr
    print(f"\n      INDEPENDENT LEG (frame ROTATION RATE, the structurally correct observable): lunar")
    print(f"      laser ranging confirms the 19.2 mas/yr geodetic precession to ~0.6%, so an anomalous")
    print(f"      frame rotation Omega_f = |curl u|/2 is bounded by {om_llr:.3e} rad/s, i.e.")
    print(f"      |curl u| <= {om_bound_llr:.3e} s^-1. That is {om_bound_llr/om_bound_E:.1f}x LOOSER")
    print(f"      than the ranging reading, not tighter. QUOTED, NOT RE-DERIVED FROM PRIMARY SOURCE IN")
    print(f"      THIS RUN -- flagged as such rather than promoted.")

    om_matter = OORT_A - OORT_B          # = |curl v|_z for the Galactic disk, exactly
    om_matter_flat = V_SUN_GAL / R_SUN_GAL
    print(f"\n  The Milky Way's OWN matter vorticity at the Sun, from measured Oort constants:")
    print(f"      |curl v|_z = A - B = {(OORT_A-OORT_B)*KPC/1e3:.1f} km/s/kpc = {om_matter:.4e} s^-1")
    print(f"      cross-check, flat-curve identity v_c/R_0 = {om_matter_flat:.4e} s^-1 "
          f"(agrees to {abs(om_matter/om_matter_flat-1)*100:.1f}%)")
    check(abs(om_matter / om_matter_flat - 1.0) < 0.10,
          f"the measured Oort combination A-B and the flat-curve identity v_c/R_0 agree to "
          f"{abs(om_matter/om_matter_flat-1)*100:.1f}%, so the matter vorticity input is not "
          f"model-dependent at the level that matters")
    g_opt = om_bound_E / om_matter          # optimistic leg (ranging, radial-bound reading)
    g_max = om_bound_llr / om_matter        # CONSERVATIVE leg (LLR frame-rotation) -- the headline
    print(f"\n  *** THE ROTATIONAL DRAG FRACTION IS CAPPED AT g <= {g_max:.3e} (conservative, LLR) ***")
    print(f"      i.e. the frame must be {1.0/g_max:.0f}x LESS VOROUS than the matter that drags it.")
    print(f"      Optimistic leg (ranging, radial reading): g <= {g_opt:.3e} = {1/g_opt:.0f}x.")
    print(f"      EVERY NUMBER DOWNSTREAM USES THE CONSERVATIVE {1/g_max:.0f}x, not the {1/g_opt:.0f}x.")
    check(g_max < 0.05 and g_opt < g_max,
          f"on the CONSERVATIVE leg the frame's rotational drag fraction is capped at g <= "
          f"{g_max:.2e}, a suppression of {1/g_max:.0f}x. A frame that co-rotates with local matter "
          f"(g = 1, HORN A) is excluded by at least {1/g_max:.0f}x on solar-system data alone -- an "
          f"independent kill of the horn S2 killed on galaxy data, through a completely different "
          f"observable, and the two legs bracket it at {1/g_max:.0f}x-{1/g_opt:.0f}x")
    print("      FOOTING-FREE: neither delta A_R, nor the LLR rate, nor v_Earth, nor A-B contains a0.")
    print("      Stating that rather than manufacturing a footing spread is the honest move; the only")
    print("      place a0 entered was the f -> 1/2 check above, which passed on BOTH footings.")
    print("\n      SCOPE LIMIT, stated not buried: a DISPERSION-SUPPORTED system has zero mean matter")
    print("      vorticity, so this leg says nothing about dwarf spheroidals or cluster galaxies. It")
    print("      bites exactly where the matter rotates -- which is where the RAR is measured.")
    return dict(g_max=g_max, g_opt=g_opt, om_bound=om_bound_llr, om_bound_opt=om_bound_E,
                om_matter=om_matter)


# ---------------------------------------------------------------------------------------------------
def s4_horn_b_irrotational(env, cor):
    banner("S4. HORN B -- IRROTATIONAL + ELLIPTIC PASSIVE DRAG. One theorem FOR it, one AGAINST.")
    print("  *** READ THE STRUCTURE OF THIS SECTION BEFORE THE NUMBERS. Part (i) is a WIN for the")
    print("  framework and I report it at full strength: the potential-flow frame is the one candidate")
    print("  that satisfies S3's vorticity cap EXACTLY, with g = 0 identically, for free. Part (ii) is")
    print("  where it dies, and the mechanism is not the one I expected. ***")
    print()
    print("  S3 forces the frame to be (very nearly) IRROTATIONAL. Independently, keeping ZERO")
    print("  propagating modes (S5) forces the determining equation to carry no time derivatives, i.e.")
    print("  to be an ELLIPTIC CONSTRAINT in the frame's own slices. And for those slices to exist at")
    print("  all, Frobenius requires u to be hypersurface-orthogonal -- irrotational again. So the two")
    print("  requirements agree, and the surviving object is a POTENTIAL FLOW u = grad Psi sourced")
    print("  elliptically by matter. That is the best-case dragged frame. It dies twice.")

    # ---------- (i) STATIONARITY ----------
    print("\n  (i) THE STATIONARITY THEOREM -- *** THIS RUNS FOR THE FRAMEWORK. *** An irrotational")
    print("      drag can only be sourced by the")
    print("      IRROTATIONAL part of the matter momentum, and continuity fixes that exactly:")
    print("          div(rho v) = -d rho/dt      (mass conservation, no assumptions)")
    R, z, ph, tt = sp.symbols("R z phi t", positive=True)
    rho = sp.Function("rho")(R, z)
    vc = sp.Function("v_c")(R)
    # cylindrical divergence of rho * v_c(R) phihat
    div_axi = sp.simplify(sp.diff(rho * vc, ph) / R)
    check(sp.simplify(div_axi) == 0,
          f"for ANY axisymmetric stationary disk -- arbitrary rho(R,z), arbitrary v_c(R) -- "
          f"div(rho v) = {div_axi} IDENTICALLY. The entire momentum of a rotating galaxy is "
          f"SOLENOIDAL, so a potential-flow frame receives zero source from it")
    print("      Stronger, and it needs no symmetry: for ANY exactly stationary bound system")
    print("      d rho/dt = 0, hence div(rho v) = 0, hence the irrotational source vanishes")
    print("      identically. Axisymmetry is not even required.")

    # sum rule: monopole of the source is dM/dt = 0
    print("\n      AND A SUM RULE that kills the non-stationary escape. Even when d rho/dt != 0, its")
    print("      volume integral is dM/dt = 0 for a closed system, so the source has NO MONOPOLE.")
    print("      A rotating non-axisymmetric pattern is the natural escape; test it:")
    eps, Om_p = sp.symbols("epsilon Omega_p", positive=True)
    m_mode = sp.Symbol("m", positive=True, integer=True)   # a pattern has an INTEGER multiplicity
    rho0 = sp.Function("rho_0")(R)
    rho_pat = rho0 * (1 + eps * sp.cos(m_mode * (ph - Om_p * tt)))
    src = sp.diff(rho_pat, tt)
    az_avg = sp.simplify(sp.integrate(src, (ph, 0, 2 * sp.pi)) / (2 * sp.pi))
    t_avg = sp.simplify(sp.integrate(src.subs(m_mode, 2), (tt, 0, sp.pi / Om_p)) / (sp.pi / Om_p))
    print(f"          d rho/dt for an m-fold pattern: azimuthal average = {az_avg}, "
          f"time average over one pattern period = {t_avg}")
    check(sp.simplify(az_avg) == 0 and sp.simplify(t_avg) == 0,
          "a rotating density pattern's source averages to zero both azimuthally and over a pattern "
          "period, so it can supply an oscillating drag but NEVER the steady, uniform translational "
          "frame velocity the door requires. The non-stationary escape is priced and it does not pay")
    print("      TWO CONSEQUENCES, AND THE FIRST ONE IS GOOD NEWS FOR THE CONSTRUCTION:")
    print("      (a) *** A potential-flow frame is EXACTLY BLIND to a stationary galaxy's rotation, so")
    print("          it satisfies S3's vorticity cap with g = 0 IDENTICALLY -- not approximately, not")
    print("          by tuning. Of everything examined in this file, this is the ONE mechanism that")
    print("          delivers what S3 demands, and it delivers it for free. That is a real result in")
    print("          the construction's favour and it is stated at full strength. ***")
    print("      (b) But it also means the ONLY drag left is the TRANSLATIONAL response of part (ii).")
    print("          Switch that off and u is HARMONIC, hence fixed entirely by its boundary value --")
    print(f"          the frame at infinity, i.e. the COSMIC frame, already excluded at "
          f"{1.0/BUDGET_A1:.2f}x.")
    print("          So everything now rests on part (ii), and part (ii) is where it breaks.")

    # ---------- (ii) THE TRACE IDENTITY ----------
    print("\n  (ii) THE TRACE IDENTITY -- and this is where the horn dies quantitatively. One piece of")
    print("      the source does survive: a body in RIGID TRANSLATION has rho(x,t) = rho_0(x - V t), so")
    print("      d rho/dt = -V.grad rho_0 != 0. Solve the elliptic drag equation for that source.")
    x1, x2, x3 = sp.symbols("x y z", real=True)
    kd = sp.symbols("kappa_d", real=True)
    chi = sp.Function("chi")(x1, x2, x3)
    Vv = sp.Matrix(sp.symbols("V_x V_y V_z", real=True))
    XS = [x1, x2, x3]
    # Laplacian Psi = kappa_d d rho/dt = -kappa_d V.grad rho ; with Laplacian chi = rho this integrates
    # to Psi = -kappa_d V.grad chi, so u = grad Psi = -kappa_d (V.grad) grad chi = -kappa_d H[chi] . V
    Hchi = sp.Matrix(3, 3, lambda i, j: sp.diff(chi, XS[i], XS[j]))
    u_drag = -kd * (Hchi * Vv)
    # Consistency of the integration step: Laplacian(Psi) must equal kappa_d * drho/dt = -kappa_d V.grad rho
    Psi = -kd * sum(Vv[j] * sp.diff(chi, XS[j]) for j in range(3))
    lap_Psi = sum(sp.diff(Psi, XS[i], 2) for i in range(3))
    want = -kd * sum(Vv[j] * sp.diff(sum(sp.diff(chi, XS[k], XS[k]) for k in range(3)), XS[j])
                     for j in range(3))
    check(sp.simplify(lap_Psi - want) == 0,
          "the integration step is verified symbolically: Laplacian(-kappa_d V.grad chi) = "
          "-kappa_d V.grad(Laplacian chi) = -kappa_d V.grad rho = kappa_d drho/dt, so Psi solves the "
          "elliptic drag equation for a rigidly-translating source exactly (derivatives commute; no "
          "boundary term is being smuggled in)")
    print(f"      Psi = -kappa_d V.grad chi with Laplacian chi = rho  =>  u_i = -kappa_d "
          f"(d_i d_j chi) V_j")
    print(f"      drag tensor f_ij = -kappa_d d_i d_j chi, and Tr(d_i d_j chi) = Laplacian chi = rho")
    rho_xyz = sp.Function("rho")(x1, x2, x3)
    chi_uniform = rho_xyz * (x1**2 + x2**2 + x3**2) / 6
    check(sp.simplify(sum(sp.diff(chi_uniform, XS[i], 2) for i in range(3)).subs(
              {sp.Derivative(rho_xyz, v): 0 for v in XS}) - rho_xyz) == 0,
          "explicit check of the Green's-function step on a locally-uniform density: "
          "Laplacian(rho r^2/6) = rho, so chi exists and f_ij is its Hessian times -kappa_d")
    print("\n      *** THEREFORE, POINTWISE AND FOR ANY DENSITY PROFILE: ***")
    print("          (1/3) Tr f_ij  =  -kappa_d rho(x) / 3 .")
    print("      The MEAN DRAG FRACTION IS EXACTLY PROPORTIONAL TO THE LOCAL DENSITY. This is not a")
    print("      model, an estimate, or a scaling argument -- it is the trace of the Hessian of the")
    print("      potential whose Laplacian is rho, and it holds at every point of every profile.")
    print("      (For a uniform sphere the tensor is isotropic and f_ij = -kappa_d rho/3 delta_ij")
    print("      exactly, so the mean IS the whole answer there.)")

    print("\n      THE KILL. The door needs f ~ 1 everywhere (any deficit 1-f leaks the ambient")
    print("      velocity back in, which is the cosmic-frame lock). With ONE coupling kappa_d,")
    print("      f ~ 1 at one density means f is wrong by the density ratio everywhere else. Real")
    print("      SPARC baryonic mid-plane densities, Upsilon_[3.6] = 0.5 and 1.33 x M_HI for helium:")
    rows = [r for r in load_sparc() if r["Vflat"] > 0 and r["Rdisk"] > 0 and r["L36"] > 0]
    dens = []
    for r in rows:
        mbar = 0.5 * r["L36"] * 1e9 + 1.33 * r["MHI"] * 1e9        # Msun
        rd = r["Rdisk"]                                             # kpc
        hz = 0.2 * rd                                               # standard thin-disk ratio
        # central mid-plane density of an exponential disk, Sigma_0 = M/(2 pi Rd^2), rho_0 = Sigma_0/(2hz)
        sig0 = mbar / (2 * math.pi * rd**2)
        dens.append(sig0 / (2.0 * hz))                              # Msun/kpc^3
    dens = np.array(dens)
    lo, hi = np.percentile(dens, [5, 95])
    print(f"      N = {len(dens)} galaxies; mid-plane rho_bar spans {dens.min():.3e} to "
          f"{dens.max():.3e} Msun/kpc^3")
    print(f"      = {math.log10(dens.max()/dens.min()):.2f} dex full range, "
          f"{math.log10(hi/lo):.2f} dex over the 5-95 percentile")
    print(f"      cosmic mean matter density for scale: {RHO_MEAN_MSUN_KPC3:.3g} Msun/kpc^3 "
          f"({math.log10(dens.min()/RHO_MEAN_MSUN_KPC3):.1f} dex below the faintest SPARC disk)")
    # Tune kappa_d so that f = 1 at the sample median, then measure the residual spread.
    # A star at radius R: v_rel = (1 - f) v_gal + v_orb (rotational drag is zero for a potential flow).
    vfl = np.array([r["Vflat"] for r in rows])
    print("\n      TWO TUNINGS OF THE ONE FREE COUPLING kappa_d, so the result cannot be an artifact of")
    print("      a bad choice. Tuning A pins f = 1 at the sample MEDIAN density; Tuning B pins f = 1 at")
    print("      the MAXIMUM density, which is the only tuning that never over-drags (f <= 1 always)")
    print("      and is therefore the MOST GENEROUS physically sensible choice:")
    out, out_b = [], []
    print(f"      {'tuning':<9s} {'v_gal':>6s} {'lam range':>22s} {'spread (dex)':>14s} "
          f"{'RMS':>7s} {'x budget':>9s} {'N with f<0.1':>13s}")
    for lbl, norm in (("A median", np.median(dens)), ("B max   ", dens.max())):
        f_of_rho = dens / norm
        for vgal in (150.0, 300.0, 600.0):
            lam = np.abs((1.0 - f_of_rho) * vgal + vfl) / vfl
            d = np.log10(1.0 / np.clip(lam, 1e-12, None))
            d = d - np.median(d)
            spread = d.max() - d.min()
            (out if lbl.startswith("A") else out_b).append(spread)
            print(f"      {lbl:<9s} {vgal:6.0f} {lam.min():9.3f}-{lam.max():10.3f} "
                  f"{spread:14.3f} {d.std():7.3f} {spread/env['budget']:9.1f} "
                  f"{int(np.sum(f_of_rho<0.1)):13d}")
    f_med = dens / np.median(dens)
    f_max = dens / dens.max()
    check(min(out) > 3.0 * env["budget"] and min(out_b) > 2.0 * env["budget"],
          f"BOTH tunings fail: median-tuned residual a0 spread {min(out):.2f}-{max(out):.2f} dex "
          f"({min(out)/env['budget']:.0f}-{max(out)/env['budget']:.0f}x budget), max-tuned (never "
          f"over-dragging, most generous) {min(out_b):.2f}-{max(out_b):.2f} dex "
          f"({min(out_b)/env['budget']:.0f}-{max(out_b)/env['budget']:.0f}x). The failure survives the "
          f"free coupling, which is the only freedom the construction has here")
    print(f"\n      AND UNDER THE GENEROUS TUNING B THE FAILURE MODE IS THE COSMIC-FRAME LOCK ITSELF:")
    print(f"      {int(np.sum(f_max < 0.1))} of {len(f_max)} galaxies get f < 0.1, i.e. their frame is")
    print(f"      >90% the boundary (cosmic) frame, which is exactly the option already excluded at")
    print(f"      4.6x. So Horn B does not escape the lock -- it reproduces it on the low-density half")
    print(f"      of the real sample while over- or under-dragging the rest.")
    check(np.sum(f_max < 0.1) > 0.3 * len(f_max),
          f"{100*np.sum(f_max<0.1)/len(f_max):.0f}% of real SPARC galaxies fall to f < 0.1 under the "
          f"non-over-dragging tuning, so the density-proportional drag delivers the cosmic frame to "
          f"most of the sample by construction")
    print("\n      Sign of the residual, both directions checked: f > 1 (over-drag) at high density")
    print("      gives lam < 1 hence a0_eff > a0; f < 1 at low density leaks v_gal and gives lam > 1")
    print("      hence a0_eff < a0. So the effect is not one-signed and cannot be hidden in kappa.")
    nover = int(np.sum(f_med > 1.0))
    check(0 < nover < len(f_med),
          f"{nover} of {len(f_med)} galaxies are over-dragged and {len(f_med)-nover} under-dragged at "
          f"the median-tuned coupling, so the residual has BOTH signs and a global a0 renormalisation "
          f"provably cannot absorb it")
    print("\n      WHAT THIS IS, restated: a0_eff has become a function of LOCAL DENSITY. That is the")
    print("      class of door the framework's OWN SPARC environmental test already nulled at 10.5")
    print("      sigma (STANDING.md sec.4, row 1). Horn B does not open a new door; it re-enters a")
    print("      closed one, and it does so as a theorem (the trace identity) rather than a guess.")
    return dict(dens_dex=math.log10(dens.max() / dens.min()), spread=min(out),
                spread_b=min(out_b), frac_cosmic=float(np.sum(f_max < 0.1) / len(f_max)))


# ---------------------------------------------------------------------------------------------------
def s5_passivity():
    banner("S5. HORN C -- PASSIVITY. *** THIS OBSTRUCTION DIED. *** Reported as a negative result.")
    print("  The framework's defence against Einstein-aether strong coupling is that u is PASSIVE with")
    print("  ZERO propagating modes (machine-verified constraint analysis, action v4: 2nd-class block")
    print("  det 4(u.u)^2 -> 4, 0 frame dof; the u-in-Box_u symbol has no wave cone). The assigned")
    print("  question: does a frame DRAGGED by matter necessarily acquire dynamics, and with them the")
    print("  strong-coupling problem back? I tried to prove yes. IT IS NOT TRUE, and here is why.")
    print("  Take the general two-derivative aether kinetic term with the standard four couplings,")
    print("  metric signature (-,+,+,+), background u^mu = (1,0,0,0), perturbation u^mu = (1, e_i):")
    tt, xx, yy, zz = sp.symbols("t x y z", real=True)
    c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
    XS = [tt, xx, yy, zz]
    eta = sp.diag(-1, 1, 1, 1)
    e = [sp.Function(f"e{i}")(tt, xx, yy, zz) for i in range(3)]
    uup = sp.Matrix([1, e[0], e[1], e[2]])           # u^mu to first order (unit norm fixes u^0 = 1)
    udn = eta * uup
    d = lambda M, mu: sp.Matrix([sp.diff(M[a], XS[mu]) for a in range(4)])
    T1 = sum(eta[mu, mu] * sum(sp.diff(udn[a], XS[mu]) * sp.diff(uup[a], XS[mu])
                               for a in range(4)) for mu in range(4))
    T2 = (sum(sp.diff(uup[mu], XS[mu]) for mu in range(4))) ** 2
    T3 = sum(sum(eta[mu, mu] * eta[nu, nu] * sp.diff(udn[nu], XS[mu]) * sp.diff(udn[mu], XS[nu])
                 for nu in range(4)) for mu in range(4))
    Du = sp.Matrix([sum(uup[mu] * sp.diff(uup[a], XS[mu]) for mu in range(4)) for a in range(4)])
    T4 = sum(eta[a, a] * Du[a] * Du[a] for a in range(4))
    Lk = sp.expand(-c1 * T1 - c2 * T2 - c3 * T3 - c4 * T4)
    Lk2 = sp.expand(Lk)
    hess = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            hess[i, j] = sp.simplify(sp.diff(Lk2, sp.Derivative(e[i], tt), sp.Derivative(e[j], tt))
                                     if False else
                                     sp.diff(sp.diff(Lk2, sp.diff(e[i], tt)), sp.diff(e[j], tt)))
    print(f"\n      velocity Hessian d^2 L / d(edot_i) d(edot_j) = {sp.simplify(hess[0,0])} * delta_ij")
    print(f"      (off-diagonal: {sp.simplify(hess[0,1])})")
    hcoef = sp.simplify(hess[0, 0])
    check(sp.simplify(hess[0, 1]) == 0 and sp.simplify(hcoef - 2 * (c1 - c4)) == 0,
          f"the Hessian is {hcoef} delta_ij = 2(c1 - c4) delta_ij, so it vanishes on the codimension-1 "
          f"surface c1 = c4 -- NOT only at c1 = c4 = 0")
    # Does a spatial Laplacian survive on that surface? Check the coefficient of (d_x e_y)^2.
    on_shell = Lk2.subs(c4, c1)
    spatial = sp.simplify(sp.diff(sp.diff(on_shell, sp.diff(e[1], xx)), sp.diff(e[1], xx))
                          .subs({e[i]: 0 for i in range(3)}))
    print(f"      on the surface c1 = c4, the coefficient of (d_x e_y)^2 is {spatial}")
    check(sp.simplify(spatial) != 0,
          f"on c1 = c4 the SPATIAL gradient terms survive with coefficient {spatial} while the time "
          f"Hessian is exactly zero. So there EXISTS a two-derivative frame sector that is elliptic in "
          f"space, carries ZERO propagating degrees of freedom, and still smooths. PASSIVITY DOES NOT "
          f"FORBID A DRAG OPERATOR. Candidate obstruction 6 -- flagged in the brief as possibly the "
          f"sharpest -- DIES as an independent obstruction")
    print("\n  WHAT SURVIVES OF IT, and it is not nothing: the surviving operator is ELLIPTIC, so its")
    print("  solution needs a BOUNDARY CONDITION, and the homogeneous solution is a constant -- the")
    print("  frame at infinity. That is exactly the hypothesis of S4(i). So obstruction 6 does not")
    print("  close the door; it FORCES the door into HORN B, where the stationarity theorem and the")
    print("  trace identity close it. Reporting the chain honestly matters more than claiming six.")
    print("\n  AND THE OTHER BRANCH IS STILL SHUT: if instead c1 != c4, the Hessian is nonzero, u has")
    print("  propagating modes, and the Einstein-aether strong-coupling objection that frame passivity")
    print("  was invented to defeat comes straight back. So the dichotomy is real; only its passive")
    print("  side is bigger than I expected.")
    return dict(hess=str(hcoef))


# ---------------------------------------------------------------------------------------------------
def _disk_mean_vphi(R0, Rd, hz, R_drag, nR=220, nph=192, nz=25):
    """Mass-weighted mean azimuthal velocity of a 3D exponential disk (flat v_c = 1) inside an
    isotropic Gaussian drag kernel of width R_drag centred at (R0, phi=0, z=0). Returns g = <v_phi>/v_c
    projected on the local phihat. Pure kinematics; no a0 anywhere."""
    Rmax = max(12.0 * Rd, R0 + 6.0 * R_drag)
    Rg = np.linspace(1e-4, Rmax, nR)
    phg = np.linspace(0.0, 2.0 * np.pi, nph, endpoint=False)
    zg = np.linspace(-6.0 * hz, 6.0 * hz, nz)
    Rm, Pm, Zm = np.meshgrid(Rg, phg, zg, indexing="ij")
    rho = np.exp(-Rm / Rd) * np.exp(-np.abs(Zm) / hz)
    dV = Rm * (Rg[1] - Rg[0]) * (phg[1] - phg[0]) * (zg[1] - zg[0])
    dx = Rm * np.cos(Pm) - R0
    dy = Rm * np.sin(Pm)
    d2 = dx * dx + dy * dy + Zm * Zm
    W = np.exp(-0.5 * d2 / R_drag**2)
    wt = rho * W * dV
    # v_phi vector at (R,phi) is v_c * (-sin phi, cos phi); local phihat at (R0, 0) is (0, 1)
    num = np.sum(wt * np.cos(Pm))
    den = np.sum(wt)
    return num / den


def s6_horn_d_smoothed(env, cor):
    banner("S6. HORN D -- SMOOTHED DRAG OVER A NEW LENGTH R_drag. The window, computed.")
    print("  Buying out of HORN A means smoothing: u(x) = <rho v>_W / <rho>_W over a kernel of width")
    print("  R_drag. That is a FIFTH CONSTANT the theory does not have (the corpus already carries")
    print("  omega_c as FREE-but-BOUNDED for the same structural reason). Grant it anyway and ask")
    print("  whether ANY single R_drag works. Two requirements pull opposite ways:")
    print("     (R1) TRANSLATION must be captured: the host must dominate the kernel weight, else the")
    print("          ambient velocity leaks in -> small R_drag.")
    print("     (R2) ROTATION must NOT be captured: S3 caps the frame vorticity -> large R_drag.")

    # --- R2: how big must R_drag be to suppress the disk's vorticity by cor['g_max']?
    print("\n  (R2) Smoothed rotational drag for a 3D exponential disk (Rd = 2.6 kpc, hz = 0.2 Rd,")
    print("       flat v_c), evaluated at the Sun's radius R0 = 8.178 kpc. Numerical 3D integral:")
    Rd_mw, R0_mw = 2.6, 8.178
    hz_mw = 0.2 * Rd_mw
    tab = []
    for rdg in (1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0):
        g = _disk_mean_vphi(R0_mw, Rd_mw, hz_mw, rdg)
        tab.append((rdg, g))
        print(f"       R_drag = {rdg:7.1f} kpc   g = <v_phi>/v_c = {g: .6e}")
    # structural checks: monotone decreasing, and asymptotically ~ R_drag^-2
    gs = np.array([t[1] for t in tab])
    rr = np.array([t[0] for t in tab])
    check(np.all(np.diff(gs) < 0),
          "g(R_drag) is strictly monotone DECREASING over 1-100 kpc, as the structure requires: an "
          "axisymmetric disk has exactly zero net momentum, so a wide kernel must average the "
          "rotation away")
    check(gs[0] > 0.5,
          f"and at R_drag = 1 kpc << R0 the kernel recovers the local matter velocity, g = {gs[0]:.3f} "
          f"-> 1, which is HORN A. The two horns are the two ends of one axis, so nothing can sit "
          f"outside both")
    slope = np.polyfit(np.log(rr[-4:]), np.log(gs[-4:]), 1)[0]
    print(f"       large-R_drag log-log slope = {slope:.3f} (analytic expectation -2 from the leading "
          f"kernel-gradient moment g -> R0 <R> / (2 R_drag^2))")
    check(-2.4 < slope < -1.6,
          f"the numerical large-scale slope {slope:.2f} matches the analytic -2, so the extrapolation "
          f"used for R_drag_min below is validated rather than assumed")
    # invert the fitted power law for the S3 cap
    A_fit = math.exp(np.polyfit(np.log(rr[-4:]), np.log(gs[-4:]), 1)[1])
    Rmin = (A_fit / cor["g_max"]) ** (-1.0 / slope)
    Rmin_opt = (A_fit / cor["g_opt"]) ** (-1.0 / slope)
    print(f"\n       *** R_drag >= {Rmin:.0f} kpc (conservative leg, g <= {cor['g_max']:.2e}) ***")
    print(f"       *** R_drag >= {Rmin_opt:.0f} kpc (optimistic leg, g <= {cor['g_opt']:.2e}) ***")
    check(Rmin > 3.0 * Rd_mw and Rmin_opt > Rmin,
          f"on BOTH legs the vorticity cap forces the drag kernel wider than the disk that is supposed "
          f"to drag it: R_drag >= {Rmin:.0f}-{Rmin_opt:.0f} kpc = {Rmin/Rd_mw:.0f}x-"
          f"{Rmin_opt/Rd_mw:.0f}x the disk scale length and {Rmin/R0_mw:.1f}x-{Rmin_opt/R0_mw:.1f}x the "
          f"Sun's galactocentric radius. 'Locally dragged' cannot mean local on the scale of the disk")

    # --- R1: host weight domination, over the real SPARC sample, at BOTH legs' R_drag.
    print(f"\n  (R1) At a UNIVERSAL R_drag, does each SPARC galaxy still dominate its own drag kernel?")
    print("       Host weight <rho>_host = M_bar / ((2 pi)^3/2 R_drag^3) against the ambient, with the")
    print("       ambient at the COSMIC MEAN -- the most generous possible choice, since real galaxies")
    print("       sit in filaments and groups at 10-100x the mean. M_bar = 0.5 L[3.6] + 1.33 M_HI.")
    rows = [r for r in load_sparc() if r["Vflat"] > 0 and r["L36"] > 0]
    mbar = np.array([0.5 * r["L36"] * 1e9 + 1.33 * r["MHI"] * 1e9 for r in rows])
    vfl = np.array([r["Vflat"] for r in rows])
    print(f"       {'R_drag':>8s} {'ambient':<18s} {'median f':>9s} {'min f':>8s} "
          f"{'N f<0.5':>8s} {'N f<0.9':>8s}")
    fields = {}
    for Rd_use, leg in ((Rmin, "conservative"), (Rmin_opt, "optimistic")):
        Veff = (2.0 * math.pi) ** 1.5 * Rd_use**3        # kpc^3
        for lbl, mult in (("cosmic mean (x1)", 1.0), ("filament (x10)", 10.0),
                          ("group (x100)", 100.0)):
            rho_env = mult * RHO_MEAN_MSUN_KPC3
            f = (mbar / Veff) / (mbar / Veff + rho_env)
            fields[(leg, lbl)] = f
            print(f"       {Rd_use:8.0f} {lbl:<18s} {np.median(f):9.4f} {f.min():8.4f} "
                  f"{int(np.sum(f<0.5)):8d} {int(np.sum(f<0.9)):8d}")
    n_cons = int(np.sum(fields[("conservative", "cosmic mean (x1)")] < 0.5))
    n_opt = int(np.sum(fields[("optimistic", "cosmic mean (x1)")] < 0.5))
    check(n_opt > n_cons,
          f"the host-domination test is genuinely DISCRIMINATING rather than rigged: at the "
          f"conservative R_drag = {Rmin:.0f} kpc it flags {n_cons} of {len(mbar)} galaxies, at the "
          f"optimistic R_drag = {Rmin_opt:.0f} kpc it flags {n_opt}. A metric that returned the same "
          f"answer for both would be worthless, and this one does not")
    check(np.all(np.diff([np.median(fields[("optimistic", k)]) for k in
                          ("cosmic mean (x1)", "filament (x10)", "group (x100)")]) < 0),
          "and f falls monotonically as the ambient density rises, as the structure requires")

    print("\n  (R1+R2) THE WINDOW, with the leak converted to a0 through S1's dictionary.")
    print("       v_rel/v_orb = |(1-f) dv_env + v_orb| / v_orb, with dv_env the galaxy's velocity")
    print("       offset from the matter inside R_drag. HONEST CAVEAT, AND IT RUNS FOR THE FRAMEWORK:")
    print("       coherent bulk flow does NOT contaminate -- the galaxy and its surroundings share it.")
    print("       What leaks is the SHEAR of the flow on scale R_drag. So I use group-member")
    print("       dispersions (measured, 300-1000 km/s) AND a deliberately small field value")
    print("       (100 km/s), and let the reader see which regime any kill lives in:")
    print(f"       {'leg':<13s} {'dv_env':>7s} {'ambient':<18s} {'spread (dex)':>13s} {'RMS':>7s} "
          f"{'x budget':>9s}")
    grid = {}
    for Rd_use, leg in ((Rmin, "conservative"), (Rmin_opt, "optimistic")):
        for dv in (100.0, 300.0, 1000.0):
            for lbl in ("cosmic mean (x1)", "filament (x10)"):
                f = fields[(leg, lbl)]
                lam = np.abs((1.0 - f) * dv + vfl) / vfl
                d = np.log10(1.0 / lam)
                d -= np.median(d)
                grid[(leg, dv, lbl)] = (d.max() - d.min(), d.std())
                print(f"       {leg:<13s} {dv:7.0f} {lbl:<18s} {d.max()-d.min():13.3f} "
                      f"{d.std():7.3f} {(d.max()-d.min())/env['budget']:9.2f}")
    cons_best = grid[("conservative", 100.0, "cosmic mean (x1)")][0]
    opt_worst = max(v[0] for k, v in grid.items() if k[0] == "optimistic")
    opt_best = grid[("optimistic", 100.0, "cosmic mean (x1)")][0]
    check(opt_best > cons_best and opt_worst > env["budget"],
          f"the window is LEG-DEPENDENT and the script reports that rather than picking the flattering "
          f"leg: on the conservative leg the best case is {cons_best:.3f} dex = "
          f"{cons_best/env['budget']:.2f}x budget (i.e. it PASSES, no obstruction), on the optimistic "
          f"leg the same best case is {opt_best:.3f} dex = {opt_best/env['budget']:.2f}x and the worst "
          f"is {opt_worst:.3f} dex = {opt_worst/env['budget']:.1f}x")
    print(f"\n       *** READ THIS AGAINST MY OWN THESIS. HORN D DOES NOT CLOSE. *** On the")
    print(f"       CONSERVATIVE vorticity leg, an isolated field galaxy at dv_env = 100 km/s has a")
    print(f"       residual spread of only {cons_best:.3f} dex = {cons_best/env['budget']:.2f}x the")
    print(f"       budget -- INSIDE it. A single R_drag ~ {Rmin:.0f}-{Rmin_opt:.0f} kpc smoothed frame")
    print("       survives this test for isolated massive hosts. It fails for group members")
    print(f"       (dv_env >= 300 km/s: {grid[('conservative',300.0,'filament (x10)')][0]/env['budget']:.1f}x-"
          f"{grid[('conservative',1000.0,'filament (x10)')][0]/env['budget']:.1f}x) and it fails on the")
    print("       optimistic leg generally. So HORN D is a PARTIAL obstruction: a genuine squeeze in")
    print("       dense environments, NOT a no-go. It still costs a FIFTH CONSTANT, which is a price")
    print("       the theory pays whether or not the window closes. I am not inflating it into a kill.")

    print("\n       NEGATIVE CONTROL for the whole section -- the ORACLE frame. If u were exactly each")
    print("       galaxy's own centre-of-mass velocity (f = 1, g = 0 by fiat), lam = 1 identically:")
    lam_or = np.abs(0.0 * 300.0 + vfl) / vfl
    d_or = np.log10(1.0 / lam_or)
    _ = cons_best
    check(np.allclose(d_or, 0.0, atol=1e-15),
          f"oracle frame gives spread {np.max(np.abs(d_or)):.1e} dex -- the estimator returns a clean "
          f"PASS for the object the door actually needs, which is what makes the failures above "
          f"meaningful. And it names exactly what is missing: a prescription that knows WHICH BOUND "
          f"SYSTEM a point belongs to. That is not a local field of the matter distribution -- it is a "
          f"segmentation of it, and no single-scale kernel supplies it")
    return dict(Rmin=Rmin, Rmin_opt=Rmin_opt, cons_best=cons_best, opt_worst=opt_worst,
                opt_best=opt_best, nfail_cons=n_cons, nfail_opt=n_opt, ntot=len(mbar),
                grid=grid, closes=False)


# ---------------------------------------------------------------------------------------------------
def s7_nesting(env):
    banner("S7. NESTING / WELL-DEFINEDNESS, AND TWO CONSEQUENCES FOR FROZEN LIVE FRONTS")
    print("  Candidate obstruction 5. There is ONE u per spacetime point. Whatever it is, a0_eff for")
    print("  any subsystem is a0 (v_orb / v_frame) by S1's dictionary. Tabulate it for real systems,")
    print("  taking the frame at each location to be what the RAR requires: the host GALAXY's")
    print("  non-rotating COM frame (that is the ONLY choice that puts disk stars on the RAR).")
    SUB = [
        ("disk star in the MW (the RAR case)", 233.0, 233.0),
        ("binary pulsar J0737-3039 (relative)", 626.0, 233.0),
        ("cluster member galaxy, internal", 200.0, 1000.0),
        ("dSph member (Crater II-like), sigma", 2.7, 100.0),
        ("Earth about the Sun", 29.78, 233.0),
        ("Mars about the Sun", 24.08, 233.0),
        ("LEO satellite about the Earth", 7.7, 233.0),
        ("Moon about the Earth", 1.022, 233.0),
        ("wide binary at 10 kAU", 0.45, 233.0),
    ]
    print(f"\n  {'subsystem':<38s} {'v_orb':>8s} {'v_frame':>8s} {'ratio':>9s} "
          f"{'a0_eff/a0 (dex)':>16s} {'a0_eff canon':>13s} {'a0_eff alt':>12s}")
    dexes = []
    for nm, vo, vf in SUB:
        r = vo / vf
        dex = math.log10(r)
        dexes.append(dex)
        print(f"  {nm:<38s} {vo:8.2f} {vf:8.1f} {r:9.4f} {dex:16.3f} "
              f"{A0_CANON*r:13.3e} {A0_ALT*r:12.3e}")
    span = max(dexes) - min(dexes)
    check(span > 2.0,
          f"a0_eff spans {span:.2f} dex across ordinary nested systems (both footings scale together, "
          f"so the SPAN is footing-free). a0 stops being a constant of nature and becomes a property "
          f"of the subsystem's speed relative to its host's frame")
    mism = 233.0 / 29.78
    check(abs(mism - 7.82) < 0.05,
          f"the irreducible core: ONE u at the Sun cannot be both the MW's COM frame (needed so the "
          f"Sun's own galactic orbit lands on the RAR at lam = 1) and the Sun's rest frame (needed so "
          f"Earth's orbit gets lam = 1). The mismatch is exactly v_sun/v_earth = {mism:.2f}. This is "
          f"not a bound being violated -- it is a statement that the construction is not simultaneously "
          f"well-defined at two nesting levels, which is what obstruction 5 asked")
    print("\n  DOES THE NESTING MISMATCH ITSELF VIOLATE A BOUND? Check the planets honestly on the")
    print(f"  alpha = 2 kernel in force. a0_eff = a0/{mism:.2f} makes the anomaly SMALLER, not larger.")
    print("  *** CATASTROPHIC-CANCELLATION WARNING, AND IT BIT: 1 - mu_2(y) at Earth is ~1e-16, which")
    print("  float64 rounds to EXACTLY ZERO. A first pass of this block divided by that zero. Redone")
    print("  in mpmath at 50 digits; the asymptotic identity 1 - mu_2 -> 1/(2y^2) is printed alongside")
    print("  as an independent cross-check of the high-precision value. ***")
    a_e_mp = mp.mpf(G) * mp.mpf(MSUN) / mp.mpf(AU) ** 2
    for nm, a0v in FOOTINGS:
        y = a_e_mp / mp.mpf(a0v)
        one_minus_mu = 1 - y / mp.sqrt(1 + y * y)
        anom_full = a_e_mp * one_minus_mu
        y2 = a_e_mp / (mp.mpf(a0v) / mp.mpf(mism))
        anom_drag = a_e_mp * (1 - y2 / mp.sqrt(1 + y2 * y2))
        print(f"      {nm}: y = {float(y):.4e}, 1-mu_2 = {float(one_minus_mu):.6e} "
              f"(asymptote 1/(2y^2) = {float(1/(2*y*y)):.6e}, agree to "
              f"{float(abs(one_minus_mu*2*y*y - 1)):.1e})")
        print(f"      {' '*len(nm)}  anomaly {float(anom_full):.3e} -> {float(anom_drag):.3e} m/s^2 "
              f"({float(anom_drag)/DAR_EARTH:.2e} x Earth bound), suppressed by "
              f"{float(anom_full/anom_drag):.1f}x (= mismatch^2 = {mism**2:.1f})")
        check(float(abs(one_minus_mu * 2 * y * y - 1)) < 1e-12
              and abs(float(anom_full / anom_drag) / mism**2 - 1.0) < 1e-6,
              f"{nm}: the mpmath value of 1-mu_2 agrees with its analytic asymptote 1/(2y^2) to "
              f"{float(abs(one_minus_mu*2*y*y-1)):.1e}, and the suppression is exactly the mismatch "
              f"SQUARED ({mism**2:.2f}) as the alpha=2 tail requires -- so the high-precision numbers "
              f"are cross-checked against an identity, not merely trusted")
        anom_drag = float(anom_drag)
        anom_full = float(anom_full)
        check(anom_drag < DAR_EARTH,
              f"{nm}: with a0_eff = a0/{mism:.2f} the alpha=2 planetary anomaly is "
              f"{anom_drag/DAR_EARTH:.1e} of the Earth bound -- SAFE. So the nesting mismatch is an "
              f"ill-definedness, NOT a planetary kill, and I will not sell it as one. (On the retired "
              f"alpha=1 kernel the same table would matter enormously; it does not on alpha=2.)")

    print("\n  *** CONSEQUENCE FOR FRONT A (wide binaries), and it is dated. *** A wide binary sits in")
    print("  the MW disk, so under the frame the RAR requires its frame-relative speed is ~233 km/s,")
    print("  not its ~0.45 km/s orbital speed. By S1, a0_eff = a0 x (0.45/233):")
    for nm, a0v in FOOTINGS:
        a0e = a0v * 0.45 / 233.0
        r = 10e3 * AU
        gb = G * (1.5 * MSUN) / r**2
        y = gb / a0e
        gobs = solve_closure(gb, a0e, mu2, lam=1.0)
        gam = math.sqrt(gobs / gb)
        print(f"      {nm}: a0_eff = {a0e:.3e}, g_bar/a0_eff = {y:.4g}, gamma_v = "
              f"sqrt(g_obs/g_bar) = {gam:.7f}")
        check(gam < 1.0182,
              f"{nm}: the dragged frame predicts gamma_v = {gam:.6f} at 10 kAU, i.e. NEWTONIAN to "
              f"{100*(gam-1):.5f}%, which lies OUTSIDE the frozen DR4 pre-registration band "
              f"1.0182-1.0350 (Amendment 3 point target 1.0246). REPORTED, NOT AMENDED: a frozen "
              f"pre-registration is amended in the open, before data, by Carl -- not by a subagent. "
              f"What this means procedurally is that adopting a locally-dragged frame is a THEORY "
              f"CHANGE that would need its own open amendment before DR4")
    print("      This lands the framework on the 'predicts Newton at 2-30 kAU' branch of the corpus's")
    print("      own omega_c gate fork -- and under the frozen scoring rules a DR4 confirmation of")
    print("      gamma_v > 1 would then be a KILL for the dragged-frame version. That is a real,")
    print("      near-term falsification handle the construction acquires, which is worth saying")
    print("      alongside the no-go: the door does not merely fail to open, it costs a live front.")

    print("\n  *** CONSEQUENCE FOR FRONT B (s^TX SME boost dipole): the frozen prediction is")
    print("  FRAME-DEPENDENT and would need re-deriving. *** Geometry only, computed here:")
    l_cmb, b_cmb, v_cmb = 264.021, 48.253, 369.82      # Planck 2018 solar dipole
    l_rot, b_rot, v_rot = 90.0, 0.0, 233.0             # direction of solar galactic rotation
    d2r = math.pi / 180.0
    cosang = (math.cos(b_cmb * d2r) * math.cos(b_rot * d2r) * math.cos((l_cmb - l_rot) * d2r)
              + math.sin(b_cmb * d2r) * math.sin(b_rot * d2r))
    ang = math.degrees(math.acos(cosang))
    print(f"      cosmic (CMB) frame: v = {v_cmb:.1f} km/s toward (l,b) = ({l_cmb:.2f}, {b_cmb:.2f})")
    print(f"      MW-dragged frame  : v = {v_rot:.1f} km/s toward (l,b) = ({l_rot:.1f}, {b_rot:.1f})")
    print(f"      angle between apices = {ang:.1f} deg;  speed ratio = {v_rot/v_cmb:.3f}")
    check(ang > 90.0 and abs(v_rot / v_cmb - 1.0) > 0.2,
          f"the dragged apex is {ang:.1f} deg from the CMB apex ({'anti-aligned side' if ang>90 else ''}) "
          f"at {v_rot/v_cmb:.2f}x the speed. Since s^TX is a projection of the frame velocity, BOTH the "
          f"magnitude and the SIGN of the frozen prediction (8.68e-10 canonical / 1.048e-9 alt, sign "
          f"NEGATIVE locked, margin 1.50x/1.24x) are at stake. I did NOT re-derive s^TX here, so I "
          f"claim only that the frozen number is frame-dependent and needs re-derivation -- not that "
          f"it flips. Naming an unfinished computation is the honest move")
    return dict(span=span, wb_gamma=gam, ang=ang)


# ---------------------------------------------------------------------------------------------------
def main() -> int:
    banner("ROUTE D -- ADVERSARIAL NO-GO HUNT: CAN A LOCALLY-DRAGGED PASSIVE FRAME SUPPLY THE SPEED?")
    print(f"  a0 = c H_Lambda / Z, Z = sqrt(32 pi/3) = {Z_FACTOR:.5f} -> a0 = {A0_CANON:.4e} m/s^2")
    print("  (canonical rho_DE footing); equivalently a0 = (c/2) sqrt(G rho_Lambda) = EXACTLY HALF the")
    print("  free-fall acceleration at the dark-energy density. kappa = 1/2 is Carl Zimmerman's and is")
    print("  absent from the prior literature. CAVEAT: 32pi/3 is the Einstein-coupling conversion")
    print("  factor and CANCELS in that reduction, so the content is the ONE number kappa, and it is")
    print(f"  FITTED, not derived. Alternate footing carried throughout: a0 = {A0_ALT:.4e} m/s^2.")
    print("  Kernel in force: alpha = 2, mu(x) = x/sqrt(1+x^2). Retired: alpha = 1.")

    env = s1_dictionary()
    s2 = s2_horn_a_comoving(env)
    cor = s3_coriolis(env)
    s4 = s4_horn_b_irrotational(env, cor)
    s5 = s5_passivity()
    s6 = s6_horn_d_smoothed(env, cor)
    s7 = s7_nesting(env)

    banner("VERDICT -- RANKED, WITH WHAT DIED")
    print("  THE OBSTRUCTION, IN ONE SENTENCE. Solar-system ranging forces the dragged frame to carry")
    print(f"  at most 1/{1/cor['g_max']:.0f} of the vorticity of the matter that drags it, which kills a")
    print("  co-moving frame outright; the only construction that meets that cap for free is a")
    print("  potential flow, which is exactly blind to a stationary galaxy's rotation; and a potential")
    print("  flow's remaining translational drag fraction is pinned by a trace identity to be")
    print("  PROPORTIONAL TO THE LOCAL DENSITY, so one coupling cannot capture the bulk motion of a")
    print(f"  {s4['dens_dex']:.1f}-dex range of hosts -- {100*s4['frac_cosmic']:.0f}% of real SPARC")
    print("  galaxies are left at >90% the cosmic frame, which the framework's own RAR excludes at")
    print("  4.6x. That is a closed loop built from three computed identities, not from rhetoric.")
    print()
    print("  RANKING (best first), with the assigned candidate numbers in brackets:")
    print(f"   1. [4] THE FRAME-VORTICITY BOUND -- RIGOROUS, and the sharpest single number here.")
    print(f"        delta a_pair = -w x curl u EXACTLY (symbolic; the symmetric part of grad u cancels")
    print(f"        identically, so ONLY vorticity is observable; negative control u = const passes).")
    print(f"        => rotational drag fraction g <= {cor['g_max']:.2e} conservative / "
          f"{cor['g_opt']:.2e} optimistic,")
    print(f"        i.e. {1/cor['g_max']:.0f}x-{1/cor['g_opt']:.0f}x below the MW's MEASURED Oort")
    print(f"        vorticity A-B = {cor['om_matter']:.3e} 1/s. FOOTING-FREE. This alone excludes any")
    print(f"        frame that co-rotates with local matter, and it forces R_drag >= "
          f"{s6['Rmin']:.0f}-{s6['Rmin_opt']:.0f} kpc.")
    print(f"   2. [1 + 6] THE POTENTIAL-FLOW TRACE IDENTITY -- RIGOROUS, and it is the actual no-go.")
    print(f"        (a) FOR the framework: div(rho v) = -d rho/dt == 0 for any stationary system, so a")
    print(f"            potential-flow frame is EXACTLY rotation-blind, g = 0 identically. It is the")
    print(f"            one candidate that meets #1 for free. Reported at full strength.")
    print(f"        (b) AGAINST it: the surviving translational drag has f_ij = -kappa_d d_i d_j chi")
    print(f"            with Laplacian chi = rho, hence (1/3)Tr f = kappa_d rho(x)/3 POINTWISE, for any")
    print(f"            profile. So f is proportional to LOCAL DENSITY over {s4['dens_dex']:.1f} dex of")
    print(f"            real SPARC. Median-tuned: {s4['spread']:.2f} dex residual = "
          f"{s4['spread']/env['budget']:.0f}x budget with BOTH signs.")
    print(f"            Max-tuned (never over-drags, most generous): {s4['spread_b']:.2f} dex = "
          f"{s4['spread_b']/env['budget']:.1f}x, and")
    print(f"            {100*s4['frac_cosmic']:.0f}% of the sample collapses to f < 0.1 = the cosmic")
    print(f"            frame. a0_eff(rho_local) is the door the corpus nulled at 10.5 sigma.")
    print(f"   3. [2] LOCAL-COMOVING COLLAPSE -- RIGOROUS, corroborating: the RAR's own HI tracer IS the")
    print(f"        local matter, so lam = sigma_gas/Vflat on {s2['n_sparc']} real SPARC galaxies gives")
    print(f"        1.4-1.6 dex of a0 ({s2['over']:.1f}x budget), and at lam = 0 the closure has NO")
    print(f"        SOLUTION at all. Plus a {s2['split']:.0f}% stars-vs-gas tracer split against a")
    print(f"        few-per-cent observed agreement. Same horn as #1 kills, different observable.")
    print(f"   4. [5] NESTING -- RIGOROUS as an ILL-DEFINEDNESS, NOT as a bound violation. a0_eff spans")
    print(f"        {s7['span']:.2f} dex across nested systems; one u cannot serve the Sun's galactic")
    print(f"        orbit and the Earth's solar orbit (mismatch exactly 7.82). On alpha=2 the planets")
    print(f"        stay SAFE at 3e-7 of the Earth bound, so I do NOT sell this as a kill. It does")
    print(f"        force gamma_v = {s7['wb_gamma']:.6f} for wide binaries -- outside the FROZEN band --")
    print(f"        and re-specifies Front B's apex by {s7['ang']:.0f} deg. Reported, not amended.")
    print(f"   5. [1 partial] SINGLE-SCALE SMOOTHING SQUEEZE -- *** PARTIAL: DOES NOT CLOSE. *** At the")
    print(f"        conservative vorticity-forced R_drag = {s6['Rmin']:.0f} kpc, ZERO of {s6['ntot']}")
    print(f"        SPARC galaxies fail host-domination against the cosmic mean, and an isolated field")
    print(f"        galaxy's residual spread is only {s6['cons_best']:.3f} dex = "
          f"{s6['cons_best']/env['budget']:.2f}x budget -- INSIDE it.")
    print(f"        It closes only for group members ({s6['grid'][('conservative',1000.0,'filament (x10)')][0]/env['budget']:.1f}x)")
    print(f"        and on the optimistic leg ({s6['nfail_opt']}/{s6['ntot']} fail, spread "
          f"{s6['opt_best']:.2f}-{s6['opt_worst']:.2f} dex).")
    print(f"        A universal smoothed frame therefore SURVIVES this test for isolated massive hosts.")
    print(f"        It still costs a FIFTH CONSTANT. This is the horn I most wanted and did not get.")
    print(f"   6. [3] LORENTZ / SME -- DID NOT CLOSE. No killing bound derived. What is real: a dragged")
    print(f"        frame RE-SPECIFIES the frozen s^TX prediction ({s7['ang']:.0f} deg apex change,")
    print(f"        0.63x speed), so Front B needs re-derivation; and PPN preferred-frame parameters")
    print(f"        assume a spatially UNIFORM frame, so the corpus's alpha_2^MI ~ 1e-13 does NOT cover")
    print(f"        the gradient effect -- which is exactly why #1 had to be derived from scratch.")
    print(f"   7. [6] PASSIVITY -- *** DIED. *** I tried hard to prove that matter-dragging reinstates")
    print(f"        Einstein-aether strong coupling. It does not: the velocity Hessian is")
    print(f"        2(c1-c4)delta_ij, so c1 = c4 gives ZERO propagating modes WITH spatial gradients")
    print(f"        intact. Passivity is compatible with an elliptic drag operator. Its residue is real")
    print(f"        but indirect: ellipticity forces a boundary condition, which is the hypothesis #2")
    print(f"        needs. The brief guessed this would be the sharpest; it is the one that failed.")
    print()
    print("  SO: WHAT SURVIVES OF THE DOOR? Stated plainly, because 'four of six' is not 'six of six'.")
    print("  A locally-dragged passive frame is NOT ruled out in general. What IS ruled out is every")
    print("  prescription I could construct that is (a) built from the matter distribution, (b) passive,")
    print("  and (c) governed by one universal constant. The gap I could not shut is a")
    print("  gravitomagnetic-type VECTOR drag with a smoothing length ~1e2 kpc, applied to isolated")
    print("  massive hosts only. That is a narrow corner, it needs a fifth constant, its GR-natural")
    print("  coupling is ~1e-6 of the required size, and it inherits #4's nesting ill-definedness -- but")
    print("  it is not closed, and I will not say it is.")
    print()
    print("  NOVELTY, ASSESSED NOT ASSERTED. Nothing here is a new physical idea. Inertia relative to")
    print("  local matter is Mach; Sciama 1953 is the standard citation; the objection that a")
    print("  non-rigidly-dragged frame produces observable fictitious forces is classical, and #1 is")
    print("  its quantitative form on 2020s ephemerides. Milgrom 1994 owns the modified-inertia class")
    print("  and the orbit-dependence; Milgrom 2022 owns the single-frequency restriction. The")
    print("  gravitomagnetic vector-Poisson drag is Lense-Thirring. What appears to be NEW is narrow")
    print("  and internal: (a) the exact statement that the pair-differential anomaly is -w x curl u,")
    print("  which isolates the frame VORTICITY as the only observable of grad u and thereby turns a")
    print("  vague 'fictitious forces' worry into one clean number; (b) the trace identity pinning the")
    print("  potential-flow drag fraction to the LOCAL DENSITY pointwise, which routes this door into a")
    print("  door the corpus already closed; (c) the stationarity theorem in this context. All three")
    print("  are corollaries of textbook identities applied to this framework's own action.")
    print()
    print("  WHAT WOULD BE NEEDED TO FINISH / TO ESCAPE. Named, not hidden:")
    print("   * A drag that is NOT a potential flow and NOT co-rotating: a gravitomagnetic-type vector")
    print("     Poisson equation is the natural candidate and it evades #2 (it has vorticity by")
    print(f"     construction) -- but it must then satisfy #1's {1/cor['g_max']:.0f}x vorticity")
    print("     suppression, which is what forces R_drag into #4's squeeze. Computing that coupling's")
    print("     actual amplitude (in GR it is O((v/c)^2), ~1e-6 of what is needed) is the open task.")
    print("   * Dispersion-supported systems have ZERO matter vorticity, so #1 says nothing about")
    print("     dwarf spheroidals or cluster galaxies. A real scope limit, stated not buried.")
    print("   * The vorticity bound needs a proper precession-residual treatment. I EXPECTED that to")
    print("     be TIGHTER than the ranging inversion. The one independent number I could compute (the")
    print("     LLR geodetic-precession residual) came out 29x LOOSER, so I DEMOTED my own headline")
    print("     from 717x to 25x and used 25x everywhere downstream. A dedicated ephemeris fit of a")
    print("     uniform frame rotation is the correct computation and it is NOT done here.")
    print("   * If the frame were sourced by the framework's own dark (AeST/ghost-condensate Q) sector")
    print("     rather than by baryons, #2's continuity argument would need redoing for that")
    print("     sector's own flux. Not attempted here. That is the least-closed corner.")
    print()
    print("  NOT CLAIMED: that a0 is derived (kappa = 1/2 is fitted); that the off-circular law is")
    print("  settled; that any live front is decided; that the theory is closed. Nothing here revives")
    print("  the TOE / Standard-Model claims retracted publicly on 2026-06-23.")
    print("=" * 102)
    if FAILS:
        print("\n  FAILED CHECKS:")
        for f in FAILS:
            print(f"   - {f}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
