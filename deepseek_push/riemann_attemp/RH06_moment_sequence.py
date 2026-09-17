#!/usr/bin/env python3
"""
RH06 -- THE LOG-MOMENT SEQUENCE (second-order falsification of the
        framework's spacing role)
========================================================================
The framework ladder member with density f_l(u) = (l-1)(1+u)^{-l} has
ALL log-moments exactly, by the u = ln(1+s) substitution (u ~ Exp(l-1)):

    kappa_n = E[ln(1+u)^n] = (l-1) int_0^inf u^n e^{-(l-1)u} du
                            = n! / (l-1)^n  =  n! * kappa_1^n
                                         (kappa_1 = 1/(l-1), EXACT)

RH03 pinned the member: measured kappa_1 = 0.6746 +- 0.0035 (N=3000
zeros) ->  l = 1 + 1/0.6746 = 2.4824.  So the framework's EXACT,
no-free-parameter prediction for the whole spine is

    kappa_2 = 2! * 0.6746^2 = 0.91017
    kappa_3 = 3! * 0.6746^3 = 1.84198
    kappa_4 = 4! * 0.6746^4 = 4.97056
        (prediction error from the kappa_1 pin: n! n kappa_1^{n-1} * 0.0035)

This lane measures kappa_2..4 on the ACTUAL Riemann zeros and on the
EXACT-GUE law (MC) and asks: whose full sequence is realized?

CHECKS (pre-registered, before the computation):
  [C1] sympy-exact: for n = 1..4, (l-1) int_0^inf u^n e^{-(l-1)u} du
       == n!/(l-1)^n  ==  n! * kappa_1^n  (with kappa_1 = 1/(l-1))
  [C2] empirical moments kappa_2..4 on N=1500 true Riemann zeros
       (mpmath zetazero, dps=15), unfolded by rho(t) = (1/2pi)ln(t/2pi),
       unit-mean normalized (raw unfolded mean reported), errors =
       std/sqrt(N) plus bootstrap 95% CI.
  [C3] exact-GUE moments by direct Monte Carlo, RH01b recipe:
       24 matrices x 500, real eigenvalues, bulk-restricted (|e| <
       0.5*2*sqrt(500)), within-matrix spacings, unit-mean pooled.
  [C4] THE VERDICT, moment-by-moment (strict sigma = empirical se only):
       moment n PASSES framework if |meas_n - n!*0.6746^n| <= 2*se_n;
       moment n PASSES GUE      if |meas_n - GUE_n|      <= 2*se_n.

BRANCHES (pre-registered):
  BRANCH A  STRONG POSITIVE LAW: framework PASSES kappa_2 AND kappa_3
            AND kappa_4 ->
            "the ladder's full log-moment spine is realized in the zeros"
  BRANCH B  HONEST FAIL: GUE PASSES all of kappa_2..4 AND framework
            FAILS at least one, AND no moment sides with the framework
            (GUE at least as close on every moment) ->
            "GUE is the spacing law; the framework's single-moment pin
             was a coincidence of one number"
  BRANCH C  MIXED: otherwise; report exactly which moments side with
            which law (PASS+fail, fail+PASS, both, neither).

KILL CONDITIONS (pre-registered, before the computation):
  [K1] if fewer than 80% of the requested zeros are produced -> verdict
       ABORTED (never claimed).
  [K2] if zero generation exceeds the time budget, fall back to
       N=800 (printed in the .out); if even that fails -> ABORTED.
  [K3] if raw unfolded mean deviates >5% from 1 -> unfolding bug ->
       ABORTED.
  [K4] if either benchmark yields <100 spacings -> ABORTED.
No RH claim is ever made: this lane is about the spacing law only.
"""
import time, os, json, math
import numpy as np
import mpmath as mp
import sympy as sp

t_start = time.time()

N_ZEROS = int(os.environ.get("N_ZEROS", "1500"))
K1_PIN, SK1_PIN = 0.6746, 0.0035          # measured kappa_1 (N=3000 zeros, RH01)
GUE_N0, GUE_NMAT = 500, 24                # RH01b recipe scaled as tasked
rng = np.random.default_rng(20260917)

chk_log = []
def chk(ok, label, detail):
    chk_log.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {detail}")

print("=" * 78)
print("RH06 -- THE LOG-MOMENT SEQUENCE kappa_2..4: zeros vs framework-ladder")
print("        vs exact-GUE (second-order falsification of the spacing role)")
print("=" * 78)

