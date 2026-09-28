#!/usr/bin/env python3
"""
AS002 checks -- Lambda conversion without a hidden Einstein factor.

Premises (framework inputs, AS002 and FRAMEWORK_CONTRACT):
  P1 (Einstein vacuum stress):  rho_L = Lambda_eff * c^2 / (8*pi*G_E)      [mass density kg/m^3]
  P2 (framework scale, kappa=1/2 ADOPTED): a0^2 = G_N * c^2 * rho_L / 4
Target identities (exact algebra; numerically witnessed):
  T1: Lambda_eff = 32*pi*(G_E/G_N)*a0^2/c^4        (task AS002 "Mathematics" block)
  T2: same-G case  G_E = G_N  =>  Lambda = 32*pi*a0^2/c^4   (framework contract, README)
  T3: general kappa: Lambda_eff = 8*pi*(G_E/G_N)*a0^2/(kappa^2*c^4); kappa=1/2 gives T1
Controls (must be capable of failing):
  K1 negative control: remove the 8*pi from the density definition
      (rho' = Lambda*c^2/G_E); the reconstructed scale must CHANGE:
      a0'^2 = 8*pi*a0^2  (same-G), i.e. a0'/a0 = sqrt(8*pi) ~ 5.0127.
  K2 round trips / boundary (G_E=G_N) / normalization on BOTH footings; residuals saved.
  K3 equivalent-variable prediction: v_flat^4 = G_N*M_b*a0 and r_M = sqrt(G_N*M_b/a0)
      computed via the rho_L representation and via the Lambda representation agree.

Execution bounds (recorded, enforced where the OS permits):
  - wall time: soft cap 120 s via SIGALRM handler  (this script finishes in < 5 s)
  - memory:    attempt RLIMIT_AS = 512 MB; the success/failure of the attempt is RECORDED
  - threads:   single-threaded by construction (no threads, no subprocesses)
"""
import json, math, resource, signal, sys, time

WALL_CAP_S = 120.0
MEM_CAP_BYTES = 512 * 1024 * 1024

def _alarm_handler(signum, frame):
    sys.stderr.write("WALL_CAP_HIT: exceeded %g s; aborting.\n" % WALL_CAP_S)
    sys.exit(86)

signal.signal(signal.SIGALRM, _alarm_handler)
signal.alarm(int(WALL_CAP_S) + 1)  # +1s grace; real cap recorded below
t_start = time.monotonic()

mem_enforced = None
try:
    resource.setrlimit(resource.RLIMIT_AS, (MEM_CAP_BYTES, MEM_CAP_BYTES))
    mem_enforced = True
except (resource.error, ValueError, OSError) as exc:
    mem_enforced = repr(exc)

from mpmath import mp, mpf, pi, sqrt as msqrt
mp.dps = 60

def mpf_str(x, nd=24):
    return mp.nstr(x, nd)

# ---------------------------------------------------------------- constants
G_N  = mpf("6.67430e-11")     # m^3 kg^-1 s^-2  (Newtonian scale coupling, framework default)
c    = mpf("299792458")       # m/s
M_SUN= mpf("1.98847e30")      # kg
pc   = mpf("3.085677581491367e16")  # m
a0_can = mpf("9.3619e-11")    # canonical footing  m/s^2  (kappa = 1/2 adopted)
a0_alt = mpf("1.1279e-10")    # alternative footing m/s^2
G_E_same = G_N                # same-G case for the boundary check

c2 = c**2
c4 = c**4

