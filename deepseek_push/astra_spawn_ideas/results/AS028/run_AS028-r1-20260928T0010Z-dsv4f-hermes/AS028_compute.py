#!/usr/bin/env python3
"""
AS028 - RAR deep expansion with stable evaluation.

nu_RAR(y) = 1/(1 - exp(-sqrt(y))),  s = sqrt(y) = sqrt(B/a0),  g = a0 * y * nu(y).

Deliverables computed here (all real, reproducible):
  (1) Formal power-series coefficients of nu(y) = s^{-1} * Q(s), Q = exact rational
      formal reciprocal of P(s) = (1 - exp(-s))/s (Fraction arithmetic).
  (2) Naive float 1/(1 - exp(-s)) vs stable -1/expm1(-s) vs 60-term series vs a
      70-digit Decimal reference over y = 10^k, k in [-16, 8], step 0.1 (241 pts;
      the mandated diagnostic grid k in [-10, 8] is a subset), plus the deep tail.
  (3) Negative control A: the naive form must FAIL a 1e-14 relative-accuracy bar in
      the deep regime (catastrophic cancellation); the stable form must pass at all
      points.
  (4) Negative control B / limiting regimes: y -> inf (nu -> 1) and y -> 0+
      (sqrt(y) nu -> 1 + sqrt(y)/2 + O(y)), with observed residuals and the
      leading-correction scale stated.
  (5) Independent representation: substitution into the defining relation
      (1 - exp(-s)) * nu_series = 1 within the radius.
  (6) Series radius: converges for y < 4 pi^2; 60th-term decay probe near the
      boundary and divergence beyond (domain statement, not a proof of convergence).
  (7) MONO splice comparison at the operative landmarks (y* = 2.337412,
      y_p = 2.53964, h_p = 0.647610, delta = 0.05): h_RAR(y) = y*(nu-1),
      h_mono(y) = h_RAR(y*) + delta*h_p*ln((y+y_p)/(y*+y_p)) for y > y*, else h_RAR;
      nu_mono = 1 + h_mono/y. Landmarks independently re-derived by bisection.
  (8) Dimensional examples on BOTH footings (a0 = 9.3619e-11 and 1.1279e-10 m/s^2):
      rho_Lambda = 4 a0^2/(G c^2), g = a0*y*nu(y), r_M, v_flat (M_b = 1e11 M_sun).
      kappa = 1/2 adopted input.

Bounds are ENFORCED in-script: wall <= 120 s (exit 66), RSS <= 512 MB (exit 67),
single-threaded by construction.
"""
import sys, os, json, math, time, resource
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 70
T_START = time.monotonic()
WALL_BUDGET = 120.0
MEM_BUDGET_MB = 512.0

def enforce_bounds():
    if time.monotonic() - T_START > WALL_BUDGET:
        print("WALL_BUDGET_EXCEEDED", file=sys.stderr)
        sys.exit(66)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_mb = rss / (1024.0 * 1024.0) if sys.platform == "darwin" else rss / 1024.0
    if rss_mb > MEM_BUDGET_MB:
        print("MEM_BUDGET_EXCEEDED", file=sys.stderr)
        sys.exit(67)

G = 6.67430e-11          # m^3 kg^-1 s^-2 (SI, framework convention)
C_LIGHT = 299792458.0    # m/s
A0_CANON = 9.3619e-11    # m/s^2 canonical footing
A0_ALT = 1.1279e-10      # m/s^2 alternative footing
M_SUN = 1.98847e30       # kg
PC_M = 3.085677581491367e16  # m

# ---------------------------------------------------------------- exact series
def formal_reciprocal(N):
    """P(s) = sum (-1)^k/(k+1)! s^k ; exact Q with P*Q = 1 + O(s^{N+1})."""
    P = [Fraction((-1) ** k, math.factorial(k + 1)) for k in range(N + 1)]
    Q = [Fraction(0)] * (N + 1)
    Q[0] = Fraction(1)
    for n in range(1, N + 1):
        Q[n] = -sum(P[k] * Q[n - k] for k in range(1, n + 1))
    return P, Q

