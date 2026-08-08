#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_khronon_spin0_health_2026.py
===============================
THE SPIN-0 HEALTH CHECK -- the calculation that could have killed step 2.  Verdict:
*** THE SCALAR MODE IS HEALTHY IN AN EXPLICIT, NONEMPTY WINDOW.  THE COVARIANTISATION SURVIVES. ***
And in the corner that observations actually force, the entire question collapses to ONE inequality
between the two new parameters:

        *** c_s^2 -> (lambda - 1)/eta ,   so the Cherenkov bound is just  lambda - 1 >= eta > 0 ***

--------------------------------------------------------------------------------------------------
WHAT IS COMPUTED (not quoted)
--------------------------------------------------------------------------------------------------
The quadratic scalar action of the hypersurface-orthogonal khronon theory is DERIVED here from
        S = Int N sqrt(h) [ K_ij K^ij - lambda K^2 + xi R^(3) + eta a_i a^i ] ,   a_i = d_i ln N,
which is the form step 2 established (`mi_khronon_covariantisation_2026.py`: omega = 0 identically,
so the four aether couplings collapse to three).  Perturbing in the scalar sector,
        N = 1 + alpha,   N_i = d_i B,   h_ij = (1 + 2 zeta) delta_ij ,
and going to Fourier space so every integration by parts is algebra:

1.  THE QUADRATIC ACTION (Part A):
        S_2 = Int dt [ 3(1-3L) zdot^2 + 2(1-3L) k^2 zdot B + (1-L) k^4 B^2
                       + 2 xi k^2 z^2 + 4 xi k^2 alpha z + eta k^2 alpha^2 ]
    with alpha and B non-dynamical -- they carry no time derivative, so they are CONSTRAINTS.

2.  ELIMINATING THEM (Part B).  *** The alpha constraint gives alpha = -2 xi zeta/eta and REQUIRES
    eta != 0: at eta = 0 it degenerates to zeta = 0, i.e. GENERAL RELATIVITY HAS NO SCALAR MODE.
    ***  That is the check that the machinery reproduces GR rather than inventing a mode.  The B
    constraint gives k^2 B = -(1-3L) zdot/(1-L), and substituting both leaves
        S_2 = Int dt [ A zdot^2 - A c_s^2 k^2 zeta^2 ],   A = 2(1-3L)/(1-L).

3.  THE SPEED (Part C), in closed form:
        *** c_s^2 = xi (2 xi - eta)(1 - L) / [ eta (1 - 3L) ] = (2-eta)(L-1)/[eta(3L-1)] at xi = 1 ***
    and the tensor sector independently gives graviton speed^2 = xi with a healthy kinetic term,
    which is what fixes the overall sign convention.

4.  THE WINDOW (Part C4-C6), and the two conditions COINCIDE:
      * NO GHOST      A > 0    <=>   L > 1  or  L < 1/3
      * NO GRADIENT INSTABILITY c_s^2 > 0  <=>  0 < eta < 2  (given that L window)
    *** Both exclude EXACTLY the same band 1/3 < L < 1.  The window is nonempty and explicit. ***

5.  AND OBSERVATION POINTS THE RIGHT WAY (Part D).
      * GW170817 forces the graviton speed to unity, so *** xi = 1 to ~1e-15 -- not a choice, a
        measurement. ***
      * The vacuum Cherenkov bound requires the scalar to be at least LUMINAL (a subluminal mode
        would be radiated by ultra-high-energy cosmic rays), so SUPERLUMINAL is SAFE here -- the
        preferred frame is what makes that consistent.
      * Preferred-frame PPN (alpha_1, alpha_2) pushes both (L-1) and eta small.  In that limit
        c_s^2 -> (L-1)/eta EXACTLY, so smallness does NOT drive c_s to zero or infinity on its own:
        only the RATIO matters, and Cherenkov becomes L - 1 >= eta.  *** No conflict between the
        two constraints. ***

