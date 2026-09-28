#!/usr/bin/env python3
# AS006 — The MOND radius as a dimensionless reduction.
# Bounded prototype: 1 thread, pure scalar/log-spaced grid computation, target
# wall << 120 s and RSS << 512 MB. Records actually enforced bounds.
#
# Framework inputs (FRAMEWORK_CONTRACT.md): a0 = kappa*c*sqrt(G*rho_Lambda),
# kappa = 1/2 ADOPTED (fitted, not derived here, not derived anywhere in this task).
# Two footings carried separately:
#   canonical    a0 = 9.3619e-11 m s^-2   (kappa = 1/2 on rho_Lambda = rho_DE)
#   alternative  a0 = 1.1279e-10 m s^-2   (kappa = 1/2 on rho_total)
# Point baryon: B = G*M_b/r^2 (spherical).  x = r/r_M, r_M = sqrt(G*M_b/a0).
# Claim under test:  B/a0 = x^-2 exactly, i.e. all acceleration ratios reduce to
# functions of x = r/r_M alone; deep limit g/a0 = x^-1, v_flat^4 = G*M_b*a0.
#
# Branches DISTINCT (never identified): Q (g^2 = B^2 + a0*B), RAR
# (nu = 1/(1-exp(-sqrt(y)))), MU2 (mu = 1-(1+g/(2a0))^-2), EXP historical AQUAL
# (mu = 1-exp(-x)), MONO operative filtered target (h'_mono = max(h'_RAR,
# delta*h_p/(y+y_p)), delta = 0.05). Here MONO is used UNFILTERED (spherical
# algebraic level); the heat-filter (S = exp[(xi^2/2)Delta], coherence length xi)
# dependence is analysed separately as the gate-transfer step.
from __future__ import annotations
import json, math, os, resource, sys, time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
import numpy as np
import mpmath as mp

# ---------------------------------------------------------------- constants
G = 6.67430e-11            # m^3 kg^-1 s^-2   (framework default; single Newtonian G here)
C_LIGHT = 299792458.0      # m s^-1
M_SUN = 1.98847e30         # kg
PC = 3.085677581491367e16  # m
KAPPA = 0.5                # adopted (measured 0.551 +- 0.043; fitted, NOT derived)
CANON, ALT = 9.3619e-11, 1.1279e-10   # m s^-2
FOOTINGS = {"canonical": CANON, "alternative": ALT}
MASSES = [1e6, 1e9, 1e12]  # in M_sun
DELTA_MONO = 0.05

t0 = time.time()

NX = 2001
XMIN, XMAX = 10.0 ** -2.5, 10.0 ** 2.5     # x = r/r_M in [3.162e-3, 316]
x = np.geomspace(XMIN, XMAX, NX)
y = x ** -2.0                              # B/a0 = x^-2 (identity under test)

# ---------------------------------------------------------------- kernels
def nu_RAR(yv): return 1.0 / (1.0 - np.exp(-np.sqrt(yv)))
def h_RAR(yv):  return yv * (nu_RAR(yv) - 1.0)

def solve_implicit(tgt, f, hi_scale=40.0):
    """solve f(xi)*xi = tgt on [0, hi] by bisection (monotone mu on each branch)."""
    a, b = 0.0, max(40.0, 2.0 * tgt * (1.0 + 1.0 / hi_scale))
    for _ in range(300):
        m = 0.5 * (a + b)
        if f(m) * m - tgt < 0.0: a = m
        else: b = m
    return 0.5 * (a + b)

def F_zeta_mu2(zz):
    """F(x) for MU2: xi solves (1-(1+xi/2)^-2)*xi = zz^-2.  F = xi."""
    return np.array([solve_implicit(float(t), lambda m: 1.0 - 1.0 / (1.0 + 0.5 * m) ** 2)
                     for t in zz ** -2.0])

def F_zeta_exp(zz):
    """F(x) for EXP historical AQUAL: xi solves (1-e^-xi)*xi = zz^-2.  F = xi."""
    return np.array([solve_implicit(float(t), lambda m: 1.0 - math.exp(-m))
                     for t in zz ** -2.0])

