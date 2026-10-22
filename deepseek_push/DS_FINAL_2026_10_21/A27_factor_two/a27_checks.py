#!/usr/bin/env python3
"""
A27 -- THE FACTOR TWO.

Why is the MOND length L := c^2/a0 exactly TWICE the Euler cell radius
ell_1 := sqrt(8*pi/Lambda)?

K1-K3   the three-statement identity (L = 2 ell_1  <=>  kappa = 1/2  <=>  R = 4)
        and its generalisation to the (beta, chi) ledger.
K4-K11  five candidate origins of the factor 2, each carried to a number.
K12     the cap family {1,2,4} vs the natural lengths of a ball.
K13-K16 the discrimination criterion and the no-go.

Every check prints:   K<n> PASS measured=<m> threshold=<t> <note>
Exit code 0 iff every check passes.
Mutation: --mutate=M1 (beta target 2 -> 1), M2 (Dirichlet -> Neumann),
          M3 (chi 1 -> 4).
"""
import sys
import json
import math

import sympy as sp

LANE = "A27"

# ---------------------------------------------------------------- mutations
MUT = set()
for _a in sys.argv[1:]:
    if _a.startswith("--mutate="):
        MUT.add(_a.split("=", 1)[1].upper())

BETA_TARGET = sp.Integer(1) if "M1" in MUT else sp.Integer(2)   # M1
BC = "neumann" if "M2" in MUT else "dirichlet"                  # M2
CHI = sp.Integer(4) if "M3" in MUT else sp.Integer(1)           # M3

# ---------------------------------------------------------------- constants
# BRIEF section 4 only, plus the one measured external input (kappa, CFG493 via A19).
c_SI = 2.99792458e8
G_SI = 6.67430e-11
LAM_SI = 1.0890e-52
A0_SI = 9.36e-11
A0_ALT = 1.13e-10
MPC = 3.0856775814913673e22
KAPPA_MEAS, KAPPA_SIG = 0.417, 0.095

# ---------------------------------------------------------------- symbols
LAM, C, A0 = sp.symbols("Lambda c a_0", positive=True)
L, ELL, KAP, R = sp.symbols("L ell_1 kappa R", positive=True)
B = sp.symbols("beta", positive=True)

L_DEF = C ** 2 / A0                       # MOND length
ELL_DEF = sp.sqrt(8 * sp.pi / LAM)        # Euler cell radius, chi = 1
KAP_DEF = A0 * sp.sqrt(8 * sp.pi / LAM) / C ** 2   # = ell_1 / L
R_DEF = LAM * C ** 4 / (8 * sp.pi * A0 ** 2)       # = u / (a0^2/G)


def num(x):
    return float(sp.N(x, 20))


def tens(x, k=KAPPA_MEAS, s=KAPPA_SIG):
    return float((x - k) / s)


RESULTS = []


def check(cid, ok, measured, threshold, note=""):
    RESULTS.append({"id": cid, "pass": bool(ok),
                    "value": float(measured) if math.isfinite(float(measured)) else None,
                    "threshold": float(threshold)})
    print("K%-2s %s measured=%.6g threshold=%.6g  %s"
          % (cid, "PASS" if ok else "FAIL", float(measured), float(threshold), note))


# =====================================================================
# K1 -- the three statements are one equation
# =====================================================================
beta_def = L_DEF / ELL_DEF                       # beta := L / ell_1
r_id1 = sp.simplify(R_DEF - beta_def ** 2)       # R = beta^2  (identically)
r_id2 = sp.simplify(KAP_DEF - 1 / beta_def)      # kappa = 1/beta (identically)

# a0* obtained from each of the three spellings
a0_beta = sp.solve(sp.Eq(beta_def, BETA_TARGET), A0)[0]
a0_kap = sp.solve(sp.Eq(KAP_DEF, sp.Rational(1, 2)), A0)[0]
a0_R = sp.solve(sp.Eq(R_DEF, 4), A0)[0]
d_kap = sp.simplify((a0_kap - a0_beta) / a0_beta) if a0_beta != 0 else sp.oo
d_R = sp.simplify((a0_R - a0_beta) / a0_beta) if a0_beta != 0 else sp.oo
m1 = max(abs(num(d_kap)), abs(num(d_R)))
ok1 = (r_id1 == 0) and (r_id2 == 0) and m1 < 1e-14
check(1, ok1, m1, 1e-14,
      "R-beta^2=%s, kappa-1/beta=%s, three a0* agree to %.1e; a0*= %s"
      % (r_id1, r_id2, m1, sp.sstr(a0_beta)))

