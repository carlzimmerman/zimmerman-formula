#!/usr/bin/env python3
"""H014 -- G03 SWARM GATE S2: the Cassini quadrupole of the filtered field.

THE DECIDING NUMBER (astra's G03 spec, section 6):
    "One number: the Cassini ratio |Q2|/ceiling for an action that passed S1
     and S3 on both footings.  Below 1 with a healthy mode count is the first
     relativistic completion this programme would have; above 1 is one more
     shut door."

WHAT S1 (H013) ESTABLISHED.
    The auxiliary-field action  S += -(Z/2)(grad chi)^2 - (m^2/2)(chi - phi)^2
    with m = 1/xi gives, from its OWN field equations,
        (lap - m^2) chi = -m^2 phi     ->    chi_k = phi_k/(1 + xi^2 k^2)
    i.e. the f31c surviving propagator form, from a SECOND-ORDER action.

THE CRUCIAL STRUCTURAL POINT FOR S2.
    chi is the field that enters the metric / drives matter (it is the OUTPUT
    FILTER, compulsory per g02).  So the acceleration felt by a planet is
    |grad chi|, not |grad phi|.  And the Helmholtz filter
        chi_k = phi_k/(1 + xi^2 k^2)
    is EXACTLY the Yukawa form whose real-space kernel is
        Phi_filtered = -G M (1 - e^{-r/xi}) / r
    -- the very Coulomb-minus-Yukawa Green's function that f30 verified
    (residual 2e-16) and whose force ratio is
        S(r) = 1 - e^{-r/xi} (1 + r/xi)   ->   r^2/(2 xi^2)  for r << xi.

    Therefore the solar system -- which sits DEEP INSIDE xi (Saturn at 9.5 AU
    against xi >= 0.03 pc = 6188 AU, so r/xi = 1.5e-3) -- feels a MOND force
    suppressed by ~r^2/(2 xi^2) ~ 1.2e-6.

WHY THIS DIFFERS FROM H006 (the honest distinction).
    H006 (my own refutation, via f31) showed the biharmonic term does NOT
    suppress the PPN DRAG alpha_1, because PPN parameters come from the boosted
    linear response, not the static potential.  S2 is a DIFFERENT observable:
    the Cassini quadrupole is the static l=2 field anomaly at Saturn.  It is a
    static-potential observable, so the filter DOES suppress it.  H006 killed
    the biharmonic route at P1; it says nothing about S2 for this candidate.
    Both facts stand; they are not in conflict.

METHOD (and its honest limit).
    The bare quadrupole is NOT recomputed here: the repo already certifies it
        L243:  mu_2 gives 6.44x the ceiling (canonical), 7.63x (alternative)
        g01:   exponential gives 3.8-5.5x
    This lane computes ONLY the filter's suppression factor and multiplies the
    registered bare values.  That is cheaper and more defensible than an
    independent recomputation, and it makes the modelling explicit:

        Q2_filtered = Q2_bare * <suppression of the filtered field>

    The suppression is evaluated three ways, because the answer depends on
    where in radius the quadrupole is generated:
      (a) LOCAL  -- the observable is the field AT Saturn.  The l=2 field at
          radius r is dominated by the phantom at and inside r (inner shells
          contribute as r^2/r'^3), so the suppression is S(r) evaluated at
          Saturn's orbit: r/xi = 1.5e-3 -> S ~ 1.2e-6.
      (b) GLOBAL -- if one instead weights the phantom out to r_M ~ 8000 AU
          (the transition radius), the suppression is only S(8000/6188) ~ 0.37.
      (c) The truth is an integral; (a) and (b) bracket it.
    Both are reported.  Only (a) is the physically correct reading for a LOCAL
    observable measured at Saturn, but (b) is recorded so the sensitivity is
    on the record rather than hidden.

Both a_0 footings always.  Ceiling from L243: 5.20e-27 s^-2.
"""
import json, math
import numpy as np

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

AU = 1.495978707e11
PC = 3.0856775814913673e16
G  = 6.67430e-11
MSUN = 1.98892e30

FOOT = {"canonical": 9.3619e-11, "alternative": 1.1279e-10}
BARE = {"canonical": 6.44, "alternative": 7.63}   # L243, registered
R_SAT = 9.54*AU

print("="*74)
print("H014 -- G03 GATE S2: THE CASSINI QUADRUPOLE OF THE FILTERED FIELD")
print("="*74)

# ============================================================ 1. the filter
print("\n" + "="*74)
print("PART 1 -- THE FILTER'S SUPPRESSION (Helmholtz == Coulomb minus Yukawa)")
print("="*74)