def F_Q(xv):    return np.sqrt(xv ** -4.0 + xv ** -2.0)
def F_RAR(xv):  return xv ** -2.0 / (1.0 - np.exp(-1.0 / xv))
def F_MU2(xv):  return F_zeta_mu2(xv)
def F_EXP(xv):  return F_zeta_exp(xv)

# ---------------- MONO: locate y_p, h_p, splice y*  --------------------------
# Analytic derivatives:  nu(y) = 1/(1 - e^{-t}), t = sqrt(y),
#   nu'(y) = -e^{-t}/(2 t (1-e^{-t})^2) < 0,
#   h'_RAR(y) = (nu - 1) + y nu'(y) = (nu-1) - y e^{-t}/(2 t (1-e^{-t})^2).
def hp_RAR(yv):
    t = np.sqrt(yv); e = np.exp(-t); nu = 1.0 / (1.0 - e)
    return (nu - 1.0) - yv * e / (2.0 * t * (1.0 - e) ** 2)

# y_p: refine the grid maximum by parabolic fit on the top-3 grid points
ygrid = np.geomspace(1e-5, 1e5, 20001)
hg = h_RAR(ygrid)
ip = int(np.argmax(hg))
lg = np.log(ygrid)
# parabola through (lg[ip-1],hg[ip-1]), (lg[ip],hg[ip]), (lg[ip+1],hg[ip+1])
x1, x2, x3 = lg[ip - 1], lg[ip], lg[ip + 1]
f1, f2, f3 = hg[ip - 1], hg[ip], hg[ip + 1]
den = (x1 - x2) * (x1 - x3) * (x2 - x3)
a_par = (x3 * (f2 - f1) + x2 * (f1 - f3) + x1 * (f3 - f2)) / den
b_par = (x3 * x3 * (f1 - f2) + x1 * x1 * (f2 - f3) + x2 * x2 * (f3 - f1)) / den
ln_y_p = -b_par / (2.0 * a_par)
y_p = float(np.exp(ln_y_p))
h_p = float(h_RAR(y_p))
# y*: unique crossing of hp_RAR(y) with the floor, on (y_p/2, y_p*1.05] where
# hp_RAR is decreasing through the floor (hp_RAR(y) = 0 at y_p; hp_RAR > floor on (0, y*)).
def floor_f(yv): return DELTA_MONO * h_p / (yv + y_p)
def cross(yv): return float(hp_RAR(yv)) - floor_f(yv)
lo, hi = y_p * 0.5, y_p * 1.20
assert cross(lo) > 0.0 and cross(hi) < 0.0, "bracket failed"
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if cross(mid) > 0.0: lo = mid
    else: hi = mid
y_star = 0.5 * (lo + hi)
h_star = h_RAR(y_star)
x_star = 1.0 / math.sqrt(y_star)
def h_mono(yv):
    yv = np.asarray(yv, dtype=float)
    out = np.empty_like(yv)
    m = yv <= y_star
    out[m] = h_RAR(yv[m])
    out[~m] = h_star + DELTA_MONO * h_p * np.log((yv[~m] + y_p) / (y_star + y_p))
    return out
def nu_MONO(yv): return 1.0 + h_mono(yv) / np.asarray(yv, dtype=float)
def F_MONO(xv):  return xv ** -2.0 * nu_MONO(xv ** -2.0)

BRANCHES = {"Q": F_Q, "RAR": F_RAR, "MU2": F_MU2, "EXP": F_EXP, "MONO": F_MONO}

# ---------------------------------------------------------------- C1 seed identity
c1 = {}
for fname, a0 in FOOTINGS.items():
    for Mm in MASSES:
        rM = (G * Mm * M_SUN / a0) ** 0.5
        B = G * Mm * M_SUN / (x * rM) ** 2.0
        B_over_a0 = B / a0
        rel = np.abs(B_over_a0 - x ** -2.0) / x ** -2.0
        c1[f"{fname}_M{Mm:g}"] = {"max_rel_err": float(rel.max())}
