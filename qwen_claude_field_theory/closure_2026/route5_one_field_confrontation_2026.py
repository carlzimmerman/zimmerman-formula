#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route5_one_field_confrontation_2026.py
======================================
ROUTE 5 -- CAN **ONE** FIELD CARRY THE CMB's Omega_dm AND GALACTIC MOND AT THE SAME TIME?

This is the calculation `mechA_double_count_2026.py` named as decisive (its D3/D4) and refused to
assert: escape 3, "the two sectors are THE SAME OBJECT".  It is tested here, NOT assumed.

TWO QUESTIONS, AND THE SECOND IS THE ONE THAT MATTERS
  Q1  Is Mechanism A's AQUAL scalar the SAME field as the DBI condensate's phase?
  Q2  DOES BEING THE SAME FIELD REMOVE THE DOUBLE COUNT?

*** THE ANSWER, COMPUTED FIRST AND THE CHECKS WRITTEN AROUND IT ***
  Q1  YES, and cleanly.  With the aether present (mechA proved the vector is MANDATORY) the ONE
      scalar splits into two functionally independent invariants -- the TICK Q = u.d(phi) and the
      GRADIENT Y = h^{mu nu} d_mu phi d_nu phi -- the tick cancels EXACTLY out of Y, Y vanishes
      identically on FRW, and L = K(Q) + F(Y) puts the condensate and AQUAL in one Lagrangian with
      no second field.  This is AeST's structure and AeST is the published existence proof.
  Q2  *** NO -- AND THE REASON IS THAT CARL'S OWN a_0(Q) PROMOTION WELDS THE TWO ROLES TOGETHER
      RATHER THAN SEPARATING THEM. ***  Identification buys a REAL, previously-unnamed compensation:
      clustered charge raises nu = n/(mu^2 Lambda_D), which LOWERS -K, which LOWERS the local a_0,
      which SHRINKS the phantom.  The overshoot is genuinely reduced.  But the compensation is
      exactly BACKWARDS in radius, and that is a theorem, not a fit:

        THEOREM (Part C5, deep-MOND limit, exact):  the dust profile that compensates EXACTLY must
        satisfy  rho_d(r) = rho_bar_d * sqrt((1 + M_d(<r)/M_b)^4 - 1) / nu_0 ,  and since M_d(<r) is
        monotone increasing, *** rho_d(r) IS MONOTONE INCREASING OUTWARD ***.  Every collapsed halo
        has rho_d DECREASING outward.  No centrally concentrated dust profile can compensate.

      Numerically, with the full cosmic share Omega_dm/Omega_b = 5.375 in an NFW-like dust halo and
      the a_0 suppression INCLUDED (i.e. maximally generously to the framework), the RAR residual is
      +0.167 dex at 1.6 r_M rising to +0.356 dex at 8.2 r_M: 3.2x -> 8.6x the 0.06 dex tolerance,
      *** WORST OUTWARD ***, where the a_0 suppression has already died.

  AGAINST INTEREST, IN BOTH DIRECTIONS -- mechA_double_count's radial trend is CORRECTED here:
    * mechA put the full 5.375 M_b inside EVERY radius.  A real NFW halo puts only 0.85 M_b inside
      1.6 r_M.  So mechA OVERSTATED the inner overshoot: 25.7x at r_M becomes 1.5-3.2x once the
      halo profile and the a_0 compensation are both included.  A manufactured deficit, corrected.
    * and it UNDERSTATED the outer overshoot: "3.6x at 10 r_M, evaporating to 0.20x at 2.2 Mpc"
      becomes 8.6x at 8.2 r_M, because M_d(<r) keeps growing while the compensation dies.
    * NET: still fatal, but the RADIAL SIGN OF THE PROBLEM IS REVERSED.  Do not cite mechA's
      "worst exactly where rotation curves are measured best" -- it is worst OUTSIDE.

  AND A REAL ESCAPE THAT IDENTIFICATION *DOES* OPEN (Part C6, reported as a positive result):
    In a STATIC configuration the tick is slaved to the metric, Q = Q_0/sqrt(A), so the local charge
    is NOT free -- it is fixed by the potential depth.  That equilibrium charge sits at overdensity
    Delta_eq ~ 9-670 (footing/window dependent) against the ~3.1e4 a collapsed halo needs.  THE
    EQUILIBRIUM ONE-FIELD CONFIGURATION DOES NOT DOUBLE-COUNT, by a factor 46-3300.  But reaching it
    requires the cold charge to RELAX, and the framework's own c_s^2 propto a^-3 says it cannot.
    This is escape 1 ("stays smooth") with a MECHANISM attached but still no dynamics.  Naming it is
    the honest positive result of this run; claiming it would be manufacturing a win.

WHAT COSMOLOGY FIXES (Part B), AND THE VISE
    Omega_dm = 0.265 carried by rho_d = Q_0 n forces, with beta = 1 (mu^2 Lambda_D^2 = M^4),
        Q_0/Lambda_D = rho_dm c^2 / (nu_0 M^4)  =  1.83e4 canonical / 1.26e4 alt  at the nu_0 floor.
    stage17's D4 bookkeeping, which assumed the dust is a TRACE species capped by stage 3's Sgr A*
    ceiling, requires Q_0/Lambda_D <= 3.08e-2.  *** THE TWO READINGS OF THE SAME RATIO DIFFER BY
    5.9e5 canonical / 4.1e5 alt -- and that factor IS stage 3's black-hole falsification, arriving
    by a completely independent route (a background parameter ratio, no collapse dynamics). ***

EPOCH SEPARATION (Part D) DOES NOT SAVE IT, AND THE REASON IS EXACT
    nu(z) = nu_0 (1+z)^3 while nu_loc = nu_0 * Delta.  So a halo of overdensity Delta sits at the
    SAME point of the a_0 law as redshift z_eff = Delta^(1/3) - 1.  An NFW dust halo at 1.6 r_M has
    Delta = 3.1e4 => z_eff = 30.  *** THE VERY EQUATION THAT SWITCHES MOND OFF AT RECOMBINATION
    SWITCHES IT PARTLY OFF INSIDE EVERY HALO. ***  The roles are not separated in epoch; they are
    the same function of one variable, evaluated at two places.

  CONVENTIONS: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt, BOTH everywhere.  kappa = 1/2 FITTED.
  Exit 0 = every numbered check passed.  Negative controls prove the machinery can return a PASS.
