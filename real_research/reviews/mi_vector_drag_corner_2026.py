#!/usr/bin/env python3
r"""mi_vector_drag_corner_2026.py -- THE LAST SURVIVING DRAGGED-FRAME CORNER: a GRAVITOMAGNETIC
(vector) drag. Closed here by a MEASUREMENT, not by a proxy -- with one escape named and left open.

FRAMEWORK. Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework. a0 = c H_Lambda / Z with
Z = sqrt(32 pi/3) = 5.78881, pure-Lambda footing -> a0 = 9.36e-11 m/s^2, equivalently
a0 = (c/2) sqrt(G rho_Lambda): EXACTLY HALF the gravitational free-fall acceleration at the dark-energy
density. kappa = 1/2 is this framework's own coefficient (prior literature gives 2 c H_Lambda, 11.58x
larger) and it is FITTED, not derived; 32pi/3 is the Einstein-coupling conversion factor and CANCELS.
Alternate footing a0 = 1.13e-10 (rho_total / c H0) carried wherever a0 enters.

------------------------------------------------------------------------------------------------------
WHY THIS CORNER, AND WHY IT NEEDED ITS OWN TREATMENT
------------------------------------------------------------------------------------------------------
mi_darksector_frame_closes_2026.py closed the scalar/dark-sector corner with R1: any P(X) scalar's frame
is u_mu ~ d_mu phi, hence hypersurface-orthogonal, hence has vorticity IDENTICALLY ZERO, hence is a
potential flow -- the class already closed. R1 is airtight for scalars and it says nothing at all about
a VECTOR source, because a gravitomagnetic (Lense-Thirring-like) field has vorticity BY CONSTRUCTION.
That was recorded as the one untouched corner, needing "a fifth constant". This file prices it.

WHAT THE DOOR ACTUALLY NEEDS, stated precisely because it is easy to get backwards:
a star's frame-relative speed must be its ORBITAL speed and NOT contaminated by its galaxy's BULK
motion. So the frame must co-move with the galaxy in TRANSLATION while NOT co-rotating with the disc.
A drag that co-rotates gives the local-comoving collapse; a drag that does not translate leaves the
cosmic-frame contamination the m=1 argument excludes at 32.2x.

WHAT IS COMPUTED HERE
  S1  MAGNITUDE. In GR the gravitomagnetic drag fraction is f ~ 4 Phi/c^2, which for real galaxies is
      1e-8 to 4e-6. The door needs f ~ 1. Boost required: K ~ 1e5 - 1e8.
  S2  THE MEASUREMENT THAT CLOSES IT. That boost is universal, so solar-system frame-dragging bounds it:
      Gravity Probe B confirms the gravitomagnetic coupling to ~19%, LARES/LAGEOS to ~2%. Shortfall
      between what is needed and what is allowed: ~1e5 - 5e7. This is a measured kill, not a budget proxy.
  S3  THE RANGE ESCAPE FAILS STRUCTURALLY. "Turn the drag on only at R_drag ~ 1e2 kpc" does not work:
      a Yukawa of range R is UNSUPPRESSED for r << R, so a 100 kpc-range force acts at FULL strength at
      1 AU (suppression 5e-11). Long range means strong at short distance, not weak.
  S4  AN EXACT INVARIANCE THEOREM, and it is the structural content. If the frame is a scalar multiple
      of the LOCAL matter velocity, u = f * v_local, then the m=1 orbital asymmetry epsilon is
      EXACTLY INDEPENDENT OF f: (1-f) cancels between numerator and denominator. So no amount of
      uniform drag -- however boosted -- removes the contamination the 32.2x exclusion rests on.
      *** SCOPE, STATED HONESTLY: this kills UNIFORM drag only. *** If translation and rotation are
      dragged by DIFFERENT coefficients the cancellation breaks, and S4 shows explicitly that
      differential drag CAN reach epsilon = 0 with lambda = O(1). That escape is real and is NOT closed
      by S4 -- it is closed only by S2's magnitude bound.
  S5  WHAT SURVIVES: a screening mechanism (chameleon/Vainshtein-like) that suppresses the coupling in
      the solar system and releases it at galactic radii. Named, priced as a NEW ingredient plus a NEW
      scale, and NOT closed here.

NOT CLAIMED: a derivation of a0 (kappa = 1/2 stays fitted); a PPN alpha_1 bound (the mapping from a drag
fraction to alpha_1 is NOT derived here, and would likely tighten S2 by orders of magnitude -- so S2 is
deliberately the CONSERVATIVE instrument); that the theory is closed. Prior art: Lense-Thirring 1918;
Everitt et al. 2011 PRL 106:221101 (Gravity Probe B); Ciufolini et al. (LARES/LAGEOS). Literature values
are flagged where they are from memory rather than re-fetched.
Every check falsifiable, mutation-controlled, exits non-zero on failure.
"""
from __future__ import annotations