c1_max = max(v["max_rel_err"] for v in c1.values())

# ---------------------------------------------------------------- C2 collapse in (g/a0, x)
c2 = {}
for fname, a0 in FOOTINGS.items():
    worst = 0.0
    refs = {}
    for Mm in MASSES:
        rM = (G * Mm * M_SUN / a0) ** 0.5
        B = G * Mm * M_SUN / (x * rM) ** 2.0
        g_a0 = np.sqrt(B * B + a0 * B) / a0          # Q branch in physical variables
        refs[Mm] = g_a0
    for i, Ml in enumerate(MASSES):
        for Mr in MASSES[i + 1:]:
            worst = max(worst, float(np.max(np.abs(refs[Ml] - refs[Mr]))))
    c2[fname] = {"max_pairwise_|g/a0(M1,x)-g/a0(M2,x)|": worst,
                 "note": "zero = identical reduced profile in the (g/a0, x) plane"}
c2_max = max(v["max_pairwise_|g/a0(M1,x)-g/a0(M2,x)|"] for v in c2.values())

# ---------------------------------------------------------------- C3 deep regime + leading term
xd = np.geomspace(1e2, 1e3, 50)
c3 = {}
for name, F in BRANCHES.items():
    Fd = F(xd); pr = Fd * xd
    c3[name] = {"F_x_minus_1_at_1e2": float(pr[0] - 1.0),
                "F_x_minus_1_at_1e3": float(pr[-1] - 1.0),
                "leading_2x*(Fx-1)@1e3": float(2.0 * xd[-1] * (pr[-1] - 1.0)),
                "leading_8x3*(Fx-1)@1e3": float(8.0 * xd[-1] / 3.0 * (pr[-1] - 1.0)),
                "leading_4x*(Fx-1)@1e3": float(4.0 * xd[-1] * (pr[-1] - 1.0)),
                "leading_2x2*(Fx-1)@1e3": float(2.0 * xd[-1] ** 2 * (pr[-1] - 1.0))}
# theory: Q: F*x = sqrt(1+x^-2) = 1 + x^-2/2 + ...   ->  2 x^2 (F x - 1) -> 1
#         RAR: F*x = 1 + 1/(2x) + 1/(12x^2) + ...    ->  2 x   (F x - 1) -> 1
#         MU2: F*x = 1 + 3/(8x)  + ...               ->  (8x/3)(F x - 1) -> 1
#         EXP: F*x = 1 + 1/(4x)  + ...               ->  4 x   (F x - 1) -> 1
#         MONO: equals RAR for y < y* (deep is y -> 0) -> same 2x rule

# ---------------------------------------------------------------- C4 Newtonian regime
xn = np.geomspace(3.16e-3, 1e-2, 20)
c4 = {}
for name, F in BRANCHES.items():
    Fn = F(xn)
    c4[name] = {"F/x^-2 -1 at x=3.16e-3": float(Fn[0] / xn[0] ** -2.0 - 1.0),
                "F/x^-2 -1 at x=1e-2": float(Fn[-1] / xn[-1] ** -2.0 - 1.0)}

# ---------------------------------------------------------------- C5 normalization x=1
c5 = {}
for name, F in BRANCHES.items():
    c5[name] = {"F(1)": float(F(np.array([1.0]))[0])}
c5["Q_exact"] = 2.0 ** 0.5
c5["RAR_exact"] = 1.0 / (1.0 - math.e ** -1.0)

# ---------------------------------------------------------------- C6 MONO splice audit
c6 = {"y_p": y_p, "h_p": h_p, "y_star": y_star, "x_star": x_star,
      "rounded_landmarks_from_spec": {"y_p": 2.5396, "y_star": 2.3374},
      "|y_p - landmark|": abs(y_p - 2.5396), "|y_star - landmark|": abs(y_star - 2.3374),
      "cross(y_star) (want ~0)": cross(y_star)}
