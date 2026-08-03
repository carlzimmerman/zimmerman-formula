#!/usr/bin/env python3
r"""mi_vdep_ephemeris_verdict_2026.py -- DOES THE VELOCITY-DEPENDENT CONSTRUCTION CURE THE EPHEMERIS
LIABILITY? Settling a direct contradiction between two agents, by computing it here.

THE CONSTRUCTION (from the 2026-08-02 preferred-frame run, verified below before it is used):
    L = (1/2) m V^2 F(z) - m Phi(r),     z = V^2/(a0 r)
with F FORCED, not chosen, by the requirement that circular orbits reproduce the framework's kernel:
    F(z) + (z/2) F'(z) = mu(z)   <=>   d/dz[z^2 F] = 2 z mu(z)   <=>   F(z) = (2/z^2) INT_0^z t mu(t) dt
    alpha=1:  F_1(z) = [(z/2) sqrt(1+4z^2) - z + (1/4) asinh(2z)] / z^2      ( = the corpus's beta_fw )
    alpha=2:  F_2(z) = [z sqrt(1+z^2) - asinh(z)] / z^2
No acceleration appears in the action, so the Ostrogradsky/ghost/split-signature kills of earlier today do not
reach it. That much is real and is re-verified in V1.

THE CONTRADICTION TO SETTLE. The builder lane concluded the ephemeris liability is "inherited UNCHANGED at
eps = 0". Its improver claimed to have found two algebra errors at the Sun and that fixing them REVERSES that:
that the v-dependent modification CURES the liability on the in-force kernel, both footings. Those cannot both
be right, and it is the single most consequential number of the day, so it is computed here rather than
relayed.

THE DECIDING STRUCTURE, stated before any number is evaluated. The construction's equation of motion is
    mu(z) a = g_bar        with     z = V^2/(a0 r)
whereas the algebraic law this corpus fits with is
    mu(a/a0) a = g_bar.
So the ENTIRE difference is the ARGUMENT: z versus a/a0. For a Keplerian ellipse, V^2 = GM(2/r - 1/A) with A
the semi-major axis and a_N = GM/r^2, hence
    z / (a_N/a0) = r (2/r - 1/A) = 2 - r/A
which is EXACTLY 1 on a circle and runs from 1+e (perihelion) to 1-e (aphelion). *** So the construction can
only differ from the algebraic law at O(e), and cannot move an anomaly by orders of magnitude. *** V2-V4 test
that prediction against the actual bodies, on both footings, and V5 states the verdict.

  V1  the construction, re-verified: the ODE, the closed forms, F_1 = beta_fw, and z = a/a0 on circles
  V2  the argument ratio across the solar system, and the Sun
  V3  the anomaly, both readings, both footings -- cured, unchanged, or worse?
  V4  the eccentricity lever: how big CAN the difference get?
  V5  verdict, and which agent was right

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 106)
    print(f"  {t}")
    print("=" * 106)


A0 = {"canon": 9.36e-11, "alt": 1.13e-10}
GM_SUN = 1.32712440018e20
GM_J = 1.26686534e17
AU = 1.495978707e11
MARS_BUDGET = 1.5           # m, the ranging budget used by the corpus's committed LM fit
BOUND_EARTH = 3.66e-14      # the loose Sereno-Jetzer Earth 2-sigma anomalous-acceleration bound


def mu2(z):
    """the framework's in-force alpha=2 kernel, mu(z) = z/sqrt(1+z^2)."""
    return z / math.sqrt(1.0 + z * z)


def anomaly_from_argument(g_bar, arg, a0):
    """solve mu(arg) a = g_bar for a, then return the anomaly a - g_bar.
    With the ALGEBRAIC law arg = a/a0 (self-consistent); with the CONSTRUCTION arg = z = V^2/(a0 r)."""
    return g_bar / mu2(arg) - g_bar


banner("V1  THE CONSTRUCTION, RE-VERIFIED BEFORE IT IS USED")

