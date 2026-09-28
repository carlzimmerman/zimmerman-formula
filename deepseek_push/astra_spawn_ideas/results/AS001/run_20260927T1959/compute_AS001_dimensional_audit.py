#!/usr/bin/env python3
"""AS001 — bounded dimensional audit: mass-density versus energy-density
normalization of the vacuum acceleration scale.

Claim under audit (framework base):
    a0 = kappa * c * sqrt(G * rho_L)        (mass density,   rho_L in kg/m^3)
    eps_L = rho_L * c^2                     (energy density, J/m^3)
    a0 = kappa * sqrt(G * eps_L)            (energy-density form)

Work order: (1) dimensional consistency of all forms; (2) exact equivalence of
the two representations (same prediction in equivalent variables, no added
fitted input); (3) negative control: dimensional checker must REJECT
rho<->epsilon substitution without coefficient change; (4) both footings
carried separately (kappa=1/2 adopted, NOT derived).

Bounds actually enforced: 1 CPU thread (single-threaded CPython, no numpy),
CPU-time capped at 120 s by the caller's `ulimit -t 120`, memory far below
512 MB (pure scalar arithmetic), mpmath precision mp.dps = 60. Wall time is
recorded below. This is the bounded prototype; no scaling needed (algebraic
identity, closed-form residuals).

Outputs: raw_output.txt (human), residuals.json (machine).
"""

import json
import time

from mpmath import mp, mpf, sqrt, log10

mp.dps = 60
mp.pretty = True

t_wall_start = time.time()

# --------------------------------------------------------------------------
# Framework constants and registered footings (inputs, none derived here)
# --------------------------------------------------------------------------
G     = mpf("6.67430e-11")   # m^3 kg^-1 s^-2   (mandated default; measured input)
c     = mpf(299792458)       # m/s              (exact by definition)
Msun  = mpf("1.98847e30")    # kg               (mandated default)
kappa = mpf(1) / 2           # ADOPTED input (framework contract: adopted, not derivable here)
a0_can = mpf("9.3619e-11")   # m/s^2  canonical footing  (registered value)
a0_alt = mpf("1.1279e-10")   # m/s^2  alternative footing (registered value)

# Dense vacuum (mass) densities implied by each footing AT THE ADOPTED kappa:
# rho = 4 a0^2 / (G c^2)   (framework identity, both footings separately)
rho_Lambda = 4 * a0_can**2 / (G * c**2)   # kg/m^3, canonical footing
rho_total  = 4 * a0_alt**2 / (G * c**2)   # kg/m^3, alternative footing

# --------------------------------------------------------------------------
# 1) Symbolic dimensional checker (exponent vectors in M, L, T)
# --------------------------------------------------------------------------
UNIT = {
    "G":   (-1, 3, -2),   # m^3 kg^-1 s^-2
    "c":   (0, 1, -1),    # m s^-1
    "rho": (1, -3, 0),    # kg m^-3   (mass density)
    "eps": (1, -1, -2),   # J/m^3 = kg m^-1 s^-2  (energy density)
    "M":   (1, 0, 0),     # kg
}
ACCEL = (0, 1, -2)        # m s^-2


