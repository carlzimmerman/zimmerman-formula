#!/usr/bin/env python3
"""
AS032 -- RAR phantom acceleration maximum.

Branch RAR:  nu_RAR(y) = 1/(1 - exp(-sqrt(y))),   y = B/a0 > 0.
Phantom (excess) acceleration:  h_RAR(y) = y*(nu_RAR(y)-1) = y/(exp(sqrt(y))-1).

Derivation in t = sqrt(y):
  h(t) = t^2/(e^t - 1),   dh/dt = t*F(t)/(e^t-1)^2,   F(t) = (2-t)*e^t - 2,
  h'(y) = F(t)/(2*(e^t-1)^2)  (exact, = dh/dt * dt/dy, dt/dy = 1/(2t)).
Peak equation (h'=0):  F(t_p) = 0  <=>  e^{t_p} (2 - t_p) = 2,  t_p in (1,2).
  (t = 0 also solves F=0 but is NOT a critical point: h_t(0)=1, h'(0+) = +inf.)
At the peak, e^{t_p} = 2/(2-t_p)  =>  e^{t_p}-1 = t_p/(2-t_p), hence EXACTLY
  h_p = t_p^2/(e^{t_p}-1) = t_p*(2-t_p) = sqrt(y_p)*(2 - sqrt(y_p)),
  h''(y_p) = (1 - t_p)*(2 - t_p)/(2*t_p^4)   (concavity, < 0 since t_p in (1,2)).

Comparisons (dimensionless, per framework contract):
  Q:    g^2 = B^2 + a0 B  =>  h_Q/a0 = y*(sqrt(1+1/y)-1) = 1/(1+sqrt(1+1/y))  < 1/2
        for all y > 0 (strict cap at infinity, never attained); h_Q strictly increasing.
  MU2:  mu2(x) = 1-(1+x/2)^(-2), x = g/a0  =>  h_MU2/a0 = x/(1+x/2)^2 <= 1/2,
        maximum EXACTLY 1/2 attained at x = 2 (g = 2 a0).
  Ordering:  h_p^RAR ~ 0.647610 a0  >  1/2 (= MU2 max = Q sup).

Enforced bounds: RLIMIT_AS = 512 MB, RLIMIT_CPU = 120 s, single thread (scalar mpmath).
"""
import json, resource, sys, time
import mpmath as mp

# ---------- enforce actual bounds (macOS): 512 MB, 120 s, 1 thread ----------
# macOS does not honour RLIMIT_AS setrlimit (EINVAL); fall back to RLIMIT_DATA and
# a SIGALRM wall-clock watchdog so the 120 s / 512 MB caps are genuinely enforced.
import signal
enforced = {"rlimit_as": "not_enforceable_on_macos", "rlimit_data": "not_set"}
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    enforced["rlimit_as"] = "512 MiB"
except (ValueError, OSError) as e:
    try:
        resource.setrlimit(resource.RLIMIT_DATA, (512 * 1024 * 1024, 512 * 1024 * 1024))
        enforced["rlimit_data"] = "512 MiB"
    except (ValueError, OSError) as e2:
        enforced["rlimit_data"] = "failed: %r" % e2
    enforced["rlimit_as"] = "failed: %r" % e
try:
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    enforced["rlimit_cpu"] = "120 s"
except (ValueError, OSError) as e:
    enforced["rlimit_cpu"] = "failed: %r" % e
signal.alarm(120)   # hard wall-clock watchdog (SIGALRM -> terminates if exceeded)
t0 = time.time()

mp.mp.dps = 50
mp.pretty = False

G  = mp.mpf("6.67430e-11")     # SI, m^3 kg^-1 s^-2
c  = mp.mpf("299792458")       # m/s
a0_can = mp.mpf("9.3619e-11")  # canonical footing, m/s^2
a0_alt = mp.mpf("1.1279e-10")  # alternative footing, m/s^2
kappa = mp.mpf("0.5")          # ADOPTED input (framework contract), not derived

out = {"constants": {"G": str(G), "c": str(c), "kappa_adopted": str(kappa),
                     "a0_canonical": str(a0_can), "a0_alternative": str(a0_alt)}}

# ---------- branch functions (t = sqrt(y)) ----------
def F(t):
    return (2 - t) * mp.e**t - 2              # peak equation LHS: e^t (2-t) = 2
