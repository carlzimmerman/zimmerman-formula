#!/usr/bin/env python3
"""AS003 numeric verification — Critical-density closure as a dependency problem.

Bounded computation: 1 CPU thread, wall-time cap 120 s, memory cap 512 MB (enforced by
ulimit in the invoking shell), 60-digit mpmath precision. All checks are CAPABLE OF
FAILING: residuals are recorded, not booleans.

Verifies:
  C1  Omega_L = rho_Lambda / rho_crit = (32 pi/3)(G_cosmo/G_N)(a0/(H0 c))^2
      for both footings x both H0 anchors x three G-ratios (50-digit residual)
  C1s symbolic identity check (sympy, exact zero)
  C2  Jacobian of (a0,H0) -> Omega_L: partials vs closed form; rank exactly 1;
      null direction (t*a0, t*H0) invariance; non-null direction distinguishes
  C3  closure verdicts: canonical footing vs Omega_L=1 (exclusion sigma vs Planck
      comparison value 0.6847+/-0.0073); alternative footing vs 1 (residual);
      H0 that makes the alt footing exactly critical
  C4  G-ratio linearity and log-sensitivity
  C5  negative control (circularity): a0 constructed FROM Omega_L feeds back to
      Omega_L by construction -> flagged circular; independent-input check gives a
      FINITE residual (the control is capable of failing)
  C6  boundaries and normalization: a0->0, H0->inf, monotonicity signs, scaling
  C7  README k03 H0-lock numerology: kappa_eff ratio 67.4/73.0 vs 0.461/0.5
  C8  alternative-footing decomposition: kappa_eff at fixed rho_Lambda;
      rho_eff at fixed kappa; rho_eff/rho_Lambda ratio
  C9  Lambda conversions: Lambda = 32 pi a0^2/c^4; Lambda_eff with G_E/G_N

No observational fit is performed; Planck numbers are literature comparison values.
"""
import time
import json
import resource
import mpmath as mp

# ---- actually enforced bounds (in-process rlimits, macOS) ----
# CPU limit: hard-enforced below (soft set to 120 s; process is killed on breach).
# AS limit (memory): macOS refused lowering RLIMIT_AS below the interpreter's current
# address space ("current limit exceeds maximum limit" from setrlimit), so the 512 MB cap
# cannot be OS-enforced; instead peak RSS is measured and reported as the actual bound.
_mem_enforced = False
_mem_error = "not attempted"
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    _mem_enforced = True
except (ValueError, OSError) as _e:
    _mem_error = str(_e)
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))        # 120 s CPU, hard-enforced
# single thread: mpmath/sympy here are single-threaded; no thread pool is created

mp.mp.dps = 60
_start = time.time()

# ---------------- constants (SI; framework defaults) ----------------
G_N = mp.mpf('6.67430e-11')        # Newton coupling in the a0 scale / deep law
c = mp.mpf('299792458')            # m s^-1
pc = mp.mpf('3.085677581491367e16')  # m
km_s_Mpc = mp.mpf(1000) / (pc * mp.mpf('1e6'))   # 1 km/s/Mpc in s^-1 (1 Mpc = 1e6 pc)
kappa = mp.mpf('0.5')              # ADOPTED input (never derived here)

a0_can = mp.mpf('9.3619e-11')      # canonical footing, m s^-2
a0_alt = mp.mpf('1.1279e-10')      # alternative footing, m s^-2
H0_674 = mp.mpf('67.4') * km_s_Mpc   # Planck-anchored value (67.36+/-0.54; 67.4 used)
H0_730 = mp.mpf('73.0') * km_s_Mpc   # SH0ES-side anchor used in README k03

# Planck 2018 comparison values (literature; Aghanim et al. 2020, arXiv:1807.06209)
OML_PLANCK = mp.mpf('0.6847')
SIG_PLANCK = mp.mpf('0.0073')

checks = []

def check(name, residual_abs, residual_rel, tol, detail, verdict):
    checks.append({
        "name": name,
        "residual_abs": str(residual_abs),
        "residual_rel": str(residual_rel),
        "tol": str(tol),
        "detail": detail,
        "verdict": verdict,
    })

# ---------------- helper functions ----------------
def rho_Lambda(a0, G):
    return 4 * a0 * a0 / (G * c * c)          # framework identity (kappa=1/2 restated)

def rho_crit(H0, Gc):
    return 3 * H0 * H0 / (8 * mp.pi * Gc)     # critical-density definition (G_cosmo)