N_COEF = 121   # indices 0..120 (120-term partial sums used for the series checks)
P, Q = formal_reciprocal(N_COEF)
assert Q[0] == 1 and Q[1] == Fraction(1, 2) and Q[2] == Fraction(1, 12)
assert Q[3] == 0 and Q[4] == Fraction(-1, 720) and Q[5] == 0 and Q[6] == Fraction(1, 30240), \
    [str(q) for q in Q[:7]]

def Qdec(k):
    f = Q[k]
    return Decimal(f.numerator) / Decimal(f.denominator)

# ---------------------------------------------------------------- evaluators
def nu_naive(y):
    s = math.sqrt(y)
    return 1.0 / (1.0 - math.exp(-s))

def nu_stable(y):
    s = math.sqrt(y)
    return -1.0 / math.expm1(-s)

def nu_series_terms(y, M):
    s = Decimal(y).sqrt()
    acc = Decimal(0)
    sk = Decimal(1)
    for k in range(M + 1):
        acc += Qdec(k) * sk
        sk *= s
    return acc / s

def nu_ref(y):
    s = Decimal(y).sqrt()
    return Decimal(1) / (Decimal(1) - (-s).exp())

def rel_err(x, ref):
    return abs(Decimal(x) - ref) / ref

# ---------------------------------------------------------------- grid
ks = [k / 10.0 for k in range(-160, 81)]   # k/10 = -16.0 .. 8.0 step 0.1 -> 241 pts
grid_y = [10.0 ** k for k in ks]
RHO_SERIES = 4.0 * math.pi ** 2             # 39.4784... = (2 pi)^2

max_err_naive_all = Decimal(0); max_err_stable_all = Decimal(0)
max_err_naive_deep = Decimal(0); max_err_stable_deep = Decimal(0)
naive_fail_bar_y = []
MAXERR_SERIES_Y_LE_10 = Decimal(0)        # accuracy claim domain
MAXERR_SERIES_NEAR_RADIUS = Decimal(0)    # diagnostic: degradation toward 4 pi^2
SERIES_TERMS = 120

for y in grid_y:
    r = nu_ref(y)
    e_n = rel_err(nu_naive(y), r)
    e_s = rel_err(nu_stable(y), r)
    max_err_naive_all = max(max_err_naive_all, e_n)
    max_err_stable_all = max(max_err_stable_all, e_s)
    if y <= 1e-4:
        max_err_naive_deep = max(max_err_naive_deep, e_n)
        max_err_stable_deep = max(max_err_stable_deep, e_s)
    if e_n > Decimal("1e-14"):
        naive_fail_bar_y.append((y, float(e_n)))
    if y < RHO_SERIES:
        sv = nu_series_terms(y, SERIES_TERMS)
        es = rel_err(float(sv), r)
        if y <= 10.0:
            MAXERR_SERIES_Y_LE_10 = max(MAXERR_SERIES_Y_LE_10, es)
        if y < RHO_SERIES * 0.97:
            MAXERR_SERIES_NEAR_RADIUS = max(MAXERR_SERIES_NEAR_RADIUS, es)
    enforce_bounds()

detail_rows = [{"y": 10.0 ** k, "naive": float(nu_naive(10.0 ** k)), "stable": float(nu_stable(10.0 ** k)),
                "ref_30dig": str(nu_ref(10.0 ** k)),
                "err_naive": float(rel_err(nu_naive(10.0 ** k), nu_ref(10.0 ** k))),
                "err_stable": float(rel_err(nu_stable(10.0 ** k), nu_ref(10.0 ** k)))}
               for k in range(-16, 9)]

tail_y = [10.0 ** k for k in [-16, -15.5, -15, -14.5, -14, -13, -12, -11, -10.5, -10.25, -10.1]]
tail_rows = []
for y in tail_y:
    r = nu_ref(y)
    e_n = rel_err(nu_naive(y), r)
    e_s = rel_err(nu_stable(y), r)
    tail_rows.append({"y": y, "err_naive": float(e_n), "err_stable": float(e_s),
                      "ratio_naive_over_stable": float(e_n / e_s)})
    enforce_bounds()

