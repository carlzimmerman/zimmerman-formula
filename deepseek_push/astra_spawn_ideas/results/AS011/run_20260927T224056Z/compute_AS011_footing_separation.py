#!/usr/bin/env python3
"""
AS011 — Alternative footing as a separate hypothesis.
Bounded seed computation.

Claims checked (framework branch: CORE scale identities; kappa=1/2 ADOPTED input):
  a0 = kappa * c * sqrt(G * rho_Lambda)   [m s^-2]
  rho_Lambda = 4 a0^2 / (G c^2)           [kg m^-3]  (derived from the identity, same G)
  Lambda = 32 pi a0^2 / c^4               [m^-2]     (holds when Einstein G == scale G)
  r_M = sqrt(G M_b / a0)                  [m]
  v_flat^4 = G M_b a0                     [m^4 s^-4]

Two SEPARATE footings:
  canonical    a0_c = 9.3619e-11  m/s^2   (kappa = 1/2 adopted)
  alternative  a0_a = 1.1279e-10  m/s^2   (separate hypothesis, NOT an uncertainty band)

Key question: a0_a is not a re-labelling of the canonical model. Holding rho_Lambda
fixed forces kappa_a = R_a / 2 (a NEW adopted coefficient, no longer 1/2); holding
kappa = 1/2 fixed forces rho_Lambda,a = R_a^2 rho_Lambda,c. Both cannot hold at once.

Every number is computed at 60 significant decimal digits (Decimal) unless marked
float64. All residuals are recorded, not Boolean-only.
"""
import json, math, time, resource, sys
from decimal import Decimal, getcontext, InvalidOperation

class _Enc(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)

getcontext().prec = 60
D = Decimal

t_start = time.perf_counter()
bounds: dict = {"declared_wall_s": 120, "declared_mem_mb": 512, "declared_threads": 1}
# Enforce: CPU limit 120 s; address-space limit 512 MB; single thread (no thread spawned by design).
try:
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    bounds["rlimit_cpu_capped_s"] = 120
except Exception as e:
    bounds["rlimit_cpu_error"] = str(e)
try:
    mem = 512 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
    bounds["rlimit_as_capped_bytes"] = mem
except Exception as e:
    bounds["rlimit_as_error"] = str(e)
bounds["threads_actually_spawned"] = 0  # single-threaded by construction

# ---------------------------------------------------------------- constants (SI)
G   = D("6.67430e-11")       # m^3 kg^-1 s^-2  (G_N / scale G, treated as measured input here)
c   = D("299792458")         # m s^-1
M_sun = D("1.98847e30")      # kg
pc  = D("3.085677581491367e16")  # m
k_B = D("1.380649e-23")      # J K^-1
kappa_can = D("0.5")         # adopted, NOT derived
a0_can = D("9.3619e-11")     # m s^-2, canonical footing
a0_alt = D("1.1279e-10")     # m s^-2, alternative footing (separate hypothesis)

KPC = D(1000) * pc           # m

# ---------------------------------------------------------------- derived quantities
R_a   = a0_alt / a0_can                        # dimensionless footing ratio
R_a2  = R_a * R_a
rho_L_can = D(4) * a0_can * a0_can / (G * c * c)      # kg m^-3, from canonical
eps_L_can = rho_L_can * c * c                          # J m^-3 energy density
Lambda_can = D(32) * D("3.14159265358979323846264338327950288419716939937510") * a0_can * a0_can / (c**4)  # m^-2, G_E = G_N
# alternative footing, kappa = 1/2 KEPT: same formula with a0_alt
rho_L_alt = D(4) * a0_alt * a0_alt / (G * c * c)      # kg m^-3
eps_L_alt = rho_L_alt * c * c
Lambda_alt = D(32) * D("3.14159265358979323846264338327950288419716939937510") * a0_alt * a0_alt / (c**4)

# alternative footing, rho_Lambda KEPT at canonical value: effective kappa
kappa_alt_fixedrho = a0_alt / (c * (G * rho_L_can).sqrt())

