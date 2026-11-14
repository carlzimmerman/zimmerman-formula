#!/usr/bin/env python3
"""XJ1R grading of part (a) (FROZEN_CRITERIA.md sections 3 to 8). Built from FWN1's fwn1_grade.py (closure_2026_11_13/
FWN1_forest_flux_split_f_ceiling): the gate is FRZ3R's grading set-up (frz3r_grade.py up to its "parts" marker, executed
read-only: ss1_cosmo.forest_setup / forest_eval, DESI DR1 P1D, 755 points, full covariance); the estimator (est), r_points,
dchi2_sel, matter projection, e statistic, known answers (a) to (f), twins T1 / T2, brackets and label rule are FWN1's code.
Changed: cases SEc2, SEc3; control S5.00 in place of control C ((j1) fields vs FWN1's parts, (j2) S5 graded from FWN1's
committed parts); (i) identity against FWN1's parts; the caustic known answers KS1-KS3 (xj1r_rk.json) and the profile known
answers KP1-KP7 (tables) gate the cases; (g) and the ceiling are dropped. FWN1's, FRZ4's and FRZ3R's files are read only.
Usage (the lead, when run_r.done exists; xj1r_rk.json and xj1r_c0_<footing>.json must be on disk):
    nice -n 19 python3 -I -B xj1r_grade.py canonical
    nice -n 19 python3 -I -B xj1r_grade.py alt
-> xj1r_grade_<footing>.json / .out, xj1r_grade_<footing>_MUTATE.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, glob, warnings, copy
warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ3R = os.path.join(REPO, "closure_2026_11_12", "FRZ3R_blind_flux_forest_regrade")
FRZ4 = os.path.join(REPO, "closure_2026_11_13", "FRZ4_forest_flux_graded")
FWN1 = os.path.join(REPO, "closure_2026_11_13", "FWN1_forest_flux_split_f_ceiling")
JNT2 = os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint")
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
src = open(os.path.join(FRZ3R, "frz3r_grade.py")).read(); cut = src.index("# ------------------------------------------------------------------ parts")
g = {"__file__": os.path.join(FRZ3R, "frz3r_grade.py"), "__name__": "frz3r_grade_setup_xj1r"}; _a = sys.argv; sys.argv = ["frz3r_grade.py", FOOT]
exec(compile(src[:cut], "frz3r_grade_setup", "exec"), g); sys.argv = _a
FD, forest_eval, BGB, amp, dchi2_sel, ZB, ALL, bin_sel, md5ok = (g[k] for k in ("FD", "forest_eval", "BGB", "amp", "dchi2_sel", "ZB", "ALL", "bin_sel", "md5ok"))
sys.path.insert(0, HERE); import xj1r_tables as TB
KT = TB.KT
SC = ["SEc2", "SEc3"]                                    # this lane's cases
CTRL = "S5.00"                                           # control
ZC = [2.2, 2.6, 3.0, 3.4, 3.8, 4.4]
ANCH = (2.2, 3.0, 4.4)
NSEED = 12
TOL_P, TOL_3D = 1e-12, 1e-6                              # criteria 5(i), FRZ6's AMENDMENT_A1 tolerances (as FWN1)
OUT, OUTM = [], []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)
def tau_eff(z): return 0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132

# ------------------------------------------------------------------ parts
def load(folder, stage):
    D = {}
    for f in sorted(glob.glob(os.path.join(folder, "parts", f"{stage}_z*_s*_{FOOT}*.json"))):
        d = json.load(open(f)); D.setdefault(round(d["z"], 1), {})[d["seed"]] = d
    return D
PR4 = load(FRZ4, "primary")
INF1, FIN1, OZ1, BRF1, CLF1 = (load(FWN1, s) for s in ("inf", "fin", "oz", "bracketF", "clusteredF"))
PRIM, OZ, BRF, CLF = (load(HERE, s) for s in ("prim", "oz", "bracketF", "clusteredF"))
def maxrel(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); z0 = b == 0
    if np.any(a[z0] != 0): return float("inf")
    return float(np.max(np.abs(a[~z0] / b[~z0] - 1))) if np.any(~z0) else 0.0
def cmp_fields(A, B, names, specs, acc):
    for sp in specs:
        if sp not in A["flux"] or sp not in B["flux"]: continue
        for nm in names:
            if nm in A["flux"][sp] and nm in B["flux"][sp]:
                for w in ("p", "P3D"):
                    if w in A["flux"][sp][nm] and w in B["flux"][sp][nm]:
                        x = maxrel(A["flux"][sp][nm][w], B["flux"][sp][nm][w]); acc[w] = max(acc[w], x); acc["n"] += 1
def boxes_of(d): return [("base", d["base"])] + [(str(b), d["forced_boxes"][str(b)]) for b in d["boxes"]]
def acc0(): return {"p": 0.0, "P3D": 0.0, "n": 0}
def acc_ok(a): return bool(a["n"] > 0 and a["p"] <= TOL_P and a["P3D"] <= TOL_3D)

# FWN1's parts merged exactly as FWN1's grader merges them (pass 1 + pass 2 at z 2.2, oz elsewhere)
PR1 = {}; MERGE1_OK = True
for s, d in INF1.get(2.2, {}).items():
    d = copy.deepcopy(d); f2 = FIN1.get(2.2, {}).get(s)
    if f2 is not None:
        a = acc0(); cmp_fields(d["base"], f2["base"], ["R"], ["primary", "M1_lin"], a)
        ok = a["n"] > 0 and a["p"] <= TOL_P and a["P3D"] <= TOL_3D and f2["boxes"] == d["boxes"]
        MERGE1_OK &= bool(ok)
        if ok:
            for sp, F in f2["base"]["flux"].items():
                for nm, v in F.items():
                    if nm != "R": d["base"]["flux"][sp][nm] = v
            for b in d["boxes"]:
                for nm, v in f2["forced_boxes"][str(b)]["flux"]["primary"].items(): d["forced_boxes"][str(b)]["flux"]["primary"][nm] = v
    else: MERGE1_OK = False
    PR1.setdefault(2.2, {})[s] = d
for z, ps in OZ1.items():
    for s, d in ps.items(): PR1.setdefault(z, {})[s] = d

# this lane's parts
PR = {}
for s, d in PRIM.get(2.2, {}).items(): PR.setdefault(2.2, {})[s] = d
for z, ps in OZ.items():
    for s, d in ps.items(): PR.setdefault(z, {})[s] = d
# (i): R of every part vs FWN1's R at the same (z, seed, box), primary and M1_lin; brackets / clustered on common boxes and specs
KI = dict(R_vs_FWN1=acc0(), R_vs_FWN1_brackets=acc0(), parts=[])
for z, ps in PR.items():
    for s, d in ps.items():
        f1 = PR1.get(z, {}).get(s)
        if f1 is None: KI["parts"].append(dict(z=z, seed=s, missing_in_FWN1=True)); KI["R_vs_FWN1"]["p"] = float("inf"); continue
        a = acc0()
        if d["boxes"] != f1["boxes"]: KI["parts"].append(dict(z=z, seed=s, boxes_differ=True)); a["p"] = float("inf")
        for bx, A in boxes_of(d):
            B = f1["base"] if bx == "base" else f1["forced_boxes"].get(bx)
            if B is not None: cmp_fields(A, B, ["R"], ["primary", "M1_lin"], a)
        KI["parts"].append(dict(z=z, seed=s, p=a["p"], P3D=a["P3D"], n=a["n"]))
        for w in ("p", "P3D"): KI["R_vs_FWN1"][w] = max(KI["R_vs_FWN1"][w], a[w])
        KI["R_vs_FWN1"]["n"] += a["n"]
for mine, theirs, st in ((BRF, BRF1, "bracketF"), (CLF, CLF1, "clusteredF")):
    for z, ps in mine.items():
        for s, d in ps.items():
            f1 = theirs.get(z, {}).get(s)
            if f1 is None: continue
            a = acc0()
            for bx, A in boxes_of(d):
                B = f1["base"] if bx == "base" else f1["forced_boxes"].get(bx)
                if B is not None: cmp_fields(A, B, ["R"], list(A["flux"].keys()), a)
            KI["parts"].append(dict(stage=st, z=z, seed=s, p=a["p"], P3D=a["P3D"], n=a["n"]))
            for w in ("p", "P3D"): KI["R_vs_FWN1_brackets"][w] = max(KI["R_vs_FWN1_brackets"][w], a[w])
            KI["R_vs_FWN1_brackets"]["n"] += a["n"]
KI["pass_"] = bool(acc_ok(KI["R_vs_FWN1"]) and (KI["R_vs_FWN1_brackets"]["n"] == 0 or acc_ok(KI["R_vs_FWN1_brackets"])))
ZCOMP = [z for z in ZC if z in PR and 0 in PR[z]]
ZEST = [z for z in ZB if round(z, 1) not in ZCOMP]
SEEDS22 = sorted(PR.get(2.2, {}).keys())
P(f"[{FOOT}] XJ1R: computed bins {ZCOMP}; estimated bins {[round(z, 1) for z in ZEST]}; z 2.2 seeds {SEEDS22} (frozen {NSEED})")

# ------------------------------------------------------------------ FWN1's estimator and sets (unchanged)
def est(d, key, spec="primary", what="p", pre="B|", boxes=None, pre_base=None):
    F = d["base"]["flux"][spec]; XRb = np.array(F["R"][what]); XR = XRb.copy()
    dX = np.array(F[(pre_base or pre) + key][what]) - XRb
    use = d["boxes"] if boxes is None else [b for b in d["boxes"] if b in boxes]
    for ib in use:
        fb = d["forced_boxes"][str(ib)]; Fb = fb["flux"][spec]; E = fb["E"]
        XR = XR + E * (np.array(Fb["R"][what]) - XRb)
        dX = dX + E * (np.array(Fb[pre + key][what]) - np.array(Fb["R"][what]))
    return 1.0 + dX / XR
def has(d, key, pre="B|"): return (pre + key) in d["base"]["flux"]["primary"]
def r_points(Rz_kv):
    r = np.ones(FD["NB"])
    for z in ZB:
        s_ = FD["zs"] == round(z, 2); ks = FD["ks"][s_]; zz = round(z, 1)
        if zz in Rz_kv:
            kv, R = Rz_kv[zz]; r[s_] = np.interp(ks, kv[1:], R[1:])
        else:
            lo = max([c for c in Rz_kv if c < zz], default=None); hi = min([c for c in Rz_kv if c > zz], default=None)
            if lo is None or hi is None: continue
            a = np.interp(ks, Rz_kv[lo][0][1:], Rz_kv[lo][1][1:]); b = np.interp(ks, Rz_kv[hi][0][1:], Rz_kv[hi][1][1:])
            r[s_] = a + (b - a) * (zz - lo) / (hi - lo)
    return r
def rp_only(Rset):
    r = np.ones(FD["NB"])
    for z, (kv, R) in Rset.items():
        s_ = np.round(FD["zs"], 1) == z; r[s_] = np.interp(FD["ks"][s_], kv[1:], R[1:])
    return r
def mat_dchi(Rk, k, only=None):
    full = {}
    for z in ZB:
        zz = round(z, 1)
        if zz in Rk: full[z] = Rk[zz]
        else:
            lo = max([c for c in Rk if c < zz], default=None); hi = min([c for c in Rk if c > zz], default=None)
            full[z] = Rk[lo] + (Rk[hi] - Rk[lo]) * (zz - lo) / (hi - lo) if (lo is not None and hi is not None) else np.ones_like(k)
        if only is not None and abs(z - only) > 1e-6: full[z] = np.ones_like(k)
    return float(forest_eval(FD, BGB, amp(full, k))["dchi2"])
def zcomp_of(C): return [z for z in ZC if z in C and 0 in C[z]]
def seeds_with(C, z, key): return [s for s in sorted(C[z]) if has(C[z][s], key)]
def seed_mean(C, z, key, fn): return np.mean([fn(C[z][s]) for s in seeds_with(C, z, key)], 0)
def flux_set(C, key, fn=None):
    fn = fn or (lambda d: est(d, key)); return {z: (np.array(C[z][0]["kv"]), seed_mean(C, z, key, fn)) for z in zcomp_of(C)}
def mat_set(C, key):
    zc = zcomp_of(C); kok = np.all([np.array(C[z][s]["base"]["flux"]["primary"]["R"]["P3D"]) > 0 for z in zc for s in C[z]], 0)
    k = np.array(C[zc[0]][0]["k3d"]); m = (k <= 10) & kok
    return {z: seed_mean(C, z, key, lambda d: est(d, key, what="P3D"))[m] for z in zc}, k[m]
def e_stat(C, key, D):
    ss = seeds_with(C, 2.2, key); n = len(ss); kv = np.array(C[2.2][ss[0]]["kv"])
    Rs = [est(C[2.2][s], key) for s in ss]; Rb = np.mean(Rs, 0)
    N22 = sum(dchi2_sel(rp_only({2.2: (kv, 1.0 + (R - Rb))}), ALL) for R in Rs) / (n * (n - 1))
    D22 = dchi2_sel(rp_only({2.2: (kv, Rb)}), ALL); N12 = D * N22 / D22 if D22 > 0 else float("inf")
    return dict(n_seeds=n, seeds=ss, N22=N22, D22=D22, N12=N12, SE=2 * math.sqrt(D * N12) + N12)

# ------------------------------------------------------------------ halo model per case
T = {round(z, 1): TB.tables(z)[FOOT] for z in ZB}
KKF = np.geomspace(1e-3, 10.0, 260)
def hm_D(key, q, only=None):
    Rz = {}
    for z in ZB:
        Rz[z] = np.interp(np.log(KKF), np.log(KT[1:]), T[round(z, 1)]["spec"][key][q][1:])
        if only is not None and abs(z - only) > 1e-6: Rz[z] = np.ones_like(KKF)
    return float(forest_eval(FD, BGB, amp(Rz, KKF))["dchi2"])
Drec = {k: hm_D(k, "Rcold") for k in SC}; Dta = {k: hm_D(k, "Rta") for k in SC}

# ------------------------------------------------------------------ primary table
RES = dict(lane="XJ1R", footing=FOOT, computed_bins=ZCOMP, estimated_bins=[round(z, 1) for z in ZEST], seeds_z22=SEEDS22,
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
rows = {}; RPTS = {}; KE = {}
BINS_OK = ZCOMP == ZC
for key in SC:
    if not (2.2 in PR and seeds_with(PR, 2.2, key)) or not all(has(PR[z][0], key) for z in ZCOMP):
        rows[key] = None; continue
    Fs = flux_set(PR, key); RPTS[key] = r_points(Fs); Df = dchi2_sel(RPTS[key], ALL); Ms, k3 = mat_set(PR, key); Dm = mat_dchi(Ms, k3)
    perbin = {f"{z:.1f}" + ("" if round(z, 1) in ZCOMP else " (estimated)"): dchi2_sel(RPTS[key], bin_sel(z)) for z in ZB}
    ss = seeds_with(PR, 2.2, key)
    rows[key] = dict(flux=Df, matter=Dm, ratio=Df / Dm if Dm > 0 else None, D_ta=Dta[key], D_rec=Drec[key], c1_ratio=Dm / Dta[key] if Dta[key] > 0 else None,
                     per_bin=perbin, R_F={f"{z:.1f}": [float(np.interp(x, Fs[z][0][1:], Fs[z][1][1:])) for x in (0.003, 0.005, 0.01, 0.02, 0.03)] for z in ZCOMP},
                     z22_single_seed=[dchi2_sel(rp_only({2.2: (np.array(PR[2.2][s]["kv"]), est(PR[2.2][s], key))}), ALL) for s in ss])
    KE[key] = e_stat(PR, key, Df) if len(ss) >= 2 else dict(n_seeds=len(ss), SE=float("inf"), N12=float("inf"))
RES["rows"] = rows; RES["r_points"] = {k: v.tolist() for k, v in RPTS.items()}
P(f"[{FOOT}] case | flux dchi2 (12 bins) | SE | D + 2 SE | D - 2 SE | matter, same fields | D_ta | matter/D_ta | D_rec")
for key, r in rows.items():
    if r is None: P(f"[{FOOT}] {key}: fields missing"); continue
    e = KE[key]
    P(f"[{FOOT}] {key:6} | {r['flux']:10.4f} | {e['SE']:8.4f} | {r['flux'] + 2 * e['SE']:10.4f} | {r['flux'] - 2 * e['SE']:10.4f} | {r['matter']:10.4f} | {r['D_ta']:9.4f} | {(r['c1_ratio'] or 0):.3f} | {r['D_rec']:9.4f}")
for key, r in rows.items():
    if r is None: continue
    P(f"[{FOOT}] per bin {key}: " + " ".join(f"{z}:{v:.4g}" for z, v in r["per_bin"].items()))
    P(f"[{FOOT}]   {key} z 2.2 single-seed dchi2 (seeds {seeds_with(PR, 2.2, key)}): " + " ".join(f"{v:.4g}" for v in r["z22_single_seed"]))
    for z in ZCOMP:
        P(f"[{FOOT}]   {key} z {z}: R_F at 0.003/0.005/0.01/0.02/0.03 s/km " + "/".join(f"{v:.5f}" for v in r["R_F"][f"{z:.1f}"]))

# ------------------------------------------------------------------ control S5 (j2) graded from FWN1's committed parts
G1 = json.load(open(os.path.join(FWN1, f"fwn1_grade_{FOOT}.json")))
Fc = flux_set(PR1, CTRL); Dc = dchi2_sel(r_points(Fc), ALL); ec = e_stat(PR1, CTRL, Dc)
c_ref = G1["rows"][CTRL]["flux"]; se_ref = G1["known_answers"]["e"][CTRL]["SE"]
J2 = dict(D=Dc, SE=ec["SE"], D_FWN1=c_ref, SE_FWN1=se_ref, rel_D=abs(Dc / c_ref - 1), rel_SE=abs(ec["SE"] / se_ref - 1),
          D_minus_2SE=Dc - 2 * ec["SE"], seeds=ec["n_seeds"], FWN1_label=G1["labels"][CTRL], merge_ok=bool(MERGE1_OK))
J2["D_above_gate"] = bool(Dc > 4)
J2["pass_"] = bool(MERGE1_OK and J2["rel_D"] <= 1e-6 and J2["rel_SE"] <= 1e-6 and J2["D_above_gate"])
P(f"[{FOOT}] control S5 (FWN1's parts, this grader): D {Dc:.4f} (FWN1 {c_ref:.4f}, rel {J2['rel_D']:.1e}), SE {ec['SE']:.4f} (FWN1 {se_ref:.4f}, rel {J2['rel_SE']:.1e}), "
  f"D - 2 SE {J2['D_minus_2SE']:.2f}; D > 4: {J2['D_above_gate']}; known answer (j2) {'PASS' if J2['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ known answers
KA = {"i": KI, "j2": J2}
# caustics KS1-KS3 (xj1r_rk.json)
RKJ = os.path.join(HERE, "xj1r_rk.json")
KSJ = json.load(open(RKJ))["known_answers"] if os.path.exists(RKJ) else None
KA["KS"] = dict(file=bool(KSJ is not None), **({k: v["pass_"] for k, v in KSJ.items()} if KSJ else {}))
KA["KS"]["pass_"] = bool(KSJ is not None and all(v["pass_"] for v in KSJ.values()))
# profiles KP1-KP7 (tables, every z bin)
KP = {}
for key in SC:
    per = {f"{z:.1f}": T[round(z, 1)]["kp"]["KP"][key] for z in ZB}
    KP[key] = dict(per_z=per, KP5={f"{z:.1f}": T[round(z, 1)]["kp"]["KP5"] for z in ZB}, KP7={f"{z:.1f}": T[round(z, 1)]["kp"]["KP7"] for z in ZB},
                   pass_=bool(all(v["pass_"] for v in per.values())))
KA["KP"] = KP
# (a)
amax = 0.0; nbox = 0
for z in ANCH:
    if z not in PR or 0 not in PR[z]: continue
    for bx in [PR[z][0]["base"]] + list(PR[z][0]["forced_boxes"].values()):
        F = bx["flux"]["primary"]
        if "B|f0.00" in F: amax = max(amax, maxrel(F["B|f0.00"]["p"], F["R"]["p"])); nbox += 1
za = [z for z in ANCH if z in PR and 0 in PR[z] and has(PR[z][0], "f0.00")]
Da = dchi2_sel(rp_only({z: (np.array(PR[z][0]["kv"]), est(PR[z][0], "f0.00")) for z in za}), ALL) if za else float("inf")
KA["a"] = dict(max_rel_box=amax, boxes=nbox, bins=za, dchi2_f0=Da, md5ok=md5ok, pass_=bool(nbox > 0 and len(za) == 3 and amax <= 1e-12 and Da <= 1e-12 and md5ok))
# (b) FRZ4's Poisson-only answer on FRZ4's parts (FWN1's code)
bmax = 0.0; mine, frz, mineM, frzM = {}, {}, {}, {}; kf = None
for z in [z for z in ZC if z in PR4]:
    arr, arr2, a3, b3 = [], [], [], []
    for s, d in PR4[z].items():
        fr = json.load(open(os.path.join(FRZ3R, "parts", f"turn_z{z:.1f}_s{s}_{FOOT}_N384.json"))); F = d["base"]["flux"]["primary"]
        bmax = max(bmax, maxrel(F["Rall"]["p"], fr["flux"]["primary"]["R"]["p"]), maxrel(F["BPall|finf"]["p"], fr["flux"]["primary"]["B"]["p"]))
        arr.append(np.array(F["BPall|finf"]["p"]) / np.array(F["Rall"]["p"])); arr2.append(np.array(fr["flux"]["primary"]["B"]["p"]) / np.array(fr["flux"]["primary"]["R"]["p"]))
        a3.append(np.array(F["BPall|finf"]["P3D"]) / np.array(F["Rall"]["P3D"])); kf = np.array(fr["P3D"]["k"]); b3.append(np.array(fr["P3D"]["B"]) / np.array(fr["P3D"]["R"]))
    mine[z] = (np.array(PR4[z][0]["kv"]), np.mean(arr, 0)); frz[z] = (np.array(fr["kv"]), np.mean(arr2, 0)); mineM[z] = np.mean(a3, 0); frzM[z] = np.mean(b3, 0)
Db_m, Db_f = dchi2_sel(rp_only(mine), ALL), dchi2_sel(rp_only(frz), ALL)
z4 = [z for z in ZC if z in PR4]
KOK4 = np.all([np.array(PR4[z][s]["base"]["flux"]["primary"]["R"]["P3D"]) > 0 for z in z4 for s in PR4[z]], 0)
k3 = np.array(PR4[z4[0]][0]["k3d"]); mk = (k3 <= 10) & KOK4; mkf = (kf <= 10) & np.all([np.isfinite(v) for v in frzM.values()], 0)
def mat_only(Rk, k):
    full = {z: (Rk[round(z, 1)] if round(z, 1) in Rk else np.ones_like(k)) for z in ZB}; return float(forest_eval(FD, BGB, amp(full, k))["dchi2"])
Dbm_m = mat_only({z: v[mk] for z, v in mineM.items()}, k3[mk]); Dbm_f = mat_only({z: v[mkf] for z, v in frzM.items()}, kf[mkf])
KA["b"] = dict(max_rel_part=bmax, flux_computed_bins=[Db_m, Db_f], matter_computed_bins=[Dbm_m, Dbm_f],
               pass_=bool(bmax <= 1e-4 and abs(Db_m / Db_f - 1) <= 0.01 and abs(Dbm_m / Dbm_f - 1) <= 0.01))
# (c0) against the independent chain (xj1r_c0.py)
KA["c0"] = {}
cfile = os.path.join(HERE, f"xj1r_c0_{FOOT}.json")
CC = json.load(open(cfile)) if os.path.exists(cfile) else None
s5_ok = bool(CC is not None and abs(CC["chain_S5_vs_fwn1_rel"]) <= 1e-9)
for key in SC:
    if CC is None: KA["c0"][key] = dict(pass_=False, note="chain file missing"); continue
    mn, rf = Drec[key], CC["cases"][key]["dchi2"]
    KA["c0"][key] = dict(mine=mn, chain=rf, chain_S5_vs_FWN1=CC["chain_S5_vs_fwn1_rel"], t_by_z=CC["cases"][key]["t_min_median_max_by_z"],
                         pass_=bool(s5_ok and (abs(mn / rf - 1) <= 0.01 or abs(mn - rf) <= 0.002)))
# (c1)
KA["c1"] = {}
for key in SC:
    if rows.get(key) is None: KA["c1"][key] = dict(pass_=False, note="fields missing"); continue
    Ms, k3m = mat_set(PR, key); Dm = rows[key]["matter"]; pb = {}
    okc = (0.67 <= Dm / Dta[key] <= 1.5) if Dta[key] >= 1 else (Dm <= 1.0)
    for z in ZCOMP:
        h = hm_D(key, "Rta", only=z)
        if h >= 1.0:
            rz = mat_dchi(Ms, k3m, only=z); pb[f"{z:.1f}"] = dict(realised=rz, halo_model=h, ratio=rz / h, ok=bool(0.5 <= rz / h <= 2.0)); okc &= pb[f"{z:.1f}"]["ok"]
        else:
            pb[f"{z:.1f}"] = dict(halo_model=h, checked=False)
    KA["c1"][key] = dict(realised=Dm, halo_model_ta=Dta[key], rule="ratio 0.67-1.5" if Dta[key] >= 1 else "D_ta < 1: D_mat <= 1", per_bin=pb, pass_=bool(okc))
# (d)
dmax = 0.0
for coll in (PR, BRF, CLF):
    for z, ps in coll.items():
        for d in ps.values():
            for bx in [d["base"]] + list(d["forced_boxes"].values()):
                for sp, fields in bx["flux"].items():
                    sF = {"tau_x0.9": 0.9, "tau_x1.1": 1.1}.get(sp, 1.0)
                    for nm, v in fields.items(): dmax = max(dmax, abs(v["meanF"] - math.exp(-sF * tau_eff(z))))
KA["d"] = dict(max_abs=dmax, pass_=bool(dmax <= 1e-4))
# (e)
KA["e"] = {}
for key in SC:
    if rows.get(key) is None: KA["e"][key] = dict(pass_=False, note="fields missing"); continue
    e = KE[key]; D = rows[key]["flux"]
    KA["e"][key] = dict(e, pass_=bool(e["n_seeds"] >= NSEED and (e["N12"] <= 0.1 * D or e["N12"] <= 0.05)), pass_at_reached_seeds=bool(e["N12"] <= 0.1 * D or e["N12"] <= 0.05))
# (f) split identity and membership
fmax = 0.0; fn = 0; memb = {}
JM = json.load(open(os.path.join(JNT2, "jnt2_hm.json")))["membership"][FOOT]
for coll in (PR, BRF, CLF):
    for z, ps in coll.items():
        for d in ps.values():
            fa = d["forced_info"]["frac_above"]
            for b in d["boxes"]:
                if fa[b] >= 1.0:
                    for sp, F in d["forced_boxes"][str(b)]["flux"].items():
                        for key in SC:
                            if "B|" + key in F: fmax = max(fmax, maxrel(F["B|" + key]["p"], F["R"]["p"])); fn += 1
            memb[f"{z:.1f}"] = (d["forced_info"]["n_above"], JM[f"{z:.1f}"]["n_above"])
KA["f"] = dict(max_rel_above_boxes=fmax, fields=fn, membership_mine_vs_JNT2=memb,
               pass_=bool(fn > 0 and fmax <= 1e-12 and all(a == b for a, b in memb.values()) and all(f"{z:.1f}" in memb for z in ANCH)))
# (j1) control S5 fields at z 2.2 seeds 0, 1 against FWN1's B|S5.00
a = acc0(); sj = []
for s in (0, 1):
    d = PR.get(2.2, {}).get(s); f1 = PR1.get(2.2, {}).get(s)
    if d is None or f1 is None or not has(d, CTRL): continue
    sj.append(s)
    for bx, A in boxes_of(d):
        B = f1["base"] if bx == "base" else f1["forced_boxes"].get(bx)
        if B is not None: cmp_fields(A, B, ["B|" + CTRL], ["primary"], a)
KA["j1"] = dict(seeds=sj, **a, pass_=bool(sj == [0, 1] and acc_ok(a)))
RES["known_answers"] = KA
def ka_case(key):
    return dict(KS=KA["KS"]["pass_"], KP=KA["KP"][key]["pass_"], a=KA["a"]["pass_"], b=KA["b"]["pass_"], c0=KA["c0"][key]["pass_"], c1=KA["c1"][key]["pass_"],
                d=KA["d"]["pass_"], e=KA["e"][key]["pass_"], f=KA["f"]["pass_"], i=KI["pass_"], j1=KA["j1"]["pass_"])
P(f"[{FOOT}] known answers KS1-KS3 (caustics, xj1r_rk.json): {'PASS' if KA['KS']['pass_'] else 'FAIL'} {json.dumps(KA['KS'])}")
for key in SC:
    kp = KA["KP"][key]
    P(f"[{FOOT}] known answers KP1-KP7 {key}: {'PASS' if kp['pass_'] else 'FAIL'}; per z (KP1 max|M-M_B| inside, KP2, KP3, min t, median t, max t, R_set/r_ta median, capped): "
      + "; ".join(f"{z}: {v['KP1_max_abs_inside']:.0e}/{v['KP2_max_rel_Mta']:.0e}/{v['KP3_min_diff_over_Mta']:.0e}/{v['t_min']:.4f}/{v['t_median']:.4f}/{v['t_max']:.4f}/{(v['rset_over_rta_median'] or 0):.3f}/{v['n_capped']}" for z, v in kp["per_z"].items()))
P(f"[{FOOT}] known answer (i) identity with FWN1 (P1D {TOL_P:g}, P3D {TOL_3D:g}): {'PASS' if KI['pass_'] else 'FAIL'}; R vs FWN1 {json.dumps(KI['R_vs_FWN1'])}; brackets/clustered {json.dumps(KI['R_vs_FWN1_brackets'])}")
P(f"[{FOOT}] known answer (a): {'PASS' if KA['a']['pass_'] else 'FAIL'} max |B_f0/R - 1| {amax:.2e} over {nbox} boxes (bins {za}); dchi2 at f 0 {Da:.2e}; md5 {md5ok}")
P(f"[{FOOT}] known answer (b): {'PASS' if KA['b']['pass_'] else 'FAIL'} max rel {bmax:.2e}; flux {Db_m:.3f} vs FRZ3R {Db_f:.3f}; matter {Dbm_m:.2f} vs {Dbm_f:.2f}")
for key in SC:
    c0 = KA["c0"][key]; c1 = KA["c1"][key]; e = KA["e"][key]
    P(f"[{FOOT}] known answer (c0) {key}: {'PASS' if c0['pass_'] else 'FAIL'} " + json.dumps({k: v for k, v in c0.items() if k != 'pass_'}, default=float))
    if "realised" in c1:
        P(f"[{FOOT}] known answer (c1) {key}: {'PASS' if c1['pass_'] else 'FAIL'} realised {c1['realised']:.4g} / halo model {c1['halo_model_ta']:.4g} ({c1['rule']}); per bin "
          + "; ".join(f"{z}: " + (f"{v['realised']:.3g}/{v['halo_model']:.3g}={v['ratio']:.2f}{'' if v['ok'] else ' OUT'}" if v.get("checked", True) else f"hm {v['halo_model']:.3g} (<1)") for z, v in c1["per_bin"].items()))
    P(f"[{FOOT}] known answer (e) {key}: {'PASS' if e['pass_'] else 'FAIL'} " + json.dumps({k: v for k, v in e.items() if k != 'pass_'}, default=float))
P(f"[{FOOT}] known answer (d): {'PASS' if KA['d']['pass_'] else 'FAIL'} max |<F> - target| {dmax:.2e}")
P(f"[{FOOT}] known answer (f) split identity: {'PASS' if KA['f']['pass_'] else 'FAIL'} max rel {fmax:.2e} over {fn} wholly-above spectra; membership mine vs JNT2 {json.dumps(memb)}")
P(f"[{FOOT}] known answer (j1) control S5 fields vs FWN1: {'PASS' if KA['j1']['pass_'] else 'FAIL'} {json.dumps({k: v for k, v in KA['j1'].items() if k != 'pass_'})}")
P(f"[{FOOT}] known answer (j2) control S5 graded: {'PASS' if J2['pass_'] else 'FAIL'}")
FI = {}
for z in ZCOMP:
    fi = PR[z][0]["forced_info"]
    FI[f"{z:.1f}"] = dict(n_forced=len(fi["forced"]), forced_share_S=fi["forced_share_S"], nonforced_rare_share_S=fi["nonforced_rare_share_S"], common_share_S=fi["common_share_S"],
                          subset_S_lM=[round(fi["lM_lo"][i], 1) for i in fi["subset_S"]], vstar=fi["vstar"], n_above=fi["n_above"])
    P(f"[{FOOT}] forced set z {z}: cases' share of the 1h change at k 3 in forced / non-forced rare / common bins: "
      + "; ".join(f"{k} {fi['forced_share_S'][k]:+.3f} / {fi['nonforced_rare_share_S'][k]:+.4f} / {fi['common_share_S'][k]:+.3f}" for k in SC) + f"; subset log M {FI[f'{z:.1f}']['subset_S_lM']}")
RES["forced_sets_S"] = FI

# ------------------------------------------------------------------ twins (12 seeds at z 2.2)
MU = {}
def z22(key, fn):
    ss = seeds_with(PR, 2.2, key); kv = np.array(PR[2.2][ss[0]]["kv"]); return dchi2_sel(rp_only({2.2: (kv, np.mean([fn(PR[2.2][s]) for s in ss], 0))}), ALL)
t1 = {}; t2 = {}
for key in SC:
    ss = seeds_with(PR, 2.2, key) if 2.2 in PR else []
    have = len(ss) > 0 and all(has(PR[2.2][s], key, "D2|") and all(("D2|" + key) in PR[2.2][s]["forced_boxes"][str(b)]["flux"]["primary"] for b in PR[2.2][s]["boxes"])
                                and ("B|" + key) in PR[2.2][s]["base"]["flux"].get("M1_lin", {}) for s in ss)
    if not have: t1[key] = t2[key] = dict(bites=False, note="twin fields missing"); continue
    p = z22(key, lambda d: est(d, key)); a_ = z22(key, lambda d: est(d, key, pre="D2|"))
    t1[key] = dict(doubled_every_box=a_, primary=p, factor=a_ / p if p > 0 else float("inf"), bites=bool(p > 0 and a_ / p >= 1.5), seeds=ss)
    pb = z22(key, lambda d: est(d, key, boxes=[])); mb = z22(key, lambda d: est(d, key, spec="M1_lin", boxes=[]))
    t2[key] = dict(M1=mb, primary_base_only=pb, factor=mb / pb if pb > 0 else float("inf"), bites=bool(pb > 0 and (mb / pb >= 1.25 or mb / pb <= 0.8)), seeds=ss)
MU["T1_change_doubled_every_box"] = dict(rows=t1); MU["T2_base_saturation_removed"] = dict(rows=t2)
RES["mutations"] = MU
for k, v in MU.items():
    P(f"[{FOOT}] MUTATE {k}: " + "; ".join(f"{kk}: {json.dumps(vv, default=float)}" for kk, vv in v["rows"].items()), m=True)
mu_case = {key: bool(t1[key]["bites"] and t2[key]["bites"]) for key in SC}
P(f"[{FOOT}] twins bite (T1 and T2): {json.dumps(mu_case)}")

# ------------------------------------------------------------------ brackets (seed 0)
def d_multi(BRc, zs, key, spec):
    Rb_, Rp_ = {}, {}
    for z in zs:
        d = BRc[z][0]; sub = d["boxes"]
        Rb_[z] = (np.array(d["kv"]), est(d, key, spec, boxes=sub)); Rp_[z] = (np.array(PR[z][0]["kv"]), est(PR[z][0], key, "primary", boxes=sub))
    return dchi2_sel(rp_only(Rb_), ALL), dchi2_sel(rp_only(Rp_), ALL)
TAGS = ("lam_x0.5", "lam_x2", "lam_rec", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1")
BRK = {k: {} for k in SC}; BRZ = {}
for key in SC:
    if rows.get(key) is None: continue
    zs = [z for z in (2.2, 3.0) if z in BRF and 0 in BRF[z] and z in PR and 0 in PR[z]]; BRZ[key] = zs
    for tag in TAGS + ("lam_mr_lo", "lam_mr_hi"):
        if zs: b_, p_ = d_multi(BRF, zs, key, tag); BRK[key][tag] = rows[key]["flux"] * b_ / max(p_, 1e-300)
    if 2.2 in CLF and 0 in CLF[2.2]:
        b_, p_ = d_multi(CLF, [2.2], key, "primary"); BRK[key]["clustered"] = rows[key]["flux"] * b_ / max(p_, 1e-300)
    if zs != [2.2, 3.0]:
        for tag in TAGS + ("lam_mr_lo", "lam_mr_hi"): BRK[key].pop(tag, None)
RES["brackets"] = BRK
for key in SC:
    P(f"[{FOOT}] brackets {key} (bins {BRZ.get(key)}; 12-bin estimates): " + "; ".join(f"{t} {v:.4g}" for t, v in BRK[key].items()))

# ------------------------------------------------------------------ labels (criteria section 8)
LAB = {}; LAB_MR = {}
FROZEN_BR = TAGS + ("clustered",)
MR_BR = ("lam_mr_lo", "lam_mr_hi", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1", "clustered")
def label(key, brset):
    if rows.get(key) is None: return "NO VERDICT (fields missing)"
    D = rows[key]["flux"]; ka = ka_case(key); SE = KE[key].get("SE", float("inf")); n = KE[key].get("n_seeds", 0)
    bad = [f"known answer {k} fails" for k, v in ka.items() if not v] + ([] if mu_case[key] else ["a twin does not bite"])
    if n < NSEED: bad.append(f"seed count not reached ({n} of {NSEED})")
    if not BINS_OK: bad.append(f"bins missing (computed {ZCOMP})")
    if bad: return "NO VERDICT (" + ", ".join(bad) + ")"
    if D + 2 * SE < 4:
        if not J2["pass_"]: return "NO VERDICT (control S5 does not pass j2)"
        lab = "FOREST ROW HOLDS AT FLUX LEVEL"
    elif D - 2 * SE > 4: lab = "FOREST ROW FAILS AT FLUX LEVEL"
    else: return f"NO VERDICT (unresolved at {n} seeds: D {D:.3g}, SE {SE:.3g})"
    present = [t for t in brset if t in BRK[key]]
    frag = [t for t in present if (BRK[key][t] > 4) != (D > 4)]
    if frag: lab += ", FRAGILE (" + "; ".join(frag) + ")"
    if len(present) < len(brset): lab += " [brackets incomplete: " + ", ".join(t for t in brset if t not in BRK[key]) + "]"
    return lab
for key in SC:
    LAB[key] = label(key, FROZEN_BR); LAB_MR[key] = label(key, MR_BR)
    P(f"[{FOOT}] LABEL (a) {key}: {LAB[key]}")
for key in SC:
    P(f"[{FOOT}] measured-range reading (reported, not the label) {key}: {LAB_MR[key]}")
RES["labels"] = LAB; RES["labels_measured_range_reading"] = LAB_MR
json.dump(RES, open(os.path.join(HERE, f"xj1r_grade_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"xj1r_grade_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
json.dump(dict(lane="XJ1R", footing=FOOT, mutations=MU, note=RES["note"]), open(os.path.join(HERE, f"xj1r_grade_{FOOT}_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"xj1r_grade_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