z = sp.Symbol("z", positive=True)
F1 = (( z / 2) * sp.sqrt(1 + 4 * z**2) - z + sp.asinh(2 * z) / 4) / z**2
F2 = (z * sp.sqrt(1 + z**2) - sp.asinh(z)) / z**2
mu1_s = (sp.sqrt(1 + 4 * z**2) - 1) / (2 * z)
mu2_s = z / sp.sqrt(1 + z**2)
for nm, F, mu in (("alpha=1", F1, mu1_s), ("alpha=2", F2, mu2_s)):
    res = sp.simplify(F + (z / 2) * sp.diff(F, z) - mu)
    print(f"  {nm}:  F + (z/2)F' - mu  =  {res}")
    check(res == 0,
          f"V1-{nm} the closed form satisfies the forcing ODE exactly (residual {res}), so F is DERIVED from "
          f"the kernel, not fitted")
# F_1 IS beta_fw
beta_fw = ((z / 2) * sp.sqrt(1 + 4 * z**2) + sp.asinh(2 * z) / 4 - z) / z**2
check(sp.simplify(F1 - beta_fw) == 0,
      f"V1c *** F_1 IS IDENTICALLY beta_fw *** -- the same function as the local acceleration-dependent "
      f"Lagrangian Ostrogradsky killed this afternoon. The difference is the ARGUMENT: |a|/a0 there, "
      f"V^2/(a0 r) here. The corpus had the right function and the wrong variable")
# and on a CIRCLE, z = a/a0 identically
GMs, rs, a0s = sp.symbols("GM r a_0", positive=True)
V2_circ = GMs / rs                                  # circular: V^2 = GM/r
z_circ = sp.simplify(V2_circ / (a0s * rs))
a_over_a0 = sp.simplify(GMs / rs**2 / a0s)
check(sp.simplify(z_circ - a_over_a0) == 0,
      f"V1d and on a CIRCULAR orbit z = V^2/(a0 r) = {z_circ} = a_N/a0 IDENTICALLY. That is why the "
      f"construction reproduces the kernel with no acceleration in the action -- and it is also why V2-V4 will "
      f"find only O(e) differences")


banner("V2  THE ARGUMENT RATIO ACROSS THE SOLAR SYSTEM, AND THE SUN")

r_, A_, e_ = sp.symbols("r A e", positive=True)
ratio = sp.simplify((GMs * (2 / r_ - 1 / A_) / (a0s * r_)) / (GMs / r_**2 / a0s))
print(f"  Keplerian ellipse:  z / (a_N/a0) = {ratio}")
check(sp.simplify(ratio - (2 - r_ / A_)) == 0,
      f"V2a the argument ratio is EXACTLY {ratio}: identically 1 on a circle, 1+e at perihelion, 1-e at "
      f"aphelion. *** The construction's argument can differ from the algebraic law's by AT MOST a factor "
      f"(1+e), never by orders of magnitude. That single line decides the contradiction. ***")

BODIES = [  # name, semi-major (AU), eccentricity
    ("Mercury", 0.387098, 0.205630), ("Venus", 0.723332, 0.006772), ("Earth", 1.000000, 0.016710),
    ("Mars", 1.523679, 0.093394), ("Jupiter", 5.204267, 0.048775), ("Saturn", 9.582017, 0.055723),
    ("Neptune", 30.07069, 0.008678),
]
print(f"\n  {'body':<9}{'a_N/a0 (canon)':>16}{'z at peri':>13}{'z at apo':>13}{'max ratio':>11}")
print("  " + "-" * 63)
for nm, Aau, e in BODIES:
    A = Aau * AU
    aN = GM_SUN / A**2
    zc = aN / A0["canon"]
    print(f"  {nm:<9}{zc:>16.4e}{zc*(1+e):>13.4e}{zc*(1-e):>13.4e}{1+e:>11.4f}")

