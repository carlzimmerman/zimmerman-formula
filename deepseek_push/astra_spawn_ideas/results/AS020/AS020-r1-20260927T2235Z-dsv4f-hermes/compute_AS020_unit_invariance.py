#!/usr/bin/env python3
"""
AS020 — Scale-relation invariance under unit changes.

CORE scale cell of the Zimmerman framework (branch: CORE scale identities):

    a0  = kappa * c * sqrt(G * rho_Lambda)          (kappa = 1/2 ADOPTED)
    rho_Lambda = 4 a0^2 / (G c^2)
    r_M  = sqrt(G*M_b/a0),  v_flat^4 = G*M_b*a0,  C = sqrt(G*M_b*a0),  sigma^2 = C/2

Claim under test: every relation in this cell is invariant under CONSISTENT
changes of units (one new unit per base dimension):

    a0' = a0 * T_u^2 / L_u ;  G' = G * M_u * T_u^2 / L_u^3 ;
    rho' = rho * L_u^3 / M_u ;  c' = c * T_u / L_u ;  M' = M / M_u

(value in new units for a quantity of dimension M^b L^a T^g:
 v' = v * L_u^{-a} * M_u^{-b} * T_u^{-g}); quantities change numerically but
every dimensionless combination is exactly preserved; and the task-mandated
negative control (lengths converted, a0 left at its SI number) MUST fail,
along with the hybrid galactic convention (kpc, km/s, M_sun), which is not a
rescaling and which forces explicit (kpc/km) factors into every relation.

High precision (mpmath, 80 digits) so every check is a real residual, not a
Boolean.  Single-threaded; wall-clock alarm at 120 s actual enforced bound.
No observational fit is performed.

Usage:  python3 compute_AS020_unit_invariance.py > raw_output.txt 2>&1
"""
import json
import signal
import time
import resource
import sys
import mpmath as mp

WALL_S = 120


def _alarm(_signum, _frame):
    raise TimeoutError("AS020 prototype exceeded the 120 s wall-clock bound")


signal.signal(signal.SIGALRM, _alarm)
signal.alarm(WALL_S)
t_start = time.monotonic()

mp.mp.dps = 80

# ---------------------------------------------------------------------------
# declared constants (SI; FRAMEWORK_CONTRACT numerics)
# ---------------------------------------------------------------------------
G_N = mp.mpf("6.67430e-11")           # measured Newton coupling, m^3 kg^-1 s^-2
c = mp.mpf("299792458")               # exact, m/s
M_sun = mp.mpf("1.98847e30")          # kg
pc = mp.mpf("3.085677581491367e16")   # m
yr = mp.mpf("31557600")               # Julian year, s
AU = mp.mpf("149597870700")           # m
k_B = mp.mpf("1.380649e-23")          # J/K (declared, NOT used in this cell)
kappa = mp.mpf("0.5")                 # adopted normalization (framework input)

A0_CAN = mp.mpf("9.3619e-11")         # canonical footing, m/s^2
A0_ALT = mp.mpf("1.1279e-10")         # alternative footing, m/s^2 (SEPARATE hypothesis)


def rho_of(a0):
    return 4 * a0 * a0 / (G_N * c * c)


RHO_LAM = rho_of(A0_CAN)
RHO_TOT = rho_of(A0_ALT)

# exponent vectors (M, L, T)
DIM = {
    "a0": (0, 1, -2), "c": (0, 1, -1), "G": (-1, 3, -2),
    "rho": (1, -3, 0), "M": (1, 0, 0),
}


def transform(value, dimv, Lu, Mu, Tu):
    b, a, g = dimv
    return value * mp.power(Lu, -a) * mp.power(Mu, -b) * mp.power(Tu, -g)


SYSTEMS = [
    ("SI (m,kg,s)",    1,            1,            1),
    ("km-s-kg",      1000,            1,            1),
    ("m-s-g",           1,    mp.mpf("1e-3"),       1),
    ("km-s-g",       1000,    mp.mpf("1e-3"),       1),
    ("m-yr-kg",         1,            1,            yr),
    ("km-yr-g",      1000,    mp.mpf("1e-3"),       yr),
    ("kpc-s-Msun", pc*1000,        M_sun,           1),
    ("pc-yr-Msun",    pc,            M_sun,         yr),
    ("au-yr-Msun",    AU,            M_sun,         yr),
]

TOL = mp.mpf("1e-60")
results = {"checks": [], "residuals": {}, "witnesses": {}}
failures = []


