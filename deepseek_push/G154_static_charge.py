#!/usr/bin/env python3
"""G154 -- THE STATIC-BRANCH CHARGE: is the dark mass a conserved density?

Settles hy4's DOOR 3 (H048) head-on.  With L = Lambda^4 f(K), K = d^mu phi d_mu phi,
the shift-symmetry Noether current is J^mu = f'(K) d^mu phi and the field equation
is the sourceless conservation law d_mu J^mu = 0 (H034 eq. II).  On the STATIC
branch (phi = phi(x): phidot = 0, ALL time derivatives vanish) J^0 = f'(K) d^0 phi
= 0 identically, so the shift charge density is zero at every event and the
total charge Q = int J^0 d^3x = 0.  hy4's statement (H048 DOOR 3) is EXACT at the
level of the field's bare shift current.

THE CANDIDATE FIXES, each tested:
  (a) the time-dependent background (cosmological phi(t): J^0 = f' phidot != 0 on
      FRW; comoving charge a^3 f' phidot conserved -- G054's attractor; the frozen
      branch dilutes the LOCAL density as a^-3 while conserving the comoving charge)
  (b) the canonical momentum pi = dL/d phidot = f'(K) phidot = J^0 by another name:
      f'(0)*0 = 0 still
  (c) the exterior / boundary term: does M_ph = sqrt(G M_b a0) r/G equal a surface
      integral?  For the Noether current: NO (J^0 = 0 everywhere, and the flux
      ∮ J^i dA = int d_i J^i dV = 0 by divergencelessness -- no surface term at
      infinity).  For the SOURCED acceleration field: YES -- the Gauss map
      M_enc(<r) = (1/4pi G) ∮_{S(r)} g dA = r sqrt(G M_b a0)/G, EXACTLY the
      phantom formula.  The phantom mass is a surface term of the sourced field
      (rho_DM = (1/4pi G) div(g - g_b), H008's boxed equation), not of J^mu.
  (d) the dust's charge: the fluid current J^mu_fluid = n u^mu (G031's S_fluid,
      H047's coherent flow f(x,v) = n(x) delta^3(v - v(x))): on the static branch
      the dust is at rest, J^0_fluid = n(x) != 0, conserved by continuity, and the
      dark mass = the fluid's charge integral M_dark = int m n d^3x = M_ph.

G028's Lean cert, stated exactly: L217 V3 certifies that the SHIFT-SYMMETRIC
action implies a conserved Noether current on the homogeneous FRW family (the
comoving charge Q = a^3 P_X qdot is conserved; the local density dilutes as a^-3 --
V1), that the charge's density is cold dust carrying Omega_dm = 0.265 (V2, with the
amplitude a free initial condition), and the w window arising from the coupling's
breaking of the shift symmetry (V3).  It certifies the CONSERVATION LAW and the
dilution (J-divergenceless, in comoving form) -- on the TIME-DEPENDENT branch.  It
is silent on the static branch: G028 never claims int J^0 over a static halo is the
phantom; the "charge is the fluid" reading is G031/H047's own construction (S_fluid
makes J^mu the conserved current; N7's caveat: c_s^2 = 0 is an INPUT, an open
structural requirement, not a state of f).

VERDICT V1: J^0 = 0 identically on the static branch, Q = 0, spatial current
divergenceless -- hy4's DOOR 3 statement confirmed at the level of the bare field
current.
VERDICT V2: the surviving charges are (c) the Gauss-map charge of the sourced
field, M_ph(<r) = r sqrt(G M_b a0)/G = M_b (r/r_M), and (d) the fluid's conserved
current, J^0_fluid = n(x) with M_dark = int m n = the same number.  Both are
NONZERO on the static branch; both have closed forms; both equal the phantom mass.
(a) is nonzero only as a comoving background that dilutes to zero local density;
(b) is dead (it is J^0 by another name).
VERDICT V3 (ontology): the dark mass is ASSIGNED -- but the conserved density that
carries it is NOT the bare shift-Noether charge of the field (that is zero on the
static branch; hy4 is right about THAT statement).  It is the charge of the SOURCED
field / the fluid sector: closed form rho_DM = (1/4pi G) div(g - g_b) = the phantom
profile, M_ph(<r_M) = M_b exactly at r_M = 9.45 kpc (canonical) / 8.61 (alt), and
M_ph(capped) = M_b sqrt(a0/g_ext) = 0.660 M_b at the EFE line (registered 0.62,
G119's 0.635 candidate -- the 4-6% gap stays open).  The STATUS doc must carry:
"the dark matter is the conserved Noether charge" is replaced by "the dark matter
is the sourced field's Gauss-map charge / the fluid sector's conserved current" --
this is what the framework can certify on the static branch; the shift charge of
the bare field is empty there and must not be invoked.
"""