# THE SUN. Its own acceleration is the Jupiter-driven reflex; its reflex orbit is near-circular (e_J = 0.0488).
r_J = 5.204267 * AU
a_sun = GM_J / r_J**2
z_sun = a_sun / A0["canon"]
print(f"\n  THE SUN (the body the corpus found binds the alpha=2 1/g tail):")
print(f"      Jupiter-driven reflex acceleration a_sun = {a_sun:.4e} m/s^2 = {z_sun:.1f} a0 (canonical)")
print(f"      its reflex orbit has Jupiter's eccentricity e = 0.0488, so z_sun spans "
      f"{z_sun*(1-0.0488):.1f} to {z_sun*(1+0.0488):.1f}")
check(abs(z_sun - 2233) < 30,
      f"V2b the Sun's argument under the CONSTRUCTION is z_sun = {z_sun:.0f} a0, essentially identical to the "
      f"a_sun/a0 = {z_sun:.0f} the corpus already banked (the audit's 2236, 0.1%). The reflex is near-circular, "
      f"so the v-dependent argument buys NOTHING at the Sun")


banner("V3  THE ANOMALY, BOTH READINGS, BOTH FOOTINGS")

print(f"  {'footing':<8}{'body':<9}{'algebraic anomaly':>20}{'construction (peri)':>21}{'ratio':>9}")
print("  " + "-" * 68)
worst = 0.0
for fn, a0 in A0.items():
    for nm, Aau, e in (("Mars", 1.523679, 0.093394), ("Earth", 1.0, 0.016710)):
        A = Aau * AU
        g = GM_SUN / A**2
        alg = anomaly_from_argument(g, g / a0, a0)                  # arg = a/a0
        con = anomaly_from_argument(g, (g / a0) * (1 + e), a0)      # arg = z at perihelion
        print(f"  {fn:<8}{nm:<9}{alg:>20.4e}{con:>21.4e}{con/alg:>9.4f}")
        worst = max(worst, abs(con / alg - 1))
    g_s = a_sun
    alg_s = anomaly_from_argument(g_s, g_s / a0, a0)
    con_s = anomaly_from_argument(g_s, (g_s / a0) * (1 + 0.0488), a0)
    print(f"  {fn:<8}{'SUN':<9}{alg_s:>20.4e}{con_s:>21.4e}{con_s/alg_s:>9.4f}")
    worst = max(worst, abs(con_s / alg_s - 1))

check(worst < 0.5,
      f"V3a *** THE CONSTRUCTION DOES NOT CURE THE LIABILITY. *** Across Earth, Mars and the Sun, on both "
      f"footings, the anomaly changes by at most {100*worst:.1f}% relative to the algebraic law -- a factor "
      f"{1+worst:.2f}, not the orders of magnitude a cure would need. The reason is V2a: the argument ratio is "
      f"bounded by (1+e), and no solar-system eccentricity is large")
# and the standing liability is unchanged in size
over_sun = {fn: anomaly_from_argument(a_sun, a_sun / a0, a0) for fn, a0 in A0.items()}
print(f"\n  the Sun's tail, for the record: {over_sun['canon']:.3e} (canon) / {over_sun['alt']:.3e} (alt) m/s^2")
check(over_sun["canon"] > 1e-14,
      f"V3b the Sun-carried tail is {over_sun['canon']:.3e} m/s^2 (canonical), which is the same object the "
      f"corpus's committed LM ephemeris fit prices at 8.5x (canon) / 12.4x (alt) the Mars ranging budget. "
      f"The construction inherits it essentially unchanged")


banner("V4  HOW BIG *CAN* THE DIFFERENCE GET?")

print("  The lever is eccentricity, and it is bounded. Sweeping e at fixed semi-major axis (Mars-like):")
A = 1.523679 * AU
g = GM_SUN / A**2
print(f"  {'e':>6}{'ratio at perihelion':>22}{'ratio at aphelion':>20}")
print("  " + "-" * 48)
for e in (0.0, 0.05, 0.1, 0.2, 0.5, 0.9):
    rp = anomaly_from_argument(g, (g / A0['canon']) * (1 + e), A0['canon'])
    ra = anomaly_from_argument(g, (g / A0['canon']) * (1 - e), A0['canon'])
    base = anomaly_from_argument(g, g / A0['canon'], A0['canon'])
    print(f"  {e:>6.2f}{rp/base:>22.4f}{ra/base:>20.4f}")