def check(name, ok, detail=""):
    results["checks"].append({"name": name, "pass": bool(ok), "detail": str(detail)})
    if not ok:
        failures.append(name)
    print(("[PASS] " if ok else "[FAIL] ") + name + (("  -- " + str(detail)) if detail else ""))


def relerr(a, b):
    d = a - b
    return mp.mpf(0) if d == 0 else d / b


# ===========================================================================
# 1.  Pi = a0/(c*sqrt(G*rho)) invariance under consistent rescaling
# ===========================================================================
print("=" * 78)
print("SECTION 1: Pi = a0/(c*sqrt(G*rho)) invariance under consistent rescaling")
print("=" * 78)
for A0, foot, rho in ((A0_CAN, "canonical", RHO_LAM), (A0_ALT, "alternative", RHO_TOT)):
    for (name, Lu, Mu, Tu) in SYSTEMS:
        a0p = transform(A0, DIM["a0"], Lu, Mu, Tu)
        cp = transform(c, DIM["c"], Lu, Mu, Tu)
        Gp = transform(G_N, DIM["G"], Lu, Mu, Tu)
        rhop = transform(rho, DIM["rho"], Lu, Mu, Tu)
        Pi = a0p / (cp * mp.sqrt(Gp * rhop))
        key = f"Pi_{foot}_{name}"
        results["residuals"][key] = {"Pi": str(Pi), "residual_vs_kappa": str(relerr(Pi, kappa))}
        check(f"Pi == kappa = 1/2  [{foot}, {name}]",
              abs(Pi - kappa) < TOL,
              f"Pi = {mp.nstr(Pi, 20)}; residual {mp.nstr(relerr(Pi, kappa), 5)}")

# ===========================================================================
# 2.  Derived scales r_M, v_flat, C, sigma -- numbers change, relations exact
# ===========================================================================
print("=" * 78)
print("SECTION 2: derived scales transform covariantly; relations exact")
print("=" * 78)
M_b = M_sun
for A0, foot in ((A0_CAN, "canonical"), (A0_ALT, "alternative")):
    rM_si = mp.sqrt(G_N * M_b / A0)
    v4_si = G_N * M_b * A0
    v_si = mp.power(v4_si, mp.mpf("0.25"))
    C_si = mp.sqrt(v4_si)
    sig_si = mp.sqrt(C_si / 2)
    results["witnesses"][f"SI_{foot}"] = {
        "a0[m/s^2]": mp.nstr(A0, 20),
        "rho[kg/m^3]": mp.nstr(rho_of(A0), 22),
        "r_M(Msun)[m]": mp.nstr(rM_si, 22),
        "r_M(Msun)[pc]": mp.nstr(rM_si / pc, 15),
        "v_flat(Msun)[m/s]": mp.nstr(v_si, 22),
        "C(Msun)[m^2/s^2]": mp.nstr(C_si, 22),
        "sigma(Msun)[m/s]": mp.nstr(sig_si, 22),
    }
    for (name, Lu, Mu, Tu) in SYSTEMS:
        a0p = transform(A0, DIM["a0"], Lu, Mu, Tu)
        Gp = transform(G_N, DIM["G"], Lu, Mu, Tu)
        Mbp = transform(M_b, DIM["M"], Lu, Mu, Tu)
        rMp = mp.sqrt(Gp * Mbp / a0p)
        v4p = Gp * Mbp * a0p
        Cp = mp.sqrt(v4p)
        sigp = mp.sqrt(Cp / 2)
        r = {
            "rM_transforms_as_L^-1": relerr(rMp, rM_si / Lu),
            "v4_rel_preserved": relerr(v4p / (Gp * Mbp * a0p), 1),
            "C_eq_a0_rM": relerr(Cp / (a0p * rMp), 1),
            "sigma2_eq_C_over_2": relerr(sigp * sigp / (Cp / 2), 1),
            "vflat4_vs_SI": relerr(v4p, v4_si * mp.power(Tu, 4) / mp.power(Lu, 4)),
        }
        key = f"derived_{foot}_{name}"
        results["residuals"][key] = {k2: str(v) for k2, v in r.items()}
        for k2, v in r.items():
            check(f"{k2} exact  [{foot}, {name}]", abs(v) < TOL, f"residual {mp.nstr(v, 5)}")
    check(f"v_flat^2 == C  (SI, {foot})", abs(v_si * v_si - C_si) < TOL)
    check(f"C == a0*r_M  (SI, {foot})", abs(C_si - A0 * rM_si) < TOL)
    check(f"sigma == v_flat/sqrt(2)  (SI, {foot})", abs(sig_si * mp.sqrt(2) - v_si) < TOL)