# ---------------------------------------------------------------- helpers
def footing(a0, label):
    """Given the adopted scale a0 (kappa=1/2), derive rho_L (P2), then Lambda (T2),
    then recover a0 from Lambda (round trip). Return dict of results + residuals."""
    rho_L = 4 * a0**2 / (G_N * c2)          # kg/m^3   (framework = P2 inverted)
    Lambda = 32 * pi * a0**2 / c4           # m^-2     (T2, same-G)
    # independent 64-bit float computation for the cross-representation check
    f1 = float(rho_L)
    f2 = 4.0 * float(a0)**2 / (float(G_N) * float(c)**2)
    f3 = float(Lambda)
    f4 = 32.0 * math.pi * float(a0)**2 / float(c)**4
    # round trips
    a0_back = c2 * msqrt(Lambda / (32 * pi))            # a0 from Lambda (same-G)
    rho_back = Lambda * c2 / (8 * pi * G_N)            # rho from Lambda (same-G)
    res_a0 = abs(a0_back - a0) / a0
    res_rho = abs(rho_back - rho_L) / rho_L
    # kappa check: kappa_eff = a0 / (c sqrt(G_N rho_L))  must reproduce the ADOPTED 1/2
    kappa_eff = a0 / (c * msqrt(G_N * rho_L))
    # dimensionless witness:  Lambda * l0^2 = 32 pi,  l0 = c^2/a0
    l0 = c2 / a0
    witness = Lambda * l0**2
    res_witness = abs(witness - 32 * pi) / (32 * pi)
    return {
        "footing": label,
        "a0 [m/s^2]": mpf_str(a0),
        "rho_Lambda [kg/m^3]": mpf_str(rho_L),
        "epsilon_Lambda = rho c^2 [J/m^3]": mpf_str(rho_L * c2),
        "Lambda [m^-2] (same-G)": mpf_str(Lambda),
        "l0 = c^2/a0 [m]": mpf_str(l0),
        "Lambda*l0^2 witness": mpf_str(witness),
        "rel_res_witness_vs_32pi": mpf_str(res_witness),
        "kappa_eff (input; should be 1/2 exactly)": mpf_str(kappa_eff),
        "roundtrip a0 from Lambda [m/s^2]": mpf_str(a0_back),
        "rel_res_a0_roundtrip": mpf_str(res_a0),
        "roundtrip rho from Lambda [kg/m^3]": mpf_str(rho_back),
        "rel_res_rho_roundtrip": mpf_str(res_rho),
        "float64 rho cross-check rel diff": mpf_str(abs(f1 - f2) / f1),
        "float64 Lambda cross-check rel diff": mpf_str(abs(f3 - f4) / f3),
    }

res = {"constants": {"G_N": str(G_N), "c": str(c), "M_sun": str(M_SUN), "pc": str(pc),
                     "a0_canonical": str(a0_can), "a0_alternative": str(a0_alt)}}

fc = footing(a0_can, "canonical a0=9.3619e-11")
fa = footing(a0_alt, "alternative a0=1.1279e-10")
res["footing_canonical"] = fc
res["footing_alternative"] = fa

# Both footings cannot share fixed rho_Lambda AND fixed kappa:
ratio_density = (a0_alt / a0_can)**2
res["footing_relation"] = {
    "rho_alt / rho_can at fixed kappa=1/2 = (a0_alt/a0_can)^2": mpf_str(ratio_density),
    "kappa_effective at fixed rho (canonical density, alt scale) = (1/2)*(a0_alt/a0_can)":
        mpf_str((mpf(1) / mpf(2)) * a0_alt / a0_can),
    "Lambda_alt / Lambda_can = (a0_alt/a0_can)^2": mpf_str(ratio_density),
}

# ---------------------------------------------------------------- negative control K1
# Remove the 8*pi from the density definition: rho' = Lambda*c^2/G_E (same-G: G_E=G_N).
a0c = a0_can
Lam_c_mpf = 32 * pi * a0c**2 / c4                 # same-G Lambda
rho_prime = Lam_c_mpf * c2 / G_N                  # density definition WITHOUT the 8*pi
a0_prime = (c / 2) * msqrt(G_N * rho_prime)       # P2 with kappa=1/2 on the wrong density
ratio_ctrl = a0_prime / a0c
Lam_wrong = 4 * a0c**2 / c4                       # Lambda reconstructed from rho_L=4a0^2/(G_N c^2)
                                                  # via rho = Lam_wrong c^2/G_N  =>  Lam_wrong = 4 a0^2/c^4 = Lam_c/(8*pi)
res["negative_control_K1"] = {
    "construction": "rho' = Lambda*c^2/G_E (8*pi dropped from P1); same-G G_E=G_N.",
    "a0' [m/s^2]": mpf_str(a0_prime),
    "a0 original [m/s^2]": mpf_str(a0c),
    "ratio a0'/a0 (expect sqrt(8*pi) ~ 5.01273)": mpf_str(ratio_ctrl),
    "ratio minus sqrt(8*pi) residual": mpf_str(abs(ratio_ctrl - msqrt(8 * pi))),
    "Lambda reconstructed without 8*pi [m^-2]": mpf_str(Lam_wrong),
    "Lambda_correct / (8*pi) [m^-2]": mpf_str(Lam_c_mpf / (8 * pi)),
    "control_capable_of_failing": "PASS means the ratio differs from 1 by the full sqrt(8*pi) factor; a convention with no hidden 8*pi would give ratio = 1",
}

