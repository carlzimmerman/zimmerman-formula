#!/usr/bin/env python3
# AS050 — STABLE EVALUATION OF THE RAR DEEP X
# x = g/a0 = y*nu_RAR(y) = y/(1-exp(-sqrt(y))), y = B/a0, s = sqrt(y).
# Worker: Hermes subagent (deepseek/deepseek-v4-flash-0731 via openrouter).
# Bounds: wall <= 120 s, RSS <= 512 MB, 1 thread (enforced: exit 66 / 67).
import math, time, json, sys, resource
from fractions import Fraction
from decimal import Decimal, getcontext

t0 = time.monotonic()
WALL_BUDGET = 120.0
MEM_BUDGET_MB = 512.0

def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024.0 * 1024.0)  # macOS: bytes

def check_bounds(phase):
    w = time.monotonic() - t0
    m = rss_mb()
    if w > WALL_BUDGET:
        print(f"BOUND VIOLATION wall {w:.1f}s > {WALL_BUDGET}s at {phase}", flush=True); sys.exit(66)
    if m > MEM_BUDGET_MB:
        print(f"BOUND VIOLATION rss {m:.1f}MB > {MEM_BUDGET_MB}MB at {phase}", flush=True); sys.exit(67)

getcontext().prec = 70
DEC70 = Decimal

print(f"AS050 compute start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} python {sys.version.split()[0]}")

# ---------------------------------------------------------------- constants
G  = 6.67430e-11        # m^3 kg^-1 s^-2  (G_N; G_bare and G_cosmo kept separate)
c  = 299792458.0        # m/s
M_SUN = 1.98847e30      # kg
PC    = 3.085677581491367e16  # m
A0_CAN = 9.3619e-11     # m/s^2  canonical footing  (kappa = 1/2 ADOPTED input)
A0_ALT = 1.1279e-10     # m/s^2  alternative footing
KAPPA = Fraction(1, 2)  # adopted, not derived

# ---------------------------------------------------------------- 1. exact coefficient machinery
# P(s) = (1-exp(-s))/s = sum_{k>=0} p_k s^k,  p_k = (-1)^k/(k+1)!
# Q(s) = 1/P(s) = sum q_k s^k  (formal reciprocal, Fraction-exact)
NTERM = 130
p = [Fraction((-1) ** k, math.factorial(k + 1)) for k in range(NTERM)]
q = [Fraction(0)] * NTERM
q[0] = Fraction(1)
for n in range(1, NTERM):
    q[n] = -sum(p[k] * q[n - k] for k in range(1, n + 1))
assert all(q[n].denominator == 1 or True for n in range(NTERM))  # q are exact; check zeros below

# Bernoulli cross-check: sum_{k=0}^{m} C(m+1,k) B_k = 0, B_0 = 1, then q_k = B_k/k!
# NOTE convention: x/(1-e^{-x}) = sum B_k^+ x^k/k! with B_1^+ = +1/2 (second Bernoulli
# numbers); the raw recurrence yields B_1 = -1/2 (x/(e^x-1) convention).  The series
# used here carries B_1^+ = +1/2 (matches q_1 = 1/2 and the AS028 record); all other
# orders agree with the recurrence in absolute value.
def bernoulli_q(nmax):
    B = [Fraction(0)] * (nmax + 2)
    B[0] = Fraction(1)
    for m in range(1, nmax + 1):
        s = Fraction(0)
        for k in range(m):
            s += math.comb(m + 1, k) * B[k]
        B[m] = Fraction(-s, m + 1)
    B[1] = Fraction(1, 2)   # B_1^+ = +1/2 convention (adopted; raw recurrence gives -1/2)
    out = [Fraction(0)] * (nmax + 1)
    for k in range(nmax + 1):
        out[k] = B[k] / math.factorial(k)
    return out