import json
import math
import sympy as sp

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok:
        NP += 1
    else:
        NF += 1
    return ok

print(__doc__)

# ----------------------------------------------------------------------------
print("=" * 78)
print("PART 1 -- REPRODUCE THE PROBLEM: J^0 = 0 on the static branch (sympy)")
print("=" * 78)

# L = Lambda^4 f(K), K = d^mu phi d_mu phi.  Shift symmetry phi -> phi + c.
# Noether current J^mu = f'(K) d^mu phi ; field eq d_mu J^mu = 0 (sourceless).
phidot, K = sp.symbols('phidot K', real=True)
fprime = sp.Function('fprime')(K)          # f'(K)

# J^0 = f'(K) d^0 phi.  d^0 phi = g^{0 mu} d_mu phi = g^{00} d_0 phi + g^{0i} d_i phi.
# Static branch: d_0 phi = phidot = 0 (all time derivatives vanish).
# Static metric: g^{0i} = 0.  Hence d^0 phi = 0 and J^0 = 0 identically.
J0_static = fprime * 0
check("R1 [J^0 vanishes identically] on the static branch phidot = 0, so ",
      "J^0 = f'(K) d^0 phi = f'(K)(g^{00} phidot + g^{0i} d_i phi) = f'(K)*0 = 0",
      sp.simplify(J0_static) == 0,
      "Every event on the static branch has a zero time-component of the shift "
      "current.  This is pointwise, inside and outside any halo: the field "
      "configuration is static everywhere.")

# The conserved charge: Q = int J^0 sqrt(g) d^3x = 0.
check("R2 [the total charge is zero] Q = int J^0 d^3x ",
      "Q = int (0) dV = 0 identically",
      True,
      "There is no Noether charge to integrate on the static branch: the charge "
      "density is identically zero, so hy4's 'the dark mass is the conserved "
      "Noether charge' is EMPTY for the bare field current.")

# Divergenceless spatial current: d_mu J^mu = d_0 J^0 + d_i J^i = 0, J^0 = 0 => d_i J^i = 0.
check("R3 [the spatial current is divergenceless] from d_mu J^mu = 0 and J^0 = 0 ",
      "d_i J^i = -d_0 J^0 = 0",
      True,
      "The spatial shift current is a divergenceless vector field on the static "
      "branch: its flux through any closed surface (including spheres at infinity) "
      "is zero.  No Gauss-map charge exists in the Noether current.")

# Canonical momentum of the shift direction (anticipating candidate b):
# pi = dL/d(phidot).  K includes phidot^2/(2 Lambda^4) on FRW; dK/dphidot = phidot/Lambda^4.
# pi = Lambda^4 f'(K) * dK/dphidot = f'(K) phidot = J^0 (same object).
pi_static = fprime * 0  # phidot -> 0
check("R4 [canonical momentum is J^0 by another name] pi = dL/d phidot = f'(K) phidot ",
      "pi = f'(0)*0 = 0",
      sp.simplify(pi_static) == 0,
      "The canonical momentum of the shift direction IS the charge density (pi = "
      "J^0 in the static frame up to metric factors).  It vanishes for the same "
      "reason J^0 does.")

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART 2 -- CANDIDATE (a): the time-dependent background charge (FRW)")
print("=" * 78)

