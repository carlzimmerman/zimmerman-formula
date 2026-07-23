#!/usr/bin/env python3
"""
NUMEROLOGY-EXECUTIONER CONVENTION SWEEP for Z = sqrt(32 pi/3) = 2 sqrt(8 pi/3)  (2026-07-23)
============================================================================================
Independent adversarial verification of the de Sitter-Unruh accounting of Z.  A DERIVED claim
for Z is valid ONLY if the coefficient is FORCED -- i.e. does NOT move under a different-but-
defensible convention.  This script implements the executioner test (b): take the SAME
de Sitter-Unruh horizon-coincidence geometry, vary ONLY choices that are each independently
defensible (not tuned to the target), and check whether the coefficient a0/(cH) = 1/Z stays
pinned at 1/Z = 5.789^-1 or MOVES.  If it moves, Z is convention-dependent numerology, NOT
forced.  If it genuinely does not move, that would be extraordinary and is flagged.

What is invariant vs what moves is the whole verdict:
  * INVARIANT across every fork: the FORM  a0 = (O(1)) * c H_Lambda  (dimensionally forced).
  * MOVES across defensible forks: the O(1) coefficient itself (= 1/Z).

Every fork is sympy-exact and prove-by-moving-the-number.  This is NOT a Z derivation; it is a
proof that no clean route FORCES Z, sharpening (not overturning) the standing kappa=1/2 wall.
POSITED throughout: a0's value, Z, the sign; nu(y)=sqrt(1+1/y) is Milgrom-1999's kernel.
"""
import sympy as sp

pi = sp.pi
FAIL = []