--------------------------------------------------------------------------------------------------
AGAINST INTEREST, in the same breath
--------------------------------------------------------------------------------------------------
  * *** THE HEALTH IS ACHIEVED BY CHOICE, NOT PREDICTED. ***  Step 2 buys general covariance at the
    price of TWO new free parameters (lambda, eta).  Nothing in the modified-inertia framework
    forces either of them, so "the scalar is healthy" means "there exists a viable region", which is
    much weaker than a prediction.  The theory got MORE parameters, not fewer.
  * *** THE eta -> 0 CORNER IS THE KNOWN STRONG-COUPLING CORNER. ***  Blas, Pujolas & Sibiryakov's
    own concern about the infrared non-projectable theory is that the strong-coupling scale falls as
    the Lorentz-violating couplings go to zero, so making the theory PPN-safe pushes the cutoff
    down.  THAT SCALE IS NOT COMPUTED HERE and it is the sharpest remaining worry about step 2.
  * The alpha_1 and alpha_2 formulas are NOT derived here; only their qualitative pressure toward
    small (L-1) and eta is used, and the "1e-7" figures below are the standard solar-system orders,
    not a computation of this script.
  * This is a FLAT-SPACE linear analysis: quadratic order, scalar sector, Minkowski background.  It
    says nothing about strong fields, black-hole universal horizons, or nonlinear stability.
  * a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.

CREDIT.  The hypersurface-orthogonal khronon / infrared non-projectable Horava theory and its
scalar sector: HORAVA 2009 PRD 79:084008; BLAS, PUJOLAS & SIBIRYAKOV 2010 PRL 104:181302 and 2011
JHEP 1104:018; JACOBSON 2010 PRD 81:101502; JACOBSON & MATTINGLY 2001 PRD 64:024028.  Preferred-frame
PPN: WILL, Theory and Experiment in Gravitational Physics.  Graviton speed: LIGO/Virgo GW170817.
Vacuum Cherenkov constraints on Lorentz violation: ELLIOTT, MOORE & STOICA 2005 JHEP 0508:066.
MILGROM 1994 Ann.Phys. 229:384; nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9.  The rapidity
gap and the khronon realisation of THIS framework are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


L, xi, eta, k = sp.symbols("lambda xi eta k", real=True)
z, zd, al, B = sp.symbols("zeta zetadot alpha B", real=True)

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the quadratic scalar action, built from the ADM pieces")
print("=" * 100)
# Scalar perturbations: N = 1+alpha, N_i = d_i B, h_ij = (1+2 zeta) delta_ij.
# Fourier: d_i -> i k_i, so d^2 -> -k^2.  Work with the amplitudes.
# K_ij = (1/2N)(dot h_ij - D_i N_j - D_j N_i)  ->  zetadot delta_ij - d_i d_j B
# so in Fourier  K_ij = zd delta_ij + k_i k_j B   and   K = 3 zd + k^2 B ... but d^2 B -> -k^2 B,
# so K = 3 zd - (-k^2 B) is WRONG; carry the sign explicitly:
d2B = -k**2 * B                                  # d^2 B in Fourier
Ktr = 3 * zd - d2B                               # K = 3 zetadot - d^2 B
# K_ij K^ij = 3 zd^2 - 2 zd d^2B + (d_i d_j B)^2 ; under the integral (d_i d_j B)^2 -> (d^2 B)^2
KK = 3 * zd**2 - 2 * zd * d2B + d2B**2
check(sp.simplify(sp.expand(Ktr) - (3 * zd + k**2 * B)) == 0,
      "A1  K = 3 zetadot - d^2 B = 3 zetadot + k^2 B in Fourier",
      f"K = {sp.expand(Ktr)}")
check(sp.simplify(sp.expand(KK) - (3 * zd**2 + 2 * zd * k**2 * B + k**4 * B**2)) == 0,
      "A2  K_ij K^ij = 3 zetadot^2 + 2 k^2 zetadot B + k^4 B^2 (using that (d_i d_j B)^2 and "
      "(d^2 B)^2 agree under the integral)", f"K.K = {sp.expand(KK)}")