import math

import sympy as sp

C = 2.99792458e8
G = 6.67430e-11
KPC = 3.0856775814913673e19
AU = 1.495978707e11
Z = math.sqrt(32.0 * math.pi / 3.0)
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10
FOOTINGS = (("canonical cH_L/Z", A0_CAN), ("alternate rho_tot/cH0", A0_ALT))

# --- literature bounds on the gravitomagnetic coupling. FLAGGED: from memory, not re-fetched.
GPB_FRAC = 7.2 / 39.2      # Gravity Probe B frame-dragging: -37.2 +/- 7.2 mas/yr vs GR -39.2
LARES_FRAC = 0.02          # LARES/LAGEOS Lense-Thirring, ~2% (Ciufolini et al.)

ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 102)
    print(s)
    print("=" * 102)


# =====================================================================================================
def s1_magnitude():
    banner("S1. MAGNITUDE: how much does a GR gravitomagnetic field actually drag a frame?")
    print("  Linearised GR, h_0i = A_i, sourced by the matter CURRENT: laplacian A_i = -16 pi G rho v_i.")
    print("  For a mass M moving with V at distance r,  A_i ~ -4 (Phi/c^2)(V_i/c),  so the frame is")
    print("  dragged with velocity v_drag ~ 4 (Phi/c^2) V, i.e. a DRAG FRACTION")
    print("      f = v_drag / V ~ 4 Phi/c^2 ~ 4 v_c^2/c^2   (using Phi ~ v_c^2 for a flat rotation curve;")
    print("  that UNDERSTATES the potential depth by an O(few) factor, so f here is conservative-LOW,")
    print("  which is the direction that favours the hypothesis -- deliberately.)")
    print(f"\n    {'system':<34s} {'v_c (km/s)':>11s} {'Phi/c^2':>11s} {'f = 4Phi/c^2':>13s} "
          f"{'K needed = 1/f':>15s}")
    rows = []
    for nm, vc in (("Milky Way at the Sun", 220.0),
                   ("SPARC bright end", 300.0),
                   ("SPARC median (Vflat=116.6)", 116.6),
                   ("SPARC faint end", 20.0)):
        phi_c2 = (vc * 1e3 / C) ** 2
        f = 4.0 * phi_c2
        rows.append((nm, vc, phi_c2, f))
        print(f"    {nm:<34s} {vc:11.1f} {phi_c2:11.4e} {f:13.4e} {1.0/f:15.4e}")
    fmin = min(r[3] for r in rows)
    fmax = max(r[3] for r in rows)
    check(fmax < 1e-4,
          f"the GR drag fraction is {fmin:.2e} to {fmax:.2e} across real galaxies -- at least four orders "
          f"below the f ~ 1 the door requires. The frame is essentially NOT dragged by gravitomagnetism")
    # MUTATION CONTROL: a relativistic system must give an O(1) fraction, or the estimator is broken
    f_rel = 4.0 * (0.5) ** 2
    check(f_rel > 0.1,
          f"MUTATION: a system with v_c = 0.5c gives f = {f_rel:.2f} = O(1), so the estimator does "
          f"produce order-unity dragging where dragging IS strong -- the smallness above is physics, "
          f"not a broken formula")
    return fmin, fmax