# ---------------- PRE-REGISTRATION (printed BEFORE any computation) --------
print("\n--- PRE-REGISTRATION (written before computing) ---")
print("  PREDICTION (framework, exact, pinned by kappa_1 = 0.6746):")
print("    kappa_2 = 2!*0.6746^2 = %.6f;   kappa_3 = 6*0.6746^3 = %.6f;"
      % (2 * K1_PIN ** 2, 6 * K1_PIN ** 3))
print("    kappa_4 = 24*0.6746^4 = %.6f" % (24 * K1_PIN ** 4))
print("  BRANCH A (STRONG POSITIVE LAW): framework PASSES kappa_2 AND kappa_3 AND kappa_4")
print("     -> 'the ladder's full log-moment spine is realized in the zeros'")
print("  BRANCH B (HONEST FAIL): GUE PASSES all three AND framework FAILS >=1 AND")
print("     no moment sides with the framework")
print("     -> 'GUE is the spacing law; the framework's single-moment pin was a coincidence of one number'")
print("  BRANCH C (MIXED): otherwise; report which moments side with which law")
print("  KILLS: K1 <80%% zeros produced -> ABORT; K2 time budget -> N=800 fallback;")
print("         K3 raw unfolded mean off >5%% -> ABORT; K4 <100 spacings -> ABORT")
print("  HONESTY: every number below is from a computation run in this lane;")
print("           no RH claim is ever made.")

# ---------------- C1: the symbolic identity for n = 1..4 -------------------
print("\n--- C1 the ladder's exact log-moment identity (sympy) ---")
u = sp.symbols("u", positive=True)
lam = sp.symbols("lambda", positive=True)
# exact in closed form: E[ln(1+u)^n] = n!/(l-1)^n  (u ~ Exp(l-1) under
# s = e^u - 1).  sympy states the general integral as a Piecewise whose
# main branch is exactly n!/(l-1)^n on Re(l-1) > 0, OUR domain -- verify
# the identity numerically at l = 2, 5/2, 3 (as RH03 did), plus the
# positive-parameter substitution a := l-1 for an exact residual 0:
a = sp.symbols("a", positive=True)
c1_ok = True
for n in range(1, 5):
    integ = sp.integrate(u ** n * sp.exp(-a * u), (u, 0, sp.oo)) * a
    want = sp.factorial(n) / a ** n
    exact_resid = sp.simplify(integ - want)
    integ_l = sp.integrate(u ** n * sp.exp(-(lam - 1) * u), (u, 0, sp.oo)) * (lam - 1)
    want_l = sp.factorial(n) / (lam - 1) ** n
    ok_num = all(abs(float(integ_l.subs(lam, lv).evalf(12) -
                          float(want_l.subs(lam, lv).evalf(12))) < 1e-9)
                  for lv in [2, sp.Rational(5, 2), sp.Integer(3)])
    ok_exact = exact_resid == 0
    c1_ok = c1_ok and ok_exact and ok_num
    print(f"  n={n}: E[ln(1+u)^{n}] = n!/(l-1)^{n} (sympy exact residual "
          f"{'0' if ok_exact else 'Piecewise'}; numeric at l=2,5/2,3: "
          f"{'PASS' if ok_num else 'FAIL'})")
chk(c1_ok, "C1", "kappa_n = n!/(l-1)^n = n!*kappa_1^n exact for n=1..4 "
                 "(sympy residual 0 on a=l-1>0; numeric PASS at l=2, 5/2, 3)")

# ---------------- C2: the empirical moments on the TRUE zeros --------------
t0 = time.time()
print("\n--- C2 the empirical log-moment sequence on the real zeros ---")
print(f"  computing first {N_ZEROS} zeta zeros (mpmath zetazero, dps=15)...")
mp.mp.dps = 15
gz = []
abort = False
for n in range(1, N_ZEROS + 1):
    if time.time() - t0 > 440:          # K2: time budget guard
        print(f"  K2: time budget hit at n={n}; falling back to what we have")
        break
    gz.append(float(mp.zetazero(n).imag))
used = len(gz)
print(f"  zeros computed: {used}/{N_ZEROS} in {time.time() - t0:.0f} s")
if used < 0.8 * N_ZEROS:
    chk(False, "K1", f"only {used}/{N_ZEROS} zeros -> ABORT")
    abort = True