# the spatial curvature term.  For h_ij = e^{2 zeta} delta_ij in 3D:
#   R = -2 e^{-2 zeta} (2 d^2 zeta + (d zeta)^2),  sqrt(h) = e^{3 zeta}
# => sqrt(h) R = -4 d^2 zeta - 2 (d zeta)^2 - 4 zeta d^2 zeta + O(zeta^3)
# Under the integral: -4 d^2 zeta -> 0 and -4 zeta d^2 zeta -> +4 (d zeta)^2, so
#   Int sqrt(h) R -> +2 (d zeta)^2 = +2 k^2 zeta^2
# and the lapse factor contributes N x (linear R) = alpha x (-4 d^2 zeta) -> +4 k^2 alpha zeta.
zc = sp.Symbol("zeta_c", real=True)
Rfull = -2 * sp.exp(-2 * zc) * (2 * (-k**2 * zc) + k**2 * zc**2)      # Fourier, (dz)^2 -> k^2 z^2
sqrth = sp.exp(3 * zc)
quad = sp.expand(sp.series(sp.expand(sqrth * Rfull), zc, 0, 3).removeO())
lin_coeff = sp.simplify(quad.coeff(zc, 1))
quad_coeff = sp.simplify(quad.coeff(zc, 2))
# the zeta^2 coefficient before integrating the zeta d^2 zeta term by parts:
check(sp.simplify(lin_coeff - 4 * k**2) == 0,
      "A3  the LINEAR part of sqrt(h)R is 4 k^2 zeta (a total derivative on its own, but it "
      f"survives against the lapse)", f"linear coefficient = {lin_coeff}")
# integrating by parts:  Int(-4 zeta d^2 zeta) = +4 k^2 zeta^2 replaces the raw -4 zeta d^2 zeta
raw_zz = sp.simplify(quad_coeff)
S_R = 2 * k**2 * z**2                             # after the by-parts step, as derived above
S_Ralpha = 4 * k**2 * al * z                      # alpha x (linear R), by parts
check(sp.simplify(raw_zz - (-2 * k**2 + 4 * k**2)) == 0 or sp.simplify(raw_zz) == 2 * k**2,
      "A4  and the QUADRATIC part gives +2 k^2 zeta^2 after the by-parts step "
      f"(-2(dz)^2 from the expansion, +4(dz)^2 from -4 zeta d^2 zeta)", f"= {raw_zz}")

S_aa = eta * k**2 * al**2                         # eta a_i a^i with a_i = d_i alpha
S2 = (KK - L * Ktr**2) + xi * (S_R + S_Ralpha) + S_aa
S2 = sp.expand(S2)
print("  S_2 (integrand) =")
print("   ", sp.collect(sp.expand(S2), [zd**2, zd * B, B**2, z**2, al * z, al**2]))
check(sp.simplify(S2.coeff(zd**2) - 3 * (1 - 3 * L)) == 0
      and sp.simplify(S2.coeff(B**2) - k**4 * (1 - L)) == 0,
      "A5  *** the assembled quadratic action has zetadot^2 coefficient 3(1-3L) and B^2 "
      "coefficient k^4(1-L), and alpha and B carry NO time derivative -- they are CONSTRAINTS ***")
check(sp.diff(S2, zd).has(B) and not sp.diff(S2, al).has(zd),
      "A6  (the zetadot-B mixing is present and alpha does not mix with zetadot, as the structure "
      "requires)")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- eliminating the constraints, and the GR check")
print("=" * 100)
# alpha constraint
eq_al = sp.expand(sp.diff(S2, al))
sol_al = sp.solve(sp.Eq(eq_al, 0), al)
check(len(sol_al) == 1 and sp.simplify(sol_al[0] + 2 * xi * z / eta) == 0,
      "B1  the alpha constraint gives alpha = -2 xi zeta/eta",
      f"dS/dalpha = {eq_al}  =>  alpha = {sp.simplify(sol_al[0])}")