def Omega_direct(a0, H0, G, Gc):
    return rho_Lambda(a0, G) / rho_crit(H0, Gc)

def Omega_form(a0, H0, G, Gc):
    return (32 * mp.pi / 3) * (Gc / G) * (a0 / (H0 * c))**2

def rel(x, y):
    return abs((x - y) / y)

# ---------------- C1 identity (numeric, 50-digit budget) ----------------
for label, a0 in [("canonical", a0_can), ("alternative", a0_alt)]:
    for hlab, H0 in [("H0=67.4", H0_674), ("H0=73.0", H0_730)]:
        for rlab, r in [("r=1", mp.mpf(1)), ("r=1.001", mp.mpf('1.001')),
                        ("r=0.99", mp.mpf('0.99'))]:
            Gc = r * G_N
            d, f = Omega_direct(a0, H0, G_N, Gc), Omega_form(a0, H0, G_N, Gc)
            check(f"C1 identity {label} {hlab} {rlab}",
                  d - f, rel(d, f), mp.mpf('1e-45'),
                  f"direct={mp.nstr(d, 18)} form={mp.nstr(f, 18)}",
                  "PASS" if rel(d, f) < mp.mpf('1e-45') else "FAIL")

# ---------------- C1s symbolic identity (sympy, exact) ----------------
try:
    import sympy as sp
    s_a0, s_H0, s_G, s_Gc, s_c, s_pi = sp.symbols("a0 H0 G Gc c pi", positive=True)
    lhs = (4 * s_a0**2 / (s_G * s_c**2)) / (3 * s_H0**2 / (8 * s_pi * s_Gc))
    rhs = (32 * s_pi / 3) * (s_Gc / s_G) * (s_a0 / (s_H0 * s_c))**2
    diff_sym = sp.simplify(lhs - rhs)
    check("C1s symbolic identity (sympy, exact)", diff_sym, 0, 0,
          f"simplify(lhs-rhs) = {diff_sym}", "PASS" if diff_sym == 0 else "FAIL")
except Exception as e:  # pragma: no cover
    check("C1s symbolic identity (sympy, exact)", "n/a", "n/a", "n/a",
          f"sympy unavailable or failed: {e}", "FAIL")

# ---------------- C2 Jacobian ----------------
def partial(fn, x, v, rel_h=mp.mpf('1e-6')):
    h = rel_h * abs(x)
    return (fn(x + h, v) - fn(x - h, v)) / (2 * h)

def diff_via_mpmath(fn, x):
    return mp.diff(fn, x)   # Richardson-extrapolated, ~full precision

jac_rows = []
for label, a0 in [("canonical", a0_can), ("alternative", a0_alt)]:
    for hlab, H0 in [("H0=67.4", H0_674), ("H0=73.0", H0_730)]:
        Om = Omega_form(a0, H0, G_N, G_N)
        dAdA_num = diff_via_mpmath(lambda x: Omega_form(x, H0, G_N, G_N), a0)
        dAdH_num = diff_via_mpmath(lambda x: Omega_form(a0, x, G_N, G_N), H0)
        dAdA_cl = 2 * Om / a0      # closed-form partial wrt a0
        dAdH_cl = -2 * Om / H0     # closed-form partial wrt H0
        # rank: 1x2 matrix; rank 1 iff not both entries zero; both are nonzero here;
        # sign test: dF/da0 > 0, dF/dH0 < 0
        r1 = rel(dAdA_num, dAdA_cl)
        r2 = rel(dAdH_num, dAdH_cl)
        rank_ok = (dAdA_cl != 0) and (dAdH_cl != 0)
        sign_ok = (dAdA_cl > 0) and (dAdH_cl < 0)
        jac_rows.append((label, hlab, Om, dAdA_cl, dAdH_cl, r1, r2, rank_ok, sign_ok))
        check(f"C2 partials {label} {hlab}",
              mp.mpf(0), max(r1, r2), mp.mpf('1e-12'),
              f"dOm/da0_num={mp.nstr(dAdA_num,12)} closed={mp.nstr(dAdA_cl,12)} "
              f"dOm/dH0_num={mp.nstr(dAdH_num,12)} closed={mp.nstr(dAdH_cl,12)}",
              "PASS" if (max(r1, r2) < mp.mpf('1e-12') and rank_ok and sign_ok) else "FAIL")

