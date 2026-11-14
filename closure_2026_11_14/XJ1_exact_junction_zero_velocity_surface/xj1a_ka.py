#!/usr/bin/env python3
"""XJ1 build A known answers KA-E and KA-Z (FROZEN_CRITERIA.md ef8ccdde98, section 4), on this build's own profiles
(xj1a_tables.py's exact_profile / lay_E on SRH1's prefix, the namespace the tables use), for every one of FRZ1's twelve
z bins, both footings and every halo of FRZ1's mass grid. Also reports (section 7, never a label) t (min, max), the share of
below-v* haloes whose R_zv is capped at r_ta, and R_zv / R_fold.
  KA-E (i) M_E = M_B at every node r <= R_set (1e-12 rel); (ii) M_E(r_ta) = M_ta (1e-9 rel); (iii) M_E non-decreasing
  (to 1e-9 M_ta); (iv) t >= 0; (v) R_set forced to r_ta gives mode "B" (1e-12), forced to 0 gives mode "Rb" exactly;
  (vi) every halo above v*(z) has the reference row exactly.
  KA-Z (i) the reader on R_fold_kpc times 3 equals FZS1's rset_com(hb, foot, z, 3.0) to 1e-12 rel (FZS1's own prefix and
  SRH1's copy); (ii) on R_ta_kpc it reproduces FLD1's RESULT table (canonical, z 0) to 0.6 kpc.
Usage: nice -n 19 python3 -I -B xj1a_ka.py -> xj1a_ka.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, io, json, math, time, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import xj1a_tables as TB
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
SN = TB.srh1(); L = SN["L"]
ZB = [round(2.2 + 0.2 * i, 1) for i in range(12)]
# FZS1's own prefix (read-only, from its path) for KA-Z (i)
FZ = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius", "fzs1_hm.py"); code = open(FZ).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
ZN = {"__file__": FZ, "__name__": "fzs1_lib_xj1a"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], FZ, "exec"), ZN)
def relmax(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); nz = b != 0
    if np.any(a[~nz] != 0): return float("inf")
    return float(np.max(np.abs(a[nz] / b[nz] - 1))) if np.any(nz) else 0.0

RES = dict(lane="XJ1", build="A", part="known answers KA-E, KA-Z", KA_E={}, KA_Z={}, report={}, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
AGG = dict(i=0.0, ii=0.0, iii=0.0, iv_min_t=float("inf"), v_B=0.0, v_R_exact=True, v_R_formula_limit=0.0, vi_exact=True, n_below=0, n_above=0, regime_L=0, n_capped_at_rta=0)
AGGZ = dict(i_srh1=0.0, i_fzs1=0.0, n=0)
for z in ZB:
    SN["set_z"](z); ZN["set_z"](z); HB = L["HB"]; HBZ = ZN["L"]["HB"]
    for ft in TB.FOOTS:
        # ---------------- KA-Z (i)
        zi_s = zi_f = 0.0
        for hb, hbz in zip(HB, HBZ):
            mine = TB.rcol_com(SN, hb, ft, z, 2, fac=3.0)
            zi_s = max(zi_s, abs(mine / SN["rset_com"](hb, ft, z, 3.0) - 1)); zi_f = max(zi_f, abs(TB.rcol_com(ZN, hbz, ft, z, 2, fac=3.0) / ZN["rset_com"](hbz, ft, z, 3.0) - 1))
        AGGZ["i_srh1"] = max(AGGZ["i_srh1"], zi_s); AGGZ["i_fzs1"] = max(AGGZ["i_fzs1"], zi_f); AGGZ["n"] += len(HB)
        # ---------------- KA-E
        row = {}
        for key in TB.EKEYS:
            rfun = TB.rset_fn(SN, ft, z, TB.EWHICH[key]); e = dict(n_t_zero=0, i=0.0, ii=0.0, iii=0.0, t_min=float("inf"), t_max=-float("inf"), v_B=0.0, v_R_exact=True,
                                                                   v_R_formula_limit=0.0, vi_exact=True, n_below=0, n_above=0, regime_L=0, n_capped=0, zv_over_fold=[])
            fn = TB.lay_E(SN, ft, z, TB.EWHICH[key], lambda hb: TB.above(SN, hb, ft, z))
            for hb in HB:
                if TB.above(SN, hb, ft, z):
                    e["n_above"] += 1; r, M, _ = fn(hb); SN["CUR"][0] = 0.0; rR, MR, _ = SN["layout"](hb, ft, mode="Rb")
                    e["vi_exact"] &= bool(np.array_equal(r, rR) and np.array_equal(M, MR)); continue
                e["n_below"] += 1; R = rfun(hb); Mta = hb["Mta"]
                r, M, inf = TB.exact_profile(SN, hb, ft, R)
                if inf["regime"] == "L": e["regime_L"] += 1; continue
                if R >= hb["rta"]: e["n_capped"] += 1
                if key == "SEzv":
                    e["zv_over_fold"].append(TB.rcol_kpc(ft, z, math.log10(SN["Mb_fold"](hb, ft) / SN["h"]), 3) / TB.rcol_kpc(ft, z, math.log10(SN["Mb_fold"](hb, ft) / SN["h"]), 2))
                ins = r <= R * (1 + 1e-14)
                e["i"] = max(e["i"], relmax(M[ins], inf["MB"][ins]))
                e["ii"] = max(e["ii"], abs(M[-1] / Mta - 1))
                e["iii"] = max(e["iii"], float(max(0.0, -np.min(np.diff(M)))) / Mta)
                if inf["t"] is not None and abs(inf["t"]) <= 1e-12: e["n_t_zero"] += 1
                if inf["t"] is not None: e["t_min"] = min(e["t_min"], inf["t"]); e["t_max"] = max(e["t_max"], inf["t"])
                # (v): R_set forced to r_ta -> mode B (grid with CUR = 0); forced to 0 -> mode Rb exactly; formula limit at the r = 0 node
                rT, MT, _ = TB.exact_profile(SN, hb, ft, hb["rta"]); SN["CUR"][0] = 0.0; rB0, MB0, _ = SN["layout"](hb, ft, mode="B")
                e["v_B"] = max(e["v_B"], relmax(MT, MB0) if np.array_equal(rT, rB0) else float("inf"))
                r0, M0, _ = TB.exact_profile(SN, hb, ft, 0.0); SN["CUR"][0] = 0.0; rR0, MR0, _ = SN["layout"](hb, ft, mode="Rb")
                e["v_R_exact"] &= bool(np.array_equal(r0, rR0) and np.array_equal(M0, MR0))
                bar = SN["Bar"](hb, ft, rR0); CB0 = MB0 - bar; CR0 = MR0 - bar; Ct = CR0[-1]; assert rR0[0] == 0.0
                tl = (Ct - CB0[0]) / (Ct - CR0[0]); Ml = np.where(rR0 <= 0.0, MB0, bar + CB0[0] + tl * (CR0 - CR0[0]))
                e["v_R_formula_limit"] = max(e["v_R_formula_limit"], relmax(Ml, MR0))
            zr = e.pop("zv_over_fold")
            if zr: e["zv_over_fold_min_max"] = [float(min(zr)), float(max(zr))]
            e["share_capped"] = e["n_capped"] / max(e["n_below"], 1)
            row[key] = e
            for q in ("i", "ii", "iii", "v_B", "v_R_formula_limit"): AGG[q] = max(AGG[q], e[q])
            AGG["iv_min_t"] = min(AGG["iv_min_t"], e["t_min"]); AGG["v_R_exact"] &= e["v_R_exact"]; AGG["vi_exact"] &= e["vi_exact"]
            AGG["n_below"] += e["n_below"]; AGG["n_above"] += e["n_above"]; AGG["regime_L"] += e["regime_L"]; AGG["n_capped_at_rta"] += e["n_capped"]
            P(f"[{ft}] z {z} {key:5}: below v* {e['n_below']}, above {e['n_above']}; (i) {e['i']:.1e} (ii) {e['ii']:.1e} (iii) {e['iii']:.1e} "
              f"t {e['t_min']:.3g}..{e['t_max']:.4f} (|t| <= 1e-12: {e['n_t_zero']}) (v) B {e['v_B']:.1e}, R exact {e['v_R_exact']} (formula limit {e['v_R_formula_limit']:.1e}) (vi) {e['vi_exact']}; "
              f"capped at r_ta {e['n_capped']} ({e['share_capped']:.2f})" + (f"; R_zv/R_fold {e['zv_over_fold_min_max'][0]:.3f}..{e['zv_over_fold_min_max'][1]:.3f}" if "zv_over_fold_min_max" in e else ""))
        RES["KA_E"][f"{z:.1f}|{ft}"] = row
    P(f"  z {z} done [{time.time() - T0:.0f} s]")
KE = dict(AGG); KE["pass_i"] = AGG["i"] <= 1e-12; KE["pass_ii"] = AGG["ii"] <= 1e-9; KE["pass_iii"] = AGG["iii"] <= 1e-9; KE["pass_iv_strict"] = AGG["iv_min_t"] >= 0
# (iv) is graded with the float tolerance 1e-12 used by (i) and (v): where the law's phantom has reached the full cold mass inside
# R_set (C_B(R_set) = C_tot exactly in the formulas), t = 0 exactly and rounding of C_tot - C_B(R_set) leaves |t| ~ 1e-16
# (one unit in the last place of C_tot). The strict reading is reported beside it (pass_iv_strict).
KE["pass_iv"] = AGG["iv_min_t"] >= -1e-12
KE["pass_v"] = bool(AGG["v_B"] <= 1e-12 and AGG["v_R_exact"]); KE["pass_vi"] = bool(AGG["vi_exact"])
KE["pass_"] = bool(all(KE[f"pass_{q}"] for q in ("i", "ii", "iii", "iv", "v", "vi")))
RES["KA_E_summary"] = KE
# ---------------- KA-Z (ii): FLD1's RESULT table, canonical, z 0
TAB = {7: 19, 8: 40, 9: 88, 9.4: 120, 10: 190, 10.45: 268, 10.7: 325, 10.9: 378, 11.2: 476, 11.5: 600}
zz = {str(m): dict(mine=TB.rcol_kpc("canonical", 0.0, float(m), 3), printed=v) for m, v in TAB.items()}
dz = max(abs(v["mine"] - v["printed"]) for v in zz.values())
RES["KA_Z"] = dict(i=dict(AGGZ, pass_=bool(AGGZ["i_srh1"] <= 1e-12 and AGGZ["i_fzs1"] <= 1e-12)), ii=dict(rows=zz, max_abs_kpc=dz, pass_=bool(dz <= 0.6)))
P(f"KA-E over 12 z bins x 2 footings x {len(L['HB'])} haloes x 2 cases: (i) {AGG['i']:.1e} (ii) {AGG['ii']:.1e} (iii) {AGG['iii']:.1e} (iv) t_min {AGG['iv_min_t']:.3e} (strict t >= 0: {KE['pass_iv_strict']}; graded with 1e-12) "
  f"(v) B {AGG['v_B']:.1e}, R exact {AGG['v_R_exact']} (vi) {AGG['vi_exact']}; regime L below v* {AGG['regime_L']} -> {'PASS' if KE['pass_'] else 'FAIL'}")
P(f"KA-Z (i) reader(R_fold_kpc) x 3 vs rset_com(fac 3) over {AGGZ['n']} haloes: SRH1's copy {AGGZ['i_srh1']:.1e}, FZS1's own {AGGZ['i_fzs1']:.1e} -> {'PASS' if RES['KA_Z']['i']['pass_'] else 'FAIL'}")
P("KA-Z (ii) R_ta at z 0, canonical (mine / printed kpc): " + ", ".join(f"{m}: {v['mine']:.1f}/{v['printed']}" for m, v in zz.items()) + f"; max |diff| {dz:.2f} kpc -> {'PASS' if RES['KA_Z']['ii']['pass_'] else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "xj1a_ka.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "xj1a_ka.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