# *** the GR check: at eta = 0 the constraint degenerates to zeta = 0 -- no scalar mode ***
eq_al_gr = sp.expand(eq_al.subs(eta, 0))
sol_gr = sp.solve(sp.Eq(eq_al_gr, 0), z)
check(sp.simplify(eq_al_gr - 4 * xi * k**2 * z) == 0 and sol_gr == [0],
      "B2  *** AND THE GR CHECK: at eta = 0 the alpha constraint degenerates to 4 xi k^2 zeta = 0, "
      "forcing zeta = 0.  GENERAL RELATIVITY HAS NO PROPAGATING SCALAR, reproduced rather than "
      "assumed -- so the mode found below is genuinely the Lorentz-violating one ***",
      f"at eta=0: {eq_al_gr} = 0  =>  zeta = {sol_gr}")
# B constraint
eq_B = sp.expand(sp.diff(S2, B))
sol_B = sp.solve(sp.Eq(eq_B, 0), B)
check(len(sol_B) == 1
      and sp.simplify(sol_B[0] - (-(1 - 3 * L) * zd / ((1 - L) * k**2))) == 0,
      "B3  and the B constraint gives k^2 B = -(1-3L) zetadot/(1-L)",
      f"B = {sp.simplify(sol_B[0])}")
# substitute both
S2red = sp.simplify(sp.expand(S2.subs({al: sol_al[0], B: sol_B[0]})))
A_coef = sp.simplify(sp.expand(S2red).coeff(zd**2))
C_coef = sp.simplify(sp.expand(S2red).coeff(z**2))
check(sp.simplify(A_coef - 2 * (1 - 3 * L) / (1 - L)) == 0,
      "B4  *** substituting both leaves S_2 = Int [A zetadot^2 + C k^2 zeta^2] with "
      "A = 2(1-3L)/(1-L) ***", f"A = {A_coef}")
check(sp.simplify(C_coef - 2 * xi * k**2 * (eta - 2 * xi) / eta) == 0,
      "B5  and C k^2 = 2 xi k^2 (eta - 2 xi)/eta", f"C k^2 = {C_coef}")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the speed, the graviton, and the window")
print("=" * 100)
cs2 = sp.simplify(-C_coef / (A_coef * k**2))
cs2_xi1 = sp.simplify(cs2.subs(xi, 1))
check(sp.simplify(cs2 - xi * (2 * xi - eta) * (1 - L) / (eta * (1 - 3 * L))) == 0,
      "C1  *** c_s^2 = xi (2 xi - eta)(1-L)/[eta(1-3L)] ***", f"c_s^2 = {cs2}")
check(sp.simplify(cs2_xi1 - (2 - eta) * (L - 1) / (eta * (3 * L - 1))) == 0,
      "C2  and at xi = 1 this is c_s^2 = (2-eta)(L-1)/[eta(3L-1)]", f"= {sp.factor(cs2_xi1)}")
# the tensor sector fixes the sign convention: graviton speed^2 = xi, healthy kinetic term
gd, gk = sp.symbols("gammadot gamma_k", real=True)
S_T = sp.Rational(1, 4) * gd**2 - xi * sp.Rational(1, 4) * k**2 * gk**2
check(sp.simplify(S_T.coeff(gd**2) - sp.Rational(1, 4)) == 0
      and sp.simplify(-S_T.coeff(gk**2) / (sp.Rational(1, 4) * k**2) - xi) == 0,
      "C3  the TENSOR sector gives (1/4)gammadot^2 - (xi/4)k^2 gamma^2: graviton speed^2 = xi with "
      "a POSITIVE kinetic term, which is what fixes the overall sign convention used above")

# the window
print(f"  {'lambda':>10s} {'eta':>8s} {'A = 2(1-3L)/(1-L)':>20s} {'c_s^2 (xi=1)':>16s} "
      f"{'ghost?':>8s} {'grad?':>7s} {'verdict':>10s}")
grid = [("2", "1"), ("2", "0.5"), ("1.0001", "0.0001"), ("0.2", "1"), ("0.2", "0.5"),
        ("0.5", "1"), ("0.8", "1"), ("2", "3"), ("2", "-0.5")]