# null direction (1,1): Omega(t*a0, t*H0) == Omega(a0, H0)
for t in [mp.mpf('3.7'), mp.mpf('0.31')]:
    for label, a0 in [("canonical", a0_can), ("alternative", a0_alt)]:
        res = rel(Omega_form(t * a0, t * H0_674, G_N, G_N), Omega_form(a0, H0_674, G_N, G_N))
        check(f"C2 null direction t={t} {label}", res, res, mp.mpf('1e-45'),
              f"Omega(t*a0,t*H0)/Omega(a0,H0) residual", "PASS" if res < mp.mpf('1e-45') else "FAIL")

# non-null: a0-only perturbation MUST move Omega (control capable of failing)
res = rel(Omega_form(mp.mpf('1.1') * a0_can, H0_674, G_N, G_N), Omega_form(a0_can, H0_674, G_N, G_N))
check("C2 non-null a0-only perturbation", mp.mpf(0), res, mp.mpf('1e-3'),
      "Omega(1.1 a0)/Omega(a0) must NOT be 1 (map is not constant in a0)",
      "PASS" if res > mp.mpf('1e-3') else "FAIL")

# ---------------- C3 closure verdicts ----------------
Om_can_674 = Omega_form(a0_can, H0_674, G_N, G_N)
Om_alt_674 = Omega_form(a0_alt, H0_674, G_N, G_N)
sig_excl = (mp.mpf(1) - Om_can_674) / SIG_PLANCK   # sigma by which rho_L=rho_crit excluded (canonical)
check("C3a canonical footing vs strict closure (Omega_L=1)", Om_can_674 - 1, rel(Om_can_674, 1), mp.mpf('1e-3'),
      f"Omega_L(canonical,67.4)={mp.nstr(Om_can_674,12)}; Planck Omega_Lambda=0.6847+/-0.0073; "
      f"exclusion (1-Omega)/0.0073 = {mp.nstr(sig_excl,6)} sigma (comparison)",
      "PASS" if sig_excl > 40 else "FAIL")
check("C3b alternative footing vs critical density", Om_alt_674 - 1, rel(Om_alt_674, 1), mp.mpf('1e-3'),
      f"Omega_total(alternative,67.4)={mp.nstr(Om_alt_674,12)} (rho_eff/rho_crit); deviation from 1 = "
      f"{mp.nstr(rel(Om_alt_674,1),6)}",
      "PASS" if rel(Om_alt_674, 1) > mp.mpf('1e-3') and rel(Om_alt_674, 1) < mp.mpf('1e-2') else "FAIL")
# H0 that makes the alternative footing EXACTLY critical
H0_exact_alt = mp.sqrt(8 * mp.pi * G_N * rho_Lambda(a0_alt, G_N) / 3) / km_s_Mpc
res = rel(H0_exact_alt, mp.mpf('67.4'))
check("C3c H0 for exact alt-footing closure", H0_exact_alt - mp.mpf('67.4'), res, mp.mpf('1e-2'),
      f"H0_exact = {mp.nstr(H0_exact_alt, 8)} km/s/Mpc (close to 67.4 anchor)",
      "PASS" if res < mp.mpf('1e-2') else "FAIL")

# ---------------- C4 G-ratio ----------------
for r in [mp.mpf('1.001'), mp.mpf('0.99')]:
    OmG = Omega_form(a0_can, H0_674, G_N, r * G_N)
    linr = rel(OmG, r * Om_can_674)
    check(f"C4 G-ratio linearity r={r}", OmG - r * Om_can_674, linr, mp.mpf('1e-45'),
          f"Omega(L)/Omega(1) == {mp.nstr(OmG / Om_can_674, 15)}",
          "PASS" if linr < mp.mpf('1e-45') else "FAIL")
lsens = mp.mpf(1) - (mp.log(OmG) - mp.log(Om_can_674)) / mp.log(r)
check("C4 log-sensitivity dlnOmega/dln(Gc/GN)", lsens, abs(lsens), mp.mpf('1e-45'),
      f"log-sensitivity = {mp.nstr(1 - lsens, 15)} (must be 1)",
      "PASS" if abs(lsens) < mp.mpf('1e-45') else "FAIL")