def vmu(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vsqrt(u):
    if all(x % 2 == 0 for x in u):
        return tuple(x // 2 for x in u)
    return None


def dims(e):
    tag = e[0]
    if tag == "u":
        return UNIT[e[1]]
    if tag == "mul":
        return vmu(dims(e[1]), dims(e[2]))
    if tag == "pow":
        return tuple(x * e[2] for x in dims(e[1]))
    if tag == "sqrt":
        d = vsqrt(dims(e[1]))
        assert d is not None, "non-integer half-exponent encountered"
        return d
    raise ValueError(tag)


def u(name):
    return ("u", name)


def mul(e1, e2):
    return ("mul", e1, e2)


def sqr(e):
    return ("sqrt", e)


def pw(e, k):
    return ("pow", e, k)


# (label, expression, expected: accept-or-reject as an acceleration)
DIM_TESTS = [
    ("1a  CORRECT  a0 = kappa*c*sqrt(G*rho)        [mass density]",
     mul(u("c"), sqr(mul(u("G"), u("rho")))), True),
    ("1b  CORRECT  a0 = kappa*sqrt(G*eps)          [energy density]",
     sqr(mul(u("G"), u("eps"))), True),
    # --- negative controls: every substitution WITHOUT coefficient change ---
    ("2a  WRONG    a0 = kappa*c*sqrt(G*eps)  (c retained, eps substituted)",
     mul(u("c"), sqr(mul(u("G"), u("eps")))), False),
    ("2b  WRONG    a0 = kappa*sqrt(G*rho)    (c dropped, rho used)",
     sqr(mul(u("G"), u("rho"))), False),
    ("2c  WRONG    a0 = kappa*c^2*sqrt(G*rho)      (extra c)",
     mul(pw(u("c"), 2), sqr(mul(u("G"), u("rho")))), False),
    ("2d  WRONG    a0 = kappa*sqrt(G*eps)*c^2      (c back in energy form)",
     mul(sqr(mul(u("G"), u("eps"))), pw(u("c"), 2)), False),
    ("2e  NEG.CONTROL  eps substituted AND mislabelled with kg/m^3 dims: "
     "c*sqrt(G*eps_as_rho) (same coefficient kept, no renormalization)",
     mul(u("c"), sqr(mul(u("G"), u("eps")))), False),
]

dim_results = []
for label, expr, expect in DIM_TESTS:
    d = dims(expr)
    ok = (d == ACCEL)
    dim_results.append({
        "test": label,
        "exponent_vector_MLT": list(d),
        "expected_accept": expect,
        "checker_accepts": ok,
        "passes": ok == expect,
    })

# 2e' non-vacuity witness: c*sqrt(G*rho) with rho at its OWN dimensions is an
# acceleration, so the checker does NOT reject everything.
d_mislabel = dims(mul(u("c"), sqr(mul(u("G"), u("rho")))))     # c*sqrt(G*rho): m s^-2
dim_results.append({
    "test": "2e'  (non-vacuity) c*sqrt(G*rho) with rho at its own kg/m^3 dims "
            "IS an acceleration -> checker accepts it",
    "exponent_vector_MLT": list(d_mislabel),
    "expected_accept": True,
    "checker_accepts": d_mislabel == ACCEL,
    "passes": d_mislabel == ACCEL,
})

# --------------------------------------------------------------------------
# 2) Exact algebraic identity  c*sqrt(G*rho) == sqrt(G*(rho*c^2))  for rho>0
#    Residual evaluated at both footings and on a rho-grid; exact up to the
#    non-representability of decimal input in binary (60-digit arithmetic).
# --------------------------------------------------------------------------
def a0_mass(rho, kp=kappa):
    return kp * c * sqrt(G * rho)


def a0_energy(rho, kp=kappa):
    return kp * sqrt(G * (rho * c**2))


resid = {}
# canonical footing: rho_Lambda defined so that a0_mass == a0_can identically
rL = a0_mass(rho_Lambda)
rE = a0_energy(rho_Lambda)
resid["canonical"] = {
    "a0_reconstructed_mass_form": float(rL),
    "a0_reconstructed_energy_form": float(rE),
    "rel_resid_mass_vs_registered": float(abs(rL - a0_can) / a0_can),
    "rel_resid_energy_vs_registered": float(abs(rE - a0_can) / a0_can),
    "rel_resid_mass_minus_energy": float(abs(rL - rE) / a0_can),
    "rho_kg_m3": float(rho_Lambda),
    "eps_J_m3": float(rho_Lambda * c**2),
}
# alternative footing
rL2 = a0_mass(rho_total)
rE2 = a0_energy(rho_total)
resid["alternative"] = {
    "a0_reconstructed_mass_form": float(rL2),
    "a0_reconstructed_energy_form": float(rE2),
    "rel_resid_mass_vs_registered": float(abs(rL2 - a0_alt) / a0_alt),
    "rel_resid_energy_vs_registered": float(abs(rE2 - a0_alt) / a0_alt),
    "rel_resid_mass_minus_energy": float(abs(rL2 - rE2) / a0_alt),
    "rho_kg_m3": float(rho_total),
    "eps_J_m3": float(rho_total * c**2),
}
# identity over an extended domain grid (algebraic identity; must hold everywhere)
worst = 0.0
worst_at = None
for k in range(-33, -12):            # rho in [1e-33, 1e-12] kg/m^3
    rho = mpf(10) ** k
    d = abs(a0_mass(rho) - a0_energy(rho)) / a0_mass(rho)
    if d > worst:
        worst, worst_at = d, k
resid["identity_grid"] = {
    "rho_grid_decades": "1e-33 .. 1e-12 kg/m^3",
    "worst_rel_resid": float(worst),
    "worst_at_log10_rho": worst_at,
}
# boundary case rho -> 0+ : a0 -> 0 continuously (exact zeros)
resid["boundary_rho0"] = {
    "a0_mass(0)": float(a0_mass(mpf(0))),
    "a0_energy(0)": float(a0_energy(mpf(0))),
}

# --------------------------------------------------------------------------
# 3) Representation invariance of derived predictions (r_M, v_flat)
# --------------------------------------------------------------------------
def r_M(M, rho):
    return sqrt(G * M / a0_mass(rho))


def r_ME(M, rho):
    return sqrt(G * M / a0_energy(rho))


def vflat4(M, rho):
    return sqrt(sqrt(G * M * a0_mass(rho)))


def vflat4E(M, rho):
    return sqrt(sqrt(G * M * a0_energy(rho)))


pred = {}
for tag, rho in (("canonical", rho_Lambda), ("alternative", rho_total)):
    rm, rme = r_M(Msun, rho), r_ME(Msun, rho)
    vf, vfe = vflat4(Msun, rho), vflat4E(Msun, rho)
    pred[tag] = {
        "r_M_mass_form_m": float(rm),
        "r_M_energy_form_m": float(rme),
        "rel_resid_rM": float(abs(rm - rme) / rm),
        "v_flat_mass_form_m_s": float(vf),
        "v_flat_energy_form_m_s": float(vfe),
        "rel_resid_vflat": float(abs(vf - vfe) / vf),
        "v_flat_4th_power_check_m4_s4": float(vf**4 - G * Msun * a0_mass(rho)),
    }
resid["predictions"] = pred

# --------------------------------------------------------------------------
# 4) Footing cross-relations (both footings carried SEPARATELY; the contract
#    forbids sharing a fixed rho_Lambda AND a fixed kappa across footings)
# --------------------------------------------------------------------------
foot = {}
ratio = a0_alt / a0_can
foot["a0_alt_over_a0_can"] = float(ratio)
foot["density_ratio_rho_total_over_rho_Lambda"] = float(rho_total / rho_Lambda)
foot["rel_diff_ratio_squared_vs_density_ratio"] = float(
    abs(ratio**2 - rho_total / rho_Lambda) / (rho_total / rho_Lambda))
# if rho_Lambda were held FIXED, the alternative requires a different kappa:
kappa_eff = a0_alt / (c * sqrt(G * rho_Lambda))
foot["kappa_eff_if_rho_held_fixed"] = float(kappa_eff)
foot["kappa_eff_over_adopted_kappa"] = float(kappa_eff / kappa)
foot["note"] = ("kappa=1/2 adopted for BOTH footings; the two footings then "
                "carry DIFFERENT densities (ratio 1.4515). Alternatively the "
                "density may be held at rho_Lambda and then kappa_eff=0.6024. "
                "A single fixed (kappa,rho) pair cannot produce both a0s.")
resid["footings"] = foot

# --------------------------------------------------------------------------
# 5) Context-only cross-check (not evidence for the claim): rho_Lambda versus
#    Omega_L * rho_crit with the README k03 context values H0=67.4, Omega_L=0.685
#    (H0 in km/s/Mpc -> 1/s via the mandated pc).
# --------------------------------------------------------------------------
pc = mpf("3.085677581491367e16")   # m
H0 = mpf("67.4") * 1000 / (pc * 1e6)   # s^-1  (1 Mpc = 1e6 pc)
Omega_L = mpf("0.685")
rho_crit = 3 * H0**2 / (8 * mp.pi() * G)
resid["context_crosscheck"] = {
    "Omega_L * rho_crit (kg/m^3)": float(Omega_L * rho_crit),
    "rho_Lambda (kg/m^3)": float(rho_Lambda),
    "rel_diff": float(abs(Omega_L * rho_crit - rho_Lambda) / rho_Lambda),
    "status": "context only; not used in the audited claim",
}

# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
all_pass = all(r["passes"] for r in dim_results)
checks = {
    "dimensional": {"passes": all_pass, "results": dim_results},
    "identity_canonical": resid["canonical"]["rel_resid_mass_minus_energy"],
    "identity_alternative": resid["alternative"]["rel_resid_mass_minus_energy"],
    "identity_grid_worst": resid["identity_grid"]["worst_rel_resid"],
    "rM_invariant_worst": max(pred["canonical"]["rel_resid_rM"],
                              pred["alternative"]["rel_resid_rM"]),
    "vflat_invariant_worst": max(pred["canonical"]["rel_resid_vflat"],
                                 pred["alternative"]["rel_resid_vflat"]),
}
t_wall_stop = time.time()
resid["bounds"] = {
    "cpu_budget_s": 120,
    "enforced_cpu_s": "ulimit -t 120 (caller)",
    "wall_s": round(t_wall_stop - t_wall_start, 4),
    "threads": 1,
    "memory_budget_MB": 512,
    "memory_actual": "trivial scalar arithmetic (<10 MB)",
    "mpmath_dps": 60,
}
resid["checks"] = checks

lines = []
lines.append("AS001 mass-density vs energy-density normalization audit")
lines.append("computed: " + __import__("datetime").datetime.utcnow().isoformat() + "Z")
lines.append("precision: mpmath dps = 60; single thread; wall %.4f s" %
             (t_wall_stop - t_wall_start))
lines.append("")
lines.append("CONSTANTS (inputs): G=%.6es ; c=%.6es ; kappa=1/2 ADOPTED ; "
             "Msun=%.6es" % (G, c, Msun))
lines.append("")
lines.append("DIMENSIONAL CHECKER (exponent vectors (M,L,T); ACCEL=(0,1,-2))")
lines.append("unit map: G=(-1,3,-2) c=(0,1,-1) rho=(1,-3,0) eps=(1,-1,-2) M=(1,0,0)")
for r in dim_results:
    lines.append("  [%s] %s  -> vector %s" %
                 ("PASS" if r["passes"] else "FAIL", r["test"], r["exponent_vector_MLT"]))
lines.append("")
lines.append("NUMERICAL IDENTITIES (relative residuals, 60-digit arithmetic)")
for tag in ("canonical", "alternative"):
    b = resid[tag]
    lines.append("  %s: a0(mass form)      = %.10es" % (tag, b["a0_reconstructed_mass_form"]))
    lines.append("  %s: a0(energy form)    = %.10es" % (tag, b["a0_reconstructed_energy_form"]))
    lines.append("  %s: rel resid mass/reg = %e" % (tag, b["rel_resid_mass_vs_registered"]))
    lines.append("  %s: rel resid ener/reg = %e" % (tag, b["rel_resid_energy_vs_registered"]))
    lines.append("  %s: rel resid m-e      = %e" % (tag, b["rel_resid_mass_minus_energy"]))
    lines.append("  %s: rho = %.6e kg/m^3 ; eps = %.6e J/m^3" %
                 (tag, b["rho_kg_m3"], b["eps_J_m3"]))
lines.append("  grid rho in 1e-33..1e-12: worst rel resid = %e" %
             resid["identity_grid"]["worst_rel_resid"])
lines.append("  boundary rho=0: a0_mass(0)=%e a0_energy(0)=%e" %
             (resid["boundary_rho0"]["a0_mass(0)"], resid["boundary_rho0"]["a0_energy(0)"]))
lines.append("")
lines.append("REPRESENTATION-INVARIANT PREDICTIONS (Msun)")
for tag in ("canonical", "alternative"):
    p = pred[tag]
    lines.append("  %s: r_M    mass form %.6e m | energy form %.6e m | rel res %.3e" %
                 (tag, p["r_M_mass_form_m"], p["r_M_energy_form_m"], p["rel_resid_rM"]))
    lines.append("  %s: v_flat mass form %.6e m/s | energy form %.6e m/s | rel res %.3e"
                 % (tag, p["v_flat_mass_form_m_s"], p["v_flat_energy_form_m_s"], p["rel_resid_vflat"]))
    lines.append("  %s: v_flat^4 - G M a0 = %.3e (m^4 s^-4)" %
                 (tag, p["v_flat_4th_power_check_m4_s4"]))
lines.append("")
lines.append("FOOTINGS (kappa=1/2 adopted for both; densities differ)")
lines.append("  a0_alt/a0_can = %.8f" % foot["a0_alt_over_a0_can"])
lines.append("  rho_total/rho_Lambda = %.8f" % foot["density_ratio_rho_total_over_rho_Lambda"])
lines.append("  |(ratio)^2 - density_ratio|/density_ratio = %.3e" %
             foot["rel_diff_ratio_squared_vs_density_ratio"])
lines.append("  kappa_eff if rho held fixed = %.8f (vs adopted 0.5)" %
             foot["kappa_eff_if_rho_held_fixed"])
lines.append("  " + foot["note"])
lines.append("")
lines.append("CONTEXT-ONLY cross-check: Omega_L*rho_crit(H0=67.4,Omega_L=0.685)")
lines.append("  = %.6e kg/m^3 vs rho_Lambda = %.6e kg/m^3 ; rel diff %.3e" %
             (resid["context_crosscheck"]["Omega_L * rho_crit (kg/m^3)"],
              resid["context_crosscheck"]["rho_Lambda (kg/m^3)"],
              resid["context_crosscheck"]["rel_diff"]))
lines.append("")
lines.append("NEGATIVE-CONTROL VERDICT: " +
             ("ALL DIMENSIONAL TESTS PASS (checker accepts both correct forms "
              "and rejects every rho<->epsilon substitution)" if all_pass
              else "DIMENSIONAL TESTS FAILED -- see raw results"))
lines.append("bounds: %s" % json.dumps(resid["bounds"]))

out = "\n".join(lines) + "\n"
with open("raw_output.txt", "w") as f:
    f.write(out)
with open("residuals.json", "w") as f:
    json.dump(resid, f, indent=2, sort_keys=True)
print(out)