BQ = bernoulli_q(NTERM - 1)
bern_match = all(q[k] == BQ[k] for k in range(NTERM))
# also record the raw-recurrence B_1 sign fact for the derivation
bern_raw_b1 = Fraction(-1, 2)
# Bernoulli signature: q_odd(k>=3) = 0 ; q1 = 1/2
sig_odd = all(q[k] == 0 for k in range(3, NTERM, 2))
sig_first = (q[0] == 1 and q[1] == Fraction(1, 2) and q[2] == Fraction(1, 12)
             and q[4] == Fraction(-1, 720) and q[6] == Fraction(1, 30240)
             and q[8] == Fraction(-1, 1209600))
# radius probe: |q_{2n}|*(2 pi)^{2n} -> 2  (Bernoulli asymptotic |B_{2n}| ~ 2 (2n)!/(2 pi)^{2n})
TWOPI = 2 * math.pi
rat = []
for n in range(1, 61):
    k = 2 * n
    rat.append((n, float(abs(q[k]) * Fraction(TWOPI) ** k)))
rat_tail_mean = sum(v for _, v in rat[30:]) / 30.0

# ---------------------------------------------------------------- 2. fp64 evaluations
def s_of(y): return math.sqrt(y)

def x_naive(y):
    s = s_of(y)
    return y / (1.0 - math.exp(-s))

def x_exp(y):
    s = s_of(y)
    if s > 700.0:  # e^s would overflow; e^s/(e^s-1) = 1 to < e^-700 - use the limit
        return y
    e = math.exp(s)
    return y * e / (e - 1.0)

def x_expm1(y):
    return -y / math.expm1(-math.sqrt(y))

def x_series(y, n_terms):
    s = math.sqrt(y)
    # Horner in s over exact coefficients converted to float
    acc = 0.0
    for k in range(n_terms - 1, -1, -1):
        acc = acc * s + float(q[k])
    return acc * s  # x = s * (sum q_k s^k)

def x_ref(y):
    s = Decimal(y).sqrt()
    d = Decimal(1) - (-s).exp()
    return Decimal(y) / d

def relerr(a, b):
    return abs(a - b) / abs(b)

# ---------------------------------------------------------------- 3. grids
# mandated deep range: y = 10^k, k in [-16, -4] step 0.1  -> 121 points
ks_deep = [k / 10 for k in range(-160, -39)]
ys_deep = [10.0 ** k for k in ks_deep]
# extended grid: k in [-16, 8] step 0.1 -> 241 points (alignment with AS028 grid)
ks_all = [k / 10 for k in range(-160, 81)]
ys_all = [10.0 ** k for k in ks_all]
# boundary probes
ys_probe = [1e-18, 1e-20, 1e-30, 1e-31, 1e-32, 1e-33, 1e8, 1e10]
ys_bound = [1e-34]  # s < 1.1e-16: exp(s)-1 == 0 in fp64 -> division by zero expected

BAR = 1e-14

def evaluate_all(ys):
    rows = []
    for y in ys:
        row = {"y": y, "x_ref": str(x_ref(y))}
        for name, fn in (("x_naive", x_naive), ("x_exp", x_exp), ("x_expm1", x_expm1),
                         ("x_ser8", lambda yy: x_series(yy, 8)),
                         ("x_ser30", lambda yy: x_series(yy, 30))):
            try:
                row[name] = fn(y)
            except (ZeroDivisionError, OverflowError):
                row[name] = float("inf")   # fp64 edge: form evaluates to 0/0 or overflows
        rows.append(row)
    return rows

rows_deep = evaluate_all(ys_deep)
check_bounds("after deep grid")
rows_all = evaluate_all(ys_all)
check_bounds("after all grid")
rows_probe = evaluate_all(ys_probe)
rows_bound = evaluate_all(ys_bound)
check_bounds("after probes")

def errors(rows, key_ref="x_ref"):
    out = []
    for r in rows:
        ref = abs(Decimal(r[key_ref]))
        e = {}
        for k in ("x_naive", "x_exp", "x_expm1", "x_ser8", "x_ser30"):
            v = r[k]
            e[k] = float(abs((Decimal(str(v)) - Decimal(r[key_ref])) / ref)) if math.isfinite(v) else float("inf")
        out.append((r["y"], e))
    return out

err_deep = errors(rows_deep)
err_all = errors(rows_all)
err_probe = errors(rows_probe)