# ---------------------------------------------------------------- series radius probes
def termN_abs(y, N=120):
    """|Q_N| * s^N (Decimal) at y: decay probe for the radius statement."""
    s = Decimal(y).sqrt()
    return abs(Qdec(N)) * s ** N

series_probe_rows = []
for y in [1e-4, 1.0, 10.0, 19.73, 30.0, 35.0, 39.0, 39.4, 39.478, 40.0, 50.0]:
    r = nu_ref(y)
    inside = y < RHO_SERIES
    es = float(rel_err(float(nu_series_terms(y, SERIES_TERMS)), r)) if inside else None
    series_probe_rows.append({"y": y, "inside_radius": inside,
                              "series120_rel_err": es, "term120_abs": float(termN_abs(y, 120)),
                              "nu_ref_head": str(r)[:22]})
    enforce_bounds()

# ---------------------------------------------------------------- limits
lim_newton_resid = rel_err(1.0, nu_ref(1e4))                 # ~ e^{-100}
y0 = 1e-16
s0 = math.sqrt(y0)
lim_deep_resid = rel_err(1.0 / s0, nu_ref(y0))               # first correction ~ s/2
lim_deep_next = rel_err(1.0 / s0 + 0.5, nu_ref(y0))          # next correction ~ s/12

# ---------------------------------------------------------------- defining-relation substitution check
sub_rows = []
for y in [1e-16, 1e-12, 1e-8, 1e-4, 1e-2, 1.0, 2.337412, 2.53964, 10.0, 30.0, 39.0]:
    sv = nu_series_terms(y, SERIES_TERMS)
    sd = Decimal(y).sqrt()
    back = (Decimal(1) - (-sd).exp()) * sv - Decimal(1)
    sub_rows.append({"y": y, "defining_relation_residual": float(back),
                     "series_vs_ref_relerr": float(rel_err(float(sv), nu_ref(y)))})
    enforce_bounds()

# ---------------------------------------------------------------- MONO splice
def h_RAR(y):
    s = math.sqrt(y)
    return y * (1.0 / (1.0 - math.exp(-s)) - 1.0)

def h_RAR_prime(y):
    s = math.sqrt(y)
    e = math.exp(-s)
    nu = 1.0 / (1.0 - e)
    return nu - 1.0 - y * e / (2.0 * s * (1.0 - e) ** 2)

def bisect(f, a, b, iters=200):
    fa, fb = f(a), f(b)
    assert fa * fb < 0, (a, b, fa, fb)
    for _ in range(iters):
        m = 0.5 * (a + b)
        fm = f(m)
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b)

y_p_ref = bisect(h_RAR_prime, 2.3, 2.8)
h_p_ref = h_RAR(y_p_ref)
DELTA = 0.05
y_star_ref = bisect(lambda y: h_RAR_prime(y) - DELTA * h_p_ref / (y + y_p_ref), 2.2, y_p_ref)

YSTAR_Q, YP_Q, HP_Q = 2.337412, 2.53964, 0.647610   # quoted operative landmarks

def nu_mono_D(y, ystar=Decimal(YSTAR_Q), yp=Decimal(YP_Q), hp=Decimal(HP_Q), delta=Decimal("0.05")):
    yd = Decimal(y)
    if yd <= ystar:
        return nu_ref(y)
    s = ystar.sqrt()
    hstar = ystar * (Decimal(1) / (Decimal(1) - (-s).exp()) - Decimal(1))
    h = hstar + delta * hp * ((yd + yp) / (ystar + yp)).ln()
    return Decimal(1) + h / yd