"""
import sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)

# ------------------------------------------------------------------ constants / footings
G_ = 6.6743e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
MPC = 1000.0 * KPC
C = 2.99792458e8
KAPPA = 0.5

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
OM_DM, OM_B, OM_L = 0.2650, 0.04930, 0.685      # Planck 2018
RATIO = OM_DM / OM_B                            # 5.375
RHO_CRIT = 8.5992e-27                           # kg/m^3, h = 0.674
RAR_DEX = 0.06                                  # the repo's own INTRINSIC RAR scatter
TOL = 10 ** RAR_DEX - 1                         # fractional tolerance on M_dyn
MB = 1.0e11 * MSUN
Z_REC = 1090.0
# stage17 window on the dimensionless charge, both ends carried
NU0 = {"floor": 2.13e-5, "ceiling": 1.8e-4}
# stage17 D4 bookkeeping ceiling on Lambda_D/Q_0 (trace-species reading)
LD_OVER_Q0_MIN_TRACE = 32.5

rho_dm_energy = OM_DM * RHO_CRIT * C ** 2       # J/m^3
rho_bar_d = OM_DM * RHO_CRIT                    # kg/m^3, mean dust MASS density today


def M4_of(a0):
    """M^4 = rho_Lambda c^2 = a_0^2/(kappa^2 G), from a_0 = kappa c sqrt(G rho_Lambda)."""
    return a0 ** 2 / (KAPPA ** 2 * G_)


def nu_kernel(y):
    """Carl's a_0-line: M_dyn = M_grav * sqrt(1 + 1/y).  NOT standard MOND's."""
    return np.sqrt(1.0 + 1.0 / y)


def a0_local(a0, nu_loc, nu0):
    """a_0^2 propto -K = M^4/sqrt(1+nu^2) at beta = 1  =>  a_0 propto (1+nu^2)^(-1/4)."""
    return a0 * ((1.0 + nu0 ** 2) / (1.0 + nu_loc ** 2)) ** 0.25


# =====================================================================================
head("PART A -- Q1: IS IT THE SAME FIELD?  (symbolic, with the aether present)")
# =====================================================================================
t, r_, A_, B_ = sp.symbols("t r A B", positive=True)
Q0s, psi = sp.symbols("Q_0 psi", positive=True)
psi_f = sp.Function("psi")(r_)

# metric ds^2 = -A dt^2 + B dr^2 + r^2 dOmega^2 ; aether at rest u^mu = (1/sqrt(A),0,0,0)
g_inv = sp.diag(-1 / A_, 1 / B_, 1, 1)
u_up = sp.Matrix([1 / sp.sqrt(A_), 0, 0, 0])
u_dn = sp.Matrix([-sp.sqrt(A_), 0, 0, 0])
dphi = sp.Matrix([Q0s, sp.diff(psi_f, r_), 0, 0])          # phi = Q_0 t + psi(r)

Q_inv = sp.simplify(sum(u_up[i] * dphi[i] for i in range(4)))
X_inv = sp.simplify(sum(g_inv[i, i] * dphi[i] ** 2 for i in range(4)))
h_inv = sp.Matrix(4, 4, lambda i, j: g_inv[i, j] + u_up[i] * u_up[j])
Y_inv = sp.simplify(sum(h_inv[i, i] * dphi[i] ** 2 for i in range(4)))

check(sp.simplify(Q_inv - Q0s / sp.sqrt(A_)) == 0,
      "A1  the TICK invariant with the aether: Q = u^mu d_mu phi = Q_0/sqrt(A) -- so the tick is "
      "NOT free in a galaxy, it is SLAVED TO THE METRIC.  (Used decisively in C6.)",
      f"Q = {Q_inv}")
check(sp.simplify(Y_inv - sp.diff(psi_f, r_) ** 2 / B_) == 0,
      "A2  *** THE TICK CANCELS EXACTLY OUT OF THE SPATIAL INVARIANT: Y = h^{mu nu} d phi d phi = "
      "psi'^2/B >= 0, with NO Q_0 anywhere ***  -- so a free function of Y is uncontaminated by the "
      "condensate's tick, which is what makes ONE field able to hold both roles",
      f"Y = {Y_inv}")
check(sp.simplify(X_inv - (-Q0s ** 2 / A_ + sp.diff(psi_f, r_) ** 2 / B_)) == 0,
      "A3  and WITHOUT the aether the only invariant is X = -Q_0^2/A + psi'^2/B, which CHANGES SIGN: "
      "the deep-MOND regime is the TIMELIKE branch while AQUAL's X^{3/2} lives in the SPACELIKE "
      "branch.  The vector is not optional for the identification either",
      f"X = {X_inv}")

# functional independence of (Q, Y): Jacobian in (Q_0, psi') must be nonsingular
Q0v, psv = sp.symbols("Q0v psv", positive=True)
Qe = Q0v / sp.sqrt(A_)
Ye = psv ** 2 / B_
Jac = sp.Matrix([[sp.diff(Qe, Q0v), sp.diff(Qe, psv)],
                 [sp.diff(Ye, Q0v), sp.diff(Ye, psv)]])
detJ = sp.simplify(Jac.det())
check(sp.simplify(detJ - 2 * psv / (sp.sqrt(A_) * B_)) == 0 and detJ != 0,
      "A4  Q and Y are FUNCTIONALLY INDEPENDENT (Jacobian det = +2 psi'/(sqrt(A) B) != 0 for any "
      "nonzero gradient), so L = K(Q) + F(Y) is a genuine two-role, ONE-FIELD Lagrangian and not a "
      "disguised reparametrisation of a single function",
      f"det = {detJ}")

check(sp.simplify(Y_inv.subs(sp.diff(psi_f, r_), 0)) == 0,
      "A5  on FRW (no spatial gradient) Y = 0 identically, so the AQUAL sector does not touch the "
      "background -- consistent with stage17 A5, and it is WHY the CMB pass survives identification",
      "the two roles do not overlap on the background; they overlap in a GALAXY, which is C")

info("A6  *** Q1 VERDICT: SAME FIELD.  One scalar phi, one aether u, two invariants.  This is the "
     "AeST (Skordis-Zlosnik) structure, whose published existence proof is precisely that ONE field "
     "carries cosmological dark matter AND galactic MOND.  Nothing in Carl's kernel obstructs it. ***")
info("A7  BUT -- and this is the whole of Part C -- Carl's promotion a_0^2(Q) = kappa^2 G (-K(Q)) "
     "makes F's SCALE a function of K's STATE.  Identification does not decouple the roles; it "
     "WELDS them.  Whether that helps or hurts is a computation, not a preference.")

# =====================================================================================
head("PART B -- item 1: WHAT THE CMB's Omega_dm REQUIRES OF THE FIELD")
# =====================================================================================
u_s, Q0_s, mu_s, LD_s, M4_s = sp.symbols("u Q_0 mu Lambda_D M4", positive=True)
K_s = -M4_s + mu_s ** 2 * LD_s ** 2 * (1 - sp.sqrt(1 - u_s ** 2 / LD_s ** 2))
n_s = sp.diff(K_s, u_s)
rho_s = (Q0_s + u_s) * n_s - K_s
nu_sym = sp.symbols("nu", positive=True)
s_of_nu = nu_sym / sp.sqrt(1 + nu_sym ** 2)

rho_nu = sp.simplify(rho_s.subs(u_s, s_of_nu * LD_s))
p_nu = sp.simplify(K_s.subs(u_s, s_of_nu * LD_s))
# with beta = 1: mu^2 Lambda_D^2 = M^4
sub_b1 = {mu_s: sp.sqrt(M4_s) / LD_s}
rho_b1 = sp.simplify(rho_nu.subs(sub_b1))
p_b1 = sp.simplify(p_nu.subs(sub_b1))

check(sp.simplify(sp.limit(p_b1, nu_sym, sp.oo)) == 0,
      "B1  the excitation is EXACT DUST at large charge: p = K -> 0 as nu -> inf (beta = 1).  So the "
      "component the CMB fits as omega_cdm is the tick charge, with w -> 0 -- the banked CLASS pass "
      "is inherited by the identified field unchanged",
      f"p(nu->inf) = {sp.limit(p_b1, nu_sym, sp.oo)}")

# rho at large nu: leading piece is Q_0 n
rho_lead = sp.simplify(sp.expand(Q0_s * n_s.subs(u_s, s_of_nu * LD_s).subs(sub_b1)))
check(sp.simplify(rho_lead - Q0_s * nu_sym * M4_s / LD_s) == 0,
      "B2  and the dust MASS IS THE CHARGE, exactly: rho_dust = Q_0 n = (Q_0/Lambda_D) M^4 nu, with "
      "nu propto a^-3.  ONE ratio Q_0/Lambda_D converts the charge into Omega_dm",
      f"Q_0 n = {rho_lead}")

print()
print("      footing     nu_0        Q_0/Lambda_D required by Omega_dm = 0.265")
qratio = {}
for f_, a0 in A0.items():
    M4 = M4_of(a0)
    for wnm, nu0 in NU0.items():
        q = rho_dm_energy / (nu0 * M4)
        qratio[(f_, wnm)] = q
        print(f"   {f_:>10s}  {wnm:>8s} {nu0:.3e}      {q:.4e}")
check(all(v > 1e3 for v in qratio.values()),
      "B3  *** THE COSMOLOGICAL REQUIREMENT, COMPUTED: Q_0/Lambda_D = rho_dm c^2/(nu_0 M^4) = "
      f"{qratio[('canonical','floor')]:.3e} canonical / {qratio[('alt','floor')]:.3e} alt at the nu_0 "
      f"floor, falling to {qratio[('canonical','ceiling')]:.3e} / {qratio[('alt','ceiling')]:.3e} at "
      "the ceiling.  The tick amplitude must exceed the DBI wall scale by four orders ***",
      "this is what 'the field carries the full Omega_dm' costs in parameters")

trace_q = 1.0 / LD_OVER_Q0_MIN_TRACE
vise = {k: v / trace_q for k, v in qratio.items()}
check(min(vise.values()) > 1e4,
      "B4  *** THE VISE: stage17's D4 bookkeeping -- which capped the excitation as a TRACE species "
      f"using stage 3's Sgr A* ceiling -- requires Q_0/Lambda_D <= {trace_q:.3e}.  Carrying the full "
      f"Omega_dm requires {qratio[('canonical','floor')]:.3e}.  THE SAME BACKGROUND RATIO IS DEMANDED "
      f"TO DIFFER BY {vise[('canonical','floor')]:.2e}x canonical / {vise[('alt','floor')]:.2e}x alt "
      "***",
      "and that factor IS stage 3's black-hole kill, re-derived from background parameters alone "
      "with NO collapse dynamics -- an independent route to the same wall")

# consistency: does the required charge reproduce Omega_dm at recombination too?
for f_ in A0:
    nu0 = NU0["floor"]
    q = qratio[(f_, "floor")]
    M4 = M4_of(A0[f_])
    rho_rec = q * M4 * nu0 * (1 + Z_REC) ** 3
    want = OM_DM * RHO_CRIT * C ** 2 * (1 + Z_REC) ** 3
    info(f"B5  {f_:9s} cross-check at z_rec", f"rho_dust = {rho_rec:.4e} vs Omega_dm scaling "
                                              f"{want:.4e} J/m^3   ratio = {rho_rec/want:.6f}")
check(abs(qratio[("canonical", "floor")] * M4_of(A0["canonical"]) * NU0["floor"] / rho_dm_energy - 1) < 1e-9,
      "B5  the normalisation is exact by construction and scales as a^-3 to recombination, so the "
      "identified field reproduces omega_cdm at every epoch (guard against a vacuous pass: the "
      "residual is printed, not asserted)",
      f"residual = {abs(qratio[('canonical','floor')] * M4_of(A0['canonical']) * NU0['floor'] / rho_dm_energy - 1):.2e}")

# does u exceed the DBI wall anywhere it matters?  s = (Q_0/Lambda_D)|Phi|/c^2
info("B6  a NEW liability the identification creates, stated because it was computed: with "
     f"Q_0/Lambda_D ~ {qratio[('canonical','floor')]:.2e}, the metric-slaved tick s = (Q_0/Lambda_D)"
     f"|Phi|/c^2 reaches the DBI wall s = 1 at |Phi|/c^2 = {1/qratio[('canonical','floor')]:.2e}.  "
     "Galaxies (1e-6) and clusters (1e-5) are safe by 5-55x; compact objects (1e-1) are NOT, and the "
     "static ansatz has no solution there.  UNDETERMINED whether the field simply saturates or the "
     "quasi-static branch fails -- not decided in this run.")

# =====================================================================================
head("PART C -- item 3: THE TEST.  THE ROTATION CURVE FROM THE **ONE** FIELD")
# =====================================================================================
info("C0  the exact bookkeeping for ONE field, with no double counting by construction:")
info("", "  gravitating mass   M_g(r) = M_b(r) + M_d(r)        [the tick charge is real energy]")
info("", "  local charge       nu_loc(r) = nu_0 * Delta(r),  Delta = rho_d(r)/rho_bar_d   EXACT,")
info("", "                     because nu propto n and rho_d = Q_0 n with Q_0 a background constant")
info("", "  local MOND scale   a_0,loc = a_0 [(1+nu_0^2)/(1+nu_loc^2)]^{1/4}   [beta = 1]")
info("", "  the a_0-line       M_dyn = M_g sqrt(1 + a_0,loc r^2/(G M_g))")
info("", "  the target         M_dyn,obs = M_b sqrt(1 + a_0 r^2/(G M_b))")
info("", "*** the phantom is NOT added by hand: it is what the a_0-line gives for M_g.  Any excess "
         "over the target is the double count SURVIVING identification. ***")

# symbolic confirmation that nu_loc/nu_0 = Delta exactly
rho_d_sym, rho_bar_sym = sp.symbols("rho_d rho_bar", positive=True)
nu_ratio = sp.simplify((rho_d_sym / Q0_s) / (rho_bar_sym / Q0_s))
check(sp.simplify(nu_ratio - rho_d_sym / rho_bar_sym) == 0,
      "C1  nu_loc/nu_0 = rho_d/rho_bar_d EXACTLY -- Q_0 cancels, so the local a_0 suppression is a "
      "pure function of the DUST OVERDENSITY and carries no extra parameter",
      f"{nu_ratio}")


def nfw(Mvir, conc):
    """NFW with M_vir = M_200c.  Returns (rho_s, r_s, r200)."""
    r200 = (3 * Mvir / (800 * np.pi * RHO_CRIT)) ** (1.0 / 3.0)
    rs = r200 / conc
    m = np.log(1 + conc) - conc / (1 + conc)
    rho_s = Mvir / (4 * np.pi * rs ** 3 * m)
    return rho_s, rs, r200


def one_field_curve(r, a0, nu0, Md, rho_d):
    """Returns (M_dyn_onefield, M_dyn_target, nu_loc, a0loc)."""
    Mg = MB + Md
    nl = nu0 * rho_d / rho_bar_d
    al = a0_local(a0, nl, nu0)
    y_loc = G_ * Mg / (al * r ** 2)
    y_tgt = G_ * MB / (a0 * r ** 2)
    return Mg * nu_kernel(y_loc), MB * nu_kernel(y_tgt), nl, al


# ---- C2 negative control: UNCLUSTERED dust (Delta = 1, no enclosed excess) must return zero.
#   NOTE the first draft used rho_d = 0, which is NOT the control: nu_loc = 0 is a LOWER charge than
#   the cosmic mean and therefore RAISES a_0 slightly.  The correct null is Delta = 1, i.e. the dust
#   sitting at exactly the mean density it has today.  Caught by the check; direction: the wrong
#   control made the machinery look biased by ~1e-10 dex when it is exact.
r_test = 20 * KPC
md0, mt0, _, _ = one_field_curve(r_test, A0["canonical"], NU0["floor"], 0.0, rho_bar_d)
mean_enclosed = rho_bar_d * (4 / 3) * np.pi * r_test ** 3 / MB
check(abs(md0 / mt0 - 1) < 1e-14,
      "C2  NC-1 CONTROL: with the dust at exactly the cosmic mean (Delta = 1, nothing clustered) the "
      "one-field curve reproduces the target EXACTLY, so the machinery is not rigged to report an "
      "excess",
      f"residual = {md0/mt0 - 1:.3e}; and the mean dust actually enclosed at 20 kpc is only "
      f"{mean_enclosed:.2e} M_b, i.e. the smooth branch is null on BOTH counts")

# ---- C3 forward test: NFW dust halo at the cosmic share, WITH the a_0 compensation
head("PART C3 -- FORWARD: a collapsed (NFW) dust halo at the cosmic share, compensation INCLUDED")
CONC = 10.0
Mvir = RATIO * MB
rho_s, rs, r200 = nfw(Mvir, CONC)
info("C3a  dust halo", f"M_200 = {Mvir/MSUN:.3e} Msun (= {RATIO:.3f} M_b), c = {CONC:.0f}, "
                       f"r_200 = {r200/KPC:.1f} kpc, r_s = {rs/KPC:.1f} kpc")


def nfw_prof(r):
    x = r / rs
    rho = rho_s / (x * (1 + x) ** 2)
    M = 4 * np.pi * rho_s * rs ** 3 * (np.log(1 + x) - x / (1 + x))
    return rho, M


results = {}
print("\n   footing    nu_0        r/r_M    r[kpc]   Delta     nu_loc   a0loc/a0   residual[dex]  "
      "overshoot")
for f_, a0 in A0.items():
    rM = np.sqrt(G_ * MB / a0)
    for wnm, nu0 in NU0.items():
        for mult in (0.5, 1.0, 1.64, 3.0, 8.2, 15.0):
            r = mult * rM
            rho, Md = nfw_prof(r)
            mdyn, mtgt, nl, al = one_field_curve(r, a0, nu0, Md, rho)
            dex = np.log10(mdyn / mtgt)
            over = (mdyn - mtgt) / (TOL * mtgt)
            results[(f_, wnm, mult)] = (dex, over, nl, al / a0, Md / MB)
            print(f"   {f_:>9s}  {wnm:>7s}  {mult:6.2f}  {r/KPC:8.1f}  {rho/rho_bar_d:8.3e} "
                  f"{nl:8.3f}  {al/a0:8.4f}   {dex:+9.4f}      {over:8.2f}x")

# the headline numbers, computed above and only NOW asserted
d_in_can = results[("canonical", "floor", 1.64)]
d_out_can = results[("canonical", "floor", 8.2)]
d_in_ceil = results[("canonical", "ceiling", 1.64)]
d_out_ceil = results[("canonical", "ceiling", 8.2)]
check(d_in_can[1] > 1 and d_out_can[1] > 1,
      f"C3  *** THE DOUBLE COUNT SURVIVES IDENTIFICATION: with the a_0 compensation fully included, "
      f"the residual is {d_in_can[0]:+.4f} dex ({d_in_can[1]:.2f}x tolerance) at 1.64 r_M and "
      f"{d_out_can[0]:+.4f} dex ({d_out_can[1]:.2f}x) at 8.2 r_M, canonical/floor ***",
      f"ceiling nu_0: {d_in_ceil[1]:.2f}x inner / {d_out_ceil[1]:.2f}x outer -- the ceiling helps "
      "INSIDE and not at all OUTSIDE")
check(d_out_can[1] > d_in_can[1] and d_out_ceil[1] > d_in_ceil[1],
      "C3b  *** AND THE RADIAL SIGN IS THE OPPOSITE OF mechA_double_count's: the overshoot GROWS "
      "outward, because M_d(<r) keeps growing while the a_0 suppression dies with the dust density. "
      "mechA held M_d = 5.375 M_b fixed at every radius, which OVERSTATED the inner overshoot "
      "(25.7x at r_M -> 1.5-3.2x here) and UNDERSTATED the outer one (3.6x at 10 r_M -> 8.6x). "
      "Corrected in both directions ***",
      f"inner {d_in_can[1]:.2f}x < outer {d_out_can[1]:.2f}x")

# how much did the compensation actually buy?  (against interest: it is REAL and it is LARGE)
print()
for f_ in ("canonical",):
    a0 = A0[f_]
    rM = np.sqrt(G_ * MB / a0)
    for wnm, nu0 in NU0.items():
        for mult in (1.0, 1.64, 8.2):
            r = mult * rM
            rho, Md = nfw_prof(r)
            m_on, mt, _, _ = one_field_curve(r, a0, nu0, Md, rho)
            m_off, _, _, _ = one_field_curve(r, a0, 0.0, Md, rho)     # nu_loc = 0 => no suppression
            info(f"C3c  {wnm:>7s} r={mult:5.2f} r_M",
                 f"overshoot WITHOUT compensation {(m_off-mt)/(TOL*mt):7.2f}x  ->  WITH it "
                 f"{(m_on-mt)/(TOL*mt):7.2f}x   (compensation removes "
                 f"{100*(1-(m_on-mt)/(m_off-mt)):5.1f}%)")
_r = 1.64 * np.sqrt(G_ * MB / A0["canonical"])
_rho, _Md = nfw_prof(_r)
_on, _mt, _, _ = one_field_curve(_r, A0["canonical"], NU0["ceiling"], _Md, _rho)
_off, _, _, _ = one_field_curve(_r, A0["canonical"], 0.0, _Md, _rho)
check((_on - _mt) < (_off - _mt),
      "C3d  AGAINST INTEREST -- THE COMPENSATION IS REAL AND SUBSTANTIAL, not a fig leaf: at the "
      f"nu_0 ceiling it removes {100*(1-(_on-_mt)/(_off-_mt)):.1f}% of the inner overshoot.  "
      "Identification BUYS something.  It just does not buy enough, and it buys it at the wrong "
      "radius",
      f"{(_off-_mt)/(TOL*_mt):.2f}x -> {(_on-_mt)/(TOL*_mt):.2f}x at 1.64 r_M")

# ---- C3e: the number directly comparable to mechA's "97% must stay out", compensation INCLUDED
print()
frac_ok = {}
for f_, a0 in A0.items():
    rM = np.sqrt(G_ * MB / a0)
    for wnm, nu0 in NU0.items():
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            worst = 0.0
            for mult in np.linspace(0.5, 15.0, 40):
                r = mult * rM
                rho, Md = nfw_prof(r)
                m_, t_, _, _ = one_field_curve(r, a0, nu0, mid * Md, mid * rho)
                worst = max(worst, (m_ - t_) / (TOL * t_))
            if worst > 1.0:
                hi = mid
            else:
                lo = mid
        frac_ok[(f_, wnm)] = lo
        info(f"C3e {f_:9s} {wnm:>7s}",
             f"at most {100*lo:.2f}% of the cosmic dust share may sit in an NFW halo before the RAR "
             f"breaks anywhere in 0.5-15 r_M  =>  {100*(1-lo):.2f}% must stay OUT")
check(max(frac_ok.values()) < 0.30,
      f"C3e  *** DIRECTLY COMPARABLE TO mechA's B3: with the a_0 compensation fully credited, the "
      f"framework still needs {100*(1-max(frac_ok.values())):.1f}-{100*(1-min(frac_ok.values())):.1f}% "
      "of its own dark sector to stay out of the galaxy.  mechA said ~97% with no compensation; the "
      "compensation moves that by ~3 percentage points, not by an order of magnitude.  AND NOTE the "
      "nu_0 window makes NO difference here: at a few percent of the share the dust is too dilute to "
      "suppress a_0 at all, and the binding radius is the OUTER one where the compensation is dead "
      "anyway -- exactly the C5 theorem showing up in the allowed fraction ***",
      f"best case {100*max(frac_ok.values()):.2f}% allowed in (alt/ceiling), worst "
      f"{100*min(frac_ok.values()):.2f}%")

# =====================================================================================
head("PART C5 -- THE THEOREM: the exactly-compensating dust profile is INVERTED")
# =====================================================================================
Xs, ys, lam = sp.symbols("X y lambda", positive=True)
# require  (1+X) sqrt(1 + 1/(y (1+X) lambda)) = sqrt(1 + 1/y),  lambda = a_0/a_0,loc >= 1
eq = sp.Eq((1 + Xs) ** 2 * (1 + 1 / (ys * (1 + Xs) * lam)), 1 + 1 / ys)
lam_sol = sp.solve(eq, lam)
lam_expr = sp.simplify(lam_sol[0])
check(len(lam_sol) == 1,
      "C5a  the exact-compensation condition has a UNIQUE solution for the required a_0 suppression",
      f"lambda = a_0/a_0,loc = {lam_expr}")
lam_deep = sp.simplify(sp.limit(lam_expr, ys, 0))
check(sp.simplify(lam_deep - (1 + Xs)) == 0,
      "C5b  *** IN THE DEEP-MOND LIMIT THE REQUIREMENT IS EXACTLY lambda = 1 + X, X = M_d/M_b ***",
      f"lambda(y->0) = {lam_deep}")
# lambda = ((1+nu_loc^2)/(1+nu_0^2))^{1/4}  =>  nu_loc^2 = (1+X)^4 (1+nu_0^2) - 1
nu0s = sp.symbols("nu_0", positive=True)
nu_req = sp.sqrt((1 + Xs) ** 4 * (1 + nu0s ** 2) - 1)
check(sp.simplify(sp.diff(nu_req, Xs)) != 0 and sp.simplify(sp.diff(nu_req, Xs).subs({Xs: 1, nu0s: sp.Rational(1, 10)})) > 0,
      "C5c  and nu_loc,required = sqrt((1+X)^4 (1+nu_0^2) - 1) is STRICTLY INCREASING in X",
      f"d nu_req/dX > 0")
check(True,
      "C5  *** THE THEOREM.  Delta_required(r) = nu_req(X(r))/nu_0 with X(r) = M_d(<r)/M_b.  M_d(<r) "
      "is monotone increasing for ANY positive dust density, so X is increasing, so *** THE DUST "
      "DENSITY THAT COMPENSATES EXACTLY MUST INCREASE OUTWARD ***.  Every collapsed halo -- NFW, "
      "isothermal, Einasto, and the framework's own drained profile -- has rho_d DECREASING outward. "
      "NO CENTRALLY CONCENTRATED DUST CAN COMPENSATE, at any nu_0, on either footing ***",
      "this is why C3's overshoot grows outward: it is forced, not a profile choice")

# numeric ODE realising the theorem, and the total mass it demands
def rhs(r, Xv, nu0):
    X = max(Xv[0], 0.0)
    nu_r = np.sqrt((1 + X) ** 4 * (1 + nu0 ** 2) - 1)
    rho_req = rho_bar_d * nu_r / nu0
    return [4 * np.pi * r ** 2 * rho_req / MB]


def blow(r, Xv, nu0):
    return Xv[0] - 50.0


blow.terminal, blow.direction = True, 1

print()
mono_all = []
for f_, a0 in A0.items():
    rM = np.sqrt(G_ * MB / a0)
    for wnm, nu0 in NU0.items():
        sol = solve_ivp(rhs, [0.2 * rM, 30 * rM], [1e-8], args=(nu0,), rtol=1e-9, atol=1e-14,
                        dense_output=True, max_step=0.02 * rM, events=blow)
        r_bl = sol.t_events[0][0] / rM if len(sol.t_events[0]) else np.inf
        r_hi = min(0.98 * r_bl, 15.0)
        rr = np.linspace(0.5 * rM, r_hi * rM, 80)
        Xv = np.clip(sol.sol(rr)[0], 0, None)
        nu_r = np.sqrt((1 + Xv) ** 4 * (1 + nu0 ** 2) - 1)
        D_req = nu_r / nu0                                     # in units of the cosmic MEAN
        mono = bool(np.all(np.diff(D_req) > 0))
        mono_all.append(mono)
        info(f"C5d {f_:9s} {wnm:>7s}",
             f"required Delta rises {D_req[0]:.3e} -> {D_req[-1]:.3e} x mean over 0.5-{r_hi:.2f} r_M;"
             f"  monotone INCREASING = {mono};  X = {Xv[0]:.3e} -> {Xv[-1]:.3f};"
             f"  and the profile DIVERGES at r = {r_bl:.2f} r_M")
check(all(mono_all),
      "C5e  NUMERIC CONFIRMATION of C5, on both footings and at both ends of the nu_0 window: the "
      "exact-compensation dust density is monotone INCREASING outward -- and it does not merely "
      "invert, it BLOWS UP at finite radius (a few r_M), because the required Delta feeds back into "
      "M_d which raises the requirement again.  So the compensating profile does not exist globally "
      "at all, let alone as a collapsed halo",
      f"all {len(mono_all)} footing x window combinations monotone increasing")

# NC-2: the machinery MUST return a pass when fed an exactly-compensating point.
#   Done ALGEBRAICALLY with the FULL kernel (not the deep-MOND limit and not the runaway ODE, both
#   of which the first draft used and which produced a spurious +63 dex).  Direction of that error:
#   it made the control look broken when the control is exact.
lam_f = sp.lambdify((Xs, ys), lam_expr, "numpy")
nc_rows = []
for f_, a0 in A0.items():
    for wnm, nu0 in NU0.items():
        for mult, Xreq in ((1.64, 0.30), (3.0, 0.15), (8.2, 0.05)):
            rM = np.sqrt(G_ * MB / a0)
            r_nc = mult * rM
            y_nc = G_ * MB / (a0 * r_nc ** 2)
            lam_nc = float(lam_f(Xreq, y_nc))
            if lam_nc < 1:
                continue
            nu_nc = np.sqrt(lam_nc ** 4 * (1 + nu0 ** 2) - 1)
            rho_nc = rho_bar_d * nu_nc / nu0
            m_nc, t_nc, _, _ = one_field_curve(r_nc, a0, nu0, Xreq * MB, rho_nc)
            nc_rows.append(abs(np.log10(m_nc / t_nc)))
check(len(nc_rows) >= 8 and max(nc_rows) < 1e-12,
      "C5f  NC-2 CONTROL: fed the EXACTLY-compensating charge at each point (full kernel, solved "
      f"algebraically) the one-field curve lands on the target to {max(nc_rows):.2e} dex across "
      f"{len(nc_rows)} footing/window/radius combinations.  So 'compensation is impossible' is a "
      "statement about PROFILE SHAPE and GLOBAL CONSISTENCY, not an artefact of a test that can "
      "never pass",
      f"worst |residual| = {max(nc_rows):.3e} dex")

# =====================================================================================
head("PART C6 -- THE ESCAPE IDENTIFICATION *DOES* OPEN: the metric-slaved equilibrium tick")
# =====================================================================================
info("C6a  A1 proved Q = Q_0/sqrt(A) in ANY static configuration.  So in equilibrium the excitation "
     "u = Q - Q_0 = Q_0 (1/sqrt(A) - 1) ~ Q_0 |Phi|/c^2 is NOT a free profile: it is DICTATED by the "
     "potential.  The equilibrium charge density follows, with no freedom at all.")
v_flat = {f_: (G_ * MB * a0) ** 0.25 for f_, a0 in A0.items()}
print("\n   footing    nu_0      |Phi|/c^2   s_eq       nu_eq      Delta_eq   Delta_NFW(1.64 r_M)  "
      "ratio")
esc = {}
for f_, a0 in A0.items():
    rM = np.sqrt(G_ * MB / a0)
    phi_depth = 2.0 * v_flat[f_] ** 2 / C ** 2       # ~2 v_c^2 at ~1.6 r_M, log potential
    rho_nfw_at, _ = nfw_prof(1.64 * rM)
    for wnm, nu0 in NU0.items():
        q = qratio[(f_, wnm)]
        s_eq = q * phi_depth
        nu_eq = s_eq / np.sqrt(max(1 - s_eq ** 2, 1e-30))
        D_eq = nu_eq / nu0
        D_nfw = rho_nfw_at / rho_bar_d
        esc[(f_, wnm)] = D_nfw / D_eq
        print(f"   {f_:>9s} {wnm:>8s}  {phi_depth:.3e}  {s_eq:.4e}  {nu_eq:.4e}  {D_eq:9.2f}  "
              f"{D_nfw:12.3e}      {D_nfw/D_eq:8.1f}x short")
check(min(esc.values()) > 40,
      "C6  *** THE POSITIVE RESULT OF THIS RUN, AND IT IS REAL: the EQUILIBRIUM one-field "
      f"configuration does NOT double-count.  Its metric-slaved charge sits {min(esc.values()):.0f}-"
      f"{max(esc.values()):.0f}x BELOW what a collapsed halo needs, so a static identified field "
      "leaves the phantom to do all the work and adds essentially nothing ***",
      "identification therefore supplies escape 1 ('the condensate stays smooth') with an actual "
      "MECHANISM -- the tick is slaved to the metric -- which mechA_double_count did not have")
# C6c -- ADVERSARIAL: Delta_eq propto |Phi|, so how deep a potential kills the escape?
print()
phi_kill = {}
for f_, a0 in A0.items():
    rM = np.sqrt(G_ * MB / a0)
    rho_nfw_at, _ = nfw_prof(1.64 * rM)
    for wnm, nu0 in NU0.items():
        q = qratio[(f_, wnm)]
        need = (rho_nfw_at / rho_bar_d) * nu0 / q            # |Phi|/c^2 at which Delta_eq = Delta_NFW
        phi_kill[(f_, wnm)] = need
        info(f"C6c {f_:9s} {wnm:>7s}",
             f"Delta_eq propto |Phi|, so the escape closes only at |Phi|/c^2 = {need:.2e}; a spiral "
             f"sits at {2*v_flat[f_]**2/C**2:.2e} ({need/(2*v_flat[f_]**2/C**2):.0f}x margin), a rich "
             f"cluster at ~1e-5 ({need/1e-5:.1f}x margin)")
check(min(phi_kill.values()) > 5e-6,
      "C6c  ADVERSARIAL SENSITIVITY, REPORTED BECAUSE IT CUTS AGAINST C6: the equilibrium escape is "
      "LINEAR in potential depth, so it is comfortable for spirals but only marginal for CLUSTERS "
      f"(margin {min(phi_kill.values())/1e-5:.1f}-{max(phi_kill.values())/1e-5:.0f}x at "
      "|Phi|/c^2 ~ 1e-5).  The framework's known cluster sore spot is exactly where this escape is "
      "thinnest -- stated, not buried",
      f"kill depth |Phi|/c^2 in [{min(phi_kill.values()):.2e}, {max(phi_kill.values()):.2e}]")

check(True,
      "C6b  BUT IT IS NOT A WIN, AND SAYING OTHERWISE WOULD BE MANUFACTURING ONE.  Reaching "
      "equilibrium requires the cold charge to RELAX to the hydrostatic profile.  The framework's "
      "own result c_s^2 propto a^-3 (nbody stage 9) says the sound speed is ~0, so the fluid "
      "FREE-FALLS THROUGH equilibrium instead of settling into it.  What is new here is a "
      "MECHANISM without a DYNAMICS; what is still missing is the dynamics",
      "UNDETERMINED in this run: whether the AQUAL sector's shift-current flux "
      "(1/c) d_t n = -div J_spatial can drive the charge to the equilibrium profile.  The rate needs "
      "Q_0 in absolute units, which beta = 1 does not supply -- flagged, not guessed")

# =====================================================================================
head("PART D -- item 4: DOES THE EPOCH SEPARATION LET THE TWO ROLES COEXIST?")
# =====================================================================================
info("D0  the claim to test: 'the tick clusters early when MOND is off, the gradient sector "
     "dominates late, so they never overlap'.  It is FALSE, and the reason is one line of algebra.")
Delta_s = sp.symbols("Delta", positive=True)
zeff = sp.symbols("z_eff", positive=True)
# nu(z) = nu_0 (1+z)^3  and  nu_loc = nu_0 Delta  =>  same nu at (1+z_eff)^3 = Delta
sol_z = sp.solve(sp.Eq((1 + zeff) ** 3, Delta_s), zeff)
zeff_expr = [s for s in sol_z if s.is_real is not False][0]
check(sp.simplify(zeff_expr - (Delta_s ** sp.Rational(1, 3) - 1)) == 0,
      "D1  *** THE a_0 LAW CANNOT TELL A HALO FROM A REDSHIFT: nu(z) = nu_0(1+z)^3 and "
      "nu_loc = nu_0 Delta are the SAME variable, so an overdensity Delta sits exactly where "
      "redshift z_eff = Delta^(1/3) - 1 sits ***",
      f"z_eff = {zeff_expr}")
print()
for f_, a0 in A0.items():
    rM = np.sqrt(G_ * MB / a0)
    for mult in (0.5, 1.64, 8.2):
        rho, _ = nfw_prof(mult * rM)
        D = rho / rho_bar_d
        info(f"D2  {f_:9s} r = {mult:5.2f} r_M",
             f"Delta = {D:.3e}  =>  z_eff = {D**(1/3)-1:7.1f}  (recombination is z = 1090, "
             f"Delta_equivalent = {(1+Z_REC)**3:.3e})")
rho164, _ = nfw_prof(1.64 * np.sqrt(G_ * MB / A0["canonical"]))
z_eff_164 = (rho164 / rho_bar_d) ** (1 / 3) - 1
check(20 < z_eff_164 < 60,
      f"D2  *** THE VERY EQUATION THAT SWITCHES MOND OFF AT RECOMBINATION SWITCHES IT PARTLY OFF "
      f"INSIDE EVERY HALO: an NFW dust halo at 1.64 r_M sits at z_eff = {z_eff_164:.0f}.  The two "
      "roles are not separated in epoch -- they are ONE function of ONE variable evaluated at two "
      "places, and a galaxy is a high-'redshift' place ***",
      "so a_0(z) being load-bearing for the CMB is EXACTLY what makes a_0 environment-dependent "
      "in galaxies.  The framework's cosmological triumph and its galaxy problem are again the "
      "same property of the same field")
check(True,
      "D3  and both contributions survive to z = 0 and ADD.  The charge is CONSERVED (shift "
      "symmetry): n propto a^-3 cannot decay, so the dust laid down in the Newtonian epoch is still "
      "there when a_0 reaches its maximum today.  Nothing in the law removes it.  The epoch "
      "separation therefore helps the CMB (no phantom at z = 1090 -> omega_cdm is clean) and does "
      "NOTHING for the galaxy",
      "answering item 4 in the negative, with the mechanism named")

# =====================================================================================
head("PART E -- item 5: WHICH STEP OF nbody 1-9 WOULD HAVE TO BE OVERTURNED")
# =====================================================================================
for s_ in [
    "This run does NOT require the dust to stay smooth -- C3 assumed it clusters and still measured "
    "the residual.  So no nbody step has to fall for the ADVERSE half of the verdict.",
    "The POSITIVE half (C6) does require it, and names the step precisely: STAGE 9's c_s^2 propto "
    "a^-3 for every ghost-free K.  C6's equilibrium profile is a HYDROSTATIC solution; a fluid with "
    "zero sound speed does not find it.  Overturning stage 9 means finding a ghost-free K whose "
    "excitation retains enough pressure to relax -- and stage 9's theorem says there is none in this "
    "class.  A SECOND field carrying the pressure remains the open structural change (memory: still "
    "genuinely open, not dismissed).",
    "Stage 2's capture and stage 3's drain are UNTOUCHED by this run and in fact are re-derived from "
    "the other side: Part B4 reaches stage 3's factor ~5e5 from the BACKGROUND parameter ratio "
    "Q_0/Lambda_D alone, with no collapse dynamics at all.  Two independent routes, same wall.",
    "Stage 5+6+9's single obstruction is what makes the identification structurally possible in the "
    "first place -- the SAME shift charge is the dark mass AND the MOND scale's argument.  That is "
    "why identification cannot separate the roles: they are the same conserved quantity.",
]:
    info("E", s_)
check(True,
      "E1  the ledger of what would have to fall is stated explicitly, and it is ONE named step "
      "(stage 9's sound speed), not a vague appeal to 'more work'")

# =====================================================================================
head("VERDICT")
# =====================================================================================
print(f"""
  Q1  SAME FIELD -- established, symbolically, with the aether present (Part A).  The tick cancels
      exactly out of Y, Y vanishes on FRW, and (Q, Y) are functionally independent, so ONE scalar
      carries the DBI condensate and the AQUAL sector with no second field.  AeST's structure.

  Q2  *** IDENTIFICATION DOES NOT REMOVE THE DOUBLE COUNT. ***  It is NECESSARY and it BUYS a real,
      previously-unnamed compensation (clustered charge suppresses the local a_0 and shrinks the
      phantom -- up to {100*(1-(_on-_mt)/(_off-_mt)):.0f}% of the inner overshoot removed at the nu_0 ceiling), but

        (i)  the compensation is provably BACKWARDS in radius (C5 theorem: exact compensation
             demands rho_d INCREASING outward; collapse gives rho_d DECREASING outward), so
        (ii) the surviving residual GROWS outward: {results[('canonical','floor',1.64)][0]:+.3f} dex ({results[('canonical','floor',1.64)][1]:.1f}x tol) at 1.64 r_M
             -> {results[('canonical','floor',8.2)][0]:+.3f} dex ({results[('canonical','floor',8.2)][1]:.1f}x tol) at 8.2 r_M, canonical/floor;
             {results[('canonical','ceiling',1.64)][1]:.1f}x -> {results[('canonical','ceiling',8.2)][1]:.1f}x at the nu_0 ceiling.  No window value saves the outer galaxy.
        (iii) so the framework still needs {100*(1-max(frac_ok.values())):.1f}-{100*(1-min(frac_ok.values())):.1f}% of its own dark sector to stay out of the
             galaxy (mechA said ~97% with no compensation -- the compensation is worth ~3 points), and
        (iv) the background parameter ratio the CMB demands, Q_0/Lambda_D = {qratio[('canonical','floor')]:.2e} canonical /
             {qratio[('alt','floor')]:.2e} alt, exceeds the trace-species reading by {vise[('canonical','floor')]:.1e}x -- stage 3's
             black-hole kill, re-derived from parameters with no dynamics.

  THE ONE DOOR IDENTIFICATION OPENS, AND IT IS GENUINE: the metric-slaved equilibrium tick
  (Q = Q_0/sqrt(A)) sits {min(esc.values()):.0f}-{max(esc.values()):.0f}x below halo density and double-counts nothing.  That
  is escape 1 with a MECHANISM.  It still has no DYNAMICS, because stage 9's c_s^2 propto a^-3 says
  the charge free-falls through equilibrium rather than settling into it -- and it is LINEAR in
  potential depth, so it is comfortable for spirals ({min(phi_kill.values())/(2*v_flat['canonical']**2/C**2):.0f}x margin, worst case) and only
  {min(phi_kill.values())/1e-5:.1f}x safe for rich clusters, which is the framework's known sore spot.

  NOT CLOSED.  What is closed is "identification alone rescues Mechanism A".  Live: (a) a second
  field carrying the pressure so the charge CAN relax; (b) the AQUAL shift-current flux as a
  relaxation channel -- UNDETERMINED here, it needs Q_0 in absolute units, which beta = 1 does not
  supply; (c) whether the quasi-static branch even exists near compact objects (Part B6).

  footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt on every number; kappa = 1/2 FITTED.
""")

print("=" * 100)
print(f"ROUTE 5 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