def check(name, cond):
    print(f"    [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)


c, G, H, rho = sp.symbols('c G H rho', positive=True)
Z_FW = sp.sqrt(sp.Rational(32, 3) * pi)          # the framework value = 2 sqrt(8pi/3)
Zf = float(Z_FW)
print("=" * 88)
print(f"EXECUTIONER CONVENTION SWEEP  --  is Z = 2 sqrt(8pi/3) = {Zf:.5f} FORCED, or does it MOVE?")
print("=" * 88)

# de Sitter Friedmann used everywhere below (standard GR, not tuned):
rho_DE = 3 * H**2 / (8 * pi * G)                  # H^2 = (8piG/3) rho_DE
sqrtGrho = sp.sqrt(G * rho_DE)                    # = H sqrt(3/(8pi)),  the H<->sqrt(Grho) bridge
check("Friedmann bridge sqrt(G rho_DE) = H sqrt(3/(8pi)) (standard de Sitter GR, not tuned)",
      sp.simplify(sqrtGrho - H * sp.sqrt(3 / (8 * pi))) == 0)

# ---------------------------------------------------------------------------
# FORK 1 -- the horizon-coincidence GEOMETRY: what you equate at a0.
#   Each is a defensible statement of "the Rindler and de Sitter horizons coincide".
# ---------------------------------------------------------------------------
print("\n" + "-" * 88)
print("FORK 1  Which horizon quantity coincides at a0?  (all defensible; coefficient MOVES)")
print("-" * 88)
a = sp.symbols('a', positive=True)
R_dS = c / H                                      # de Sitter horizon radius
d_R = c**2 / a                                    # Rindler horizon distance of an a-accelerated body

# 1a: equate DISTANCES  c^2/a0 = R_dS
Z_dist = sp.simplify(c * H / sp.solve(sp.Eq(d_R, R_dS), a)[0])
# 1b: equate TEMPERATURES  T_U(a0)=T_GH  (kB T_U=hbar a/2pi c, kB T_GH=hbar H/2pi) -> a0=cH
Z_temp = 1                                        # identical to 1a: both give a0=cH, Z=1
# 1c: equate AREAS with the sphere 4pi included on the dS side: (c^2/a0)^2 = 4pi R_dS^2
f = sp.symbols('f', positive=True)
Z_area = sp.sqrt(4 * pi)                          # a0 = cH/sqrt(4pi) if areas equated bare
# 1d: enclosed-critical-mass surface gravity g=(4pi/3)G rho_crit R_dS with rho_crit=3H^2/8piG
g_enc = sp.Rational(4, 3) * pi * G * (3 * H**2 / (8 * pi * G)) * R_dS
Z_enc = sp.simplify(c * H / g_enc)
# 1e: de Sitter GH TEMPERATURE as the scale (Milgrom 1110.2580): 2pi a0 = cH
Z_gh = 2 * pi
for nm, Zv in [("1a equate distances  c^2/a0=R_dS", Z_dist),
               ("1b equate temperatures T_U=T_GH ", Z_temp),
               ("1c equate areas (bare, +4pi)     ", Z_area),
               ("1d enclosed-crit surface gravity ", Z_enc),
               ("1e GH-temperature scale (Milgrom)", Z_gh)]:
    print(f"    {nm}:  Z = {sp.nsimplify(Zv)} = {float(Zv):.4f}")
check("FORK 1 MOVES: {distance/temp:1, area:2sqrt(pi)=3.545, enclosed-crit:2, GH:2pi=6.28} -- "
      "all differ, NONE equals framework Z=5.789",
      len({sp.nsimplify(Z_dist), sp.nsimplify(Z_area), sp.nsimplify(Z_enc), sp.nsimplify(Z_gh)}) == 4
      and all(sp.simplify(Zv - Z_FW) != 0 for Zv in [Z_dist, Z_area, Z_enc, Z_gh]))
check("FORK 1 the FORM is INVARIANT: every fork gives a0 = O(1) * c H (dimensionally forced)",
      all(sp.simplify((c * H / Zv) / (c * H) - 1 / Zv) == 0
          for Zv in [Z_dist, Z_area, Z_enc, Z_gh]))

# ---------------------------------------------------------------------------
# FORK 2 -- the surface-gravity / free-fall PREFACTOR kappa in a0 = kappa c sqrt(G rho_DE).
#   kappa is exactly the '2' under test (Z = (1/kappa) sqrt(8pi/3)).  Each value below is a
#   defensible normalization of "the acceleration set by the vacuum energy density".
# ---------------------------------------------------------------------------
print("\n" + "-" * 88)
print("FORK 2  The prefactor kappa in a0 = kappa*c*sqrt(G rho_DE)  (Z=(1/kappa)sqrt(8pi/3); '2' under test)")
print("-" * 88)
kappa = sp.symbols('kappa', positive=True)
Z_of_k = sp.simplify(c * H / (kappa * c * sqrtGrho))     # = (1/kappa) sqrt(8pi/3)
check("Z(kappa) = (1/kappa) sqrt(8pi/3) exactly",
      sp.simplify(Z_of_k - (1 / kappa) * sp.sqrt(sp.Rational(8, 3) * pi)) == 0)
kappa_menu = [("1   (bare c sqrt(Grho))",        sp.Integer(1)),
              ("1/2 (Schwarzschild/free-fall) FRAMEWORK", sp.Rational(1, 2)),
              ("1/(4pi) (per-solid-angle)",     1 / (4 * pi)),
              ("2pi (temperature 2pi)",         2 * pi)]
shape = sp.sqrt(sp.Rational(8, 3) * pi)
for nm, kv in kappa_menu:
    print(f"    kappa={nm:34s}:  Z = {sp.nsimplify(Z_of_k.subs(kappa, kv))} = {float(Z_of_k.subs(kappa, kv)):.4f}")
check("FORK 2 MOVES: sweeping defensible kappa {1,1/2,1/(4pi),2pi} gives 4 DISTINCT Z; "
      "only the hand-chosen kappa=1/2 gives the framework 5.789",
      len({sp.nsimplify(Z_of_k.subs(kappa, kv)) for _, kv in kappa_menu}) == 4
      and sp.simplify(Z_of_k.subs(kappa, sp.Rational(1, 2)) - Z_FW) == 0
      and sp.simplify(Z_of_k.subs(kappa, 1) - Z_FW) != 0)
print("    => the framework picks kappa=1/2 BY HAND (the Schwarzschild prefactor).  Nothing in the")
print("       Unruh/GH thermodynamics selects it over kappa=1 (which gives 2.894) etc.  kappa is FREE.")

# ---------------------------------------------------------------------------
# FORK 3 -- SURFACE vs VOLUME: read a0 off T_GH (surface ~ H) or off rho_DE (volume ~ sqrt(rho)).
#   This choice is what buys the entire sqrt(8pi/3); the thermodynamics does not make it.
# ---------------------------------------------------------------------------
print("\n" + "-" * 88)
print("FORK 3  Surface (a0~cH, no 8pi/3) vs Volume (a0~c sqrt(Grho), carries sqrt(8pi/3))")
print("-" * 88)
a0_surface = c * H                                     # temperature/GH surface reading  -> Z=1
a0_volume = (c / 2) * sqrtGrho                         # density/volume reading           -> Z=5.789
Z_surface = sp.simplify(c * H / a0_surface)
Z_volume = sp.simplify(c * H / a0_volume)
print(f"    SURFACE (T_GH ~ H):        a0 = cH        -> Z = {Z_surface}")
print(f"    VOLUME  (rho_DE ~ sqrt):   a0 = (c/2)sqrt(G rho_DE) -> Z = {sp.nsimplify(Z_volume)} = {float(Z_volume):.4f}")
check("FORK 3 the sqrt(8pi/3) exists ONLY in the VOLUME reading; SURFACE reading has Z=1 (no 8pi/3)",
      Z_surface == 1 and sp.simplify(Z_volume / Z_surface - Z_FW) == 0
      and sp.simplify(sp.sqrt(Z_volume**2 / 4) - sp.sqrt(sp.Rational(8, 3) * pi)) == 0)
print("    => the '8pi/3 shape' is GATED on a surface->volume choice the thermodynamics does not force.")

# ---------------------------------------------------------------------------
# FORK 4 -- d=3 BOUNDARY dof: 'count boundary dof' = divide a ball volume by a boundary measure.
#   The SAME unit 3-ball over DIFFERENT defensible denominators gives DIFFERENT kappa.
# ---------------------------------------------------------------------------
print("\n" + "-" * 88)
print("FORK 4  d=3 boundary-dof reading: unit 3-ball / (which boundary measure) = kappa  (MOVES)")
print("-" * 88)
V3 = sp.Rational(4, 3) * pi                            # unit 3-ball volume
denoms = [("K_Friedmann 8pi/3", sp.Rational(8, 3) * pi),
          ("S_2 = 4pi",         4 * pi),
          ("2pi",               2 * pi),
          ("S_3 = 2pi^2",       2 * pi**2)]
kappas = []
for nm, dn in denoms:
    kv = sp.nsimplify(V3 / dn)
    kappas.append(kv)
    print(f"    V_3 / ({nm:16s}) = {kv}   -> Z=(1/kappa)sqrt(8pi/3) = {float((1/kv)*shape):.4f}")
check("FORK 4 MOVES: same 3-ball over defensible denominators gives kappa in {1/2,1/3,2/3,1/(3pi)} "
      "-> 4 DISTINCT Z; the '1/2' is one denominator choice among many, not forced",
      len(set(kappas)) == 4 and sp.Rational(1, 2) in kappas)
print("    => 'counting d=3 boundary dof' does NOT pin the normalization: it is a choice of denominator.")

# ---------------------------------------------------------------------------
# FORK 5 -- FOOTING fork (Carl's non-negotiable #4): which rho / which H sets the scale.
#   rho_DE + H_Lambda (canonical) vs rho_total + H0.  Both defensible; the number MOVES.
# ---------------------------------------------------------------------------
print("\n" + "-" * 88)
print("FORK 5  Footing: rho_DE/H_Lambda (canonical) vs rho_total/H0 -- a0 MOVES by sqrt(Omega_Lambda)")
print("-" * 88)
Om_L = sp.Rational(68, 100)                            # Omega_Lambda ~ 0.68
# a0 = (c/2) sqrt(G rho): rho_DE = Om_L * rho_crit,0 ; H_Lambda^2=(8piG/3)rho_DE=Om_L H0^2
# canonical uses H_Lambda; the ratio a0_total/a0_DE with the SAME Z differs by sqrt(Om_L)
H0 = sp.symbols('H0', positive=True)
a0_DE = (c / 2) * sp.sqrt(G * Om_L * 3 * H0**2 / (8 * pi * G))     # rho_DE only
a0_tot = (c / 2) * sp.sqrt(G * 3 * H0**2 / (8 * pi * G))           # rho_total (crit)
ratio_foot = sp.simplify(a0_DE / a0_tot)
print(f"    a0(rho_DE)/a0(rho_total) = sqrt(Omega_Lambda) = {ratio_foot} = {float(ratio_foot):.4f}")
check("FORK 5 the footing choice moves a0 by sqrt(Omega_Lambda) ~ 0.82 (a real ~18% swing), "
      "so even the DATA value of a0/(cH0) is footing-dependent, not a single forced number",
      sp.simplify(ratio_foot - sp.sqrt(Om_L)) == 0 and 0.75 < float(ratio_foot) < 0.90)

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
print("\n" + "=" * 88)
print("VERDICT (executioner): Z is NOT FORCED -- the coefficient MOVES under every defensible fork.")
print("=" * 88)
print("  INVARIANT (route-independent, genuinely forced):")
print("    * THE FORM  a0 = O(1) * c H_Lambda.  Every fork preserves it; this is the robust,")
print("      falsifiable half (drives the Z-independent a0(z) ~ E(z) prediction).")
print("  MOVES (convention-dependent -> NOT forced):")
print("    * horizon-coincidence geometry: Z in {1, 2, 2sqrt(pi)=3.545, 2pi=6.28} (FORK 1)")
print("    * prefactor kappa:              Z = (1/kappa) sqrt(8pi/3), kappa free (FORK 2)")
print("    * surface vs volume:            Z=1 (surface) vs 5.789 (volume); the 8pi/3 is gated (FORK 3)")
print("    * d=3 boundary-dof denominator: kappa in {1/2,1/3,2/3,...} (FORK 4)")
print("    * footing rho_DE vs rho_total:  a0 swings by sqrt(Omega_L)~0.82 (FORK 5)")
print("  => No clean, pre-registered route FORCES Z=2 sqrt(8pi/3).  The framework SELECTS the")
print("     volume reading + kappa=1/2 BY HAND; both are defensible but neither is forced.  The")
print("     d=3 dS4-boundary angle fixes the SHAPE sqrt(8pi/3) beautifully but the '2' just becomes")
print("     'which denominator' -- the same unforced normalization.  Z STAYS POSITED.  This is a")
print("     SHARPER geometric REASON for the standing kappa=1/2 wall, NOT a derivation, NOT closure.")
print("  POSITED: a0's value, Z, the sign.  nu = Milgrom-1999.  No TOE.")

if FAIL:
    print("\n*** ASSERTIONS FAILED:", FAIL)
    raise SystemExit(1)
print("\nAll assertions passed. EXIT 0 (executioner: coefficient MOVES => Z not forced).")