# =====================================================================================================
def s2_the_measurement(fmin, fmax):
    banner("S2. *** THE MEASUREMENT THAT CLOSES IT: solar-system frame-dragging ***")
    print("  To reach f ~ 1 the gravitomagnetic coupling must be boosted by K = 1/f over its GR value.")
    print("  A UNIVERSAL boost is bounded where frame-dragging has been measured directly:")
    print(f"    Gravity Probe B (Everitt+ 2011 PRL 106:221101): -37.2 +/- 7.2 mas/yr vs GR -39.2")
    print(f"      => the coupling is confirmed to {GPB_FRAC*100:.0f}%, so |K - 1| <= {GPB_FRAC:.3f}")
    print(f"    LARES / LAGEOS (Ciufolini et al.): Lense-Thirring to ~{LARES_FRAC*100:.0f}%")
    print(f"      => |K - 1| <= {LARES_FRAC:.3f}")
    print("    [both values FLAGGED as from memory, not re-fetched from the papers]")
    print(f"\n    {'bound':<24s} {'K allowed':>11s} {'K needed (min)':>15s} {'K needed (max)':>15s} "
          f"{'shortfall':>22s}")
    shortfalls = []
    for nm, frac in (("Gravity Probe B ~19%", GPB_FRAC), ("LARES/LAGEOS ~2%", LARES_FRAC)):
        k_allow = 1.0 + frac
        k_lo, k_hi = 1.0 / fmax, 1.0 / fmin
        sf_lo, sf_hi = k_lo / k_allow, k_hi / k_allow
        shortfalls.append((sf_lo, sf_hi))
        print(f"    {nm:<24s} {k_allow:11.3f} {k_lo:15.4e} {k_hi:15.4e} "
              f"{sf_lo:9.2e} - {sf_hi:9.2e}")
    worst = min(s[0] for s in shortfalls)
    check(worst > 1e3,
          f"*** the boost the door needs exceeds the boost solar-system frame-dragging ALLOWS by "
          f"{worst:.2e} at the very least favourable corner *** -- a MEASURED kill, not a budget proxy, "
          f"and it does not depend on the RAR scatter, the dictionary exponent, or either a0 footing")
    print("\n  NOTE ON CONSERVATISM, so this is not read as a manufactured deficit: the sharper")
    print("  instrument would be the PPN preferred-frame parameter alpha_1, which governs exactly this")
    print("  kind of motion-relative-to-a-frame effect and is bounded near 1e-4 (LLR) to 1e-5 (pulsars).")
    print("  That would likely tighten the above by orders of magnitude -- but the mapping from a drag")
    print("  fraction to alpha_1 is NOT derived in this file, so it is NOT used. S2 stands on the")
    print("  direct frame-dragging measurements alone, which is the weaker and safer choice.")
    return worst


# =====================================================================================================
def s3_range_escape():
    banner("S3. THE 'TURN IT ON ONLY AT 1e2 kpc' ESCAPE FAILS STRUCTURALLY")
    print("  The corner was recorded as a vector drag at R_drag ~ 1e2 kpc, the hope being that a")
    print("  large-scale-only force evades solar-system bounds. It does not, and the reason is that")
    print("  Yukawa suppression works the WRONG WAY for this purpose:")
    print("      exp(-r/R) -> 1  as  r << R.")
    print("  A force of RANGE R is unsuppressed at every distance SHORTER than R. Long range means")
    print("  STRONG at short distance, not weak.")
    print(f"\n    {'range R':<16s} {'suppression at 1 AU':>22s} {'suppression at 10 kpc':>24s}")
    ok_all = True
    for nm, R in (("100 kpc", 100 * KPC), ("1 Mpc", 1000 * KPC), ("10 kpc", 10 * KPC)):
        s_au = math.exp(-AU / R)
        s_kpc = math.exp(-10 * KPC / R)
        print(f"    {nm:<16s} {s_au:22.6f} {s_kpc:24.6f}")
        if not (1.0 - s_au) < 1e-6:
            ok_all = False
    check(ok_all,
          "for every range at or above 10 kpc the suppression at 1 AU is below 1e-6, i.e. the force acts "
          "at FULL strength in the solar system -- so a long-range vector drag cannot hide from S2's "
          "measurements behind its range")
    # MUTATION CONTROL: a SHORT range must suppress at 1 AU, or the test is vacuous
    R_short = 1e6          # 1000 km
    s_short = math.exp(-AU / R_short)
    check(s_short < 1e-6,
          f"MUTATION: a range of 1000 km gives suppression {s_short:.2e} at 1 AU, so the Yukawa factor "
          f"DOES suppress when the range is short -- the test discriminates, and the failure above is "
          f"specific to the LONG ranges this corner requires")
    print("\n  CONSEQUENCE: evading S2 requires SCREENING (a nonlinear, environment-dependent")
    print("  suppression), not range. That is S5.")