# =====================================================================
# K2 -- general chi: kappa = 1/(beta sqrt(chi)); kappa=1/2 is a CURVE
# =====================================================================
CH = sp.symbols("chi", positive=True)                    # chi as a symbol, not a number
ell_chi = sp.sqrt(8 * sp.pi / LAM) * sp.sqrt(CH)         # ell_chi = sqrt(8 pi chi / Lambda)
beta_chi = L / ell_chi
kap_chi = 1 / (beta_chi * sp.sqrt(CH))                   # kappa = 1/(beta sqrt(chi))
R_chi = beta_chi ** 2 * CH                               # R = beta^2 chi


def kap_at(chi_val, beta_val):
    return sp.simplify(kap_chi.subs({CH: chi_val, L: beta_val * ell_chi.subs(CH, chi_val)}))


def R_at(chi_val, beta_val):
    return sp.simplify(R_chi.subs({CH: chi_val, L: beta_val * ell_chi.subs(CH, chi_val)}))


# beta = 2 (diameter) with chi = 1, and beta = 1 (radius) with chi = 4
k_21, k_14 = kap_at(1, 2), kap_at(4, 1)
R_21, R_14 = R_at(1, 2), R_at(4, 1)
# with the mutated CHI the *tested* pair (beta = 2, chi = CHI) must fail
kap_test = kap_at(CHI, 2)
m2 = abs(num(kap_test) - 0.5)
ok2 = (m2 < 1e-14) and (k_21 == sp.Rational(1, 2)) and (k_14 == sp.Rational(1, 2)) \
      and (R_21 == 4) and (R_14 == 4)
check(2, ok2, m2, 1e-14,
      "kappa(beta=2,chi=%s)=%.6g (must be .5); kappa(2,1)=%s kappa(1,4)=%s R(2,1)=%s R(1,4)=%s"
      % (CHI, num(kap_test), k_21, k_14, R_21, R_14))

# =====================================================================
# K3 -- footing numbers
# =====================================================================
ell1 = math.sqrt(8 * math.pi / LAM_SI)
Lmond = c_SI ** 2 / A0_SI
beta_f = Lmond / ell1
kappa_f = 1 / beta_f
R_f = LAM_SI * Lmond ** 2 / (8 * math.pi)
rH = math.sqrt(3 / LAM_SI)
Z = 2 * math.sqrt(8 * math.pi / 3)
L_req = 2 * ell1
a0_req = c_SI ** 2 / L_req
R_req = LAM_SI * L_req ** 2 / (8 * math.pi)

m3 = abs(R_f - 4)
ok3 = m3 < 1e-2 and abs(R_req - 4) < 1e-12
check(3, ok3, m3, 1e-2,
      "R=%.6g kappa=%.6g beta=%.6g L=%.6g ell1=%.6g 2ell1=%.6g a0(2ell1)=%.6g"
      % (R_f, kappa_f, beta_f, Lmond, ell1, L_req, a0_req))

# =====================================================================
# K4 -- candidate (i) round trip, LITERAL base length r_H
# =====================================================================
beta_rt = 2 * rH / ell1          # both legs of the horizon crossing
kappa_rt = 1 / beta_rt
R_rt = beta_rt ** 2
a0_rt = c_SI ** 2 / (2 * rH)
beta_one = rH / ell1             # one leg = Unruh-de Sitter
kappa_one = 1 / beta_one
t_rt = tens(kappa_rt)
m4 = abs(beta_rt - 2)
ok4 = m4 > 1.0                            # it is NOT 2, and not close
check(4, ok4, m4, 1.0,
      "beta_rt=4/Z=%.6g kappa=%.6g R=%.6g a0=%.4g m/s2 tension=%.2f sigma; "
      "one-leg kappa=%.6g" % (beta_rt, kappa_rt, R_rt, a0_rt, t_rt, kappa_one))