eps6 = 1e-4
c6["continuity_|h_mono(y*+e)-h_RAR(y*+e)|"] = float(abs(h_mono(y_star + eps6) - h_RAR(y_star + eps6)))
ys_below = np.geomspace(1e-5, y_star * 0.99, 500)
c6["max_rel_dev_nuMONO_vs_nuRAR_below_y*"] = float(
    np.max(np.abs(nu_MONO(ys_below) - nu_RAR(ys_below)) / nu_RAR(ys_below)))
# derivative rule h'_mono = max(h'_RAR, floor): check the max transitions at the splice
deps = 1e-3
c6["hp_RAR-minus-floor at y*-deps (want >0)"] = float(hp_RAR(y_star - deps) - floor_f(y_star - deps))
c6["hp_RAR-minus-floor at y*+deps (want <0)"] = float(hp_RAR(y_star + deps) - floor_f(y_star + deps))
c6["max floor at y*"] = float(DELTA_MONO * h_p / (y_star + y_p))

# ---------------------------------------------------------------- C7 NEGATIVE CONTROL
# Candidate WRONG radius: r_M' = G*M_b/a0  (dimension L^2, not L).
# It must FAIL (a) dimensional analysis, (b) forward substitution B/a0 = (r/r_M')^-2,
# (c) profile collapse.  The control is capable of failing: had r_M' been right, (b)
# and (c) would hold; we verify they do not, and we state the tolerances beforehand.
tol_b = 1e-6   # tolerance for "forward substitution holds"
c7 = {"tolerances_set_before": {"forward_substitution_rel_tol": tol_b}}
for fname, a0 in FOOTINGS.items():
    row = {}
    # (a) dimensional exponents [L, M, T]
    dim_cand = [3 + 0 - 1, -1 + 1 - 0, -2 + 0 + 2]          # = [2,0,0] -> L^2
    row["units_of_G*M_b/a0"] = dim_cand
    row["is_length"] = bool(np.array_equal(np.array(dim_cand), np.array([1, 0, 0])))
    # (b) forward substitution at real radii r = rM_true * x, M_b = 1e6 M_sun:
    #     claim: B/a0 == (r/r_M')^-2   ->  B/a0 * (r_M'/r)^2 should be 1 if claim held.
    rM_p = G * 1e6 * M_SUN / a0                       # L^2
    rr = (G * 1e6 * M_SUN / a0) ** 0.5 * x            # true radii (L)
    B_a0 = G * 1e6 * M_SUN / (a0 * rr ** 2.0)
    lhs_claim = B_a0 * (rM_p / rr) ** 2.0             # = 1/rM_p identically (dimensionful)
    row["max_|B/a0*(rM'/r)^2 - 1|"] = float(np.max(np.abs(lhs_claim - 1.0)))
    row["log10_mismatch_factor (want ~0)"] = float(
        math.log10(float(np.abs(lhs_claim[NX // 2]))) if lhs_claim[NX // 2] > 0 else float("nan"))
    # (c) same physical radius r = r_M_true(M1) maps to x' values 1e6 apart for M2/M1:
    xprime_M1 = (G * 1e6 * M_SUN / a0) ** 0.5 / (G * 1e6 * M_SUN / a0)
    xprime_M2 = (G * 1e6 * M_SUN / a0) ** 0.5 / (G * 1e12 * M_SUN / a0)
    row["x'(M1) at r=rM(M1) [units 1/m]"] = xprime_M1
    row["x'(M2) at r=rM(M1) [units 1/m]"] = xprime_M2
    row["same-physical-point x' separation factor M2/M1"] = xprime_M1 / xprime_M2
    c7[fname] = row
c7["verdict"] = ("CONTROL ACTIVE: r_M'=G*M_b/a0 REJECTED — units [L,M,T]=[2,0,0] != [1,0,0]; "
                 "forward substitution B/a0=(r/r_M')^-2 is off by ~1e"
                 + str(int(max(float(v["log10_mismatch_factor (want ~0)"])
                               for k, v in c7.items() if k in FOOTINGS)))
                 + " in dimensionless matching (mismatch factor carries the length scale "
                   "'(G*M_b/a0)^{-1}', i.e. x' is NOT dimensionless); the same physical radius maps "
                   "to x'-values " +
                 f"{max(v['same-physical-point x\' separation factor M2/M1'] for k, v in c7.items() if k in FOOTINGS):.3e}"
                 + " apart for M_b = 1e6 vs 1e12 M_sun"
                 ) if all(v["is_length"] is False
                          and v["max_|B/a0*(rM'/r)^2 - 1|"] > tol_b
                          for k, v in c7.items() if k in FOOTINGS) else "CONTROL NOT DETECTING (unexpected)"

# ---------------------------------------------------------------- C8 mpmath 50-digit spot
mp.mp.dps = 50
c8 = {}
for xs_ in [0.01, 0.1, 1.0, 10.0, 100.0]:
    Mb = mp.mpf(M_SUN) * 1e6
    rM = mp.sqrt(mp.mpf(G) * Mb / mp.mpf(CANON))
    B_a0_phys = mp.mpf(G) * Mb / (mp.mpf(CANON) * (mp.mpf(xs_) * rM) ** 2)
    diff = mp.fabs(B_a0_phys - mp.mpf(xs_) ** -2)
    c8[str(xs_)] = {"|B/a0 - x^-2| @50dps": float(diff),
                    "rel": float(diff / (mp.mpf(xs_) ** -2))}

# ---------------------------------------------------------------- C9 translations
tr = []
for fname, a0 in FOOTINGS.items():
    for Mm in MASSES:
        Mb = Mm * M_SUN
        rM = (G * Mb / a0) ** 0.5
        Cv = (G * Mb * a0) ** 0.5
        vf = Cv ** 0.5
        row = {"footing": fname, "M_b(Msun)": Mm,
               "r_M(m)": rM, "r_M(pc)": rM / PC, "r_M(kpc)": rM / PC / 1e3,
               "v_flat(m/s)": vf, "v_flat(km/s)": vf / 1e3, "C(m^2/s)=v_flat^2": Cv,
               "relerr_vflat4_eq_GMb_a0": abs(vf ** 4 - G * Mb * a0) / (G * Mb * a0),
               "relerr_vflat2_eq_a0_rM": abs(vf ** 2 - a0 * rM) / (a0 * rM)}
        for bname in BRANCHES:
            row[f"F_{bname}(1)"] = float(BRANCHES[bname](np.array([1.0]))[0])
        tr.append(row)
rho_can = 4.0 * CANON ** 2 / (G * C_LIGHT ** 2)
rho_alt = 4.0 * ALT ** 2 / (G * C_LIGHT ** 2)
kappa_eff_fixed_rho = ALT / (C_LIGHT * (G * rho_can) ** 0.5)
footing_audit = {"rho_Lambda_canonical(kg/m^3)": rho_can, "rho_Lambda_alternative(kg/m^3)": rho_alt,
                 "kappa_effective_if_rho_fixed_and_a0=alt": kappa_eff_fixed_rho,
                 "a0_ratio_alt/can": ALT / CANON,
                 "r_M_ratio_alt/can": (CANON / ALT) ** 0.5,
                 "v_flat_ratio_alt/can": (ALT / CANON) ** 0.25}

# ---------------------------------------------------------------- C10 no fit
c10 = {"free_parameters_in_F(x)": 0,
       "note": "F(x) = x^-2 nu(x^-2) contains no free parameter within a footing; "
               "kappa=1/2 remains an adopted (fitted) framework input, not derived here."}

# ------------------------------------------------- filtered-MONO gate transfer: argument level
# u_N = -GM/r point mass; S = exp[(xi^2/2) Delta] is a Gaussian smoother of width sigma=xi;
# (S u_N) = -(GM/r) erf(r/(sqrt2 xi))  =>  |grad S u_N| = (GM/r^2)[erf(z) - (2z/sqrt(pi)) e^{-z^2}],
# z = r/(sqrt2 xi).  Deviation of the MOND argument from its unfiltered value at r = r_M:
# eps = (2/sqrt pi) z e^{-z^2} + O(z^-1 e^{-z^2}), exponentially small in (r_M/xi)^2.
cF = {}
# asymptotic: y_xi = x^-2 (1 + eps(r/xi)), eps = -(2/sqrt(pi)) z e^{-z^2} (1 + 1/(2 z^2) + ...),
# valid for z = r/(sqrt2 xi) >> 1. Cross-checked against the exact erf formula at z = 3.
mp.mp.dps = 60
z_check = mp.mpf(3)
erfz = float(mp.erf(z_check))
exact = erfz - (2.0 * z_check / math.sqrt(math.pi)) * math.exp(-float(z_check) ** 2) - 1.0
asym_lead = -(2.0 / math.sqrt(math.pi)) * float(z_check) * math.exp(-float(z_check) ** 2)
cF["_asymptotic_crosscheck_z3"] = {"exact_brack-1": exact,
                                   "leading_term": asym_lead,
                                   "relative_diff": abs(exact - asym_lead) / abs(exact)}
for fname, a0 in FOOTINGS.items():
    xi_pc = 0.10 if fname == "canonical" else 0.15
    xi = xi_pc * PC
    for Mm in MASSES:
        rM = (G * Mm * M_SUN / a0) ** 0.5
        zz = rM / (math.sqrt(2.0) * xi)
        # log10 |eps| = log10(2/sqrt(pi)) + log10(z) - z^2 * log10(e)  (leading; rel err 1+1/(2z^2))
        log10_eps = math.log10(2.0 / math.sqrt(math.pi)) + math.log10(zz) - zz * zz * math.log10(math.e)
        cF[f"{fname}_M{Mm:g}"] = {"r_M/xi": rM / xi,
                                  "log10|eps(r=r_M)|_leading": log10_eps,
                                  "xi(pc)": xi_pc}

# ---------------------------------------------------------------- outputs
t1 = time.time()
ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_kB = ru / 1024.0 if sys.platform == "darwin" else ru  # darwin: bytes; linux: kB
wall = t1 - t0
assert wall < 120.0, "prototype wall bound (120 s) violated"
assert rss_kB < 512 * 1024, "prototype RSS bound (512 MB) violated"
print(f"wall_time_s={wall:.3f} max_rss_kB={rss_kB} nx={NX}")

out = {"wall_time_s": wall, "max_rss_kB": rss_kB,
       "constants": {"G": G, "c": C_LIGHT, "M_sun": M_SUN, "pc": PC, "kappa_adopted": KAPPA},
       "grid": {"nx": NX, "xmin": XMIN, "xmax": XMAX},
       "c1_seed_identity": c1, "c1_max": c1_max,
       "c2_collapse": c2, "c2_max": c2_max,
       "c3_deep": c3, "c4_newtonian": c4, "c5_normalization": c5, "c6_mono": c6,
       "c7_negative_control": c7, "c8_mpmath_spot": c8, "c9_translations": tr,
       "footing_audit": footing_audit, "c10_no_fit": c10,
       "filtered_transfer": cF}
with open("AS006_outputs.json", "w") as fh:
    json.dump(out, fh, indent=1, default=str)
with open("AS006_outputs_summary.txt", "w") as fh:
    fh.write(json.dumps({k: v for k, v in out.items() if k != "c9_translations"},
                        indent=1, default=str))
    fh.write("\n\n--- c9 translations ---\n")
    for row in tr:
        fh.write(json.dumps(row, indent=1, default=str) + "\n")
print("C1 seed identity max rel err =", c1_max)
print("C2 collapse max pairwise dev  =", c2_max)
print("C7 negative control:", c7["verdict"])
print("C8 mpmath spot:", c8)
sys.exit(0)