# ===========================================================================
# 3.  Normalization identity survives in every system; footing ratio invariant
# ===========================================================================
print("=" * 78)
print("SECTION 3: normalization rho = 4 a0^2/(G c^2); footing ratio invariant")
print("=" * 78)
for A0, foot, rho in ((A0_CAN, "canonical", RHO_LAM), (A0_ALT, "alternative", RHO_TOT)):
    for (name, Lu, Mu, Tu) in SYSTEMS:
        a0p = transform(A0, DIM["a0"], Lu, Mu, Tu)
        Gp = transform(G_N, DIM["G"], Lu, Mu, Tu)
        cp = transform(c, DIM["c"], Lu, Mu, Tu)
        rhop_back = 4 * a0p * a0p / (Gp * cp * cp)
        rhop = transform(rho, DIM["rho"], Lu, Mu, Tu)
        results["residuals"][f"norm_{foot}_{name}"] = {
            "rho_back_vs_rho_prime": str(relerr(rhop_back, rhop))}
        check(f"normalization identity survives  [{foot}, {name}]",
              abs(rhop_back - rhop) < TOL,
              f"residual {mp.nstr(relerr(rhop_back, rhop), 5)}")
rat_km = transform(A0_ALT, DIM["a0"], 1000, 1, 1) / transform(A0_CAN, DIM["a0"], 1000, 1, 1)
results["residuals"]["footing_ratio_km"] = str(relerr(rat_km, A0_ALT / A0_CAN))
check("a0_alt/a0_can invariant under m->km", abs(rat_km - A0_ALT / A0_CAN) < TOL)
rat_yr = transform(A0_ALT, DIM["a0"], pc, M_sun, yr) / transform(A0_CAN, DIM["a0"], pc, M_sun, yr)
check("a0_alt/a0_can invariant under pc-Msun-yr", abs(rat_yr - A0_ALT / A0_CAN) < TOL)

# ===========================================================================
# 4.  NEGATIVE CONTROL (task-mandated, capable of failing):
#     convert lengths (and masses) but LEAVE a0 at its SI number.
# ===========================================================================
print("=" * 78)
print("SECTION 4: NEGATIVE CONTROL — lengths converted, a0 left in SI")
print("=" * 78)
Lu, Tu = 1000, 1                      # m -> km only
for A0, foot, rho in ((A0_CAN, "canonical", RHO_LAM), (A0_ALT, "alternative", RHO_TOT)):
    a0_wrong = A0                     # NOT converted (deliberate corruption)
    cp = transform(c, DIM["c"], Lu, 1, Tu)
    Gp = transform(G_N, DIM["G"], Lu, 1, Tu)
    rhop = transform(rho, DIM["rho"], Lu, 1, Tu)
    Pi_bad = a0_wrong / (cp * mp.sqrt(Gp * rhop))
    pred = kappa * Lu / (Tu * Tu)     # exact failure factor: L_u / T_u^2
    results["residuals"][f"neg_control_{foot}"] = {
        "Pi_bad": str(Pi_bad), "Pi_SI": str(kappa),
        "Pi_bad_over_kappa": str(Pi_bad / kappa),
        "predicted_factor_Lu_ov_Tu2": str(Lu / (Tu * Tu)),
        "matches_prediction": str(relerr(Pi_bad, pred))}
    check(f"NEGATIVE CONTROL: Pi fails by exactly L_u  [{foot}]",
          abs(Pi_bad - pred) < TOL and abs(Pi_bad - kappa) > mp.mpf("1e-3"),
          f"Pi_bad = {mp.nstr(Pi_bad, 12)} vs kappa = {mp.nstr(kappa, 12)}"
          f"  (factor {mp.nstr(Pi_bad / kappa, 12)})")

# ===========================================================================
# 5.  NEGATIVE CONTROL B: the two footings cannot share (rho, kappa)
# ===========================================================================
print("=" * 78)
print("SECTION 5: NEGATIVE CONTROL B — mixed footings give Pi != kappa")
print("=" * 78)
Pi_mix = A0_ALT / (c * mp.sqrt(G_N * RHO_LAM))     # alt a0 over canonical density
k_eff = kappa * A0_ALT / A0_CAN                    # kappa_eff at fixed rho_Lambda
results["residuals"]["neg_control_footing_mix"] = {
    "Pi_alt_over_canon_rho": str(Pi_mix),
    "effective_kappa": str(k_eff),
    "residual_vs_kappa_eff": str(relerr(Pi_mix, k_eff))}
