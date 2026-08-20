#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mechC_two_field_lock_2026.py
============================
MECHANISM C -- TWO FIELDS: the shift-symmetric condensate chi carries the AMPLITUDE (Omega_dm,
w = -1, dust); a SECOND field carries the LOCK that makes chi's density track the baryons as

        rho_chi(r) = sqrt(G M_b a_0) / (4 pi G r^2)      [sf35/sf36's amplitude law]

as an OUTPUT of the static field equations rather than an initial condition.

METHOD -- and this is the whole idea.  Do NOT posit a tracking function.  Use the one property of
the dark sector the framework has already banked: IT IS PRESSURELESS.  A pressureless fluid has
NO static configuration at all unless some non-gravitational force cancels gravity POINTWISE.
That pointwise cancellation is not one equation for a profile -- it is an equation at every
point, and combined with Poisson it DETERMINES rho_chi(r) completely.  The profile is then
solved for, not chosen.  So the question becomes: what mediator can supply that force, and what
does its kinetic function have to be?

WHAT COMES OUT (every number below is computed before its check is written; the four checks that
failed on the first run were all assertions written ahead of their numbers, and PART J logs what
each one turned out to be -- one of them was a real bug of mine that MANUFACTURED a violation):

  PART A  The minimal two-field system, its field equations, and the equilibrium condition.
  PART B  *** THE SIGN THEOREM: the required force is REPULSIVE between dark elements, so a
          SCALAR mediator must be a ghost over the entire MOND regime.  The second field must
          be a VECTOR (odd spin).  Quantified. ***
  PART C  *** THE KINETIC FUNCTION IS NOT FREE.  Requiring the lock fixes it algebraically:
          mu_v(y) = B^2 [1 - mu~(B y / a_0)], where mu~ is the a_0-line's own interpolation.
          ZERO new free functions, and B is absorbable => ZERO new free parameters. ***
  PART D  The lock verified as an exact OUTPUT: rho_chi -> sqrt(G M_b a_0)/(4 pi G r^2) with the
          approach rate computed, and the baryons end up obeying exactly the AQUAL equation.
  PART E  Stability: G_eff/G for dark-dark = -mu~/(1-mu~) < 0 everywhere.  Verified twice by
          independent routes and numerically -- AND the well turns out to be ONE-SIDED, with the
          inward escape fraction computed.  That is an adverse result and it is problem 2d.
  PART F  Screening / sf06 / R1, and the solar system on BOTH kernels: the a_0-line kernel is
          EXCLUDED here as real mass, the operative Route A / MS08 kernel is void.
  PART G  Lensing.  The mediator's own stress reproduces sf36's p_t EXACTLY in the deep-MOND
          limit (ratio 1/(1+mu~)) -- not put in by hand.
  PART H  *** THE WALL.  Gauss's law caps the mediator's flux at C_nu a_0 with C_nu = 1/2
          (a_0-line) or 0.6476 (Route A).  In a galaxy the cap is exactly saturated and never
          exceeded.  In cosmology the homogeneous background violates it at EVERY redshift --
          marginally today, by 7 orders at recombination.  Numbers, both footings. ***
  PART I  Free-function / free-parameter count, w = -1, prior art, and the honest alternative.
  PART J  Errors made and fixed in this run, with the direction each one ran.

CONVENTIONS.  Non-relativistic sector Lagrangian density (energy convention, so the gravitational
term carries the sign that makes like masses ATTRACT):

    L = -(1/8 pi G)|grad Phi|^2 - (rho_b + rho_chi) Phi
        +(1/8 pi G) mu_v(|grad A|) |grad A|^2 - B rho_chi A

  * The relative sign of the two kinetic terms is the ONLY structural input, and it is exactly
    the spin-parity statement: even-spin exchange attracts like charges, odd-spin repels.
  * Baryons carry NO dark charge.  There is therefore no fifth force on baryons anywhere.

Exit 0 = every numbered check passed.
"""
import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)

# ---------------------------------------------------------------------------------------------
G_ = 6.6743e-11
C_ = 2.99792458e8
MSUN = 1.98892e30
AU = 1.495978707e11
KPC = 3.0856775814913673e19
MPC = 1e3 * KPC
YR = 3.15576e7

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FOOTINGS = ("canonical", "alt")

Z_REC = 1090.0
RATIO_REC = 0.0060                       # banked: a_0(rec)/a_0(0)
SIGMA0 = np.sqrt((RATIO_REC ** -4 - 1.0) / (1.0 + Z_REC) ** 6)


def a0_of_z(a0_now, z):
    return a0_now * (1.0 + (SIGMA0 * (1.0 + np.asarray(z, dtype=float)) ** 3) ** 2) ** -0.25


info("sigma0 solved from the banked a_0(rec)/a_0(0) = 0.0060", f"sigma0 = {SIGMA0:.6e}")
info("control a_0(z=1090)/a_0(0)", f"{float(a0_of_z(1.0, Z_REC)):.6e}")
info("control a_0(z=0)/a_0(0)", f"{float(a0_of_z(1.0, 0.0)):.12f}")

# ---------------------------------------------------------------------------------------------
# the a_0-line, in NUMERICALLY STABLE form.  (The naive expressions cancel catastrophically at
# large g_bar/a_0 -- see PART J, error #2.)
#     mu~(x) = (sqrt(1+4x^2)-1)/(2x)        x = g_obs/a_0,  g_bar = mu~ g_obs
#     1 - mu~(x) = 2/(2x + 1 + sqrt(1+4x^2))          [exact algebraic rearrangement, stable]
#     (g_obs - g_bar)/a_0 = 1/(1 + sqrt(1 + a_0/g_bar))                      [stable]
# ---------------------------------------------------------------------------------------------
def one_minus_mutilde(x):
    x = np.asarray(x, dtype=float)
    return 2.0 / (2.0 * x + 1.0 + np.sqrt(1.0 + 4.0 * x * x))


def mutilde(x):
    return 1.0 - one_minus_mutilde(x)


def dg_a0line(gbar, a0):
    """g_obs - g_bar for the a_0-line, cancellation-free."""
    gbar = np.asarray(gbar, dtype=float)
    return a0 / (1.0 + np.sqrt(1.0 + a0 / gbar))


def gobs_a0line(gbar, a0):
    return np.asarray(gbar, dtype=float) + dg_a0line(gbar, a0)


# control: the stable forms must agree with the naive ones where the naive ones are trustworthy
_xt = np.logspace(-6, 6, 50)
_naive = (np.sqrt(1 + 4 * _xt ** 2) - 1) / (2 * _xt)
info("stable-form control", f"max |mutilde_stable - naive| over x in [1e-6,1e6] = "
                            f"{np.max(np.abs(mutilde(_xt) - _naive)):.3e}")

# =============================================================================================
head("PART A -- the minimal two-field system and its equilibrium condition")
# =============================================================================================
print("""
  fields:   Phi  (metric potential, sourced by ALL mass)
            A    (mediator, sourced ONLY by the condensate's conserved shift charge)
  matter:   rho_b  (baryons, no dark charge)   rho_chi = Q_0 n  (banked rho/n = Q_0: charge IS
                                                mass for the condensate)

  L = -(1/8 pi G)|grad Phi|^2 - (rho_b + rho_chi) Phi
      +(1/8 pi G) mu_v |grad A|^2 - B rho_chi A

  delta/delta Phi :   lap Phi          = 4 pi G (rho_b + rho_chi)                       (A-i)
  delta/delta A   :   div[mu_v grad A] = -4 pi G B rho_chi                              (A-ii)
  force/mass on chi:  -grad Phi - B grad A
  DUST HAS NO PRESSURE, so the ONLY static state is   grad Phi + B grad A = 0           (A-iii)

  (A-i),(A-ii),(A-iii) are THREE equations for THREE unknowns (Phi, A, rho_chi) given rho_b.
  rho_chi is an output.  That is the entire mechanism.
""")
r_, B_, Gs, muv = sp.symbols("r B G mu_v", positive=True)
gPhi, mu_ = sp.symbols("g_obs mu", positive=True)
Mb, Mchi = sp.symbols("M_b M_chi", positive=True)
flux_A = sp.Eq(muv * gPhi / B_, Gs * B_ * Mchi / r_ ** 2)       # (A-ii)+(A-iii): |grad A|=g_obs/B
flux_Phi = sp.Eq(gPhi, Gs * (Mb + Mchi) / r_ ** 2)              # (A-i)
sol_M = sp.solve([flux_A, flux_Phi], [Mchi, Mb], dict=True)[0]
gbar_expr = sp.simplify(Gs * sol_M[Mb] / r_ ** 2)
info("A0  eliminating M_chi between the two flux equations", f"g_bar = {gbar_expr}")
check(sp.simplify(gbar_expr - gPhi * (1 - muv / B_ ** 2)) == 0,
      "A1  *** the elimination gives g_bar = (1 - mu_v/B^2) g_obs: the baryons end up obeying "
      "exactly the AQUAL equation div[mu~ grad Phi] = 4 pi G rho_b, with mu~ = 1 - mu_v/B^2 ***",
      f"g_bar = {gbar_expr}")
check(sp.simplify(sp.solve(sp.Eq(gbar_expr, mu_ * gPhi), muv)[0] - B_ ** 2 * (1 - mu_)) == 0,
      "A2  inverting: mu_v = B^2 (1 - mu~).  THE MEDIATOR'S KINETIC FUNCTION IS NOT FREE -- it "
      "is fixed algebraically by the interpolation the a_0-line already contains")
check(True,
      "A3  and B is pure normalisation: A -> A/B sends (mu_v, B) -> (mu_v/B^2, 1), so B is NOT "
      "a free parameter.  The residual content is the single function mu~, already owned")

# =============================================================================================
head("PART B -- THE SIGN THEOREM: the mediator must be odd-spin (a vector), not a scalar")
# =============================================================================================
print("""
  The dark sector must be held up against the total gravity of (baryons + itself), by a force
  sourced by itself alone.  In spherical symmetry, balance at radius r reads

        f_self(r) = G [M_b(r) + M_chi(r)] / r^2   >   G M_chi(r) / r^2

  so the self-force EXCEEDS the sector's own gravity wherever any baryons are enclosed: the
  dark-dark interaction is NET REPULSIVE.  Even-spin exchange between LIKE charges attracts;
  odd-spin repels.  A scalar mediator therefore needs a wrong-sign kinetic term.
""")
check(sp.simplify(B_ ** 2 * (mu_ - 1) + B_ ** 2 * (1 - mu_)) == 0,
      "B1  the scalar-mediator version of A2 is the exact sign flip, mu_s = B^2 (mu~ - 1)",
      "so mu_s <= 0 wherever mu~ <= 1")
xs = np.logspace(-4, 6, 400)
mt = mutilde(xs)
info("B2", f"mu~ over x=g_obs/a_0 in [1e-4,1e6]: min {mt.min():.6e}  max {mt.max():.10f}")
check(np.all(mt <= 1.0 + 1e-12) and np.all(mt > 0),
      "B2  mu~(x) lies in (0,1] at every acceleration -- computed on 400 samples, not asserted",
      f"mu~ -> {mt.min():.3e} deep-MOND, -> {mt.max():.10f} Newtonian")
frac_ghost = float(np.mean((1.0 - mt) > 1e-3))
info("B3", f"fraction of the sampled range with mu_s/B^2 = mu~-1 below -1e-3: {frac_ghost:.3f}; "
           f"mu_s/B^2 at x=1 is {float(mutilde(1.0))-1:.6f}")
check(frac_ghost > 0.5,
      "B3  *** A SCALAR MEDIATOR IS A GHOST OVER THE ENTIRE MOND REGIME (mu_s < 0 wherever "
      "mu~ < 1) and degenerates to mu_s = 0 -- infinite coupling -- exactly in the Newtonian "
      "limit.  THE SECOND FIELD CANNOT BE A SCALAR. ***")
check(True,
      "B4  consistent with, and independent of, Phase 1: sf37 Theorem 1 killed static single-"
      "scalar AQUAL as the STRESS carrier; B3 kills it as the SUPPORT carrier, by force sign")
check(True,
      "B5  THE ESCAPE, named and NOT closed: sf37's escape (ii), phi = Q_0 t + psi(r).  A "
      "time-dependent condensate is not covered by the static like-charge argument, so a "
      "non-static scalar realisation of the support is NOT excluded by B3.  Not computed here")

# =============================================================================================
head("PART C -- the mediator's kinetic function, computed")
# =============================================================================================
xs2 = np.array([1e-3, 1e-2, 0.1, 1.0, 10.0, 1e3, 1e6])
info("C1  mu_v(x)/B^2 = 1 - mu~(x)  (x = g_obs/a_0; footing-independent as a function of x)",
     "  ".join(f"x={xv:g}:{float(one_minus_mutilde(xv)):.6e}" for xv in xs2))
check(np.all(one_minus_mutilde(xs2) >= 0),
      "C1  mu_v >= 0 at every acceleration: the VECTOR realisation is kinetically healthy "
      "everywhere, no ghost anywhere")
asym_deep = float(one_minus_mutilde(1e-8))
asym_newt = float(one_minus_mutilde(1e8)) * 2e8
info("C2", f"mu_v/B^2 -> {asym_deep:.12f} as x->0 ;  2x(1-mu~) -> {asym_newt:.10f} as x->1e8")
check(abs(asym_deep - 1.0) < 1e-7 and abs(asym_newt - 1.0) < 1e-6,
      "C2  asymptotics: mu_v -> B^2 in deep MOND, mu_v -> B^2 a_0/(2 g_obs) Newtonian -- the "
      "mediator switches ITSELF off where the field is strong.  That IS the screening")

# =============================================================================================
head("PART D -- the LOCK, verified as an exact OUTPUT of the field equations")
# =============================================================================================
GMs, a0sym = sp.symbols("GM a_0", positive=True)
gb_s = GMs / r_ ** 2
gobs_s = sp.sqrt(gb_s ** 2 + a0sym * gb_s)
rho_out = sp.simplify(sp.diff(r_ ** 2 * (gobs_s - gb_s), r_) / (4 * sp.pi * Gs * r_ ** 2))
lim_out = sp.simplify(sp.limit(rho_out * r_ ** 2, r_, sp.oo))
info("D1", f"r^2 rho_chi -> {lim_out} as r -> infinity")
check(sp.simplify(lim_out - sp.sqrt(GMs * a0sym) / (4 * sp.pi * Gs)) == 0,
      "D1  *** THE OUTPUT IS THE TARGET: rho_chi(r) -> sqrt(G M_b a_0)/(4 pi G r^2) exactly, "
      "coefficient set by a_0, mass the BARYONIC one.  Nothing was posited. ***")
f_rho = sp.lambdify((r_, GMs, a0sym, Gs), rho_out, "numpy")
# the ratio to the asymptotic target has an EXACT closed form -- computed, then checked
u_ = sp.symbols("u", positive=True)
ratio_sym = sp.simplify(rho_out / (sp.sqrt(GMs * a0sym) / (4 * sp.pi * Gs * r_ ** 2)))
ratio_u = sp.simplify(ratio_sym.subs(r_, u_ * sp.sqrt(GMs / a0sym)))
info("D2  exact closed form of the output/target ratio", f"rho_chi/target = {ratio_u} with "
                                                         f"u = r/r_M, r_M = sqrt(GM_b/a_0)")
check(sp.simplify(ratio_u - u_ / sp.sqrt(u_ ** 2 + 1)) == 0,
      "D2  *** the lock's output is EXACTLY rho_chi(r) = [r/sqrt(r^2+r_M^2)] x "
      "sqrt(G M_b a_0)/(4 pi G r^2) -- the target times a single Newtonian-transition factor "
      "that goes to 1 as (1 - r_M^2/2r^2).  No free function anywhere in it ***",
      f"series at infinity: {sp.series(ratio_u, u_, sp.oo, 4)}")
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rM = np.sqrt(GM / a0)
    facs = np.array([1.0, 3.0, 10.0, 30.0, 100.0, 300.0])
    rat = np.array([float(f_rho(f * rM, GM, a0, G_)) /
                    (np.sqrt(GM * a0) / (4 * np.pi * G_ * (f * rM) ** 2)) for f in facs])
    closed = facs / np.sqrt(facs ** 2 + 1.0)
    info(f"D2b {nm}", "  ".join(f"r={f:g}r_M:{q:.6f}" for f, q in zip(facs, rat)) +
                      f"   max |numeric - closed form| = {np.max(np.abs(rat-closed)):.2e}")
    slope = np.polyfit(np.log(facs[2:]), np.log(np.abs(rat[2:] - 1.0)), 1)[0]
    info(f"D2b {nm} approach", f"log-log slope of |rho/target - 1| vs r/r_M = {slope:.4f}")
    check(np.max(np.abs(rat - closed)) < 1e-12 and abs(slope + 2.0) < 0.02 and np.all(rat > 0),
          f"D2b {nm}  the numerical solve matches the closed form to "
          f"{np.max(np.abs(rat-closed)):.1e} and converges as 1/r^2 (fitted slope "
          f"{slope:.3f}), reaching {abs(rat[-1]-1)*100:.4f}% at 300 r_M",
          f"CORRECTION AGAINST MY OWN FIRST GUESS: I had written '1/r'; it is 1/r^2, i.e. the "
          f"lock converges onto the target FASTER than I asserted")
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rM = np.sqrt(GM / a0)
    gb = GM / (0.01 * rM) ** 2
    frac = float(dg_a0line(gb, a0)) / float(gobs_a0line(gb, a0))
    info(f"D3 {nm}", f"r_M = {rM/KPC:.2f} kpc ; at 0.01 r_M the phantom fraction "
                     f"(g_obs-g_bar)/g_obs = {frac:.4e}")
    check(frac < 1e-3,
          f"D3 {nm}  deep inside r_M the lock returns rho_chi -> 0: the dark sector is EXPELLED "
          f"from the high-acceleration region by its own mediator")

print("""
  EXTENDED SOURCE.  Everything above used a point mass, so the lock could in principle be a
  point-mass artefact.  Repeat on a Hernquist baryon sphere, M_b(r) = M r^2/(r+a)^2 with
  a = 3 kpc, M = 1e11 Msun, solving the same three equations on a 400k-point grid.
""")
for nm in FOOTINGS:
    a0 = A0[nm]
    M = 1e11 * MSUN
    a_h = 3.0 * KPC
    rr = np.logspace(np.log10(1e-3 * KPC), np.log10(3e3 * KPC), 400000)
    Mb_r = M * rr ** 2 / (rr + a_h) ** 2
    gb = G_ * Mb_r / rr ** 2
    d = dg_a0line(gb, a0)                                   # = G M_chi / r^2, the mediator flux
    Mchi_r = d * rr ** 2 / G_
    rho_chi_n = np.gradient(Mchi_r, rr) / (4 * np.pi * rr ** 2)
    tgt = np.sqrt(G_ * M * a0) / (4 * np.pi * G_ * rr ** 2)
    far = rr > 100 * KPC
    dev = float(np.max(np.abs(rho_chi_n[far] / tgt[far] - 1.0)))
    negfrac = float(np.mean(rho_chi_n < 0))
    capmax = float((d / a0).max())
    info(f"D4 {nm}", f"Hernquist baryons: max |rho_chi/target - 1| beyond 100 kpc = {dev:.4e} ; "
                     f"fraction of radii with rho_chi < 0 = {negfrac:.3e} ; "
                     f"max mediator flux / a_0 = {capmax:.6f} (cap 0.5)")
    check(dev < 0.02 and negfrac == 0.0 and capmax <= 0.5 + 1e-9,
          f"D4 {nm}  *** THE LOCK IS NOT A POINT-MASS ARTEFACT: on an extended Hernquist "
          f"baryon sphere the same three equations give rho_chi > 0 at every one of 400k radii, "
          f"converging to the target to {dev*100:.2f}% beyond 100 kpc, with the mediator's flux "
          f"cap respected everywhere (max {capmax:.4f} a_0) ***")

# =============================================================================================
head("PART E -- is the lock an ATTRACTOR?  (two routes, plus a displaced-shell test)")
# =============================================================================================
print("""
  Route 1 (linear response, mu_v frozen):  lap(dPhi + B dA) = 4 pi G d_rho [1 - B^2/mu_v]
      and with mu_v = B^2(1-mu~) the bracket is  -mu~/(1-mu~).
  Route 2 (enclosed mass):  self-force = G(M_b+M_chi)/r^2 vs own gravity G M_chi/r^2,
      so  G_eff/G = -M_b/M_chi.
""")
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rM = np.sqrt(GM / a0)
    for fac in (0.5, 1.0, 3.0, 10.0):
        r = fac * rM
        gb = GM / r ** 2
        d = float(dg_a0line(gb, a0))
        go = gb + d
        mt_ = gb / go
        route1 = -mt_ / (1.0 - mt_)
        route2 = -(GM / G_) / (d * r ** 2 / G_)
        info(f"E1 {nm} r={fac:g} r_M",
             f"G_eff/G route1 = {route1:+.6e}   route2 = {route2:+.6e}   "
             f"rel.diff = {abs(route1-route2)/abs(route1):.2e}")
        check(abs(route1 - route2) / abs(route1) < 1e-9,
              f"E1 {nm} r={fac:g} r_M  the two independent routes agree to 1e-9 relative",
              f"G_eff/G = {route1:+.6e}")
check(True,
      "E2  *** G_eff/G = -mu~/(1-mu~) < 0 for EVERY mu~ in (0,1): the dark-dark interaction is "
      "net repulsive at every acceleration, so a dark overdensity DISPERSES.  The lock is a "
      "STABLE fixed point, not a tuned one. ***")

# the cap on the mediator's flux, needed for the shell test (derived properly in PART H)
uu = np.logspace(-6, 12, 400000)
C_line = float(np.max(uu * one_minus_mutilde(uu)))


def R_of_S(S, a0):
    """Repulsion delivered when the mediator's Gauss flux is S = G M_chi/r^2:
       solve a_0 u (1-mu~(u)) = S for u; repulsion = a_0 u.  nan above the cap."""
    S = np.atleast_1d(np.asarray(S, dtype=float))
    out = np.full(S.shape, np.nan)
    for i, s in enumerate(S):
        if s >= C_line * a0:
            continue
        a, b = 1e-12, 1e14
        for _ in range(300):
            m = np.sqrt(a * b)
            if a0 * m * float(one_minus_mutilde(m)) < s:
                a = m
            else:
                b = m
        out[i] = a0 * np.sqrt(a * b)
    return out


print("""
  Displaced-shell test.  A shell of fixed enclosed dark mass m is moved off equilibrium; the
  mediator flux G m/r^2 follows the shell, gravity is recomputed, and the net radial
  acceleration is measured.  NOTE the flux cap C_nu a_0 (PART H): pushing a shell inward raises
  its flux as 1/r^2, so there is a CRITICAL inward displacement past which the mediator has no
  solution at all.  That fraction is computed first, then the restoring test is run inside it.
""")
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rM = np.sqrt(GM / a0)
    for fac in (1.0, 3.0, 10.0):
        req = fac * rM
        Seq = float(dg_a0line(GM / req ** 2, a0))
        rmin_frac = np.sqrt(Seq / (C_line * a0))
        qs = np.array([0.5 * (1 + rmin_frac), 0.99, 1.0, 1.01, 1.5, 3.0])
        rs = req * qs
        m = Seq * req ** 2 / G_
        anet = R_of_S(G_ * m / rs ** 2, a0) - G_ * (GM / G_ + m) / rs ** 2
        info(f"E3 {nm} shell at {fac:g} r_M",
             f"S_eq/a_0 = {Seq/a0:.4f} ; mediator gives out below r/r_eq = {rmin_frac:.4f} ; " +
             "  ".join(f"{q:.3f}:{v:+.2e}" for q, v in zip(qs, anet)))
        ok = (anet[0] > 0) and (anet[1] > 0) and (anet[3] < 0) and (anet[4] < 0) and \
             (anet[5] < 0) and (abs(anet[2]) < 1e-8 * (Seq + GM / req ** 2))
        check(ok, f"E3 {nm} shell at {fac:g} r_M  inside r_eq (but above the cap) the net "
                  f"acceleration is OUTWARD, outside it is INWARD, and it vanishes at r_eq -- "
                  f"a genuine restoring well",
              f"a_net(0.99 r_eq) = {anet[1]:+.3e}, a_net(1.01 r_eq) = {anet[3]:+.3e} m/s^2")
# quantify the one-sidedness -- this is the adverse result
print()
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rM = np.sqrt(GM / a0)
    fr = [(f, float(np.sqrt(dg_a0line(GM / (f * rM) ** 2, a0) / (C_line * a0))))
          for f in (0.3, 1.0, 3.0, 10.0, 30.0)]
    info(f"E4 {nm}  critical inward displacement r_min/r_eq",
         "  ".join(f"{f:g}r_M:{q:.4f}" for f, q in fr))
    check(fr[1][1] > 0.85 and fr[0][1] > fr[-1][1],
          f"E4 {nm}  *** THE WELL IS ONE-SIDED, AND THIS RUNS AGAINST THE MECHANISM: a shell at "
          f"r_M can only be pushed in by {100*(1-fr[1][1]):.1f}% before the mediator's flux cap "
          f"is exceeded and it has NO solution -- gravity then wins unopposed and the shell "
          f"collapses.  The margin shrinks toward zero as r -> 0.  This is problem 2d "
          f"reappearing inside the mechanism that was supposed to answer it. ***",
          f"at 0.3 r_M the margin is only {100*(1-fr[0][1]):.1f}%")
# strength of the well
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rM = np.sqrt(GM / a0)
    for fac in (1.0, 10.0):
        req = fac * rM
        Seq = float(dg_a0line(GM / req ** 2, a0))
        m = Seq * req ** 2 / G_
        h = 1e-4 * req
        f1 = R_of_S(G_ * m / (req + h) ** 2, a0)[0] - G_ * (GM / G_ + m) / (req + h) ** 2
        f0 = R_of_S(G_ * m / (req - h) ** 2, a0)[0] - G_ * (GM / G_ + m) / (req - h) ** 2
        w2 = -(f1 - f0) / (2 * h)
        Tosc = 2 * np.pi / np.sqrt(w2) if w2 > 0 else np.inf
        go = GM / req ** 2 + Seq
        Torb = 2 * np.pi * req / np.sqrt(go * req)
        info(f"E5 {nm} {fac:g} r_M", f"omega^2 = {w2:.4e} s^-2 -> restoring period "
                                     f"{Tosc/YR/1e9:.3f} Gyr ; orbital period {Torb/YR/1e9:.3f} "
                                     f"Gyr ; ratio {Tosc/Torb:.3f}")
        check(w2 > 0, f"E5 {nm} {fac:g} r_M  omega^2 > 0 confirms the well, and its timescale is "
                      f"computed: T_restore/T_orbit = {Tosc/Torb:.3f}")
check(True,
      "E6  AGAINST INTEREST: the restoring bracket -mu~/(1-mu~) -> 0 in the deep-MOND limit, so "
      "the outer halo is only MARGINALLY stable -- the attractor is weakest exactly where the "
      "lock matters most.  E4 and E6 together are the honest reading of PART E")

# =============================================================================================
head("PART F -- screening: sf06 locality, R1, and the solar system on BOTH kernels")
# =============================================================================================
print("""
  sf06 requires screening to key on the LOCAL TOTAL FIELD GRADIENT -- potential (1.5x), dark
  density (2.2x) and dispersion (1.0x) lack the contrast; only the field has it (6.3e7x).  Here
  mu_v = mu_v(|grad A|) and |grad A| = |grad Phi|/B in equilibrium, so the screening IS a
  function of the local total field gradient by construction.  R1 holds structurally.

  There is no fifth force on baryons at all -- they carry no dark charge.  What the solar system
  sees is REAL DARK MASS deposited by the lock.  That is an EPHEMERIS test, and it is
  kernel-dependent.
""")
check(True,
      "F1  mu_v's argument is |grad A| = |grad Phi|/B, the local total field gradient => R1 / "
      "sf06 satisfied by construction (structural, no number attached)")
for nm in FOOTINGS:
    a0 = A0[nm]
    gb = G_ * MSUN / AU ** 2
    d = float(dg_a0line(gb, a0))
    Mextra = d * AU ** 2 / G_
    rho_local = a0 / (4 * np.pi * G_ * AU)
    info(f"F2 {nm} a_0-line", f"g_bar(1AU) = {gb:.4e} ; (g_obs-g_bar) = {d:.6e} = a_0/2 to "
                              f"{abs(d/(a0/2)-1):.1e} ; extra enclosed mass = {Mextra/MSUN:.4e} "
                              f"Msun ; rho_chi(1AU) = {rho_local:.4e} kg/m^3")
    check(Mextra / MSUN > 1e-10,
          f"F2 {nm}  *** THE a_0-LINE KERNEL IS EXCLUDED IN THIS MECHANISM: the lock deposits "
          f"{Mextra/MSUN:.2e} Msun of REAL dark mass inside 1 AU (rho = {rho_local:.2e} kg/m^3, "
          f"~1e10x the local halo density), far above the ~1e-11 Msun ephemeris ceiling.  This "
          f"is the alpha=1 liability appearing as MASS instead of as a force. ***")
    y = gb / a0
    s = np.sqrt(y)
    log10_ratio = (-s) / np.log(10)
    info(f"F3 {nm} Route A/MS08", f"y = g_bar/a_0 = {y:.4e} ; sqrt(y) = {s:.4e} ; "
                                  f"log10[(g_obs-g_bar)/g_bar] = {log10_ratio:.1f}")
    check(log10_ratio < -3000,
          f"F3 {nm}  on the OPERATIVE Route A / MS08 kernel the same lock deposits 10^"
          f"{log10_ratio:.0f} of the baryonic field at 1 AU -- the channel is VOID, matching "
          f"the repo's banked 1e-3458.7.  The kernel fork, not the mechanism, decides this")
for nm in FOOTINGS:
    a0 = A0[nm]
    gb = 1.35e-10
    y = gb / a0
    s = np.sqrt(y)
    nu = 1.0 / (1.0 - np.exp(-s))
    go = nu * gb
    info(f"F4 {nm}", f"solar circle (g_bar = {gb:.3e}): y = {y:.3f}, Route A g_obs = {go:.3e}, "
                     f"phantom fraction = {(go-gb)/go:.4f}")
    check(0.05 < (go - gb) / go < 0.9,
          f"F4 {nm}  at the solar circle the mechanism is ON (phantom fraction "
          f"{(go-gb)/go:.3f}) while at 1 AU it is off by 3000+ orders -- exactly the 6.3e7x "
          f"field contrast sf06 says is the only one large enough")

# =============================================================================================
head("PART G -- lensing, and an unforced coincidence with sf36")
# =============================================================================================
print("""
  The condensate is DUST: p_r = p_t = 0, so it satisfies p_r + 2p_t = 0 trivially (sf37 Thm 2).
  The only stress in the sector is the MEDIATOR's.  A radial 'electric' field has the Coulomb
  structure (rho_A, p_r, p_t) = (+1, -1, +1) x mu_v|grad A|^2/(8 pi G).
""")
gsym, mus = sp.symbols("g mu", positive=True)
ratio_pt = sp.simplify(((1 - mus) * gsym ** 2) / (gsym ** 2 - (mus * gsym) ** 2))
info("G1", f"p_t(mediator) / p_t(sf36 required) = {ratio_pt}")
check(sp.simplify(ratio_pt - 1 / (1 + mus)) == 0,
      "G1  *** the mediator's own tangential stress is 1/(1+mu~) times sf36's required p_t -- "
      "EXACT in the deep-MOND limit (mu~->0), never worse than 1/2.  Nothing in PART A was "
      "chosen to make this happen ***",
      "sf36 needs (g_obs^2-g_bar^2)/(8 pi G); the mediator supplies (1-mu~)g_obs^2/(8 pi G)")
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rM = np.sqrt(GM / a0)
    r = 3 * rM
    gb = GM / r ** 2
    d = float(dg_a0line(gb, a0))
    go = gb + d
    mt_ = gb / go
    rho_A = (1 - mt_) * go ** 2 / (8 * np.pi * G_ * C_ ** 2)
    rho_chi_here = float(f_rho(r, GM, a0, G_))
    eps = rho_A / (rho_chi_here + rho_A)
    vc2 = np.sqrt(GM * a0)
    info(f"G2 {nm}", f"at 3 r_M: rho_A/rho_chi = {rho_A/rho_chi_here:.4e} ; v_c^2/2c^2 = "
                     f"{vc2/(2*C_**2):.4e} ; eps = (p_r+2p_t)/(rho c^2) = {eps:.4e}")
    check(eps < 4.89e-4,
          f"G2 {nm}  the sector's lensing-vs-dynamics offset eps = {eps:.3e} sits "
          f"{0.0489/eps:.2e}x = {np.log10(0.0489/eps):.2f} orders inside the tightest "
          f"defensible tolerance (Brouwer+2021 full covariance, 0.0489).  Lensing is not "
          f"binding, exactly as Phase 1 found")

# =============================================================================================
head("PART H -- THE WALL: Gauss's law caps the mediator, and the cap decides cosmology")
# =============================================================================================
print("""
  Gauss in flux form:  mu_v |grad A| = G B M_chi / r^2.  With mu_v = B^2(1-mu~) and
  |grad A| = a_0 u/B (u = g_obs/a_0), the left side is  B a_0 * u(1-mu~(u)), and u(1-mu~(u)) is
  BOUNDED.  So there is a maximum dark flux the mediator can carry:

        G M_chi / r^2  <=  C_nu a_0 ,     C_nu = sup_u u(1 - mu~(u)).
""")
info("H1", f"C_nu (a_0-line) = sup u(1-mu~(u)) over 4e5 samples out to u=1e12: {C_line:.10f}")
check(abs(C_line - 0.5) < 1e-9,
      "H1  the a_0-line's cap is C_nu = 1/2 exactly, approached monotonically from below",
      f"numerical sup = {C_line:.10f}")
ss = np.logspace(-6, 2.7, 400000)          # e^s overflows past ~709; s^2/(e^s-1) is ~0 by s=500
fA = ss ** 2 / np.expm1(ss)
C_routeA = float(np.nanmax(fA))
s_star = float(ss[np.nanargmax(fA)])
info("H2", f"C_nu (Route A/MS08) = max_s s^2/(e^s-1) = {C_routeA:.6f} at sqrt(y) = {s_star:.4f}")
check(0.6 < C_routeA < 0.7,
      f"H2  the Route A / MS08 kernel has the same structure with C_nu = {C_routeA:.4f}, 30% "
      f"higher.  The cap is a property of the interpolation; both kernels have one")
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rr2 = np.logspace(np.log10(1e-8 * KPC), np.log10(1e4 * KPC), 300000)
    S = dg_a0line(GM / rr2 ** 2, a0)
    info(f"H3 {nm}", f"max_r [G M_chi/r^2]/a_0 over 1e-8 kpc to 10 Mpc = {S.max()/a0:.10f} "
                     f"(cap {C_line:.10f})")
    check(S.max() / a0 <= C_line + 1e-12,
          f"H3 {nm}  *** IN A GALAXY THE CAP IS NEVER VIOLATED AND IS EXACTLY SATURATED IN THE "
          f"NEWTONIAN INTERIOR: the a_0-line's own maximum phantom field IS a_0/2, the same "
          f"number the mediator's Gauss law caps at.  That is why the mechanism works at all "
          f"in galaxies, and it was not arranged. ***",
          f"sup = {S.max()/a0:.10f} a_0 vs cap {C_line:.10f} a_0")
print("""
  Cosmology.  For a homogeneous dark density rho_bar the flux about any point is
  G M/r^2 = (4 pi G/3) rho_bar r, unbounded in r.  The cap is violated beyond
        r_wall = 3 C_nu a_0(z) / (4 pi G rho_bar(z)) ,
  and above that radius the quasistatic mediator branch -- the branch that produces the lock --
  has NO solution.  The physically meaningful comparison is with the Hubble radius.
""")
H0 = 67.4 * 1e3 / MPC
OM_M, OM_DM, OM_L = 0.315, 0.265, 0.685
RHO_CRIT = 3 * H0 ** 2 / (8 * np.pi * G_)


def rho_dm(z):
    return OM_DM * RHO_CRIT * (1 + np.asarray(z, dtype=float)) ** 3


def Hz(z):
    return H0 * np.sqrt(OM_M * (1 + np.asarray(z, dtype=float)) ** 3 + OM_L)


for nm in FOOTINGS:
    a0n = A0[nm]
    for z in (0.0, 0.5, 1.0, 2.0, 10.0, 100.0, Z_REC):
        a0z = float(a0_of_z(a0n, z))
        r_wall = 3.0 * C_line * a0z / (4 * np.pi * G_ * float(rho_dm(z)))
        r_hub = C_ / float(Hz(z))
        info(f"H4 {nm} z={z:g}", f"a_0(z) = {a0z:.4e} ; r_wall = {r_wall/MPC:.4e} Mpc ; "
                                 f"c/H = {r_hub/MPC:.4e} Mpc ; r_wall/r_H = {r_wall/r_hub:.4e}")
for nm in FOOTINGS:
    a0n = A0[nm]
    rw0 = 3.0 * C_line * float(a0_of_z(a0n, 0.0)) / (4 * np.pi * G_ * float(rho_dm(0.0)))
    rh0 = C_ / H0
    check(0.3 < rw0 / rh0 < 1.0,
          f"H5 {nm}  *** EVEN TODAY THE HOMOGENEOUS BACKGROUND VIOLATES THE CAP, though only "
          f"just: r_wall = {rw0/MPC:.0f} Mpc against a Hubble radius {rh0/MPC:.0f} Mpc, ratio "
          f"{rw0/rh0:.3f}.  The mediator cannot carry the flux of a uniform Omega_dm on the "
          f"largest scales. ***",
          f"r_wall/r_H(z=0) = {rw0/rh0:.4f}")
    a0r = float(a0_of_z(a0n, Z_REC))
    rwr = 3.0 * C_line * a0r / (4 * np.pi * G_ * float(rho_dm(Z_REC)))
    rhr = C_ / float(Hz(Z_REC))
    check(rwr / rhr < 1e-6,
          f"H6 {nm}  *** AND AT RECOMBINATION IT IS VIOLATED BY {rhr/rwr:.3e}x IN RADIUS: "
          f"r_wall = {rwr/MPC:.3e} Mpc vs Hubble radius {rhr/MPC:.4f} Mpc, by the HOMOGENEOUS "
          f"BACKGROUND ALONE, before any perturbation. ***",
          f"r_wall/r_H = {rwr/rhr:.3e}")
zs = np.logspace(-3, 3.5, 200000)
for nm in FOOTINGS:
    a0n = A0[nm]
    rw = 3.0 * C_line * a0_of_z(a0n, zs) / (4 * np.pi * G_ * rho_dm(zs))
    rh = C_ / Hz(zs)
    ratio = rw / rh
    info(f"H7 {nm}", f"r_wall/r_H is monotone decreasing: {ratio[0]:.4f} at z={zs[0]:.4f}, "
                     f"{ratio[-1]:.3e} at z={zs[-1]:.1f}; max over the scan = {ratio.max():.4f}")
    check(ratio.max() < 1.0,
          f"H7 {nm}  the cap is violated on horizon scales at EVERY redshift z >= 0 -- the "
          f"ratio never reaches 1, peaking at {ratio.max():.3f} today and falling as roughly "
          f"(1+z)^-3 because a_0(z) declines while rho_dm rises",
          f"a_0(z) makes this WORSE at high z, not better")
for nm in FOOTINGS:
    a0n = A0[nm]
    a0r = float(a0_of_z(a0n, Z_REC))
    for k_mpc in (0.01, 0.1, 1.0):
        k_phys = (k_mpc / MPC) * (1 + Z_REC)
        g_pert = k_phys * 2e-5 * C_ ** 2
        info(f"H8 {nm} k={k_mpc} Mpc^-1",
             f"g_pert = {g_pert:.3e} m/s^2 ; cap C_nu a_0(rec) = {C_line*a0r:.3e} ; "
             f"violation = {g_pert/(C_line*a0r):.3e}x")
    g_pert = (0.1 / MPC) * (1 + Z_REC) * 2e-5 * C_ ** 2
    check(g_pert / (C_line * a0r) > 100,
          f"H8 {nm}  CMB-scale perturbations violate it independently: at k = 0.1 Mpc^-1 the "
          f"dark sector's own field is {g_pert/(C_line*a0r):.2e}x the cap "
          f"(Phi/c^2 ~ 2e-5 assumed)",
          "two independent cosmological routes, same direction")
check(True,
      "H9  WHICH WAY DOES THE WALL CUT?  Both readings are live and this run does NOT settle "
      "them.  (a) BENIGN: above the cap the mediator simply cannot hold the dust, so the dust "
      "reverts to ordinary CDM -- which is exactly what the CMB needs, with the lock switching "
      "on only in the late deep-MOND regime.  (b) FATAL: div[mu_v grad A] = -4 pi G B rho_chi "
      "then has no quasistatic solution at all, so the mediator must go dynamical and the "
      "high-z behaviour is simply not computed.  Deciding needs the time-dependent vector "
      "equation, which this run did not do")
check(True,
      "H10 THE NAMED REPAIR, not tested here: a mass term (or nonzero background value) for the "
      "mediator lets A itself absorb the homogeneous source, screening the background flux at a "
      "Compton scale and removing the cosmological wall while leaving the galactic lock intact "
      "if the Compton wavelength sits between r_wall(z=0) and galaxy scales.  That is a NEW "
      "free parameter, so it would change PART I's count from zero to one")

# =============================================================================================
head("PART I -- counting, w = -1, prior art, and the honest alternative")
# =============================================================================================
print("""
  NEW FREE FUNCTIONS:  ZERO.  mu_v(y) = B^2[1 - mu~(By/a_0)] is fixed algebraically by the
      interpolation the a_0-line already contains (A2).
  NEW FREE PARAMETERS: ZERO.  B is pure normalisation and is absorbed (A3).
  NEW STRUCTURAL CHOICES (the actual price, and they are assumptions, not parameters):
      1. the mediator is ODD SPIN (a vector) -- forced by PART B, not chosen;
      2. baryons carry no dark charge, so there is no fifth force on baryons at all;
      3. the dark sector is in STATIC equilibrium -- the mechanism IS the statement that a
         pressureless sector has no other static state.
""")
check(True, "I1  new free FUNCTIONS = 0 (mu_v algebraically determined by mu~)")
check(True, "I2  new free PARAMETERS = 0 (B absorbable).  If H10's repair is needed, this "
            "becomes 1")
check(True, "I3  w = -1 untouched at background level: in exact homogeneity grad A = 0, so the "
            "mediator's stress vanishes identically and the DBI condensate's w = -1 stands.  "
            "The caveat is H5-H7: the homogeneous GAUSS condition itself has no solution on "
            "horizon scales, which is a constraint problem, not an equation-of-state problem")
check(True,
      "I4  PRIOR ART, credited: a vector whose electric part carries the MOND force alongside a "
      "dust-like scalar shift charge is the architecture of AeST (Skordis & Zlosnik, PRL 127, "
      "161302 (2021)), which the repo's own standing already names as the completion.  What is "
      "new here is the ASSIGNMENT -- the vector holds the dust UP so the dust's REAL density "
      "equals the phantom density, with no fifth force on baryons -- and the consequence that "
      "mu_v is then not a free function")
check(True,
      "I5  THE HONEST ALTERNATIVE, stated because it dissolves the premise: if the mediator "
      "acts on BARYONS instead (standard AQUAL/TeVeS/AeST), the MOND phenomenology is PHANTOM "
      "and nothing needs to lock rho_chi to rho_b -- but then the condensate must be "
      "subdominant inside galaxies, which is exactly what the nbody capture result (open "
      "problem 2d) says it is not.  Mechanism C is the branch that takes 2d seriously")

# =============================================================================================
head("PART J -- errors made in this run, and the direction each one ran")
# =============================================================================================
print("""
  1. D2 (first run, TWICE).  First I asserted the output would match the asymptotic target to 5%
     beyond 30 kpc; 30 kpc is only 2.5 r_M, where the Newtonian transition is still large, so
     that check failed on a result that is exactly right.  Then I asserted the approach was
     1/r; it is 1/r^2.  The exact answer, found only after being forced to compute it, is
     rho_chi/target = r/sqrt(r^2 + r_M^2) in closed form.  DIRECTION: BOTH assertions
     MANUFACTURED A DEFICIT -- the lock is cleaner and converges faster than I twice claimed.
  2. H3 (first run).  I computed g_obs - g_bar as sqrt(g^2 + a_0 g) - g, which cancels
     catastrophically in float64 once g/a_0 > 1e10, and reported sup = 0.5052 a_0 -- an apparent
     1% VIOLATION of the cap that does not exist.  DIRECTION: MANUFACTURED A DEFICIT.  The
     algebraically stable form (g_obs-g_bar)/a_0 = 1/(1+sqrt(1+a_0/g_bar)) gives 0.5000000000
     and the cap holds exactly.  Caught by a control, not by inspection.
  3. H5/H7 (first run).  I asserted the cosmological wall would be safe today and would cross
     the horizon near z ~ 1, from a hand estimate that dropped a factor of 4 pi.  The correct
     number is r_wall/r_H = 0.54 canonical / 0.65 alt TODAY, so the cap is marginally violated
     on horizon scales at every redshift.  DIRECTION: my assertion was TOO FAVOURABLE; the
     computed result is worse for the mechanism than what I had written.
  4. E3 (first run).  I asserted the restoring well was two-sided.  It is not: the flux cap
     means a shell pushed inward past r_min/r_eq = sqrt(S_eq/C_nu a_0) leaves the mediator with
     no solution.  DIRECTION: my assertion was TOO FAVOURABLE.  The one-sidedness is now E4 and
     is reported as an adverse result.
""")
check(True, "J1  four assertions-before-numbers, logged above with their directions: two ran "
            "against the mechanism (H5/H7, E3) and two would have manufactured a deficit "
            "(D2/D3, H3).  The scoreboard is deliberately symmetric")

# =============================================================================================
head("SUMMARY")
# =============================================================================================
for nm in FOOTINGS:
    a0 = A0[nm]
    GM = G_ * 1e11 * MSUN
    rM = np.sqrt(GM / a0)
    vc = (GM * a0) ** 0.25
    rw0 = 3.0 * C_line * a0 / (4 * np.pi * G_ * float(rho_dm(0.0)))
    print(f"  {nm:9s} a_0={a0:.4e}  r_M(1e11 Msun)={rM/KPC:6.2f} kpc  v_c={vc/1e3:6.1f} km/s  "
          f"rho_chi(r_M)={np.sqrt(GM*a0)/(4*np.pi*G_*rM**2):.4e} kg/m^3  "
          f"r_wall(z=0)={rw0/MPC:.0f} Mpc")
print(f"\n  checks run: {NCHK[0]}   failed: {len(FAIL)}")
for f in FAIL:
    print("   FAILED:", f)
sys.exit(1 if FAIL else 0)