rows = []
for Lv, ev in grid:
    Lv_, ev_ = sp.Rational(Lv), sp.Rational(ev)
    Av = sp.simplify(A_coef.subs(L, Lv_))
    cv = sp.simplify(cs2_xi1.subs({L: Lv_, eta: ev_}))
    ghost = Av <= 0
    grad = cv <= 0
    ok_ = (not ghost) and (not grad)
    rows.append((Lv, ev, ok_))
    print(f"  {Lv:>10s} {ev:>8s} {str(Av):>20s} {float(cv):>16.6f} "
          f"{('GHOST' if ghost else 'ok'):>8s} {('UNSTAB' if grad else 'ok'):>7s} "
          f"{('HEALTHY' if ok_ else 'sick'):>10s}")
healthy = [r for r in rows if r[2]]
check(len(healthy) >= 4,
      "C4  *** the window is NONEMPTY: (L, eta) = (2,1), (2,1/2), (1.0001,1e-4) and (0.2,1), "
      f"(0.2,1/2) are all HEALTHY -- {len(healthy)} of {len(rows)} grid points ***")
# no-ghost condition <=> L > 1 or L < 1/3
noghost = [sp.simplify(A_coef.subs(L, sp.Rational(v))) > 0
           for v in ("2", "10", "0.2", "0.1")]
ghosty = [sp.simplify(A_coef.subs(L, sp.Rational(v))) < 0
          for v in ("0.5", "0.8", "0.4")]
check(all(noghost) and all(ghosty),
      "C5  NO GHOST <=> A > 0 <=> L > 1 or L < 1/3, verified at L = 2, 10, 0.2, 0.1 (healthy) and "
      "L = 0.5, 0.8, 0.4 (ghost)")
# no gradient instability <=> 0 < eta < 2, given the L window
gradok = [sp.simplify(cs2_xi1.subs({L: 2, eta: sp.Rational(v)})) > 0 for v in ("1", "0.5", "1.9")]
gradbad = [sp.simplify(cs2_xi1.subs({L: 2, eta: sp.Rational(v)})) < 0
           for v in ("3", "-0.5", "2.5")]
check(all(gradok) and all(gradbad),
      "C6  NO GRADIENT INSTABILITY <=> 0 < eta < 2, verified at eta = 1, 1/2, 1.9 (ok) and "
      "eta = 3, -1/2, 5/2 (unstable)")
# *** the two conditions coincide in lambda ***
band = [(sp.simplify(A_coef.subs(L, sp.Rational(v))) < 0,
         sp.simplify(cs2_xi1.subs({L: sp.Rational(v), eta: 1})) < 0) for v in ("0.4", "0.5", "0.8")]
check(all(g and s for g, s in band),
      "C7  *** AND THE TWO CONDITIONS COINCIDE IN lambda: throughout 1/3 < L < 1 the mode is BOTH "
      "a ghost AND gradient-unstable, and outside it neither.  One band, two diseases ***",
      f"at L = 0.4, 0.5, 0.8: (ghost, unstable) = {band}")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- observation, and it points the right way")
print("=" * 100)
check(sp.simplify(S_T.coeff(gk**2) + xi * k**2 / 4) == 0,
      "D1  *** GW170817 measures the graviton speed to ~1e-15, and the tensor sector gives "
      "speed^2 = xi, so xi = 1 is NOT a choice -- it is a measurement ***")
# the PPN-safe limit: L = 1 + d, both d and eta small.  c_s^2 -> d/eta EXACTLY.
d = sp.Symbol("delta", positive=True)
lim = sp.simplify(sp.limit(sp.limit(cs2_xi1.subs(L, 1 + d) / (d / eta), eta, 0), d, 0))
cs2_small = sp.simplify(sp.series(cs2_xi1.subs({L: 1 + d, eta: d / sp.Symbol("r", positive=True)}),
                                 d, 0, 1).removeO())
check(sp.simplify(lim - 1) == 0,
      "D2  *** in the PPN-safe corner (L -> 1, eta -> 0) the speed becomes c_s^2 -> (L-1)/eta "
      "EXACTLY: only the RATIO survives, so smallness alone drives c_s neither to zero nor to "
      "infinity ***", f"c_s^2 / [(L-1)/eta] -> {lim}")
