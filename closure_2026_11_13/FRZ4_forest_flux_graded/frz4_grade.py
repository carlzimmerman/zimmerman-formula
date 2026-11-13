#!/usr/bin/env python3
"""FRZ4 grading (FROZEN_CRITERIA.md 199d710a9a). The gate is FRZ3R's grading set-up (frz3r_grade.py up to its "parts" marker,
executed read-only from FRZ3R's folder, as SRF1's srf1_grade.py does: the record's ss1_cosmo.forest_setup / forest_eval, DESI
DR1 P1D, full covariance). Usage: nice -n 19 python3 frz4_grade.py <footing>
-> frz4_grade_<footing>.json/.out and frz4_grade_<footing>_MUTATE.json/.out.  kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, glob, warnings
warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ3R = os.path.join(REPO, "closure_2026_11_12", "FRZ3R_blind_flux_forest_regrade")
SRF1 = os.path.join(REPO, "closure_2026_11_12", "SRF1_settled_radius_flux_window")
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
src = open(os.path.join(FRZ3R, "frz3r_grade.py")).read(); cut = src.index("# ------------------------------------------------------------------ parts")
g = {"__file__": os.path.join(FRZ3R, "frz3r_grade.py"), "__name__": "frz3r_grade_setup_frz4"}; _a = sys.argv; sys.argv = ["frz3r_grade.py", FOOT]
exec(compile(src[:cut], "frz3r_grade_setup", "exec"), g); sys.argv = _a
FD, forest_eval, BGB, amp, dchi2_sel, ZB, ALL, bin_sel, md5ok = (g[k] for k in ("FD", "forest_eval", "BGB", "amp", "dchi2_sel", "ZB", "ALL", "bin_sel", "md5ok"))
sys.path.insert(0, HERE); import frz4_tables as TB
KT = TB.KT; fk_ = TB.fkey
CASES = [fk_(f) for f in TB.CASES]
ZC = [2.2, 2.6, 3.0, 3.4, 3.8, 4.4]                      # computed bins (criteria section 4)
ANCH = (2.2, 3.0, 4.4)
OUT, OUTM = [], []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)
def tau_eff(z): return 0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132

# ------------------------------------------------------------------ parts
def load(stage):
    D = {}
    for f in sorted(glob.glob(os.path.join(HERE, "parts", f"{stage}_z*_s*_{FOOT}.json"))):
        d = json.load(open(f)); D.setdefault(round(d["z"], 1), {})[d["seed"]] = d
    return D
PR = load("primary"); BR = load("bracket"); CL = load("clustered")
ZCOMP = [z for z in ZC if z in PR and 0 in PR[z]]
ZEST = [z for z in ZB if round(z, 1) not in ZCOMP]
P(f"[{FOOT}] FRZ4: computed bins {ZCOMP}; estimated bins (linear in z between computed neighbours) {[round(z, 1) for z in ZEST]}")

def est(d, key, spec="primary", what="p", pre="B|", boxes=None, regime=None, RG=None):
    """stratified ratio X_B / X_R (criteria section 3). boxes: restrict to a subset of forced boxes (brackets).
    regime 'galaxy' / 'cluster': the change split (denominator unchanged)."""
    F = d["base"]["flux"][spec]; XRb = np.array(F["R"][what]); XR = XRb.copy(); dX = np.zeros_like(XRb)
    if regime in (None, "galaxy"): dX = dX + np.array(F[pre + key][what]) - XRb
    use = d["boxes"] if boxes is None else [b for b in d["boxes"] if b in boxes]
    for ib in use:
        fb = d["forced_boxes"][str(ib)]; Fb = fb["flux"][spec]; E = fb["E"]
        XR = XR + E * (np.array(Fb["R"][what]) - XRb)
        if regime is None or (RG is not None and (RG[ib] >= 0.5) == (regime == "cluster")):
            dX = dX + E * (np.array(Fb[pre + key][what]) - np.array(Fb["R"][what]))
    return 1.0 + dX / XR

def seed_mean(z, fn):
    ps = PR[z]; return np.mean([fn(ps[s]) for s in sorted(ps)], 0)

def r_points(Rz_kv):
    """ratio at the 755 DESI points; Rz_kv: {z: (kv, R)} for computed bins; estimated bins linear in z between neighbours."""
    r = np.ones(FD["NB"])
    for z in ZB:
        s_ = FD["zs"] == round(z, 2); ks = FD["ks"][s_]
        zz = round(z, 1)
        if zz in Rz_kv:
            kv, R = Rz_kv[zz]; r[s_] = np.interp(ks, kv[1:], R[1:])
        else:
            lo = max([c for c in Rz_kv if c < zz], default=None); hi = min([c for c in Rz_kv if c > zz], default=None)
            if lo is None or hi is None: continue
            a = np.interp(ks, Rz_kv[lo][0][1:], Rz_kv[lo][1][1:]); b = np.interp(ks, Rz_kv[hi][0][1:], Rz_kv[hi][1][1:])
            r[s_] = a + (b - a) * (zz - lo) / (hi - lo)
    return r
def mat_dchi(Rk, k, only=None):
    """record projection of the 3D ratio; Rk {z computed: R(k)}; estimated bins linear in z; only: keep one bin, others 1."""
    full = {}
    for z in ZB:
        zz = round(z, 1)
        if zz in Rk: full[z] = Rk[zz]
        else:
            lo = max([c for c in Rk if c < zz], default=None); hi = min([c for c in Rk if c > zz], default=None)
            full[z] = Rk[lo] + (Rk[hi] - Rk[lo]) * (zz - lo) / (hi - lo) if (lo is not None and hi is not None) else np.ones_like(k)
        if only is not None and abs(z - only) > 1e-6: full[z] = np.ones_like(k)
    return float(forest_eval(FD, BGB, amp(full, k))["dchi2"])

def flux_set(key, fn=None, zs=None):
    fn = fn or (lambda d: est(d, key))
    return {z: (np.array(PR[z][0]["kv"]), seed_mean(z, fn)) for z in (zs or ZCOMP)}
def mat_set(key, fn=None, zs=None):
    fn = fn or (lambda d: est(d, key, what="P3D"))
    k = np.array(PR[ZCOMP[0]][0]["k3d"]); m = (k <= 10) & KOK
    return {z: seed_mean(z, fn)[m] for z in (zs or ZCOMP)}, k[m]
KOK = np.all([np.array(PR[z][s]["base"]["flux"]["primary"]["R"]["P3D"]) > 0 for z in ZCOMP for s in PR[z]], 0)   # 3D bins holding modes (SRF1: isfinite)
def dflux(Rset, sel=ALL): return dchi2_sel(r_points(Rset), sel)
def only_bins(zs): return np.isin(np.round(FD["zs"], 1), [round(z, 1) for z in zs])

# ------------------------------------------------------------------ halo model per case
T = {round(z, 1): TB.tables(z)[FOOT] for z in ZB}
KKF = np.geomspace(1e-3, 10.0, 260)
def hm_D(key, q, only=None):
    Rz = {}
    for z in ZB:
        Rz[z] = np.interp(np.log(KKF), np.log(KT[1:]), T[round(z, 1)]["spec"][key][q][1:])
        if only is not None and abs(z - only) > 1e-6: Rz[z] = np.ones_like(KKF)
    return float(forest_eval(FD, BGB, amp(Rz, KKF))["dchi2"])
Drec = {k: hm_D(k, "Rcold") for k in CASES}; Dta = {k: hm_D(k, "Rta") for k in CASES}

# ------------------------------------------------------------------ primary table
RES = dict(lane="FRZ4", footing=FOOT, criteria="199d710a9a", computed_bins=ZCOMP, estimated_bins=[round(z, 1) for z in ZEST],
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
rows = {}
for key in CASES:
    Fs = flux_set(key); Df = dflux(Fs); Ms, k3 = mat_set(key); Dm = mat_dchi(Ms, k3)
    perbin = {f"{z:.1f}" + ("" if round(z, 1) in ZCOMP else " (estimated)"): dchi2_sel(r_points(Fs), bin_sel(z)) for z in ZB}
    rows[key] = dict(flux=Df, matter=Dm, ratio=Df / Dm if Dm > 0 else None, D_ta=Dta[key], D_rec=Drec[key], c1_ratio=Dm / Dta[key],
                     q=Dm / Drec[key], record_convention_reading=Df * Drec[key] / Dm if Dm > 0 else None, per_bin=perbin,
                     R_F={f"{z:.1f}": [float(np.interp(x, Fs[z][0][1:], Fs[z][1][1:])) for x in (0.003, 0.005, 0.01, 0.02, 0.03)] for z in ZCOMP},
                     R_mat={f"{z:.1f}": [float(np.exp(np.interp(math.log(x), np.log(k3), np.log(Ms[z])))) for x in (1, 3, 5)] for z in ZCOMP},
                     R_ta={f"{z:.1f}": [float(np.interp(math.log(x), np.log(KT[1:]), T[z]["spec"][key]["Rta"][1:])) for x in (1, 3, 5)] for z in ZCOMP})
RES["rows"] = rows
P(f"[{FOOT}] case | flux dchi2 (12 bins) | matter, same fields | flux/matter | D_ta (halo model) | matter/D_ta (c1) | D_rec (record) | record-convention reading flux x D_rec/D_mat")
for key, r in rows.items():
    P(f"[{FOOT}] {key:5} | {r['flux']:10.4f} | {r['matter']:10.2f} | {r['ratio']:.5f} | {r['D_ta']:9.2f} | {r['c1_ratio']:.3f} | {r['D_rec']:9.2f} | {r['record_convention_reading']:.4f}")
for key, r in rows.items():
    P(f"[{FOOT}] per bin {key}: " + " ".join(f"{z}:{v:.4g}" for z, v in r["per_bin"].items()))
    for z in ZCOMP:
        P(f"[{FOOT}]   {key} z {z}: R_F at 0.003/0.005/0.01/0.02/0.03 s/km " + "/".join(f"{v:.5f}" for v in r["R_F"][f"{z:.1f}"]) + "; R_mat k1/3/5 "
          + "/".join(f"{v:.4f}" for v in r["R_mat"][f"{z:.1f}"]) + " (halo model ta " + "/".join(f"{v:.4f}" for v in r["R_ta"][f"{z:.1f}"]) + ")")

# ------------------------------------------------------------------ known answers
KA = {}
# (a)
amax = 0.0; nbox = 0
for z in ANCH:
    if z not in PR or 0 not in PR[z]: continue
    d = PR[z][0]
    for bx in [d["base"]] + list(d["forced_boxes"].values()):
        F = bx["flux"]["primary"]
        if "B|f0.00" in F:
            amax = max(amax, float(np.max(np.abs(np.array(F["B|f0.00"]["p"]) / np.array(F["R"]["p"]) - 1)))); nbox += 1
za = [z for z in ANCH if z in PR and 0 in PR[z]]
Fa = {z: (np.array(PR[z][0]["kv"]), est(PR[z][0], "f0.00")) for z in za}
ra = np.ones(FD["NB"])
for z in za:
    s_ = FD["zs"] == round(z, 2); ra[s_] = np.interp(FD["ks"][s_], Fa[z][0][1:], Fa[z][1][1:])
Da = dchi2_sel(ra, ALL)
KA["a"] = dict(max_rel_box=amax, boxes=nbox, dchi2_f0=Da, md5ok=md5ok, pass_=bool(nbox > 0 and amax <= 1e-12 and Da <= 1e-12 and md5ok))
# (b)
bmax = 0.0; mine, frz, mineM, frzM = {}, {}, {}, {}
kf = None
for z in ZCOMP:
    arr, arr2, a3, b3 = [], [], [], []
    for s, d in PR[z].items():
        fr = json.load(open(os.path.join(FRZ3R, "parts", f"turn_z{z:.1f}_s{s}_{FOOT}_N384.json")))
        F = d["base"]["flux"]["primary"]
        bmax = max(bmax, float(np.max(np.abs(np.array(F["Rall"]["p"]) / np.array(fr["flux"]["primary"]["R"]["p"]) - 1))),
                   float(np.max(np.abs(np.array(F["BPall|finf"]["p"]) / np.array(fr["flux"]["primary"]["B"]["p"]) - 1))))
        arr.append(np.array(F["BPall|finf"]["p"]) / np.array(F["Rall"]["p"])); arr2.append(np.array(fr["flux"]["primary"]["B"]["p"]) / np.array(fr["flux"]["primary"]["R"]["p"]))
        a3.append(np.array(F["BPall|finf"]["P3D"]) / np.array(F["Rall"]["P3D"]))
        kf = np.array(fr["P3D"]["k"]); b3.append(np.array(fr["P3D"]["B"]) / np.array(fr["P3D"]["R"]))
    kv = np.array(PR[z][0]["kv"]); mine[z] = (kv, np.mean(arr, 0)); frz[z] = (np.array(fr["kv"]), np.mean(arr2, 0))
    mineM[z] = np.mean(a3, 0); frzM[z] = np.mean(b3, 0)
selC = only_bins(ZCOMP)
def rp_only(Rset):
    r = np.ones(FD["NB"])
    for z, (kv, R) in Rset.items():
        s_ = np.round(FD["zs"], 1) == z; r[s_] = np.interp(FD["ks"][s_], kv[1:], R[1:])
    return r
Db_m, Db_f = dchi2_sel(rp_only(mine), ALL), dchi2_sel(rp_only(frz), ALL)
k3 = np.array(PR[ZCOMP[0]][0]["k3d"]); mk = (k3 <= 10) & KOK; mkf = (kf <= 10) & np.all([np.isfinite(v) for v in frzM.values()], 0)
def mat_only(Rk, k):
    full = {z: (Rk[round(z, 1)] if round(z, 1) in Rk else np.ones_like(k)) for z in ZB}; return float(forest_eval(FD, BGB, amp(full, k))["dchi2"])
Dbm_m = mat_only({z: v[mk] for z, v in mineM.items()}, k3[mk]); Dbm_f = mat_only({z: v[mkf] for z, v in frzM.items()}, kf[mkf])
KA["b"] = dict(max_rel_part=bmax, flux_computed_bins=[Db_m, Db_f], matter_computed_bins=[Dbm_m, Dbm_f],
               pass_=bool(bmax <= 1e-4 and abs(Db_m / Db_f - 1) <= 0.01 and abs(Dbm_m / Dbm_f - 1) <= 0.01))
# (c0)
SF = json.load(open(os.path.join(SRH, f"srh1_forest_{FOOT}.json")))["cases"]
SR = json.load(open(os.path.join(SRF1, f"srf1_grade_{FOOT}.json")))["rows"]
ref0 = {"f1.00": ("SRH1 f1.00 (= FZS1)", SF["f1.00"]["dchi2"]), "f2.00": ("SRH1 f2.00", SF["f2.00"]["dchi2"]),
        "f3.00": ("SRF1 f3.00 (own chain)", SR["f3.00"]["D_rec"]), "finf": ("SRH1 KA_T (= FRZ1)", SF["KA_T"]["dchi2"])}
KA["c0"] = {key: dict(mine=Drec[key], ref=ref0[key][1], source=ref0[key][0], pass_=bool(abs(Drec[key] / ref0[key][1] - 1) <= 0.01)) for key in CASES}
# (c1)
KA["c1"] = {}
for key in CASES:
    Ms, k3m = mat_set(key); okc = 0.67 <= rows[key]["c1_ratio"] <= 1.5; pb = {}
    for z in ZCOMP:
        h = hm_D(key, "Rta", only=z)
        if h >= 1.0:
            rz = mat_dchi(Ms, k3m, only=z); pb[f"{z:.1f}"] = dict(realised=rz, halo_model=h, ratio=rz / h, ok=bool(0.5 <= rz / h <= 2.0)); okc &= pb[f"{z:.1f}"]["ok"]
        else:
            pb[f"{z:.1f}"] = dict(halo_model=h, checked=False)
    KA["c1"][key] = dict(realised=rows[key]["matter"], halo_model_ta=Dta[key], ratio=rows[key]["c1_ratio"], per_bin=pb, pass_=bool(okc))
# (d)
dmax = 0.0
for stg, PP in (("primary", PR), ("bracket", BR), ("clustered", CL)):
    for z, ps in PP.items():
        for d in ps.values():
            for bx in [d["base"]] + list(d["forced_boxes"].values()):
                for sp, fields in bx["flux"].items():
                    sF = {"tau_x0.9": 0.9, "tau_x1.1": 1.1}.get(sp, 1.0)
                    for v in fields.values(): dmax = max(dmax, abs(v["meanF"] - math.exp(-sF * tau_eff(z))))
KA["d"] = dict(max_abs=dmax, pass_=bool(dmax <= 1e-4))
# (e)
KA["e"] = {}
S22 = bin_sel(2.2)
for key in CASES:
    if 2.2 in PR and 1 in PR[2.2]:
        d0, d1 = PR[2.2][0], PR[2.2][1]; kv = np.array(d0["kv"])
        half = 1.0 + 0.5 * (est(d0, key) - est(d1, key)); mean = 0.5 * (est(d0, key) + est(d1, key))
        N22 = dchi2_sel(rp_only({2.2: (kv, half)}), ALL); D22 = dchi2_sel(rp_only({2.2: (kv, mean)}), ALL)
        D = rows[key]["flux"]; N12 = D * N22 / D22 if D22 > 0 else float("inf"); SE = 2 * math.sqrt(D * N12) + N12
        KA["e"][key] = dict(N22=N22, D22=D22, N12=N12, SE=SE, D_seed0_z22=dchi2_sel(rp_only({2.2: (kv, est(d0, key))}), ALL),
                            D_seed1_z22=dchi2_sel(rp_only({2.2: (kv, est(d1, key))}), ALL), marginal=bool(abs(D - 4) < 2 * SE),
                            pass_=bool(N12 <= 0.1 * D or N12 <= 0.05))
    else:
        KA["e"][key] = dict(pass_=False, note="seed 1 at z 2.2 not computed")
RES["known_answers"] = KA
def ka_case(key):
    return dict(a=KA["a"]["pass_"], b=KA["b"]["pass_"], c0=KA["c0"][key]["pass_"], c1=KA["c1"][key]["pass_"], d=KA["d"]["pass_"], e=KA["e"][key]["pass_"])
P(f"[{FOOT}] known answer (a): {'PASS' if KA['a']['pass_'] else 'FAIL'} max |B_f0/R - 1| {amax:.2e} over {nbox} boxes; 12-bin (anchors) dchi2 at f 0 {Da:.2e}; md5 {md5ok}")
P(f"[{FOOT}] known answer (b): {'PASS' if KA['b']['pass_'] else 'FAIL'} max rel vs FRZ3R turn parts {bmax:.2e}; Poisson-only f inf on computed bins: flux {Db_m:.3f} vs FRZ3R {Db_f:.3f}; matter {Dbm_m:.2f} vs {Dbm_f:.2f}")
for key in CASES:
    c0 = KA["c0"][key]; c1 = KA["c1"][key]; e = KA["e"][key]
    P(f"[{FOOT}] known answer (c0) {key}: {'PASS' if c0['pass_'] else 'FAIL'} D_rec {c0['mine']:.3f} vs {c0['source']} {c0['ref']:.3f}")
    P(f"[{FOOT}] known answer (c1) {key}: {'PASS' if c1['pass_'] else 'FAIL'} realised {c1['realised']:.3f} / halo model {c1['halo_model_ta']:.3f} = {c1['ratio']:.3f} (0.67 to 1.5); per bin "
      + "; ".join(f"{z}: " + (f"{v['realised']:.3g}/{v['halo_model']:.3g}={v['ratio']:.2f}{'' if v['ok'] else ' OUT'}" if v.get("checked", True) else f"hm {v['halo_model']:.3g} (<1, not checked)") for z, v in c1["per_bin"].items()))
    P(f"[{FOOT}] known answer (e) {key}: {'PASS' if e['pass_'] else 'FAIL'} " + json.dumps({k: v for k, v in e.items() if k != 'pass_'}, default=float))
P(f"[{FOOT}] known answer (d): {'PASS' if KA['d']['pass_'] else 'FAIL'} max |<F> - target| {dmax:.2e}")

# ------------------------------------------------------------------ reported readings
Fp = {z: (np.array(PR[z][0]["kv"]), seed_mean(z, lambda d: np.array(d["base"]["flux"]["primary"]["BPall|finf"]["p"]) / np.array(d["base"]["flux"]["primary"]["Rall"]["p"]))) for z in ZCOMP}
Mp = {z: seed_mean(z, lambda d: np.array(d["base"]["flux"]["primary"]["BPall|finf"]["P3D"]) / np.array(d["base"]["flux"]["primary"]["Rall"]["P3D"]))[mk] for z in ZCOMP}
RES["poisson_only_finf"] = dict(flux=dflux(Fp), matter=mat_dchi(Mp, k3[mk]))
P(f"[{FOOT}] Poisson-only reading (FRZ3R's reading T path, every halo at its Poisson position, f inf, 12 bins with the same estimated bins): flux {RES['poisson_only_finf']['flux']:.2f}, matter {RES['poisson_only_finf']['matter']:.1f}")
FI = {f"{z:.1f}": {k: (v if not isinstance(v, list) or len(v) < 60 else None) for k, v in PR[z][0]["forced_info"].items() if k in ("forced", "subset", "forced_share", "nonforced_rare_share", "common_share", "forced_ref_share", "over_cap")} for z in ZCOMP}
for z in ZCOMP:
    fi = PR[z][0]["forced_info"]; FI[f"{z:.1f}"]["forced_lM"] = [round(fi["lM_lo"][i], 1) for i in fi["forced"]]; FI[f"{z:.1f}"]["subset_lM"] = [round(fi["lM_lo"][i], 1) for i in fi["subset"]]
    sub = fi["subset"]; FI[f"{z:.1f}"]["subset_cover"] = {k: float(sum(fi["share"][k][j] for j in sub) / sum(fi["share"][k][j] for j in fi["forced"])) for k in CASES}
RES["forced_sets"] = FI
for z, v in FI.items():
    P(f"[{FOOT}] forced set z {z}: {len(v['forced'])} bins, log M {v['forced_lM'][0]} to {v['forced_lM'][-1]}; share of the ta-scope 1h difference at k 3 carried: "
      + "/".join(f"{x:+.3f}" for x in v["forced_share"].values()) + "; non-forced rare: " + "/".join(f"{x:+.4f}" for x in v["nonforced_rare_share"].values())
      + f"; reference rare 1h share forced {v['forced_ref_share']:.3f}; over cap {v['over_cap']}; bracket subset log M {v['subset_lM']} covering " + "/".join(f"{x:.2f}" for x in v["subset_cover"].values()))

# regime split (criteria section 9)
SN = TB.srh1(); RGs = {}; base_cl = {}
for z in ZCOMP:
    SN["set_z"](z); L_ = SN["L"]; LMg = L_["LM"]; fi = PR[z][0]["forced_info"]; rg = {}
    for ib in range(len(fi["lM_lo"])):
        lo = fi["lM_lo"][ib]; cl = [SN["regime"](hb, FOOT) == "cluster" for hb, lm in zip(L_["HB"], LMg) if lo - 1e-9 <= lm < lo + 0.1 - 1e-9]
        rg[ib] = sum(cl) / max(len(cl), 1)
    RGs[z] = rg
    nf = [i for i in range(len(fi["lM_lo"])) if i not in fi["forced"]]
    base_cl[f"{z:.1f}"] = {k: float(sum(fi["share"][k][i] * rg[i] for i in nf) / (sum(fi["share"][k][i] for i in nf) or 1e-300)) for k in CASES}
SPLIT = {}
for key in CASES:
    SPLIT[key] = {}
    for which in ("galaxy", "cluster"):
        Fs = {z: (np.array(PR[z][0]["kv"]), seed_mean(z, lambda d, z=z: est(d, key, regime=which, RG=RGs[z]))) for z in ZCOMP}
        Ms = {z: seed_mean(z, lambda d, z=z: est(d, key, what="P3D", regime=which, RG=RGs[z]))[mk] for z in ZCOMP}
        SPLIT[key][which] = dict(flux=dflux(Fs), matter=mat_dchi(Ms, k3[mk]))
RES["regime_split"] = dict(split=SPLIT, base_box_cluster_share_of_nonforced_1h_change=base_cl,
                          note="galaxy = base-box change (non-forced bins + two-halo term, counted below the boundary) + forced bins mostly below FRZ1's v_stiff; cluster = forced bins mostly above. Delta chi^2 is quadratic: the parts do not add.")
for key in CASES:
    P(f"[{FOOT}] regime split {key}: below boundary (galaxy) flux {SPLIT[key]['galaxy']['flux']:.4g}, matter {SPLIT[key]['galaxy']['matter']:.4g}; above (cluster) flux {SPLIT[key]['cluster']['flux']:.4g}, matter {SPLIT[key]['cluster']['matter']:.4g}")
P(f"[{FOOT}] halo-model share of the base box's (non-forced) 1h change at k 3 lying above the boundary: " + json.dumps(base_cl))

# ------------------------------------------------------------------ mutations
MU = {}
def d_sub(parts, z, key, spec, boxes, pre="B|"):
    d = parts[z][0]; return dchi2_sel(rp_only({z: (np.array(d["kv"]), est(d, key, spec, pre=pre, boxes=boxes))}), ALL)
if 2.2 in BR and 0 in BR[2.2]:
    sub = BR[2.2][0]["boxes"]; m1 = {}
    for key in CASES:
        a = d_sub(BR, 2.2, key, "M1_lin", sub); p = d_sub(PR, 2.2, key, "primary", sub)
        m1[key] = dict(M1=a, primary=p, factor=a / p if p > 0 else float("inf"), bites=bool(p > 0 and (a / p >= 1.25 or a / p <= 0.8)))
    MU["M1_saturation_removed"] = dict(rows=m1, bites=all(v["bites"] for v in m1.values()))
else:
    MU["M1_saturation_removed"] = dict(rows={}, bites=False, note="bracket parts at z 2.2 missing")
m2 = {}
for key in CASES:
    a = d_sub(PR, 2.2, key, "primary", None, pre="D2|"); p = d_sub(PR, 2.2, key, "primary", None)
    m2[key] = dict(doubled=a, primary=p, factor=a / p if p > 0 else float("inf"), bites=bool(p > 0 and a / p >= 1.5))
MU["M2_layout_change_doubled"] = dict(rows=m2, bites=all(v["bites"] for v in m2.values()))
RES["mutations"] = MU
for k, v in MU.items():
    P(f"[{FOOT}] MUTATE {k}: " + "; ".join(f"{kk}: {json.dumps(vv, default=float)}" for kk, vv in v["rows"].items()) + f" -> {'bites' if v['bites'] else 'DOES NOT BITE'}", m=True)
mu_case = {key: all(MU[m]["rows"].get(key, {}).get("bites", False) for m in MU) for key in CASES}

# ------------------------------------------------------------------ brackets
BRK = {}; zbr = [z for z in (2.2, 3.0) if z in BR and 0 in BR[z]]
tags = ("lam_x0.5", "lam_x2", "lam_rec", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1")
def d_multi(parts, zs, key, spec):
    Rset = {}
    for z in zs:
        d = parts[z][0]; Rset[z] = (np.array(d["kv"]), est(d, key, spec, boxes=d["boxes"] if parts is not PR else BR[z][0]["boxes"]))
    return dchi2_sel(rp_only(Rset), ALL)
for tag in tags:
    if not zbr: break
    BRK[tag] = {key: rows[key]["flux"] * d_multi(BR, zbr, key, tag) / max(d_multi(PR, zbr, key, "primary"), 1e-300) for key in CASES}
    BRK[tag]["_zs"] = zbr
if 2.2 in CL and 0 in CL[2.2]:
    BRK["clustered"] = {key: rows[key]["flux"] * d_sub(CL, 2.2, key, "primary", CL[2.2][0]["boxes"]) / max(d_sub(PR, 2.2, key, "primary", CL[2.2][0]["boxes"]), 1e-300) for key in CASES}
    BRK["clustered"]["_zs"] = [2.2]
RES["brackets"] = BRK
brk_complete = len(BRK) == 8 and zbr == [2.2, 3.0]
for tag, e in BRK.items():
    P(f"[{FOOT}] bracket {tag} (bins {e['_zs']}): 12-bin estimate " + " / ".join(f"{key} {e[key]:.4g}" for key in CASES))

# ------------------------------------------------------------------ labels
LAB = {}
for key in CASES:
    D = rows[key]["flux"]; ka = ka_case(key)
    if not all(ka.values()) or not mu_case[key]:
        lab = "NO VERDICT (" + ", ".join([f"known answer {k} fails" for k, v in ka.items() if not v] + ([] if mu_case[key] else ["a mutation does not bite"])) + ")"
    else:
        lab = "FOREST ROW FAILS AT FLUX LEVEL" if D > 4 else "FOREST ROW HOLDS AT FLUX LEVEL"
        frag = [t for t, e in BRK.items() if (e[key] > 4) != (D > 4)]
        if frag: lab += ", FRAGILE (" + "; ".join(frag) + ")"
        if KA["e"][key].get("marginal"): lab += ", MARGINAL"
        if not brk_complete: lab += " [brackets incomplete]"
        if D <= 4: lab += "; a hit that awaits an independent re-grade, not a pass of the theory"
    LAB[key] = lab
    P(f"[{FOOT}] LABEL {key}: {lab}")
RES["labels"] = LAB
json.dump(RES, open(os.path.join(HERE, f"frz4_grade_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"frz4_grade_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
json.dump(dict(lane="FRZ4", footing=FOOT, mutations=MU, note=RES["note"]), open(os.path.join(HERE, f"frz4_grade_{FOOT}_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"frz4_grade_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
