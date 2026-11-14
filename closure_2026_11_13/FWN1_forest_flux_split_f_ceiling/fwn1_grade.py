#!/usr/bin/env python3
"""FWN1 grading (FROZEN_CRITERIA.md fab8a8ee0e, sections 4 to 9). Built from FRZ6's frz6_grade.py
(closure_2026_11_13/FRZ6_forest_flux_candidate_graded): the gate is FRZ3R's grading set-up (frz3r_grade.py up to its "parts"
marker, executed read-only: ss1_cosmo.forest_setup / forest_eval, DESI DR1 P1D, 755 points, full covariance); the
estimator, matter projection, known answers (a) to (f), the brackets and the label rule are FRZ6's functions; this lane adds
(g) f = inf identity, (i) identity with FRZ6 at the A1 tolerances, (j1) control S3, (j2) control C graded from FRZ6's parts,
twin T1 doubled in every box, and the ceiling reading. FRZ6's and FRZ4's part files are read read-only.
Usage: nice -n 19 python3 -I -B fwn1_grade.py <footing> -> fwn1_grade_<footing>.json/.out, fwn1_grade_<footing>_MUTATE.json/.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, glob, warnings, copy
warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ3R = os.path.join(REPO, "closure_2026_11_12", "FRZ3R_blind_flux_forest_regrade")
FRZ4 = os.path.join(REPO, "closure_2026_11_13", "FRZ4_forest_flux_graded")
FRZ6 = os.path.join(REPO, "closure_2026_11_13", "FRZ6_forest_flux_candidate_graded")
JNT2 = os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint")
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
src = open(os.path.join(FRZ3R, "frz3r_grade.py")).read(); cut = src.index("# ------------------------------------------------------------------ parts")
g = {"__file__": os.path.join(FRZ3R, "frz3r_grade.py"), "__name__": "frz3r_grade_setup_fwn1"}; _a = sys.argv; sys.argv = ["frz3r_grade.py", FOOT]
exec(compile(src[:cut], "frz3r_grade_setup", "exec"), g); sys.argv = _a
FD, forest_eval, BGB, amp, dchi2_sel, ZB, ALL, bin_sel, md5ok = (g[k] for k in ("FD", "forest_eval", "BGB", "amp", "dchi2_sel", "ZB", "ALL", "bin_sel", "md5ok"))
sys.path.insert(0, HERE); import fwn1_tables as TB
KT = TB.KT
SC = ["S5.00", "S10.00", "Sinf"]                         # this lane's cases
FVAL = {"S5.00": 5.0, "S10.00": 10.0, "Sinf": math.inf}
UC6 = [TB.fkey(f) for f in TB.CASES]                     # f1.00 f2.00 f3.00 finf (FRZ4 / FRZ6 U and C keys)
ZC = [2.2, 2.6, 3.0, 3.4, 3.8, 4.4]
ANCH = (2.2, 3.0, 4.4)
NSEED = 12
TOL_P, TOL_3D = 1e-12, 1e-6                              # criteria 5(i), citing FRZ6's AMENDMENT_A1
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
PR4, BR4, CL4 = load(FRZ4, "primary"), load(FRZ4, "bracket"), load(FRZ4, "clustered")
SP6, FU6, BRS6 = load(FRZ6, "sprim"), load(FRZ6, "full"), load(FRZ6, "bracketS")
INF, FIN, OZ = load(HERE, "inf"), load(HERE, "fin"), load(HERE, "oz")
BRF, CLF = load(HERE, "bracketF"), load(HERE, "clusteredF")
def maxrel(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); z0 = b == 0
    if np.any(a[z0] != 0): return float("inf")
    return float(np.max(np.abs(a[~z0] / b[~z0] - 1))) if np.any(~z0) else 0.0
def cmp_fields(A, B, names, specs, acc):
    """compare spectra of fields `names` under `specs` in box dicts A, B; acc collects per-quantity maxima and counts"""
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

# FRZ6's merged parts (FRZ6's grader merge, copied): FRZ6 sprim parts get FRZ4's U / C forced-box fields
PR6 = {}
for z, ps in SP6.items():
    for s, d in ps.items():
        f4 = PR4.get(z, {}).get(s)
        if f4 is not None:
            for b in d["boxes"]:
                mine = d["forced_boxes"][str(b)]["flux"]["primary"]; fr = f4["forced_boxes"][str(b)]["flux"]["primary"]
                for k in UC6 + ["f0.00"]:
                    nm = "B|" + k
                    if nm not in mine and nm in fr: mine[nm] = fr[nm]
        PR6.setdefault(z, {})[s] = d
for z, ps in FU6.items():
    for s, d in ps.items(): PR6.setdefault(z, {})[s] = d

# this lane's parts: pass 1 + pass 2 at z 2.2 (pass-2 base R must equal pass-1 base R first), oz elsewhere
KI = dict(R_vs_FRZ6=acc0(), R_vs_FRZ6_brackets=acc0(), pass2_base_R=acc0(), parts=[])
PR = {}; MERGE_OK = True; missing_fin = []
for s, d in INF.get(2.2, {}).items():
    d = copy.deepcopy(d); f2 = FIN.get(2.2, {}).get(s)
    if f2 is None: missing_fin.append(s)
    else:
        a = acc0(); cmp_fields(d["base"], f2["base"], ["R"], ["primary", "M1_lin"], a)
        KI["pass2_base_R"]["p"] = max(KI["pass2_base_R"]["p"], a["p"]); KI["pass2_base_R"]["P3D"] = max(KI["pass2_base_R"]["P3D"], a["P3D"]); KI["pass2_base_R"]["n"] += a["n"]
        ok = a["n"] > 0 and a["p"] <= TOL_P and a["P3D"] <= TOL_3D and f2["boxes"] == d["boxes"]
        MERGE_OK &= bool(ok)
        if ok:
            for sp, F in f2["base"]["flux"].items():
                for nm, v in F.items():
                    if nm != "R": d["base"]["flux"][sp][nm] = v
            for b in d["boxes"]:
                for nm, v in f2["forced_boxes"][str(b)]["flux"]["primary"].items(): d["forced_boxes"][str(b)]["flux"]["primary"][nm] = v
    PR.setdefault(2.2, {})[s] = d
for z, ps in OZ.items():
    for s, d in ps.items(): PR.setdefault(z, {})[s] = d
# (i): R of every part vs FRZ6's R at the same (z, seed), base and every forced box, primary and M1_lin
for z, ps in PR.items():
    for s, d in ps.items():
        f6 = PR6.get(z, {}).get(s)
        if f6 is None: continue
        a = acc0()
        if d["boxes"] != f6["boxes"]: KI["parts"].append(dict(z=z, seed=s, boxes_differ=True)); a["p"] = float("inf")
        for bx, A in boxes_of(d):
            B = f6["base"] if bx == "base" else f6["forced_boxes"].get(bx)
            if B is not None: cmp_fields(A, B, ["R"], ["primary", "M1_lin"], a)
        KI["parts"].append(dict(z=z, seed=s, p=a["p"], P3D=a["P3D"], n=a["n"]))
        for w in ("p", "P3D"): KI["R_vs_FRZ6"][w] = max(KI["R_vs_FRZ6"][w], a[w])
        KI["R_vs_FRZ6"]["n"] += a["n"]
for z, ps in BRF.items():
    for s, d in ps.items():
        f6 = BRS6.get(z, {}).get(s)
        if f6 is None: continue
        a = acc0()
        for bx, A in boxes_of(d):
            B = f6["base"] if bx == "base" else f6["forced_boxes"].get(bx)
            if B is not None: cmp_fields(A, B, ["R"], list(A["flux"].keys()), a)
        KI["parts"].append(dict(stage="bracketF", z=z, seed=s, p=a["p"], n=a["n"]))
        for w in ("p", "P3D"): KI["R_vs_FRZ6_brackets"][w] = max(KI["R_vs_FRZ6_brackets"][w], a[w])
        KI["R_vs_FRZ6_brackets"]["n"] += a["n"]
KI["pass_"] = bool(MERGE_OK and acc_ok(KI["R_vs_FRZ6"]) and (KI["R_vs_FRZ6_brackets"]["n"] == 0 or acc_ok(KI["R_vs_FRZ6_brackets"])))
ZCOMP = [z for z in ZC if z in PR and 0 in PR[z]]
ZEST = [z for z in ZB if round(z, 1) not in ZCOMP]
SEEDS22 = sorted(PR.get(2.2, {}).keys()); SEEDS22_FIN = sorted(FIN.get(2.2, {}).keys())
P(f"[{FOOT}] FWN1: computed bins {ZCOMP}; estimated bins {[round(z, 1) for z in ZEST]}; z 2.2 seeds pass 1 {SEEDS22}, pass 2 {SEEDS22_FIN} (frozen {NSEED})")

# ------------------------------------------------------------------ FRZ6's estimator and sets, parametrised by the part collection
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
RES = dict(lane="FWN1", footing=FOOT, computed_bins=ZCOMP, estimated_bins=[round(z, 1) for z in ZEST], seeds_z22=SEEDS22, seeds_z22_pass2=SEEDS22_FIN,
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

# ------------------------------------------------------------------ control C (j2) from FRZ6's parts, and FRZ6's stored S rows
G6 = json.load(open(os.path.join(FRZ6, f"frz6_grade_{FOOT}.json")))
Fc = flux_set(PR6, "finf"); Dc = dchi2_sel(r_points(Fc), ALL); ec = e_stat(PR6, "finf", Dc)
c_ref = G6["rows"]["finf"]["flux"]; se_ref = G6["known_answers"]["e"]["finf"]["SE"]
J2 = dict(D=Dc, SE=ec["SE"], D_FRZ6=c_ref, SE_FRZ6=se_ref, rel_D=abs(Dc / c_ref - 1), rel_SE=abs(ec["SE"] / se_ref - 1), D_minus_2SE=Dc - 2 * ec["SE"],
          seeds=ec["n_seeds"], FRZ6_label_A1=G6["labels_A1"]["finf"])
J2["still_fails"] = bool(J2["D_minus_2SE"] > 4)
J2["pass_"] = bool(J2["rel_D"] <= 1e-6 and J2["rel_SE"] <= 1e-6 and J2["still_fails"])
P(f"[{FOOT}] control C (FRZ6's parts, this grader): D {Dc:.4f} (FRZ6 {c_ref:.4f}, rel {J2['rel_D']:.1e}), SE {ec['SE']:.4f} (FRZ6 {se_ref:.4f}), D - 2 SE {J2['D_minus_2SE']:.2f}: "
  + ("still FAILS" if J2["still_fails"] else "does NOT fail") + f"; known answer (j2) {'PASS' if J2['pass_'] else 'FAIL'}")
for key in SC:
    if rows.get(key): P(f"[{FOOT}] {key} minus C: D {rows[key]['flux'] - Dc:.4f}")

# ------------------------------------------------------------------ known answers
KA = {"i": KI, "j2": J2}
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
# (b) FRZ4's Poisson-only answer on FRZ4's parts (FRZ6's code)
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
# (c0) against the JNT2 chain (fwn1_c0.py)
KA["c0"] = {}
cfile = os.path.join(HERE, f"fwn1_c0_{FOOT}.json")
CC = json.load(open(cfile)) if os.path.exists(cfile) else None
f3_ok = bool(CC is not None and abs(CC["chain_vs_jnt2_f3"]) <= 0.01)
for key in SC:
    if CC is None: KA["c0"][key] = dict(pass_=False, note="chain file missing"); continue
    mn, rf = Drec[key], CC["cases"][key]["dchi2"]
    KA["c0"][key] = dict(mine=mn, chain=rf, chain_f3_vs_JNT2=CC["chain_vs_jnt2_f3"], pass_=bool(f3_ok and (abs(mn / rf - 1) <= 0.01 or abs(mn - rf) <= 0.002)))
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
# (f) split identity (FRZ6's)
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
# (g) f = inf identity: g1 tables, g2 fields at z 2.2 against FRZ6's / FRZ4's B|finf in wholly-below boxes
g1 = {f"{z:.1f}": T[round(z, 1)]["g1"] for z in ZB}
g1ok = all(v["max_abs_below_vs_finf"] == 0.0 and v["max_abs_above_vs_ref"] == 0.0 and v["n_below"] > 0 for v in g1.values())
a = acc0(); nb_ = 0
for s, d in PR.get(2.2, {}).items():
    f6 = PR6.get(2.2, {}).get(s)
    if f6 is None: continue
    fa = d["forced_info"]["frac_above"]
    for b in d["boxes"]:
        if fa[b] == 0.0 and str(b) in f6["forced_boxes"]:
            A = d["forced_boxes"][str(b)]["flux"]["primary"]; B = f6["forced_boxes"][str(b)]["flux"]["primary"]
            if "B|Sinf" in A and "B|finf" in B:
                nb_ += 1
                for w in ("p", "P3D"):
                    if w in A["B|Sinf"] and w in B["B|finf"]:
                        x = maxrel(A["B|Sinf"][w], B["B|finf"][w]); a[w] = max(a[w], x); a["n"] += 1
KA["g"] = dict(g1=g1, g1_pass=bool(g1ok), g2=dict(boxes=nb_, **a), g2_pass=acc_ok(a), pass_=bool(g1ok and acc_ok(a)))
# (j1) control S3 at z 2.2 seeds 0, 1 against FRZ6's B|S3.00
a = acc0(); sj = []
for s in (0, 1):
    d = PR.get(2.2, {}).get(s); f6 = PR6.get(2.2, {}).get(s)
    if d is None or f6 is None or not has(d, "S3.00"): continue
    sj.append(s)
    for bx, A in boxes_of(d):
        B = f6["base"] if bx == "base" else f6["forced_boxes"].get(bx)
        if B is not None: cmp_fields(A, B, ["B|S3.00"], ["primary"], a)
KA["j1"] = dict(seeds=sj, **a, pass_=bool(sj == [0, 1] and acc_ok(a)))
RES["known_answers"] = KA
def ka_case(key):
    k = dict(a=KA["a"]["pass_"], b=KA["b"]["pass_"], c0=KA["c0"][key]["pass_"], c1=KA["c1"][key]["pass_"], d=KA["d"]["pass_"], e=KA["e"][key]["pass_"],
             f=KA["f"]["pass_"], i=KI["pass_"], j1=KA["j1"]["pass_"])
    if key == "Sinf": k["g"] = KA["g"]["pass_"]
    return k
P(f"[{FOOT}] known answer (i) identity with FRZ6 (P1D {TOL_P:g}, P3D {TOL_3D:g}, A1's tolerances): {'PASS' if KI['pass_'] else 'FAIL'}; R vs FRZ6 {json.dumps(KI['R_vs_FRZ6'])}; "
  f"brackets {json.dumps(KI['R_vs_FRZ6_brackets'])}; pass-2 base R vs pass 1 {json.dumps(KI['pass2_base_R'])}; merge ok {MERGE_OK}; pass 2 missing seeds {missing_fin}")
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
P(f"[{FOOT}] known answer (g) f = inf identity: {'PASS' if KA['g']['pass_'] else 'FAIL'}; g1 tables {'PASS' if g1ok else 'FAIL'} " + json.dumps({z: [v['max_abs_below_vs_finf'], v['max_abs_above_vs_ref'], v['n_below'], v['n_above']] for z, v in g1.items()})
  + f"; g2 fields {'PASS' if KA['g']['g2_pass'] else 'FAIL'} {json.dumps(KA['g']['g2'])}")
P(f"[{FOOT}] known answer (j1) control S3 vs FRZ6: {'PASS' if KA['j1']['pass_'] else 'FAIL'} {json.dumps({k: v for k, v in KA['j1'].items() if k != 'pass_'})}")
P(f"[{FOOT}] known answer (j2) control C: {'PASS' if J2['pass_'] else 'FAIL'}")

FI = {}
for z in ZCOMP:
    fi = PR[z][0]["forced_info"]
    FI[f"{z:.1f}"] = dict(n_forced=len(fi["forced"]), forced_share_S=fi["forced_share_S"], nonforced_rare_share_S=fi["nonforced_rare_share_S"], common_share_S=fi["common_share_S"],
                          subset_S_lM=[round(fi["lM_lo"][i], 1) for i in fi["subset_S"]], vstar=fi["vstar"], n_above=fi["n_above"])
    P(f"[{FOOT}] forced set z {z}: new cases' share of the 1h change at k 3 in forced / non-forced rare / common bins: "
      + "; ".join(f"{k} {fi['forced_share_S'][k]:+.3f} / {fi['nonforced_rare_share_S'][k]:+.4f} / {fi['common_share_S'][k]:+.3f}" for k in SC) + f"; S subset log M {FI[f'{z:.1f}']['subset_S_lM']}")
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
rep = {}
if 2.2 in BRF and 0 in BRF[2.2] and 2.2 in PR and 0 in PR[2.2]:
    sb = BRF[2.2][0]["boxes"]
    def d_one(d, key, spec, boxes): return dchi2_sel(rp_only({2.2: (np.array(d["kv"]), est(d, key, spec, boxes=boxes))}), ALL)
    rep["M1_new_subset_seed0"] = {k: d_one(BRF[2.2][0], k, "M1_lin", sb) / max(d_one(PR[2.2][0], k, "primary", sb), 1e-300) for k in SC if has(PR[2.2][0], k)}
MU["reported_factors"] = rep
RES["mutations"] = MU
for k, v in MU.items():
    if k == "reported_factors": P(f"[{FOOT}] MUTATE reported (not graded) factors: {json.dumps(v, default=float)}", m=True); continue
    P(f"[{FOOT}] MUTATE {k}: " + "; ".join(f"{kk}: {json.dumps(vv, default=float)}" for kk, vv in v["rows"].items()), m=True)
mu_case = {key: bool(t1[key]["bites"] and t2[key]["bites"]) for key in SC}

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
    # [brackets incomplete] also when a bracket bin is missing
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
        if not J2["still_fails"]: return "NO VERDICT (control C does not still fail)"
        lab = "FOREST ROW HOLDS AT FLUX LEVEL"
    elif D - 2 * SE > 4: lab = "FOREST ROW FAILS AT FLUX LEVEL"
    else: return f"NO VERDICT (unresolved at {n} seeds: D {D:.3g}, SE {SE:.3g})"
    present = [t for t in brset if t in BRK[key]]
    frag = [t for t in present if (BRK[key][t] > 4) != (D > 4)]
    if frag: lab += ", FRAGILE (" + "; ".join(frag) + ")"
    if len(present) < len(brset): lab += " [brackets incomplete: " + ", ".join(t for t in brset if t not in BRK[key]) + "]"
    if lab.startswith("FOREST ROW HOLDS"): lab += "; a hit that awaits an independent blind re-grade, not a pass of the theory"
    return lab
for key in SC:
    LAB[key] = label(key, FROZEN_BR); LAB_MR[key] = label(key, MR_BR)
    P(f"[{FOOT}] LABEL {key}: {LAB[key]}")
for key in SC:
    P(f"[{FOOT}] measured-range reading (reported, not the label) {key}: {LAB_MR[key]}")
RES["labels"] = LAB; RES["labels_measured_range_reading"] = LAB_MR

# ------------------------------------------------------------------ the ceiling (section 9; reported, never a label)
def qvals(which):
    q = {}
    for key, f in (("S2.00", 2.0), ("S3.00", 3.0)):
        D = G6["rows"][key]["flux"]; SE = G6["known_answers"]["e"][key]["SE"]; q[f] = {"D": D, "hi": D + 2 * SE, "lo": D - 2 * SE}[which]
    for key in SC:
        if rows.get(key) is None: continue
        D = rows[key]["flux"]; SE = KE[key]["SE"]; q[FVAL[key]] = {"D": D, "hi": D + 2 * SE, "lo": D - 2 * SE}[which]
    return q
def ceiling(q):
    fs = sorted(q)
    if q[fs[0]] >= 4: return dict(text=f"f* < {fs[0]:g}", f=None)
    for fa, fb in zip(fs, fs[1:]):
        if q[fa] < 4 <= q[fb]:
            if math.isinf(fb): return dict(text=f"f* > {fa:g}, not interpolable", f=None, pair=[fa, fb])
            if q[fa] <= 0: return dict(text=f"f* between {fa:g} and {fb:g} (lower value <= 0, log form undefined)", f=None, pair=[fa, fb])
            t = (math.log(4) - math.log(q[fa])) / (math.log(q[fb]) - math.log(q[fa])); fstar = math.exp(math.log(fa) + t * (math.log(fb) - math.log(fa)))
            return dict(text=f"f* = {fstar:.2f} (between {fa:g} and {fb:g})", f=fstar, pair=[fa, fb])
    return dict(text="no ceiling up to the largest f graded", f=None)
CEIL = {w: dict(q={str(k): v for k, v in qvals(w).items()}, **ceiling(qvals(w))) for w in ("hi", "D", "lo")}
RES["ceiling"] = CEIL
P(f"[{FOOT}] CEILING (reported, never a label): D + 2 SE = 4 at {CEIL['hi']['text']}; D = 4 at {CEIL['D']['text']}; D - 2 SE = 4 at {CEIL['lo']['text']}")
P(f"[{FOOT}]   Q(f) = D + 2 SE: " + ", ".join(f"f {k}: {v:.3f}" for k, v in CEIL['hi']['q'].items()) + " (f 2, 3 = FRZ6's stored S rows)")
json.dump(RES, open(os.path.join(HERE, f"fwn1_grade_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"fwn1_grade_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
json.dump(dict(lane="FWN1", footing=FOOT, mutations=MU, note=RES["note"]), open(os.path.join(HERE, f"fwn1_grade_{FOOT}_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"fwn1_grade_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
