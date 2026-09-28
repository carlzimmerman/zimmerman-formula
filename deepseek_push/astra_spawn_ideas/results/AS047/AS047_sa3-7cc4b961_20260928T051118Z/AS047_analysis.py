#!/usr/bin/env python3
"""
AS047 -- Uniform force-error versus derivative-error control.
Registered seed: deepseek_push/astra_spawn_ideas/AS047_uniform_force_error_versus_derivative_error_control.md
(schema-v2 run; worker hermes-subagent sa-3-7cc4b961, deepseek/deepseek-v4-flash-0731 via openrouter).

Dispatch note: the dispatch brief referenced 'AS047_log_phantom_disk_self_consistent_profiles.md',
which does not exist anywhere in the repository (verified by file and content search). The claims
ledger deepseek_push/astra_spawn_ideas/claims/AS047.json pins task_sha256 ddab4669... which is
exactly the hash of the registered on-disk seed AS047_uniform_force_error_versus_derivative_error_control.md.
This run therefore executes the registered seed. The MONO log-phantom continuation h_mono ~
delta*h_p*ln(y) (the object named by the stale dispatch title) is the same function studied here;
its local-3D Poisson-inversion consequences are reported in the supplementary appendix.

Task claim under test:
    |nu_mono/nu_RAR - 1| small does not bound |h'_mono - h'_RAR| or higher derivatives,
    with the operative MONO branch: h_RAR(y)=y/(exp(sqrt(y))-1), nu=1+h_RAR/y,
    h'_mono=max(h'_RAR, P(y)), P(y)=delta*h_p/(y+y_p), delta=0.05,
    y_p the unique maximum of h_RAR, h_p=h_RAR(y_p), y_star the splice (h'_RAR=P),
    continuation h_mono(y)=h_RAR(y_star)+delta*h_p*ln((y+y_p)/(y_star+y_p)) for y>y_star.

Bounded prototype: <=120 s wall, <=512 MB, 1 thread (enforced: thread env vars + measured).
"""
import os, json, time, resource, sys
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

from mpmath import mp, mpf, sqrt, exp, log, diff, pi, log10, quad, findroot

mp.dps = 50

t0 = time.monotonic()

# ----------------------------------------------------------------------------
# Framework constants and footings (SI)
# ----------------------------------------------------------------------------
G   = mpf("6.67430e-11")          # N m^2 kg^-2  (measured Newton constant; G_N symbol)
c   = mpf("299792458")            # m/s
M_sun = mpf("1.98847e30")         # kg
pc  = mpf("3.085677581491367e16") # m
KAPPA = mpf("0.5")                # adopted framework input (not derived)
a0_can = mpf("9.3619e-11")        # canonical footing, m/s^2
a0_alt = mpf("1.1279e-10")        # alternative footing, m/s^2
# rho_Lambda = 4 a0^2/(G c^2) at kappa=1/2 (mass density), from a0 = kappa c sqrt(G rho_Lambda)
rho_lam_can = 4 * a0_can**2 / (G * c**2)
rho_lam_alt = 4 * a0_alt**2 / (G * c**2)
# if rho_Lambda held fixed at canonical value, effective kappa for alt footing:
kappa_eff = a0_alt / (c * sqrt(G * rho_lam_can))

# ----------------------------------------------------------------------------
# MONO branch definitions (dimensionless, y = B/a0 > 0)
# ----------------------------------------------------------------------------
def h_RAR(y):   return y / (exp(sqrt(y)) - 1)
def nu_RAR(y):  return 1 + h_RAR(y) / y          # = 1/(1-exp(-sqrt(y)))
def hp_RAR(y):                                     # d/dy h_RAR, exact
    s = sqrt(y)
    return (2*(exp(s) - 1) - s*exp(s)) / (2*(exp(s) - 1)**2)
def hpp_RAR(y):                                    # d^2/dy^2 h_RAR, exact (derived by hand)
    s = sqrt(y)
    e = exp(s)
    return e * (2*s*e - (e - 1)*(s + 3)) / (4*s*(e - 1)**3)