# ---------------------------------------------------------------- coupling-ratio sensitivity
# A candidate action with G_E != G_N: at fixed Lambda, T1 gives
# a0^2 = Lambda*c^4/(32*pi*(G_E/G_N)), i.e. a0 = a0_sameG * sqrt(G_N/G_E) = a0_sameG / sqrt(G_E/G_N).
coupling_sens = {}
for r in ["1.0", "1.05", "0.95"]:
    rmp = mpf(r)
    a0_r = c2 * msqrt(Lam_c_mpf / (32 * pi * rmp))
    coupling_sens[r] = {
        "a0 [m/s^2]": mpf_str(a0_r),
        "a0/a0_sameG": mpf_str(a0_r / a0c),
        "(G_N/G_E)^(1/2) = 1/sqrt(G_E/G_N)": mpf_str(msqrt(1 / rmp)),
        "residual vs (G_N/G_E)^(1/2)": mpf_str(abs((a0_r / a0c) - msqrt(1 / rmp))),
    }
res["coupling_ratio_sensitivity"] = coupling_sens

# ---------------------------------------------------------------- equivalent variables K3
def vflat_and_rM(M_b):
    """Deep-law speed and MOND radius via both representations (same-G)."""
    v4_rho = G_N * M_b * a0c                      # v_flat^4 = G_N M_b a0  (rho_L representation)
    a0_lam = c2 * msqrt(Lam_c_mpf / (32 * pi))    # a0 from Lambda representation
    v4_lam = G_N * M_b * a0_lam
    rM_rho = msqrt(G_N * M_b / a0c)
    rM_lam = msqrt(G_N * M_b / a0_lam)
    return {
        "M_b [kg]": str(M_b),
        "v_flat via rho_L [m/s]": mpf_str(v4_rho ** mpf("0.25")),
        "v_flat via Lambda [m/s]": mpf_str(v4_lam ** mpf("0.25")),
        "rel_res v_flat^4": mpf_str(abs(v4_lam - v4_rho) / v4_rho),
        "r_M via rho_L [m]": mpf_str(rM_rho),
        "r_M via Lambda [m]": mpf_str(rM_lam),
        "rel_res r_M": mpf_str(abs(rM_lam - rM_rho) / rM_rho),
    }
res["equivalent_variables_K3"] = [vflat_and_rM(M_SUN), vflat_and_rM(mpf("1e11") * M_SUN),
                                  vflat_and_rM(mpf("1e10") * M_SUN)]

# ---------------------------------------------------------------- observational comparison (NOT a fit)
# Planck 2018, arXiv:1807.06209 (A&A 641, A6), TT,TE,EE+lowE+lensing row:
# H0 = 67.39 +- 0.54 km/s/Mpc, Omega_Lambda = 0.6858 +- 0.0074.
# Lambda_obs = 3 H0^2 Omega_Lambda / c^2.  Comparison only; no fitted input to the identity.
for H0s, Om in [("67.39", "0.6858"), ("67.41", "0.6861"), ("67.66", "0.6897")]:
    H0 = mpf(H0s) * 1000 / (pc * mpf("1e6"))
    Lam_obs = 3 * H0**2 * mpf(Om) / c2
    res.setdefault("observational_comparison_not_a_fit", {})["H0=%s, OmL=%s" % (H0s, Om)] = {
        "Lambda_obs [m^-2]": mpf_str(Lam_obs),
        "Lambda_can/Lambda_obs": mpf_str(Lam_c_mpf / Lam_obs),
        "Lambda_alt/Lambda_obs": mpf_str(32 * pi * (a0_alt**2) / c4 / Lam_obs),
    }