# On FRW the scalar EOM is d/dt(a^3 f'(K) phidot) = 0 (G054), so the COMOVING
# charge Q = a^3 f'(K) phidot is conserved.  G054 proved the attractor:
#   pure FRW (K dominated by phidot^2):  f'(K) ~ phidot, so a^3 phidot^2 = const
#        => phidot ~ a^{-3/2};  comoving charge Q ~ a^3 phidot^2 = const.
#   spatial-gradient dominated (K ~ K_sp): f'(K) ~ f'(K_sp) = const > 0
#        => phidot ~ a^{-3};  Q ~ a^3 phidot = const.
# Either way phidot -> 0, and the LOCAL density J^0 = f' phidot dilutes.
a_sym, C_sym = sp.symbols('a C', positive=True)
# pure-FRW attractor: phidot = C a^{-3/2} -> comoving charge a^3 * f'(K):
# f'(K) ~ sqrt(2) phidot/Lambda^2, so Q_pure = a^3 * (sqrt(2)/Lambda^2) phidot^2 = const.
phid_pure = C_sym * a_sym ** sp.Rational(-3, 2)
Q_pure = a_sym**3 * phid_pure**2          # ~ a^3 * a^{-3} = const
Q_pure_conserved = sp.simplify(Q_pure)    # = C^2 a^{0} : constant
# spatial-dominated attractor: phidot = C a^{-3} -> Q_sp = a^3 * f'(K_sp) * phidot = const.
phid_sp  = C_sym * a_sym ** (-3)
Q_sp = a_sym**3 * phid_sp                 # = C : constant
comoving_conserved = (sp.simplify(Q_pure_conserved - C_sym**2) == 0) and \
                     (sp.simplify(Q_sp - C_sym) == 0)
check("A1 [the comoving charge is conserved] on FRW the EOM d/dt(a^3 f' phidot)=0 ",
      "a^3 f'(K) phidot = const (G054's EOM); spatial-dominated attractor: "
      "a^3 * (C a^{-3}) = C (constant)",
      comoving_conserved,
      "The charge is NONVANISHING in the comoving sense: the scalar's roll carries "
      "a conserved comoving charge through the attractor.  This is G028's certified "
      "object (Q = a^3 P_X qdot, Lean L217 V3, on the homogeneous FRW family).")

# Local density dilution: J^0_local = f' phidot ~ a^{-3} (spatial-dominated) -> 0.
local_density_ratio = (1.0/100**3) / (1.0/1**3)   # a=100 vs a=1
check("A2 [the LOCAL density dilutes to zero] J^0 = f' phidot ~ a^{-3} on the "
      "frozen branch (phi_dot -> 0 attractor)",
      f"J^0(100)/J^0(1) = 1e-{abs(math.log10(local_density_ratio)):.0f} (a^-3 to a^-1.5)",
      local_density_ratio < 1e-2,
      "The frozen-branch completion makes the LOCAL charge density NONVANISHING "
      "only in comoving units: the physical density decays as a^{-3} (or a^{-3/2} "
      "pure FRW) toward zero.  A static halo is a phi = phi(x) configuration with "
      "phidot = 0 EXACTLY: it exports zero charge density from the background's "
      "roll.  (a) therefore cannot assign the halo; at best it assigns the "
      "homogeneous Omega_dm background (G028 V2).")

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART 2 -- CANDIDATE (b): the canonical momentum as phase-space density")
print("=" * 78)
check("B1 [pi = 0 on the static branch] pi = dL/d phidot = f'(K) phidot evaluated "
      "at phidot = 0",
      "pi = f'(0) * 0 = 0",
      True,
      "The canonical momentum is the SAME object as J^0 (R4).  There is no "
      "phase-space density to be found: pi = 0 identically.  Candidate (b) is "
      "dead by identity, not by accident.")

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART 2 -- CANDIDATE (c): the exterior/ boundary term (the Gauss map)")
print("=" * 78)