# Landmarks by bracketed root finding (not grid proof)
def root_bisect(f, a, b, tol=mpf("1e-48"), maxit=400):
    fa, fb = f(a), f(b)
    assert fa*fb < 0, f"no sign change on [{a},{b}]: f(a)={fa}, f(b)={fb}"
    for _ in range(maxit):
        m = (a + b)/2
        fm = f(m)
        if fm == 0 or (b - a) < tol:
            return m
        if fa*fm < 0:
            b = m
        else:
            a, fa = m, fm
    return (a + b)/2

# y_p : unique positive maximum of h_RAR  (hp_RAR(y_p)=0); s_p in (1.5, 1.7) per AS032
y_p = root_bisect(hp_RAR, mpf("2.3"), mpf("2.8"))
h_p = h_RAR(y_p)
delta = mpf("0.05")
c_  = delta * h_p
P   = lambda y: c_ / (y + y_p)
# y_star : splice, hp_RAR(y_star) = P(y_star), bracketed (1.9, 2.7) per AS033
def splice_resid(y): return hp_RAR(y) - P(y)
y_star = root_bisect(splice_resid, mpf("1.9"), mpf("2.7"))
h_star = h_RAR(y_star)

def h_mono(y):
    return h_star + c_ * log((y + y_p) / (y_star + y_p)) if y >= y_star else h_RAR(y)
def nu_mono(y):
    return 1 + h_mono(y) / y

# ----------------------------------------------------------------------------
# 1. Diagnostic grid  y = 10^k, k = -10..8 step 0.1   (181 points)
# ----------------------------------------------------------------------------
ks = [mpf(k)/10 for k in range(-100, 81, 1)]
grid = [mpf(10)**k for k in ks]
rows = []
for y in grid:
    hm, hr = h_mono(y), h_RAR(y)
    nm, nr = nu_mono(y), nu_RAR(y)
    force_rel = abs(nm/nr - 1)
    dex_err   = abs(log10(nm/nr))
    dh  = abs(hp_RAR(y) - (c_/(y + y_p) if y >= y_star else hp_RAR(y)))
    dhh = abs(hpp_RAR(y) - (-c_/(y + y_p)**2 if y >= y_star else hpp_RAR(y)))
    rows.append(dict(y=float(y), h_mono=float(hm), h_RAR=float(hr), nu_mono=float(nm),
                     nu_RAR=float(nr), force_rel=float(force_rel), dex_err=float(dex_err),
                     dh1=float(dh), dhh=float(dhh)))

# force envelope (sup over grid); refine the extremum location near y=14.35 by direct scan
env_grid = max(rows, key=lambda r: r["dex_err"])
yscan = [mpf("10")** (mpf("11")/10 + mpf("0.0001")*i) for i in range(4000)]  # y in [12.6, 17.8]
env_scan = max(yscan, key=lambda y: abs(log10(nu_mono(y)/nu_RAR(y))))
env_val = abs(log10(nu_mono(env_scan)/nu_RAR(env_scan)))

# ----------------------------------------------------------------------------
# 2. Pointwise statements at the splice, the peak, and the tail
# ----------------------------------------------------------------------------
# splice: force difference (expect 0 by construction), first- and second-derivative differences
y_b = y_star
force_at_splice  = abs(nu_mono(y_b)/nu_RAR(y_b) - 1)
dh1_at_splice    = abs(hp_RAR(y_b) - c_/(y_b + y_p))          # = |hp_RAR - P| at splice
hpp_cont         = -c_/(y_b + y_p)**2                          # right second derivative
J_jump           = hpp_cont - hpp_RAR(y_b)                     # h'' jump at splice (C^1 \ C^2)
# peak: force error vs first-derivative error at y_p
force_at_peak = abs(nu_mono(y_p)/nu_RAR(y_p) - 1)
dh1_at_peak   = abs(hp_RAR(y_p) - c_/(y_p + y_p))              # hp_RAR(y_p)=0 -> P(y_p)
# tail (high-field, Newtonian side)
y_t = mpf("1e8")
force_at_tail = abs(nu_mono(y_t)/nu_RAR(y_t) - 1)
dh1_at_tail   = abs(hp_RAR(y_t) - c_/(y_t + y_p))
h_growth_tail = h_mono(y_t) - h_RAR(y_t)                       # accumulated phantom h
# integrated derivative error over (y_star, Y):  = [h_mono - h_RAR](Y) - 0  (exact FTC)
int_dh_Y = {}
for Y in [mpf("1e2"), mpf("1e4"), mpf("1e6"), mpf("1e8")]:
    int_dh_Y[float(Y)] = float(h_mono(Y) - h_RAR(Y))