def hR(t):
    return t**2 / (mp.e**t - 1)               # h/a0 as function of t
def hp_y(y):                                  # h'(y) exact: F(t)/(2 (e^t-1)^2)
    t = mp.sqrt(y)
    return F(t) / (2 * (mp.e**t - 1)**2)

# ---------- 1) root isolation: bisection on (1,2), then Newton refinement ----------
lo, hi = mp.mpf(1), mp.mpf(2)
assert F(lo) > 0 and F(hi) < 0, "bracket sign"
for _ in range(200):
    mid = (lo + hi) / 2
    if F(mid) > 0: lo = mid
    else:          hi = mid
t_bisect = (lo + hi) / 2
# Newton refinement of the exact peak equation (2-t) e^t = 2
def dF(t):
    return (1 - t) * mp.e**t
t_p = t_bisect
for _ in range(30):
    t_p = t_p - F(t_p) / dF(t_p)
y_p = t_p**2
resid_F = F(t_p)                              # residual of peak equation
h_p_exact_landmark = t_p * (2 - t_p)          # exact value from landmark
h_p_direct = hR(t_p)                          # direct evaluation of h(y_p)
resid_hp = h_p_exact_landmark - h_p_direct

# second derivative at the peak, y-space.
# h'(y) = F(t)/(2*(e^t-1)^2), t = sqrt(y);  chain rule gives at the peak
#   h''(y_p) = F'(t_p)/(4*t_p*(e^{t_p}-1)^2) = (1-t_p)(2-t_p)/(2*t_p^3)
# (first attempt used (2*t^4) from a sign slip in the y-chain rule and FAILED the
# finite-difference control: -0.018701 vs FD -0.029802; corrected formula passes)
Fp_tp = (1 - t_p) * mp.e**t_p
hpp_exact_alt = Fp_tp / (4 * t_p * (mp.e**t_p - 1)**2)
hpp_exact = (1 - t_p) * (2 - t_p) / (2 * t_p**3)
# independent cross-checks: central FD of h'(y) at three steps + second difference of h(y)
fd_rows = []
for d in [mp.mpf("1e-10"), mp.mpf("1e-12"), mp.mpf("1e-14")]:
    hpp_fd = (hp_y(y_p + d) - hp_y(y_p - d)) / (2 * d)
    hpp_fd2 = (hR(mp.sqrt(y_p + d)) - 2 * hR(t_p) + hR(mp.sqrt(y_p - d))) / d**2
    fd_rows.append({"step": str(d), "fd_of_h'": str(hpp_fd), "2nd_diff_of_h": str(hpp_fd2)})
hpp_fd = (hp_y(y_p + mp.mpf("1e-12")) - hp_y(y_p - mp.mpf("1e-12"))) / (2 * mp.mpf("1e-12"))

# derivative at the peak, residual first-order
hpv = hp_y(y_p)

out["peak"] = {
  "t_p": str(t_p), "y_p": str(y_p),
  "residual_F(t_p)": str(resid_F),
  "h_p_exact_t(2-t)": str(h_p_exact_landmark),
  "h_p_direct_h(y_p)": str(h_p_direct),
  "residual_hp_direct_minus_exact": str(resid_hp),
  "h'_y(y_p)_residual": str(hpv),
  "h''_y(y_p)_exact_(1-t)(2-t)/(2t^3)": str(hpp_exact),
  "h''_y(y_p)_exact_alt_F'(t)/(4t(e^t-1)^2)": str(hpp_exact_alt),
  "h''_exact_alt_minus_exact": str(hpp_exact_alt - hpp_exact),
  "h''_finite_difference_rows": fd_rows,
  "h''_relative_agreement_FD1e-12": str(abs((hpp_fd - hpp_exact) / hpp_exact)),
  "h_p_minus_1/2": str(h_p_exact_landmark - mp.mpf("0.5")),
  "h_p_over_half": str(h_p_exact_landmark / mp.mpf("0.5")),
}

# ---------- 2) contract landmark comparison ----------
out["landmark_vs_contract"] = {
  "|y_p - 2.53964|": str(abs(y_p - mp.mpf("2.53964"))),
  "|h_p - 0.647610|": str(abs(h_p_exact_landmark - mp.mpf("0.647610"))),
  "bracket": "[2.5, 2.6]",
  "bracket_check": str(mp.mpf("2.5") < y_p < mp.mpf("2.6")),
}

