#!/usr/bin/env python3
"""CL5 Part B, reported only: LS1's Upsilon and dV by V_flat at the stipulated eta 21.2/14.3/14.3. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os
S = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "LS1_lstar_analogs", "ls1_analogs.py")).read()
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec"))
def Mh(q): b = BGS[TAG]; return 10 ** (b["a"] + b["b"] * (q["lMb"] - 10))
def halo_eta(q, f):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = Mh(q); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
    eta = float(np.interp(math.log10(M), [12, 13, 14], [21.2, 14.3, 14.3])); s = max(SIG[f], eta * sigma_coll(TAG, M)[0] * MSUNE / PC2); r0 = solve_r0(M * MSUNE, R200, s)
    return GE * math.pi * s * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
R = {}
for f in ("canonical", "alt"):
    R[f] = {}
    for lo, hi in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)):
        U, D = [], []
        for q in sel(lo, hi):
            gh = halo_eta(q, f); _, _, iu = fit_one(q, np.log10(np.maximum(q["GB"] + gh[:, None], 1e-300))); U.append(UPS[iu]); d = dv(q, gh)
            if d is not None: D.append(d)
        R[f][f"{lo}-{hi}"] = (len(U), round(float(np.median(U)), 2), round(float(np.median(D)), 1)); P(f"[{f}] V_flat {lo}-{hi}: n {len(U)}, median U {R[f][f'{lo}-{hi}'][1]}, dV {R[f][f'{lo}-{hi}'][2]}")
json.dump(R, open(os.path.join(HERE, "cl5_bins.json"), "w"), indent=1); open(os.path.join(HERE, "cl5_bins.out"), "w").write("\n".join(OUT) + "\n")
