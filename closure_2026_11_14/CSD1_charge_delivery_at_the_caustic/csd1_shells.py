#!/usr/bin/env python3
"""CSD1 (FROZEN_CRITERIA.md section 2): the charge the clock's own flow holds inside its moving caustics.
FLD1's fld1_shells.py (fable52_push/FLD1_fold_reach) is executed with stated text insertions only (XJ1's pattern; nothing on
disk is changed):
  1. XJ1's per-shell passage counter (reflections) and its three series columns R_1, R_2, R_3;
  2. (S-cos) an initial growing-mode Lagrangian overdensity delta_i = min(A M_b / M_X, 0.3): r_i -> r_i (1 - delta_i/3),
     v_i -> H r_i (new) (1 - delta_i/3); A = 0 leaves the code path exactly FLD1's;
  3. per output, a call to csd_extra() (below), which reads r, v, the shell charges dM, the crossed flags and the passage
     counts, and appends this lane's columns. It changes no state of the integration.
  python3 -I -B csd1_shells.py <footing> <logMb> [--grid scaled|a4] [--A 0] [--law on|off] [--N 2400] [--mutate lagr]
      -> runs/<name>.json
Limits: behind the fold FLD1's independent-shell equation is not exact (each shell keeps its Lagrangian enclosed charge)
and the central reflection is FLD1's device; the action gives no answer there (COL1). Adopts nothing.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "fable52_push", "FLD1_fold_reach", "fld1_shells.py"); code = open(SRC).read()

ap = argparse.ArgumentParser()
ap.add_argument("footing"); ap.add_argument("logMb", type=float)
ap.add_argument("--grid", default="scaled"); ap.add_argument("--A", type=float, default=0.0)
ap.add_argument("--law", default="on"); ap.add_argument("--N", type=int, default=2400)
ap.add_argument("--mutate", default="")          # 'lagr': TW3, count charge by Lagrangian radius X a(t)
ap.add_argument("--tag", default="")
a = ap.parse_args()

def ins(x, y):
    global code
    assert code.count(x) == 1, x
    code = code.replace(x, y)

# 1. XJ1's passage counter and columns (identical text to XJ1's xj1_shells.py), plus this lane's extra columns
ins("    crossed = np.zeros(N, bool)\n", "    crossed = np.zeros(N, bool)\n    nhit = np.zeros(N, int)\n")
ins("            rn[hit] = 2 * rw[hit] - rn[hit]; vh[hit] = np.abs(vh[hit])\n",
    "            rn[hit] = 2 * rw[hit] - rn[hit]; vh[hit] = np.abs(vh[hit]); nhit[hit] += 1\n")
ins("                       float(crossed.mean())])\n",
    "                       float(crossed.mean())] + [float(r[nhit >= k].max()) if (nhit >= k).any() else 0.0 for k in (1, 2, 3)]"
    " + CSD_EXTRA(t, cos, r, v, X, dM, crossed, nhit, nbar(t), Mb, a0, rf, rta))\n")
# 2. S-cos initial perturbation (hubble mode only)
ins("        r = X / (1 + zi) * (1 + r_perturb); v = cos.H_of_a(1 / (1 + zi)) * r\n",
    "        r = X / (1 + zi) * (1 + r_perturb); v = cos.H_of_a(1 / (1 + zi)) * r\n"
    "        if CSD_A > 0:\n"
    "            _d = np.minimum(CSD_A * Mb / MX, 0.3); r = r * (1 - _d / 3); v = cos.H_of_a(1 / (1 + zi)) * r * (1 - _d / 3)\n")

NS = {"__file__": SRC, "__name__": "fld1_shells_csd1"}
exec(compile(code, SRC, "exec"), NS)
L = NS["L"]; EPS = NS["EPS"]; G = L.G

def mph(R, Mb, a0):
    """FLD1's Mph (the law's phantom mass of the softened point baryon), the same expression."""
    gN = G * Mb * R / (R * R + EPS * EPS) ** 1.5
    return R * R * (L.law_g(gN, a0) - gN) / G

WS = (0.05, 0.10, 0.20)
ZSNAP = (0.0, 0.5, 1.0, 2.2, 3.0, 4.4)
SNAP = {}
GRID = np.logspace(-2, 1, 61)                    # r / R_fold for the stored profiles

def csd_extra(t, cos, r, v, X, dM, crossed, nhit, nbar, Mb, a0, rf, rta):
    z = 1 / cos.a_of_t(t) - 1
    rcount = X * cos.a_of_t(t) if a.mutate == "lagr" else r
    o = np.argsort(rcount); rs = rcount[o]; cum = np.cumsum(dM[o])
    cum_unc = np.cumsum((dM * ~crossed)[o])
    def Q(R):
        if R <= 0: return 0.0, 0.0
        i = np.searchsorted(rs, R, side="left")
        return (float(cum[i - 1]) if i > 0 else 0.0), (float(cum_unc[i - 1]) if i > 0 else 0.0)
    Rk = [float(r[nhit >= k].max()) if (nhit >= k).any() else 0.0 for k in (1, 2, 3)] + [0.5 * rf]
    out = []
    for R in Rk:
        if R <= 0:
            out += [0.0] * (5 + 3 * len(WS)); continue
        q, qu = Q(R)
        C = float(mph(R, Mb, a0)); Cp = float((mph(R * (1 + 1e-5), Mb, a0) - mph(R * (1 - 1e-5), Mb, a0)) / (2e-5 * R))
        Nin = Cp / (4 * math.pi * R * R)
        row = [q / C, (q - (4 * math.pi / 3) * nbar * R ** 3) / C, qu / C, C, Nin]
        for w in WS:
            m = (r >= R) & (r < (1 + w) * R); vol = (4 * math.pi / 3) * R ** 3 * ((1 + w) ** 3 - 1)
            mi = (r >= (1 - w) * R) & (r < R); voli = (4 * math.pi / 3) * R ** 3 * (1 - (1 - w) ** 3)
            Mo = float(dM[m].sum())
            row += [Mo / vol, float((dM[m] * v[m]).sum() / Mo) if Mo > 0 else float("nan"), float(dM[mi].sum()) / voli]
        out += row
    # equal-charge radius on the shell radii, r in [1 kpc, R_ta]
    sel = (rs >= 1.0) & (rs <= max(rta, 1.0))
    if sel.any():
        rr = rs[sel]; D = cum[sel] / mph(rr, Mb, a0)
        ge = np.where(D >= 1)[0]; lt = np.where(D < 1)[0]
        req = float(rr[ge].max()) if len(ge) else 0.0; rlt = float(rr[lt].min()) if len(lt) else 0.0
        dmax = float(D.max()); rdmax = float(rr[int(np.argmax(D))])
    else:
        req = rlt = dmax = rdmax = float("nan")
    out += [req, rlt, dmax, rdmax]
    out += [Q(R)[0] / float(mph(R, Mb, a0)) for R in (10.0, 30.0, 100.0, 300.0)]   # FLD1's fixed-radius reads, this lane's count
    for zs in ZSNAP:
        if zs not in SNAP and z <= zs and rf > 0:
            RG = GRID * rf; qq = np.array([Q(R)[0] for R in RG])
            SNAP[zs] = dict(z=float(z), R_fold=float(rf), r_over_Rfold=GRID.tolist(), D=(qq / mph(RG, Mb, a0)).tolist())
    return out

NS["CSD_EXTRA"] = csd_extra; NS["CSD_A"] = a.A
COLS = ["t_since_start_gyr", "z", "R_fold_kpc", "R_ta_kpc", "fraction_crossed", "R_1_kpc", "R_2_kpc", "R_3_kpc"]
for nm in ("k1", "k2", "k3", "half"):
    COLS += [f"D_{nm}", f"Dexc_{nm}", f"Dunc_{nm}", f"Claw_{nm}", f"Nin_{nm}"]
    for w in WS:
        COLS += [f"Nout_w{w:g}_{nm}", f"vout_w{w:g}_{nm}", f"Nflowin_w{w:g}_{nm}"]
COLS += ["R_eq_kpc", "R_first_short_kpc", "D_max_1kpc_to_Rta", "r_at_D_max_kpc"]
COLS += ["read_10", "read_30", "read_100", "read_300"]

res = NS["run"](a.footing, a.logMb, mode="hubble", law=a.law, N=a.N, grid=a.grid)
S = np.array(res["series"]); assert S.shape[1] == len(COLS), (S.shape, len(COLS))
name = a.tag or (f"csd1_{a.footing}_M{a.logMb:g}_N{a.N}" + ("" if a.grid == "scaled" else f"_{a.grid}")
                 + ("" if a.A == 0 else f"_A{a.A:g}") + ("" if a.law == "on" else "_lawoff") + (f"_MUT{a.mutate}" if a.mutate else ""))
out = dict(lane="CSD1", footing=a.footing, logMb=a.logMb, grid=a.grid, A=a.A, law=a.law, N=a.N, mutate=a.mutate,
           series_cols=COLS, series=res["series"], snapshots={f"{k:g}": v for k, v in SNAP.items()},
           reads_end=res["reads_end"], R_fold_end_kpc=res["R_fold_end_kpc"], R_ta_end_kpc=res["R_ta_end_kpc"],
           charge_turned_around_over_Mb=res["charge_turned_around_over_Mb"], steps=res["steps"], wall_s=res["wall_s"],
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "runs", name + ".json"), "w"))
print(f"{name}: R_fold(end) {res['R_fold_end_kpc']:.1f} kpc; turned around {res['charge_turned_around_over_Mb']:.3f} M_b; "
      f"steps {res['steps']}, {res['wall_s']:.0f} s")
