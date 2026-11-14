#!/usr/bin/env python3
"""BJ1 known answers on the profiles (FROZEN_CRITERIA.md, 9e7ce0dfe6, section 2, items i to vii) and the reported layout
items of section 3 (share of haloes per branch by mass and redshift, R_set / R_k, R_set / R_fold, the t-free check), on
FRZ1's halo grid (321 haloes), all 12 forest redshifts, both footings, cases B1, B2, B3. z = 0 is added as a reported row
(no known answer is graded there). Light; no boxes.
  (i)   C = C_B at every node r <= R_set, 1e-12 relative
  (ii)  C = C_R at every node r >= max(R_k, R_set), 1e-12 relative
  (iii) C(r_ta) = C_tot, 1e-12 relative
  (iv)  C non-decreasing (no tolerance: the smallest step is printed)
  (v)   under: C(R_k) = C_R(R_k); over: C(R_set) = C_R(R_set); 1e-9 of C_tot
  (vi)  R_k forced to r_ta gives mode B at every node (1e-12 relative); R_k forced to 0 gives the reference exactly
  (vii) haloes above v*(z) have the reference row exactly
  t-free: every node's C is bit-equal to C_B at that node, to Q_k = C_R(R_k), or to C_R at that node.
  nice -n 19 python3 -I -B bj1_ka_tables.py -> bj1_ka_tables.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bj1_lib as BL
INSTALL_DEV = BL.install()
X = BL.X; Z = X.rec(); F, L = Z["F"], Z["L"]; layout, CUR = Z["layout"], Z["CUR"]
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
KS = (1, 2, 3)
MBINS = [(8, 9), (9, 10), (10, 11), (11, 12), (12, 17)]
def rel(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return np.where(a == b, 0.0, np.abs(a - b) / np.maximum(np.abs(b), 1e-300))
def mmx(v): return [float(np.min(v)), float(np.median(v)), float(np.max(v))] if len(v) else None
RES = dict(lane="BJ1", criteria="9e7ce0dfe6", install_max_rel=INSTALL_DEV, KA={}, reported={}, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
P(f"BJ1 profile-level known answers and branch shares. XJ1 shell runs installed (first five columns against FLD1's loaded series: max rel {INSTALL_DEV:.1e}).")
okall = True
for ft in BL.FOOTS:
    for z in [0.0] + list(BL.ZB):
        Z["set_z"](z); vs = X.vstar(ft, z); HB = L["HB"]; graded = z > 0
        w = dict(i=0.0, ii=0.0, iii=0.0, iv_min_step=math.inf, v=0.0, vi_rta=0.0, vi_zero=0.0, vii=0.0, tfree=True, n_below=0, n_above=0)
        rep = {f"B{k}": dict(rows=[]) for k in KS}
        for hb in HB:
            CUR[0] = 0.0
            above = F["v_vir"](hb) > vs
            if above:
                w["n_above"] += 1; rR, MR, _ = layout(hb, ft, mode="Rb")
                for k in KS:
                    r, M, inf = BL.budget_fn(ft, z, vs, k)(hb)
                    w["vii"] = max(w["vii"], float(np.max(np.abs(M - MR))) if (len(M) == len(MR) and np.array_equal(r, rR)) else math.inf)
                continue
            w["n_below"] += 1
            for k in KS:
                r, M, inf = BL.budget_fn(ft, z, vs, k)(hb)
                if inf.get("branch") not in ("under", "over"): continue
                Rk, Rs, Q, Ct = inf["R_k"], inf["R_set"], inf["Q"], inf["C_tot"]
                nodes = [Rk] + ([Rs] if 0 < Rs < hb["rta"] else [])
                rr, MB, MR, bar, CB, CR, _ = BL.rows_at(hb, ft, nodes); assert np.array_equal(rr, r)
                C = M - bar
                inn = r <= Rs; out = r >= max(Rk, Rs)
                w["i"] = max(w["i"], float(np.max(rel(C[inn], CB[inn]))) if inn.any() else 0.0)
                w["ii"] = max(w["ii"], float(np.max(rel(C[out], CR[out]))) if out.any() else 0.0)
                w["iii"] = max(w["iii"], float(rel(C[-1], Ct)))
                w["iv_min_step"] = min(w["iv_min_step"], float(np.min(np.diff(C))) / Ct)
                if inf["branch"] == "under": w["v"] = max(w["v"], abs(C[inf["i_k"]] - CR[inf["i_k"]]) / Ct)
                else:
                    iS = inf["i_set"]; w["v"] = max(w["v"], abs(CB[iS] - CR[iS]) / Ct)
                # t-free: each node's C is C_B, Q_k or C_R at that node, bit for bit
                w["tfree"] &= bool(np.all((C == CB) | (C == Q) | (C == CR)))
                rep[f"B{k}"]["rows"].append(dict(lM=float(math.log10(hb["M"])), lMb=float(math.log10(Z["Mb_fold"](hb, ft) / Z["h"])), branch=inf["branch"], capped=inf["capped"],
                                                 Rset_Rk=Rs / Rk, Rset_Rfold=Rs / inf["R_fold"], Rk_Rfold=Rk / inf["R_fold"], D_k=inf["D_k"]))
            # (vi)
            r, M, inf = BL.budget_fn(ft, z, vs, 1, force="rta")(hb)
            if inf.get("branch") in ("under", "over"):
                nodes = [inf["R_k"]] + ([inf["R_set"]] if 0 < inf["R_set"] < hb["rta"] else [])
                rr, MB, MR, bar, CB, CR, _ = BL.rows_at(hb, ft, nodes)
                w["vi_rta"] = max(w["vi_rta"], float(np.max(rel(M, MB))) if np.array_equal(rr, r) else math.inf)
            r, M, inf = BL.budget_fn(ft, z, vs, 1, force="zero")(hb)
            CUR[0] = 0.0; rR, MR, _ = layout(hb, ft, mode="Rb")
            w["vi_zero"] = max(w["vi_zero"], float(np.max(np.abs(M - MR))) if (len(M) == len(MR) and np.array_equal(r, rR)) else math.inf)
        ok = (w["i"] <= 1e-12 and w["ii"] <= 1e-12 and w["iii"] <= 1e-12 and w["iv_min_step"] >= 0 and w["v"] <= 1e-9
              and w["vi_rta"] <= 1e-12 and w["vi_zero"] == 0 and w["vii"] == 0 and w["tfree"])
        if graded: okall &= ok
        RES["KA"][f"{ft}|{z}"] = dict(w, pass_=bool(ok), graded=graded)
        line = []
        for k in KS:
            rows = rep[f"B{k}"]["rows"]; un = [x for x in rows if x["branch"] == "under"]; ov = [x for x in rows if x["branch"] == "over"]
            bym = {}
            for a, b in MBINS:
                s_ = [x for x in rows if a <= x["lM"] < b]
                if s_: bym[f"{a}-{b}"] = dict(n=len(s_), under=sum(1 for x in s_ if x["branch"] == "under"), over=sum(1 for x in s_ if x["branch"] == "over"))
            d = dict(n=len(rows), n_under=len(un), n_over=len(ov), n_over_capped_at_rta=sum(1 for x in ov if x["capped"]),
                     share_under=len(un) / len(rows) if rows else None, by_logM200m=bym,
                     lMb_under_min_max=[min(x["lMb"] for x in un), max(x["lMb"] for x in un)] if un else None,
                     lMb_over_min_max=[min(x["lMb"] for x in ov), max(x["lMb"] for x in ov)] if ov else None,
                     Rset_Rk_under=mmx([x["Rset_Rk"] for x in un]), Rset_Rk_over=mmx([x["Rset_Rk"] for x in ov]),
                     Rset_Rfold_under=mmx([x["Rset_Rfold"] for x in un]), Rset_Rfold_over=mmx([x["Rset_Rfold"] for x in ov]),
                     Rk_Rfold=mmx([x["Rk_Rfold"] for x in rows]), D_k=mmx([x["D_k"] for x in rows]))
            RES["reported"][f"{ft}|{z}|B{k}"] = d
            line.append(f"B{k}: under {d['n_under']} / over {d['n_over']} (capped at r_ta {d['n_over_capped_at_rta']})"
                        + (f", under at log M_b {d['lMb_under_min_max'][0]:.2f}-{d['lMb_under_min_max'][1]:.2f}" if un else "")
                        + (f"; R_set/R_fold under {d['Rset_Rfold_under'][0]:.3f}-{d['Rset_Rfold_under'][2]:.3f}" if un else "")
                        + (f", over {d['Rset_Rfold_over'][0]:.3f}-{d['Rset_Rfold_over'][2]:.3f}" if ov else "")
                        + (f"; R_set/R_k under {d['Rset_Rk_under'][0]:.3f}-{d['Rset_Rk_under'][2]:.3f}" if un else "")
                        + (f", over {d['Rset_Rk_over'][0]:.3f}-{d['Rset_Rk_over'][2]:.3f}" if ov else "")
                        + (f"; D_k {d['D_k'][0]:.3f}-{d['D_k'][2]:.3f}" if rows else ""))
        P(f"[{ft}] z {z}: " + (f"KA {'PASS' if ok else 'FAIL'} " if graded else "(reported only) ") + f"(i) {w['i']:.1e} (ii) {w['ii']:.1e} (iii) {w['iii']:.1e} (iv) min step / C_tot {w['iv_min_step']:.2e} (v) {w['v']:.1e} "
          f"(vi) {w['vi_rta']:.1e} / {w['vi_zero']:.1e} (vii) {w['vii']:.1e} t-free {w['tfree']}; below v* {w['n_below']}, above {w['n_above']}  [{time.time() - T0:.0f} s]")
        for s_ in line: P(f"[{ft}] z {z}   {s_}")
RES["KA_pass_all_forest_z"] = bool(okall)
P(f"profile-level known answers (i) to (vii) and the t-free check, 12 forest redshifts, both footings, B1 B2 B3: {'PASS' if okall else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "bj1_ka_tables.json"), "w"), indent=1)
open(os.path.join(HERE, "bj1_ka_tables.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