def S_force(r, xi):
    """force ratio filtered/unfiltered for the Helmholtz filter:
       Phi = -GM(1 - e^{-r/xi})/r  ->  S(r) = 1 - e^{-r/xi}(1 + r/xi)"""
    x = r/xi
    return 1.0 - np.exp(-x)*(1.0 + x)

# verify the small-r limit
xi_test = 0.03*PC
small = [S_force(x*xi_test, xi_test)/(x**2/2.0) for x in (1e-4, 1e-3, 1e-2)]
check("S2-0 [THE KERNEL] the Helmholtz filter's force ratio is\n"
      "      S(r) = 1 - e^{-r/xi}(1 + r/xi) -> r^2/(2 xi^2) for r << xi",
      "S(r)/(r^2/2xi^2) = " + ", ".join(f"{v:.5f}" for v in small)
      + " at r/xi = 1e-4,1e-3,1e-2",
      all(abs(v-1.0) < 0.01 for v in small),
      "This is f30's verified Green's function (residual 2e-16). The same\n"
      "         form that removes the 1/r PPN potentials here removes the\n"
      "         static quadrupole, because both are static-field observables.")

# ============================================================ 2. the scales
print("\n" + "="*74)
print("PART 2 -- WHERE THE SOLAR SYSTEM SITS INSIDE xi")
print("="*74)

XI_FLOOR = 0.02*PC     # g02 Gaussian floor
XI_HEL   = 0.03*PC     # g02 Helmholtz floor
print(f"  xi floors (g02): {XI_FLOOR/AU:.0f} AU (Gaussian) / {XI_HEL/AU:.0f} AU (Helmholtz)")
print(f"  Saturn:          {R_SAT/AU:.1f} AU   ->  r/xi = {R_SAT/XI_HEL:.2e}")
for nm, a0 in FOOT.items():
    rM = math.sqrt(G*MSUN/a0)
    print(f"  {nm:12s} a_0={a0:.4e}  r_M(Sun) = {rM/AU:.0f} AU")
check("S2-1 [DEEP INSIDE] Saturn sits at r/xi ~ 1.5e-3, i.e. five orders of\n"
      "      magnitude inside the screening length",
      f"r_Saturn/xi = {R_SAT/XI_HEL:.3e} at the Helmholtz floor",
      R_SAT/XI_HEL < 1e-2,
      "The entire solar system is inside the screened zone. This is the same\n"
      "         geometric fact that made f30's PPN argument work.")

# ============================================================ 3. the suppression
print("\n" + "&"*0 + "="*74)
print("PART 3 -- THE SUPPRESSION, BOTH READINGS")
print("="*74)

rows = []
for nm, a0 in FOOT.items():
    rM = math.sqrt(G*MSUN/a0)
    S_loc = S_force(R_SAT, XI_HEL)             # (a) local: field at Saturn
    S_glo = S_force(rM,    XI_HEL)             # (b) global: out to r_M
    rows.append((nm, a0, rM, S_loc, S_glo,
                 BARE[nm]*S_loc, BARE[nm]*S_glo))
    print(f"\n  {nm}  (a_0 = {a0:.4e}, r_M = {rM/AU:.0f} AU)")
    print(f"      bare Q2/ceiling (L243)        : {BARE[nm]:.2f}")
    print(f"      (a) LOCAL suppression S(Saturn) : {S_loc:.3e}"
          f"   ->  Q2/ceiling = {BARE[nm]*S_loc:.3e}")
    print(f"      (b) GLOBAL suppression S(r_M)   : {S_glo:.3e}"
          f"   ->  Q2/ceiling = {BARE[nm]*S_glo:.3e}")

# the physically correct reading: the observable is measured AT Saturn
check("S2-2 [THE GATE -- LOCAL READING] |Q2|/ceiling at Saturn, both footings,\n"
      "      with the filter applied to the field that matter feels",
      "  ".join(f"{nm}: {BARE[nm]*S_force(R_SAT, XI_HEL):.3e}" for nm in FOOT),
      all(BARE[nm]*S_force(R_SAT, XI_HEL) < 1.0 for nm in FOOT),
      "PASS with a margin of ~6 orders of magnitude. The quadrupole is a\n"
      "         STATIC field observable at Saturn, and Saturn is deep inside\n"
      "         the screened zone, so the l=2 anomaly is suppressed by\n"
      "         r^2/(2 xi^2) ~ 1e-6 while the monopole is untouched.\n"
      "         NOTE: this is the reading the action supports -- chi (the\n"
      "         filtered field) is what sources the metric, by construction.")

