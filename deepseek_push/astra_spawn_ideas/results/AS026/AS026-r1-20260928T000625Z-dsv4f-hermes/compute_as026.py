#!/usr/bin/env python3
"""
AS026 -- Exact inverse of the algebraic a0 line (Q branch).

Q:  g^2 = B^2 + a0*B            (y = B/a0 > 0, x = g/a0)
Exact inverse (closed form):    B(g) = 2 g^2 / (sqrt(a0^2 + 4 g^2) + a0)
                 dimensionless: y(x) = (sqrt(1+4x^2) - 1)/2 = 2x^2/(sqrt(1+4x^2)+1)

Bounded prototype: <=120 s wall clock (signal.alarm, ENFORCED), <=512 MB target
(RLIMIT_AS attempted; macOS rejects it -- recorded, not enforceable), 1 thread,
mpmath 80 decimal digits, diagnostic grid y = 10^k, k = -10..8 step 0.1 (181 pts).

Branches: Q is the conclusion branch. RAR/MU2/EXP/MONO appear ONLY as labelled
comparison curves (identical deep limit, branch-specific approach rates, finite-y
disagreement); the task's declared branch for conclusions is Q.

Controls that can fail:
  NC1a sign-perturbed inverse (mirror image -y_plus): the FORWARD LAW must reject
       it with a real residual (max ~1 over the grid).
  NC1b true other quadratic root y_neg = -(1+sqrt(1+4x^2))/2: the RAW QUADRATIC
       ACCEPTS it to 80 dps (residual ~1e-81) -- root discarding is NOT automatic.
       Rejection comes from the physical branch (y = B/a0 > 0 with B = g_N > 0 per
       the framework contract), the wrong deep limit (y_neg ~ -x - 1/2 vs +x^2)
       and the wrong g=0 boundary (B = -a0 vs B = 0 with continuity from g>0).
  NC2 perturbed coefficient (4 -> 3 in the discriminant): forward law must reject
       with a real residual at every grid point (max ~0.28; knee 0.1505).
  NC3 subtractive quadratic root near g=0 in float64: catastrophic cancellation
       (relerr -> 100% as x -> 1e-9); the rationalized form is the stable
       representative of the SAME function (agreement to 80 dps at high precision).
"""
import signal, resource, sys, json, time
import sympy as sp

mp = __import__("mpmath")
mp.mp.dps = 80
import numpy as np

T0 = time.monotonic()
signal.alarm(120)              # ENFORCED wall clock
try:
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    MEM_ENFORCED = "ENFORCED (RLIMIT_AS 512 MB set)"
except Exception as e:
    MEM_ENFORCED = f"NOT ENFORCEABLE on this host ({e})"

G   = mp.mpf("6.67430e-11")
c   = mp.mpf("299792458")
M_sun = mp.mpf("1.98847e30")
a0_can = mp.mpf("9.3619e-11")
a0_alt = mp.mpf("1.1279e-10")

# ---------------- symbolic (sympy, exact identities) ----------------
x = sp.symbols("x", positive=True)
yQ = (sp.sqrt(1 + 4*x**2) - 1)/2
D = {}
D["res_forward_symbolic"] = str(sp.simplify(yQ**2 + yQ - x**2))                     # 0
D["res_rationalized_symbolic"] = str(sp.simplify(2*x**2/(sp.sqrt(1+4*x**2)+1) - yQ))  # 0
D["dydx_identity"] = str(sp.simplify(sp.diff(yQ, x) - 2*x/sp.sqrt(1+4*x**2)))       # 0
D["deep_series"] = str(sp.series(yQ, x, 0, 12))           # x^2 - x^4 + 2x^6 - 5x^8 + 14x^10 + O(x^12)
D["newtonian_series"] = str(sp.series(yQ, x, sp.oo, 6))   # x - 1/2 + 1/(8x) - 1/(128x^3) + 1/(1024x^5) + O(x^-6)
D["Bpp_x"] = str(sp.simplify(sp.diff(yQ, x, 2)))          # 2/(1+4x^2)^(3/2) in units of a0 (conditioning; noise-bias analysis is AS453)

# ---------------- exact identities on the mandated grid (181 pts) ----------------
def yQ_num(xx): return (mp.sqrt(1 + 4*xx**2) - 1)/2
def y_neg_num(xx): return -(1 + mp.sqrt(1 + 4*xx**2))/2   # true other quadratic root