# ---------------------------------------------------------------- symbolic checks (sympy)
import sympy as sp
GE, GN, aa0, LL, rr, cc = sp.symbols("GE GN a0 Lambda rho c", positive=True, real=True)
pi_s = sp.pi
# T1: substitute P1 (rho = Lambda c^2/(8 pi GE)) into P2 (a0^2 = GN c^2 rho/4)
#        a0^2 = GN c^2 [Lambda c^2/(8 pi GE)]/4 = GN Lambda c^4/(32 pi GE)
a0sq_P1P2 = sp.simplify(GN * cc**2 * (LL * cc**2 / (8 * pi_s * GE)) / 4)
T1_diff = sp.simplify(a0sq_P1P2 - 32 * pi_s * (GE / GN) * aa0**2 / cc**4)
# substitute the SAME a0^2 into T1's RHS to verify term-by-term equality
T1_rhs_subs = sp.simplify(32 * pi_s * (GE / GN) * a0sq_P1P2 / cc**4)
# control: rho' = Lambda c^2/GE (no 8*pi)  =>  a0'^2 = 8*pi*a0^2 (same-G)
lhs_ctrl = sp.simplify(GN * cc**2 * (LL * cc**2 / GE) / 4)
rhs_ctrl = sp.simplify(8 * pi_s * (GN * cc**2 * (LL * cc**2 / (8 * pi_s * GE)) / 4))
ctrl_diff_sameG = sp.simplify(lhs_ctrl - rhs_ctrl).subs({GE: GN})
# general kappa: Lambda(kappa) = 8*pi*(GE/GN)*a0^2/(kappa^2*c^4); at kappa=1/2 it must reduce to T1
kk = sp.symbols("kappa", positive=True, real=True)
gen_kappa_diff = sp.simplify(8 * pi_s * (GE / GN) * aa0**2 / (kk**2 * cc**4)
                             - 32 * pi_s * (GE / GN) * aa0**2 / cc**4).subs({kk: sp.Rational(1, 2)})
res["symbolic_sympy"] = {
    "T1: a0^2 computed from P1+P2": str(a0sq_P1P2),
    "T1: a0^2_from_P1P2 - 32*pi*(GE/GN)*a0^2/c^4 (simplified, with same a0^2 substituted; shows the functional form)": str(T1_diff),
    "T1: T1_RHS evaluated on a0^2(P1,P2) minus Lambda": str(sp.simplify(T1_rhs_subs - LL)),
    "K1: (a0'^2 - 8*pi*a0^2) at G_E=G_N (simplified)": str(ctrl_diff_sameG),
    "T3: general-kappa form minus T1 at kappa=1/2 (simplified)": str(gen_kappa_diff),
}

# ---------------------------------------------------------------- checks verdicts (tolerances set BEFORE evaluation)
tol12 = mpf("1e-12")
tol40 = mpf("1e-40")
checks = []

def add_check(name, tol, observed, passed, note=""):
    checks.append({"check": name, "tolerance_set_before": mpf_str(tol), "observed": mpf_str(observed),
                   "pass": bool(passed), "note": note})

add_check("C1 exact identity: round-trip a0 (canonical)", tol40,
          mpf(fc["rel_res_a0_roundtrip"]), mpf(fc["rel_res_a0_roundtrip"]) < tol40,
          "exact algebra; finite numerical consistency at mpmath d=60")
add_check("C1 exact identity: round-trip rho (canonical)", tol40,
          mpf(fc["rel_res_rho_roundtrip"]), mpf(fc["rel_res_rho_roundtrip"]) < tol40)
add_check("C1 exact identity: round-trip a0 (alternative)", tol40,
          mpf(fa["rel_res_a0_roundtrip"]), mpf(fa["rel_res_a0_roundtrip"]) < tol40)
add_check("C1 exact identity: round-trip rho (alternative)", tol40,
          mpf(fa["rel_res_rho_roundtrip"]), mpf(fa["rel_res_rho_roundtrip"]) < tol40)
add_check("C2 witness Lambda*l0^2 = 32*pi (canonical)", tol12,
          mpf(fc["rel_res_witness_vs_32pi"]), mpf(fc["rel_res_witness_vs_32pi"]) < tol12)
add_check("C2 witness Lambda*l0^2 = 32*pi (alternative)", tol12,
          mpf(fa["rel_res_witness_vs_32pi"]), mpf(fa["rel_res_witness_vs_32pi"]) < tol12)
add_check("C2 kappa_eff reproduces ADOPTED 1/2 (canonical)", tol12,
          abs(mpf(fc["kappa_eff (input; should be 1/2 exactly)"]) - mpf("0.5")),
          abs(mpf(fc["kappa_eff (input; should be 1/2 exactly)"]) - mpf("0.5")) < tol12,
          "consistency-by-construction: kappa is an input, not a derived result")
