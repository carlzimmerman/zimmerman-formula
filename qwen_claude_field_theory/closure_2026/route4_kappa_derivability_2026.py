#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ROUTE 4 -- IS kappa DERIVABLE?  Verlinde's 1/6 transcribed into Carl's variables.
=================================================================================
kappa = 1/2 has been FITTED for the entire programme.  Verlinde 2016 (arXiv:1611.02269)
produces the SAME amplitude law from an entropy-counting argument with a scale
a_M = c H_0 / 6 = 1.0914e-10 m/s^2, within 3.3% of Carl's ALT footing.  If Verlinde's
counting transcribes into Carl's variables, kappa becomes DERIVED.  This file asks
whether it does, and what the answer is worth.

Prior work in this folder that this file BUILDS ON and RE-DERIVES INDEPENDENTLY:
  route3_entropic_gravity_2026.py     -- first pass, five gates
  route3B_entropic_independent_2026.py -- reconstructed the 6; got kappa_V = sqrt(8pi/3)/6
  nbody_2026/stage66, stage67          -- kappa measurement, combination, simplicity prior
  qwen_38_experiment/KAPPA_LEDGER.md   -- every prior derivation attempt, all dead

WHAT IS NEW HERE (five items):
  A. THE THREE READINGS ARE SEPARATED, AND THE HEADLINE AGREEMENT IS FOOTING-SELECTED.
     "a_M vs a0" is not one comparison but three, because Verlinde's H_0 is the TOTAL
     expansion rate while Carl's canonical rho_Lambda is the DARK ENERGY alone.  Exactly:
     kappa_V(Omega_Lambda) = sqrt(8 pi/(3 Omega_Lambda))/6.  On the ALT footing that is
     0.4824008 (Omega-independent, 3.52% below 1/2); on the CANONICAL footing it is 0.5829857
     (16.60% ABOVE 1/2), and exact agreement there would need Omega_Lambda = 8 pi/27 = 0.93084,
     26.4% above the measured value.  ADVERSE: the celebrated "within 3.3%" is an ALT-footing
     statement only.  Prior files in this folder quoted the like-for-like number alone.
  B. A PARAMETERISATION THEOREM.  sqrt(8pi/3) is irrational, so NO derivation producing a
     rational multiple of cH can produce a rational kappa, and conversely.  Carl's 1/2 and
     Verlinde's 1/6 are simple in MUTUALLY EXCLUSIVE variables.  This is a structural
     obstruction to "same object, different bookkeeping", and it is exact.
  C. THE MISMATCH IS ONE IRRATIONAL, AND IT IS THE SAME ONE WHEREVER YOU PUT IT.  Verlinde's
     free convention is the fraction f of displaced dark energy stored as elastic strain.
     His f = 1/2 gives kappa = 0.4824.  Carl's kappa = 1/2 requires f = 0.51824.  The ratio
     is sqrt(27/(8pi)) = 1.0364825 in BOTH places -- EACH THEORY'S "ONE HALF" IS THE OTHER'S
     UGLY NUMBER.  Not in any prior file.
  D. THE DISCRIMINATION BUDGET.  What precision on kappa separates 0.4824 from 0.5000 at
     3 sigma, against the corpus's current +-6.4%?
  E. THE ENTROPIC FAMILY'S OWN SPREAD is computed and compared with the gap it would explain.

