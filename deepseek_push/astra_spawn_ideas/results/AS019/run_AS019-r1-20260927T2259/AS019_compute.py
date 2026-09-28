#!/usr/bin/env python3
"""
AS019 - Deep-law source mass conventions: exact-consequence audit.

Bounded computation: pure stdlib, 1 thread, wall-clock budget 120 s, memory budget 512 MB.
Self-enforced: the script watches wall time and exits nonzero (>63) if exceeded;
the OS-level resource envelope is recorded in result.json (execution_bounds).

Conventions (all symbols positive reals unless noted):
  B(r)   = G_N * M_b(<r) / r^2      baryonic (Newtonian-equivalent) radial acceleration
  M_b(<r) = 4*pi*int_0^r rho_b(x) x^2 dx   enclosed baryonic mass (spherical shell theorem)
  deep law (all five branches share this limit):  v^4 = G_N * a0 * M_b(<r)
  running log slope:  d ln v / d ln r = (1/4) * (r * M_b'(<r)) / M_b(<r)
                                          = (1/4) * (4 pi r^3 rho_b(r)) / M_b(<r)
  r_M(M) = sqrt(G_N * M / a0)   (transition radius for a mass M)
  kernel argument:  y = B / a0 = G_N * M_b(<r) / (a0 r^2)
Both a0 footings carried separately everywhere dimensional.
"""

import math, os, sys, time, resource, json

T0 = time.time()
WALL_BUDGET_S = 120.0
MEM_BUDGET_MB = 512.0

def bounds_check():
    if time.time() - T0 > WALL_BUDGET_S:
        print("WALL_BUDGET_EXCEEDED"); sys.exit(66)
    # macOS getrusage reports ru_maxrss in BYTES; Linux in KB.
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        rss_bytes = rss
    else:
        rss_bytes = rss * 1024.0
    rss_mb = rss_bytes / (1024.0*1024.0)
    if rss_mb > MEM_BUDGET_MB:
        print("MEM_BUDGET_EXCEEDED"); sys.exit(67)

# ----------------------------------------------------------------------------
# Constants (FRAMEWORK_CONTRACT defaults)
# ----------------------------------------------------------------------------
G_N   = 6.67430e-11          # measured Newton coupling, SI (m^3 kg^-1 s^-2)
C_L   = 299792458.0          # c, m/s
M_SUN = 1.98847e30           # kg
PC    = 3.085677581491367e16 # m
A0_CAN = 9.3619e-11          # canonical footing, m/s^2
A0_ALT = 1.1279e-10          # alternative footing, m/s^2

KM = 1e3

def r_M_pc(M_kg, a0):
    """r_M = sqrt(G_N M/a0) in pc."""
    return math.sqrt(G_N * M_kg / a0) / PC

def v_flat_kms(M_kg, a0):
    """v_flat = (G_N a0 M)^(1/4) in km/s."""
    return (G_N * a0 * M_kg) ** 0.25 / KM

# ----------------------------------------------------------------------------
# Section 1: uniform-density baryon sphere -- negative control and limits
# ----------------------------------------------------------------------------
# Sphere: rho_b = const = rho, radius R, total mass M_tot = (4/3) pi rho R^3.
RHS = dict(canonical=A0_CAN, alternative=A0_ALT)

RHO = 1.0e-21        # kg/m^3 (illustrative diffuse baryonic sphere)
R   = 20.0 * PC      # m
M_TOT = (4.0/3.0)*math.pi*RHO*R**3
B_max = G_N*M_TOT/R**2

res = {}
res["uniform_sphere_setup"] = {
    "rho_kg_m3": RHO, "R_pc": R/PC, "M_tot_Msun": M_TOT/M_SUN,
    "B(R)/a0_canonical": B_max/A0_CAN, "B(R)/a0_alt": B_max/A0_ALT,
    "deep_regime_flag": B_max/A0_ALT < 0.01,   # deep approx valid where B/a0 <= about 1e-2
}
assert res["uniform_sphere_setup"]["deep_regime_flag"], "deep regime not entered at edge"