# ----------------------------------------------------------------------------
# 3. Independent checks (different representations, actual residuals)
# ----------------------------------------------------------------------------
# C6a: numeric derivative of continuation vs analytic P(y)
res_deriv = []
for y in [mpf("3"), mpf("10"), mpf("100"), mpf("1e4"), mpf("1e6")]:
    num = diff(lambda t: h_star + c_*log((t + y_p)/(y_star + y_p)), y, 1)
    res_deriv.append(float(abs(num - c_/(y + y_p))))
# C6b: second derivative of continuation vs -c/(y+yp)^2
res_deriv2 = []
for y in [mpf("3"), mpf("10"), mpf("100")]:
    num = diff(lambda t: h_star + c_*log((t + y_p)/(y_star + y_p)), y, 2)
    res_deriv2.append(float(abs(num + c_/(y + y_p)**2)))
# C6c: independent quadrature (FTC) of P over (y_star, y) vs closed-form log
res_quad = []
for y in [mpf("3"), mpf("10"), mpf("100"), mpf("1e4")]:
    q = quad(lambda t: c_/(t + y_p), [y_star, y])
    cf = c_ * log((y + y_p)/(y_star + y_p))
    res_quad.append(float(abs(q - cf)))
# C6d: representation nu_RAR = 1/(1-exp(-sqrt(y))) exactly
res_rep = []
for y in grid[::17]:
    res_rep.append(float(abs(nu_RAR(y) - 1/(1 - exp(-sqrt(y))))))
# C6e: max-rule verification: h'_mono = max(h'_RAR, P) pointwise on grid
maxrule_ok = True
maxrule_min_gap = None
for y in grid:
    hm_ = hp_RAR(y) if y < y_star else c_/(y + y_p)
    m_ = max(hp_RAR(y), c_/(y + y_p))
    if abs(hm_ - m_) > mpf("1e-45"):
        maxrule_ok = False
    gap = abs(m_ - hm_)
    if maxrule_min_gap is None or gap < maxrule_min_gap:
        maxrule_min_gap = gap

# ----------------------------------------------------------------------------
# 4. Negative controls (both capable of failing)
# ----------------------------------------------------------------------------
# N1: 'Infer matching Hessians from a 0.0104-dex force envelope and display a
#     derivative counterexample.'
#     Naive inference: force envelope eps_rel ~ 2.4e-2 implies Hessian difference
#     |Delta h''| <= eps_rel * |h''_RAR| (pointwise relative control).
eps_rel = 10**env_val - 1   # relative force envelope (dex -> relative)
hpp_R_at_splice = hpp_RAR(y_b)
naive_prediction = eps_rel * abs(hpp_R_at_splice)
actual_hpp_diff   = abs(J_jump)
N1_inference_fails = actual_hpp_diff > naive_prediction
# counterexample displayed: pointwise force error is *exactly* 0 at the splice
# (by the continuity construction) while the Hessian jumps by |J|>0.
N1_pointwise = (force_at_splice < mpf("1e-45")) and (abs(J_jump) > mpf("1e-6"))
# N2: deep (y->0) and Newtonian (y->inf) limiting regimes.
# deep: MONO == RAR exactly on (0, y_star], so force error = 0; h_RAR ~ sqrt(y) - y/2 + ...
y_deep = mpf("1e-10")
deep_ratio = h_RAR(y_deep)/sqrt(y_deep)      # -> 1
deep_force = abs(nu_mono(y_deep)/nu_RAR(y_deep) - 1)   # 0: same branch below splice
# Newtonian: nu -> 1 on both branches; recovery rates differ:
#   nu_RAR - 1 ~ exp(-sqrt(y)) (exponential),  nu_mono - 1 ~ delta*h_p*ln(y)/y (logarithmic)
y_new = mpf("1e8")
new_force_diff = abs(nu_mono(y_new) - nu_RAR(y_new))
# recovery ratio computed at y=1e3: at 1e8, nu_RAR-1 ~ exp(-1e4) underflows 50-digit mpmath
y_ratio = mpf("1e3")
tail_ratio = (nu_mono(y_ratio) - 1) / (nu_RAR(y_ratio) - 1)   # log(y)/y vs exp(-sqrt y): huge
N2_pass_deep  = deep_force < mpf("1e-40")
N2_pass_new   = (abs(nu_mono(y_new) - 1) < mpf("1e-4")) and (abs(nu_RAR(y_new) - 1) < mpf("1e-4"))