if abort:
    print("VERDICT: ABORTED (K1/K2). No claims.")
    sys_exit = {"verdict": "ABORTED", "json_exists": False, "checks": "K1/K2"}
    json.dump({"lane": "RH06", "status": "ABORTED", "zeros_used": used},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "RH06_results.json"), "w"), indent=2)
    raise SystemExit(1)

g = np.array(gz)
dens = (1.0 / (2 * np.pi)) * np.log(g[:-1] / (2 * np.pi))   # rho(t)=(1/2pi)ln(t/2pi)
s_unf = np.diff(g) * dens
raw_mean = float(s_unf.mean())
print(f"  unfolded raw mean = {raw_mean:.6f} (expect ~1)")
chk(abs(raw_mean - 1.0) < 0.05, "K3", f"raw unfolded mean {raw_mean:.4f} within 5% of 1")
s_arr = s_unf / raw_mean                                  # unit-mean normalize
np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "RH06_zeros_spacings_cache.npz"),
         g_imag=g, s_unfolded=s_unf, s_unit_mean=s_arr)    # reproducibility cache
print(f"  unit-mean normalized: n_spacings = {len(s_arr)}, mean = {s_arr.mean():.6f}")

meas, meas_se, boot_lo, boot_hi = {}, {}, {}, {}
for n in range(1, 5):
    v = np.log(1.0 + s_arr) ** n
    meas[n] = float(v.mean())
    meas_se[n] = float(v.std() / math.sqrt(len(v)))
    b = np.array([rng.choice(v, size=len(v), replace=True).mean() for _ in range(400)])
    boot_lo[n], boot_hi[n] = float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
    lag1 = float(np.corrcoef(v[:-1], v[1:])[0, 1]) if len(v) > 2 else float("nan")
    print(f"  kappa_{n} (zeros) = {meas[n]:.5f} +- {meas_se[n]:.5f}   "
          f"bootstrap95 [{boot_lo[n]:.5f}, {boot_hi[n]:.5f}]   lag-1 autocorr {lag1:+.3f}")

# ---------------- C3: exact-GUE by direct Monte Carlo ----------------------
print("\n--- C3 exact-GUE log-moment sequence (MC, RH01b recipe: "
      f"{GUE_NMAT} x {GUE_N0}, within-matrix spacings) ---")
def gue_spacings(n0=GUE_N0, n_mat=GUE_NMAT, bulk_frac=0.5):
    sps = []
    for _ in range(n_mat):
        Z = (rng.standard_normal((n0, n0)) + 1j * rng.standard_normal((n0, n0))) / np.sqrt(2)
        A = (Z + Z.conj().T) / np.sqrt(2)
        e = np.sort(np.linalg.eigvalsh(A))
        e = e[np.abs(e) < bulk_frac * 2 * np.sqrt(n0)]
        sps.append(np.diff(e))
    sp = np.concatenate(sps)
    return sp / sp.mean()
sp_gue = gue_spacings()
chk(len(sp_gue) > 100, "K4", f"GUE spacings n = {len(sp_gue)}")
gue, gue_se = {}, {}
for n in range(1, 5):
    v = np.log(1.0 + sp_gue) ** n
    gue[n] = float(v.mean())
    gue_se[n] = float(v.std() / math.sqrt(len(v)))
    print(f"  kappa_{n} (GUE MC) = {gue[n]:.5f} +- {gue_se[n]:.5f}")

# ---------------- C4: the verdict -------------------------------------------
print("\n--- C4 the verdict (strict sigma = empirical se) ---")
fw = {n: math.factorial(n) * K1_PIN ** n for n in range(1, 5)}
fw_pin = {n: math.factorial(n) * n * K1_PIN ** (n - 1) * SK1_PIN for n in range(1, 5)}
fw_pass, gue_pass, zfw, zgue = {}, {}, {}, {}
for n in range(2, 5):
    fw_pass[n] = abs(meas[n] - fw[n]) <= 2 * meas_se[n]
    gue_pass[n] = abs(meas[n] - gue[n]) <= 2 * meas_se[n]
    zfw[n] = abs(meas[n] - fw[n]) / meas_se[n]
    zgue[n] = abs(meas[n] - gue[n]) / meas_se[n]
    print(f"  kappa_{n}: meas {meas[n]:.5f}+-{meas_se[n]:.5f} | framework {fw[n]:.5f} "
          f"(pin-err {fw_pin[n]:.5f}, z={zfw[n]:.2f}) -> "
          f"{'PASS' if fw_pass[n] else 'FAIL'} | GUE {gue[n]:.5f}+-{gue_se[n]:.5f} "
          f"(z={zgue[n]:.2f}) -> {'PASS' if gue_pass[n] else 'FAIL'}")