checks = []
def check(name, observed, ref, tol, kind, unit, fmt=lambda x: str(x)):
    """Record a check with observed value, reference, relative tolerance, pass/fail."""
    obs = D(observed) if isinstance(observed, (int, float, str, D)) else observed
    try:
        rel = abs((obs - ref) / ref)
    except (InvalidOperation, ZeroDivisionError):
        rel = D("Infinity")
    passed = rel <= tol
    checks.append({"name": name, "observed": fmt(obs), "reference": fmt(ref),
                   "relresidual": str(rel), "tol": str(tol), "pass": passed,
                   "kind": kind, "unit": unit})
    return passed

def check_flag(name, observed, ref, tol, kind, unit, fmt=lambda x: str(x)):
    """Negative-control flag check: PASSES when |obs - ref|/|ref| EXCEEDS tol,
    i.e. when the model actually flags the inconsistency. Capable of failing:
    if the inputs were mislabelled so that the inconsistency did NOT appear,
    this check fails."""
    obs = D(observed) if isinstance(observed, (int, float, str, D)) else observed
    try:
        rel = abs((obs - ref) / ref)
    except (InvalidOperation, ZeroDivisionError):
        rel = D("Infinity")
    passed = rel > tol
    checks.append({"name": name, "observed": fmt(obs), "reference": fmt(ref),
                   "relresidual": str(rel), "tol": str(tol), "pass": passed,
                   "kind": kind, "unit": unit})
    return passed

def check_abs(name, observed, ref, atol, kind, unit, fmt=lambda x: str(x)):
    """Absolute-residual check (for ref == 0 or scale-free residuals)."""
    obs = D(observed) if isinstance(observed, (int, float, str, D)) else observed
    ares = abs(obs - ref)
    passed = ares <= atol
    checks.append({"name": name, "observed": fmt(obs), "reference": fmt(ref),
                   "absresidual": str(ares), "atol": str(atol), "pass": passed,
                   "kind": kind, "unit": unit})
    return passed

# ---------------------------------------------------------------- step 2 / NC1: the two model comparisons
# Round-trip: canonical footing reproduces itself at kappa=1/2, rho_L_can (consistency).
a0_repro_can = kappa_can * c * (G * rho_L_can).sqrt()
# Round-trip: alternative footing reproduces itself at kappa=1/2, rho_L_alt (consistency).
a0_repro_alt = kappa_can * c * (G * rho_L_alt).sqrt()
# Effective kappa when rho fixed at canonical value.
kappa_alt_eff = a0_alt / (c * (G * rho_L_can).sqrt())
delta_kappa = kappa_alt_eff - kappa_can

ok = True
ok &= check("NC1a canonical round-trip a0(kappa=1/2, rho_L_can) == a0_can",
            a0_repro_can, a0_can, D("1e-50"), "negative control (self-consistency)", "m s^-2")
ok &= check("NC1b alternative round-trip a0(kappa=1/2, rho_L_alt) == a0_alt",
            a0_repro_alt, a0_alt, D("1e-50"), "negative control (self-consistency)", "m s^-2")
# THE inconsistency flag: a0(kappa=1/2, rho_L_can) != a0_alt — both fixed cannot hold.
rel_alt_vs_can = abs((a0_repro_can - a0_alt) / a0_alt)
nc1_flag = rel_alt_vs_can > D("1e-9")   # expects INconsistency (large residual)
ok &= check_flag("NC1c BOTH (kappa, rho_L) fixed at canonical: different a0 MUST be flagged",
                 a0_repro_can, a0_alt, D("1e-9"), "negative control (inconsistency detection)", "m s^-2")
rel_alt2 = abs((a0_repro_alt - a0_can) / a0_can)
nc1_flag2 = rel_alt2 > D("1e-9")
ok &= check_flag("NC1d BOTH fixed at alternative: a0_can MUST be flagged as unreproducible",
                 a0_repro_alt, a0_can, D("1e-9"), "negative control (inconsistency detection)", "m s^-2")

# Interpretation A: fixed rho_L -> kappa shifts to R_a/2 (exact identity, 60 digits)
ok &= check("A1 kappa_alt(fixed rho) == R_a/2", kappa_alt_fixedrho, R_a / D(2), D("1e-55"),
            "exact algebraic identity (numerical witness)", "dimensionless")