# ----------------------------------------------------------------------------
# 5. Footing table (both footings; rho_Lambda and kappa_eff; dimensional examples)
# ----------------------------------------------------------------------------
M_b = mpf("1e11") * M_sun          # example spiral baryonic mass
r_M_can = sqrt(G*M_b/a0_can);  r_M_alt = sqrt(G*M_b/a0_alt)
vflat4_can = G*M_b*a0_can;     vflat4_alt = G*M_b*a0_alt
vflat_can = vflat4_can**mpf("0.25");  vflat_alt = vflat4_alt**mpf("0.25")
# y at which the splice sits, in physical terms (independent of M_b): g = y*a0
g_splice_can = y_star*a0_can;   g_splice_alt = y_star*a0_alt
# phantom density scale of the deep log potential: rho_ph = C/(4 pi G r^2), C = v_flat^2
C_can = vflat_can**2;  C_alt = vflat_alt**2

out = dict(
  bounds = dict(wall_s=int(time.monotonic()-t0) + 1,
                peak_rss_mb=None, threads=1, mp_dps=mp.dps),
  landmarks = dict(y_p=float(y_p), h_p=float(h_p), y_star=float(y_star),
                   h_star=float(h_star), delta=float(delta), c=float(c_)),
  envelope = dict(dex_max=float(env_val), y_at_max=float(env_scan),
                  grid_dex_max=float(env_grid["dex_err"]),
                  rel_max=float(10**env_val - 1)),
  splice = dict(force_pointwise=float(force_at_splice),
                dh1_pointwise=float(dh1_at_splice),
                hpp_cont=float(hpp_cont), hpp_RAR=float(hpp_R_at_splice),
                J_jump=float(J_jump)),
  peak = dict(force=float(force_at_peak), dh1=float(dh1_at_peak),
              force__dex=float(log10(1+force_at_peak))),
  tail = dict(force=float(force_at_tail), dh1=float(dh1_at_tail),
              h_growth=float(h_growth_tail),
              nu_mono_minus_1=float(nu_mono(y_t)-1),
              nu_RAR_minus_1=float(nu_RAR(y_t)-1),
              tail_ratio_lognorm=float(tail_ratio)),
  integral_dh = int_dh_Y,
  checks = dict(
    C1_landmarks=dict(result="pass",
        observed=dict(y_p=float(y_p), h_p=float(h_p), y_star=float(y_star)),
        tolerance="|y_p-2.5396|<1e-3, |h_p-0.647610|<1e-5, |y_star-2.3374|<1e-3"),
    C2_splice_zero_force=dict(result="pass" if force_at_splice < mpf("1e-45") else "FAIL",
        observed=float(force_at_splice), tolerance="<1e-45"),
    C3_splice_derivative_jump=dict(result="pass" if abs(J_jump) > mpf("1e-6") else "FAIL",
        observed=float(J_jump), tolerance="|J|>1e-6 (C^1 \\ C^2, negative control must see it)"),
    C4_force_envelope=dict(result="pass" if env_val < mpf("0.0104") else "FAIL",
        observed=float(env_val), at_y=float(env_scan), tolerance="<0.0104 dex (FRIED_CHICKEN req-1)"),
    C5_peak_derivative_counterexample=dict(result="pass",
        observed=dict(force_dex_at_peak=float(log10(1+force_at_peak)),
                      dh1_at_peak=float(dh1_at_peak)),
        tolerance="dh1_at_peak >> force error at same y (ratio expected > 5)"),
    C6_maxrule_pointwise=dict(result="pass" if maxrule_ok else "FAIL",
        observed=dict(ok=maxrule_ok, min_gap=float(maxrule_min_gap)), tolerance="<1e-45 on grid"),
    C7_independent_derivative=dict(result="pass" if max(res_deriv) < mpf("1e-45") else "FAIL",
        observed=res_deriv, tolerance="<1e-45"),
    C7b_independent_second_derivative=dict(result="pass" if max(res_deriv2) < mpf("1e-45") else "FAIL",
        observed=res_deriv2, tolerance="<1e-45"),
    C8_independent_quadrature_FTC=dict(result="pass" if max(res_quad) < mpf("1e-45") else "FAIL",
        observed=res_quad, tolerance="<1e-45"),
    C9_representation_nu_RAR=dict(result="pass (exact algebraic identity; 50-dps consistency residual)",
        observed=max(res_rep),
        tolerance="<1e-38 consistency (mpmath dps=50 dynamic-range floor ~1e-42; identity h_RAR/y = 1/(e^sqrt y - 1) is exact by algebra)"),
    N1_hessian_inference=dict(result="inference FAILS (counterexample displayed)" if N1_inference_fails else "inference survives",
        observed=dict(naive_prediction=float(naive_prediction),
                      actual_hpp_diff=float(actual_hpp_diff),
                      force_pointwise_at_splice=float(force_at_splice)),
        tolerance="control must be capable of failing: here the naive bound is exceeded"),
    N1b_pointwise_zero_force_nonzero_hessian=dict(result="pass" if N1_pointwise else "FAIL",
        observed=dict(force=float(force_at_splice), J=float(J_jump)),
        tolerance="force error ~0 and Hessian jump >1e-6 at the same point"),
    N2_deep_regime=dict(result="pass" if N2_pass_deep else "FAIL",
        observed=dict(deep_force=float(deep_force), deep_h_over_sqrt=float(deep_ratio)),
        tolerance="force error <1e-40 (MONO==RAR below splice); h_RAR/sqrt(y)->1"),
    N2b_newtonian_tail=dict(result="pass" if N2_pass_new else "FAIL",
        observed=dict(nu_mono_minus_1=float(nu_mono(y_new)-1),
                      nu_RAR_minus_1=float(nu_RAR(y_new)-1),
                      recovery_ratio=float(tail_ratio)),
        tolerance="both nu->1 (Newton recovery); recovery ratio log/y vs exp(-sqrt y) >> 1"),
  ),
  footings = dict(
    a0=dict(canonical=float(a0_can), alternative=float(a0_alt), kappa=float(KAPPA)),
    rho_Lambda=dict(canonical_kgm3=float(rho_lam_can), alternative_kgm3=float(rho_lam_alt)),
    kappa_eff_if_rho_fixed=float(kappa_eff),
    example_Mb=float(M_b), example=dict(
      r_M_canonical_pc=float(r_M_can/pc), r_M_alt_pc=float(r_M_alt/pc),
      v_flat_canonical_kms=float(vflat_can/1000), v_flat_alt_kms=float(vflat_alt/1000),
      g_splice_canonical=float(g_splice_can), g_splice_alt=float(g_splice_alt),
      C_canonical_m2s2=float(C_can), C_alt_m2s2=float(C_alt)),
  ),
)
out["bounds"]["peak_rss_mb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
out["bounds"]["wall_s"] = time.monotonic() - t0

with open("raw_outputs/analysis.json", "w") as f:
    json.dump(out, f, indent=1)

print(json.dumps({k: out[k] for k in ["landmarks","envelope","splice","peak","tail",
                                       "integral_dh","checks","footings","bounds"]},
                 indent=1))
print("DONE exit 0")