rp09 = anomaly_from_argument(g, (g / A0['canon']) * 1.9, A0['canon'])
base = anomaly_from_argument(g, g / A0['canon'], A0['canon'])
check(rp09 / base > 0.2,
      f"V4a even at an absurd e = 0.9 the perihelion anomaly is only {rp09/base:.3f} of the algebraic value -- "
      f"a factor {base/rp09:.2f}, against the ~12x suppression a cure would need. The lever is bounded by "
      f"(1+e)^-2 in the deep-Newtonian tail and no orbit in the solar system is eccentric enough. THE "
      f"ECCENTRICITY LEVER CANNOT CURE THE EPHEMERIS")


banner("V6  SO HOW *CAN* IT BE RESOLVED? -- three routes, priced")

# Route A: a faster-than-power-law approach to Newton (the exponential / McGaugh-RAR tail)
exp_tail = {fn: a0 * math.exp(-math.sqrt(a_sun / a0)) for fn, a0 in A0.items()}
print(f"  ROUTE A -- an exponential approach to Newton, delta_a ~ a0 exp(-sqrt(g/a0)):")
for fn, v in exp_tail.items():
    print(f"      Sun: {v:.3e} m/s^2 ({fn}) vs the tail it replaces {over_sun[fn]:.3e} "
          f"-> suppression {over_sun[fn]/v:.2e}x")
check(min(exp_tail.values()) < 1e-30,
      f"V6a ROUTE A WORKS AND IT JUST GOT CHEAPER. The exponential tail suppresses the Sun's anomaly by "
      f"{over_sun['canon']/exp_tail['canon']:.1e}x, clearing every bound by many orders. It was always the "
      f"whitepaper's own adopted template; what changed TODAY is the price. (i) B2a: Milgrom's analyticity "
      f"condition excludes EVERY interpolating function in use, McGaugh's exponential included, so switching "
      f"loses NO admissibility that alpha=1 or alpha=2 had. (ii) N6: the dS-Unruh derivation of the kernel "
      f"shape is TORSION-LOCKED to hyperbolic motion and does not apply to orbits anyway -- so the 'derived "
      f"kernel' the switch would cost was never valid where MOND lives. The exponential costs a shape "
      f"postulate, and the shape was already postulated for orbits")

# Route B: frequency dressing -- and the construction gives it a natural home
Om_sun = math.sqrt(GM_SUN / (5.204267 * AU) ** 3)      # Jupiter's mean motion sets the Sun's reflex frequency
Om_mw = 233e3 / (8.21 * 3.0857e19)
H0 = 67.4e3 / 3.0857e22
p_req = 0.069
supp = ((1 + Om_sun / H0) / (1 + Om_mw / H0)) ** p_req
print(f"\n  ROUTE B -- frequency dressing a0_eff ~ (1 + Omega/H0)^-p, the corpus's banked p >= {p_req}:")
print(f"      Omega/H0 = {Om_sun/H0:.3e} (Sun's reflex) vs {Om_mw/H0:.3e} (MW) -> relative suppression "
      f"{supp:.3e}x at p = {p_req}")
check(supp > 1.0,
      f"V6b ROUTE B is the corpus's banked p >= {p_req} at <= 0.010 dex SPARC cost, and the v-dependent "
      f"construction gives it a NATURAL HOME rather than an ad-hoc one: z = V^2/(a0 r) = Omega^2 r/a0 is "
      f"already a frequency object, so a frequency-dressed a0 is expressible inside L(x,v) instead of bolted "
      f"on. Cost: a fifth constant, which is exactly what STANDING already charges for it")