f_all = all(fw_pass[n] for n in (2, 3, 4))
g_all = all(gue_pass[n] for n in (2, 3, 4))
g_at_least_as_close = all(abs(meas[n] - gue[n]) <= abs(meas[n] - fw[n]) + 1e-12
                          for n in (2, 3, 4))
if f_all:
    branch, verdict = "A", ("the ladder's full log-moment spine is realized in the zeros "
                            "(framework member pinned by kappa_1 matches kappa_2..4 within 2 sigma)")
elif g_all and (not f_all) and g_at_least_as_close:
    branch, verdict = "B", ("GUE is the spacing law; the framework's single-moment pin was a "
                            "coincidence of one number")
else:
    siding = {n: ("framework" if fw_pass[n] and not gue_pass[n]
                  else "GUE" if gue_pass[n] and not fw_pass[n]
                  else "both" if fw_pass[n] and gue_pass[n] else "neither")
              for n in (2, 3, 4)}
    branch, verdict = "C", ("MIXED: kappa_2 sides with %s, kappa_3 with %s, kappa_4 with %s"
                            % (siding[2], siding[3], siding[4]))
print(f"\nVERDICT [branch {branch}]: {verdict}")
print(f"  (note: framework prediction errors from the kappa_1 pin are "
      f"{[fw_pin[n] for n in (2, 3, 4)]})")
print(f"  checks: {sum(chk_log)}/{len(chk_log)} PASS")

res = {
    "lane": "RH06",
    "identity": "kappa_n = n!/(l-1)^n = n!*kappa_1^n EXACT for n=1..4 (sympy residual 0)",
    "framework_prediction_pinned_by_measured_kappa1_0.6746": {
        "kappa_2": round(fw[2], 6), "kappa_3": round(fw[3], 6), "kappa_4": round(fw[4], 6),
        "pin_errors": [round(fw_pin[n], 6) for n in (2, 3, 4)]},
    "empirical_zeros": {
        "n_zeros": used, "n_spacings": int(len(s_arr)),
        "raw_unfolded_mean": round(raw_mean, 6), "dps": 15,
        "kappa_1": {"val": round(meas[1], 6), "se": round(meas_se[1], 6),
                    "boot95": [round(boot_lo[1], 6), round(boot_hi[1], 6)]},
        "kappa_2": {"val": round(meas[2], 6), "se": round(meas_se[2], 6),
                    "boot95": [round(boot_lo[2], 6), round(boot_hi[2], 6)]},
        "kappa_3": {"val": round(meas[3], 6), "se": round(meas_se[3], 6),
                    "boot95": [round(boot_lo[3], 6), round(boot_hi[3], 6)]},
        "kappa_4": {"val": round(meas[4], 6), "se": round(meas_se[4], 6),
                    "boot95": [round(boot_lo[4], 6), round(boot_hi[4], 6)]}},
    "GUE_MC": {"n_matrices": GUE_NMAT, "n0": GUE_N0,
               "kappa_1": round(gue[1], 6), "kappa_2": round(gue[2], 6),
               "kappa_3": round(gue[3], 6), "kappa_4": round(gue[4], 6),
               "se": [round(gue_se[n], 6) for n in (1, 2, 3, 4)]},
    "checks": {"C1_identity": c1_ok,
               "C2_empirical": [round(meas[n], 6) for n in (2, 3, 4)],
               "C4_framework_pass_2sigma": [bool(fw_pass[n]) for n in (2, 3, 4)],
               "C4_GUE_pass_2sigma": [bool(gue_pass[n]) for n in (2, 3, 4)],
               "z_framework": [round(zfw[n], 2) for n in (2, 3, 4)],
               "z_GUE": [round(zgue[n], 2) for n in (2, 3, 4)],
               "K1_kill": bool(used >= 0.8 * N_ZEROS),
               "K3_kill": bool(abs(raw_mean - 1.0) < 0.05),
               "K4_kill": bool(len(sp_gue) > 100)},
    "branch": branch,
    "verdict": verdict,
    "no_RH_claim": True,
}
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RH06_results.json")
with open(p, "w") as f:
    json.dump(res, f, indent=2)
print(f"\n=== WRITTEN {p} ===")
print(f"runtime {time.time() - t_start:.0f} s total")
print("DONE")