# =====================================================================
# K5 -- candidate (ii) standing wave: Dirichlet ball vs Neumann ball
# =====================================================================
r_s, R_s, k_s = sp.symbols("r R k", positive=True)
j0 = sp.sin(k_s * r_s) / (k_s * r_s)
node_at_wall = sp.simplify(j0.subs(r_s, R_s).subs(k_s, sp.pi / R_s))     # 0
centre = sp.limit(j0.subs(k_s, sp.pi / R_s), r_s, 0)                    # 1
lam_max = 2 * sp.pi / (sp.pi / R_s)                                     # 2R
lam_2 = 2 * sp.pi / (2 * sp.pi / R_s)                                   # R
if BC == "dirichlet":
    lam_over_ell = num(lam_max.subs(R_s, 1))
else:
    lam_over_ell = float("inf")        # Neumann: constant mode, no finite lambda
m5 = abs(lam_over_ell - 2)
ok5 = (m5 == 0) and (node_at_wall == 0) and (centre == 1) and (lam_2.subs(R_s, 1) == 1)
check(5, ok5, m5, 0,
      "BC=%s lambda_max/ell=%.6g (Dirichlet gives exactly 2), overtone lambda/ell=%s"
      % (BC, lam_over_ell, lam_2.subs(R_s, 1)))

# =====================================================================
# K6 -- candidate (ii) surplus: the harmonic tower and its size
# =====================================================================
y = sp.symbols("y", positive=True)          # y := g_N / a0
g_can = (y / 2) * (1 + sp.sqrt(1 + 4 / y))
ratio = [sp.simplify(g_can / sp.sqrt(y)).subs(y, n) for n in (1, 2, 3)]
r1_, r2_, r3_ = [num(x) for x in ratio]
m6 = r1_ - (1 + math.sqrt(5)) / 2
ok6 = abs(m6) < 1e-14 and r1_ > 1.5 and r3_ > 2.0
check(6, ok6, abs(m6), 1e-14,
      "RAR at the tower points a=n*a0: g/deep = %.6f, %.6f, %.6f (excess %.1f%%, %.1f%%, %.1f%%)"
      % (r1_, r2_, r3_, 100 * (r1_ - 1), 100 * (r2_ - 1), 100 * (r3_ - 1)))

# =====================================================================
# K7 -- candidate (iii) natural lengths of the cell ball
# =====================================================================
p = r_s / (2 * R_s ** 2)                                  # chord pdf on [0,2R]
norm = sp.integrate(p, (r_s, 0, 2 * R_s))
mean_chord = sp.integrate(r_s * p, (r_s, 0, 2 * R_s)) / norm
rms_chord = sp.sqrt(sp.integrate(r_s ** 2 * p, (r_s, 0, 2 * R_s)) / norm)
mean_radius = (sp.integrate(r_s * 4 * sp.pi * r_s ** 2, (r_s, 0, R_s))
               / sp.integrate(4 * sp.pi * r_s ** 2, (r_s, 0, R_s)))

nat = {
    "radius": sp.Integer(1),
    "diameter_bulk": sp.Integer(2),
    "mean_chord": sp.simplify(mean_chord / R_s),
    "rms_chord": sp.simplify(rms_chord / R_s),
    "antipodal_arc_boundary": sp.pi,
    "mean_radius_volume": sp.simplify(mean_radius / R_s),
}
nat_f = {kk: num(vv) for kk, vv in nat.items()}
Rs = {kk: vv ** 2 for kk, vv in nat.items()}
Rs_f = {kk: num(vv) for kk, vv in Rs.items()}
distinct_R = len(set(round(v, 12) for v in Rs_f.values()))
n_equal_4 = sum(1 for v in Rs_f.values() if abs(v - 4) < 1e-12)
m7 = abs(norm - 1)
ok7 = (m7 < 1e-14) and distinct_R == 6 and n_equal_4 == 1 \
      and abs(nat_f["mean_chord"] - 4 / 3) < 1e-14 and abs(nat_f["rms_chord"] - math.sqrt(2)) < 1e-14