ks = [k/10 for k in range(-100, 81)]        # -10.0 .. 8.0 step 0.1 -> 181 pts
ys = [mp.mpf(10)**k for k in ks]
res_fw, res_rt = [], []
bracket_lo, bracket_hi = [], []
deep_rat, deep_lin = [], []                  # deep: y/x^2 = 1/(1+y) exact; approach x/sqrt(y)-1
newt_off1, newt_off2 = [], []                # Newtonian: (x-y) vs 1/2 - 1/(8y)
mono_ok = True
prev_x = mp.mpf(0)
for yy in ys:
    xx = mp.sqrt(yy**2 + yy)
    if xx <= prev_x: mono_ok = False
    prev_x = xx
    res_fw.append(abs(yy**2 + yy - xx**2)/(yy**2 + yy))
    res_rt.append(abs(yy - yQ_num(xx))/yy)
    bracket_lo.append(1 if xx**2/(1+xx**2) < yy else 0)
    bracket_hi.append(1 if yy < xx**2 else 0)
    deep_rat.append(abs(yy/xx**2 - 1))
    deep_lin.append(xx/mp.sqrt(yy) - 1)
    newt_off1.append(abs((xx - yy) - mp.mpf("0.5")))
    newt_off2.append(abs((xx - yy) - (mp.mpf("0.5") - mp.mpf(1)/(8*yy))))
D["grid_n"] = len(ys)
D["grid_span"] = [str(ys[0]), str(ys[-1])]
D["max_res_forward"] = str(max(res_fw))
D["max_res_roundtrip"] = str(max(res_rt))
D["grid_monotone_in_x"] = mono_ok
D["bracket_all_points"] = (all(bracket_lo) and all(bracket_hi))
D["bracket_form"] = "x^2/(1+x^2) < y(x) < x^2  for all x > 0  (from y = x^2/(y+1) with 0 < y < x^2; brackets any root without a grid)"
# deep end (y = 1e-10)
D["deep_y1e-10_ratio_minus1"] = str(deep_rat[0])
D["deep_y1e-10_ratio_minus1_analytic_y_over_1py"] = str(ys[0]/(1+ys[0]))
D["deep_Q_approach_x_over_sqrty_minus1"] = str(deep_lin[0])                       # = y/2 + O(y^2)
D["deep_RAR_approach_x_over_sqrty_minus1"] = str(ys[0]/(1 - mp.e**(-mp.sqrt(ys[0])))/mp.sqrt(ys[0]) - 1)  # = sqrt(y)/2 + O(y)
# Newtonian end (y = 1e8)
D["newt_y1e8_offset1_minus_half"] = str(newt_off1[-1])                            # ~ 1/(8y) - 1/(16y^2)
D["newt_y1e8_offset2_vs_1over8y"] = str(newt_off2[-1])                            # next order ~ 1/(16y^2)
D["newt_y1e8_offset2_analytic_1over16y2"] = str(mp.mpf(1)/(16*ys[-1]**2))