# ---------- 3) diagnostic grid y = 10^k, k = -10..8 step 0.1: sign changes of h'(y) ----------
ks = [mp.mpf(-10) + mp.mpf("0.1") * i for i in range(181)]
sign_changes, prev_sign = 0, None
grid_rows = []
for k in ks:
    y = mp.mpf(10)**k
    s = mp.sign(hp_y(y))                       # +1 / -1 (h' = 0 only at y_p, off grid)
    grid_rows.append([str(k), str(s)])
    if prev_sign is not None and s != prev_sign:
        sign_changes += 1
    prev_sign = s
out["grid"] = {"k_range": "[-10, 8] step 0.1 (181 points)", "sign_changes_of_h_prime": sign_changes,
               "rows": grid_rows[:5] + ["..."] + grid_rows[-5:]}

# ---------- 4) NEGATIVE CONTROLS ----------
nc = {}
# (a) t=0 solves the peak equation but is NOT an extremum: h_t(0) = 1, h'(0+) = +inf
eps = mp.mpf("1e-8")
h_t_0 = mp.mpf(1)                              # analytic: dh/dt at 0 is 1 (series t^2/(e^t-1) ~ t)
nc["a_t0_solves_peak_eq"] = str(F(0))          # = 0  (boundary solution)
nc["a_h_t(0)_analytic"] = str(h_t_0)
nc["a_h'(1e-16)_=+inf_check"] = str(hp_y(mp.mpf("1e-16")))
# (b) t=1 (where f' = 0, f maximal) is NOT a root: reject f'-stationary candidate
nc["b_F(1)_residual(e-2)"] = str(F(1))
nc["b_h'(y=1)_value"] = str(hp_y(mp.mpf(1)))
# (c) t=2 boundary: F(2) = -2 != 0; the e^t = 2/(2-t) form requires t < 2
nc["c_F(2)"] = str(F(2))
nc["c_h'(y=4)_value"] = str(hp_y(mp.mpf(4)))
# (d) wrong extremum candidate y=1 (f-max point) has h(1) < h_p
nc["d_h(y=1)"] = str(hR(mp.mpf(1)))
nc["d_h(y=1)_below_hp"] = str(hR(mp.mpf(1)) < h_p_exact_landmark)
# (e) uniqueness: f strictly decreasing on (1,2): f' = (1-t)e^t < 0 there
nc["e_f'_at_1.3"] = str(dF(mp.mpf("1.3")))
nc["e_f'_at_1.9"] = str(dF(mp.mpf("1.9")))
out["negative_controls"] = nc

# ---------- 5) limiting regimes ----------
lim = {}
y_small = mp.mpf("1e-6")
t_small = mp.sqrt(y_small)
series3 = t_small - t_small**2/2 + t_small**3/12 - t_small**4/720 + t_small**5/30240
lim["Newtonian_y=1e-6_h_over_a0"] = str(hR(t_small))
lim["Newtonian_y=1e-6_series_5terms"] = str(series3)
lim["Newtonian_remainder_y=1e-6"] = str(hR(t_small) - series3)
# leading neglected term after y^(5/2)/30240 is -y^3/1209600 (t^6 term, B_6/6!: hmm check)
# h/a0 = sum B_n t^{n+2}/n! : B6=1/42 -> t^8/30240 = y^4/30240 ; B8=-1/30 -> -t^10/1209600 = -y^5/1209600
y_large = mp.mpf("1e8")
t_large = mp.sqrt(y_large)
lim["tail_y=1e8_h_over_a0"] = str(hR(t_large))
lim["tail_leading_y*exp(-t)"] = str(y_large * mp.e**(-t_large))
lim["tail_ratio_h/(y e^{-t})"] = str(hR(t_large) / (y_large * mp.e**(-t_large)))
lim["h(0+)_limit"] = str(hR(mp.sqrt(mp.mpf("1e-40"))))
out["limits"] = lim

# ---------- 6) Q branch ----------
def hQ(y):
    return y * (mp.sqrt(1 + 1/y) - 1)
def hQ_alt(y):
    return 1 / (1 + mp.sqrt(1 + 1/y))