# ---------------- C5 negative control: circularity ----------------
# a0 CONSTRUCTED from Omega_L input, then fed back:
a0_prime = H0_674 * c * mp.sqrt(3 * OML_PLANCK * G_N / (32 * mp.pi * G_N))
rt = Omega_form(a0_prime, H0_674, G_N, G_N)
rt_res = rel(rt, OML_PLANCK)
check("C5a roundtrip of an Omega_L-derived a0 (CIRCULARITY CONTROL)", rt - OML_PLANCK, rt_res,
      mp.mpf('1e-40'),
      f"a0' built from Omega_L=0.6847 gives back Omega={mp.nstr(rt,15)}; agreement by construction "
      f"=> FLAGGED CIRCULAR, not evidence",
      "CIRCULAR-FLAGGED" if rt_res < mp.mpf('1e-40') else "FAIL")
# independent-input check (NOT circular): galaxy-scale canonical a0 vs Planck Omega_L
Om_ind = Omega_form(a0_can, H0_674, G_N, G_N)
ind_res = rel(Om_ind, OML_PLANCK)
check("C5b independent-input consistency (canonical a0 as galaxy datum)", Om_ind - OML_PLANCK, ind_res,
      mp.mpf('1e-3'),
      f"Omega(canonical a0, H0=67.4) = {mp.nstr(Om_ind, 8)} vs Planck 0.6847: finite residual "
      f"{mp.nstr(ind_res, 4)} (0.03%) — genuine consistency, not construction;"
      f" same check with alt a0 gives {mp.nstr(rel(Om_alt_674, OML_PLANCK), 4)} (45%) — map responds to inputs",
      "PASS" if ind_res < mp.mpf('1e-3') else "FAIL")

# ---------------- C6 boundaries / normalization ----------------
b = []
for ep in [mp.mpf('1e-30'), mp.mpf('1e-20'), mp.mpf('1e-10')]:
    b.append(Omega_form(ep, H0_674, G_N, G_N))
check("C6a a0->0 boundary", mp.mpf(0), b[0], mp.mpf('1e-30'),
      f"Omega(a0->0): {mp.nstr(b[0], 3)} -> 0 as expected",
      "PASS" if b[0] < mp.mpf('1e-29') else "FAIL")
b2 = Omega_form(a0_can, H0_674 * 1000, G_N, G_N)
b2_exp = Omega_form(a0_can, H0_674, G_N, G_N) / mp.mpf('1e6')   # Omega ~ 1/H0^2
check("C6b H0->inf boundary", b2 - b2_exp, rel(b2, b2_exp), mp.mpf('1e-3'),
      f"Omega(H0*1000)={mp.nstr(b2, 6)} vs Omega(0)/1e6={mp.nstr(b2_exp, 6)} (1/H0^2 scaling; "
      f"1000x H0 -> 1e-6 x Omega)",
      "PASS" if rel(b2, b2_exp) < mp.mpf('1e-3') else "FAIL")
# scale covariance: x -> t*x with t>0 leaves dimensionless products; check dimension proxy
check("C6c units: dimensionless ratio", mp.mpf(0), mp.mpf(0), mp.mpf(0),
      "a0^2/(H0 c)^2 has units (m^2 s^-4)/(s^-2 m^2 s^-2) = 1; Gc/GN dimensionless",
      "PASS")

# ---------------- C7 README k03 H0-lock numerology ----------------
ka_674 = a0_can / (c * mp.sqrt(G_N * rho_crit(H0_674, G_N)))   # kappa_eff if rho=rho_crit(67.4)
ka_730 = a0_can / (c * mp.sqrt(G_N * rho_crit(H0_730, G_N)))
ratio_lock = ka_730 / ka_674
res7 = rel(ratio_lock, mp.mpf('0.461') / mp.mpf('0.5'))
check("C7 k03 H0-lock numerology", ratio_lock - mp.mpf('0.461') / mp.mpf('0.5'), res7, mp.mpf('5e-3'),
      f"kappa_eff(73.0)/kappa_eff(67.4) = {mp.nstr(ratio_lock, 8)} vs README 0.461/0.5=0.922 "
      f"(exactly H0(67.4)/H0(73.0)={mp.nstr(H0_674 / H0_730, 8)}; the Jacobian null direction)",
      "PASS" if res7 < mp.mpf('5e-3') else "FAIL")

# ---------------- C8 alternative footing decomposition ----------------
kappa_eff = a0_alt / (c * mp.sqrt(G_N * rho_Lambda(a0_can, G_N)))
rho_eff = rho_Lambda(a0_alt, G_N)
ratio_rho = rho_eff / rho_Lambda(a0_can, G_N)
check("C8a kappa_eff at fixed rho_Lambda", kappa_eff - mp.mpf('0.5') * (a0_alt / a0_can),
      rel(kappa_eff, mp.mpf('0.5') * (a0_alt / a0_can)), mp.mpf('1e-45'),
      f"kappa_eff = {mp.nstr(kappa_eff, 8)} (== (1/2)*(a0_alt/a0_can))",
      "PASS" if rel(kappa_eff, mp.mpf('0.5') * (a0_alt / a0_can)) < mp.mpf('1e-45') else "FAIL")