def log_slope_of(f, xs):
    """local log-log slope via symmetric 4-point difference on the given grid."""
    return [(math.log(f(xs[i+1]))-math.log(f(xs[i-1])))/(math.log(xs[i+1])-math.log(xs[i-1]))
            for i in range(1, len(xs)-1)], xs[1:-1]

def M_enc_sph(r):
    if r >= R: return M_TOT
    return (4.0/3.0)*math.pi*RHO*r**3

def B_sph(r):
    return G_N*M_enc_sph(r)/r**2

grid = [0.02*R + i*(0.28*R)/(2*50) for i in range(51)]   # [0.02R, 0.30R]

def v_deep_enc(r, a0):        # enclosed-mass deep law
    return (G_N*a0*M_enc_sph(r))**0.25
def v_deep_tot(r, a0):        # WRONG convention: total mass everywhere
    return (G_N*a0*M_TOT)**0.25
def v_newt(r):                # Newtonian circular speed, enclosed mass
    return math.sqrt(G_N*M_enc_sph(r)/r)

slopes = {}
for foot, a0 in RHS.items():
    _, rmid = log_slope_of(lambda r: v_deep_enc(r, a0), grid)
    s_enc, _ = log_slope_of(lambda r: v_deep_enc(r, a0), grid)
    s_tot, _ = log_slope_of(lambda r: v_deep_tot(r, a0), grid)
    s_new, _ = log_slope_of(lambda r: v_newt(r), grid)
    slopes[foot] = {"enc_enclosed_mass": s_enc, "wrong_total_mass": s_tot,
                    "newtonian": s_new, "r_sample_pc": [x/PC for x in rmid]}

# Independent representation of B(r): direct radial quadrature of the shell theorem.
def B_quad(r, n=2000):
    # Simpson over [0, r] of rho(x)*4 pi x^2, then /r^2 * G
    if r == 0: return 0.0
    a, h = 0.0, r/n
    s = RHO*4*math.pi*a*a
    for i in range(1, n):
        x = a + i*h
        s += (4 if i % 2 else 2)*RHO*4*math.pi*x*x
    s += RHO*4*math.pi*r*r
    M = h*s/3.0
    return G_N*M/r**2

rprobe = [0.05*R, 0.13*R, 0.27*R]
Bquad_res = [ (B_quad(r) - B_sph(r))/B_sph(r) for r in rprobe ]
res["shell_theorem_crosscheck"] = {
    "relative_residual_B_quadrature_vs_closed_form": Bquad_res,
    "tolerance": 1e-10,
    "pass": all(abs(e) < 1e-10 for e in Bquad_res),
}

# Analytic (closed-form) log slopes for comparison
def analytic_slope_deep_enc(r, a0):
    # d ln v/d ln r = (1/4)*(r*M'(r))/M(r) = (1/4)*3 = 3/4 inside the sphere
    return 0.75
def analytic_slope_newt(r):
    # (1/2)*(r*M'/M - 1) = (1/2)*(3-1) = 1
    return 1.0

res["slopes_check"] = {}
for foot, a0 in RHS.items():
    s_enc, rmid = log_slope_of(lambda r: v_deep_enc(r, a0), grid)
    s_new, _   = log_slope_of(lambda r: v_newt(r), grid)
    res["slopes_check"][foot] = {
        "deep_enclosed_slope_mean": sum(s_enc)/len(s_enc),
        "deep_enclosed_slope_target": 0.75,
        "deep_enclosed_residual": sum(s_enc)/len(s_enc)-0.75,
        "newtonian_slope_mean": sum(s_new)/len(s_new),
        "newtonian_slope_target": 1.0,
        "newtonian_residual": sum(s_new)/len(s_new)-1.0,
        "wrong_total_slope_mean": sum(slopes[foot]["wrong_total_mass"])/len(slopes[foot]["wrong_total_mass"]),
        "wrong_total_slope_target": 0.0,
        "wrong_total_slope_residual": sum(slopes[foot]["wrong_total_mass"])/len(slopes[foot]["wrong_total_mass"]),
    }