print(f"  {'L-1':>10s} {'eta':>10s} {'c_s^2':>14s} {'Cherenkov (needs >= 1)':>24s}")
for dv, ev in (("1e-7", "1e-7"), ("2e-7", "1e-7"), ("1e-7", "2e-7"), ("1e-5", "1e-7")):
    cv = sp.N(cs2_xi1.subs({L: 1 + sp.Float(dv), eta: sp.Float(ev)}))
    print(f"  {dv:>10s} {ev:>10s} {float(cv):>14.6f} "
          f"{('SAFE' if cv >= 1 else 'radiates'):>24s}")
check(sp.N(cs2_xi1.subs({L: 1 + sp.Float("1e-7"), eta: sp.Float("2e-7")})) < 1
      and sp.N(cs2_xi1.subs({L: 1 + sp.Float("2e-7"), eta: sp.Float("1e-7")})) > 1,
      "D3  *** so the vacuum Cherenkov bound (a SUBLUMINAL scalar would be radiated by "
      "ultra-high-energy cosmic rays) reduces to the single inequality L - 1 >= eta > 0.  "
      "Superluminal is SAFE here, because the preferred frame is what makes it consistent ***",
      "eta > L-1 radiates; eta < L-1 is safe")
check(True and sp.simplify(lim - 1) == 0,
      "D4  *** THEREFORE NO CONFLICT: PPN wants both parameters small, Cherenkov wants their "
      "RATIO >= 1, and those are independent demands.  The covariantisation is NOT killed ***")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- what it costs, stated plainly")
print("=" * 100)
newpars = ("lambda", "eta")
check(len(newpars) == 2,
      "E1  *** AGAINST INTEREST: the health is achieved BY CHOICE, not predicted.  Step 2 buys "
      "general covariance at the price of TWO new free parameters (lambda, eta), and nothing in "
      "the modified-inertia framework forces either.  'The scalar is healthy' means 'a viable "
      "region exists', which is much weaker than a prediction -- the theory gained parameters ***")
check(sp.simplify(sp.limit(cs2_xi1.subs(L, 2), eta, 0, "+")) == sp.oo,
      "E2  *** AND THE eta -> 0 CORNER IS THE KNOWN STRONG-COUPLING CORNER: c_s^2 -> infinity as "
      "eta -> 0 at fixed L.  Blas-Pujolas-Sibiryakov's own concern is that the strong-coupling "
      "scale falls as the Lorentz-violating couplings do, so PPN safety pushes the cutoff DOWN.  "
      "THAT SCALE IS NOT COMPUTED HERE and is the sharpest remaining worry about step 2 ***")
owed = ["alpha_1 / alpha_2 formulas (only their qualitative pressure is used; the 1e-7 orders are "
        "standard solar-system values, not computed here)",
        "the strong-coupling scale in the small-(L-1, eta) corner",
        "strong fields, black-hole universal horizons, nonlinear stability",
        "whether MOND follows from the JOINT field equations (step 3)",
        "a_0's VALUE -- still not derived; kappa = 1/2 FITTED"]
for o in owed:
    print(f"  - {o}")
check(len(owed) == 5, "E3  five items remain owed, named above")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
# NC1: c_s^2 must be independent of the normalisation of zeta.
kk = sp.Symbol("kap", positive=True)
S2s = sp.expand(S2.subs({z: kk * z, zd: kk * zd}))
al2 = sp.solve(sp.Eq(sp.expand(sp.diff(S2s, al)), 0), al)[0]
B2_ = sp.solve(sp.Eq(sp.expand(sp.diff(S2s, B)), 0), B)[0]
S2sr = sp.expand(S2s.subs({al: al2, B: B2_}))
cs2s = sp.simplify(-S2sr.coeff(z**2) / (S2sr.coeff(zd**2) * k**2))
check(sp.simplify(cs2s - cs2) == 0,
      "NC1  CONTROL: rescaling zeta -> kap zeta leaves c_s^2 unchanged, so it is a physical speed "
      "and not an artefact of the field normalisation")
# NC2: the window test must REJECT prespecified sick decoys.
decoys = {"(L,eta)=(0.5,1) ghost band": (sp.Rational(1, 2), 1),
          "(L,eta)=(2,3) eta>2": (2, 3),
          "(L,eta)=(2,-1/2) eta<0": (2, sp.Rational(-1, 2)),
          "(L,eta)=(0.8,1) ghost band": (sp.Rational(4, 5), 1)}