check(7, ok7, distinct_R, 6,
      "6 natural lengths beta=%s -> R=%s ; exactly %d equals 4"
      % ({k: round(v, 6) for k, v in nat_f.items()},
         {k: round(v, 6) for k, v in Rs_f.items()}, n_equal_4))

# K8 -- candidate (iii): the data do not even single out the diameter
# tensions of every natural length against the measured kappa
nat_tens = {k: tens(1 / v) for k, v in nat_f.items()}
best = sorted(nat_tens.items(), key=lambda kv: abs(kv[1]))[:2]
m7b = abs(nat_tens["antipodal_arc_boundary"])
ok7b = m7b < 2.0            # the boundary arc is NOT excluded at 2 sigma
check(8, ok7b, m7b, 2.0,
      "kappa=1/pi tension=%.2f sigma vs diameter %.2f sigma; within 2 sigma: %s"
      % (m7b, abs(nat_tens["diameter_bulk"]), [k for k, v in nat_tens.items() if abs(v) < 2]))

# =====================================================================
# K9 -- candidate (iii) surplus: where the compact-support edge sits
# =====================================================================
edge = 2 * ell1
edge_over_rH = edge / rH
edge_Gpc = edge / MPC * 1e-3
m9 = abs(edge_over_rH - Z)
ok9 = (m9 < 1e-12) and edge_over_rH > 1
check(9, ok9, edge_over_rH, 1.0,
      "compact-support edge 2ell1 = %.4g m = %.2f Gpc = %.3f r_H (super-horizon)" %
      (edge, edge_Gpc, edge_over_rH))

# =====================================================================
# K10 -- candidate (iv) deep-MOND slope is invariant under a0 -> lambda a0
# =====================================================================
lam_ = sp.symbols("lambda_", positive=True)
GN = sp.symbols("g_N", positive=True)
g_deep = sp.sqrt(A0 * GN)                       # deep limit g = sqrt(a0 gN)
s_a0 = sp.simplify(GN * sp.diff(sp.log(g_deep), GN))                       # 1/2
s_scaled = sp.simplify(GN * sp.diff(sp.log(g_deep.subs(A0, lam_ * A0)), GN))  # still 1/2
amp_shift = sp.simplify(g_deep.subs(A0, lam_ * A0) / g_deep)              # sqrt(lambda)
m10 = max(abs(num(s_a0) - 0.5), abs(num(s_scaled) - 0.5))
R_alt = LAM_SI * (c_SI ** 2 / A0_ALT) ** 2 / (8 * math.pi)
ok10 = (m10 < 1e-14) and abs(R_alt - 2.74103) < 1e-4
check(10, ok10, m10, 1e-14,
      "d ln g/d ln gN = %s and %s after a0->lambda a0 (a0 only rescales g by %s); "
      "two footings both n=2: R=%.6g and %.6g (ratio %.6g)"
      % (s_a0, s_scaled, amp_shift, R_f, R_alt, R_f / R_alt))

# =====================================================================
# K11 -- candidate (iv) counterexample: same n=2, different capacity
# =====================================================================
g_ = sp.symbols("g", positive=True)
gn_can = g_ ** 2 / (g_ + A0)                     # canonical:  gN = g^2/(g+a0)
gn_var = sp.sqrt(g_ ** 2 - A0 * g_)              # variant:    g^2 - gN^2 = a0 gN
c_can = sp.limit(g_ - gn_can, g_, sp.oo)          # saturation offset, canonical
c_var = sp.limit(g_ - gn_var, g_, sp.oo)          # saturation offset, variant
ratio_off = sp.simplify(c_can / c_var)
m11 = abs(num(ratio_off) - 2)
ok11 = (m11 < 1e-14)
check(11, ok11, m11, 1e-14,
      "saturation offset: canonical %s, variant %s, ratio %s -> same n=2, capacity differs by 2"
      % (c_can, sp.simplify(c_var), ratio_off))