# Interpretation B: fixed kappa -> density ratio R_a^2
ok &= check("B1 rho_L_alt/rho_L_can == R_a^2", rho_L_alt / rho_L_can, R_a2, D("1e-55"),
            "exact algebraic identity (numerical witness)", "dimensionless")
ok &= check("B2 (a0_alt/a0_can)^2 == 1.45148716 stated", R_a2, D("1.45148716"), D("2e-7"),
            "finite numerical consistency vs stated constant", "dimensionless")
ok &= check("B3 Lambda_alt/Lambda_can == R_a^2", Lambda_alt / Lambda_can, R_a2, D("1e-55"),
            "exact algebraic identity (numerical witness)", "dimensionless")
# effective kappa shift
ok &= check("A3 delta kappa = R_a/2 - 1/2", delta_kappa, (R_a - D(1)) / D(2), D("1e-55"),
            "exact algebraic identity (numerical witness)", "dimensionless")

# ---------------------------------------------------------------- step 4: independent representations
pi60 = D("3.14159265358979323846264338327950288419716939937510582097494459")
# C1: Lambda representation  a0 = c^2 sqrt(Lambda/(32 pi))
a0_from_Lambda_c = c * c * (Lambda_can / (D(32) * pi60)).sqrt()
ok &= check("C1 a0 recovered from Lambda representation (canonical)", a0_from_Lambda_c, a0_can,
            D("1e-50"), "independent representation (Lambda)", "m s^-2")
# C2: energy-density representation  a0 = kappa sqrt(G eps), eps = rho c^2
a0_from_eps_c = kappa_can * (G * eps_L_can).sqrt()
ok &= check("C2 a0 recovered from energy-density representation (canonical)", a0_from_eps_c, a0_can,
            D("1e-50"), "independent representation (energy density)", "m s^-2")
# C3: dimensionless factorization  R_a^2 = K^2 * D with K=kappa ratio, D=rho ratio
K_A = kappa_alt_fixedrho / kappa_can   # = R_a  (fixed rho)
D_A = rho_L_can / rho_L_can            # = 1
K_B = kappa_can / kappa_can            # = 1  (fixed kappa)
D_B = rho_L_alt / rho_L_can            # = R_a^2
prod_A = (K_A * K_A) * D_A
prod_B = (K_B * K_B) * D_B
prod_bothfixed = D(1) * D(1) * D(1)    # K=1, D=1: cannot reach R_a^2
ok &= check("C3a R_a^2 = (kappa_alt/kappa_can)^2 * 1 under footing A", prod_A, R_a2, D("1e-55"),
            "dimensionless factorization", "dimensionless")
ok &= check("C3b R_a^2 = 1 * (rho_alt/rho_can) under footing B", prod_B, R_a2, D("1e-55"),
            "dimensionless factorization", "dimensionless")
ok &= check_flag("C3c R_a^2 = 1 * 1 under BOTH fixed: incompatibility MUST be flagged",
                 prod_bothfixed, R_a2, D("1e-9"), "negative control (both-fixed impossible)", "dimensionless")

# ---------------------------------------------------------------- rescaling of dimensional predictions (fixed baryons)
sqrtRa = R_a.sqrt()
fourthRa = (R_a.sqrt()).sqrt()
rescale = {
    "Newtonian g = G M_b / r^2":            {"exponent": D(0),   "ratio": D(1),       "note": "footing-invariant"},
    "deep circular g = sqrt(G M_b a0)/r":   {"exponent": D("0.5"),"ratio": sqrtRa,    "note": "scales with a0^(1/2)"},
    "v_flat = (G M_b a0)^(1/4)":            {"exponent": D("0.25"),"ratio": fourthRa, "note": "scales with a0^(1/4)"},
    "r_M = sqrt(G M_b / a0)":               {"exponent": D("-0.5"),"ratio": D(1)/sqrtRa, "note": "scales with a0^(-1/2)"},
}
for name, v in rescale.items():
    ok &= check(f"R1 {name} ratio == R_a^exponent", v["ratio"],
                (D(10) ** (v["exponent"] * (R_a.log10()))), D("1e-55"),
                "exact power-law rescaling (numerical witness)", "dimensionless")

