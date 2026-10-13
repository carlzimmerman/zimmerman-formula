#!/usr/bin/env python3
"""CFG676: a0-siren consistency relation (criteria 692981e55). a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE,0).
DESI DR2 w0wa read from arXiv 2503.14738 TeX (eqs w0wa_DESI_CMB_P+/U3/DY5; Omega_m from its table).
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math, hashlib
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG676_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
DESI = {"DESI+CMB+Pantheon+": (-0.838, -0.62, 0.298), "DESI+CMB+Union3": (-0.667, -1.09, 0.328),
        "DESI+CMB+DESY5": (-0.752, -0.86, 0.319)}
if MUT: DESI = {k: (-1.0, 0.0, v[2]) for k, v in DESI.items()}
ZS = [0.5, 1.0, 2.0, 3.0]
lnrho = lambda z, w0, wa: 3 * (1 + w0 + wa) * math.log(1 + z) - 3 * wa * z / (1 + z)
out = {"lane": "CFG676", "criteria": "692981e55", "mutate": MUT, "relation": "a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE,0)", "rows": {}}
L = []
for k, (w0, wa, om) in DESI.items():
    row = {}
    for z in ZS:
        dtrack = 0.5 * lnrho(z, w0, wa) / math.log(10)
        Hz = math.sqrt(om * (1 + z) ** 3 + (1 - om) * math.exp(lnrho(z, w0, wa)))
        # siren precision: sigma[ln rho] = sqrt((3 ln(1+z) s|w0|)^2 + (3 (ln(1+z) - z/(1+z)) s|wa|)^2); 2 sigma = |ln rho|
        a1, a2 = 3 * math.log(1 + z) * abs(w0), 3 * (math.log(1 + z) - z / (1 + z)) * abs(wa)
        s_req = abs(lnrho(z, w0, wa)) / 2 / math.hypot(a1, a2) if lnrho(z, w0, wa) != 0 else 0.0
        row[f"z={z}"] = {"dlog10_a0_tracking": dtrack, "dlog10_a0_H_rival": math.log10(Hz), "dlog10_a0_flat": 0.0,
                         "siren_frac_precision_for_2sigma": s_req,
                         "implied_sigma_w0": s_req * abs(w0), "implied_sigma_wa": s_req * abs(wa)}
        L.append(f"{k} z={z}: tracking {dtrack:+.4f} dex | a0~H {math.log10(Hz):+.3f} | flat 0 ; 2sigma needs sigma(w0) <= {s_req*abs(w0):.3f}, sigma(wa) <= {s_req*abs(wa):.3f}")
    out["rows"][k] = row
if MUT:
    bite = all(abs(v["dlog10_a0_tracking"]) < 1e-12 for r in out["rows"].values() for v in r.values())
    L.append(f"MUTATE w0=-1, wa=0: {'BITES' if bite else 'DOES NOT BITE'}")
js = json.dumps(out, indent=1, sort_keys=True) + "\n"
open(os.path.join(HERE, f"cfg676_predictions{TAG}.json"), "w").write(js)
L.append(f"sha256(cfg676_predictions{TAG}.json) = {hashlib.sha256(js.encode()).hexdigest()}")
open(os.path.join(HERE, f"cfg676{TAG}.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
if MUT: sys.exit(1 if bite else 0)
