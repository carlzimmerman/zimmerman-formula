#!/usr/bin/env python3
"""Read-only input authentication; output JSON to stdout. No fitting or imports of owner code."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def digest(path):
    b = path.read_bytes()
    return {"path": str(path), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def rows(path, skip=0):
    out = []
    for line in path.read_text().splitlines()[skip:]:
        if line.strip() and not line.lstrip().startswith("#"):
            out.append([float(v) for v in line.split()])
    return out


r = rows(HERE / "UGC08286_rotmod.dat")
d = rows(HERE / "UGC08286.dens")
s = rows(HERE / "UGC08286.sfb", 1)
table2 = [list(map(float, line.split()[1:]))
          for line in (HERE / "MassModels_Lelli2016c.mrt").read_text().splitlines()
          if line.split() and line.split()[0] == "UGC08286"]
local_paths = [
    REPO / "real_research/data/sparc_data/UGC08286_rotmod.dat",
    REPO.parent / "hali_flow/sparc_data/UGC08286_rotmod.dat",
    REPO.parent / "zimmerman-formula 2/sparc_data/UGC08286_rotmod.dat",
]
local = [digest(p) for p in local_paths]
remote_rotmod_hash = digest(HERE / "UGC08286_rotmod.dat")["sha256"]
projected_integral = 2 * math.pi * 1e6 * sum(
    (d[i + 1][0] - d[i][0]) *
    (d[i][0] * d[i][1] + d[i + 1][0] * d[i + 1][1]) / 2
    for i in range(len(d) - 1)
)
mu_zero = [ss[1] + 2.5 * math.log10(dd[1]) for ss, dd in zip(s, d)]
height = 0.196 * 1.05 ** 0.633
checks = {
    "all_17_rotation_points": len(r) == 17,
    "all_65_photometry_points": len(d) == len(s) == 65,
    "remote_rotmod_equals_three_local_copies": all(x["sha256"] == remote_rotmod_hash for x in local),
    "remote_table1_equals_local": (HERE / "SPARC_Lelli2016c.mrt").read_bytes() ==
                                  (REPO / "real_research/data/SPARC_Lelli2016c.mrt").read_bytes(),
    "published_table2_equals_rotmod_numeric": len(table2) == len(r) and all(
        tt[0] == 6.5 and tt[1:] == rr for tt, rr in zip(table2, r)),
    "no_bulge": all(rr[5] == rr[7] == 0 for rr in r),
    "first_three_gas_forces_outward": [rr[3] < 0 for rr in r] == [True] * 3 + [False] * 14,
    "same_projected_sfb_dens_grid": all(abs(ss[0] / 206264.80624709636 * 6500 - dd[0]) < 1e-5
                                        for ss, dd in zip(s, d)),
    "sfb_dens_photometric_conversion": max(mu_zero) - min(mu_zero) < 1e-5,
}
summary = {
    "checks": checks,
    "rotmod_columns": ["R_kpc", "Vobs_km_s", "errV_km_s", "Vgas_signed_km_s",
                       "Vdisk_at_ML1_km_s", "Vbul_at_ML1_km_s", "SBdisk_corrected_Lsun_pc2", "SBbul_Lsun_pc2"],
    "local_rotation_copies": local,
    "source_script_hashes": [digest(REPO / f) for f in [
        "campaign_fresh_gravity/CFG4_common.py",
        "argon_push/AG4g_galaxy_pull_census/ag4g.py",
        "argon_push/AG4h_pull_systematics/ag4h.py"]],
    "R_kpc_range": [r[0][0], r[-1][0]],
    "photometry_R_kpc_range": [d[0][0], d[-1][0]],
    "exponential_vertical_height_kpc_from_published_rule": height,
    "sfb_to_dens_mu_zero_min_max": [min(mu_zero), max(mu_zero)],
    "projected_2pi_R_Sigma_trapezoid_Lsun": projected_integral,
    "total_L_over_projected_integral_diagnostic_only_not_deprojection": 1.255e9 / projected_integral,
    "gas_signed_v_squared_km2_s2": [rr[3] * abs(rr[3]) for rr in r],
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(summary, indent=2, allow_nan=False))
raise SystemExit(0 if all(checks.values()) else 1)