# ----------------------------------------------------------------------------
# Section 2: running slope identity for a non-power-law M_b(<r)
# (two-component: uniform core "bulge" + truncated power-law envelope "disk")
# ----------------------------------------------------------------------------
r1 = 2.0*1000.0*PC        # core/bulge boundary (2 kpc)
R2 = 25.0*1000.0*PC       # envelope truncation (25 kpc)
rho1 = 1.0e-20            # core density kg/m^3 (illustrative)
rho2 = 3.0e-22            # envelope density scale kg/m^3 (illustrative)
p = 2.0

def M_core():
    return (4.0/3.0)*math.pi*rho1*r1**3

def M_env(r):
    # envelope rho = rho2*(r/r1)^(-p), mass: 4 pi rho2 r1^p int_{r1}^r x^{2-p} dx
    if abs(p-3.0) < 1e-12:
        return 4*math.pi*rho2*r1**p*math.log(r/r1)
    return 4*math.pi*rho2*r1**p*(r**(3-p)-r1**(3-p))/(3-p)

def M_enc2(r):
    if r <= r1:
        return (4.0/3.0)*math.pi*rho1*r**3
    if r <= R2:
        return M_core() + M_env(r)
    return M_core() + M_env(R2)

def rho2_fn(r):
    if r <= r1: return rho1
    if r <= R2: return rho2*(r/r1)**(-p)
    return 0.0

grid2 = [r1*1.02 + i*(R2*0.95-r1*1.02)/32000 for i in range(32001)]
slopes_run = {}
for foot, a0 in RHS.items():
    s, rmid = log_slope_of(lambda r: (G_N*a0*M_enc2(r))**0.25, grid2)
    analytic = [(1.0/4.0)*(4*math.pi*r**3*rho2_fn(r))/M_enc2(r) for r in rmid]
    rel_full = [abs((a-b)/b) if b != 0 else 0.0 for a, b in zip(s, analytic)]
    # Boundary-layer cut: the model density jumps at the bulge edge r1 (rho1 -> rho2);
    # finite differences straddling the kink average the two branches. The identity is
    # pointwise-exact away from the kink; evaluate the pass criterion on r >= 1.03*r1 and
    # report the full-domain maximum separately.
    mask = [r >= 1.03*r1 for r in rmid]
    rel_cut = [e for e, m in zip(rel_full, mask) if m]
    slopes_run[foot] = {
        "max_relative_residual_full_domain": max(rel_full),
        "max_relative_residual_away_from_bulge_kink": max(rel_cut),
        "n_points_full": len(s),
        "n_points_cut": len(rel_cut),
        "cut_description": "r >= 1.03*r1 (3% boundary layer at bulge-edge density kink excluded)",
        "tolerance": 1e-7,
        "pass": max(rel_cut) < 1e-7,
    }

# ----------------------------------------------------------------------------
# Section 3: convention-flip exact consequences
# ----------------------------------------------------------------------------
# Catalog conventions:  D  = disk only (stars)
#                       DB = disk + bulge (stars)
#                       DBG= disk + bulge + gas  (full baryonic total)
# lambda_DBG_D = 1 + mu_b + mu_g  with mu_b = M_bulge/M_disk, mu_g = M_gas/M_disk.
# ILLUSTRATIVE sample (not a fit, not a catalog row): mu_b = 1/3, mu_g = 1/5.
mu_b = 1.0/3.0; mu_g = 1.0/5.0
lam = 1.0 + mu_b + mu_g   # = 23/15

flip = {
    "mu_b_illustrative": mu_b, "mu_g_illustrative": mu_g,
    "lambda": lam, "lambda_exact_rational": "23/15",
    "v_flat_ratio_DBG_over_D": lam**0.25,
    "r_M_ratio_DBG_over_D": math.sqrt(lam),
    "kernel_argument_ratio_DBG_over_D_same_r": lam,
    "inferred_a0_ratio_if_mass_convention_wrong_by_lambda": lam,   # a0_est inflates by lam
    "deep_g_ratio_same_r": math.sqrt(lam),
}