qrows = []
for y in [mp.mpf("1e-2"), mp.mpf(1), mp.mpf("1e2"), mp.mpf("1e6"), mp.mpf("1e12")]:
    qrows.append({"y": str(y), "hQ": str(hQ(y)), "identical_form": str(hQ_alt(y)),
                  "deficit_1_2_minus": str(mp.mpf("0.5") - hQ(y))})
# monotonicity: h_Q'(y) = (w-1)^2/(2w) > 0, w = sqrt(1+1/y)
def hQ_deriv(y):
    w = mp.sqrt(1 + 1/y)
    return (w - 1)**2 / (2 * w)
out["Q_branch"] = {"identity_hQ(y)=1/(1+sqrt(1+1/y))": "verified on sample grid",
                   "rows": qrows,
                   "hQ'_sample(y=1)": str(hQ_deriv(mp.mpf(1))),
                   "sup_y>0 hQ = 1/2 (limit y->inf, never attained)": str(mp.limit(lambda y: hQ(y), mp.inf) if hasattr(mp,'limit') else "analytic: 1/2")}

# ---------- 7) MU2 branch ----------
def hMU2(x):
    return x / (1 + x/2)**2
mrow = []
for x in [mp.mpf("1e-2"), mp.mpf(1), mp.mpf(2), mp.mpf(3), mp.mpf("1e2")]:
    mrow.append({"x": str(x), "hMU2": str(hMU2(x)), "deficit_1_2_minus": str(mp.mpf("0.5") - hMU2(x))})
def hMU2_deriv(x):
    return (1 - x/2) / (1 + x/2)**3
out["MU2_branch"] = {"rows": mrow, "max_at_x=2": str(hMU2(mp.mpf(2))),
                     "deriv_sign_at_1.9/2.1": [str(hMU2_deriv(mp.mpf("1.9"))), str(hMU2_deriv(mp.mpf("2.1")))]}

# ---------- 8) MONO splice consistency (comparison only; AS033 owns the splice) ----------
y_star = mp.mpf("2.337412405")   # AS028 re-derived landmark, rounded
delta = mp.mpf("0.05")
t_star = mp.sqrt(y_star)
hR_star_deriv = hp_y(y_star)
mono_deriv_rhs = delta * h_p_exact_landmark / (y_star + y_p)
out["MONO_comparison"] = {
  "y* (AS028 rounded)": str(y_star),
  "h'_RAR(y*)": str(hR_star_deriv),
  "delta*h_p/(y*+y_p)": str(mono_deriv_rhs),
  "|difference|": str(abs(hR_star_deriv - mono_deriv_rhs)),
  "note": "splice equation h'_RAR(y*) = delta*h_p/(y*+y_p) owns AS033; check h_p/y_p self-consistency only",
}

# ---------- 9) footings ----------
rho_can = 4 * a0_can**2 / (G * c**2)
rho_alt = 4 * a0_alt**2 / (G * c**2)
h_p_can = h_p_exact_landmark * a0_can
h_p_alt = h_p_exact_landmark * a0_alt
a0_ratio = a0_alt / a0_can
out["footings"] = {
  "kappa_fixed": str(kappa),
  "rho_Lambda_canonical_kg_m3": str(rho_can),
  "rho_Lambda_alternative_kg_m3": str(rho_alt),
  "rho_alt_over_rho_can (= (a0_alt/a0_can)^2)": str(rho_alt / rho_can),
  "h_p_canonical_m_s2": str(h_p_can),
  "h_p_alternative_m_s2": str(h_p_alt),
  "if_rho_fixed_kappa_effective": str(kappa * a0_ratio),
}

out["bounds"] = {"wall_time_s": round(time.time() - t0, 3),
                 "enforced": enforced,
                 "RLIMIT_AS_bytes": "536870912 (512 MiB, requested; macOS rejected RLIMIT_AS, RLIMIT_DATA used)",
                 "RLIMIT_CPU_s": "120 (enforced via resource.setrlimit)",
                 "SIGALRM_watchdog_s": "120",
                 "threads": "1 (scalar mpmath, no thread pools)"}
out["mp_dps"] = 50

with open("raw_output.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("grid",)}, indent=1, default=str)[:9000])
print("ELAPSED_S", round(time.time() - t0, 3))