results["witnesses"]["kappa_eff_fixed_rho_Lambda"] = mp.nstr(k_eff, 15)
check("mixed footing: Pi = kappa_eff != 1/2 (alt a0, canonical rho)",
      abs(Pi_mix - k_eff) < TOL and abs(Pi_mix - kappa) > mp.mpf("1e-3"),
      f"Pi_mix = {mp.nstr(Pi_mix, 12)}, kappa_eff = {mp.nstr(k_eff, 12)}")

# ===========================================================================
# 6.  Hybrid galactic convention (kpc, km/s, M_sun) — hidden unit choice.
#     G is quoted as kpc*(km/s)^2/M_sun (L^3 split 1 kpc + 2 km), densities in
#     M_sun/kpc^3, a0 and c in km/s-kind units.  This is NOT a rescaling of the
#     base units, and every relation picks up an explicit (kpc/km) power.
#     The exact exponents are computed and checked here.
# ===========================================================================
print("=" * 78)
print("SECTION 6: hybrid galactic convention (kpc, km/s, M_sun)")
print("=" * 78)
KPC = pc * 1000                                   # m per kpc
for A0, foot, rho in ((A0_CAN, "canonical", RHO_LAM), (A0_ALT, "alternative", RHO_TOT)):
    a0h = A0 / 1000                               # km/s^2
    ch = c / 1000                                 # km/s
    Mbh = M_b / M_sun                             # M_sun
    Gh = G_N * M_sun / KPC / (1000 ** 2)          # kpc * (km/s)^2 / M_sun  (conventional 4.3009e-6)
    rhoh = rho * KPC ** 3 / M_sun                 # M_sun / kpc^3
    Pi_h = a0h / (ch * mp.sqrt(Gh * rhoh))
    v_si = mp.power(G_N * M_b * A0, mp.mpf("0.25"))
    vh = v_si / 1000                              # correct deep speed, km/s
    v4h = Gh * Mbh * a0h
    factor_pi = Pi_h / kappa
    factor_v4 = vh ** 4 / v4h
    kpc_over_km = KPC / 1000
    # the consistent (km, s, M_sun) system -- everything with km lengths:
    G_allkm = G_N * M_sun / (1000 ** 3)
    rho_allkm = rho * (1000 ** 3) / M_sun
    v4fix = G_allkm * Mbh * a0h
    Pi_fix = a0h / (ch * mp.sqrt(G_allkm * rho_allkm))
    results["residuals"][f"hybrid_{foot}"] = {
        "G_hybrid[kpc(km/s)^2/Msun]": str(Gh),
        "rho_hybrid[Msun/kpc^3]": str(rhoh),
        "Pi_hybrid": str(Pi_h),
        "Pi_hybrid_over_kappa": str(factor_pi),
        "kpc_over_km": str(kpc_over_km),
        "log(Pi-factor)/log(kpc/km)": str(mp.log(factor_pi) / mp.log(kpc_over_km)),
        "v4_hybrid_mismatch_factor": str(factor_v4),
        "log(v4-factor)/log(kpc/km)": str(mp.log(factor_v4) / mp.log(kpc_over_km)),
        "Pi_fixed_residual": str(relerr(Pi_fix, kappa)),
        "v4_fixed_residual": str(relerr(v4fix, vh ** 4))}
    check(f"HYBRID DETECTED: Pi_hybrid != kappa  [{foot}]",
          abs(Pi_h - kappa) > mp.mpf("1e-3"),
          f"Pi_hybrid = {mp.nstr(Pi_h, 12)};  kappa = 0.5")
    check(f"Pi mismatch is exactly (kpc/km)^-1  [{foot}]",
          abs(mp.log(factor_pi) / mp.log(kpc_over_km) - (-1)) < mp.mpf("1e-55"),
          f"exponent {mp.nstr(mp.log(factor_pi) / mp.log(kpc_over_km), 10)}")
    check(f"v4 mismatch is exactly (kpc/km)^+1  [{foot}]",
          abs(mp.log(factor_v4) / mp.log(kpc_over_km) - 1) < mp.mpf("1e-55"),
          f"exponent {mp.nstr(mp.log(factor_v4) / mp.log(kpc_over_km), 10)}")
    check(f"consistent (km,s,Msun) system restores Pi and deep law  [{foot}]",
          abs(Pi_fix - kappa) < TOL and abs(v4fix - vh ** 4) < TOL,
          f"residuals {mp.nstr(relerr(Pi_fix, kappa), 5)}, {mp.nstr(relerr(v4fix, vh**4), 5)}")
    results["witnesses"][f"hybrid_{foot}"] = {
        "G[kpc(km/s)^2/Msun]": mp.nstr(Gh, 15),
        "rho[Msun/kpc^3]": mp.nstr(rhoh, 15),
        "a0[km/s^2]": mp.nstr(a0h, 18),
        "c[km/s]": mp.nstr(ch, 12)}

