#!/usr/bin/env python3
"""Read-only CFG428 input audit; writes only the neighboring thermal_results.json."""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTRACT = HERE / "thermal_contract.json"
RESULT = HERE / "thermal_results.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    start = time.perf_counter()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    contract = json.loads(CONTRACT.read_text())
    c = contract["constants"]
    source_names = [
        "campaign_fresh_gravity/CFG428_one_bose_field_ledger/cfg428_ledger.py",
        "campaign_fresh_gravity/CFG428_one_bose_field_ledger/cfg428_results.json",
        "campaign_fresh_gravity/CFG428_one_bose_field_ledger/FROZEN_CRITERIA.md",
        "campaign_fresh_gravity/CFG383_bose_condensate_split/FROZEN_CRITERIA.md",
        "campaign_fresh_gravity/CFG384_self_interacting_bose/cfg384_si_bose.py",
    ]
    hashes_before = {name: sha(ROOT / name) for name in source_names}
    old = json.loads((ROOT / source_names[1]).read_text())
    old_rows = {row["m"]: row for row in old["rows"]}
    rho = c["total_density_kg_m3"] * (1 - c["baryon_fraction"])
    v = c["velocity_m_s"]
    # 1 cm^2 = 1e-4 m^2 and 1 g = 1e-3 kg: divide, do not omit denominator.
    sigma_si = c["cross_section_per_mass_cm2_g"] * (1e-2)**2 / 1e-3
    checks = []

    def check(name, ok, **details):
        checks.append({"name": name, "passed": bool(ok), **details})

    def close(a, b, tol=1e-12):
        return abs(a / b - 1) <= tol

    def si(m_eV, cross_section_per_mass=sigma_si):
        m = m_eV * c["eV_J"] / c["c_m_s"]**2
        n = rho / m
        occ = n * (2 * math.pi * c["hbar_J_s"])**3 / (
            m**3 * (2 * math.pi * v**2)**1.5
        )
        rate = rho * cross_section_per_mass * v * (1 + occ)
        return rate, occ, 1 / rate / c["seconds_per_Gyr"]

    def cgs(m_eV):
        # Independent dimensional path: g, cm, erg, s throughout the rate.
        rho_g_cm3 = rho * 1e3 / 1e6
        mass_g = m_eV * (c["eV_J"] * 1e7) / (c["c_m_s"] * 100)**2
        v_cm_s = v * 100
        hbar_erg_s = c["hbar_J_s"] * 1e7
        number_cm3 = rho_g_cm3 / mass_g
        thermal_wavelength_cm = (2 * math.pi * hbar_erg_s) / (
            mass_g * v_cm_s * math.sqrt(2 * math.pi)
        )
        occ = number_cm3 * thermal_wavelength_cm**3
        cross_section_cm2 = c["cross_section_per_mass_cm2_g"] * mass_g
        rate = number_cm3 * cross_section_cm2 * v_cm_s * (1 + occ)
        return rate, occ, 1 / rate / c["seconds_per_Gyr"]

    check("SI conversion is 0.1 m2/kg", close(sigma_si, 0.1), value=sigma_si)
    rows = []
    for mass in contract["primary_cases_mass_eV"]:
        rate_si, occ_si, t_si = si(mass)
        rate_cgs, occ_cgs, t_cgs = cgs(mass)
        wrong_rate, _, wrong_t = si(mass, c["old_cross_section_per_mass_m2_kg"])
        prior = old_rows[mass]
        check(f"m={mass}: independent SI/cgs rates", close(rate_si, rate_cgs),
              relative_error=abs(rate_si / rate_cgs - 1))
        check(f"m={mass}: independent SI/cgs occupations", close(occ_si, occ_cgs),
              relative_error=abs(occ_si / occ_cgs - 1))
        check(f"m={mass}: reproduce stored erroneous time", close(wrong_t, prior["t_relax_Gyr"]),
              recomputed_Gyr=wrong_t, stored_Gyr=prior["t_relax_Gyr"])
        check(f"m={mass}: time ratio 1000", close(prior["t_relax_Gyr"] / t_si, 1000),
              ratio=prior["t_relax_Gyr"] / t_si)
        check(f"m={mass}: wrong-conversion mutation detected", not close(wrong_rate, rate_cgs),
              mutated_rate_over_independent_rate=wrong_rate / rate_cgs)
        rows.append({
            "mass_eV": mass, "occupation": occ_si,
            "corrected_rate_s_inverse": rate_si, "independent_cgs_rate_s_inverse": rate_cgs,
            "stored_time_Gyr": prior["t_relax_Gyr"], "corrected_time_Gyr": t_si,
            "independent_cgs_time_Gyr": t_cgs,
            "time_over_threshold": t_si / c["threshold_Gyr"],
            "primary_thermal_allowed": t_si <= c["threshold_Gyr"],
            "corrected_depletion_sigma_over_mass_cm2_g": [
                {"normal_fraction": item[0], "value": item[2] / 1000}
                for item in prior["dep"]
            ],
        })

    # Post-hoc boundary only: occ(m_eV)=B/m_eV^4 and t=t0/(1+B/m_eV^4).
    B = si(1.0)[1]
    t0 = 1 / (rho * sigma_si * v) / c["seconds_per_Gyr"]
    threshold = c["threshold_Gyr"]
    mcrit = (B / (t0 / threshold - 1))**0.25
    root_time = si(mcrit)[2]
    check("analytic critical-mass substitution", close(root_time, threshold),
          critical_mass_eV=mcrit, substituted_time_Gyr=root_time)
    lo, hi = contract["primary_window_mass_eV"]
    continuum_allowed = lo <= mcrit
    # No grid is needed: dt/dm = 4*t0*B*m^3/(m^4+B)^2 > 0.
    boundary = {
        "label": "POST HOC numerical boundary; not a phase prediction",
        "occupation_B_in_eV_units": B, "unboosted_time_Gyr": t0,
        "formula": "mcrit=(B/(t0/tH-1))^(1/4); dt/dm=4*t0*B*m^3/(m^4+B)^2 > 0",
        "critical_mass_eV": mcrit,
        "critical_time_Gyr": root_time,
        "declared_window_eV": [lo, hi],
        "any_thermal_overlap_in_declared_continuum": continuum_allowed,
        "fractional_lower_mass_bound_shift_to_equality": 1 - mcrit / lo,
        "fastest_declared_time_Gyr": si(lo)[2],
        "minimum_sigma_over_mass_cm2_g_at_lower_bound": si(lo)[2] / threshold,
    }
    check("Claude source files unchanged", hashes_before == {name: sha(ROOT / name) for name in source_names})
    good = all(row["passed"] for row in checks)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    status = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=normal"], cwd=ROOT, text=True)
    artifact_hashes = [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)}
                       for p in (CONTRACT, Path(__file__).resolve())]
    result = {
        "schema_version": 1,
        "claim_id": contract["contract_id"],
        "repository": {"commit": commit, "dirty": bool(status.strip()),
                       "dirty_state_scope": "Whole repository; unrelated changes pre-existed. Source inputs hashed separately."},
        "command": "python3 sol61_push/cold_field_identity_2026_10_10/thermal_audit.py",
        "environment": {"software": [f"Python {platform.python_version()} (standard library only)"],
                        "hardware": f"{platform.system()} {platform.machine()}"},
        "mathematics": {
            "assertion_tested": "CFG428 contains a 1000-fold cross-section unit conversion error; correct times and assess its unchanged threshold and mass interval.",
            "coefficient_domain": "IEEE-754 Python binary64 floats; analytic monotonicity in positive real mass.",
            "conventions": "Original CFG428 rho, velocity, age, hbar and 1+occupation kept; SI and cgs evaluated independently.",
            "inputs": [{"path": name, "sha256": value} for name, value in hashes_before.items()],
            "bounds": {"primary_cases_eV": contract["primary_cases_mass_eV"],
                       "declared_continuum_eV": [lo, hi], "relative_check_tolerance": 1e-12,
                       "grid_scan_performed": False},
            "non_claims": contract["non_claims"],
        },
        "randomness": {"used": False, "generator": "none", "seed": None},
        "run": {"started_at": started, "runtime_seconds": time.perf_counter() - start,
                "exit_status": 0 if good else 1},
        "outputs": artifact_hashes,
        "checks": checks,
        "result": "implementation and finite assertion verified in the stated range" if good else "inconsistent with a benchmark or invariant",
        "primary_rows": rows,
        "posthoc_boundary": boundary,
        "documentary_reading": {
            "depletion_vs_thermal": "Alternatives: CFG428 ONE FIELD VIABLE depends on tests 1 and 3, not test 2.",
            "mass_floor": "0.62 eV is the fixed lower endpoint of the CFG383 calibrated cluster normal-fraction/velocity bracket, not a microscopic or cosmological mass floor.",
            "CFG384_units": "Uses cm2/g directly, m_kg*1000 for grams, n_SI*1e-6 for cm^-3 and v_SI*100 for cm/s; no matching factor-1000 bug found in these conversions.",
            "CFG384_differences": "Its cluster density is 0.85*500*rho_crit/3; enhancement max(D,1), with g=1 and a reported g=2 variant. It is not numerically identical to CFG428's rho and 1+D prescription.",
            "unchanged_primary_outcome": "No thermal overlap on [0.62,1.04] eV at the exact declared constants; headline severity changes from thousands-fold failure to a 2.32% boundary miss at the favorable end.",
        },
        "residual_risks": [
            "The phenomenological rate and recalled 1 cm2/g bound are inputs, not independently authenticated physical theorems.",
            "The boundary is close to the declared lower endpoint; this run does not vary density, velocity, species, thermal closure or calibrated fraction.",
            "Results JSON contains the manifest and scientific rows; output hashes cover the contract and code, not a recursive hash of this file. Input hashes are recorded explicitly.",
        ],
    }
    RESULT.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"result": result["result"], "checks_passed": sum(r["passed"] for r in checks),
                      "checks_total": len(checks), "corrected_times_Gyr": [r["corrected_time_Gyr"] for r in rows],
                      "posthoc_critical_mass_eV": mcrit, "declared_continuum_overlap": continuum_allowed}, indent=2))
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
