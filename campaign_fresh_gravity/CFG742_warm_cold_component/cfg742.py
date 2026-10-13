"""CFG742: can a warm cold component be the two-sector selector? Criteria: FROZEN_CRITERIA.md.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg742.py      (CFG742_MUTATE=1: sigma_C = 5 km/s; exit 1 iff lambda_J < 2 Mpc)
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import CFG4_common as C4  # noqa: E402
MUT = os.environ.get("CFG742_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, C, MPC = 6.6743e-11, 2.99792458e8, 3.0856775814913673e22
SIG = [5.0] if MUT else [250.0, 400.0, 700.0]
lines, res, viable = [__doc__.strip()], {}, False
for f in C4.FOOTS:
    rho_L = (C4.A0[f] / (0.5 * C)) ** 2 / G
    rho_m0 = 0.309 / 0.686 * rho_L
    lines.append(f"\n{f}: rho_Lambda {rho_L:.3e}, rho_m(0) {rho_m0:.3e} kg/m^3")
    res[f] = {}
    for s in SIG:
        for z in (0.0, 0.5):
            lam = s * 1e3 * math.sqrt(math.pi / (G * rho_m0 * (1 + z) ** 3)) * (1 + z) / MPC
            res[f][f"{s:g}|{z}"] = lam
            viable |= lam <= 2.0
            lines.append(f"    sigma_C {s:5.0f} km/s, z {z}: comoving lambda_J = {lam:7.2f} Mpc")
fac = (0.049 / 0.309) ** 2
lines.append(f"\nlinear shear power factor if only baryons cluster (k >> k_J): (Omega_b/Omega_m)^2 = {fac:.4f} (amplitude x{math.sqrt(fac):.3f})")
if MUT:
    lines.append(f"MUTATE: lambda_J < 2 Mpc at sigma 5 km/s: {viable}"); rc = 1 if viable else 0
else:
    res["verdict"] = "VIABLE" if viable else "CLOSED"; lines.append(f"\nVERDICT: {res['verdict']}"); rc = 0
    json.dump(res, open(os.path.join(HERE, "cfg742_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg742{TAG}.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines)); sys.exit(rc)