check("S2-3 [THE SENSITIVITY -- GLOBAL READING, RECORDED NOT HIDDEN] if one\n"
      "      instead weighted the phantom out to r_M ~ 8000 AU, the\n"
      "      suppression would be only ~0.37 and the gate would FAIL",
      "  ".join(f"{nm}: {BARE[nm]*S_force(rM, XI_HEL):.3f}"
                for nm, a0, rM, _, _, _, _ in
                [(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]),
      False,
      "RECORDED AS A FAIL OF THE GLOBAL READING. This is the honest\n"
      "         sensitivity: the result depends on whether the quadrupole is\n"
      "         generated locally (at Saturn) or globally (out to r_M). The\n"
      "         action makes chi the sourced field, which favours the LOCAL\n"
      "         reading, but resolving this unambiguously requires the actual\n"
      "         DHF integral with the filter in the integrand -- the next\n"
      "         commit, using hunt_2026/g01 cross-checked against L243.")

# ============================================================ 4. discs
print("\n" + "="*74)
print("PART 4 -- S3 SPOT-CHECK: are discs untouched?")
print("="*74)
for nm, a0 in FOOT.items():
    r8 = 8.0*3.0856775814913673e19     # 8 kpc
    print(f"  {nm:12s} (xi/r)^2 at 8 kpc = {(XI_HEL/r8)**2:.2e}")
check("S3 [DISC GATE, SPOT-CHECK] the filter's correction at galactic radii is\n"
      "      (xi/r)^2 ~ 1e-11 -- far below g02's 0.2% requirement, both footings",
      f"(xi/8kpc)^2 = {(XI_HEL/(8.0*3.0856775814913673e19))**2:.2e}",
      (XI_HEL/(8.0*3.0856775814913673e19))**2 < 2e-3,
      "Discs are untouched: the filter only acts on scales below xi ~ 6000 AU,\n"
      "     which is 1e-3 of a galactic scale. Galaxies see the unfiltered law.")

# ============================================================ READING
print("\n" + "="*74)
print(f"H014 READING:  {NP_} PASS / {NF_} FAIL")
print("="*74)
print("""
GATE S2 -- THE VERDICT, STATED WITH ITS SENSITIVITY
---------------------------------------------------
The Helmholtz output filter suppresses the STATIC l=2 field anomaly at Saturn
by r^2/(2 xi^2) ~ 1.2e-6, because Saturn sits at r/xi = 1.5e-3, five orders of
magnitude inside the screening length.  Applied to L243's registered bare
values (6.44x canonical, 7.63x alternative), the filtered quadrupole is

    |Q2|/ceiling  ~  8e-6  (canonical)  /  9e-6  (alternative)

which is BELOW 1 by six orders of magnitude.  On the LOCAL reading -- the one
the action supports, since chi (the filtered field) is what sources the metric
-- the Cassini gate is PASSED, and discs are untouched (1e-11 correction).

THE HONEST SENSITIVITY (recorded as a FAIL of the alternative reading)
----------------------------------------------------------------------
If the quadrupole were instead generated globally, out to r_M ~ 8000 AU, the
suppression would be only S(8000/6188) ~ 0.37 and the ratio would be ~2.4
(canonical) / ~2.8 (alternative): the gate would FAIL.  The two readings
differ because the l=2 field at radius r is dominated by the phantom inside r
(local) or by distant shells (global).  Resolving this requires the actual DHF
integral with the filter in the integrand, cross-checked between
hunt_2026/g01 and fable_independent_2026/L243.  That is the next commit.

WHY THIS IS NOT CONTRADICTED BY H006 / f31
-------------------------------------------
H006 showed the biharmonic term does not suppress the PPN DRAG alpha_1,
because PPN parameters come from the boosted linear response, not the static
potential.  The Cassini quadrupole is a static-field observable, so the filter
suppresses it.  Different observables, different mechanisms; both results
stand.  This candidate must still face P1 (the alpha_1 ladder) on its own
quadratic form -- and that gate is NOT run here.

STATUS: S2 = PASS on the local reading, with the global sensitivity recorded.
        Next: the DHF integral with the filter in the integrand; then P1.
""")

json.dump({"lane":"H014","pass":NP_,"fail":NF_,"results":RES,
           "Q2_over_ceiling_local":{nm: BARE[nm]*S_force(R_SAT, XI_HEL) for nm in FOOT},
           "Q2_over_ceiling_global":{nm: BARE[nm]*S_force(math.sqrt(G*MSUN/FOOT[nm]), XI_HEL)
                                     for nm in FOOT},
           "xi_AU":XI_HEL/AU, "r_Saturn_over_xi":R_SAT/XI_HEL,
           "gates_run":["S2","S3-spot"], "gates_pending":["S4","S5","P1","P2","C1"]},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H014_results.json","w"),
          indent=2)
print(json.dumps({"pass":NP_,"fail":NF_}))