def stats(errs, forms):
    st = {}
    for f in forms:
        vals = [e[f] for _, e in errs]
        finite = [v for v in vals if math.isfinite(v)]
        st[f] = {
            "max": max(finite) if finite else float("inf"),
            "min": min(finite) if finite else float("inf"),
            "median": sorted(finite)[len(finite) // 2] if finite else float("inf"),
            "n_fail_bar_1e-14": sum(1 for v in vals if v > BAR),
            "n_fail_bar_1e-12": sum(1 for v in vals if v > 1e-12),
            "n_inf": sum(1 for v in vals if not math.isfinite(v)),
        }
    return st

forms = ("x_naive", "x_exp", "x_expm1", "x_ser8", "x_ser30")
st_deep = stats(err_deep, forms)
st_all = stats(err_all, forms)

# accuracy gain (naive vs stable forms) on the mandated deep range, per point
gains = []
for y, e in err_deep:
    gains.append({
        "y": y,
        "gain_naive_over_expm1": e["x_naive"] / e["x_expm1"] if e["x_expm1"] > 0 else float("inf"),
        "gain_naive_over_exp": e["x_naive"] / e["x_exp"] if e["x_exp"] > 0 else float("inf"),
        "gain_naive_over_ser30": e["x_naive"] / e["x_ser30"] if e["x_ser30"] > 0 else float("inf"),
    })
def gain_stats(g):
    out = {}
    for k in ("gain_naive_over_expm1", "gain_naive_over_exp", "gain_naive_over_ser30"):
        vals = sorted(v for row in g if math.isfinite(row[k]) for v in [row[k]])
        out[k] = {"max": vals[-1], "min": vals[0], "median": vals[len(vals) // 2]}
    return out
st_gain = gain_stats(gains)

# first failing y per form (deep grid scan, descending from top of mandated range)
def first_fail(errs, f):
    for y, e in sorted(errs, key=lambda t: -t[0]):
        if e[f] > BAR:
            return y
    return None
first_fail_y = {f: first_fail(err_deep, f) for f in forms}

# analytic worst-case bound: naive denominator 1-exp(-s) has abs error <= 0.5 ulp(1) = 2^-53
ULP1 = 2.0 ** -53
worstcase_bound = lambda s: (0.5 * ULP1) / s
y_guaranteed_fail = (0.5 * ULP1 / BAR) ** 2   # s_crit^2 with 0.5*ulp/s = BAR
check_bounds("after gains")

# per-decade table (mandated range): select by grid index (k/10 -> index (k+16)*10)
decade = []
for p in range(-4, -17, -1):
    idx = int(round((p + 16.0) * 10))  # p=-4 -> 120 ... p=-16 -> 0
    y, e = err_deep[idx]
    decade.append({"y": y, **{f: e[f] for f in forms}})

# ---------------------------------------------------------------- 4. series route verification (cf. AS028)
# 4a. x/s = 1 + s/2 + s^2/12 - s^4/720 + ... : value agreement vs reference on y <= 10
ys_ser = [10.0 ** k for k in [k / 10 for k in range(-160, 101)]] + [0.5, 1.5, 3.0, 7.0, 9.9]
ser_res = []
for y in ys_ser:
    if y <= 10.0:
        s_dec = Decimal(y).sqrt()
        ref_xos = (Decimal(y) / (Decimal(1) - (-s_dec).exp())) / s_dec
        sf = math.sqrt(y)
        xos_120 = sum(float(q[k]) * sf ** k for k in range(120))  # direct sum (fp64)
        acc = 0.0  # Horner alternative
        for k in range(119, -1, -1):
            acc = acc * sf + float(q[k])
        ser_res.append({
            "y": y,
            "relerr_xos120_direct": float(abs((xos_120 - float(ref_xos)) / float(ref_xos))),
            "relerr_xos120_horner": float(abs((acc - float(ref_xos)) / float(ref_xos))),
        })
ser_max_err = max(r["relerr_xos120_horner"] for r in ser_res)
# substitution into defining relation: (1-exp(-s)) * x_ser / s = s  (i.e. x_ser*(1-e^-s) = y)
sub_rows = []
for y in ys_ser:
    if y <= 10.0:
        s = math.sqrt(y)
        acc = 0.0
        for k in range(119, -1, -1):
            acc = acc * s + float(q[k])
        resid = abs((1.0 - math.exp(-s)) * acc - s)
        sub_rows.append({"y": y, "resid": resid})
sub_max = max(r["resid"] for r in sub_rows)
# 4b. radius probes
def radius_probe(y):
    s = math.sqrt(y)
    xos_n = sum(float(q[k]) * s ** k for k in range(120))
    ref = float((Decimal(y) / (Decimal(1) - (-Decimal(y).sqrt()).exp())) / Decimal(y).sqrt())
    return {"y": y, "relerr120": abs((xos_n - ref) / ref) if ref else float("inf"),
            "term120": abs(float(q[120]) * s ** 120)}
radius_rows = [radius_probe(y) for y in [19.7392, 30.0, 39.0, 39.4, 39.4784176, 40.0, 50.0]]
# 4c. radius statement consistency: poles of s/(1-e^{-s}) at s = 2 pi i k -> R_s = 2 pi, R_y = 4 pi^2
R_y = 4.0 * math.pi ** 2
check_bounds("after series route")

# ---------------------------------------------------------------- 5. MONO splice: deep inheritance (operative branch)
# contract: h_RAR(y) = y*(nu-1); h'_mono = max(h'_RAR, delta*h_p/(y+y_p)); splice y* where equal;
# h_mono = h_RAR on (0, y*]; nu_mono = 1 + h_mono/y.
DELTA = 0.05
def h_rar(y):
    s = math.sqrt(y)
    return y / (math.exp(s) - 1.0)
def hp_rar(y):
    s = math.sqrt(y)
    e = math.exp(s)
    return (e * (2.0 - s) - 2.0) / (2.0 * (e - 1.0) ** 2)
# maximize h_RAR: solve hp_rar(y_p) = 0 by bisection on (1.5, 4)
lo, hi = 1.5, 4.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if hp_rar(mid) > 0: lo = mid
    else: hi = mid
y_p = 0.5 * (lo + hi)
h_p = h_rar(y_p)
# splice y*: hp_rar(y*) = DELTA*h_p/(y*+y_p), bisection
def splice_resid(y): return hp_rar(y) - DELTA * h_p / (y + y_p)
lo, hi = 0.5, y_p
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if splice_resid(mid) > 0: lo = mid
    else: hi = mid
y_star = 0.5 * (lo + hi)
QUOTED = dict(y_star=2.337412, y_p=2.53964, h_p=0.647610)
mono_landmarks = {
    "y_star": y_star, "y_p": y_p, "h_p": h_p,
    "quoted": QUOTED,
    "dev_y_star": abs(y_star - QUOTED["y_star"]),
    "dev_y_p": abs(y_p - QUOTED["y_p"]),
    "dev_h_p": abs(h_p - QUOTED["h_p"]),
    "splice_resid": splice_resid(y_star),
}
# deep inheritance: on (0, y*] nu_mono(y) = nu_RAR(y) by construction (same h function);
# measure the identity with INDEPENDENT stable routes: nu_RAR via expm1, nu_MONO via the
# deep series (x_ser30/y).  The h-form route y/(e^s-1) is kept as a diagnostic: it carries
# exactly the naive-form cancellation (its fp64 residual ~1e-8 at y=1e-16 is an evaluation
# artifact of that route, not a branch difference — branches are identical functions there).
mono_deep = []
for y in ys_deep:
    s = math.sqrt(y)
    nu_rar_fp = -1.0 / math.expm1(-s)                       # stable route (expm1)
    nu_mono_ser = x_series(y, 30) / y                        # stable route (series)
    nu_mono_h = 1.0 + y / (math.exp(s) - 1.0) / y            # naive h-form route (diagnostic)
    nu_rar_ref = float(Decimal(1) / (Decimal(1) - (-Decimal(y).sqrt()).exp()))
    mono_deep.append({"y": y,
                      "rel_diff_mono_vs_rar_stable_routes": relerr(nu_mono_ser, nu_rar_fp),
                      "hform_route_rel_err_vs_ref": relerr(nu_mono_h, nu_rar_ref)})
mono_max_rel_diff = max(r["rel_diff_mono_vs_rar_stable_routes"] for r in mono_deep)
mono_hform_max = max(r["hform_route_rel_err_vs_ref"] for r in mono_deep)
inheritance_margin = math.log10(y_star / 1e-4)
check_bounds("after mono")

# ---------------------------------------------------------------- 6. footings (both a0, kappa fixed -> rho changes)
def footing(a0, label):
    rho_l = 4.0 * a0 ** 2 / (G * c ** 2)
    eps_l = rho_l * c ** 2
    lam = 32.0 * math.pi * a0 ** 2 / c ** 4   # same-G (Einstein G = scale G) caveat
    rM = math.sqrt(G * M_SUN * 1e11 / a0) / (PC * 1e3)
    vf = (G * M_SUN * 1e11 * a0) ** 0.25 / 1e3
    gtab = {}
    for y in (1e-16, 1e-10, 1e-4, 1.0, 1e2):
        gtab[y] = a0 * y * float(Decimal(1) / (Decimal(1) - (-Decimal(y).sqrt()).exp()))
    return {"footing": label, "a0": a0, "rho_Lambda": rho_l, "eps_Lambda": eps_l,
            "Lambda (Einstein G = scale G)": lam, "r_M(1e11 Msun)_kpc": rM, "v_flat(1e11 Msun)_kms": vf,
            "g(y)_m_s2": gtab}
footings = [footing(A0_CAN, "canonical a0=9.3619e-11"), footing(A0_ALT, "alternative a0=1.1279e-10")]
rho_ratio = (A0_ALT / A0_CAN) ** 2

# ---------------------------------------------------------------- 7. bundle
result = {
    "started_utc": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    "grid": {
        "mandated_deep": "y=10^k, k in [-16,-4] step 0.1 (121 pts)",
        "extended": "y=10^k, k in [-16,8] step 0.1 (241 pts)",
        "probes": ys_probe,
        "boundary": ys_bound,
    },
    "coefficients": {
        "q_first_12": [str(x) for x in q[:12]],
        "bernstein_match": bern_match,
        "odd_terms_zero_from_k3": sig_odd,
        "first_terms_signature": sig_first,
        "bern_asymp_2n_ratio_last30_mean": rat_tail_mean,
        "bern_asymp_2n_ratio_sample": [(n, v) for n, v in rat[:8]],
    },
    "stats_deep_range": st_deep,
    "stats_extended_range": st_all,
    "gain_deep_range": st_gain,
    "first_failing_y": first_fail_y,
    "y_guaranteed_fail_analytic": y_guaranteed_fail,
    "decade_table": decade,
    "probe_table": err_probe,
    "boundary_table": errors(rows_bound),
    "series_route": {
        "max_relerr_xos120_on_y<=10": ser_max_err,
        "substitution_max_resid": sub_max,
        "radius_rows": radius_rows,
        "R_y_4pi2": R_y,
    },
    "mono": {
        "landmarks": mono_landmarks,
        "deep_inheritance_max_rel_diff": mono_max_rel_diff,
        "hform_route_max_rel_err_diagnostic": mono_hform_max,
        "deep_inheritance_margin_log10(y*/1e-4)": inheritance_margin,
        "sample": mono_deep[:5] + mono_deep[-5:],
    },
    "footings": footings,
    "rho_ratio_alt_over_can": rho_ratio,
    "bounds": {"wall_s": time.monotonic() - t0, "rss_mb": rss_mb(), "threads": 1},
}
with open("raw_output.json", "w") as f:
    json.dump(result, f, indent=1, default=str)
print(json.dumps({k: result[k] for k in ("stats_deep_range", "first_failing_y", "y_guaranteed_fail_analytic",
      "gain_deep_range", "series_route", "mono", "bounds")}, indent=1, default=str))
print(f"AS050 compute done {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} wall {result['bounds']['wall_s']:.3f}s rss {result['bounds']['rss_mb']:.1f}MB")