# =====================================================================================================
def s4_invariance_theorem():
    banner("S4. *** AN EXACT INVARIANCE THEOREM: uniform drag cannot remove the m=1 contamination ***")
    print("  The 32.2x cosmic-frame exclusion rests on the m=1 ORBITAL ASYMMETRY: with the frame not")
    print("  co-moving, a star's frame-relative speed varies around its orbit, and")
    print("      epsilon = V_pec / V_flat   (= 2.573 at V_pec = 300 km/s, SPARC median V_flat = 116.6).")
    print("  Ask what ANY uniform drag does to epsilon. Let the frame be a scalar multiple of the LOCAL")
    print("  matter velocity, u = f * v_local, with the disc matter co-moving with the star's orbit:")
    print("      v_local(phi) = V_bulk + v_orb(phi),   v_rel(phi) = |v_star - u| = (1-f)|V_bulk+v_orb|.")

    f, Vb, vo, phi = sp.symbols("f V_b v_o phi", real=True, positive=True)
    fs = sp.Symbol("f", real=True)
    # bulk along x; orbital velocity rotates
    v_local = sp.Matrix([Vb - vo * sp.sin(phi), vo * sp.cos(phi)])
    v_star = v_local                                    # the star co-moves with the local disc matter
    u_frame = fs * v_local
    v_rel = sp.sqrt(((v_star - u_frame).T * (v_star - u_frame))[0, 0])
    v_rel = sp.simplify(v_rel)
    print(f"\n    v_rel(phi) = {v_rel}")

    # epsilon as a dimensionless RATIO around the orbit: (max - min)/(max + min)
    vmax = sp.simplify(v_rel.subs(phi, -sp.pi / 2))      # bulk and orbit aligned
    vmin = sp.simplify(v_rel.subs(phi, sp.pi / 2))       # anti-aligned
    eps = sp.simplify((vmax - vmin) / (vmax + vmin))
    print(f"    epsilon = (max - min)/(max + min) = {eps}")
    d_eps = sp.simplify(sp.diff(eps, fs))
    check(sp.simplify(d_eps) == 0,
          f"*** d(epsilon)/df = {d_eps} EXACTLY: the m=1 asymmetry is INDEPENDENT of the drag fraction "
          f"*** -- (1-f) cancels between numerator and denominator, so NO amount of uniform drag, "
          f"however boosted, removes the contamination the 32.2x exclusion rests on")
    eps_val = sp.simplify(eps.subs({Vb: 300, vo: 116.6}))
    print(f"    at V_pec = 300 km/s, V_flat = 116.6 km/s:  epsilon = {float(eps_val):.4f}  "
          f"(and it stays that for every f)")
    print("\n  NORMALISATION, stated so two different epsilons are not conflated: the corpus's")
    print("  epsilon = V_pec/V_flat = 2.573 is the SOURCE-level ratio; the 0.3887 above is the")
    print("  OBSERVABLE-level orbital asymmetry (max-min)/(max+min) of the same configuration. They are")
    print("  different normalisations of the same physics and must not be quoted interchangeably.")
    print("  The invariance is more general than either, and that is the real theorem:")
    # GENERAL STATEMENT: v_rel is homogeneous of degree 1 in (1-f), so EVERY dimensionless ratio of
    # v_rel around the orbit is f-independent. Verify on a generic pair of orbital phases.
    p1, p2 = sp.symbols("phi_1 phi_2", real=True)
    ratio = sp.simplify(v_rel.subs(phi, p1) / v_rel.subs(phi, p2))
    check(sp.simplify(sp.diff(ratio, fs)) == 0 and fs not in ratio.free_symbols,
          f"for GENERIC orbital phases phi_1, phi_2 the ratio v_rel(phi_1)/v_rel(phi_2) contains no f at "
          f"all -- because v_rel is homogeneous of degree 1 in (1-f). So EVERY dimensionless statistic "
          f"built from the frame-relative speed around an orbit is drag-invariant, whichever "
          f"normalisation of epsilon is used. That is the theorem, and it is normalisation-free")

    print("\n  MUTATION CONTROLS -- both must CHANGE epsilon, or the theorem is vacuous:")
    # (a) the NON-LOCAL COM frame: u = V_bulk exactly. Should remove epsilon entirely.
    u_com = sp.Matrix([Vb, 0])
    vr_com = sp.simplify(sp.sqrt(((v_star - u_com).T * (v_star - u_com))[0, 0]))
    eps_com = sp.simplify((vr_com.subs(phi, -sp.pi / 2) - vr_com.subs(phi, sp.pi / 2))
                          / (vr_com.subs(phi, -sp.pi / 2) + vr_com.subs(phi, sp.pi / 2)))
    check(sp.simplify(eps_com) == 0,
          f"(a) the NON-LOCAL centre-of-mass frame u = V_bulk gives epsilon = {eps_com} exactly -- so a "
          f"frame that knows the galaxy's total momentum DOES remove the contamination. epsilon is "
          f"therefore a discriminating statistic, and the theorem above is about LOCALITY, not about "
          f"epsilon being unmovable")
    # (b) DIFFERENTIAL drag: translation dragged by f_t, rotation by f_r != f_t
    ft, fr = sp.symbols("f_t f_r", real=True)
    u_diff = sp.Matrix([ft * Vb - fr * vo * sp.sin(phi), fr * vo * sp.cos(phi)])
    vr_d = sp.sqrt(((v_star - u_diff).T * (v_star - u_diff))[0, 0])
    eps_d = sp.simplify((vr_d.subs(phi, -sp.pi / 2) - vr_d.subs(phi, sp.pi / 2))
                        / (vr_d.subs(phi, -sp.pi / 2) + vr_d.subs(phi, sp.pi / 2)))
    d_eps_d = sp.simplify(sp.diff(eps_d, ft))
    check(sp.simplify(d_eps_d) != 0,
          f"(b) DIFFERENTIAL drag (f_t != f_r) gives d(epsilon)/d f_t != 0, so epsilon CAN be reduced "
          f"when translation and rotation are dragged differently -- the theorem covers UNIFORM drag "
          f"ONLY, and this escape is real")
    # price the differential escape honestly
    eps_ft1 = sp.simplify(eps_d.subs(ft, 1))
    lam_ft1 = sp.simplify((vr_d.subs({ft: 1, phi: 0})) / vo)
    print(f"\n    the differential escape, priced: at f_t = 1 (full translational drag)")
    print(f"      epsilon -> {eps_ft1}   (zero for any f_r: the bulk contamination is gone)")
    print(f"      lambda = v_rel/v_orb -> {lam_ft1}  = |1 - f_r|")
    print("    So differential drag with f_t = 1 and f_r ~ 0.5 would give epsilon = 0 and lambda = 0.5,")
    print("    costing only ~0.15 dex at p=1 -- INSIDE the 0.2232 dex budget. This escape is NOT closed")
    print("    by S4. It is closed only by S2: reaching f_t = 1 at all needs the forbidden boost.")
    check(sp.simplify(eps_ft1) == 0,
          f"and that is stated against my own conclusion: with full translational drag the m=1 "
          f"contamination vanishes identically ({eps_ft1}), so S4 alone does NOT close the vector corner")