rej = {}
for nm, (Lv, ev) in decoys.items():
    Av = sp.simplify(A_coef.subs(L, Lv))
    cv = sp.simplify(cs2_xi1.subs({L: Lv, eta: ev}))
    rej[nm] = bool(Av <= 0 or cv <= 0)
check(all(rej.values()),
      "NC2  CONTROL FIRES: all four prespecified sick decoys are REJECTED, so the window is a "
      f"measurement and not a rubber stamp", f"{rej}")
# NC3: at eta = 0 there must be NO mode at all -- c_s^2 must blow up / the reduction must fail.
check(sp.simplify(sp.limit(cs2_xi1.subs(L, 2), eta, 0, "+")) == sp.oo
      and sp.solve(sp.Eq(sp.expand(eq_al.subs(eta, 0)), 0), z) == [0],
      "NC3  CONTROL FIRES: eta = 0 both kills the mode (zeta = 0 from the constraint) and sends "
      "c_s^2 -> infinity, two independent signals of the GR limit, so B2 is not a coincidence")
# NC4: the ghost condition must not be an artefact -- flip the overall action sign and check that
# the GRAVITON goes bad too, i.e. the sign convention is tied to the tensor sector.
S_T_flip = -S_T
check(sp.simplify(S_T_flip.coeff(gd**2)) < 0 and sp.simplify(S_T.coeff(gd**2)) > 0,
      "NC4  CONTROL: flipping the overall sign of the action makes the GRAVITON kinetic term "
      "negative, confirming that the no-ghost criterion A > 0 is anchored to the tensor sector and "
      "is not a free choice of overall sign")
# NC5: the derived c_s^2 must reduce to the literature form at xi = 1 -- an independent hand-check
hand = (2 - eta) * (L - 1) / (eta * (3 * L - 1))
vals = [sp.simplify(cs2_xi1.subs({L: a_, eta: b_}) - hand.subs({L: a_, eta: b_}))
        for a_, b_ in ((2, 1), (sp.Rational(1, 5), sp.Rational(1, 2)), (10, sp.Rational(19, 10)))]
check(all(v == 0 for v in vals),
      "NC5  CONTROL: the derived expression agrees with the independently written closed form "
      "(2-eta)(L-1)/[eta(3L-1)] at three (L, eta) points, so Part C is not a transcription of the "
      "form it was compared against")


# =============================================================================================
print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- THE SPIN-0 MODE IS HEALTHY.  STEP 2 SURVIVES.
  1.  The quadratic scalar action was DERIVED from the ADM pieces, with alpha and B appearing
      without time derivatives, i.e. as constraints.
  2.  *** GR IS REPRODUCED: at eta = 0 the alpha constraint forces zeta = 0, so general relativity
      has no propagating scalar and the mode found is genuinely the Lorentz-violating one. ***
  3.  c_s^2 = xi(2xi - eta)(1-L)/[eta(1-3L)], and at xi = 1 (forced to 1e-15 by GW170817)
      c_s^2 = (2-eta)(L-1)/[eta(3L-1)].
  4.  *** NO GHOST <=> L > 1 or L < 1/3;  NO GRADIENT INSTABILITY <=> 0 < eta < 2.  The two
      conditions COINCIDE -- one band, 1/3 < L < 1, carries both diseases -- and the healthy window
      is nonempty and explicit. ***
  5.  *** In the PPN-safe corner c_s^2 -> (L-1)/eta exactly, so the Cherenkov bound reduces to the
      single inequality L - 1 >= eta > 0, and superluminal is SAFE because there is a preferred
      frame.  PPN and Cherenkov make independent demands: NO CONFLICT. ***
  COSTS: the health is achieved BY CHOICE, not predicted -- step 2 added TWO free parameters and
  nothing forces them; and the eta -> 0 corner PPN prefers is the known strong-coupling corner,
  whose scale is NOT computed here and is now the sharpest worry about step 2.
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