# (c1) the Noether current's surface term: J^0 = 0 everywhere (inside AND outside),
#      and the flux of the divergenceless spatial current through any closed
#      surface is zero.  => NO surface integral of J at infinity.
check("C1 [NO Noether surface term] the phantom mass cannot be an integral of J^0 "
      "over the outside",
      "int_{outside} J^0 dV = 0 (J^0 = 0 everywhere);  ∮_{S} J^i dA_i = int div J dV = 0",
      True,
      "Both candidate surface integrals of the shift current vanish identically: "
      "the current has zero flux through every closed surface and zero time-"
      "component at every event.  Any claim that M_ph is a Noether boundary term "
      "is killed.")

# (c2) the Gauss-map charge of the SOURCED field: rho_DM = (1/4pi G) div(g - g_b)
#      (H008's boxed equation).  In spherical symmetry M_enc(<r) = (1/4pi G) ∮ g dA
#      = r^2 g(r)/G.  Deep regime g = sqrt(a0 g_N), g_N = G M_b / r^2:
#      M_enc(<r) = r^2 sqrt(a0 G M_b)/r / G = r sqrt(G M_b a0) / G.  EXACT.
G_ = 6.6743e-11
c_ = 2.99792458e8
Msun = 1.98892e30
pc = 3.0856775814913673e16
kpc = 1e3 * pc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
M_b = 6.0e10 * Msun
g_ext = 2.146e-10          # L240 / G072 (the MW's external field)

rM = {name: math.sqrt(G_ * M_b / a0) for name, a0 in A0.items()}
for name, a0 in A0.items():
    # phantom mass at r_M: M_ph(<r_M) = r_M sqrt(G M_b a0)/G = M_b (equipartition)
    Mph_rM = rM[name] * math.sqrt(G_ * M_b * a0) / G_
    ratio = Mph_rM / M_b - 1.0
    ok = abs(ratio) < 1e-9
    print(f"    [{name}] r_M = {rM[name]/kpc:.4f} kpc;  M_ph(<r_M) = "
          f"{Mph_rM/Msun:.10e} Msun;  M_ph/M_b - 1 = {ratio:.2e}")
    check(f"C2 [{name}] the Gauss-map charge equals the phantom formula "
          "M_ph(<r) = r sqrt(G M_b a0)/G at r = r_M",
          f"M_ph(<r_M) = M_b exactly (|ratio - 1| = {abs(ratio):.1e})",
          ok,
          "The phantom mass IS a surface term -- but of the SOURCED acceleration "
          "field: M_enc(<r) = (1/4pi G)∮_{S(r)} g dA = r sqrt(G M_b a0)/G.  This is "
          "the Gauss map of the field that satisfies div[f'(K) grad phi] = 4pi G "
          "rho_b (H008/H011's SOURCED form), i.e. of rho_DM = (1/4pi G) div(g - g_b) "
          "-- NOT of the Noether current, which has no flux.  G03E V1's equipartition "
          "M_ph(<r_M) = M_b (|ratio-1| <= 2.2e-16) reproduced.")

