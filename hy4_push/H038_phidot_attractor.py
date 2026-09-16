#!/usr/bin/env python3
r"""H038 -- IS phidot = 0 AN ATTRACTOR, OR AN IMPOSED CONSTRAINT?  (open item R10)

WHY THIS LANE EXISTS.
  H011 deleted the aether by observing that with phidot = 0 the gradient is
  SPACELIKE, so

        K = (1/2) g^{ab} d_a phi d_b phi / Lambda^4  >=  0

  automatically and sqrt(K) is real without a projector.  H011 ended with the
  honest open item:

        "Is phi_dot = 0 an ATTRACTOR, or must it be imposed?  If the scalar
         can roll, K goes negative and the theory leaves its domain.  This is
         the first thing to compute."

  This lane computes it.  The question has three parts:

    (Q1)  GROWTH.  Integrate the scalar EOM in FLRW with a small initial
          phidot.  Does |phidot| grow or decay?
    (Q2)  PROTECTION.  Does the EOM keep K >= 0 by itself, or is K >= 0 an
          external condition?
    (Q3)  STABILITY.  Is the frozen configuration stable?

THE THREE FACTS THAT DECIDED IT (all measured below, none assumed).

  FACT 1 -- KINEMATICS.  In homogeneous FLRW with signature (-,+,+,+),
        (dphi)^2 = -phidot^2, so  K = -phidot^2/(2 Lambda^4) <= 0  ALWAYS,
        with equality iff phidot = 0.  The domain K >= 0 of a homogeneous
        FLRW configuration is therefore the SINGLE POINT phidot = 0.  There
        is no open neighbourhood of the frozen configuration inside the
        theory, so "attractor" -- which needs a neighbourhood whose flow
        converges -- cannot even be posed in the homogeneous sector.

  FACT 2 -- REALITY.  Off the frozen locus the EOM coefficient is not real.
        f'(K) = mu_2(sqrt K) with mu_2(u) = u(2+u)/(1+u)^2; at K = -w^2,
        sqrt K = i w and

              mu_2(i w) = [ w^2 (w^2+3) + 2 i w ] / (1 + w^2)^2 ,

        whose imaginary part 2w/(1+w^2)^2 is strictly nonzero for w != 0.
        The conserved Noether current a^3 f'(K) phidot is therefore complex
        for every nonzero phidot: no REAL rolling FLRW solution exists.

  FACT 3 -- DEGENERACY (no protection, no restoring force).  f'(K) -> 0 as
        K -> 0+: measured bound f'(K) <= 2 sqrt(K).  The coefficient of the
        kinetic/derivative term VANISHES at the frozen point, so (i) the
        linearised EOM about the frozen background is the empty statement
        0 = 0, and (ii) there is no barrier and no restoring force pushing
        K back up.  Protection is the opposite of what the EOM supplies.

WHAT THE INTEGRATION ACTUALLY SHOWS.
  Grant the analytic continuation anyway (three inequivalent real
  projections of the complex EOM are integrated: modulus, real part,
  imaginary part).  In all three |phidot| DECAYS in an expanding universe
  -- measured exponents |phidot| ~ a^{-3/2}, a^{-1}, a^{-3/2}.  But every
  point of every one of those trajectories has K < 0: the flow converges to
  the frozen point FROM OUTSIDE the domain and never enters it.  Decay on
  the continuation is therefore a statement about a function that is not the
  theory, not a statement about the theory.

VERDICT:  phidot = 0 is an IMPOSED CONSTRAINT (a domain/reality condition
that isolates a single configuration), not a dynamical attractor.

Every check states MEASUREMENT and THRESHOLD separately.  Nothing here is a
literal-True: each check computes a number and compares it to a stated bound.
Both footings a0 = 9.3619e-11 and a0 = 1.1279e-10 are run.
"""
import json, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ------------------------------------------------------------------ harness
RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, thr="", d=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured : {measured}")
    print(f"         threshold: {thr}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "threshold": thr, "pass": ok})
    NP_ += 1 if ok else 0
    NF_ += 0 if ok else 1
    return ok

# ---------------------------------------------------------------- constants
G      = 6.67430e-11
c      = 2.99792458e8
A0_LO  = 9.3619e-11          # footing (low)
A0_HI  = 1.1279e-10          # footing (high)
FOOT   = [("low ", A0_LO), ("high", A0_HI)]
H0     = 67.4e3/3.0856775814913673e22
Om     = 0.315
Ol     = 0.685
MSUN   = 1.98847e30
PC     = 3.0856775814913673e16

print("="*78)
print("H038 -- IS phidot = 0 AN ATTRACTOR, OR AN IMPOSED CONSTRAINT?  (R10)")
print("="*78)
print(f"\n  footings: a0 = {A0_LO:.4e} and {A0_HI:.4e} m/s^2")
print(f"  background: flat LCDM, H0 = {H0*3.0856775814913673e22/1e3:.1f} km/s/Mpc,"
      f" Om = {Om}, OL = {Ol}")

# ================================================================ 1. the EOM
print("\n" + "="*78)
print("PART 1 -- THE EXACT FLRW REDUCTION OF THE SCALAR EOM")
print("="*78)

t, L4 = sp.symbols('t Lambda4', positive=True)
ph    = sp.Function('phi')
a_    = sp.Function('a', positive=True)
fpK   = sp.Function('Fp')          # f'(K) -- kept opaque, the EOM is algebraic in it

# --- explicit index computation: g^{mu nu} = diag(-1, a^-2, a^-2, a^-2),
#     sqrt(-g) = a^3, V^mu = f' g^{mu nu} d_nu phi with d_nu phi = (phidot,0,0,0).
#     div = (1/sqrt(-g)) sum_mu d_mu( sqrt(-g) V^mu ).
ginv  = [-1, 1/a_(t)**2, 1/a_(t)**2, 1/a_(t)**2]
dphi  = [sp.diff(ph(t), t), 0, 0, 0]
coords = [t, None, None, None]
V     = [fpK(t)*ginv[m]*dphi[m] for m in range(4)]
sqg   = a_(t)**3
div   = sum([sp.diff(sqg*V[0], t)] + [0, 0, 0]) / sqg      # only mu = 0 survives
target = -sp.diff(sqg*fpK(t)*sp.diff(ph(t), t), t)/sqg      # -(1/a^3) d_t(a^3 f' phidot)
resid  = sp.simplify(div - target)

# K in homogeneous FLRW, signature (-,+,+,+):  (dphi)^2 = -phidot^2
Kflrw = sum(ginv[m]*dphi[m]*dphi[m] for m in range(4))/(2*L4)
phid  = sp.Symbol('phidot')
Ksub  = -phid**2/(2*L4)
residK = sp.simplify(Kflrw - Ksub.subs(phid, sp.diff(ph(t), t)))

check("E1 [EXACT REDUCTION] grad_mu[f'(K) d^mu phi] = 0 in homogeneous FLRW reduces\n"
      "      to d_t( a^3 f'(K) phidot ) = 0, i.e. a^3 f'(K) phidot = const",
      f"divergence = {sp.simplify(div)};  residual against -(1/a^3)d_t(a^3 f' phidot)"
      f" = {resid};  K(FLRW) = {sp.simplify(Kflrw)};  residual(K) = {residK}",
      (resid == 0) and (residK == 0),
      "both symbolic residuals == 0",
      "This is exact, not perturbative: the scalar EOM in FLRW is a FIRST\n"
      "         INTEGRAL, not a second-order equation.")

# --- and K <= 0 for every real phidot
vgrid = np.array([1e-8, 1e-4, 1e-2, 1.0, 10.0, 1e3, 1e6])
Kvals = -vgrid**2/2.0                                     # in units of Lambda^4
check("E2 [KINEMATICS] in homogeneous FLRW  K = -phidot^2/(2 Lambda^4) <= 0\n"
      "      for every real phidot, with equality iff phidot = 0",
      f"max K over |v| in [1e-8, 1e6] (v = phidot/Lambda^2) = {Kvals.max():.6e}; "
      f"K at v = 0 = {0.0:.1e}",
      Kvals.max() <= 0.0,
      "K <= 0 for all v (equality only at v = 0)",
      "The domain K >= 0 of the homogeneous FLRW sector is ONE POINT: v = 0.\n"
      "         An attractor needs a neighbourhood to attract FROM. There is none.")

# ================================================================ 2. reality
print("\n" + "="*78)
print("PART 2 -- IS THE EOM REAL OFF THE FROZEN LOCUS?  (the decisive test)")
print("="*78)

w_, u_ = sp.symbols('w u', positive=True)
mu2 = lambda z: z*(2+z)/(1+z)**2

# mu_2(i w) = [w^2(w^2+3) + 2 i w]/(1+w^2)^2   -- verified by sympy.
# A(w) = Re is even in w and B(w) = Im is odd, so project with w -> -w.
claim_re = w_**2*(w_**2+3)/(1+w_**2)**2
claim_im = 2*w_/(1+w_**2)**2
mu2iw    = sp.simplify(mu2(sp.I*w_))
mu2iw_rat = sp.simplify(sp.together(sp.expand(mu2iw)))
re_part   = sp.simplify(sp.expand(sp.simplify((mu2iw_rat + mu2iw_rat.subs(w_, -w_))/2)))
im_part   = sp.simplify(sp.expand(sp.simplify((mu2iw_rat - mu2iw_rat.subs(w_, -w_))/(2*sp.I))))
re_zero   = sp.simplify(re_part - claim_re)
im_zero   = sp.simplify(im_part - claim_im)
check("R1 [CONTINUATION] for K = -w^2, f'(K) = mu_2(i w) with\n"
      "      Re = w^2(w^2+3)/(1+w^2)^2 and Im = 2w/(1+w^2)^2  (sympy exact)",
      f"residual(Re) = {re_zero}; residual(Im) = {im_zero}",
      (re_zero == 0) and (im_zero == 0),
      "both symbolic residuals == 0",
      "sqrt(K) is imaginary off the frozen locus, so f'(K) is complex -- this is\n"
      "         not a choice, it is what mu_2 does.")

def mu2_re(w): return w*w*(w*w+3.0)/(1.0+w*w)**2
def mu2_im(w): return 2.0*w/(1.0+w*w)**2
def mu2_abs(w): return math.hypot(mu2_re(w), mu2_im(w))

wgrid = np.logspace(-6, 6, 601)
imvals = mu2_im(wgrid)
check("R2 [NO REAL DYNAMICS] Im f'(K) = 2w/(1+w^2)^2 is strictly nonzero for\n"
      "      every w > 0, so the Noether current a^3 f'(K) phidot is complex\n"
      "      for every nonzero phidot",
      f"min Im f' over w in [1e-6, 1e6] = {imvals.min():.6e}; "
      f"value at w = 1e-6 = {mu2_im(1e-6):.6e}",
      imvals.min() > 0.0,
      "Im f' > 0 for all w > 0 (never real)",
      "Consequence: there is NO real rolling homogeneous FLRW solution. The\n"
      "         frozen configuration is not the endpoint of a flow -- it is the\n"
      "         only real configuration.")

# the smallest w the grid resolves still gives a definite imaginary part
for tag, a0 in FOOT:
    L2 = 2.0*a0/math.sqrt(G)                 # Lambda^2 = 2 a0 / sqrt(G)
    w = 1e-3/math.sqrt(2.0)                  # v = 1e-3  =>  w = |v|/sqrt(2)
    check(f"R3 [{tag.strip()} footing] a physical perturbation v = phidot/Lambda^2 = 1e-3\n"
          f"      gives |Im f'| / |f'| = {mu2_im(w)/mu2_abs(w):.6f} (the EOM coefficient is\n"
          f"      not even approximately real)",
          f"Lambda^2 = 2 a0/sqrt(G) = {L2:.6e}; phidot = {1e-3*L2:.6e} SI; "
          f"Im f' = {mu2_im(w):.6e}, |f'| = {mu2_abs(w):.6e}",
          mu2_im(w)/mu2_abs(w) > 0.05,
          "|Im f'|/|f'| > 0.05",
          "The imaginary part is not a small correction: at small w it is the\n"
          "         DOMINANT part of f' (Im ~ 2w while Re ~ 3w^2).")

# ================================================================ 3. integrate
print("\n" + "="*78)
print("PART 3 -- INTEGRATE IT ANYWAY: three real projections of the complex EOM")
print("="*78)
print("  d_t[a^3 G(v)] = 0 with G(v) = g(v) v,  v = phidot/Lambda^2,  w = |v|/sqrt2")
print("  continuation:  g = |mu_2(iw)|  [M] |  Re mu_2(iw)  [R] |  Im mu_2(iw)  [I]")

def make_G(kind):
    if kind == 'M':
        g = lambda v: mu2_abs(abs(v)/math.sqrt(2.0))
    elif kind == 'R':
        g = lambda v: mu2_re(abs(v)/math.sqrt(2.0))
    else:
        g = lambda v: mu2_im(abs(v)/math.sqrt(2.0))
    return lambda v: g(v)*v

def dGdv(G, v, h=None):
    h = h or max(1e-7, 1e-7*abs(v))
    return (G(v+h) - G(v-h))/(2*h)

def integrate(kind, v0, s_span=(0.0, math.log(4.0)), n=4000):
    """s = ln a.  dv/ds = -3 G(v)/G'(v).  Returns s, v."""
    Gf = make_G(kind)
    def rhs(s, y):
        v = y[0]
        return [-3.0*Gf(v)/dGdv(Gf, v)]
    sol = solve_ivp(rhs, s_span, [v0], rtol=1e-11, atol=1e-14*abs(v0),
                    dense_output=True, method='Radau', max_step=0.01)
    s = np.linspace(s_span[0], s_span[1], n)
    return s, sol.sol(s)[0]

s_all, v_all, K_all, inv_all = {}, {}, {}, {}
for kind in ['M', 'R', 'I']:
    v0 = 1e-3
    s, v = integrate(kind, v0)
    s_all[kind], v_all[kind] = s, v
    K_all[kind] = -v**2/2.0
    Gf = make_G(kind)
    inv_all[kind] = np.exp(3*s)*np.array([Gf(x) for x in v])  # a^3 G(v) -- conserved

    # measured decay exponent p in |v| ~ a^{-p}, fitted over the last decade of a
    m = s > math.log(1.0)
    p = -np.polyfit(s[m], np.log(np.abs(v[m])), 1)[0]
    ratio = abs(v[-1])/abs(v[0])
    print(f"\n  --- continuation [{kind}] ---")
    print(f"      |v| : {abs(v[0]):.6e} -> {abs(v[-1]):.6e}  over a = 1 -> 4")
    print(f"      fitted  |v| ~ a^-p :  p = {p:.6f}")
    print(f"      K range over the trajectory: [{K_all[kind].min():.6e}, "
          f"{K_all[kind].max():.6e}]")

    check(f"G1[{kind}] [DIRECTION OF FLOW] |phidot| DECAYS: |v_final|/|v_initial| < 1",
          f"|v_f|/|v_i| = {ratio:.6e}",
          ratio < 1.0,
          "ratio < 1 (decay, not growth)",
          "On the continuation the flow does move toward the frozen point.")
    check(f"G2[{kind}] [RATE] fitted decay exponent p in |v| ~ a^-p",
          f"p = {p:.6f}",
          p > 0.5,
          "p > 0.5",
          "Measured p: 3/2 for the modulus and imaginary projections, 1 for the\n"
          "         real-part projection -- consistent with G(v) ~ v^2 and ~ v^3.")
    nK = int((K_all[kind] > 0).sum())
    check(f"G3[{kind}] [BUT IT NEVER ENTERS THE DOMAIN] K < 0 at every point of\n"
          f"      the trajectory: the count of samples with K >= 0 is zero",
          f"samples with K >= 0: {nK} of {len(v)};  max K = {K_all[kind].max():.6e}",
          nK == 0,
          "0 samples with K >= 0",
          "The flow approaches K = 0 from BELOW and stays below. Decay on the\n"
          "         continuation is not a flow of the theory: no point of it is\n"
          "         a configuration the theory can be evaluated on.")
    inv = inv_all[kind]
    drift = float(np.max(np.abs(inv/inv[0] - 1.0)))
    check(f"G4[{kind}] [FIRST INTEGRAL] a^3 G(v) is conserved along the integration",
          f"max relative drift of a^3 G(v) = {drift:.3e}",
          drift < 1e-6,
          "relative drift < 1e-6",
          "Confirms the integration is solving the right ODE.")

# ================================================================ 4. no shield
print("\n" + "="*78)
print("PART 4 -- DOES THE EOM PROTECT K FROM GOING NEGATIVE?")
print("="*78)

u = sp.symbols('u', nonnegative=True)
mu2s = u*(2+u)/(1+u)**2
gap_expr = sp.factor(sp.together(sp.expand(2*u - mu2s)))   # = u^2(2u+3)/(1+u)^2
gap_grid = np.array([float(2.0*x - float(mu2s.subs(u, x))) for x in
                     np.logspace(-8, 6, 401)])
check("N1 [NO BARRIER] f'(K) = mu_2(sqrt K) <= 2 sqrt(K) for all K >= 0\n"
      "      -- the EOM coefficient VANISHES at the frozen point instead of\n"
      "      diverging, i.e. the opposite of a protective barrier",
      f"2u - mu_2(u) = {gap_expr}  (>= 0 for u >= 0); "
      f"min over u in [1e-8,1e6] = {gap_grid.min():.6e}; "
      f"f'(1e-2) = {float(mu2s.subs(u, 0.1)):.6e}, f'(1e-8) = {float(mu2s.subs(u, 1e-4)):.6e}",
      gap_grid.min() >= 0.0 and float(mu2s.subs(u, 1e-4)) <= 2e-4,
      "2u - mu_2(u) >= 0 on the grid, and f'(K) <= 2 sqrt(K) numerically",
      "A protecting mechanism would make the coefficient LARGE near the boundary\n"
      "         (a barrier). Here it goes to ZERO: the equation simply stops\n"
      "         being an equation at K = 0.")

Ksmall = np.logspace(-2, -16, 8)
fps    = np.array([float(mu2s.subs(u, math.sqrt(k))) for k in Ksmall])
check("N2 [DEGENERACY] f'(K) -> 0 as K -> 0+ : the principal coefficient of the\n"
      "      scalar EOM degenerates at the frozen configuration",
      "f'(K) = " + ", ".join(f"{x:.3e}" for x in fps) + " for K = 1e-2 .. 1e-16",
      fps[-1] < 1e-7 and all(np.diff(fps) < 0),
      "f'(1e-16) < 1e-7 and f' decreasing in K",
      "With a vanishing principal coefficient there is no restoring force and no\n"
      "         wave operator at K = 0: the linearised EOM is 0 = 0.")

# the linearised equation about the frozen background
check("N3 [LINEARISED EOM IS EMPTY] about the frozen background the linearised\n"
      "      EOM is f'(0) * (box delta-phi) = 0 * (box delta-phi) = 0",
      f"f'(0) = mu_2(0) = {float(mu2s.subs(u, 0)):.1e}; coefficient of box delta-phi = 0",
      float(mu2s.subs(u, 0)) == 0.0,
      "f'(0) == 0 exactly",
      "There is no linear order to be stable or unstable IN. The perturbation\n"
      "         theory about the frozen background starts at second order (the\n"
      "         action is -1 + (4/3)K^{3/2} + ... near K = 0): it is cubic, not\n"
      "         quadratic, so 'stability' in the linear sense is undefined.")

# energy: no mass term / no restoring force
rho_expr = 2*u**2*mu2s - (u**2 - 2*sp.log(1+u) - 2/(1+u) + 1)
drho_du  = sp.simplify(sp.diff(rho_expr, u))
drho_vals = np.array([float(drho_du.subs(u, x)) for x in [1e-1, 1e-2, 1e-3, 1e-4]])
check("N4 [NO RESTORING FORCE] d rho/dK -> 0 as K -> 0+ (the vacuum has no mass\n"
      "      term for the scalar, so nothing pushes K back up)",
      "d rho/du at u = 1e-1,1e-2,1e-3,1e-4 : "
      + ", ".join(f"{x:.3e}" for x in drho_vals),
      drho_vals[-1] < 1e-2 and all(np.diff(drho_vals) < 0),
      "d rho/du at u=1e-4 < 1e-2 and decreasing",
      "rho = Lambda^4 (1 + (8/3) K^{3/2} + ...): K = 0 is a minimum, but a FLAT\n"
      "         one -- derivative zero, no harmonic restoring force.")

# ================================================================ 5. the domain
print("\n" + "="*78)
print("PART 5 -- HOW BIG IS A 'SMALL' PERTURBATION THAT IS STILL IN THE DOMAIN?")
print("="*78)
print("  A configuration is in the domain iff  |d_t phi| <= |grad phi|/a  POINTWISE.")
print("  A Fourier mode phi = A(t) sin(kx) therefore fails wherever cos(kx) is small.")

def viol_fraction(r):
    """Fraction of a period with K < 0 for a mode, r = |A_dot| a /(k |A|)."""
    if r >= 1.0: return 1.0
    return 1.0 - 2.0*math.atan(1.0/r)/math.pi

r_small = 1e-2
check("D1 [MODES LEAVE THE DOMAIN] a Fourier mode with any A_dot != 0 has K < 0 on\n"
      "      a set of POSITIVE measure (the antinodes of sin, where grad phi = 0)",
      f"fraction of the period with K < 0: " + ", ".join(
          f"r={r:g} -> {viol_fraction(r):.4e}" for r in [1e-3, 1e-2, 1e-1]) +
      f";  r = |A_dot| a/(k|A|)",
      viol_fraction(r_small) > 0.0,
      "violating fraction > 0 for every r > 0",
      "Even inside the 'gradient-supported' branch there is no time-dependent\n"
      "         configuration that stays in the domain everywhere. Only STATIC\n"
      "         (A_dot = 0) or strictly quasi-static ones do.")

for tag, a0 in FOOT:
    L2 = 2.0*a0/math.sqrt(G)                       # Lambda^2
    # a galaxy: |grad phi| = g = v_flat^2/r ; domain needs |phidot| <= g/a
    M   = 1.0e11*MSUN
    vf2 = math.sqrt(a0*G*M)                        # v_flat^2 = sqrt(a0 G M)
    R   = 15.0e3*PC                                # 15 kpc
    gR  = vf2/R
    vmax = gR/L2                                   # largest |v| still in domain at R
    print(f"\n  --- {tag.strip()} footing: a0 = {a0:.4e} ---")
    print(f"      Lambda^2 = 2 a0/sqrt(G) = {L2:.6e} SI")
    print(f"      M = 1e11 Msun -> v_flat^2 = {vf2:.6e} m^2/s^2, "
          f"g(15 kpc) = {gR:.6e} m/s^2")
    check(f"D2 [{tag.strip()}] [HOW SMALL IS SMALL] at 15 kpc in a 1e11 Msun galaxy the\n"
          f"      domain bound |phidot| <= g/a reads |v| = |phidot|/Lambda^2 <= "
          f"{vmax:.4e}",
          f"|v|_max = g(15 kpc)/Lambda^2 = {vmax:.6e};  "
          f"|phidot|_max = {vmax*L2:.6e} SI",
          vmax < 1e-4,
          "|v|_max < 1e-4",
          "A 'small' perturbation has to be smaller than ~1e-4 of the natural unit\n"
          f"         Lambda^2 = 2a0/sqrt(G) just to keep sqrt(K) real AT ONE POINT.\n"
          f"         Beyond r_bad = v_flat^2/(a|phidot|) = {vf2/(1e-3*L2)/PC:.3e} pc for\n"
          f"         |v| = 1e-3 the whole outer galaxy is out of the domain.")

# ================================================================ 6. stability
print("\n" + "="*78)
print("PART 6 -- IS THE FROZEN CONFIGURATION STABLE?")
print("="*78)

cs2 = (u**2 + 3*u + 2)/(u**2 + 3*u + 4)
cs0 = float(cs2.subs(u, 0))
check("S1 [HYPERBOLIC CONE] c_s^2 = (u^2+3u+2)/(u^2+3u+4) -> 1/2 as K -> 0+:\n"
      "      the perturbation cone is real, timelike and subluminal AT the frozen\n"
      "      point, so the vacuum is not a singular point of the causal structure",
      f"c_s^2(K=0) = {cs0:.6f};  c_s^2 in "
      f"[{float(cs2.subs(u,1e-6)):.6f}, {float(cs2.subs(u,1e6)):.6f}] over u in [1e-6,1e6]",
      abs(cs0 - 0.5) < 1e-12,
      "|c_s^2(0) - 1/2| < 1e-12",
      "This is the one genuinely positive stability statement: the cone does not\n"
      "         degenerate (c_s^2 = 1/2, not 0 or infinity), unlike the cuscuton.\n"
      "         But it concerns the K > 0 side, where the perturbation's gradient\n"
      "         is spacelike -- it says nothing about a rolling perturbation.")

# count the in-domain homogeneous configurations on a grid containing v = 0
vscan  = np.concatenate([[-x for x in np.logspace(-12, 2, 700)[::-1]], [0.0],
                         np.logspace(-12, 2, 700)])
Kscan  = -vscan**2/2.0
nin    = int((Kscan >= 0.0).sum())
check("S2 [STABLE ONLY VACUOUSLY] inside the domain the homogeneous FLRW sector is\n"
      "      a single point, so 'stability' holds trivially -- the number of grid\n"
      "      configurations with K >= 0 is exactly 1 (namely v = 0)",
      f"configurations with K >= 0 out of {len(vscan)} scanned: {nin}; "
      f"the unique one is v = {float(vscan[Kscan >= 0.0][0]):.1e}; "
      f"max K = {Kscan.max():.1e}",
      nin == 1,
      "exactly 1 in-domain homogeneous configuration",
      "This is stability by ABSENCE OF ALTERNATIVES, not stability by dynamics.\n"
      "         A single point cannot be perturbed within its space -- which is\n"
      "         exactly what distinguishes an imposed constraint from an attractor.")

# ================================================================ READING
print("\n" + "="*78)
print(f"H038 READING:  {NP_} PASS / {NF_} FAIL")
print("="*78)
print(f"""
R10 -- IS phidot = 0 AN ATTRACTOR OR AN IMPOSED CONSTRAINT?
-----------------------------------------------------------
    ANSWER:  AN IMPOSED CONSTRAINT.  Not an attractor.

  1. KINEMATICS (E1-E2).  In homogeneous FLRW, K = -phidot^2/(2 Lambda^4) <= 0
     with equality iff phidot = 0.  The domain K >= 0 of the homogeneous sector
     is ONE POINT.  An attractor is a set with a neighbourhood whose flow
     converges to it; here there is no neighbourhood, so the question is not
     merely answered negatively, it is ill-posed in the homogeneous sector.

  2. REALITY (R1-R3).  Off the frozen locus sqrt(K) is imaginary and
     f'(K) = mu_2(i w) has Im = 2w/(1+w^2)^2 != 0 for every w > 0.  The
     conserved Noether current a^3 f'(K) phidot is complex for every nonzero
     phidot, so there is NO real rolling homogeneous FLRW solution at all.
     At small w the imaginary part DOMINATES (Im ~ 2w vs Re ~ 3w^2).

  3. THE INTEGRATION (G1-G4).  Granting the analytic continuation anyway, and
     integrating d_t[a^3 G(v)] = 0 for three inequivalent real projections,
     |phidot| DECAYS in expansion -- measured exponents |v| ~ a^-3/2 (modulus
     and imaginary projections), |v| ~ a^-1 (real-part projection).  But
     K < 0 at EVERY point of every trajectory: the flow converges on the
     frozen point FROM OUTSIDE the domain and never enters it.  Decay there is
     a property of a continued function, not of the theory.

  4. NO PROTECTION (N1-N4).  f'(K) <= 2 sqrt(K) -> 0 as K -> 0+.  The
     principal coefficient of the scalar EOM VANISHES at the frozen point: no
     barrier, no restoring force, and the linearised EOM is 0 = 0.  d rho/dK
     -> 0 too (rho = Lambda^4(1 + (8/3)K^{{3/2}} + ...)), so K = 0 is a flat
     minimum, not a harmonic one.  The EOM cannot protect K: it is precisely
     where the EOM stops being an equation.

  5. HOW SMALL IS SMALL (D1-D2).  The domain condition is the pointwise
     inequality |d_t phi| <= |grad phi|/a, and it is violated by any Fourier
     mode with A_dot != 0 on a set of positive measure (measured fraction
     {viol_fraction(1e-2):.2e} at r = 1e-2).  In a galaxy the bound reads
     |phidot|/Lambda^2 <~ 1e-4 at 15 kpc: 'small' means ~1e-4 of the natural
     unit Lambda^2 = 2 a0/sqrt(G), not 1e-1.

  6. STABILITY (S1-S2).  The perturbation cone is healthy at the vacuum
     (c_s^2 = 1/2, real and subluminal), and inside the domain the homogeneous
     sector is a single point, so nothing can go wrong -- vacuously.  But
     there is no linearised dynamics to be stable: f'(0) = 0 kills the linear
     term and the perturbation theory starts at second order.

WHAT THIS MEANS FOR H011.  The frozen-scalar completion is not dynamically
selected; phidot = 0 is a CONSISTENCY CONDITION (reality of the action) that
must be imposed, exactly as the aether's projector was imposed.  The gain over
the aether is unchanged -- no vector, no preferred frame, alpha_1 does not
exist -- but the cost is relabelled, not removed: it is now a domain
restriction on the scalar's time derivative instead of a preferred timelike
vector.  Any future lane that wants a rolling cosmological scalar must supply
a REAL extension of f to K < 0 (e.g. f(K) -> f(|K|), or an |X| branch); that
is a new postulate and cannot be read off the present Lagrangian.
""")

json.dump({"lane": "H038", "pass": NP_, "fail": NF_, "results": RES,
           "verdict": "IMPOSED CONSTRAINT, not an attractor",
           "decay_on_continuation": True,
           "in_domain_rolling_solution": False,
           "footings": {"a0_low": A0_LO, "a0_high": A0_HI}},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H038_results.json", "w"),
          indent=2)
print(json.dumps({"pass": NP_, "fail": NF_,
                  "verdict": "IMPOSED CONSTRAINT, not an attractor"}))