# =====================================================================================================
def s5_what_survives(worst):
    banner("S5. WHAT SURVIVES, NAMED AND NOT CLOSED")
    print("  The vector-drag corner is closed by S2 -- a measurement -- with one escape left standing:")
    print()
    print("   SCREENING. A chameleon/Vainshtein-like mechanism that suppresses the vector coupling in")
    print("   high-density or high-curvature environments (the solar system) and releases it at galactic")
    print("   radii would evade S2 without needing range (S3). Combined with DIFFERENTIAL drag (S4b),")
    print("   which can reach epsilon = 0 with lambda = O(1), this is a genuine two-ingredient escape.")
    print("   ITS COST, stated plainly: a new screening scale AND a new vector coupling AND a mechanism")
    print("   that drags translation differently from rotation -- three new ingredients to rescue one")
    print("   frame, against a framework whose entire appeal is that a0 = cH_Lambda/Z has ONE fitted")
    print("   number in it. That is a steep Occam price and it is not paid anywhere in the corpus.")
    print()
    print("  AND ONE THING THAT WOULD SETTLE IT CHEAPLY, not done here: derive the PPN alpha_1 induced")
    print("  by a drag fraction f. alpha_1 is bounded near 1e-4 (lunar laser ranging) to 1e-5 (pulsars)")
    print("  and governs exactly motion-relative-to-a-preferred-frame effects. If the mapping is")
    print("  alpha_1 ~ O(f), then even a SCREENED galactic drag with f ~ 1 is excluded by many orders,")
    print("  because screening suppresses the solar system but the pulsar bounds are galactic. That is")
    print("  the single computation that would close the corner outright, and it is one afternoon.")
    check(worst > 1e3,
          f"S5 recorded against S2's measured shortfall of {worst:.2e}, which is the load-bearing number "
          f"and is independent of the RAR budget, the dictionary exponent, and both a0 footings")