# ---------------- derivative (independent finite-difference representation) ----------------
def dBdg(xx): return 2*xx/mp.sqrt(1 + 4*xx**2)
fd_errs = []
for xx in [mp.mpf("1e-4"), mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2"), mp.mpf("1e2")]:
    h = mp.mpf("1e-40")
    fd = (yQ_num(xx+h) - yQ_num(xx-h))/(2*h)
    fd_errs.append(abs(fd - dBdg(xx))/dBdg(xx))
D["fd_derivative_max_relerr"] = str(max(fd_errs))
D["dBdg_at_0"] = str(dBdg(mp.mpf(0)))
D["dBdg_at_1e30"] = str(dBdg(mp.mpf("1e30")))
D["inverse_conditioning"] = "0 <= dB/dg < 1 on [0,inf); dB/dg(0)=0 (quadratic contact, y~x^2); dB/dg -> 1 as x->inf (y~x-1/2)"

# ---------------- knee mapping ----------------
sq2 = mp.sqrt(2)
D["knee_x_sqrt2"] = str(sq2)
D["knee_y_check_abs"] = str(abs(yQ_num(sq2) - 1))
D["knee_forward_check_abs"] = str(abs(sq2**2 - (1+1)))
D["knee_g_can_m_s2"] = str(sq2*a0_can)
D["knee_g_alt_m_s2"] = str(sq2*a0_alt)
D["knee_g_can_float"] = float(sq2*a0_can)
D["knee_g_alt_float"] = float(sq2*a0_alt)
D["knee_iff"] = "y(x)=1 <=> x = sqrt(2) on x >= 0 (y^2+y=1 -> x^2=2); B = a0 at r_M on both footings"

# ---------------- float64 subtractive vs rationalized (NC3) ----------------
def sub_f64(xx): return (np.sqrt(1.0 + 4.0*xx*xx) - 1.0)/2.0
def rat_f64(xx): return 2.0*xx*xx/(np.sqrt(1.0 + 4.0*xx*xx) + 1.0)
f64_demo = []
for lx in [-3, -5, -7, -9, -11, -13, -15]:
    xx = 10.0**lx
    hi = yQ_num(mp.mpf(10)**lx)
    f64_demo.append({"x": lx, "sub_relerr": float(abs(mp.mpf(sub_f64(xx)) - hi)/hi),
                     "rat_relerr": float(abs(mp.mpf(rat_f64(xx)) - hi)/hi)})
D["f64_cancellation"] = f64_demo

# ---------------- negative controls ----------------
# NC1a: sign-perturbed inverse (mirror image -y_plus): the FORWARD LAW rejects it.
nc1a = {"perturbed_form": "y_pert = -2x^2/(sqrt(1+4x^2)+1) = -y_plus"}
nc1a_res = []
for yy in ys:
    xx = mp.sqrt(yy**2 + yy)
    yp = -2*xx**2/(mp.sqrt(1+4*xx**2) + 1)
    nc1a_res.append(abs(yp**2 + yp - xx**2)/(yy**2 + yy))
nc1a["max_rel_residual_over_grid"] = str(max(nc1a_res))
nc1a["deep_limit_violated"] = "y_pert ~ -x^2 as x->0 (physical y ~ +x^2)"
D["NC1a_sign_perturbation_rejected_by_law"] = nc1a

# NC1b: TRUE other quadratic root: raw law accepts it to 80 dps (NOT automatic!);
# the physical branch (y>0), the limits and the g=0 boundary must reject it.
nc1b = {"true_other_root": "y_neg = -(1 + sqrt(1+4x^2))/2"}
nc1b_res, nc1b_neg = [], []
for yy in ys:
    xx = mp.sqrt(yy**2 + yy)
    yneg = y_neg_num(xx)
    nc1b_res.append(abs(yneg**2 + yneg - xx**2))     # ~0: the OTHER algebraic root
    nc1b_neg.append(1 if yneg < 0 else 0)
nc1b["raw_quadratic_residual_max_abs"] = str(max(nc1b_res))
nc1b["negative_on_all_181_grid_points"] = (all(nc1b_neg), len(nc1b_neg))
nc1b["g0_boundary"] = "y_neg(0) = -1 (B = -a0) vs physical y(0) = 0 (B = 0): non-uniqueness AT the boundary; continuity from g>0 selects B=0"
nc1b["deep_limit"] = "y_neg ~ -x - 1/2 as x->inf (wrong; physical y ~ x - 1/2)"
D["NC1b_other_root_accepted_by_raw_law_rejected_by_domain"] = nc1b

# NC2: perturbed coefficient (4 -> 3): the FORWARD LAW must reject with real residual.
nc2 = {"perturbed_form": "y_pert = 2x^2/(sqrt(1+3x^2)+1)  (discriminant 4 -> 3)"}
nc2_res = []
for yy in ys:
    xx = mp.sqrt(yy**2 + yy)
    yp = 2*xx**2/(mp.sqrt(1 + 3*xx**2) + 1)
    nc2_res.append(abs(yp**2 + yp - xx**2)/(yy**2 + yy))
nc2["max_rel_residual_over_grid"] = str(max(nc2_res))
nc2["knee_y1_rel_residual"] = str(abs((4/(mp.sqrt(7)+1))**2 + 4/(mp.sqrt(7)+1) - 2)/2)   # x=sqrt2 -> y_pert = 4/(sqrt(7)+1)
D["NC2_coefficient_perturbation_rejected_by_law"] = nc2

# ---------------- branch comparison (labelled curves ONLY; Q is the conclusion branch) ----------------
def x_Q(yy): return mp.sqrt(yy**2 + yy)
def x_RAR(yy): return yy/(1 - mp.e**(-mp.sqrt(yy)))
def x_bisect(yy, mu, lo=mp.mpf(0), hi=mp.mpf(1e6)):
    for _ in range(220):
        mid = (lo+hi)/2
        if mid*mu(mid) < yy: lo = mid
        else: hi = mid
    return (lo+hi)/2
x_MU2 = lambda yy: x_bisect(yy, lambda t: 1 - (1 + t/2)**(-2))
x_EXP = lambda yy: x_bisect(yy, lambda t: 1 - mp.e**(-t))
Y_STAR, Y_P, H_P, DELTA = mp.mpf("2.337412"), mp.mpf("2.539638"), mp.mpf("0.647610"), mp.mpf("0.05")
def h_RAR(yy): return yy*(1/(1 - mp.e**(-mp.sqrt(yy))) - 1)
def x_MONO(yy):
    if yy <= Y_STAR: return yy*(1 + h_RAR(yy)/yy)
    hm = h_RAR(Y_STAR) + DELTA*H_P*mp.log((yy + Y_P)/(Y_STAR + Y_P))
    return yy*(1 + hm/yy)
bc_pts = ["1e-4", "1e-2", "1e-1", "1.0", "2.337412", "10.0", "100.0", "1e4"]
bc = []
for syy in bc_pts:
    yy = mp.mpf(syy)
    row = {"y": syy}
    for lab, fn in [("x_Q", x_Q), ("x_RAR", x_RAR), ("x_MU2", x_MU2), ("x_EXP", x_EXP), ("x_MONO", x_MONO)]:
        row[lab] = str(fn(yy))
    bc.append(row)
D["branch_table"] = bc
D["shared_deep_limit_exact_rates"] = {
    "Q": "x/sqrt(y) = sqrt(1+y) = 1 + y/2 + O(y^2)",
    "RAR": "x/sqrt(y) = sqrt(y)/(1-e^-sqrt(y)) = 1 + sqrt(y)/2 + O(y)",
    "MU2": "mu2(x) = x + O(x^2) -> y = x^2 + O(x^3)",
    "EXP": "x(1-e^-x) -> x^2 near 0",
    "MONO": "nu_mono(y) ~ y^(-1/2) (RAR segment for y <= y* = 2.3374)",
    "statement": "all five branches give x ~ sqrt(y) as y -> 0 (identical deep a0-line), at branch-specific approach rates -- identical deep limit is NOT an identical finite law"
}
y10 = mp.mpf("1e-10")
D["approach_rates_at_y1e-10"] = {
    "Q": str(x_Q(y10)/mp.sqrt(y10) - 1),
    "RAR": str(x_RAR(y10)/mp.sqrt(y10) - 1),
    "MU2": str(x_MU2(y10)/mp.sqrt(y10) - 1),
    "EXP": str(x_EXP(y10)/mp.sqrt(y10) - 1),
    "MONO": str(x_MONO(y10)/mp.sqrt(y10) - 1),
}
y0p1 = mp.mpf("0.1")
D["finite_disagreement_at_y0p1"] = {
    "x_Q/x_RAR": str(x_Q(y0p1)/x_RAR(y0p1)),
    "x_Q/x_MU2": str(x_Q(y0p1)/x_MU2(y0p1)),
    "x_Q/x_EXP": str(x_Q(y0p1)/x_EXP(y0p1)),
    "x_Q/x_MONO": str(x_Q(y0p1)/x_MONO(y0p1)),
}

# ---------------- footings and physical scales ----------------
rhoL_can = 4*a0_can**2/(G*c**2)
rhoL_alt = 4*a0_alt**2/(G*c**2)
ratio = a0_alt/a0_can
D["footing_ratio_a0alt_a0can"] = str(ratio)
D["footing_kappa_eff_fixed_rho"] = str(ratio)
D["footing_rho_ratio_fixed_kappa"] = str(rhoL_alt/rhoL_can)
D["rho_Lambda_can_kg_m3"] = str(rhoL_can)
D["rho_Lambda_alt_kg_m3"] = str(rhoL_alt)
def rM(Mb, a0): return mp.sqrt(G*Mb/a0)
for name, Mb in [("1e9", mp.mpf(1e9)*M_sun), ("1e11", mp.mpf(1e11)*M_sun)]:
    D[f"rM_{name}_can_kpc"] = str(rM(Mb, a0_can)/(3.085677581491367e19))
    D[f"rM_{name}_alt_kpc"] = str(rM(Mb, a0_alt)/(3.085677581491367e19))
D["boundary_rM"] = "B(r_M)=a0 identically (definition of r_M); the Q-line then gives g_Q(r_M)=sqrt(2)*a0 on both footings"

# ---------------- dimensional substitution (SI values, both footings) ----------------
dim_res = []
for a0v, tag in [(a0_can, "canonical"), (a0_alt, "alternative")]:
    gs = [mp.mpf("1e-12")*a0v, mp.mpf("1e-9")*a0v, mp.mpf("1e-2")*a0v, sq2*a0v, a0v, 10*a0v, mp.mpf("1e6")*a0v]
    for g in gs:
        Bv = 2*g**2/(mp.sqrt(a0v**2 + 4*g**2) + a0v)
        dim_res.append({"footing": tag, "g/a0": str(g/a0v),
                        "rel_residual": str(abs(g**2 - (Bv**2 + a0v*Bv))/g**2)})
D["dimensional_substitution"] = dim_res

D["monotonicity"] = "y'(x) = 2x/sqrt(1+4x^2) > 0 for x>0 (symbolic identity + FD); y strictly increasing; bijection (0,inf) -> (0,inf); y(0)=0, y->inf"
D["runtime_s"] = time.monotonic() - T0
D["memory_enforced"] = MEM_ENFORCED

print(json.dumps(D, indent=1, default=str))
sys.stderr.write(f"\n[AS026] elapsed {D['runtime_s']:.3f} s; n_grid={D['grid_n']}\n")