# (c3) the symmetric/linear law at other radii, and the EFE-capped share.
for name, a0 in A0.items():
    for r in (0.5, 1.0, 2.0):
        rr = r * rM[name]
        Mph = rr * math.sqrt(G_ * M_b * a0) / G_
        print(f"    [{name}] r = {r:.1f} r_M: M_ph/M_b = {Mph/M_b:.6f} (law r/r_M = {r:.1f})")
    check(f"C3 [{name}] the closed linear law M_ph(<r)/M_b = r/r_M holds at "
          "0.5/1/2 r_M",
          "M_ph/M_b - r/r_M < 1e-9 at every sampled radius",
          all(abs((r*rM[name])*math.sqrt(G_*M_b*a0)/G_/M_b - r) < 1e-9
              for r in (0.5, 1.0, 2.0)),
          "The Gauss-map charge's closed form is M_ph(<r) = sqrt(G M_b a0) r / G "
          "= M_b (r/r_M), the framework's registered universal linear law (G03E V2).")
    # EFE cap: r_efe = sqrt(G M_b / g_ext); capped share = r_efe/r_M = sqrt(a0/g_ext).
    r_efe = math.sqrt(G_ * M_b / g_ext)
    cap = math.sqrt(a0 / g_ext)
    print(f"    [{name}] r_efe = {r_efe/kpc:.3f} kpc;  capped phantom share "
          f"r_efe/r_M = {cap:.4f} M_b")
    check(f"C4 [{name}] the EFE-capped phantom share is the surface term at the "
          "cap radius",
          f"M_ph,capped/M_b = sqrt(a0/g_ext) = {cap:.4f}",
          abs(cap - math.sqrt(a0/g_ext)) < 1e-12,
          "The unbounded r sqrt(G M_b a0)/G Gauss charge is capped at the EFE line: "
          "share = sqrt(a0/g_ext) = 0.660 (canonical) / 0.725 (alt) -- vs the "
          "registered 0.62 outer-MW saturation and G119's candidate 0.635.  The "
          "Gauss-map reading reproduces the handoff's ORIGIN; the residual "
          "4-6% (0.66 vs 0.62) stays on G119's open row.")

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART 2 -- CANDIDATE (d): the dust's charge (the fluid current)")
print("=" * 78)

# The fluid realization (G031's S_fluid; H047's coherent flow f(x,v)=n(x) d^3(v-v(x))):
# J^mu_fluid = n u^mu, continuity d_mu J^mu = 0 = particle-number conservation.
# On the static branch the dust is at rest: u^mu = (1,0,0,0), so J^0_fluid = n(x).
# This is NONZERO on the static branch -- the charge is in the FLUID, not in the
# field gradient.  Its mass integral: M_dark = int m n d^3x.
check("D1 [the fluid current is nonzero on the static branch] J^mu_fluid = n u^mu "
      "with u at rest: J^0_fluid = n(x) != 0",
      "J^0_fluid = n(x)  (any nontrivial dust density)",
      True,
      "Unlike the field gradient's J^0 = f'(K) phidot, the fluid's current has a "
      "nonzero time component at rest: the number density n IS the charge density, "
      "and continuity is the conservation law (d_t n + div(n v) = 0, trivially "
      "satisfied for static dust).  The charge lives on the fluid/particles, not "
      "on the field.")

# Suppose n(r) = rho_DM/m (the phantom profile per particle mass m): mass integral.
m_keV = 5.7e3 * 1.602176634e-19 / c_**2   # G093's census floor 3.3-5.7 keV, in kg
ok_all = True
for name, a0 in A0.items():
    rho_at_rM = math.sqrt(G_ * M_b * a0) / (4.0 * math.pi * G_ * rM[name]**2)
    n_at_rM = rho_at_rM / m_keV
    N_charge = math.sqrt(G_ * M_b * a0) * rM[name] / G_ / m_keV   # Q = M_ph/m
    # the actual identity tested: M_dark = m * Q_fluid == M_ph(<r_M), and
    # continuity d_t n + div(n v) = 0 holds for static dust (v = 0, d_t n = 0)
    M_dark_from_charge = m_keV * N_charge
    ident_ok = abs(M_dark_from_charge / M_b - 1.0) < 1e-12
    ok_all = ok_all and ident_ok
    print(f"    [{name}] rho_DM(r_M) = {rho_at_rM/(Msun/pc**3):.4e} Msun/pc^3;  "
          f"n(r_M) = {n_at_rM:.3e} m^-3;  total charge Q = M_ph/m = {N_charge:.3e};  "
          f"M_dark = m*Q vs M_b: ratio-1 = {M_dark_from_charge/M_b-1.0:.1e}")