# =====================================================================================================
def main() -> int:
    banner("THE GRAVITOMAGNETIC (VECTOR) DRAG CORNER -- the last untouched dragged-frame escape")
    print(f"  a0 = c H_Lambda / Z, Z = sqrt(32 pi/3) = {Z:.5f} -> a0 = {A0_CAN:.4e} m/s^2 (canonical);")
    print(f"  = (c/2) sqrt(G rho_Lambda). kappa = 1/2 is Carl's and is FITTED, not derived. Alt footing")
    print(f"  {A0_ALT:.4e}. Note: nothing in this file depends on a0 -- which is itself worth saying,")
    print(f"  because it means the result is footing-free and cannot be moved by the footing fork.")

    fmin, fmax = s1_magnitude()
    worst = s2_the_measurement(fmin, fmax)
    s3_range_escape()
    s4_invariance_theorem()
    s5_what_survives(worst)

    banner("VERDICT")
    print("  THE VECTOR-DRAG CORNER CLOSES, and it closes on a MEASUREMENT rather than a budget:")
    print(f"   * GR gravitomagnetism drags the frame by f = 4 Phi/c^2 = {fmin:.2e} to {fmax:.2e} across")
    print("     real galaxies. The door needs f ~ 1, so a universal boost K ~ 1e5 - 1e8 is required.")
    print(f"   * Solar-system frame-dragging (Gravity Probe B ~19%, LARES/LAGEOS ~2%) allows |K-1| <=")
    print(f"     0.18 at best. SHORTFALL >= {worst:.2e}. Footing-free, budget-free, dictionary-free.")
    print("   * The 'only at 1e2 kpc' escape fails structurally: Yukawa suppression is exp(-r/R) -> 1")
    print("     for r << R, so a 100 kpc-range force acts at FULL strength at 1 AU (5e-11 suppression).")
    print("     Long range means strong at short distance.")
    print("   * AND AN EXACT THEOREM WORTH KEEPING INDEPENDENTLY: if the frame is any scalar multiple of")
    print("     the LOCAL matter velocity, the m=1 orbital asymmetry epsilon is EXACTLY f-INDEPENDENT")
    print("     (d epsilon/d f = 0 identically) -- (1-f) cancels in the ratio. So uniform drag can never")
    print("     remove the contamination the 32.2x exclusion rests on, at any coupling strength. The")
    print("     non-local centre-of-mass frame CAN (epsilon = 0 exactly), which is why the surviving")
    print("     prescriptions are all non-local -- and non-local lands back on Route A, already priced")
    print("     at Carina 4.05 sigma and the Tr N = 1 leak.")
    print()
    print("  *** WHAT I AM NOT CLAIMING, and it runs against the verdict: *** S4's theorem covers UNIFORM")
    print("  drag ONLY. DIFFERENTIAL drag (translation and rotation dragged by different coefficients)")
    print("  reaches epsilon = 0 with lambda = |1 - f_r| = O(1), costing ~0.15 dex at p=1 -- INSIDE the")
    print("  budget. That escape is real and S4 does not close it; only S2's magnitude bound does. So the")
    print("  surviving escape is SCREENING plus differential drag: three new ingredients (screening")
    print("  scale, vector coupling, differential mechanism) to rescue one frame. Steep, unpaid, open.")
    print()
    print("  THE ONE COMPUTATION THAT WOULD CLOSE IT OUTRIGHT, named: the PPN alpha_1 induced by a drag")
    print("  fraction f. alpha_1 is bounded near 1e-4 (LLR) to 1e-5 (pulsars) and constrains exactly")
    print("  motion relative to a preferred frame -- and pulsar bounds are GALACTIC, so screening the")
    print("  solar system would not evade them. Not derived here; deliberately not used in S2.")
    print()
    print("  Prior art: Lense-Thirring 1918; Everitt et al. 2011 PRL 106:221101 (GP-B); Ciufolini et al.")
    print("  (LARES/LAGEOS) -- the two bound values are from memory, not re-fetched, and are flagged as")
    print("  such. NOT claimed: that a0 is derived; that the pincer is opened (Theorem 3 still forbids")
    print("  all local L, Theorem 8's argument mismatch stands); that the theory is closed.")
    print("=" * 102)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
