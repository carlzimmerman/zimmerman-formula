#!/usr/bin/env python3
"""QX10 iter_2 KA4b (POST-RESULT, reported only): the frozen KA4 measured M_d(<R_ref), but at z_s the whole static core
sits inside R_ref, so KA4 was vacuous. KA4b measures the half-mass and 90 %-mass radii over the same 5 sound-crossing
times with K frozen at K(z_s), 400 shells, C1, both footings, reference galaxy and X-COP median cluster.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
argv0 = sys.argv; sys.argv = [argv0[0]]
import qx10_i2 as S, qx10_i2_hydro as H
sys.argv = argv0
out = {}; lines = []
clus = sorted(S.clusters.items(), key=lambda kv: kv[1][0]["Mb_last"][0]); cname, cpts = clus[len(clus) // 2]
Ml, rl = cpts[0]["Mb_last"]; chost = S.profile_from([q["r_kpc"] for q in cpts], [q["M_b"] for q in cpts], Ml, rl)
HOSTS = {"reference": (S.expdisc(1e10, 10.0), 1e10), f"X-COP {cname}": (chost, Ml)}
l0, p = S.CELLS["C1"]; l0k = l0 * 1e3; a_s = brentq(lambda a: H.lamJ(a, l0k, p) / 2 - 10.0, 0.05, 1.0)
def radii(r, m):
    f = m / m[-1]; return float(np.interp(0.5, f, r)), float(np.interp(0.9, f, r))
for fo, a0k in S.A0K.items():
    for hn, (hfn, Mbt) in HOSTS.items():
        Mt = S.FCAP * S.R * Mbt; Kz = H.K_t(a_s, l0k, p)
        st0 = S.solve_static(hfn, Mt, Kz, S.r_ta(Mbt), a0k, n=4000)
        tsc = st0["Rs"] / math.sqrt(2 * Kz * float(st0["rho"][0]))
        r0, dm = H.shells_from_static(st0, 400); m0 = dm * np.arange(401)
        res = H.run(hfn, st0, 400, l0k, p, a0k, a_s, freeze_K=Kz, t_span=5 * tsc)
        a = radii(r0, m0); b = radii(res["r"], res["m_in"]) if res["ok"] else (float("nan"),) * 2
        row = dict(R_s_static=st0["Rs"], r50_start=a[0], r90_start=a[1], r50_end=b[0], r90_end=b[1],
                   rel50=b[0] / a[0] - 1, rel90=b[1] / a[1] - 1, steps=res.get("steps"))
        out[f"{fo} {hn}"] = row
        lines.append(f"KA4b {fo} {hn}: R_s(z_s) {st0['Rs']:.2f} kpc; r50 {a[0]:.3f} -> {b[0]:.3f} ({row['rel50']:+.2%}); r90 {a[1]:.3f} -> {b[1]:.3f} ({row['rel90']:+.2%}); {row['steps']} steps")
        print(lines[-1], flush=True)
json.dump(dict(KA4b=out, note="POST-RESULT, reported only; kappa = 1/2 FITTED; not theory closed"), open(os.path.join(HERE, "qx10_i2_ka4b.json"), "w"), indent=1)
open(os.path.join(HERE, "qx10_i2_ka4b.out"), "w").write("\n".join(lines) + "\n")
