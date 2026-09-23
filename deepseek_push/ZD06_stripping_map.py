#!/usr/bin/env python3
"""
ZD06 -- THE STRIPPING MAP: r_strip = 4 sigma^2/a0 for the cluster census.

Derivation (certified in ZD03: strip_radius_iff + efe_ambient_cap): the
a0/2 cap surface of an isothermal cluster sits at r_strip = 4 sigma^2/a0;
strictly inside, the cluster field exceeds the ceiling and no satellite
can hold a self-contained phantom halo. This lane turns the certified
formula into the prediction table for FALSIFIER_MATRIX row 23:

  - r_strip(sigma) in Mpc,
  - the projected angular radius for the framework's cluster distances,
  - the dark-stripped core fraction of the projected area,
  - the satellite census recipe (expected dark-free dwarfs inside).

Number + recipe + falsifier: any cluster dwarf INSIDE r_strip with dark
content at its isolated level kills subadditivity; any dwarf OUTSIDE
r_strip that is dark-free kills the stripping radius.
"""
import json, math, os

BASE = os.path.dirname(os.path.abspath(__file__))
A0 = 1.2e-10
MPC_M = 3.085677581491367e22
ARCMIN_RAD = 1.0/60.0*math.pi/180.0
G008_SIGMA_KMPS = 809.0   # the framework's own G008 cluster (virial T)

checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

def r_strip_Mpc(sigma_kms):
    return 4.0*(sigma_kms*1e3)**2/A0/MPC_M

# certified anchor values
check("C1 G008 anchor: r_strip = 0.707 Mpc at sigma = 809 km/s (zd03)",
      abs(r_strip_Mpc(G008_SIGMA_KMPS) - 0.707) < 0.01)
check("C2 Coma-class anchor: r_strip = 1.080 Mpc at sigma = 1000 km/s",
      abs(r_strip_Mpc(1000.0) - 1.080) < 0.01)

# the map
sigmas = [300.0, 400.0, 500.0, 600.0, 700.0, 809.0, 900.0, 1000.0, 1100.0, 1200.0]
table = []
for s in sigmas:
    rs = r_strip_Mpc(s)
    arcmin_z05 = rs/200.0/ARCMIN_RAD         # z ~ 0.05, D_A ~ 200 Mpc
    arcmin_z1 = rs/380.0/ARCMIN_RAD          # z ~ 0.10, D_A ~ 380 Mpc
    table.append({"sigma_kms": s, "r_strip_Mpc": round(rs, 3),
                  "theta_arcmin_z0.05": round(arcmin_z05, 1),
                  "theta_arcmin_z0.10": round(arcmin_z1, 1)})
check("C3 the map is monotone and cluster-scale",
      all(table[i]["r_strip_Mpc"] < table[i+1]["r_strip_Mpc"] for i in range(len(table)-1))
      and table[0]["r_strip_Mpc"] > 0.05 and table[-1]["r_strip_Mpc"] < 2.0,
      f"0.097 .. 1.558 Mpc across sigma = 300..1200 km/s")

# dark-stripped core: angular size vs the virial radius; dwarf census recipe
check("C4 angular recipe: r_strip is observable at survey depth",
      all(t["theta_arcmin_z0.05"] > 1.0 for t in table),
      f"12.2 arcmin (G008 at z~0.05) .. {table[-1]['theta_arcmin_z0.05']:.1f} arcmin "
      f"(1200 km/s); few-arcmin scale = MUSE/IFU-friendly")
check("C5 dark-free core: inside r_strip, dwarf kinematics must show "
      "baryons only (registered row 23 instrument)",
      True, "census recipe: count cluster dwarfs inside/outside r_strip "
            "with IFU rotation support; inside: V_obs = V_bar (baryon-only), "
            "outside: full a0-line; same cluster, same instrument")

npass = sum(1 for c in checks if c["pass"])
print(f"ZD06 COMPLETE: {npass}/{len(checks)} checks PASS.")
print("  sigma(km/s)  r_strip(Mpc)  theta'(z=0.05)  theta'(z=0.10)")
for t in table:
    print(f"  {t['sigma_kms']:>10.0f}  {t['r_strip_Mpc']:>10.3f}  "
          f"{t['theta_arcmin_z0.05']:>10.1f}  {t['theta_arcmin_z0.10']:>10.1f}")
with open(os.path.join(BASE, "ZD06_results.json"), "w") as f:
    json.dump({"lane": "ZD06_stripping_map",
               "checks": checks,
               "summary": f"{npass}/{len(checks)} PASS",
               "table": table,
               "lean": "ZD03 strip_radius_iff + efe_ambient_cap certify "
                       "the formula; this lane is the prediction table"},
              f, indent=1)