#!/usr/bin/env python3
"""WLJ2 (FROZEN_CRITERIA.md, c3bc2d3871), reported only, never a label: where in mass the exact junction's extra matter power at z = 0
comes from. For REF's layout and each case, the per-halo-mass contribution to the power change at k 1 and 3 h/Mpc (HLF1's A.2 per-grid-
point formula, as wlj2_hm.py's f_res uses it), with each mass's t, s, R_set / r_ta and the enclosed cold mass of the law and of the
reference at R_set. Written after wlj2_hm.py's z 0 to 1 ratio lines were seen (Ec3's R_cold at k 3 above ADOPT's at z 0, below it at
z 0.5), to check that number before any gate is read. Imports wlj2_hm.py's layout functions by executing it up to its KA section.
  OMP_NUM_THREADS=1 nice -n 19 python3 -I -B wlj2_diag.py -> wlj2_diag.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, io, contextlib
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "wlj2_hm.py"); code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ KA-V")
NS = {"__file__": SRC, "__name__": "wlj2_hm_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), NS)
L, F, KK, MM, RHO_M, setz, ratios_case, lay_case, layout, Bar, CUR = (NS[k] for k in ("L", "F", "KK", "MM", "RHO_M", "setz", "ratios_case", "lay_case", "layout", "Bar", "CUR"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = dict(lane="WLJ2", part="diagnostic (reported)", criteria="c3bc2d3871", rows={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
CS = ["ADOPT", "S2", "Ec3", "Ec2", "E0.5", "E0.75", "E1", "E2"]
EDGES = [8, 10, 11, 12, 12.5, 13, 13.5, 14, 16]
for ft in ("canonical", "alt"):
    for z in (0.0, 0.5):
        setz(z); W_M, BIAS, NORM_TA, PL = (L[k] for k in ("W_M", "BIAS", "NORM_TA", "PL")); lM = np.log10(MM)
        for cs in CS:
            r = ratios_case(ft, z, cs, keepU=True); row = {}
            for kk in (1.0, 3.0):
                j = int(np.argmin(abs(KK - kk)))
                d1 = W_M * ((r["US"][:, j] / RHO_M) ** 2 - (r["UR"][:, j] / RHO_M) ** 2)
                d2 = PL[j] * (r["IS"][j] + r["IR"][j]) * W_M * BIAS * (r["US"][:, j] - r["UR"][:, j]) / RHO_M / NORM_TA
                d = d1 + d2; tot = float(d.sum())
                row[str(kk)] = dict(total=tot, by_logM={f"{a}-{b}": float(d[(lM >= a) & (lM < b)].sum() / tot) if tot else None for a, b in zip(EDGES[:-1], EDGES[1:])})
            RES["rows"][f"{cs}|{ft}|{z}"] = row
            P(f"[{ft}] z {z} {cs:6s} k 3 total {row['3.0']['total']:+.3e}; share by log10 M (Msun/h): " + " ".join(f"{k}:{v:+.2f}" for k, v in row["3.0"]["by_logM"].items()))
        # per-halo junction numbers for the slow haloes in 12.5-14 (where the shares sit), Ec3 vs Ec2 vs ADOPT
        for cs in ("Ec3", "Ec2", "E1"):
            fn = lay_case(ft, z, cs, {}); rows = []
            for hb, m in zip(L["HB"], MM):
                if not (12.0 <= np.log10(m) < 14.0): continue
                r_, M_, inf = fn(hb)
                if inf.get("kind") != "E": continue
                i = inf["i_set"]; CUR[0] = inf["R_set"]; rB, MB, _ = layout(hb, ft, mode="B"); rR, MR, _ = layout(hb, ft, mode="Rb"); CUR[0] = 0.0; bar = Bar(hb, ft, rB)
                rows.append(dict(logM=float(np.log10(m)), R_set_over_rta=float(inf["R_set"] / hb["rta"]), t=inf["t"], s=inf["s"], CB_over_Ctot=float((MB[i] - bar[i]) / (MR[-1] - bar[-1])), CR_over_Ctot=float((MR[i] - bar[i]) / (MR[-1] - bar[-1]))))
            RES["rows"][f"junction|{cs}|{ft}|{z}"] = rows
            sel = rows[::max(1, len(rows) // 6)]
            P(f"   [{ft}] z {z} {cs}: log M, R_set/r_ta, t, C_B/C_tot, C_R/C_tot at R_set: " + "; ".join(f"{x['logM']:.2f} {x['R_set_over_rta']:.3f} {x['t']:.2f} {x['CB_over_Ctot']:.2f} {x['CR_over_Ctot']:.2f}" for x in sel))
json.dump(RES, open(os.path.join(HERE, "wlj2_diag.json"), "w"), indent=1)
open(os.path.join(HERE, "wlj2_diag.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
