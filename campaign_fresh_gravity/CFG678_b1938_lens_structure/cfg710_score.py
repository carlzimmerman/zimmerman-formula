#!/usr/bin/env python3
"""CFG710 scorer: applies the frozen rules (criteria ef9d750d0) to measured lens-structure numbers.
Usage: python3 cfg710_score.py <slope> <slope_sigma|nan> <q_M> <PA_M_deg> <m3_strength> <m4_strength> <label> [sigma_q] [sigma_PA]
PA convention: PyAutoLens angle from ell_comps (same convention as the sealed light PA). kappa = 1/2 FITTED; not theory closed."""
import sys, json, math, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "cfg710_predictions.json")))
assert hashlib.sha256(open(os.path.join(HERE, "cfg710_predictions.json"), "rb").read()).hexdigest() == \
    "ef0a780b56fa57c651908c16070f49b1832f794b5a08071fb00e73f99a664559", "sealed predictions changed!"
g, sg, qM, paM, m3, m4, label = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), sys.argv[7]
sq = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0; spa = float(sys.argv[9]) if len(sys.argv) > 9 else 0.0
out = {"label": label, "measured": dict(slope=g, slope_sigma=sg, q_M=qM, PA_M=paM, m3=m3, m4=m4)}
for foot in ("canonical", "alt"):
    gp = P["P1"][f"{foot}_V1_compact"]["gamma_eff_at_thetaE"]
    tol = max(2 * sg, 0.10) if math.isfinite(sg) else 0.10
    d = abs(g - gp)
    edge = g <= 1.501 or g >= 2.999
    v1 = "NOT DIAGNOSTIC (prior edge)" if edge else ("CONSISTENT" if d <= tol else ("TENSION" if d <= 0.25 else "INCONSISTENT"))
    out[f"P1_{foot}"] = dict(predicted=gp, measured=g, diff=d, tol=tol, verdict=v1)
pa_L, q_L = P["P2"]["light_PA_deg"], P["P2"]["light_q"]
dpa = abs(((paM - pa_L) + 90) % 180 - 90)
ok_pa = dpa <= 10 + 2 * spa; ok_q = (q_L - 2 * sq) <= qM <= (q_L + 0.1 + 2 * sq)          # frozen windows, widened only by 2 sigma
out["P2"] = dict(dPA_deg=dpa, PA_ok=ok_pa, q_ok=ok_q, q_range=[q_L, q_L + 0.1], sigma_q=sq, sigma_PA=spa,
                 verdict=("NOT DIAGNOSTIC (q_L > 0.9)" if q_L > 0.9 else ("CONSISTENT" if (ok_pa and ok_q) else "INCONSISTENT")))
out["P3"] = dict(verdict="CONSISTENT" if (m3 <= 0.02 and m4 <= 0.02) else "INCONSISTENT")
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, f"cfg710_score_{label}.json"), "w"), indent=1)
