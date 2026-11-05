#!/usr/bin/env python3
"""CC1 parts A and B: threshold on the record's eta(M) tables; direction of the velocity-rms correction."""
import json
import numpy as np
lm = np.array([11, 12, 13, 14, 15.]); S = np.array([3.83, 6.84, 11.95, 20.48, 34.71]); F = {"canonical": 106.85, "alt": 129.13}; RES = {}
def mc(s): return round(float(np.interp(np.log10(s), np.log10(S), lm)), 2) if s >= S[0] else "<11"
RES["constant"] = {str(e): {f: mc(v / e) for f, v in F.items()} for e in (10.82, 12.10, 14.30)}
T = {"X73 c_f 4": (10.82, 10.82, 10.82), "X77": (20.83, 13.79, 14.39), "CE1 converged": (25.94, 17.67, 16.91), "SH1 R 0.685": (17.77, 12.10, 11.59), "CL5 stipulated": (21.2, 14.3, 14.3)}
x = np.linspace(11, 14, 3001); RES["mass_dependent"] = {}
for n, e in T.items():
    c = np.interp(x, [12, 13, 14], e) * 10 ** np.interp(x, lm, np.log10(S)); o = dict(eta_S_1e12=round(e[0] * S[1], 1))
    for f, v in F.items():
        i = np.argmax(c >= v); o[f] = round(float(x[i]), 2); o[f + "_1e12_supercritical"] = bool(e[0] * S[1] >= v)
    RES["mass_dependent"][n] = o; print(n, o)
RES["constant_note"] = "constant-eta extrapolation below 1e12 clamped at table eta(1e12) above"
print(RES["constant"])
RES["bracket"] = "FAILS" if any(RES["mass_dependent"][n]["canonical_1e12_supercritical"] for n in ("SH1 R 0.685", "CL5 stipulated")) else "HOLDS"; print("BRACKET", RES["bracket"])
rng = np.random.default_rng(1030); N = 2000000; st = 150.; vt = rng.normal(0, st, N); r_m = .756; am = r_m * 264 / st
def Ahat(alpha, rms):
    vr = alpha * vt; n2 = rms ** 2 - alpha ** 2 * st ** 2; assert n2 >= 0; vr = vr + rng.normal(0, np.sqrt(n2), N); return float(np.sum(vt * vr) / np.sum(vr * vr))
m = Ahat(am, 264.)
def fac(q): return m / Ahat(am * q, 194.)
# correction to A = (alpha_m/alpha_d)(sigma_d/sigma_m)^2; q = alpha_d/alpha_m, q <= 0.972 since alpha_d st <= 194
RES["tier2"] = {f"q={q}": dict(mc=round(fac(q), 3), closed=round((194 / 264) ** 2 / q, 3), r_data=round(q * am * st / 194, 3)) for q in (.97, 194 / 264, .54, 396 / 1000)}; RES["tier2"]["spec_factor"] = round(264 / 194, 3); RES["tier2"]["q_for_spec_factor"] = round((194 / 264) ** 3, 3); RES["tier2"]["r_data_for_spec_factor"] = round((194 / 264) ** 3 * am * st / 194, 3)
print("true correction to A: ", RES["tier2"]); json.dump(RES, open("cc1_parts.json", "w"), indent=1)