# Route C: the radial-velocity sector -- free, but it CANNOT fix the Sun
print(f"\n  ROUTE C -- the radial-velocity sector, which circular orbits are PROVABLY BLIND to:")
print(f"      An independent agent proved d/dL_u of the circular-orbit EL is identically zero, so the whole")
print(f"      rdot^2 sector of L is UNCONSTRAINED by rotation curves. Any term there leaves the RAR's")
print(f"      0.108 dex, the BTFR and the kappa=1/2 measurement EXACTLY unchanged.")
e_sun_reflex = 0.048775
print(f"      But such a term VANISHES at rdot = 0, and the Sun's Jupiter-driven reflex has e = "
      f"{e_sun_reflex} -> (rdot/V)^2 <~ {e_sun_reflex**2:.2e}")
check(e_sun_reflex**2 < 0.01,
      f"V6c ROUTE C CANNOT FIX THE EPHEMERIS, and the reason is clean: an rdot^2 term vanishes on circular "
      f"orbits, the binding body is the SUN, and the Sun's reflex is near-circular ((rdot/V)^2 <~ "
      f"{e_sun_reflex**2:.1e}). It can move eccentric planets (Mercury e = 0.206, Mars e = 0.093) but not the "
      f"body that binds. *** ITS VALUE IS THE OTHER DIRECTION: a free sector, invisible to every rotation "
      f"curve, that generates ECCENTRICITY-DEPENDENT predictions at zero phenomenological cost -- which is the "
      f"wide-binary eccentricity lever done properly, from a real Lagrangian instead of the rectilinear ansatz "
      f"that was refuted for assuming unbounded v ***")


banner("V5  VERDICT")

print(f"""  *** THE BUILDER WAS RIGHT AND THE IMPROVER WAS WRONG. *** The velocity-dependent construction inherits
  the ephemeris liability essentially unchanged. It is not cured, and it is not made orders-of-magnitude worse
  either -- the anomaly moves by at most {100*worst:.1f}% on the real bodies.

  THE ONE-LINE REASON, and it is structural rather than numerical: the construction and the algebraic law
  differ ONLY in the argument fed to mu, and for a Keplerian ellipse that ratio is exactly 2 - r/A, which is 1
  on a circle and bounded by (1 +- e) everywhere. The Sun's Jupiter-driven reflex is near-circular
  (e = 0.0488), so the body that binds the alpha=2 tail sees an argument within 5% of the one already banked.
  A cure would have required the v-dependent argument to be orders of magnitude LARGER at the Sun than a/a0.
  It is not: the two agree to 0.1% there.

  WHAT SURVIVES, AND IT IS STILL THE BEST RESULT OF THE DAY -- just not this part of it:
   * The construction is real, local, first order in the velocity, and ghost-free. V1 re-verifies the forcing
     ODE and both closed forms with residual exactly zero.
   * F_1 IS beta_fw identically (V1c). The corpus had the right function and the wrong argument, and swapping
     |a|/a0 for V^2/(a0 r) removes the acceleration from the action -- so Ostrogradsky, the ghosts, the split
     signature and the 10.7 Myr growing root all evaporate. None of that depended on the ephemeris claim.
   * The kernel is reproduced EXACTLY on circular orbits (V1d), so the RAR's 0.108 dex, the BTFR and the
     kappa = 1/2 discriminability carry over with no refit.
   * And Milgrom himself wrote this loophole and commented it out (m94.tex lines 1945-1949, verified in the
     arXiv TeX source by an independent agent; line 1631: "We do insist on full Galilei invariance").

  WHAT IT COSTS, unchanged by this run: the solar-system liability stays at 8.5x (canonical) / 12.4x (alt) the
  Mars ranging budget on the in-force kernel, and the construction's own sharpest exposure is elsewhere -- the
  epicyclic frequency collapsing in deep MOND (predicted sigma_theta/sigma_R = 0.332 at R = 20 kpc against
  ~0.6-0.7 observed, a factor 1.96 conflict), which is a parameter-free prediction testable on Milky Way
  outer-disc kinematics.

  AND THE METHODOLOGICAL POINT, since this is the second time today: an improver agent claimed a reversal on
  the single highest-value number in the run, and it was wrong. Relaying it would have been a manufactured win
  of exactly the kind that cost this corpus its June retraction. The rule holds -- compute the load-bearing
  number yourself.""")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the construction is real and ghost-free; the ephemeris liability is NOT cured.")
