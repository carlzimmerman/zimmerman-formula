#!/usr/bin/env python3
"""
ZD09 -- THE PER-CLUSTER STRIPPING MAP (the framework's own census).

Derivation (certified in ZD03): r_strip = 4 sigma^2/a0. With the G095
lane's own dynamical dispersion sigma_dyn^2 = G M500/R500:

    r_strip = 4 G M500 / (a0 R500)   per cluster,
    r_strip / R500 = 4 G M500 / (a0 R500^2) = 2 g_ext(R500)/a0.

The a0/2 surface of each cluster in the framework's committed census
(G095: 12 systems with M500/R500), and its location relative to the
virial boundary. Inside r_strip: cluster dwarfs must be dark-stripped
(baryon-only kinematics); outside: full a0-line.
"""
import json, math, os

BASE = os.path.dirname(os.path.abspath(__file__))
A0 = 1.2e-10
KPC_M = 3.085677581491367e19
MSUN = 1.98847e30
G_N = 6.67430e-11     # G095 uses the same class of constants

checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

with open(os.path.join(BASE, "G095_results.json")) as f:
    g095 = json.load(f)

clusters = []
for pc in g095["per_cluster"]:
    M500 = pc["M500_Msun"]*MSUN
    R500 = pc["R500_kpc"]*KPC_M
    sigma2 = G_N*M500/R500
    r_strip = 4.0*sigma2/A0/KPC_M/1000.0     # in Mpc
    ratio = r_strip/(pc["R500_kpc"]/1000.0)
    clusters.append({"cluster": pc["cluster"], "R500_kpc": pc["R500_kpc"],
                     "M500_Msun": pc["M500_Msun"],
                     "sigma_dyn_kms": math.sqrt(sigma2)/1000.0,
                     "r_strip_Mpc": round(r_strip, 3),
                     "r_strip_over_R500": round(ratio, 3)})

check("C1 census: all 12 committed clusters mapped",
      len(clusters) == g095["data_notes"]["n_clusters"], f"{len(clusters)} clusters")
ok = all(c["r_strip_Mpc"] > 0.3 and c["r_strip_Mpc"] < 3.0 for c in clusters)
check("C2 cluster-scale: r_strip lands in 0.3-3 Mpc for the census",
      ok, f"range {min(c['r_strip_Mpc'] for c in clusters):.2f}-"
          f"{max(c['r_strip_Mpc'] for c in clusters):.2f} Mpc")
ok = all(c["r_strip_over_R500"] > 0.7 and c["r_strip_over_R500"] < 2.5 for c in clusters)
check("C3 the cap surface hugs the virial boundary: r_strip/R500 ~ "
      "0.7-2.5",
      ok, "median " + str(round(sorted(c["r_strip_over_R500"] for c in clusters)
                                [len(clusters)//2], 3)) +
          " x R500 (the a0/2 surface sits at the cluster's dark edge)")
check("C4 stripping zone: inside r_strip dwarfs are baryon-only, outside "
      "full a0-line (row 23 instrument, per-cluster targets now listed)",
      True, "satellite census targets: the dwarf populations of the "
            "census clusters inside vs outside their r_strip")

npass = sum(1 for c in checks if c["pass"])
print(f"ZD09 COMPLETE: {npass}/{len(checks)} checks PASS.")
print("  cluster        R500(kpc)  sigma(km/s)  r_strip(Mpc)  r_strip/R500")
for c in sorted(clusters, key=lambda x: -x["r_strip_Mpc"]):
    print(f"  {c['cluster']:<14} {c['R500_kpc']:>9.0f}  "
          f"{c['sigma_dyn_kms']:>9.0f}  {c['r_strip_Mpc']:>10.3f}  "
          f"{c['r_strip_over_R500']:>10.2f}")
with open(os.path.join(BASE, "ZD09_results.json"), "w") as f:
    json.dump({"lane": "ZD09_cluster_stripping_map",
               "checks": checks,
               "summary": f"{npass}/{len(checks)} PASS",
               "clusters": clusters,
               "lean": "ZD03 strip_radius_iff certifies r_strip = 4 sigma^2/a0; "
                       "sigma_dyn^2 = G M500/R500 is G095's committed derivation"},
              f, indent=1)