# =====================================================================
# K12 -- candidate (v) two cells per correlation volume: cube root, not 2
# =====================================================================
lin = 2 ** sp.Rational(1, 3)
kap_v = 1 / lin
R_v = lin ** 2
t_v = tens(num(kap_v))
m12 = abs(num(lin) - 2)
ok12 = (m12 > 0.5) and (sp.simplify(lin ** 3) == 2)
check(12, ok12, m12, 0.5,
      "2 cells/volume -> linear %.6g (needs 8 cells for 2): kappa=%.6g R=%.6g tension=%.2f sigma"
      % (num(lin), num(kap_v), num(R_v), t_v))

# =====================================================================
# K13 -- the cap family {1,2,4} IS the natural-length family {R,rms,2R}
# =====================================================================
caps_kappa = [sp.Integer(1), 1 / sp.sqrt(2), sp.Rational(1, 2)]
caps_beta = [1 / x for x in caps_kappa]
match = [abs(num(caps_kappa[i] - 1 / caps_beta[i])) for i in range(3)]
nat_match = [abs(nat_f["radius"] - 1), abs(nat_f["rms_chord"] - math.sqrt(2)),
             abs(nat_f["diameter_bulk"] - 2)]
m13 = max(match + nat_match)
ok13 = m13 < 1e-14
check(13, ok13, m13, 1e-14,
      "caps kappa=%s <-> beta=%s <-> lengths {radius, rms chord, diameter}"
      % ([num(x) for x in caps_kappa], [num(x) for x in caps_beta]))

# =====================================================================
# K14 -- c-invariance / unit invariance of beta
# =====================================================================
lamu = sp.symbols("lam_u", positive=True)
beta_units = (lamu * C) ** 2 / (lamu * A0) / sp.sqrt(8 * sp.pi / (LAM / lamu ** 2))
m14 = abs(num(sp.simplify(beta_units) - beta_def))
ok14 = m14 < 1e-14
check(14, ok14, m14, 1e-14,
      "beta invariant under (c,a0,Lambda) -> (lam c, lam a0, Lambda/lam^2): residual %.1e" % m14)

# =====================================================================
# K15 -- the elimination test: every "link" premise IS the answer
# =====================================================================
def elim(expr):
    return sp.simplify(expr.subs({L: L_DEF, ELL: ELL_DEF, KAP: KAP_DEF, R: R_DEF}))

link_diam = elim(L - 2 * ELL)          # "L is the cell diameter"
link_wave = elim(L - 2 * ELL)          # "L is the longest standing wave"
link_two = elim(L - 2 ** sp.Rational(1, 3) * ELL)
link_rad = elim(L - ELL)
taut = sp.simplify((L - 2 * ELL).subs(L, 2 * ELL))       # defining L := 2 ell makes it 0

def mentions_a0(e):
    return e.has(A0) and sp.simplify(e) != 0

n_inserted = sum(mentions_a0(e) for e in (link_diam, link_wave, link_two, link_rad))
m15 = abs(taut)
ok15 = (m15 == 0) and n_inserted == 4
check(15, ok15, n_inserted, 4,
      "defining L:=2ell makes the conclusion identically %s; eliminating the abbreviations from "
      "each link leaves a nontrivial a0 equation: %d/4 (the value of beta enters only through the "
      "link)" % (taut, n_inserted))

# =====================================================================
# K16 -- no-go ledger: no candidate's image is {2}
# =====================================================================
images = {
    "i_round_trip": [beta_one, beta_rt],
    "ii_standing_wave": [2.0, float("inf")],
    "iii_natural_lengths": sorted(nat_f.values()),
    "iv_deep_slope": [],
    "v_two_cells": [num(lin), 2.0],
}
single_two = [k for k, v in images.items() if len(v) == 1 and abs(v[0] - 2) < 1e-12]
sizes = [len(v) for v in images.values() if v]
m16 = len(single_two)
ok16 = (m16 == 0) and min(sizes) >= 2
check(16, ok16, m16, 0,
      "image sizes %s; candidates whose premise class returns exactly {2}: %d"
      % ({k: len(v) for k, v in images.items()}, m16))