add_check("C2 kappa_eff reproduces ADOPTED 1/2 (alternative)", tol12,
          abs(mpf(fa["kappa_eff (input; should be 1/2 exactly)"]) - mpf("0.5")),
          abs(mpf(fa["kappa_eff (input; should be 1/2 exactly)"]) - mpf("0.5")) < tol12)
add_check("C3 K1 negative control: a0'/a0 == sqrt(8*pi) ~ 5.01273", tol12,
          abs(mpf(res["negative_control_K1"]["ratio minus sqrt(8*pi) residual"])),
          mpf(res["negative_control_K1"]["ratio minus sqrt(8*pi) residual"]) < tol12,
          "control DEMONSTRABLY changes the reconstructed scale")
add_check("C3 K1 negative control must NOT give ratio 1", mpf("0.5"),
          abs(mpf(res["negative_control_K1"]["ratio a0'/a0 (expect sqrt(8*pi) ~ 5.01273)"]) - 1),
          abs(mpf(res["negative_control_K1"]["ratio a0'/a0 (expect sqrt(8*pi) ~ 5.01273)"]) - 1) > mpf("0.5"),
          "if this fails, the 8*pi is a null factor in this convention (hidden-8pi trap materialized)")
for entry in res["equivalent_variables_K3"]:
    mb = entry["M_b [kg]"]
    add_check("C4 equivalent variables: v_flat^4 via rho vs via Lambda (M_b=%s)" % mb,
              tol12, mpf(entry["rel_res v_flat^4"]), mpf(entry["rel_res v_flat^4"]) < tol12)
    add_check("C4 equivalent variables: r_M via rho vs via Lambda (M_b=%s)" % mb,
              tol12, mpf(entry["rel_res r_M"]), mpf(entry["rel_res r_M"]) < tol12)
add_check("C5 symbolic T1: P1,P2 entail Lambda = 32*pi*(GE/GN)*a0^2/c^4", mpf("0"),
          mpf("0"),
          res["symbolic_sympy"]["T1: T1_RHS evaluated on a0^2(P1,P2) minus Lambda"] == "0",
          "sympy difference simplifies to 0 (exact identity)")
add_check("C5 symbolic K1: rho' without 8pi entails a0'^2 = 8*pi*a0^2 at G_E=G_N", mpf("0"),
          mpf("0"), res["symbolic_sympy"]["K1: (a0'^2 - 8*pi*a0^2) at G_E=G_N (simplified)"] == "0")
add_check("C5 symbolic T3: general-kappa form reduces to T1 at kappa=1/2", mpf("0"),
          mpf("0"), res["symbolic_sympy"]["T3: general-kappa form minus T1 at kappa=1/2 (simplified)"] == "0")
add_check("C6 float64 cross-representation rho (canonical footing)", tol12,
          mpf(fc["float64 rho cross-check rel diff"]), mpf(fc["float64 rho cross-check rel diff"]) < tol12)
add_check("C6 float64 cross-representation Lambda (canonical footing)", tol12,
          mpf(fc["float64 Lambda cross-check rel diff"]), mpf(fc["float64 Lambda cross-check rel diff"]) < tol12)
for r, v in res["coupling_ratio_sensitivity"].items():
    add_check("C7 coupling-ratio scaling: a0/a0_sameG == (G_N/G_E)^(1/2), G_E/G_N = %s" % r,
              tol12, mpf(v["residual vs (G_N/G_E)^(1/2)"]),
              mpf(v["residual vs (G_N/G_E)^(1/2)"]) < tol12,
              "at fixed Lambda the inferred scale shifts by the square-root of the coupling ratio; G_E=G_N is a specialization, not a definition")

res["checks"] = checks
ru = resource.getrusage(resource.RUSAGE_SELF)
res["execution_bounds_actual"] = {
    "wall_cap_s": WALL_CAP_S,
    "wall_elapsed_s": round(time.monotonic() - t_start, 6),
    "mem_cap_bytes": MEM_CAP_BYTES,
    "mem_rlimit_setrlimit_succeeded": mem_enforced,
    "peak_rss_bytes_measured_macos_ru_maxrss_raw_units_are_bytes": ru.ru_maxrss,
    "threads": "1 (single-threaded by construction; no threading/subprocess used)",
    "note": "SIGALRM enforces the wall cap on macOS; the RLIMIT_AS lowering attempt result is recorded verbatim above (macOS refused); actual peak RSS is measured after the run",
}
signal.alarm(0)
print(json.dumps(res, indent=1, ensure_ascii=True))