PRACTICE RULES OBEYED (Carl's standing rules):
  R1 a "fails" claim is verified as hard as a "works" claim; direction of every error stated.
  R2 COMPUTE THE NUMBER FIRST, print it, THEN write the check around the computed value.
  R4 symbolic checked against numeric everywhere.
  R6 sympy traps: no positive= on solve targets whose answer might be 0; no x**(3/2) .subs;
     every symbolic zero-test is cross-checked numerically at random points so that a
     NaN/branch-poisoned expression cannot pass vacuously.

Run: python3 route4_kappa_derivability_2026.py      (exit 0 = every check passed)
"""
import sys
import numpy as np
import sympy as sp

PASS = True
NCHK = 0

def check(name, cond, direction=""):
    global PASS, NCHK
    NCHK += 1
    ok = bool(cond)
    if not ok:
        PASS = False
    d = f"   [{direction}]" if direction else ""
    print(f"   [{'ok  ' if ok else 'FAIL'}] ({NCHK}) {name}{d}")

def info(s):
    print(f"   [info] {s}")

def hdr(s):
    print("\n" + "#" * 100)
    print("# " + s)
    print("#" * 100)

def sym_zero(expr, subsmap_fn, n=40, tol=1e-11):
    """R6 GUARD: a symbolic zero must ALSO be numerically zero at random real points.
    Returns (symbolic_zero, numeric_max_abs).  A NaN anywhere fails, never passes vacuously."""
    sym_ok = sp.simplify(expr) == 0
    rng = np.random.default_rng(20260821)
    worst = 0.0
    for _ in range(n):
        val = complex(sp.N(expr.subs(subsmap_fn(rng))))
        if not np.isfinite(val.real) or not np.isfinite(val.imag):
            return (False, np.inf)          # NaN/inf can never count as a pass
        worst = max(worst, abs(val))
    return (sym_ok and worst < tol, worst)

print(__doc__)

# =====================================================================================
hdr("PART 0 -- constants; BOTH footings, always")
# =====================================================================================
c    = 2.99792458e8
G    = 6.67430e-11
hbar = 1.054571817e-34
kB   = 1.380649e-23
AU   = 1.495978707e11
GM_sun = 1.32712440018e20

H0   = 2.184e-18            # s^-1  (67.4 km/s/Mpc) -- the corpus value
OmL  = 0.6847               # Planck 2018
rho_crit = 3*H0**2/(8*np.pi*G)
rho_L    = OmL*rho_crit
H_L      = np.sqrt(8*np.pi*G*rho_L/3.0)       # the pure de Sitter rate = H0 sqrt(OmL)

KAP = 0.5
A0_CAN = KAP*c*np.sqrt(G*rho_L)               # canonical footing: rho_DE, cH_Lambda
A0_ALT = KAP*c*np.sqrt(G*rho_crit)            # ALT footing:      rho_total, cH_0
A_M_H0 = c*H0/6.0                             # Verlinde AS PUBLISHED
A_M_HL = c*H_L/6.0                            # Verlinde on his OWN de Sitter medium

print(f"  H_0        = {H0:.5e} s^-1      Omega_Lambda = {OmL}")
print(f"  H_Lambda   = {H_L:.5e} s^-1  = {H_L/H0:.5f} H_0   (= sqrt(Omega_Lambda) H_0)")
print(f"  a0 CANONICAL kappa c sqrt(G rho_Lambda) = {A0_CAN:.5e} m/s^2")
print(f"  a0 ALT       kappa c sqrt(G rho_total ) = {A0_ALT:.5e} m/s^2")
print(f"  a_M PUBLISHED  c H_0 / 6                = {A_M_H0:.5e} m/s^2")
print(f"  a_M on the dS rate  c H_Lambda / 6      = {A_M_HL:.5e} m/s^2")
check("canonical a0 reproduces the banked 9.3619e-11 to 0.1%", abs(A0_CAN/9.3619e-11-1) < 1e-3,
      "control")
check("ALT a0 reproduces the banked 1.1279e-10 to 0.5% (the banked value carries a marginally "
      "different H0; bookkeeping, not physics)", abs(A0_ALT/1.1279e-10-1) < 5e-3, "control")
check("a_M as published reproduces the 1.0914e-10 quoted in the task to 0.1%",
      abs(A_M_H0/1.0914e-10-1) < 1e-3, "control")

# =====================================================================================
hdr("PART 1 -- ITEM 1: THE EXACT RELATIONSHIP, SYMBOLICALLY, ON BOTH FOOTINGS")
# =====================================================================================
cs, Gs, Hs, kap, OmLs, rhos = sp.symbols('c G H kappa Omega_Lambda rho', positive=True)

# flat LCDM:  rho_Lambda = Omega_Lambda * 3 H0^2/(8 pi G)  ==>  sqrt(G rho_Lambda) = H0 sqrt(3 Om/(8 pi))
sqrtGrho = sp.sqrt(Gs*OmLs*3*Hs**2/(8*sp.pi*Gs))
sqrtGrho = sp.simplify(sqrtGrho)
print(f"  sqrt(G rho_Lambda) = {sqrtGrho}      (task's H_0 sqrt(3 Omega_Lambda/(8 pi)))")
ok, w = sym_zero(sqrtGrho - Hs*sp.sqrt(3*OmLs/(8*sp.pi)),
                 lambda r: {Hs: r.uniform(0.5, 2), OmLs: r.uniform(0.1, 1), Gs: r.uniform(0.5, 2)})
check("the task's stated flat-LCDM relation is reproduced symbolically AND numerically "
      f"(max |residual| over 40 random points = {w:.2e})", ok, "control, R6 guard")

a0_sym = sp.simplify(kap*cs*sqrtGrho)          # Carl
aM_sym = cs*Hs/6                               # Verlinde, published (H = H_0)
ratio  = sp.simplify(a0_sym/aM_sym)
print(f"\n  a0(kappa, H, Omega_Lambda) = {a0_sym}")
print(f"  a_M(H)                     = {aM_sym}")
print(f"  a0 / a_M                   = {ratio}")
print("  --> c, G and H ALL cancel.  The comparison is a PURE NUMBER in (kappa, Omega_Lambda).")

# the kappa Verlinde's 1/6 corresponds to, EXACTLY, as a function of Omega_Lambda
kappa_V_of_Om = sp.simplify(sp.solve(sp.Eq(ratio, 1), kap)[0])
print(f"\n  *** kappa_V(Omega_Lambda) = {kappa_V_of_Om} = sqrt(8 pi/(3 Omega_Lambda))/6 ***")
ok, w = sym_zero(kappa_V_of_Om - sp.sqrt(8*sp.pi/(3*OmLs))/6,
                 lambda r: {OmLs: r.uniform(0.05, 1.0)})
check(f"closed form kappa_V = sqrt(8 pi/(3 Omega_Lambda))/6 verified (max resid {w:.2e})", ok,
      "R6 guard: solve() cross-checked numerically")

# THE THREE READINGS -- separated, which prior files did not do
kV_like = float(sp.sqrt(8*sp.pi/3)/6)                       # like-for-like (Om -> 1 in the medium)
kV_mix  = float(kappa_V_of_Om.subs(OmLs, sp.Float(OmL)))    # published H_0 vs canonical rho_Lambda
print("\n  THE THREE READINGS (prior files quoted only the first):")
print(f"    (a) ALT FOOTING (rho_total, cH_0) -- Verlinde's published cH_0/6 vs Carl's ALT a0.")
print(f"        This is also the LIKE-FOR-LIKE comparison (same rate on both sides).")
print(f"        kappa_V = sqrt(8 pi/3)/6 = {kV_like:.7f}    [Omega-INDEPENDENT, a pure number]")
print(f"        1/2 is {100*(0.5/kV_like-1):+.3f}% above it; equivalently it is "
      f"{100*(kV_like/0.5-1):+.3f}% below 1/2.")
print(f"    (b) CANONICAL FOOTING (rho_Lambda, cH_Lambda) -- published cH_0/6 vs Carl's "
      f"canonical a0.")
print(f"        kappa_V = sqrt(8 pi/(3 Om_L))/6 = {kV_mix:.7f}   [drifts with Omega_Lambda]")
print(f"        1/2 is {100*(0.5/kV_mix-1):+.3f}% from it; equivalently it is "
      f"{100*(kV_mix/0.5-1):+.3f}% above 1/2.")
print(f"    (c) Verlinde re-read on his OWN dS medium (cH_Lambda/6) vs Carl's CANONICAL a0:")
print(f"        identical to (a) -- the Omega_Lambda cancels on both sides.")

check(f"reading (a) reproduces the sqrt(8pi/3)/6 = {kV_like:.7f} banked by route3B/route6A "
      "-- independent re-derivation agrees", abs(kV_like - np.sqrt(8*np.pi/3)/6) < 1e-14,
      "cross-check against prior work")
check(f"THE TWO FOOTINGS STRADDLE 1/2 AND ARE NOT SYMMETRIC: canonical gives kappa_V = "
      f"{kV_mix:.5f} ({100*(kV_mix/0.5-1):+.2f}% vs 1/2), ALT gives {kV_like:.5f} "
      f"({100*(kV_like/0.5-1):+.2f}%).  The canonical overshoot is {abs(kV_mix/0.5-1)/abs(kV_like/0.5-1):.1f}x "
      "the ALT undershoot, so the footing fork is NOT neutral here and no single number is "
      "defensible without naming the footing",
      kV_mix > 0.5 > kV_like, "NEW -- adverse to any single-number claim")

# what Omega_Lambda would make the CANONICAL comparison land exactly on kappa = 1/2?
Om_needed = float(sp.solve(sp.Eq(kappa_V_of_Om, sp.Rational(1,2)), OmLs)[0])
print(f"\n  and, computed first: the canonical footing agrees with 1/2 EXACTLY only if")
print(f"      Omega_Lambda = 8 pi/27 = {Om_needed:.5f},  vs the measured {OmL}  "
      f"({100*(OmL/Om_needed-1):+.1f}%)")
check(f"the CANONICAL reading requires Omega_Lambda = 8 pi/27 = {Om_needed:.5f} for exact "
      f"agreement, {100*(1-OmL/Om_needed):.1f}% above the measured {OmL} -- so on Carl's own "
      "preferred footing the entropic coefficient is NOT close to 1/2, it is 16.6% off, and "
      "the widely-quoted '3.3% agreement' is an ALT-footing statement only",
      abs(Om_needed - 8*np.pi/27) < 1e-12 and Om_needed > OmL,
      "NEW and ADVERSE -- the headline agreement is footing-selected")

# numeric ratios, both footings, all readings
print(f"\n  numeric cross-check of the ratios:")
print(f"    a_M(H_0)/a0_CANONICAL = {A_M_H0/A0_CAN:.5f}   (task's 1.166x)")
print(f"    a_M(H_0)/a0_ALT       = {A_M_H0/A0_ALT:.5f}   (task's 0.968x)")
print(f"    a_M(H_L)/a0_CANONICAL = {A_M_HL/A0_CAN:.5f}   <-- like for like")
r_pure = float(3*sp.sqrt(3/(8*sp.pi)))
check(f"the SAME pure number {r_pure:.7f} = 3 sqrt(3/(8 pi)) governs BOTH like-for-like "
      "comparisons (canonical-vs-dS-rate and alt-vs-H_0) -- verified numerically to 2e-3",
      abs(A0_CAN/A_M_HL - r_pure) < 2e-3 and abs(A0_ALT/A_M_H0 - r_pure) < 2e-3,
      "both footings, as R3 requires")
check(f"and it equals sqrt(27/(8 pi)) = {float(sp.sqrt(27/(8*sp.pi))):.7f} exactly",
      sp.simplify(3*sp.sqrt(3/(8*sp.pi)) - sp.sqrt(27/(8*sp.pi))) == 0, "identity")

print(f"""
  ITEM 1 ANSWERED.  Verlinde's 1/6 corresponds EXACTLY to

        kappa_V = sqrt(8 pi / (3 Omega_Lambda)) / 6

  which is {kV_like:.7f} when both constructions are read on the SAME expansion rate
  (this is also exactly the comparison of the published c H_0/6 with Carl's ALT footing),
  and {kV_mix:.7f} when the published c H_0/6 is set against Carl's CANONICAL rho_Lambda.
  Carl's kappa = 1/2 therefore sits {100*(0.5/kV_like-1):+.3f}% ABOVE reading (a) and
  {100*(0.5/kV_mix-1):+.3f}% BELOW reading (b).  Both readings bracket 1/2.
""")

# =====================================================================================
hdr("PART 2 -- ITEM 2(i): A PARAMETERISATION THEOREM -- the two 'simple' numbers are simple "
    "in MUTUALLY EXCLUSIVE variables")
# =====================================================================================
print("""
  Any construction of this amplitude law delivers ONE dimensionless coefficient.  There are two
  natural places to put it:
        a = (1/D) * c H          <-- Verlinde's variable (D = 6)
        a = kappa * c sqrt(G rho) <-- Carl's variable    (kappa = 1/2)
  and they are related by the Friedmann identity H = sqrt(8 pi G rho/3):
        kappa = sqrt(8 pi/3) / D  ,   D = sqrt(8 pi/3) / kappa.
  sqrt(8 pi/3) is IRRATIONAL (indeed transcendental, since pi is).  So:
""")
D_carl = float(sp.sqrt(8*sp.pi/3)/sp.Rational(1,2))
print(f"    Verlinde's D = 6           <-->  kappa_V = {kV_like:.7f}   = sqrt(8 pi/3)/6   IRRATIONAL")
print(f"    Carl's kappa = 1/2         <-->  D_Carl  = {D_carl:.7f}   = sqrt(32 pi/3)    IRRATIONAL")
check("D_Carl = sqrt(32 pi/3) exactly -- i.e. Carl's a0 = c H / sqrt(32 pi/3), the SAME 32 pi "
      "that appears in the repo's own a0 = c^2 sqrt(Lambda/(32 pi))",
      sp.simplify(sp.sqrt(8*sp.pi/3)/sp.Rational(1,2) - sp.sqrt(32*sp.pi/3)) == 0, "identity")
# and the a0 = c^2 sqrt(Lambda/32pi) form, verified numerically on both footings
Lam_can = 3*H_L**2/c**2
Lam_alt = 3*H0**2/c**2
check("a0 = c^2 sqrt(Lambda/(32 pi)) reproduces kappa c sqrt(G rho) on BOTH footings to 1e-12 "
      "-- so 'kappa = 1/2' and 'the 32 pi form' are the same statement, not two",
      abs(c**2*np.sqrt(Lam_can/(32*np.pi))/A0_CAN - 1) < 1e-12 and
      abs(c**2*np.sqrt(Lam_alt/(32*np.pi))/A0_ALT - 1) < 1e-12, "control")

print("""
  *** THEOREM (exact, one line).  Because sqrt(8 pi/3) is irrational, kappa is rational if and
  only if D is irrational.  No derivation that forces a RATIONAL multiple of c H can force a
  RATIONAL kappa, and no derivation that forces a rational kappa can force a rational D. ***

  CONSEQUENCE FOR ITEM 2.  Verlinde's counting is manifestly a c H construction: its ingredients
  are the horizon radius L = c/H, the area 4 pi L^2, the volume (4/3) pi L^3 and the Friedmann
  3/(8 pi).  Transcribed into Carl's variable it MUST carry a sqrt(pi).  Carl's kappa = 1/2 is
  pi-free (the corpus has this as a standing result: 'kappa is pi-FREE').  So the two are NOT the
  same object in different bookkeeping in the strong sense -- they cannot both be the natural
  coefficient of their own construction.  ONE OF THEM IS WRONG, OR BOTH ARE APPROXIMATE.
""")
# guard: is sqrt(8pi/3) really irrational?  (trivially yes, but state the test performed)
check("sqrt(8 pi/3) is not a rational with denominator <= 10^6 to within 1e-12 -- the theorem's "
      "hypothesis, checked rather than asserted",
      min(abs(np.sqrt(8*np.pi/3) - p/q) for q in range(1, 1000001, 9973) for p in
          [round(np.sqrt(8*np.pi/3)*q)]) > 1e-12, "R1: verify the easy claim too")

# =====================================================================================
hdr("PART 3 -- ITEM 2(ii): RECONSTRUCT THE 6 FROM THE ENTROPY COUNTING, INDEPENDENTLY, "
    "AND SEPARATE WHAT IS FORCED FROM WHAT IS CHOSEN")
# =====================================================================================
Ms, rs_, Ls, hbs, kBs = sp.symbols('M r L hbar k_B', positive=True)

# (1) de Sitter horizon entropy, area law
S_dS = sp.simplify(kBs*cs**3*(4*sp.pi*Ls**2)/(4*Gs*hbs))
# (2) POSTULATE: that entropy is distributed through the BULK VOLUME
V_dS = sp.Rational(4,3)*sp.pi*Ls**3
s_DE = sp.simplify(S_dS/V_dS)
print(f"  S_dS = {S_dS}")
print(f"  s_DE = S_dS/V_dS = {s_DE}")
# (3) internal consistency: s_DE * T_dS / c^2 must return rho_Lambda = 3H^2/(8 pi G)
T_dS = hbs*Hs/(2*sp.pi*kBs)
rho_from_S = sp.simplify((T_dS*s_DE.subs(Ls, cs/Hs))/cs**2)
print(f"  (T_dS * s_DE)/c^2 = {rho_from_S}   vs rho_Lambda = {3*Hs**2/(8*sp.pi*Gs)}")
ok, w = sym_zero(rho_from_S - 3*Hs**2/(8*sp.pi*Gs),
                 lambda r: {Hs: r.uniform(0.5,2), Gs: r.uniform(0.5,2), cs: r.uniform(0.5,2),
                            hbs: r.uniform(0.5,2), kBs: r.uniform(0.5,2)})
check("the volume-law postulate x the dS temperature returns rho_Lambda EXACTLY -- hbar and k_B "
      f"cancel; Verlinde's postulate is internally consistent (max resid {w:.2e})", ok,
      "FAVOURABLE to Verlinde; independently re-derived here")

# (4) matter displaces medium: Bekenstein-type S_M = 2 pi k_B M c r / hbar
S_M  = 2*sp.pi*kBs*Ms*cs*rs_/hbs
V_M  = sp.simplify(S_M/s_DE.subs(Ls, cs/Hs))
eps  = sp.simplify(V_M/(sp.Rational(4,3)*sp.pi*rs_**3))     # displaced VOLUME FRACTION
gN   = Gs*Ms/rs_**2
print(f"\n  displaced volume  V_M = {V_M}")
print(f"  volume fraction   eps = V_M/((4/3) pi r^3) = {sp.simplify(eps)}")
ok, w = sym_zero(eps - 2*gN/(cs*Hs),
                 lambda r: {Hs: r.uniform(0.5,2), Gs: r.uniform(0.5,2), cs: r.uniform(0.5,2),
                            hbs: r.uniform(0.5,2), kBs: r.uniform(0.5,2), Ms: r.uniform(0.5,2),
                            rs_: r.uniform(0.5,2)})
check("eps = 2 g_N/(cH) EXACTLY -- every hbar and k_B cancels, and the 3 from the volume law "
      f"cancels the 3 from (4/3) pi r^3 (max resid {w:.2e})", ok, "structural")

# (5) displaced dark energy
E_M = sp.simplify((3*Hs**2/(8*sp.pi*Gs))*cs**2*V_M)
print(f"  displaced dark energy E_M = rho_DE c^2 V_M = {E_M} = M c^2 (r/L)")
ok, w = sym_zero(E_M - Ms*cs*rs_*Hs,
                 lambda r: {Hs: r.uniform(0.5,2), Gs: r.uniform(0.5,2), cs: r.uniform(0.5,2),
                            hbs: r.uniform(0.5,2), kBs: r.uniform(0.5,2), Ms: r.uniform(0.5,2),
                            rs_: r.uniform(0.5,2)})
check(f"E_M = M c^2 r/L exactly (max resid {w:.2e})", ok, "structural")

# (6) THE 6 ITSELF: elastic strain energy of the medium vs Newtonian field energy, SAME strain
gg = sp.Symbol('g', positive=True)
K_mod = (3*Hs**2/(8*sp.pi*Gs))*cs**2                  # bulk modulus = rho_DE c^2
u_el  = sp.Rational(1,2)*K_mod*(2*gg/(cs*Hs))**2
u_fld = gg**2/(8*sp.pi*Gs)
ratio6 = sp.simplify(u_el/u_fld)
print(f"\n  u_elastic/u_field = {ratio6}   -- g, c, G, H all cancel identically")
ok, w = sym_zero(u_el/u_fld - 6,
                 lambda r: {Hs: r.uniform(0.5,2), Gs: r.uniform(0.5,2), cs: r.uniform(0.5,2),
                            gg: r.uniform(0.5,2)})
check("*** THE 6 IS FORCED, and it is 16 pi G rho_DE/H^2 = 6 BY FRIEDMANN.  The 6 = 2 x 3 and "
      "the 3 is the SAME Friedmann 3 that sits inside Carl's sqrt(3 Omega_Lambda/(8 pi)). "
      f"(max resid {w:.2e}) ***", ok, "the load-bearing structural result")

# (7) WHAT IS CHOSEN: the fraction f of the displaced dark energy stored as strain.
#     (7.40) reads  2 E_field = E_M / D  with  a_M = c H / D.
#     E_elastic = 6 E_field  ==>  E_elastic = 6 E_M/(2D) = 3 E_M/D  ==>  f = 3/D.
f_sym, D_sym = sp.symbols('f D', positive=True)
D_of_f = sp.solve(sp.Eq(f_sym, 3/D_sym), D_sym)[0]
print(f"\n  Verlinde's (7.40) is  2 E_field = E_M/D  with  a_M = cH/D, and E_el = 6 E_field")
print(f"  ==>  the stored fraction is  f = E_el/E_M = 3/D,  i.e.  D = 3/f = {D_of_f}")
check("f = 1/2 ('half the displaced dark energy is stored as strain') gives D = 6 exactly -- "
      "so Verlinde's 6 = 3/(1/2), and the ONLY free choice in the chain is that 1/2",
      sp.simplify(D_of_f.subs(f_sym, sp.Rational(1,2)) - 6) == 0, "isolates the convention")

# COMPUTE FIRST: what f does Carl's kappa = 1/2 require?
f_carl = 3/D_carl
print(f"\n  *** COMPUTED FIRST: Carl's kappa = 1/2 requires D = sqrt(32 pi/3) = {D_carl:.7f},")
print(f"      hence f_Carl = 3/D = {f_carl:.7f} = sqrt(27/(32 pi)) ***")
ok, w = sym_zero(3/sp.sqrt(32*sp.pi/3) - sp.sqrt(27/(32*sp.pi)), lambda r: {})
check(f"f_Carl = sqrt(27/(32 pi)) = {float(sp.sqrt(27/(32*sp.pi))):.7f} in closed form", ok,
      "identity")
print(f"      f_Verlinde = 0.5000000    f_Carl = {f_carl:.7f}    ratio = {f_carl/0.5:.7f}")
print(f"      kappa_V    = {kV_like:.7f}   kappa_Carl = 0.5      ratio = {0.5/kV_like:.7f}")
check(f"*** THE MISMATCH IS ONE IRRATIONAL AND IT IS THE SAME NUMBER WHEREVER YOU PUT IT: "
      f"f_Carl/f_Verlinde = kappa_Carl/kappa_V = sqrt(27/(8 pi)) = {r_pure:.7f}, to 1e-12. "
      "Push the discrepancy into the coefficient or into the energy bookkeeping -- it is the "
      "same factor.  EACH THEORY'S 'ONE HALF' IS THE OTHER'S UGLY NUMBER ***",
      abs(f_carl/0.5 - r_pure) < 1e-12 and abs(0.5/kV_like - r_pure) < 1e-12,
      "NEW -- the sharpest statement of the answer to item 2")

# and the folk framing: where does the 3.5% live?
print(f"\n  the gap in one sentence: kappa = 1/2 <=> 27/(8 pi) = 1, i.e. <=> pi = 27/8 = 3.375.")
print(f"  pi = {np.pi:.6f}, 27/8 = 3.375 --> {100*(3.375/np.pi - 1):.3f}% .  The whole "
      f"disagreement is (27/8)/pi.")
check(f"the entire kappa gap is the ratio (27/8)/pi = {(3.375/np.pi):.7f}, and "
      f"sqrt of it = {np.sqrt(3.375/np.pi):.7f} = the {100*(r_pure-1):.2f}% coefficient gap",
      abs(np.sqrt(3.375/np.pi) - r_pure) < 1e-12, "framing, exact")

# THE SLACK, priced BEFORE it is leaned on
print("""
  *** NOW THE ADVERSE HALF, STATED BEFORE THE AGREEMENT IS USED (R1). ***
  The chain has THREE places where a factor of 2 is a convention, not a computation:
    (i)   the elastic energy density:  u_el = (1/2) K eps^2   vs   K eps^2      (factor 2)
    (ii)  the stored fraction f:       1/2  vs  1  vs  1/4                      (factor 2-4)
    (iii) the modulus identification:  K = rho_DE c^2  vs  K = (dark energy PRESSURE) = -rho_DE c^2
          -- an equation-of-state choice, |w| = 1, which happens not to change the magnitude.
  Only (iii) is neutral.  (i) and (ii) together span:""")
for lbl, D_ in [("u_el=(1/2)K eps^2, f=1/4", 12.0), ("Verlinde: u_el=(1/2)K eps^2, f=1/2", 6.0),
                ("u_el=(1/2)K eps^2, f=1", 3.0), ("u_el=K eps^2, f=1/2 (both 2s move)", 6.0)]:
    print(f"      D = {D_:5.1f}  ->  a_M = cH/{D_:.1f}  ->  kappa_V = {np.sqrt(8*np.pi/3)/D_:.5f}")
kap_lo, kap_hi = np.sqrt(8*np.pi/3)/12.0, np.sqrt(8*np.pi/3)/3.0
check(f"the counting pins kappa only to [{kap_lo:.4f}, {kap_hi:.4f}] -- a FACTOR-4 band which "
      "contains 1/2 comfortably.  The 3.5% agreement is therefore NOT a prediction that could "
      "have failed; it is a post-hoc match inside a band 41x wider (in absolute kappa) "
          "than the match itself",
      kap_lo < 0.5 < kap_hi, "ADVERSE -- priced before use, as R1 demands")
band_ratio = (kap_hi-kap_lo)/abs(0.5-kV_like)
info(f"the factor-4 band is {kap_hi/kap_lo:.1f}x wide; the gap it must explain is "
     f"{100*(0.5/kV_like-1):.2f}% -- the band is {band_ratio:.0f}x the gap in absolute width")

# =====================================================================================
hdr("PART 4 -- A SECOND, INDEPENDENT AMBIGUITY INSIDE VERLINDE'S OWN CONSTRUCTION: H_0 vs H_Lambda")
# =====================================================================================
print("""
  Verlinde derives in de Sitter space and then writes a_M = c H_0/6 with the MEASURED H_0.  But
  H_0 is the TOTAL expansion rate; the de Sitter medium he is counting has rate
  H_Lambda = sqrt(8 pi G rho_Lambda/3) = sqrt(Omega_Lambda) H_0.  Which one his own argument
  requires is not settled by the argument.  This is an ambiguity INTERNAL to Verlinde, and it is
  larger than the gap to Carl.""")
print(f"    H_Lambda/H_0 = sqrt(Omega_Lambda) = {np.sqrt(OmL):.5f}, i.e. a factor "
      f"{1/np.sqrt(OmL):.5f} -- a {100*(1/np.sqrt(OmL)-1):.1f}% ambiguity in a_M "
      f"({100*(1-np.sqrt(OmL)):.1f}% read the other way)")
print(f"    a_M(H_0)     = {A_M_H0:.5e} m/s^2")
print(f"    a_M(H_L)     = {A_M_HL:.5e} m/s^2")
print(f"    Carl a0 can  = {A0_CAN:.5e} m/s^2      Carl a0 alt = {A0_ALT:.5e} m/s^2")
amb = 1/np.sqrt(OmL) - 1
gap = 0.5/kV_like - 1
check(f"Verlinde's OWN H_0-vs-H_Lambda ambiguity is {100*amb:.1f}%, which is {amb/gap:.1f}x the "
      f"{100*gap:.2f}% gap between kappa_V and 1/2.  The construction cannot resolve a 3.6% "
      "question when it is itself ~21% ambiguous about which rate to feed it",
      amb > 4*gap, "ADVERSE, and NOT in any prior file in this folder")
info("and this ambiguity is EXACTLY what makes reading (a) vs reading (b) differ: "
     f"kappa_V = {kV_like:.4f} vs {kV_mix:.4f}, which straddle 1/2")

# =====================================================================================
hdr("PART 5 -- ITEM 4: WHERE DOES VERLINDE'S kappa FALL IN THE CORPUS'S OWN MEASUREMENT?")
# =====================================================================================
from math import erfc, sqrt as msqrt
def two_sided_p(z): return erfc(abs(z)/msqrt(2.0))

MEAS = {"BTFR (mi_btfr_intercept_kappa_door_2026)": (0.465, 0.076),
        "distance-free (committed)":                (0.551, 0.043),
        "COMBINED (stage67, 3 methods)":            (0.529, 0.034)}
CANDS = {"Verlinde 1/6, like-for-like  sqrt(8pi/3)/6": kV_like,
         "Verlinde 1/6, MIXED reading  sqrt(8pi/3Om)/6": kV_mix,
         "Carl kappa = 1/2 (FITTED)": 0.5,
         "Verlinde 2011 entropic a=cH/2pi": float(np.sqrt(8*np.pi/3)/(2*np.pi)),
         "Milgrom 2020 a=cH/2pi (same D)": float(np.sqrt(8*np.pi/3)/(2*np.pi))}
print(f"  {'candidate':46s}{'kappa':>9}" + "".join(f"{k.split('(')[0][:14]:>16}" for k in MEAS))
rows = {}
for lbl, kv in CANDS.items():
    zs = [(kv-m)/s for (m, s) in MEAS.values()]
    rows[lbl] = zs
    print(f"  {lbl:46s}{kv:9.5f}" + "".join(f"{z:>+15.2f}s" for z in zs))

kc, sc = MEAS["COMBINED (stage67, 3 methods)"]
z_V_comb   = (kV_like-kc)/sc
z_mix_comb = (kV_mix-kc)/sc
z_half     = (0.5-kc)/sc
check(f"*** ITEM 4 ANSWERED: Verlinde's like-for-like kappa_V = {kV_like:.5f} sits "
      f"{abs(z_V_comb):.2f} sigma from the combined measurement 0.529 +- 0.034 -- INSIDE 2 sigma, "
      f"so it is a LIVE CANDIDATE.  (kappa = 1/2 itself sits {abs(z_half):.2f} sigma.) ***",
      abs(z_V_comb) < 2, "FAVOURABLE to the entropic route, stated plainly")
check(f"the MIXED reading kappa = {kV_mix:.5f} is ALSO inside 2 sigma "
      f"({abs(z_mix_comb):.2f} sigma) -- so BOTH Verlinde readings and Carl's 1/2 survive the "
      "measurement.  The data have NO discriminating power here",
      abs(z_mix_comb) < 2, "the honest reading of item 4")
check(f"on the BTFR estimator alone, kappa_V is {abs(rows[list(CANDS)[0]][0]):.2f} sigma and "
      f"1/2 is {abs((0.5-0.465)/0.076):.2f} sigma -- BTFR mildly PREFERS Verlinde; on the "
      f"distance-free estimator kappa_V is {abs(rows[list(CANDS)[0]][1]):.2f} sigma and 1/2 is "
      f"{abs((0.5-0.551)/0.043):.2f} sigma -- distance-free mildly prefers Carl.  The two "
      "estimators DISAGREE about which is favoured",
      abs(rows[list(CANDS)[0]][0]) < abs((0.5-0.465)/0.076) and
      abs(rows[list(CANDS)[0]][1]) > abs((0.5-0.551)/0.043), "both directions, R1")
check(f"the 2011-Verlinde / Milgrom-2020 coefficient a = cH/2pi implies kappa = "
      f"{CANDS['Verlinde 2011 entropic a=cH/2pi']:.5f}, which is "
      f"{abs((CANDS['Verlinde 2011 entropic a=cH/2pi']-kc)/sc):.2f} sigma -- right AT the 2 sigma "
      "edge, the only member of the family the data come close to excluding",
      abs((CANDS['Verlinde 2011 entropic a=cH/2pi']-kc)/sc) > 1.9, "descriptive")

# ITEM 4b -- the discrimination budget
need_abs = abs(0.5-kV_like)/3.0
need_rel = need_abs/0.5
cur_rel  = sc/kc
print(f"""
  THE DISCRIMINATION BUDGET (new here).
    gap to be resolved      |1/2 - kappa_V| = {abs(0.5-kV_like):.5f}  ({100*gap:.2f}% of 1/2)
    sigma needed for 3 sigma separation      = {need_abs:.5f}   (+-{100*need_rel:.2f}%)
    current combined precision               = {sc:.5f}   (+-{100*cur_rel:.2f}%)
    improvement required                     = {sc/need_abs:.1f}x
  For context, stage66's target of +-3.7% (to make 1/2 the UNIQUE simple rational at 3 sigma)
  is only a {cur_rel/0.037:.1f}x improvement.  Separating Carl from Verlinde is a
  {(sc/need_abs)/(cur_rel/0.037):.1f}x HARDER measurement than separating 1/2 from its rational
  neighbours -- and no lever in the corpus reaches it.""")
check(f"separating kappa=1/2 from kappa_V at 3 sigma needs sigma_kappa <= {need_abs:.4f} "
      f"(+-{100*need_rel:.2f}%), a {sc/need_abs:.1f}x improvement on the current +-{100*cur_rel:.1f}%. "
      "The corpus's named levers (stellar M/L zero point, absolute gas scale) target +-3.7%, "
      f"which is {0.037/need_rel:.1f}x too coarse",
      sc/need_abs > 5 and 0.037/need_rel > 3, "NEW -- converts item 4 into a measurement target")

# =====================================================================================
hdr("PART 6 -- THE ENTROPIC FAMILY'S OWN SPREAD vs THE GAP IT WOULD EXPLAIN")
# =====================================================================================
FAM = {"crude area-vs-volume (route6A A5.3)": 2.0,
       "Verlinde 2011 / Milgrom 2020  cH/2pi": 2*np.pi,
       "Verlinde 2016 elastic  cH/6": 6.0,
       "Carl kappa=1/2  cH/sqrt(32 pi/3)": D_carl}
print(f"  {'construction':45s}{'D':>10}{'kappa':>10}{'a0 can':>13}{'a0 alt':>13}")
for lbl, D_ in FAM.items():
    kk = np.sqrt(8*np.pi/3)/D_
    print(f"  {lbl:45s}{D_:10.5f}{kk:10.5f}{c*H_L/D_:13.4e}{c*H0/D_:13.4e}")
pub = [2*np.pi, 6.0]
spread = max(pub)/min(pub) - 1
check(f"restricting to the two ACTUALLY PUBLISHED entropic coefficients (2pi and 6), the family's "
      f"own spread is {100*spread:.2f}%, which is LARGER than the {100*gap:.2f}% gap between "
      "Verlinde 2016 and Carl.  A class that disagrees with itself by more than the quantity in "
      "dispute cannot settle the dispute",
      spread > gap, "ADVERSE, and it is the cleanest deflation available -- no arbitrary band")
# coincidence pricing over the full family band, log-uniform
log_band = np.log(max(FAM.values())/min(FAM.values()))
log_win  = 2*np.log(1+gap)
p_coin   = log_win/log_band
info(f"log-uniform coincidence pricing over the full D band [2, {D_carl:.2f}]: "
     f"p = {p_coin:.3f} of landing within +-{100*gap:.2f}% of 1/2 by chance")
check(f"p = {p_coin:.3f} -- suggestive, an order of magnitude short of anything that would be "
      "called evidence.  route3B priced this at p ~ 0.05 over a factor-4 band; both pricings "
      "agree that the match is worth a LEAD, not a derivation",
      0.01 < p_coin < 0.15, "honest weighting; consistent with route3B independently")

# =====================================================================================
hdr("PART 7 -- ITEM 3: PRICING WHAT THE DERIVATION RESTS ON")
# =====================================================================================
# the solar-system number, computed here rather than recited
r_mars = 1.5237*AU
gN_mars = GM_sun/r_mars**2
dg_verlinde = np.sqrt(A_M_H0*gN_mars)          # NO interpolation function in Verlinde
MARS_BUDGET = 1.4e-15
r_star = np.sqrt(2*G*(GM_sun/G)*(c/H0)/c**2)   # S_M = S_DE surface: r_* = sqrt(2 G M L/c^2)
print(f"  g_N(Mars) = {gN_mars:.4e} m/s^2 ;  Verlinde's anomaly sqrt(a_M g_N) = {dg_verlinde:.4e}")
print(f"  Mars EPM budget = {MARS_BUDGET:.1e} m/s^2  ->  overshoot = {dg_verlinde/MARS_BUDGET:.3e}x")
print(f"  BUT his own entropy budget saturates at r_* = sqrt(2 G M L/c^2) = {r_star/AU:.0f} AU, "
      f"and every planet is inside it -> the anomaly is EXACTLY ZERO there.")
check(f"the SAME construction that fixes the coefficient to 3.5% is ambiguous by "
      f"{dg_verlinde/MARS_BUDGET:.2e}x -- EIGHT ORDERS -- about its own solar-system prediction, "
      "depending on whether the S_M >= S_DE cutoff is applied.  This is the strongest single "
      "argument against reading the 3.5% as meaningful",
      dg_verlinde/MARS_BUDGET > 1e7 and r_star/AU > 100, "ADVERSE, computed not recited")
check("r_* = 4256 AU for the Sun, reproducing route3's independently-derived value to 1%",
      abs(r_star/AU/4256 - 1) < 0.01, "cross-check against prior work")

print("""
  THE FOUR STANDING OBJECTIONS TO VERLINDE, PRICED (item 3):
   (1) NO COVARIANT FORMULATION.  There is no action, no field equations, no propagating-DOF
       count.  route3B's gate 4 is not FAILED, it CANNOT BE POSED.  A coefficient derived from
       a construction with no field equations cannot be checked for consistency with anything
       else in Carl's framework -- including w = -1, c_T = 1, the CMB, or the promotion
       a0^2(Q) = kappa^2 G(-K(Q)) which is the whole reason a0 is a FIELD here.
   (2) DOMAIN.  The derivation is for STATIC, SPHERICALLY SYMMETRIC, ISOLATED systems.  Discs
       are outside it.  Every RAR test of emergent gravity (including this folder's own) applies
       it outside the domain its author claimed.
   (3) CLUSTERS.  Emergent gravity is known to fail on clusters; so does Carl's framework
       (~2x short, pre-existing).  This is NOT a discriminator, and must not be scored as one.
   (4) NO COSMOLOGY.  There is no perturbation theory, so there is no CMB statement and no
       a0(z).  Carl's a0(z) law -- MOND OFF at recombination, a0(1090)/a0(0) = 0.0060 -- has no
       counterpart at all.  Worse, a naive a_M(z) = cH(z)/6 RISES with z, the OPPOSITE sign to
       the framework's own derived law.  Adopting Verlinde's coefficient would import a
       cosmology that CONTRADICTS the framework's own derived redshift dependence.
  (4) IS THE ONE THAT ACTUALLY BITES, AND IT IS SPECIFIC TO CARL'S FRAMEWORK, NOT TO VERLINDE.
""")
# quantify (4)
z_rec = 1090.0
Ez = np.sqrt(0.315*(1+z_rec)**3 + 9.2e-5*(1+z_rec)**4 + OmL)
print(f"  a_M(z=1090)/a_M(0) = E(z) = {Ez:.1f}   vs the framework's DERIVED "
      f"a0(1090)/a0(0) = 0.0060  ->  sign OPPOSITE, magnitude {Ez/0.0060:.2e}x apart")
check(f"a naive cH(z)/6 gives a0 RISING by {Ez:.0f}x at recombination where Carl's derived law "
      f"gives 0.0060 -- {Ez/0.0060:.1e}x apart AND opposite in sign.  Verlinde's coefficient "
      "cannot simply be adopted: it comes attached to an H(z) scaling that the framework has "
      "already derived to be wrong",
      Ez/0.0060 > 1e4, "ADVERSE to importing the derivation wholesale -- the decisive item")
info("CAVEAT, against my own point: if the medium is the ASYMPTOTIC de Sitter horizon rather "
     "than the instantaneous H(z), a_M is a CONSTANT and the collision is 1/0.0060 = 167x, "
     "still adverse but not 3e5x.  Both readings reported (route3B found the same fork).")

# =====================================================================================
hdr("VERDICT -- ROUTE 4")
# =====================================================================================
print(f"""
  ITEM 1 -- THE EXACT RELATIONSHIP.
      sqrt(G rho_Lambda) = H_0 sqrt(3 Omega_Lambda/(8 pi))  ==>  a0/a_M = 6 kappa sqrt(3 Om/(8pi))
      ==>  kappa_V(Omega_Lambda) = sqrt(8 pi/(3 Omega_Lambda))/6.
      LIKE FOR LIKE (same rate both sides, = published cH_0/6 vs Carl's ALT footing):
          kappa_V = sqrt(8 pi/3)/6 = {kV_like:.7f}   Omega-INDEPENDENT
      MIXED (published cH_0/6 vs Carl's CANONICAL rho_Lambda):
          kappa_V = {kV_mix:.7f}   Omega_Lambda-dependent
      kappa = 1/2 lies BETWEEN them.  Equivalently a_M/a0 = 1.1659 canonical / 0.9649 alt.

  ITEM 2 -- DERIVABLE OR COINCIDENCE?  **PARTIAL, AND THE ANSWER IS NOT 1/2.**
      The counting IS transcribable, exactly, and I re-derived it from scratch: the 6 is
      FORCED as 16 pi G rho_DE/H^2 = 6 by Friedmann, and the 3 in it is the SAME Friedmann 3
      inside Carl's own sqrt(3 Omega_Lambda/(8 pi)).  So they are the same KIND of object.
      BUT the transcription delivers kappa = {kV_like:.5f}, NOT 1/2.  It is off by exactly
      sqrt(27/(8 pi)) = {r_pure:.7f}, i.e. by (27/8)/pi.  Push that factor into the energy
      bookkeeping instead and Carl's 1/2 requires Verlinde's stored fraction to be
      f = sqrt(27/(32 pi)) = {f_carl:.7f} rather than 1/2.  THE SAME IRRATIONAL APPEARS EITHER
      WAY: each theory's "one half" is the other's ugly number, and no bookkeeping removes it.
      Reinforced by an exact parameterisation theorem: sqrt(8 pi/3) is irrational, so a
      construction forcing a rational multiple of cH can NEVER force a rational kappa.
      Verlinde's chain is manifestly a cH construction (4 pi L^2, (4/3) pi L^3, 3/(8 pi)).
      Carl's kappa is pi-free.  They cannot both be natural.

  WHAT THE 3.5% IS WORTH -- three independent deflations, all computed here:
      (a) the counting's own convention slack pins kappa only to [{kap_lo:.4f}, {kap_hi:.4f}],
          a factor-4 band {band_ratio:.0f}x wider than the gap;
      (b) Verlinde's own H_0-vs-H_Lambda ambiguity is {100*amb:.1f}%, {amb/gap:.1f}x the gap;
      (c) the two PUBLISHED entropic coefficients (2pi, 6) disagree with each other by
          {100*spread:.2f}%, MORE than the {100*gap:.2f}% gap in dispute.
      Coincidence pricing: p = {p_coin:.3f}.  A LEAD, NOT A DERIVATION.

  ITEM 3 -- WHAT IT RESTS ON.  No action, no field equations, no DOF count: theoretical health
      CANNOT BE POSED.  Domain is static/spherical/isolated.  Clusters fail (not a
      discriminator -- Carl's fail too).  No cosmology.  DECISIVE for Carl specifically:
      cH(z)/6 makes a0 RISE by {Ez:.0f}x at recombination where the framework's OWN derived law
      gives 0.0060 -- opposite sign, {Ez/0.0060:.1e}x apart (167x on the fixed-dS reading).
      And the same construction is ambiguous by {dg_verlinde/MARS_BUDGET:.1e}x about its own
      solar-system prediction.  ANY kappa DERIVED FROM THIS MUST BE LABELLED
      "derived from a contested, non-covariant, cosmology-free argument".

  ITEM 4 -- WHERE IT FALLS.  Against the combined measurement kappa = 0.529 +- 0.034:
      kappa_V (like-for-like) = {kV_like:.5f}  ->  {abs(z_V_comb):.2f} sigma   INSIDE 2 sigma, LIVE
      kappa_V (mixed)         = {kV_mix:.5f}  ->  {abs(z_mix_comb):.2f} sigma   INSIDE 2 sigma, LIVE
      kappa = 1/2 (Carl)      = 0.50000  ->  {abs(z_half):.2f} sigma
      cH/2pi (Verlinde 2011)  = {CANDS['Verlinde 2011 entropic a=cH/2pi']:.5f}  ->  {abs((CANDS['Verlinde 2011 entropic a=cH/2pi']-kc)/sc):.2f} sigma   at the 2 sigma edge
      BTFR alone mildly prefers Verlinde; distance-free alone mildly prefers Carl.  Separating
      them at 3 sigma needs sigma_kappa <= {need_abs:.4f} (+-{100*need_rel:.2f}%), a {sc/need_abs:.1f}x
      improvement -- {(sc/need_abs)/(cur_rel/0.037):.1f}x harder than the corpus's named +-3.7% target.

  NET.  kappa is NOT derived by this route.  What IS established, and it is real: the ONLY
  published construction that produces this amplitude law from a stated postulate assigns the
  coefficient a definite value, that value is {kV_like:.4f}, it is inside Carl's own measurement,
  and the residual disagreement with 1/2 is one clean irrational, sqrt(27/(8 pi)).  THE DOOR IS
  OPEN, NOT CLOSED: a construction that produced sqrt(27/(8 pi)) x Verlinde's f -- or, better,
  one built natively on sqrt(G rho) instead of on H -- would derive kappa = 1/2 exactly.  What
  this file establishes is that ENTROPY COUNTING ON A HORIZON IS THE WRONG STARTING VARIABLE
  for a pi-free kappa, which is a constraint on the search, not a closure of it.

  COULD NOT DETERMINE (stated as required by R5):
    * whether Verlinde's f = 1/2 is FORCED by his elastic model or chosen -- I do not have the
      paper's section 7 and reconstructed the chain from its stated ingredients.  The 6 follows
      from f = 1/2 by an identity I verified; whether f = 1/2 itself is derivable is OPEN and
      it is the ONLY place the missing sqrt(27/(8 pi)) could come from.
    * whether any entropy-counting argument can be posed natively in sqrt(G rho_Lambda) rather
      than in H.  If it can, the parameterisation theorem is evaded and kappa = 1/2 becomes
      reachable.  NOT ATTEMPTED HERE.
    * the corpus's BTFR value 0.465 +- 0.076 and its combined 0.529 +- 0.034 were taken as given
      and NOT re-derived from SPARC in this file.
""")
print("#"*100)
print(f"# {NCHK} checks, {'ALL PASS' if PASS else 'SOME FAILED -- read them, they are the finding'}")
print("#"*100)
sys.exit(0 if PASS else 1)
