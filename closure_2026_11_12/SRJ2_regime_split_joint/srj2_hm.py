#!/usr/bin/env python3
"""SRJ2 (FROZEN_CRITERIA.md, b8a99499ad): G1 halo-model part. R_cold(k, z) at the DESI P1D bins under the regime-split
settled joint: FZS1's settled layout (law inside R_set = f R_fold, reference outside, junction s) for galaxy-regime haloes
only; cluster-regime haloes (FRZ1's v_vir > VST) keep the reference layout (FRZ1 mode "Rb") at every radius.
FZS1's fzs1_hm.py is executed read-only up to its "checkpointed run" marker (which executes FRZ1's frz1_hm.py prefix
unchanged); its layout function lay_S is copied here with one switch (split). Nothing is written outside this folder.
  Cases: KA_0 (f 0), off_f1.00 (split off = FZS1's rule = check C1 = twin TW-C), on_f1.00 (graded), on_f0.75, on_f1.25,
  on_f2.00 (twin TW-F2). Checks C3 (v_vir and VST against FRZ1), C4 (KA-M for the split joint at z 3). z = 0 table.
  python3 srj2_hm.py -> srj2_hm.json / .out  (checkpoint srj2_hm_partial.json; SIGTERM-safe)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, signal, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FZD = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
SRC = os.path.join(FZD, "fzs1_hm.py"); code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
Z = {"__file__": SRC, "__name__": "fzs1_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), Z)
F, L = Z["F"], Z["L"]; layout, set_z, regime, Bar, rset_com, CUR = (Z[k] for k in ("layout", "set_z", "regime", "Bar", "rset_com", "CUR"))
KK, ZB, FOOTS, VST, at = Z["KK"], Z["ZB"], Z["FOOTS"], Z["VST"], Z["at"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()

# ------------------------------------------------------------------ C3: regime constants from FRZ1's code
assert VST == {"canonical": 265.8, "alt": 288.1}, VST
GF = F["G"]
def vvir_lane(hb, z): return math.sqrt(GF * hb["M200c"] * (1 + z) / hb["r200c"])
c3 = 0.0
for z in (2.2, 0.0):
    set_z(z)
    for hb in L["HB"]: c3 = max(c3, abs(vvir_lane(hb, z) / F["v_vir"](hb) - 1))
C3 = dict(VST=VST, max_rel_vvir=c3, pass_=bool(c3 <= 1e-12))
P(f"C3 VST {VST} from FRZ1's code; lane v_vir against FRZ1's v_vir at z 2.2 and 0: max rel {c3:.1e} -> {'PASS' if C3['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ the split layout (FZS1's lay_S, copied, one switch)
def lay_J(foot, z, fac=1.0, split=True, **opt):
    optR = {k: v for k, v in opt.items() if k in ("gal_scope", "clu_scope", "rc_fac")}
    def fn(hb):
        if split and regime(hb, foot) == "cluster":                         # the joint: reference at every radius
            CUR[0] = 0.0; rR, MR, inf = layout(hb, foot, mode="Rb", **optR); return rR, MR, dict(inf, R_set=0.0, split_ref=True)
        R = rset_com(hb, foot, z, fac); CUR[0] = R
        rB, MB, inf = layout(hb, foot, mode="B", **opt); rR, MR, _ = layout(hb, foot, mode="Rb", **optR); CUR[0] = 0.0
        if R <= 0 or inf["regime"] == "L": return rR, MR, dict(inf, R_set=R)
        assert len(rB) == len(rR) and np.array_equal(rB, rR)
        bar = Bar(hb, foot, rB, **optR); CB, CR = MB - bar, MR - bar
        i = int(np.argmin(abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
        s = CR[i] / CB[i]
        return rB, np.where(rB <= rB[i], bar + s * CB, bar + CR), dict(inf, R_set=R, s=float(s))
    return fn
def ratios_J(foot, z, fac=1.0, split=True):
    CUR[0] = 0.0
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    US, inf = L["U_set"](lay_J(foot, z, fac, split)); PS, _, _ = L["spectra_ta"](US)
    Rtot = 1 + (PS - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    return Rtot, Rbar, Rtot / Rbar, inf

# ------------------------------------------------------------------ checkpointed run
PART = os.path.join(HERE, "srj2_hm_partial.json")
RES = json.load(open(PART)) if os.path.exists(PART) else dict(cases={}, KA={}, z0_table={})
def save(): json.dump(RES, open(PART, "w"))
def on_term(sig, frm):
    save(); print("SIGTERM: checkpoint written; rerun to resume", flush=True); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
P("SRJ2 G1 halo model, regime-split settled joint. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
RES["KA"]["C3"] = C3

# C4: KA-M for the split joint at z = 3
set_z(3.0); err = 0.0; mono = True
for ft in FOOTS:
    for fac in (0.75, 1.0, 1.25):
        fn = lay_J(ft, 3.0, fac, True)
        for hb in L["HB"]:
            r, Mx, _ = fn(hb)
            err = max(err, abs(Mx[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(Mx) >= -1e-9 * hb["Mta"]))
RES["KA"]["C4_KA_M"] = dict(max_rel=err, monotone=mono, pass_=bool(err <= 1e-9 and mono))
P(f"C4 KA-M (split joint, z 3, f 0.75 / 1 / 1.25): max |M(r_ta) - M_ta| / M_ta {err:.1e}, non-decreasing {mono} -> {'PASS' if RES['KA']['C4_KA_M']['pass_'] else 'FAIL'}")

# z = 0 table (reported)
set_z(0.0)
for ft in FOOTS:
    for name, fac, sp in (("on_f1.00", 1.0, True), ("off_f1.00", 1.0, False), ("f0", 0.0, True)):
        key = f"{ft}|{name}"
        if key in RES["z0_table"]: continue
        Rt, Rb, Rc, inf = ratios_J(ft, 0.0, fac, sp)
        RES["z0_table"][key] = dict(R_tot_at_k1_3=at(Rt, (1.0, 3.0)), n_cluster=sum(1 for i in inf if i.get("regime") == "cluster")); save()
    P(f"z = 0 R_tot at k 1 / 3 [{ft}]: " + "; ".join(f"{n} {RES['z0_table'][ft + '|' + n]['R_tot_at_k1_3'][0]:.4f} / {RES['z0_table'][ft + '|' + n]['R_tot_at_k1_3'][1]:.4f}" for n in ("f0", "on_f1.00", "off_f1.00")))
save()

CASES = [("KA_0", 0.0, True), ("off_f1.00", 1.0, False), ("on_f1.00", 1.0, True), ("on_f0.75", 0.75, True), ("on_f1.25", 1.25, True), ("on_f2.00", 2.0, True)]
for name, fac, sp in CASES:
    for ft in FOOTS:
        key = f"{name}|{ft}"
        if key in RES["cases"]: continue
        rows = {}
        for z in ZB:
            set_z(z); Rt, Rb, Rc, inf = ratios_J(ft, z, fac, sp)
            ss = [i.get("s") for i in inf if i.get("s") is not None]
            ncl = sum(1 for i in inf if i.get("regime") == "cluster")
            vmin = min((F["v_vir"](hb), hb["M"]) for hb in L["HB"] if regime(hb, ft) == "cluster") if ncl else None
            rows[str(z)] = dict(R_cold=Rc.tolist(), R_tot_at=at(Rt), R_cold_at=at(Rc), s_min_max=[min(ss), max(ss)] if ss else None,
                                n_cluster_regime=ncl, n_haloes=len(inf), lightest_cluster_regime_M=vmin[1] if vmin else None)
        RES["cases"][key] = rows; save()
        P(f"  {name:10s} {ft:9s} R_cold at k 1/3/5/10: z 2.2 " + "/".join(f"{x:.5f}" for x in rows["2.2"]["R_cold_at"]) + "; z 3.0 "
          + "/".join(f"{x:.5f}" for x in rows["3.0"]["R_cold_at"]) + "; z 4.4 " + "/".join(f"{x:.5f}" for x in rows["4.4"]["R_cold_at"])
          + f"; cluster-regime haloes z 2.2 / 4.4: {rows['2.2']['n_cluster_regime']} / {rows['4.4']['n_cluster_regime']} of {rows['2.2']['n_haloes']}   [{time.time() - T0:.0f} s]")
# KA-0 on the halo model; C1 halo-model part against FZS1's stored primary
FZ = json.load(open(os.path.join(FZD, "fzs1_hm.json")))
k0 = {ft: max(float(np.max(np.abs(np.array(RES["cases"][f"KA_0|{ft}"][str(z)]["R_cold"]) - 1))) for z in ZB) for ft in FOOTS}
c1 = {ft: max(float(np.max(np.abs(np.array(RES["cases"][f"off_f1.00|{ft}"][str(z)]["R_cold"]) / np.array(FZ["cases"][f"primary|{ft}"][str(z)]["R_cold"]) - 1))) for z in ZB) for ft in FOOTS}
RES["KA"]["KA_0_hm"] = dict(max_abs=k0, pass_=bool(max(k0.values()) <= 1e-12))
RES["KA"]["C1_hm"] = dict(max_rel_vs_FZS1_primary=c1, pass_=bool(max(c1.values()) <= 1e-10))
P(f"KA-0 (f 0): max |R_cold - 1| {k0} -> {'PASS' if RES['KA']['KA_0_hm']['pass_'] else 'FAIL'}")
P(f"C1 (halo model) split off, f 1 against FZS1's stored primary R_cold: max rel {c1} -> {'PASS' if RES['KA']['C1_hm']['pass_'] else 'FAIL'}")
RES.update(lane="SRJ2", part="G1 halo model", criteria="b8a99499ad", k=KK.tolist(), z_bins=ZB, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", seconds=time.time() - T0)
json.dump(RES, open(os.path.join(HERE, "srj2_hm.json"), "w"), indent=1)
open(os.path.join(HERE, "srj2_hm.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
os.remove(PART); P(f"done ({time.time() - T0:.0f} s)")