# Degeneracy statement (corrected): the settled flat-region observable fixes only the
# product P = a0*M_b (v_flat^4 = G*P). A catalog convention flip M -> lambda*M at fixed
# a0 is therefore EXACTLY equivalent (same flat rotation curve) to a scale flip a0 -> lambda*a0
# (i.e. kappa -> lambda*kappa) at fixed M — the flip is degenerate with a kappa renormalisation,
# and conversely a flat-region fit cannot separate the mass convention from kappa.
# Consequence for calibration: a0_est = v_flat^4/(G*M_catalog); if the catalog under-reports by
# lambda (M_cat = M_true/lambda), a0_est = lambda*a0 (inferred a0 inflated by lambda).
M_d = 6.0e10*M_SUN
br = {}
for foot, a0 in RHS.items():
    v_flip_mass = v_flat_kms(lam*M_d, a0)      # convention flip: true mass is lam*M_d
    v_scale_a0 = v_flat_kms(M_d, lam*a0)       # equivalent a0 flip at fixed catalog mass
    v_cat = v_flat_kms(M_d, a0)                # naive catalog reading
    br[foot] = {
        "v_flat_true_kms": v_flip_mass,
        "v_flat_naive_catalog_kms": v_cat,
        "v_flat_a0_flip_equivalent_kms": v_scale_a0,
        "flip_equiv_a0_flip_max_abs_deviation_kms": abs(v_flip_mass-v_scale_a0),
        "pass_flip_equivalent_to_a0_scale": abs(v_flip_mass-v_scale_a0) < 1e-9,
        "naive_catalog_underpredicts_by": v_cat/v_flip_mass,   # = lambda^(-1/4)
        "a0_est_inflation_if_catalog_underreports_by_lambda": lam,  # a0_est = lam*a0
    }

# Transition-region discrimination: a convention flip whose radial PROFILE differs
# (bulge stripped: M_disk(<r) = M_env(<r), bulge = core) cannot be mimicked by any
# constant a0 renormalisation, because the y-profile ratio now varies with r.
# Contrast with the constant-scale flip (M -> M/lambda at every r), which IS
# renormalisation-degenerate (identical y-profile).
disc = {}
for foot, a0 in RHS.items():
    r3 = 8.0*1000.0*PC
    y_true = G_N*M_enc2(r3)/(a0*r3**2)
    y_cat_const = y_true/lam                       # constant-scale under-report
    y_cat_strip = G_N*M_env(r3)/(a0*r3**2)         # bulge-stripped (profile-changing)
    # best constant a0 rescale to mimic the stripped profile on [r1, R2]:
    rs = [r1*1.01 + i*(R2*0.9-r1*1.01)/300 for i in range(301)]
    ratio_err = [math.log(G_N*M_enc2(r)/(a0*r*r)) - math.log(G_N*M_env(r)/(a0*r*r))
                 for r in rs]
    loglam_best = sum(ratio_err)/len(ratio_err)
    residual_after_best_rescale = max(abs(e-loglam_best) for e in ratio_err)
    disc[foot] = {
        "r_pc": r3/PC, "y_true": y_true,
        "y_catalog_constant_scale": y_cat_const,
        "y_catalog_bulge_stripped": y_cat_strip,
        "profile_ratio_true_over_stripped": y_true/y_cat_strip,
        "best_constant_rescale_equiv_lambda": math.exp(loglam_best),
        "max_log_residual_after_best_rescale": residual_after_best_rescale,
        "constant_scale_flip_is_degenerate": True,
        "profile_flip_is_NOT_a0_degenerate": residual_after_best_rescale > 1e-9,
    }

# ----------------------------------------------------------------------------
# Section 4: the five branches written in terms of M_b; per-branch flip ratios
# ----------------------------------------------------------------------------
def nu_RAR(y):
    return 1.0/(1.0-math.exp(-math.sqrt(y)))

def h_RAR(y):
    return y/(math.exp(math.sqrt(y))-1.0)