# ===========================================================================
# 7.  Numeric witnesses on both footings in several unit systems
# ===========================================================================
print("=" * 78)
print("SECTION 7: numeric witnesses (both footings)")
print("=" * 78)
for A0, foot, rho in ((A0_CAN, "canonical", RHO_LAM), (A0_ALT, "alternative", RHO_TOT)):
    w = {
        "a0[m/s^2]": mp.nstr(A0, 20),
        "a0[km/s^2]": mp.nstr(A0 / 1000, 20),
        "a0[pc/yr^2]": mp.nstr(transform(A0, DIM["a0"], pc, 1, yr), 15),
        "rho[kg/m^3]": mp.nstr(rho, 22),
        "rho[g/cm^3]": mp.nstr(transform(rho, DIM["rho"], 100, mp.mpf("1e-3"), 1), 15),
        "rho[Msun/kpc^3]": mp.nstr(transform(rho, DIM["rho"], KPC, M_sun, 1), 15),
        "r_M(Msun)[pc]": mp.nstr(mp.sqrt(G_N * M_sun / A0) / pc, 15),
        "v_flat(Msun)[km/s]": mp.nstr(mp.power(G_N * M_sun * A0, mp.mpf("0.25")) / 1000, 15),
        "sigma(Msun)[km/s]": mp.nstr(mp.sqrt(mp.sqrt(G_N * M_sun * A0) / 2) / 1000, 15),
    }
    results["witnesses"][foot] = w
    for k2, v in w.items():
        print(f"  [{foot}]  {k2:<25} = {v}")

# ===========================================================================
# 8.  Rounding covariance (declared-digit conventions are not unit changes)
# ===========================================================================
print("=" * 78)
print("SECTION 8: rounding covariance of a 5-sf declared a0 across systems")
print("=" * 78)
worst = mp.mpf(0)
for (name, Lu, Mu, Tu) in SYSTEMS:
    a0p = transform(A0_CAN, DIM["a0"], Lu, Mu, Tu)
    cp = transform(c, DIM["c"], Lu, Mu, Tu)
    Gp = transform(G_N, DIM["G"], Lu, Mu, Tu)
    rhop = transform(RHO_LAM, DIM["rho"], Lu, Mu, Tu)
    worst = max(worst, abs(relerr(a0p / (cp * mp.sqrt(Gp * rhop)), kappa)))
results["residuals"]["rounding_note"] = {
    "worst_|Pi-kappa|/kappa_over_9_systems_5sf_a0": str(worst)}
check("rounding covariance: departures from kappa uniform (<1e-4) across systems",
      worst < mp.mpf("1e-4"), f"worst {mp.nstr(worst, 5)}")

# ===========================================================================
#  finish
# ===========================================================================
signal.alarm(0)
t_el = time.monotonic() - t_start
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
bounds = {
    "wall_clock_s": round(t_el, 3),
    "wall_clock_enforced_limit_s": WALL_S,
    "threads": 1,
    "precision_digits_mpmath": 80,
}
if sys.platform == "darwin":       # macOS ru_maxrss is in BYTES
    bounds["maxrss_raw_bytes_macos"] = rss
    rss = rss // 1024
bounds["maxrss_kib"] = rss
results["bounds"] = bounds
print("=" * 78)
print(f"observed wall time {t_el:.3f} s (enforced limit {WALL_S} s); max RSS {rss} KiB; "
      f"1 thread; mpmath {mp.mp.dps} digits")
print(f"TOTAL CHECKS {len(results['checks'])}  FAILURES {len(failures)}")
if failures:
    print("FAILED: " + ", ".join(failures))
    sys.exit(1)
print("ALL CHECKS PASSED")
results["verdict"] = "ALL CHECKS PASSED"
with open("residuals.json", "w") as f:
    json.dump(results, f, indent=1)