# dimensional examples: two baryonic masses, both footings
examples = []
for label, M_b in [("M_sun", M_sun), ("1e11 M_sun (disk galaxy)", D("1e11") * M_sun)]:
    rM_c = (G * M_b / a0_can).sqrt();  rM_a = (G * M_b / a0_alt).sqrt()
    vf_c = (G * M_b * a0_can).sqrt().sqrt();  vf_a = (G * M_b * a0_alt).sqrt().sqrt()
    gN_at_rMc = G * M_b / (rM_c * rM_c)      # Newtonian g at r = r_M(canonical), same for both footings
    examples.append({
        "M_b": str(M_b), "M_b_kg": str(M_b),
        "r_M_canon_m": str(rM_c), "r_M_canon_kpc": str(rM_c / KPC),
        "r_M_alt_m": str(rM_a), "r_M_alt_kpc": str(rM_a / KPC),
        "r_M_ratio_alt_over_can": str(rM_a / rM_c),
        "v_flat_canon_m_s": str(vf_c), "v_flat_canon_km_s": str(vf_c / D(1000)),
        "v_flat_alt_m_s": str(vf_a), "v_flat_alt_km_s": str(vf_a / D(1000)),
        "v_flat_ratio_alt_over_can": str(vf_a / vf_c),
        "gN_at_rMc_m_s2": str(gN_at_rMc),
    })

# ---------------------------------------------------------------- NC2: limiting regimes (labeled Q-branch comparison)
# Exact identity on Q: v^4 = G M a0 + (G M / r)^2 for ALL r>0 (derive: v^2 = g r, g^2 = B^2 + a0 B, B = GM/r^2).
# Deep limit r >> r_M: v^4 -> G M a0; leading neglected term (G M / r)^2; relative correction (r_M/r)^2.
M_b = D("1e11") * M_sun
resid_max = D(0)
for r_over_rM in [D(2), D(3), D(10), D(100), D("1e4")]:
    r = r_over_rM * (G * M_b / a0_can).sqrt()
    B = G * M_b / (r * r)
    g = (B * B + a0_can * B).sqrt()
    v4_lhs = (g * r) * (g * r)
    v4_rhs = G * M_b * a0_can + (G * M_b / (r * r)) * (G * M_b)
    resid = abs((v4_lhs - v4_rhs) / v4_rhs)
    resid_max = max(resid_max, resid)
    if float(r_over_rM) == 10.0:
        corr = (G * M_b / (r * r)) * (G * M_b) / (G * M_b * a0_can)   # relative correction = (r_M/r)^2
        check("NC2a leading deep-limit correction (GM/r)^2 / (GMa0) == (r_M/r)^2 at r=10 r_M",
              corr, (D(1)/D(10))**2, D("1e-30"), "limiting-regime leading term", "dimensionless")
ok &= check_abs("NC2b Q-branch exact identity v^4 = GMa0 + (GM/r)^2, max |abs residual| over r/r_M in {2,3,10,100,1e4}",
                resid_max, D(0), D("1e-50"), "exact algebraic identity (60-digit witness)", "m^4 s^-4")
# (resid_max is itself a relative residual: abs((lhs-rhs)/rhs) per sample point, rhs ~ 1.24e21 m^4/s^4)

# boundary case y = B/a0 = 1: on Q, g/a0 = sqrt(2) on BOTH footings (dimensionless)
for a0, tag in [(a0_can, "canonical"), (a0_alt, "alternative")]:
    B = a0
    g = (B * B + a0 * B).sqrt()
    ok &= check(f"NC2c y=1 boundary g/a0 == sqrt(2) ({tag} footing)", g / a0,
                D(2).sqrt(), D("1e-50"), "normalization/boundary case (Q branch, labeled)", "dimensionless")

