#!/usr/bin/env python3
"""XJ1 AMENDMENT_A5: the profile-level known answers for the two caustic radii Ec2 and Ec3 (a copy of xj1_ka_tables.py through xj1_lib2, with KA-K added; outputs xj1_ka_tables3.*). XJ1 known answers on the profiles (FROZEN_CRITERIA.md, ef8ccdde98, section 4; KA-E (iv) with AMENDMENT_A1's tolerance -1e-12): KA-E (the exact junction) and KA-Z (the
surface reader), every z bin and footing, every halo of FRZ1's grid. Light; no boxes.
  python3 -I -B xj1_ka_tables.py -> xj1_ka_tables.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import xj1_lib2 as XL
INSTALL_DEV = XL.install()
X = XL.X; Z = X.rec(); F, L = Z["F"], Z["L"]; layout, CUR, Bar = Z["layout"], Z["CUR"], Z["Bar"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
CASES = {"Ec2": (XL.COL_K[2], 1.0), "Ec3": (XL.COL_K[3], 1.0)}
RES = dict(lane="XJ1", criteria="ef8ccdde98", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", KA_E={}, KA_Z={}, surfaces={})
okE = True
for ft in XL.FOOTS:
    for z in XL.ZB:
        Z["set_z"](z); vs = X.vstar(ft, z); HB = L["HB"]
        w = dict(i=0.0, ii=0.0, iii=0.0, tmin=math.inf, v_rta=0.0, v_zero=0.0, vi=0.0, n_below=0, n_settled=0)
        ratio = {k: [] for k in CASES}; capped = {k: 0 for k in CASES}; tt = {k: [] for k in CASES}; ss = {k: [] for k in CASES}
        for hb in HB:
            CUR[0] = 0.0
            above = F["v_vir"](hb) > vs
            for key, (col, mult) in CASES.items():
                r, M, inf = XL.exact_fn(ft, z, vs, col, mult)(hb)
                if above:
                    CUR[0] = 0.0; rR, MR, _ = layout(hb, ft, mode="Rb")
                    w["vi"] = max(w["vi"], float(np.max(np.abs(M - MR))) if len(M) == len(MR) else math.inf); continue
                if inf.get("regime") == "L" or "R_set" not in inf: continue
                R = inf["R_set"]; i = inf["i_set"]
                CUR[0] = R; rB, MB, _ = layout(hb, ft, mode="B"); CUR[0] = 0.0
                assert np.array_equal(rB, r)
                w["i"] = max(w["i"], float(np.max(np.abs(M[: i + 1] / MB[: i + 1] - 1))))
                w["ii"] = max(w["ii"], abs(M[-1] / hb["Mta"] - 1))
                w["iii"] = max(w["iii"], float(max(0.0, -np.min(np.diff(M)))) / hb["Mta"])
                w["tmin"] = min(w["tmin"], inf["t"]); tt[key].append(inf["t"]); ss[key].append(inf["s"])
                ratio[key].append(R / XL.rsurf_com(hb, ft, z, XL.COL_FOLD, 1.0)); capped[key] += abs(R / hb["rta"] - 1) < 1e-12
                if key == "Ec2": w["n_settled"] += 1
            if above: continue
            w["n_below"] += 1
            # (v) forced R_set
            r, M, inf = XL.exact_fn(ft, z, vs, XL.COL_FOLD, 1.0, force="rta")(hb)
            if inf.get("regime") != "L":
                CUR[0] = 0.0; rB, MB, _ = layout(hb, ft, mode="B")
                w["v_rta"] = max(w["v_rta"], float(np.max(np.abs(M / MB - 1))) if len(M) == len(MB) else math.inf)
            r, M, inf = XL.exact_fn(ft, z, vs, XL.COL_FOLD, 1.0, force="zero")(hb)
            CUR[0] = 0.0; rR, MR, _ = layout(hb, ft, mode="Rb")
            w["v_zero"] = max(w["v_zero"], float(np.max(np.abs(M - MR))) if len(M) == len(MR) else math.inf)
        ok = w["i"] <= 1e-12 and w["ii"] <= 1e-9 and w["iii"] <= 1e-9 and w["tmin"] >= -1e-12 and w["v_rta"] <= 1e-12 and w["v_zero"] == 0 and w["vi"] == 0
        okE &= ok
        RES["KA_E"][f"{ft}|{z}"] = dict(w, pass_=bool(ok))
        RES["surfaces"][f"{ft}|{z}"] = {k: dict(R_set_over_R_fold_min_med_max=[float(np.min(v)), float(np.median(v)), float(np.max(v))] if v else None,
                                                capped_at_rta=int(capped[k]), n=len(v), t_min_max=[float(min(tt[k])), float(max(tt[k]))] if tt[k] else None,
                                                s_min_max=[float(min(ss[k])), float(max(ss[k]))] if ss[k] else None) for k, v in ratio.items()}
        sz = RES["surfaces"][f"{ft}|{z}"]["Ec3"]; s2 = RES["surfaces"][f"{ft}|{z}"]["Ec2"]
        P(f"[{ft}] z {z}: KA-E {'PASS' if ok else 'FAIL'}  (i) {w['i']:.1e} (ii) {w['ii']:.1e} (iii) {w['iii']:.1e} t_min {w['tmin']:.3f} (v) {w['v_rta']:.1e} / {w['v_zero']:.1e} (vi) {w['vi']:.1e}; "
          f"below v* {w['n_below']} (settled {w['n_settled']}); Ec2 R_set/R_fold min/med/max {s2['R_set_over_R_fold_min_med_max']}; Ec3 R_set/R_fold min/med/max {sz['R_set_over_R_fold_min_med_max']}, capped {sz['capped_at_rta']}/{sz['n']}, t {sz['t_min_max']}, s {sz['s_min_max']}")
# KA-Z (i): the reader on the fold column x 3 against FZS1's rset_com
dz = 0.0
for ft in XL.FOOTS:
    for z in XL.ZB:
        Z["set_z"](z)
        for hb in L["HB"]:
            a = XL.rsurf_com(hb, ft, z, XL.COL_FOLD, 3.0); b = Z["rset_com"](hb, ft, z, 3.0)
            dz = max(dz, abs(a / b - 1) if b > 0 else abs(a))
# KA-Z (ii): FLD1's RESULT table, R_ta at z 0, canonical
TAB = {7: 19, 8: 40, 9: 88, 9.4: 120, 10: 190, 10.45: 268, 10.7: 325, 10.9: 378, 11.2: 476, 11.5: 600}
got = {M: XL.surf_kpc("canonical", 0.0, float(M), XL.COL_ZV) for M in TAB}; d2 = max(abs(got[M] - TAB[M]) for M in TAB)
RES["KA_Z"] = dict(i_max_rel=dz, ii_max_abs_kpc=d2, ii_got={str(k): v for k, v in got.items()}, pass_=bool(dz <= 1e-12 and d2 <= 0.6))
P(f"KA-Z (i) reader on R_fold x 3 against FZS1's rset_com: max rel {dz:.1e}; (ii) R_ta at z 0 against FLD1's table: max abs {d2:.2f} kpc -> {'PASS' if RES['KA_Z']['pass_'] else 'FAIL'}")
RES["KA_E_pass"] = bool(okE)
# KA-K (AMENDMENT_A5): (i) every shell run reproduces FLD1's stored series; (ii) the swapped tables' fold column equals FZS1's
# loaded series (checked at install) and the reader x 3 equals rset_com (KA-Z i above); (iii) R_3 <= R_2 <= R_fold at every stored time
import glob
ki = []; kiii = True; nrun = 0
for f in sorted(glob.glob(os.path.join(HERE, "shells", "xj1_shells_*.json"))):
    d = json.load(open(f)); nrun += 1; ki.append(d["known_answer_max_rel"]); S = np.array(d["series"])
    kiii &= bool(np.all(S[:, 7] <= S[:, 6] + 1e-9) and np.all(S[:, 6] <= S[:, 2] + 1e-9))
RES["KA_K"] = dict(runs=nrun, i_max_rel=float(max(ki)), install_max_rel=INSTALL_DEV, ii_reader_max_rel=dz, iii_ordered=kiii,
                   pass_=bool(nrun == 24 and max(ki) <= 1e-9 and INSTALL_DEV <= 1e-9 and dz <= 1e-9 and kiii))
P(f"KA-K: {nrun} shell runs; (i) max rel against FLD1's stored series {max(ki):.1e}; swapped tables against FZS1's loaded series {INSTALL_DEV:.1e}; (ii) reader x 3 against rset_com {dz:.1e}; (iii) R_3 <= R_2 <= R_fold at every time: {kiii} -> {'PASS' if RES['KA_K']['pass_'] else 'FAIL'}")
P(f"KA-E over all z and footings: {'PASS' if okE else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "xj1_ka_tables3.json"), "w"), indent=1)
open(os.path.join(HERE, "xj1_ka_tables3.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