splice_y = [YSTAR_Q / 2, YSTAR_Q, (YSTAR_Q + YP_Q) / 2, YP_Q, 3.0, 4.0, 6.0, 10.0, 1e2, 1e4]
splice_rows = []
for y in splice_y:
    yd = Decimal(y)
    r = nu_ref(y)
    m = nu_mono_D(y)
    splice_rows.append({"y": y, "nu_RAR": str(r)[:26], "nu_MONO": str(m)[:26],
                        "Delta_nu_abs": float(abs(m - r)),
                        "Delta_nu_rel": float(abs(m - r) / r),
                        "h_RAR": format(float(yd * (r - 1)), ".12e"),
                        "h_MONO": format(float(yd * (m - 1)), ".12e"),
                        "Delta_g_in_a0": float(yd * (m - r))})
    enforce_bounds()

ymax = max((y for y in [YSTAR_Q + 0.013 * i for i in range(0, 300)]),
           key=lambda y: abs(nu_mono_D(y) - nu_ref(y)))
max_delta_splice = float(abs(nu_mono_D(ymax) - nu_ref(ymax)))

land_checks = {
    "y_star_quoted_vs_recomputed": [YSTAR_Q, y_star_ref, abs(YSTAR_Q - y_star_ref)],
    "y_p_quoted_vs_recomputed": [YP_Q, y_p_ref, abs(YP_Q - y_p_ref)],
    "h_p_quoted_vs_recomputed": [HP_Q, h_p_ref, abs(HP_Q - h_p_ref)],
    "splice_condition_residual_h'_RAR(y*) - delta*h_p/(y*+y_p)": float(
        h_RAR_prime(y_star_ref) - DELTA * h_p_ref / (y_star_ref + y_p_ref)),
    "h_mono_continuous_at_y* (log term = 0)": float(abs(nu_mono_D(YSTAR_Q) - nu_ref(YSTAR_Q))),
}

# ---------------------------------------------------------------- dimensional footings
def footing(a0, tag):
    rho_L = 4.0 * a0 * a0 / (G * C_LIGHT ** 2)
    eps_L = rho_L * C_LIGHT ** 2
    Lam = 32.0 * math.pi * a0 * a0 / C_LIGHT ** 4
    Mb = 1e11 * M_SUN
    rM_kpc = math.sqrt(G * Mb / a0) / PC_M
    vflat = (G * Mb * a0) ** 0.25 / 1e3
    gs = {str(y): a0 * y * float(nu_ref(y)) for y in [1e-6, 1.0, 1e2, 1e4]}
    return {"footing": tag, "a0_m_s2": a0, "rho_Lambda_kg_m3": rho_L,
            "eps_Lambda_J_m3": eps_L, "Lambda_m2": Lam,
            "r_M_kpc_1e11Msun": rM_kpc, "v_flat_km_s_1e11Msun": vflat,
            "g_m_s2_at_y": gs}

F1 = footing(A0_CANON, "canonical")
F2 = footing(A0_ALT, "alternative")
footing_cross = {
    "a0_ratio_alt_over_can": A0_ALT / A0_CANON,
    "rho_Lambda_ratio_alt_over_can": F2["rho_Lambda_kg_m3"] / F1["rho_Lambda_kg_m3"],
    "note": ("same adopted kappa = 1/2, same G, c: rho_Lambda scales as a0^2 so the ratio is "
             "(a0_alt/a0_can)^2 = 1.4511; the dimensionless nu(y) curve is identical on both "
             "footings; dimensional g = a0*y*nu(y) scales by a0")}