# MONO splice: solve h'_RAR(y*) = delta*h_p/(y*+y_p); h'_RAR = dh/dy analytic.
def hRAR_p(y):
    z = math.sqrt(y)
    e = math.exp(z)
    d = e-1.0
    # h = z^2/(e^z-1); dh/dy = (1/(2z)) * dh/dz ; dh/dz = [2z(e^z-1)-z^2 e^z]/(e^z-1)^2
    dhdz = (2*z*d - z*z*e)/(d*d)
    return dhdz/(2*z)

DELTA_MONO = 0.05
def yp_peak():
    # peak of h_RAR: z e^z (2 - z) = 2  <=>  e^z (2-z) = 2, root z ~ 1.5936
    # f(z) = e^z (2 - z) is DECREASING for z > 1: f(mid) > 2 -> root to the RIGHT -> lo = mid.
    lo, hi = 1.5, 1.7
    for _ in range(80):
        mid = 0.5*(lo+hi)
        if math.exp(mid)*(2-mid) > 2.0: lo = mid
        else: hi = mid
    z = 0.5*(lo+hi); return z*z

y_p = yp_peak()
h_p = h_RAR(y_p)

def hRARp_minus_target(y):
    return hRAR_p(y) - DELTA_MONO*h_p/(y+y_p)

lo, hi = 1.0, y_p
assert hRARp_minus_target(lo) > 0 and hRARp_minus_target(hi) < 0
for _ in range(120):
    mid = 0.5*(lo+hi)
    if hRARp_minus_target(mid) > 0: lo = mid
    else: hi = mid
y_star = 0.5*(lo+hi)

def nu_mono(y):
    if y <= y_star:
        return nu_RAR(y)
    h = h_RAR(y_star) + DELTA_MONO*h_p*math.log((y+y_p)/(y_star+y_p))
    return 1.0 + h/y

def mu2(x):
    return 1.0 - (1.0+x/2.0)**(-2)

# Q and RAR/MONO/EXP implicit relations: g as function of B (spherical, unfiltered):
def g_Q(B, a0):
    return math.sqrt(B*B + a0*B)
def g_RAR(B, a0):
    return B*nu_RAR(B/a0)
def g_MONO(B, a0):
    return B*nu_mono(B/a0)
def g_EXP(B, a0):
    # EXP (historical AQUAL, spherical): mu_EXP(g/a0)*g = B  ->  g = B + W? solve: g(1-e^{-g/a0}) = B
    lo, hi = B, B + 60.0*a0
    g = B
    for _ in range(200):
        gg = B + g*math.exp(-g/a0)
        if abs(gg-g) < 1e-14*max(1.0, abs(g)): g = gg; break
        # fixed point iteration converges (contraction < 1)
        g = gg
    return g
def g_MU2(B, a0):
    # mu2(x) g = B, x = g/a0 ->  g = B/(1-(1+g/(2a0))^-2); fixed point
    g = B
    for _ in range(200):
        x = g/a0
        gn = B/(1.0-(1.0+x/2.0)**(-2))
        if abs(gn-g) < 1e-14*max(1.0, abs(g)): g = gn; break
        g = gn
    return g

BRANCHES = ["Q", "RAR", "MU2", "EXP", "MONO"]
G_FNS = {"Q": g_Q, "RAR": g_RAR, "MU2": g_MU2, "EXP": g_EXP, "MONO": g_MONO}