# =====================================================================
npass = sum(1 for r in RESULTS if r["pass"])
ntot = len(RESULTS)
print()
print("%s COMPLETE: %d/%d checks PASS." % (LANE, npass, ntot))

# ---------------------------------------------------------------- results
numbers = {
    "Lambda": LAM_SI, "c": c_SI, "a0_can": A0_SI, "a0_alt": A0_ALT,
    "ell1_m": ell1, "L_m": Lmond, "two_ell1_m": L_req, "a0_from_2ell1": a0_req,
    "beta_footing": beta_f, "kappa_footing": kappa_f, "R_footing": R_f,
    "r_H_m": rH, "Z": Z, "R_at_2ell1": R_req,
    "beta_roundtrip_horizon": beta_rt, "kappa_roundtrip": kappa_rt,
    "R_roundtrip": R_rt, "a0_roundtrip": a0_rt, "tension_roundtrip_sigma": t_rt,
    "beta_one_leg": beta_one, "kappa_one_leg": kappa_one,
    "lambda_dirichlet_over_ell": 2.0 if BC == "dirichlet" else None,
    "lambda_overtone_over_ell": 1.0,
    "rar_ratio_n1": r1_, "rar_ratio_n2": r2_, "rar_ratio_n3": r3_,
    "rar_excess_pct": [100 * (r1_ - 1), 100 * (r2_ - 1), 100 * (r3_ - 1)],
    "kappa_roundtrip_over_canonical": kappa_rt / 0.5,
    "n_checks": ntot,
    "natural_lengths_beta": nat_f, "R_from_natural_lengths": Rs_f,
    "distinct_R_natural": distinct_R, "n_natural_R_equal_4": n_equal_4,
    "tension_natural_lengths_sigma": nat_tens,
    "tension_sigma_abs": {k: abs(v) for k, v in nat_tens.items()},
    "kappa_from_natural_lengths": {k: 1 / v for k, v in nat_f.items()},
    "n_cells_for_linear_two": 8,
    "R_target_over_R_unruh": 4 / (3 / (8 * math.pi)),
    "sigma_kappa_hypothetical": 0.005,
    "edge_2ell1_m": edge, "edge_Gpc": edge_Gpc, "edge_over_r_H": edge_over_rH,
    "deep_slope": 0.5, "R_alt_footing": R_alt, "R_ratio_two_footings": R_f / R_alt,
    "offset_ratio_canonical_variant": num(ratio_off),
    "two_cells_linear": num(lin), "kappa_two_cells": num(kap_v),
    "R_two_cells": num(R_v), "tension_two_cells_sigma": t_v,
    "kappa_caps": [num(x) for x in caps_kappa], "beta_caps": [num(x) for x in caps_beta],
    "image_sizes": {k: len(v) for k, v in images.items()},
    "n_candidates_image_is_2": m16,
    "kappa_meas": KAPPA_MEAS, "kappa_sigma": KAPPA_SIG,
    "sigma_kappa_1pct_sep_R4_vs_R2": (1 / math.sqrt(2) - 0.5) / 0.005,
    "sigma_kappa_1pct_sep_R4_vs_R1": 0.5 / 0.005,
    "sigma_kappa_1pct_sep_R4_vs_arc": (0.5 - 1 / math.pi) / 0.005,
}
out = {
    "lane": LANE,
    "status": "NO-GO(obstruction)",
    "checks": RESULTS,
    "numbers": numbers,
    "constants_used": [
        "c=2.99792458e8 m/s (BRIEF s4)", "G=6.67430e-11 (BRIEF s4)",
        "Lambda=1.0890e-52 m^-2 (BRIEF s4)", "a0_can=9.36e-11 m/s2 (BRIEF s4)",
        "a0_alt=1.13e-10 m/s2 (BRIEF s4)", "Mpc=3.0856775814913673e22 m (BRIEF s4)",
        "kappa_meas=0.417+-0.095 (CFG493, via A19/a15 report; external measurement)",
    ],
}
suffix = ("_" + "_".join(sorted(MUT))) if MUT else ""
with open("a27_results%s.json" % suffix, "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)
sys.exit(0 if npass == ntot else 1)