# ---------------------------------------------------------------- checks
checks = [
    {"name": "C1_naive_cancellation_negative_control",
     "tolerance": ("naive relative error > 1e-14 in the deep regime (control capable of failing); "
                   "stable form <= 1e-14 at every grid point"),
     "observed": {"max_err_naive_all": float(max_err_naive_all),
                  "max_err_naive_deep_y_le_1e-4": float(max_err_naive_deep),
                  "max_err_stable_all": float(max_err_stable_all),
                  "max_err_stable_deep_y_le_1e-4": float(max_err_stable_deep),
                  "n_naive_fail_points": len(naive_fail_bar_y),
                  "first_naive_fail": naive_fail_bar_y[:6]},
     "pass": float(max_err_naive_all) > 1e-14 and float(max_err_stable_all) <= 1e-14},
    {"name": "C2_series_accuracy_on_claim_domain",
     "tolerance": ("120-term series vs 70-digit reference: rel err <= 1e-14 for y <= 10 "
                   "(the deep+intermediate domain where the series is the practical evaluator); "
                   "degradation toward y = 4 pi^2 is reported as a diagnostic"),
     "observed": {"max_rel_err_y_le_10": float(MAXERR_SERIES_Y_LE_10),
                  "max_rel_err_y_lt_0.97_radius_diagnostic": float(MAXERR_SERIES_NEAR_RADIUS),
                  "series_terms": SERIES_TERMS, "radius_y": RHO_SERIES},
     "pass": float(MAXERR_SERIES_Y_LE_10) <= 1e-14},
    {"name": "C3_series_radius_boundary_probe",
     "tolerance": ("error degrades near y = 4 pi^2 (series120 rel err at y=39.4 > 1e-3) and the 120th "
                   "series term fails to decay at the radius (|Q120|*(2 pi)^120 >= 0.5); beyond the "
                   "radius the partial sums are not evaluated"),
     "observed": {"probes": series_probe_rows},
     "pass": (float(series_probe_rows[8]["term120_abs"]) >= 0.5) and
             (float(series_probe_rows[7]["series120_rel_err"]) > 1e-3)},
    {"name": "C4_newtonian_and_deep_limiting_regimes",
     "tolerance": ("nu(1e4) - 1 ~ e^{-100} (resid to 1 < 1e-30); sqrt(y)*nu(y) = 1 + sqrt(y)/2 + O(y) "
                   "(resid to 1/s < 1e-7 at y=1e-16; resid to 1/s + 1/2 < 1e-6)"),
     "observed": {"y=1e4_rel_resid_to_1": float(lim_newton_resid),
                  "y=1e-16_rel_resid_to_1_over_s": float(lim_deep_resid),
                  "y=1e-16_rel_resid_to_1_over_s_plus_1over2": float(lim_deep_next)},
     "pass": float(lim_newton_resid) < 1e-30 and float(lim_deep_resid) < 1e-7 and float(lim_deep_next) < 1e-6},
    {"name": "C5_series_substitution_into_defining_relation",
     "tolerance": ("|(1 - exp(-s)) * nu_series - 1| <= 1e-30 for y <= 10 (independent representation "
                   "inside the accurate region); rows beyond 10 are diagnostics of near-radius degradation"),
     "observed": sub_rows,
     "pass": all(abs(r["defining_relation_residual"]) <= 1e-30 for r in sub_rows if r["y"] <= 10.0)},
    {"name": "C6_mono_splice_landmarks",
     "tolerance": "|recomputed - quoted|: y* <= 1e-6, y_p <= 1e-5, h_p <= 1e-6; splice residual |h'_RAR(y*) - delta h_p/(y*+y_p)| <= 1e-9",
     "observed": land_checks,
     "pass": (abs(YSTAR_Q - y_star_ref) <= 1e-6 and abs(YP_Q - y_p_ref) <= 1e-5 and
             abs(HP_Q - h_p_ref) <= 1e-6 and land_checks["splice_condition_residual_h'_RAR(y*) - delta*h_p/(y*+y_p)"] <= 1e-9)},
    {"name": "C7_mono_vs_RAR_branch_distinction",
     "tolerance": ("nu_MONO = nu_RAR for y <= y* (continuity), Delta nu > 1e-6 on (y*, 1e4]; "
                   "both share the Newtonian asymptote nu -> 1 but with different approach rates "
                   "(e^{-sqrt y} vs O(log y / y)): matching asymptote does not identify the branch"),
     "observed": {"splice_neighbourhood_max_Delta_nu": max_delta_splice,
                  "Delta_nu_abs_at_y": [{"y": r["y"], "Delta_nu_abs": r["Delta_nu_abs"]} for r in splice_rows]},
     "pass": land_checks["h_mono_continuous_at_y* (log term = 0)"] <= 1e-30 and max_delta_splice > 1e-6},
]

mem_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
mem_mb = mem_mb / (1024.0 * 1024.0) if sys.platform == "darwin" else mem_mb / 1024.0