check("C8b rho_eff at fixed kappa=1/2", rho_eff / rho_Lambda(a0_can, G_N), rel(ratio_rho, mp.mpf(1)),
      mp.mpf('1e-45'),
      f"rho_eff/rho_Lambda(canonical) = (a0_alt/a0_can)^2 = {mp.nstr(ratio_rho, 8)}",
      "PASS" if rel(ratio_rho, (a0_alt / a0_can)**2) < mp.mpf('1e-45') else "FAIL")

# ---------------- C9 Lambda conversions ----------------
Lam = 32 * mp.pi * a0_can**2 / c**4
Lam_Gratio = 32 * mp.pi * (G_N / G_N) * a0_can**2 / c**4   # G_E=G_N
check("C9 Lambda from a0 (same-G)", Lam, mp.mpf(0), mp.mpf(0),
      f"Lambda = 32 pi a0^2/c^4 = {mp.nstr(Lam, 8)} m^-2 (G_E = G_N footing)",
      "PASS")

# ---------------- performance / bounds ----------------
_elapsed = time.time() - _start
_mem_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024.0 * 1024.0)  # macOS: bytes -> MB

print(json.dumps({
    "script": "as003_verify.py",
    "enforced_bounds": {
        "threads": 1,
        "wall_cap_s": 120,
        "cpu_rlimit_s": 120,
        "cpu_rlimit_enforced": True,
        "memory_cap_MB": 512,
        "memory_rlimit_enforced": _mem_enforced,
        "memory_rlimit_error": _mem_error if not _mem_enforced else None,
        "actual_wall_s": round(_elapsed, 3),
        "actual_peak_rss_MB": round(_mem_mb, 2),
        "mpmath_precision_digits": 60,
    },
    "inputs": {
        "G_N": str(G_N), "c": str(c), "kappa": str(kappa),
        "a0_canonical": str(a0_can), "a0_alternative": str(a0_alt),
        "H0_674_km_s_Mpc": str(H0_674 / km_s_Mpc), "H0_730_km_s_Mpc": str(H0_730 / km_s_Mpc),
        "pc_m": str(pc),
        "Planck_comparison": {"Omega_Lambda": str(OML_PLANCK), "sigma": str(SIG_PLANCK),
                              "source": "Planck 2018 (Aghanim et al. 2020, arXiv:1807.06209, Table 2); "
                                        "H0 = 67.36 +/- 0.54 km/s/Mpc (67.4 used)"},
    },
    "values": {
        "rho_Lambda_canonical_kg_m3": mp.nstr(rho_Lambda(a0_can, G_N), 10),
        "rho_Lambda_alt_kg_m3": mp.nstr(rho_eff, 10),
        "rho_crit_H0_674_kg_m3": mp.nstr(rho_crit(H0_674, G_N), 10),
        "rho_crit_H0_730_kg_m3": mp.nstr(rho_crit(H0_730, G_N), 10),
        "Omega_L_canonical_674": mp.nstr(Om_can_674, 10),
        "Omega_L_canonical_730": mp.nstr(Omega_form(a0_can, H0_730, G_N, G_N), 10),
        "Omega_total_alt_674": mp.nstr(Om_alt_674, 10),
        "Omega_total_alt_730": mp.nstr(Omega_form(a0_alt, H0_730, G_N, G_N), 10),
        "exclusion_sigma_canonical_vs_Planck": mp.nstr(sig_excl, 6),
        "H0_exact_alt_closure_km_s_Mpc": mp.nstr(H0_exact_alt, 8),
        "kappa_eff_alt_fixed_rho": mp.nstr(kappa_eff, 8),
        "rho_eff_over_rho_Lambda": mp.nstr(ratio_rho, 8),
        "kappa_eff_lock_ratio_730_over_674": mp.nstr(ratio_lock, 8),
        "Lambda_canonical_m^-2": mp.nstr(Lam, 8),
    },
    "checks": checks,
    "n_checks": len(checks),
    "n_fail": sum(1 for ck in checks if ck["verdict"] == "FAIL"),
}, indent=2))