# ---------------------------------------------------------------- summary numbers
dens_ratio = rho_L_alt / rho_L_can
out = {
    "run_id": "run_20260927T224056Z",
    "a0_can_m_s2": str(a0_can), "a0_alt_m_s2": str(a0_alt),
    "R_a": str(R_a), "R_a2": str(R_a2), "R_a2_stated": "1.45148716",
    "rho_L_can_kg_m3": str(rho_L_can), "rho_L_alt_kg_m3": str(rho_L_alt),
    "rho_ratio_alt_over_can": str(dens_ratio),
    "eps_L_can_J_m3": str(eps_L_can), "eps_L_alt_J_m3": str(eps_L_alt),
    "Lambda_can_m2": str(Lambda_can), "Lambda_alt_m2": str(Lambda_alt),
    "Lambda_alt_over_can": str(Lambda_alt / Lambda_can),
    "kappa_can": str(kappa_can), "kappa_alt_fixed_rho": str(kappa_alt_eff),
    "kappa_shift_delta": str(delta_kappa), "kappa_rel_shift": str(delta_kappa / kappa_can),
    "kappa_alt_over_kappa_can": str(kappa_alt_eff / kappa_can),
    "inconsistency_flag_NC1c": bool(nc1_flag), "inconsistency_flag_NC1d": bool(nc1_flag2),
    "rescale_exponents": rescale,
    "dimensional_examples": examples,
    "checks": checks,
    "bounds": bounds,
    "wall_seconds": None,
}
# wall clock + rusage
out["wall_seconds"] = round(time.perf_counter() - t_start, 4)
ru = resource.getrusage(resource.RUSAGE_SELF)
out["maxrss_bytes"] = ru.ru_maxrss
bounds["measured_wall_s"] = out["wall_seconds"]
bounds["measured_maxrss_bytes"] = ru.ru_maxrss
bounds["wall_under_120s"] = out["wall_seconds"] < 120.0
bounds["rss_under_512MB"] = ru.ru_maxrss < 512 * 1024 * 1024

all_pass = all(ch["pass"] for ch in checks) and nc1_flag and nc1_flag2 and bounds["wall_under_120s"] and bounds["rss_under_512MB"]
out["all_checks_pass"] = bool(all_pass)

with open("raw_output.json", "w") as f:
    json.dump(out, f, indent=2, cls=_Enc)

# human-readable summary
print("=" * 78)
print("AS011 bounding computation — alternative footing as a separate hypothesis")
print("=" * 78)
print(f"R_a = a0_alt/a0_can            = {R_a}")
print(f"R_a^2                          = {R_a2}   (stated 1.45148716)")
print(f"rho_L_can [kg/m^3]             = {rho_L_can}")
print(f"rho_L_alt [kg/m^3]             = {rho_L_alt}   (ratio {dens_ratio})")
print(f"eps_L_can [J/m^3]              = {eps_L_can}")
print(f"Lambda_can [m^-2]              = {Lambda_can}")
print(f"kappa_alt (fixed rho)          = {kappa_alt_eff}  (= R_a/2 = {R_a/D(2)})")
print(f"delta kappa                    = {delta_kappa}   (relative {delta_kappa/kappa_can})")
print(f"NC1c both-fixed a0_alt flag    = {bool(nc1_flag)}  (residual vs a0_can {rel_alt_vs_can})")
print(f"NC1d both-fixed a0_can flag    = {bool(nc1_flag2)}  (residual vs a0_alt {rel_alt2})")
print("-" * 78)
for ch in checks:
    resid = ch.get("relresidual", ch.get("absresidual", "?"))
    tol = ch.get("tol", ch.get("atol", "?"))
    print(f"[{'PASS' if ch['pass'] else 'FAIL'}] {ch['name']}: obs={ch['observed']} ref={ch['reference']} res={resid} tol={tol}")
print("-" * 78)
print("Dimensional examples (both footings carried):")
for ex in examples:
    print(f"  M_b={ex['M_b_kg']} kg: r_M(can)={ex['r_M_canon_kpc']} kpc, r_M(alt)={ex['r_M_alt_kpc']} kpc, ratio={ex['r_M_ratio_alt_over_can']}")
    print(f"    v_flat(can)={ex['v_flat_canon_km_s']} km/s, v_flat(alt)={ex['v_flat_alt_km_s']} km/s, ratio={ex['v_flat_ratio_alt_over_can']}")
print("-" * 78)
print(f"bounds: wall={out['wall_seconds']}s (<120 enforced via RLIMIT_CPU + timer), "
      f"maxrss={ru.ru_maxrss} bytes (<512MB enforced via RLIMIT_AS), threads=0 spawned")
print(f"ALL CHECKS PASS = {all_pass}")