out = {
    "task": "AS028 RAR deep expansion with stable evaluation",
    "series_coefficients_Q_exact_first_12": {str(k): str(Q[k]) for k in range(0, 12)},
    "deep_terms": {"s^-1": "1/sqrt(y)", "s^0": "1/2", "s^1": "sqrt(y)/12",
                   "s^3": "-y^(3/2)/720", "s^5": "+y^(5/2)/30240"},
    "leading_neglected_term_after_s^5": ("-Q8*s^7 = -s^7/1209600 = -y^(7/2)/1209600 absolute; "
                                         "relative to leading term 1/s: -s^8/1209600 = -y^4/1209600"),
    "radius_of_convergence": "|s| < 2 pi  <=>  y < 4 pi^2 = %.15g" % RHO_SERIES,
    "grid": {"k_range": [-16, 8], "step": 0.1, "n_points": len(grid_y),
             "y_range": [grid_y[0], grid_y[-1]], "spec_grid_k_-10..8_is_subset": True},
    "accuracy": {"max_err_naive_all": float(max_err_naive_all),
                 "max_err_stable_all": float(max_err_stable_all),
                 "max_err_naive_deep_y_le_1e-4": float(max_err_naive_deep),
                 "max_err_stable_deep_y_le_1e-4": float(max_err_stable_deep),
                 "max_series120_rel_err_y_le_10": float(MAXERR_SERIES_Y_LE_10),
                 "max_series120_rel_err_y_lt_0.97_radius_diagnostic": float(MAXERR_SERIES_NEAR_RADIUS),
                 "naive_fail_points": naive_fail_bar_y},
    "detail_rows": detail_rows,
    "deep_tail_rows": tail_rows,
    "series_probe_rows": series_probe_rows,
    "series_substitution": sub_rows,
    "limiting_regimes": {"y_newton": 1e4, "resid_nu_to_1": float(lim_newton_resid),
                         "y_deep": y0, "resid_sqrt_y_nu_to_1": float(lim_deep_resid),
                         "resid_sqrt_y_nu_to_1_plus_s_over_2": float(lim_deep_next)},
    "mono_splice": {"quoted": {"y_star": YSTAR_Q, "y_p": YP_Q, "h_p": HP_Q, "delta": DELTA},
                    "recomputed": {"y_star": y_star_ref, "y_p": y_p_ref, "h_p": h_p_ref},
                    "landmark_checks": land_checks,
                    "neighbourhood_max_Delta_nu_at_y": (ymax, max_delta_splice),
                    "table": splice_rows},
    "footings": [F1, F2],
    "footing_cross_statement": footing_cross,
    "checks": checks,
    "bounds": {"wall_s": round(time.monotonic() - T_START, 3), "budget_wall_s": WALL_BUDGET,
               "rss_mb": round(mem_mb, 2), "budget_rss_mb": MEM_BUDGET_MB, "threads": 1,
               "threads_note": "single-threaded by construction (no Thread/Process/OpenMP usage)"},
    "config": {"G": G, "c": C_LIGHT, "M_sun": M_SUN, "kappa": "1/2 adopted input",
               "decimal_precision": getcontext().prec},
}

with open("raw_output.json", "w") as f:
    json.dump(out, f, indent=1)

print(json.dumps({"summary": {
    "max_err_naive_all": float(max_err_naive_all), "max_err_naive_deep": float(max_err_naive_deep),
    "max_err_stable_all": float(max_err_stable_all), "max_err_stable_deep": float(max_err_stable_deep),
    "n_naive_fail_points": len(naive_fail_bar_y),
    "series_max_err_y_le_10": float(MAXERR_SERIES_Y_LE_10),
    "y_star": y_star_ref, "y_p": y_p_ref, "h_p": h_p_ref,
    "splice_max_Delta_nu": max_delta_splice,
    "all_checks_pass": all(c["pass"] for c in checks),
    "wall_s": round(time.monotonic() - T_START, 3), "rss_mb": round(mem_mb, 2)}}, indent=1))
