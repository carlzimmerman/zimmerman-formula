"""CFG762: is there ONE c_P that lets P radiation export infall energy in every SPARC galaxy?

Criteria: FROZEN_CRITERIA.md (committed alone, ba35a0aae). Raw SPARC (CFG4_common via CFG760's CFG691_copy), last measured radius.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg762.py      (CFG762_MUTATE=1: no vacuum curvature; exit 1 iff D1 then opens)
"""
import os, sys, json, math

import numpy as np
from scipy.integrate import solve_bvp

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
sys.path.insert(0, os.path.join(LANES, "CFG760_p_wave_gap"))
import CFG4_common as C4  # noqa: E402  (read only)
import CFG691_copy as SP  # noqa: E402  (CFG691's SPARC loader, checked by CFG760 K5)

MUT = os.environ.get("CFG762_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg762{TAG}.out"), "w")
RES = {"lane": "CFG762", "criteria": "ba35a0aae", "mutate": MUT, "numbers": {}}
G, PC, GYR = 6.6743e-11, 3.0856775814913673e16, 3.15576e16
LSTAR, XE = 5.754 * PC, 0.71
UBEST = {"canonical": 0.46, "alt": 0.42}


def P_(s=""):
    print(s, flush=True)
    OUT.write(s + "\n")


P_(__doc__.strip())


def f(t, y):
    s = np.exp(t)
    return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) - 1.0])


tt = np.linspace(math.log(1e-4), math.log(1e4), 4001)
ss = np.exp(tt)
SOL = solve_bvp(f, lambda ya, yb: np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1e-4 - 1e-8)]), tt,
                np.vstack([1 / (ss + 2), -ss / (ss + 2) ** 2]), tol=1e-8, max_nodes=200000)


def v0(s):
    if s < 1e-4:
        return 0.5 * s
    if s > 1e4:
        return 1.0 - 1.0 / s
    return s * float(SOL.sol(math.log(s))[0])


def omega_gap(s0):
    return math.sqrt((0.0 if MUT else 2.0 * abs(v0(s0)) / s0) + 2.0 / s0 ** 2)


verdict = {}
for fo in C4.FOOTS:
    a0 = C4.A0[fo]
    iu = int(np.argmin(abs(SP.UPS - UBEST[fo])))
    rows, excl = [], 0
    for gi in range(SP.NG):
        j = SP.last[gi]
        R = SP.Rm[j]
        vb2 = SP.VB2[j, iu] * 1e6
        if vb2 <= 0 or SP.Vo[j] <= 0:
            excl += 1
            continue
        Mb = vb2 * R / G
        y = (G * Mb / R ** 2) / a0
        if y > 1:
            excl += 1
            continue
        rM = math.sqrt(G * Mb / a0)
        ell = LSTAR ** 2 / (2 * rM)
        s0 = R / ell
        V = 2 * SP.Vo[j] * 1e3
        wg = omega_gap(s0)
        cmax = V / (XE * wg * s0) if not MUT else math.inf
        cmin = R / (13.8 * GYR)
        rows.append(dict(gi=gi, R_kpc=R / PC / 1e3, y=y, s0=s0, cP_max=cmax, cP_min=cmin, own_window=bool(cmax >= cmin)))
    cmin_max = max(r["cP_min"] for r in rows)
    cmax_min = min(r["cP_max"] for r in rows)
    own = sum(r["own_window"] for r in rows)
    op = cmin_max <= cmax_min
    verdict[fo] = "OPEN" if op else "CLOSED"
    RES["numbers"][fo] = dict(n_included=len(rows), n_excluded=excl, max_cP_min=cmin_max, min_cP_max=cmax_min,
                              gap_factor=(cmin_max / cmax_min if cmax_min > 0 and math.isfinite(cmax_min) else None),
                              n_own_window=own, rows=rows)
    P_(f"\n{fo}: {len(rows)} galaxies included (y <= 1), {excl} excluded;  max c_P,min = {cmin_max:.3e} m/s, "
       f"min c_P,max = {cmax_min:.3e} m/s" + (f" (gap x{cmin_max / cmax_min:.0f})" if math.isfinite(cmax_min) else "")
       + f";  galaxies with a non-empty own window: {own}/{len(rows)}  ->  D1 {verdict[fo]}")
    cm = np.array([r["cP_max"] for r in rows]); cn = np.array([r["cP_min"] for r in rows])
    if not MUT:
        P_(f"    c_P,max range {cm.min():.3e}-{cm.max():.3e} m/s;  c_P,min range {cn.min():.3e}-{cn.max():.3e} m/s")
d1 = "OPEN" if all(v == "OPEN" for v in verdict.values()) else "CLOSED"
RES["verdict"] = dict(D1=d1, per_footing=verdict)
P_(f"\nVERDICT: D1 {d1}")
json.dump(RES, open(os.path.join(HERE, f"cfg762_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(1 if (MUT and d1 == "OPEN") else 0)