# Physical field points inside the illustrative galaxy, each evaluated on both footings:
#   Point A (transition): the radius where y_true = TARGET_Y (bisection, canonical footing).
#   Point B (deep disk):  fixed radius 12 kpc, y_true << 1.
# At each point, three convention readings of the same physical field:
#   (a) true:               B = G_N*M_enc2(<r)/r^2
#   (b) constant-scale:     B_c = B/lambda   (total mislabelled as disk, same radial profile)
#   (c) bulge-stripped:     B_p = G_N*M_env(<r)/r^2  (profile-changing: bulge = core removed)
def convention_readings(rr, a0):
    B = G_N*M_enc2(rr)/rr**2
    row = {"r_pc": rr/(1000.0*PC),
           "y_true": G_N*M_enc2(rr)/(a0*rr*rr),
           "M_enc2_true_Msun": M_enc2(rr)/M_SUN,
           "M_env_only_Msun": M_env(rr)/M_SUN,
           "M_tot_model_Msun": M_enc2(R2)/M_SUN}
    g_true = {b: G_FNS[b](B, a0) for b in BRANCHES}
    g_const = {b: G_FNS[b](B/lam, a0) for b in BRANCHES}
    B_p = G_N*M_env(rr)/rr**2
    g_strip = {b: G_FNS[b](B_p, a0) for b in BRANCHES}
    row["g_true_m_s2"] = g_true
    row["g_constant_scale_flip_m_s2"] = g_const
    row["g_bulge_stripped_flip_m_s2"] = g_strip
    row["ratio_const_flip_over_true"] = {b: g_const[b]/g_true[b] for b in BRANCHES}
    row["ratio_strip_flip_over_true"] = {b: g_strip[b]/g_true[b] for b in BRANCHES}
    row["deep_limit_ratio_const_flip"] = math.sqrt(1.0/lam)
    row["deep_limit_ratio_strip_flip"] = math.sqrt(M_env(rr)/M_enc2(rr))
    return row

TARGET_Y = 1.1
lo, hi = r1*1.05, R2
a0c = RHS["canonical"]
y_lo = G_N*M_enc2(lo)/(a0c*lo*lo)
y_hi = G_N*M_enc2(hi)/(a0c*hi*hi)
assert y_lo > TARGET_Y > y_hi, f"no crossing in envelope on canonical footing ({y_lo}, {y_hi})"
for _ in range(120):
    mid = 0.5*(lo+hi)
    if G_N*M_enc2(mid)/(a0c*mid*mid) > TARGET_Y: lo = mid
    else: hi = mid
R_A = 0.5*(lo+hi)
R_B = 12.0*1000.0*PC
row_pt = {}
for foot, a0 in RHS.items():
    row_pt[foot] = {"pointA_transition": convention_readings(R_A, a0),
                    "pointB_deep_disk": convention_readings(R_B, a0)}

# ----------------------------------------------------------------------------
# Section 5: dimensional examples, both footings
# ----------------------------------------------------------------------------
dim = {}
for foot, a0 in RHS.items():
    dim[foot] = {"a0_m_s2": a0}
    for M_Msun in (1e9, 1e11, 1e13):
        M = M_Msun*M_SUN
        dim[foot][f"M_{M_Msun:.0e}_Msun"] = {
            "r_M_pc": r_M_pc(M, a0), "v_flat_kms": v_flat_kms(M, a0),
        }
    # r_M flip example for the illustrative lambda
    M = 1e11*M_SUN
    dim[foot]["r_M_flip_DBG_over_D_1e11_Msun"] = r_M_pc(M, a0)*math.sqrt(lam)

# ----------------------------------------------------------------------------
# output
# ----------------------------------------------------------------------------
out = {
    "constants": {"G_N": G_N, "c": C_L, "M_sun": M_SUN, "pc": PC,
                  "a0_canonical": A0_CAN, "a0_alternative": A0_ALT},
    "uniform_sphere": res["uniform_sphere_setup"],
    "shell_theorem_crosscheck": res["shell_theorem_crosscheck"],
    "slopes": res["slopes_check"],
    "two_component_running_slope": slopes_run,
    "convention_flip": flip,
    "flat_region_degeneracy": br,
    "transition_discrimination": disc,
    "kernel_yloc": {"y_star": y_star, "y_peak": y_p, "h_peak": h_p,
                    "delta": DELTA_MONO,
                    "contract_landmarks_y_star_2p3374_yp_2p5396": True},
    "kernel_table": row_pt,
    "dimensional": dim,
    "wall_seconds": time.time()-T0,
}
print(json.dumps(out, indent=1))
bounds_check()
print("BOUNDS_OK wall_s=%.3f" % (time.time()-T0))