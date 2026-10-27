"""Finite-stock gravothermal-envelope diagnostic, not a kinetic simulation."""
import json
import math
import platform
import resource
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
data = json.loads((BASE / "inputs.json").read_text())
checks = []


def check(name, value):
    checks.append({"name": name, "pass": bool(value)})
    if not value:
        raise AssertionError(name)


def mass(r, rc, alpha):
    """M/(4pi rho_c), R_outer=1, continuous flat core + power envelope."""
    if r <= rc:
        return r**3 / 3
    q = 3 - alpha
    return rc**3 / 3 + rc**alpha * (r**q - rc**q) / q


def quadrature_mass(r, rc, alpha, n=12000):
    """Independent midpoint integration of r^2 rho(r) on a uniform radius grid."""
    h = r / n
    return h * sum(
        (z := (i + .5) * h)**2 * (1 if z <= rc else (rc / z)**alpha)
        for i in range(n)
    )


alpha = data["alpha"]
q = 3 - alpha
finite_rows = []
for a in [0, 1, 2, alpha, 2.208, 2.5, 2.9]:
    for k in data["outer_radius_over_aperture"]:
        x = 1 / k
        bound = x**(3-a)
        for z in [1e-6, .001, .01, .05, .1, .2, .5, .9, 1]:
            f = mass(x, z, a) / mass(1, z, a)
            check(f"envelope bound alpha={a},k={k},rc={z}", 0 <= f <= bound + 1e-13)
            if z >= .01:
                for r in [x, 1]:
                    exact = mass(r, z, a)
                    numeric = quadrature_mass(r, z, a)
                    check(f"midpoint integral alpha={a},k={k},rc={z},r={r}",
                          abs(exact-numeric) <= 5e-6 * exact)
        finite_rows.append({"alpha": a, "k": k, "aperture_upper_fraction": bound})

for k in data["outer_radius_over_aperture"]:
    check(f"uniform cloud benchmark k={k}",
          abs(mass(1/k, 1, 0)/mass(1, 1, 0)-k**-3) < 1e-15)

target_rows = []
for status, targets in [
    ("old_retained_cap_baseline", {r["name"]: r["fraction"] for r in data["old_targets"]}),
    ("conditional_relative_binary_sensitivity_rounded", data["conditional_relative_targets_from_parent_message"]),
]:
    for name, f in targets.items():
        row = {"status": status, "name": name, "target_fraction": f,
               "max_outer_over_R_if_pure_singular_cusp": f**(-1/q), "k_cases": []}
        for k in data["outer_radius_over_aperture"]:
            p = k**-q
            c = max(0, (f-p)/(1-p))
            required_alpha = 3 + math.log(f)/math.log(k)
            check(f"compact supplement inversion {status},{name},k={k}",
                  abs(c+(1-c)*p-max(f,p)) < 1e-12)
            check(f"slope inversion {status},{name},k={k}",
                  abs(k**(required_alpha-3)-f) < 1e-12)
            row["k_cases"].append({"k": k, "envelope_bound": p,
                "fails_envelope_mass_target": f > p,
                "minimum_compact_component_fraction": c,
                "minimum_allowed_slope_upper_bound": required_alpha})
        target_rows.append(row)

core_rows = []
for shrink in [2, 5, 10, 100]:
    mass_ratio = shrink**-q
    temperature_ratio = shrink**(alpha-2)
    exponent = math.log(mass_ratio)/math.log(temperature_ratio)
    check(f"selfsimilar core scaling shrink={shrink}", abs(exponent-q/(2-alpha)) < 1e-12)
    core_rows.append({"radius_shrink_factor": shrink, "core_mass_ratio": mass_ratio,
                      "central_temperature_ratio": temperature_ratio,
                      "dlogMc_dlog_temperature": exponent})

result = {"claim_id": "CFG853-KINETIC-ENVELOPE-20261019-A",
    "assertion_tested": "Flat core + r^-alpha envelopes satisfy F(R)<= (R/Rt)^(3-alpha); exact target inversions and selfsimilar core scaling for the declared finite cases.",
    "inputs": data, "alpha": alpha, "q": q, "finite_envelope_rows": finite_rows,
    "target_rows": target_rows, "core_scaling_rows": core_rows,
    "n_checks": len(checks), "all_pass": all(c["pass"] for c in checks), "checks": checks,
    "non_claims": ["Not an actual action-produced halo profile or orbit evolution",
       "Not a proof that all BSI numerical profiles obey the global slope bound",
       "No microscopic capture/viscosity cross section or source DF measured",
       "No four-dwarf kinetic history or SPARC fit", "No exclusion of a central soliton, steeper cusp, changing boundary, external work or alternative transport regime"],
    "platform": platform.platform(), "peak_rss_raw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "peak_rss_units": "bytes on Darwin; KiB on Linux"}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"all_pass": result["all_pass"], "n_checks": result["n_checks"],
                  "k5_envelope_bound": 5**-q,
                  "target_rows": target_rows, "core_scaling_rows": core_rows}, indent=2))