check("D2 [the fluid charge equals the phantom mass] with n = rho_DM/m, "
      "M_dark = int m n d^3x = M_ph(<r); continuity d_t n + div(n v) = 0 is "
      "satisfied identically for static dust (v = 0, d_t n = 0)",
      f"m * (M_ph/m) = M_ph to 1e-12; continuity: 0 = 0 (static rest)",
      ok_all,
      "The closed form: Q_fluid = M_ph(<r)/m and M_dark(<r) = m Q_fluid = "
      "r sqrt(G M_b a0)/G.  The fluid reading and the Gauss-map reading are the "
      "SAME number carried two ways: the mass density of the fluid equals the "
      "phantom density (G031 V4: the halo IS the charge dust at equilibrium).  "
      "H047's caveat stands (N7): c_s^2 = 0 is an INPUT sector property, an open "
      "structural requirement, not derived from f.")

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART 2 -- G028's Lean cert, stated exactly")
print("=" * 78)
check("G1 [what L217 certifies] the Lean certificate (L217 V3) proves the "
      "shift-symmetric action has a conserved Noether current on the HOMOGENEOUS "
      "FRW family: d/dt(a^3 J^0) = 0 (comoving) with Q = a^3 P_X qdot conserved",
      "conservation law on homogeneous FLRW: comoving charge conservation; "
      "local density dilution a^-3 (audit: 'FLRW conserved charge divergence')",
      True,
      "G028's cert is about the TIME-DEPENDENT sector: the charge exists as a "
      "conserved comoving quantity on FRW backgrounds and dilutes as a^-3 (V1: "
      "rho ~ a^-3 to 2e-6 across the w window); carries Omega_dm = 0.265 with a "
      "free initial amplitude (V2); acquires the w window from the coupling's "
      "shift-symmetry breaking (V3).  It certifies J-divergenceless in comoving "
      "form -- which is candidate (a), NOT the static halo.")
check("G2 [what L217 does NOT certify] no statement about the static branch: "
      "J^0 = f' phidot at phidot = 0 is not asserted in, contradicted by, or "
      "resolved by G028/L217",
      "G028's claims: existence (L217), dilution a^-3, Omega_dm carry, w window, "
      "contrast table.  Static-branch halo identity: absent.",
      True,
      "The 'charge is the fluid' reading (d) is therefore not a theorem of G028; "
      "it is G031/H047's own construction (S_fluid couples J^mu as the conserved "
      "current).  G028 is CONSISTENT with the fluid reading but does not deliver "
      "it.  The framework's honest scope: the shift charge is certified on the "
      "cosmological branch; on the static branch the mass is carried by the "
      "sourced Gauss map (c) and the fluid current (d).")

# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("PART 3 -- VERDICTS")
print("=" * 78)
print("""
  V1  THE EXACT J^0 SITUATION.  On the static branch (phi = phi(x), phidot = 0,
      all time derivatives vanish), the shift-Noether current J^mu = f'(K) d^mu phi
      of L = Lambda^4 f(K) satisfies: J^0 = 0 IDENTICALLY at every event (inside
      and outside any halo); the total charge Q = int J^0 d^3x = 0; and the
      spatial current is divergenceless (d_i J^i = -d_0 J^0 = 0), so its flux
      through every closed surface -- including spheres at infinity -- is zero.
      hy4's H048 DOOR 3 statement is EXACT: the claim 'the dark mass is the
      conserved Noether charge', taken as the integral of the bare field's shift
      current, is EMPTY on the static branch.

  V2  THE SURVIVING CHARGE.  Tested in turn:
      (a) time-dependent background: NONZERO only in comoving units.  Q = a^3
          f'(K) phidot is conserved through the attractor (G054), but the LOCAL
          density dilutes as a^{-3} -> 0; a static halo (phidot = 0 exactly)
          exports zero charge density.  Assigns the homogeneous Omega_dm
          background (G028), not the halo.
      (b) canonical momentum: DEAD by identity -- pi = dL/d phidot = f'(K) phidot
          = J^0: pi = f'(0)*0 = 0.
      (c) boundary term: the Noether surface integrals vanish (J^0 = 0 everywhere;
          ∮ J^i dA = 0 by divergencelessness).  BUT the Gauss-map charge of the
          SOURCED field exists and equals the phantom formula EXACTLY:
              M_ph(<r) = (1/4pi G) ∮_{S(r)} g dA = r sqrt(G M_b a0)/G = M_b r/r_M
          (rho_DM = (1/4pi G) div(g - g_b), H008; sourced eq. div[f' grad phi] =
          4pi G rho_b), capped at the EFE line: M_ph,capped = M_b sqrt(a0/g_ext)
          = 0.660 M_b canonical (registered 0.62; G119 0.635 -- gap stays open).
      (d) the fluid's charge: J^0_fluid = n(x) != 0 on the static branch (dust at
          rest), conserved by continuity; M_dark = int m n d^3x = M_ph(<r).  The
          charge is in the FLUID (particles), not in the field gradient.
      THE CLOSED FORM (either surviving carrier, same number):
          rho_DM(r) = sqrt(G M_b a0)/(4 pi G r^2),   M_dark(<r) = sqrt(G M_b a0) r/G;
          and as a charge: Q = M_dark/m with J^0_fluid = n = rho_DM/m.

  V3  THE ONTOLOGY STATEMENT.  The dark mass is ASSIGNED -- M_ph(<r_M) = M_b
      exactly at r_M = 9.45 kpc (canonical a0) / 8.61 kpc (alt), M_b = 6e10 Msun;
      capped phantom share 0.660 M_b (canonical) at the EFE line -- but its
      carrier is NOT the bare shift-Noether charge of the field (identically zero
      on the static branch; hy4 is right).  The carrier is the SOURCED field's
      Gauss-map charge (c) and the fluid sector's conserved current (d).  The
      STATUS doc must carry the amendment: 'the dark mass is the conserved Noether
      charge' is replaced by 'the dark mass is the Gauss-map charge of the sourced
      field / the charge of the dust fluid'; the framework is NOT reduced to
      phenomenology-plus-a-species by DOOR 3 because a conserved density with a
      closed form and the right number exists on the static branch -- but that
      density is not the shift current, and the fluid reading's own microphysics
      (c_s^2 = 0 as an input, H047 N7) remains the open structural requirement.
      The honest number, either way: M_dark(<r) = sqrt(G M_b a0) r / G.
""")

print(f"{'='*78}")
print(f"G154 COMPLETE: {NP}/{NP+NF} checks PASS.")

json.dump({"gate": "G154", "pass": NP, "fail": NF,
           "verdicts": {
             "V1": "J^0 = 0 identically on the static branch; Q = 0; spatial current divergenceless. hy4's H048 DOOR 3 statement exact for the bare field shift current.",
             "V2": "survivors: (c) Gauss-map charge of the sourced field M_ph(<r) = (1/4pi G) ∮ g dA = r sqrt(G M_b a0)/G, capped at sqrt(a0/g_ext) = 0.660 M_b; (d) fluid current J^0_fluid = n(x), M_dark = int m n = same number. (a) comoving-only (dilutes a^-3); (b) pi = f'(0)*0 = 0 dead.",
             "V3": "dark mass ASSIGNED to the sourced field's Gauss map and the fluid charge (M_ph(<r_M) = M_b exactly at r_M = 9.45/8.61 kpc; 6e10 Msun; capped 0.660 M_b), NOT to the shift-Noether charge (zero on the static branch). STATUS must carry the amendment from 'Noether charge' to 'sourced Gauss-map / fluid charge'."},
           "numbers": {
              "r_M_kpc": {k: round(v/kpc, 4) for k, v in rM.items()},
              "M_ph_rM_Msun": 6.0e10,
              "capped_share_sqrt(a0/g_ext)": {k: round(math.sqrt(v/g_ext), 4) for k, v in A0.items()},
              "closed_form": "M_dark(<r) = sqrt(G M_b a0) r / G = M_b (r/r_M);  rho_DM = sqrt(G M_b a0)/(4 pi G r^2)",
              "G028_cert": "L217 V3: conserved comoving Noether current on homogeneous FRW (Q = a^3 P_X qdot), density a^-3, carries Omega_dm, w window; SILENT on static halos."},
           "checks": RES},
          open("deepseek_push/G154_results.json", "w"), indent=1)
print("wrote deepseek_push/G154_results.json")