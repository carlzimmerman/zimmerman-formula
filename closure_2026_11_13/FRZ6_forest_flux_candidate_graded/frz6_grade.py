#!/usr/bin/env python3
"""FRZ6 grading (FROZEN_CRITERIA.md, sections 4 to 9). Built from FRZ4's frz4_grade.py (closure_2026_11_13/FRZ4_forest_flux_graded):
the gate is FRZ3R's grading set-up (frz3r_grade.py up to its "parts" marker, executed read-only: the record's
ss1_cosmo.forest_setup / forest_eval, DESI DR1 P1D, full covariance); estimator, matter projection, known answers (a) to (d)
and brackets are FRZ4's functions; (e) is generalised to n seeds; known answers (f) split identity and (i) identity with FRZ4,
twins T1 / T2 and the label rule are this lane's frozen additions. FRZ4's part files are read read-only.
Usage: nice -n 19 python3 -I -B frz6_grade.py <footing> -> frz6_grade_<footing>.json/.out, frz6_grade_<footing>_MUTATE.json/.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, glob, warnings
warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ3R = os.path.join(REPO, "closure_2026_11_12", "FRZ3R_blind_flux_forest_regrade")
SRF1 = os.path.join(REPO, "closure_2026_11_12", "SRF1_settled_radius_flux_window")
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
FRZ4 = os.path.join(REPO, "closure_2026_11_13", "FRZ4_forest_flux_graded")
JNT2 = os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint")
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
src = open(os.path.join(FRZ3R, "frz3r_grade.py")).read(); cut = src.index("# ------------------------------------------------------------------ parts")
g = {"__file__": os.path.join(FRZ3R, "frz3r_grade.py"), "__name__": "frz3r_grade_setup_frz6"}; _a = sys.argv; sys.argv = ["frz3r_grade.py", FOOT]
exec(compile(src[:cut], "frz3r_grade_setup", "exec"), g); sys.argv = _a
FD, forest_eval, BGB, amp, dchi2_sel, ZB, ALL, bin_sel, md5ok = (g[k] for k in ("FD", "forest_eval", "BGB", "amp", "dchi2_sel", "ZB", "ALL", "bin_sel", "md5ok"))
sys.path.insert(0, HERE); import frz6_tables as TB
KT = TB.KT; fk_ = TB.fkey
UC = [fk_(f) for f in TB.CASES]                          # f1.00 f2.00 f3.00 finf
SC = list(TB.SKEYS)                                      # S1.25 S2.00 S3.00
CASES = UC + SC
ZC = [2.2, 2.6, 3.0, 3.4, 3.8, 4.4]
ANCH = (2.2, 3.0, 4.4)
NSEED = 12
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
SP, FU = load(HERE, "sprim"), load(HERE, "full")
BRS, CLS, MRU = load(HERE, "bracketS"), load(HERE, "clusteredS"), load(HERE, "mrU")

# known answer (i): identity with FRZ4, then merge FRZ4's U / C forced-box fields into this lane's sprim parts
def maxrel(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); z0 = b == 0
    if np.any(a[z0] != 0): return float("inf")                          # empty 3D bins: both must be 0
    return float(np.max(np.abs(a[~z0] / b[~z0] - 1))) if np.any(~z0) else 0.0
KI = dict(checked_fields=0, max_rel=0.0, max_rel_p=0.0, max_rel_P3D=0.0, parts=[], whole_part=None)
MAXW = {"p": 0.0, "P3D": 0.0}                            # AMENDMENT_A1 (352a7fe6ae): per-quantity maxima
def ident(mine, frz, names, specs):
    m = 0.0; n = 0
    for bx in ["base"] + [str(b) for b in mine["boxes"]]:
        A = mine["base"] if bx == "base" else mine["forced_boxes"][bx]
        B = frz["base"] if bx == "base" else frz["forced_boxes"].get(bx)
        if B is None: continue
        for sp in specs:
            if sp not in A["flux"] or sp not in B["flux"]: continue
            for nm in names:
                if nm in A["flux"][sp] and nm in B["flux"][sp]:
                    for w in ("p", "P3D"):
                        if w in A["flux"][sp][nm] and w in B["flux"][sp][nm]:
                            x = maxrel(A["flux"][sp][nm][w], B["flux"][sp][nm][w]); m = max(m, x); n += 1; MAXW[w] = max(MAXW[w], x)
    return m, n
PR = {}
for z, ps in SP.items():
    for s, d in ps.items():
        f4 = PR4.get(z, {}).get(s)
        if f4 is None: continue
        assert d["boxes"] == f4["boxes"], "forced set differs from FRZ4"
        m, n = ident(d, f4, ["R"], ["primary"]); mb, nb = ident(dict(d, boxes=[]), f4, ["B|" + k for k in UC] + ["B|f0.00"], ["primary"])
        KI["parts"].append(dict(z=z, seed=s, R_max_rel=m, R_fields=n, base_U_max_rel=mb, base_U_fields=nb))
        KI["max_rel"] = max(KI["max_rel"], m, mb); KI["checked_fields"] += n + nb
        if d.get("whole"):
            mw, nw = ident(d, f4, ["R"] + ["B|" + k for k in UC], ["primary"]); KI["whole_part"] = dict(z=z, seed=s, max_rel=mw, fields=nw)
            KI["max_rel"] = max(KI["max_rel"], mw)
        for b in d["boxes"]:
            mine = d["forced_boxes"][str(b)]["flux"]["primary"]; fr = f4["forced_boxes"][str(b)]["flux"]["primary"]
            for k in UC + ["f0.00"]:
                nm = "B|" + k
                if nm not in mine and nm in fr: mine[nm] = fr[nm]
        PR.setdefault(z, {})[s] = d
for z, ps in FU.items():
    for s, d in ps.items(): PR.setdefault(z, {})[s] = d
# bracket parts: R of the S-subset boxes common with FRZ4's subset under FRZ4's eight specs
for z, ps in BRS.items():
    for s, d in ps.items():
        if z in BR4 and s in BR4[z]:
            m, n = ident(d, BR4[z][s], ["R"], [t for t in BR4[z][s]["base"]["flux"]]); KI["parts"].append(dict(stage="bracketS", z=z, R_max_rel=m, R_fields=n))
            KI["max_rel"] = max(KI["max_rel"], m); KI["checked_fields"] += n
if KI["whole_part"] is None:   # criteria 5(i): ONE whole part (z 2.2 seed 1 canonical) serves both footings
    for f in glob.glob(os.path.join(HERE, "parts", "sprim_z2.2_s1_canonical_whole.json")):
        dw = json.load(open(f)); f4w = json.load(open(os.path.join(FRZ4, "parts", "primary_z2.2_s1_canonical.json")))
        mw, nw = ident(dw, f4w, ["R"] + ["B|" + k for k in UC], ["primary"]); KI["whole_part"] = dict(z=2.2, seed=1, footing="canonical", max_rel=mw, fields=nw)
        KI["max_rel"] = max(KI["max_rel"], mw); del dw, f4w
KI["max_rel_p"], KI["max_rel_P3D"] = MAXW["p"], MAXW["P3D"]
_ok = KI["checked_fields"] > 0 and KI["whole_part"] is not None and KI["whole_part"]["fields"] > 0
KI["pass_"] = bool(_ok and KI["max_rel"] <= 1e-12)                                       # as frozen
KI["pass_A1"] = bool(_ok and MAXW["p"] <= 1e-12 and MAXW["P3D"] <= 1e-6)                # AMENDMENT_A1
ZCOMP = [z for z in ZC if z in PR and 0 in PR[z]]
ZEST = [z for z in ZB if round(z, 1) not in ZCOMP]
SEEDS22 = sorted(PR.get(2.2, {}).keys())
P(f"[{FOOT}] FRZ6: computed bins {ZCOMP}; estimated bins {[round(z, 1) for z in ZEST]}; z 2.2 seeds {SEEDS22} (frozen {NSEED})")

def est(d, key, spec="primary", what="p", pre="B|", boxes=None, pre_base=None):
    """FRZ4's stratified ratio X_B / X_R; pre_base: the base box's field prefix when it differs (twin T1)."""
    F = d["base"]["flux"][spec]; XRb = np.array(F["R"][what]); XR = XRb.copy()
    dX = np.array(F[(pre_base or pre) + key][what]) - XRb
    use = d["boxes"] if boxes is None else [b for b in d["boxes"] if b in boxes]
    for ib in use:
        fb = d["forced_boxes"][str(ib)]; Fb = fb["flux"][spec]; E = fb["E"]
        XR = XR + E * (np.array(Fb["R"][what]) - XRb)
        dX = dX + E * (np.array(Fb[pre + key][what]) - np.array(Fb["R"][what]))
    return 1.0 + dX / XR

def seed_mean(z, fn): ps = PR[z]; return np.mean([fn(ps[s]) for s in sorted(ps)], 0)
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
def flux_set(key, fn=None):
    fn = fn or (lambda d: est(d, key)); return {z: (np.array(PR[z][0]["kv"]), seed_mean(z, fn)) for z in ZCOMP}
KOK = np.all([np.array(PR[z][s]["base"]["flux"]["primary"]["R"]["P3D"]) > 0 for z in ZCOMP for s in PR[z]], 0)
def mat_set(key):
    k = np.array(PR[ZCOMP[0]][0]["k3d"]); m = (k <= 10) & KOK
    return {z: seed_mean(z, lambda d: est(d, key, what="P3D"))[m] for z in ZCOMP}, k[m]
def dflux(Rset, sel=ALL): return dchi2_sel(r_points(Rset), sel)
def rp_only(Rset):
    r = np.ones(FD["NB"])
    for z, (kv, R) in Rset.items():
        s_ = np.round(FD["zs"], 1) == z; r[s_] = np.interp(FD["ks"][s_], kv[1:], R[1:])
    return r

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
RES = dict(lane="FRZ6", footing=FOOT, computed_bins=ZCOMP, estimated_bins=[round(z, 1) for z in ZEST], seeds_z22=SEEDS22,
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
rows = {}; RPTS = {}
for key in CASES:
    Fs = flux_set(key); RPTS[key] = r_points(Fs); Df = dchi2_sel(RPTS[key], ALL); Ms, k3 = mat_set(key); Dm = mat_dchi(Ms, k3)
    perbin = {f"{z:.1f}" + ("" if round(z, 1) in ZCOMP else " (estimated)"): dchi2_sel(RPTS[key], bin_sel(z)) for z in ZB}
    rows[key] = dict(flux=Df, matter=Dm, ratio=Df / Dm if Dm > 0 else None, D_ta=Dta[key], D_rec=Drec[key], c1_ratio=Dm / Dta[key] if Dta[key] > 0 else None,
                     record_convention_reading=Df * Drec[key] / Dm if Dm > 0 else None, per_bin=perbin,
                     R_F={f"{z:.1f}": [float(np.interp(x, Fs[z][0][1:], Fs[z][1][1:])) for x in (0.003, 0.005, 0.01, 0.02, 0.03)] for z in ZCOMP},
                     z22_single_seed=[dchi2_sel(rp_only({2.2: (np.array(PR[2.2][s]["kv"]), est(PR[2.2][s], key))}), ALL) for s in SEEDS22])
RES["rows"] = rows; RES["r_points"] = {k: v.tolist() for k, v in RPTS.items()}
P(f"[{FOOT}] case | flux dchi2 (12 bins) | matter, same fields | flux/matter | D_ta | matter/D_ta | D_rec | record-convention reading")
for key, r in rows.items():
    P(f"[{FOOT}] {key:5} | {r['flux']:10.4f} | {r['matter']:10.4f} | {(r['ratio'] or 0):.5f} | {r['D_ta']:9.4f} | {(r['c1_ratio'] or 0):.3f} | {r['D_rec']:9.4f} | {(r['record_convention_reading'] or 0):.4f}")
for key, r in rows.items():
    P(f"[{FOOT}] per bin {key}: " + " ".join(f"{z}:{v:.4g}" for z, v in r["per_bin"].items()))
    P(f"[{FOOT}]   {key} z 2.2 single-seed dchi2 (seeds {SEEDS22}): " + " ".join(f"{v:.4g}" for v in r["z22_single_seed"]))
    for z in ZCOMP:
        P(f"[{FOOT}]   {key} z {z}: R_F at 0.003/0.005/0.01/0.02/0.03 s/km " + "/".join(f"{v:.5f}" for v in r["R_F"][f"{z:.1f}"]))

# ------------------------------------------------------------------ known answers
KA = {"i": KI}
# (a)
amax = 0.0; nbox = 0
for z in ANCH:
    if z not in PR or 0 not in PR[z]: continue
    for d in [PR[z][0]] + ([PR4[z][0]] if z in PR4 and 0 in PR4[z] else []):
        for bx in [d["base"]] + list(d["forced_boxes"].values()):
            F = bx["flux"]["primary"]
            if "B|f0.00" in F:
                amax = max(amax, maxrel(F["B|f0.00"]["p"], F["R"]["p"])); nbox += 1
za = [z for z in ANCH if z in PR and 0 in PR[z]]
Da = dchi2_sel(rp_only({z: (np.array(PR[z][0]["kv"]), est(PR[z][0], "f0.00")) for z in za}), ALL)
KA["a"] = dict(max_rel_box=amax, boxes=nbox, dchi2_f0=Da, md5ok=md5ok, pass_=bool(nbox > 0 and amax <= 1e-12 and Da <= 1e-12 and md5ok))
# (b) FRZ4's Poisson-only answer on FRZ4's parts
bmax = 0.0; mine, frz, mineM, frzM = {}, {}, {}, {}; kf = None
for z in ZCOMP:
    arr, arr2, a3, b3 = [], [], [], []
    for s, d in PR4[z].items():
        fr = json.load(open(os.path.join(FRZ3R, "parts", f"turn_z{z:.1f}_s{s}_{FOOT}_N384.json"))); F = d["base"]["flux"]["primary"]
        bmax = max(bmax, maxrel(F["Rall"]["p"], fr["flux"]["primary"]["R"]["p"]), maxrel(F["BPall|finf"]["p"], fr["flux"]["primary"]["B"]["p"]))
        arr.append(np.array(F["BPall|finf"]["p"]) / np.array(F["Rall"]["p"])); arr2.append(np.array(fr["flux"]["primary"]["B"]["p"]) / np.array(fr["flux"]["primary"]["R"]["p"]))
        a3.append(np.array(F["BPall|finf"]["P3D"]) / np.array(F["Rall"]["P3D"])); kf = np.array(fr["P3D"]["k"]); b3.append(np.array(fr["P3D"]["B"]) / np.array(fr["P3D"]["R"]))
    mine[z] = (np.array(PR4[z][0]["kv"]), np.mean(arr, 0)); frz[z] = (np.array(fr["kv"]), np.mean(arr2, 0)); mineM[z] = np.mean(a3, 0); frzM[z] = np.mean(b3, 0)
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
JF = json.load(open(os.path.join(JNT2, f"jnt2_forest_{FOOT}.json")))["cases"]
ref0 = {"f1.00": ("SRH1 f1.00 (= FZS1)", SF["f1.00"]["dchi2"]), "f2.00": ("SRH1 f2.00", SF["f2.00"]["dchi2"]),
        "f3.00": ("SRF1 f3.00 (own chain)", SR["f3.00"]["D_rec"]), "finf": ("SRH1 KA_T (= FRZ1)", SF["KA_T"]["dchi2"]),
        "S1.25": ("JNT2 G1 f1.25", JF["f1.25"]["dchi2"]), "S2.00": ("JNT2 G1 f2.00", JF["f2.00"]["dchi2"]), "S3.00": ("JNT2 G1 f3.00", JF["f3.00"]["dchi2"])}
KA["c0"] = {}
for key in CASES:
    mn, rf = Drec[key], ref0[key][1]
    ok = abs(mn / rf - 1) <= 0.01 or (key in SC and abs(mn - rf) <= 0.002)
    KA["c0"][key] = dict(mine=mn, ref=rf, source=ref0[key][0], pass_=bool(ok))
# (c1)
KA["c1"] = {}
for key in CASES:
    Ms, k3m = mat_set(key); Dm = rows[key]["matter"]; pb = {}
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
for coll in (PR, BRS, CLS, MRU, BR4, CL4):
    for z, ps in coll.items():
        for d in ps.values():
            for bx in [d["base"]] + list(d["forced_boxes"].values()):
                for sp, fields in bx["flux"].items():
                    sF = {"tau_x0.9": 0.9, "tau_x1.1": 1.1}.get(sp, 1.0)
                    for nm, v in fields.items(): dmax = max(dmax, abs(v["meanF"] - math.exp(-sF * tau_eff(z))))
KA["d"] = dict(max_abs=dmax, pass_=bool(dmax <= 1e-4))
# (e) generalised to n seeds (criteria section 5e)
KA["e"] = {}
n22 = len(SEEDS22)
for key in CASES:
    if n22 >= 2:
        kv = np.array(PR[2.2][0]["kv"]); Rs = [est(PR[2.2][s], key) for s in SEEDS22]; Rb = np.mean(Rs, 0)
        N22 = sum(dchi2_sel(rp_only({2.2: (kv, 1.0 + (R - Rb))}), ALL) for R in Rs) / (n22 * (n22 - 1))
        D22 = dchi2_sel(rp_only({2.2: (kv, Rb)}), ALL)
        D = rows[key]["flux"]; N12 = D * N22 / D22 if D22 > 0 else float("inf"); SE = 2 * math.sqrt(D * N12) + N12
        KA["e"][key] = dict(n_seeds=n22, N22=N22, D22=D22, N12=N12, SE=SE, pass_=bool(n22 >= NSEED and (N12 <= 0.1 * D or N12 <= 0.05)),
                            pass_at_reached_seeds=bool(N12 <= 0.1 * D or N12 <= 0.05))
    else:
        KA["e"][key] = dict(pass_=False, note="fewer than 2 seeds at z 2.2")
# n = 2 equivalence with FRZ4's statistic (seeds 0 and 1)
if 1 in PR.get(2.2, {}):
    kv = np.array(PR[2.2][0]["kv"]); eq = {}
    for key in UC:
        R0_, R1_ = est(PR[2.2][0], key), est(PR[2.2][1], key); Rb = 0.5 * (R0_ + R1_)
        gen = sum(dchi2_sel(rp_only({2.2: (kv, 1.0 + (R - Rb))}), ALL) for R in (R0_, R1_)) / 2
        frz4 = dchi2_sel(rp_only({2.2: (kv, 1.0 + 0.5 * (R0_ - R1_))}), ALL); eq[key] = [gen, frz4]
    KA["e_n2_equivalence"] = eq
# (f) split identity
fmax = 0.0; fn = 0; memb = {}
JM = json.load(open(os.path.join(JNT2, "jnt2_hm.json")))["membership"][FOOT]
for coll in (PR, BRS, CLS):
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
RES["known_answers"] = KA
def ka_case(key, a1=False):
    k = dict(a=KA["a"]["pass_"], b=KA["b"]["pass_"], c0=KA["c0"][key]["pass_"], c1=KA["c1"][key]["pass_"], d=KA["d"]["pass_"], e=KA["e"][key]["pass_"])
    if key in SC: k["f"] = KA["f"]["pass_"]
    else: k["i"] = KA["i"]["pass_A1" if a1 else "pass_"]
    return k
P(f"[{FOOT}] known answer (i) identity with FRZ4: as frozen {'PASS' if KI['pass_'] else 'FAIL'}, under A1 {'PASS' if KI['pass_A1'] else 'FAIL'}; max rel P1D {KI['max_rel_p']:.2e}, P3D {KI['max_rel_P3D']:.2e} over {KI['checked_fields']} spectra; whole part {json.dumps(KI['whole_part'])}")
P(f"[{FOOT}] known answer (a): {'PASS' if KA['a']['pass_'] else 'FAIL'} max |B_f0/R - 1| {amax:.2e} over {nbox} boxes; dchi2 at f 0 {Da:.2e}; md5 {md5ok}")
P(f"[{FOOT}] known answer (b): {'PASS' if KA['b']['pass_'] else 'FAIL'} max rel {bmax:.2e}; flux {Db_m:.3f} vs FRZ3R {Db_f:.3f}; matter {Dbm_m:.2f} vs {Dbm_f:.2f}")
for key in CASES:
    c0 = KA["c0"][key]; c1 = KA["c1"][key]; e = KA["e"][key]
    P(f"[{FOOT}] known answer (c0) {key}: {'PASS' if c0['pass_'] else 'FAIL'} D_rec {c0['mine']:.5g} vs {c0['source']} {c0['ref']:.5g}")
    P(f"[{FOOT}] known answer (c1) {key}: {'PASS' if c1['pass_'] else 'FAIL'} realised {c1['realised']:.4g} / halo model {c1['halo_model_ta']:.4g} ({c1['rule']}); per bin "
      + "; ".join(f"{z}: " + (f"{v['realised']:.3g}/{v['halo_model']:.3g}={v['ratio']:.2f}{'' if v['ok'] else ' OUT'}" if v.get("checked", True) else f"hm {v['halo_model']:.3g} (<1)") for z, v in c1["per_bin"].items()))
    P(f"[{FOOT}] known answer (e) {key}: {'PASS' if e['pass_'] else 'FAIL'} " + json.dumps({k: v for k, v in e.items() if k != 'pass_'}, default=float))
P(f"[{FOOT}] known answer (d): {'PASS' if KA['d']['pass_'] else 'FAIL'} max |<F> - target| {dmax:.2e}")
P(f"[{FOOT}] known answer (f) split identity: {'PASS' if KA['f']['pass_'] else 'FAIL'} max rel {fmax:.2e} over {fn} wholly-above S spectra; membership mine vs JNT2 {json.dumps(memb)}")
if "e_n2_equivalence" in KA: P(f"[{FOOT}] (e) at n = 2 (seeds 0, 1) generalised vs FRZ4 half-difference: " + json.dumps(KA["e_n2_equivalence"]))

# forced-set shares of the S cases (reported)
FI = {}
for z in ZCOMP:
    fi = PR[z][0]["forced_info"]
    FI[f"{z:.1f}"] = dict(n_forced=len(fi["forced"]), forced_share_S=fi["forced_share_S"], nonforced_rare_share_S=fi["nonforced_rare_share_S"], common_share_S=fi["common_share_S"],
                          subset_S_lM=[round(fi["lM_lo"][i], 1) for i in fi["subset_S"]], vstar=fi["vstar"], n_above=fi["n_above"])
    P(f"[{FOOT}] forced set z {z}: S cases' share of the 1h change at k 3 in forced / non-forced rare / common bins: "
      + "; ".join(f"{k} {fi['forced_share_S'][k]:+.3f} / {fi['nonforced_rare_share_S'][k]:+.4f} / {fi['common_share_S'][k]:+.3f}" for k in SC) + f"; S subset log M {FI[f'{z:.1f}']['subset_S_lM']}")
RES["forced_sets_S"] = FI

# ------------------------------------------------------------------ twins (12 seeds at z 2.2)
MU = {}
def z22(fn): kv = np.array(PR[2.2][0]["kv"]); return dchi2_sel(rp_only({2.2: (kv, np.mean([fn(PR[2.2][s]) for s in SEEDS22], 0))}), ALL)
t1 = {}; t2 = {}
have_tw = all("D2|" + CASES[0] in PR[2.2][s]["base"]["flux"]["primary"] and "M1_lin" in PR[2.2][s]["base"]["flux"] for s in SEEDS22)
for key in CASES:
    if not have_tw: t1[key] = t2[key] = dict(bites=False, note="twin fields missing"); continue
    p = z22(lambda d: est(d, key)); a = z22(lambda d: est(d, key, pre_base="D2|"))
    t1[key] = dict(doubled=a, primary=p, factor=a / p if p > 0 else float("inf"), bites=bool(p > 0 and a / p >= 1.5))
    pb = z22(lambda d: est(d, key, boxes=[])); mb = z22(lambda d: est(d, key, spec="M1_lin", boxes=[]))
    t2[key] = dict(M1=mb, primary_base_only=pb, factor=mb / pb if pb > 0 else float("inf"), bites=bool(pb > 0 and (mb / pb >= 1.25 or mb / pb <= 0.8)))
MU["T1_base_change_doubled"] = dict(rows=t1, seeds=SEEDS22); MU["T2_base_saturation_removed"] = dict(rows=t2, seeds=SEEDS22)
# reported only: FRZ4's M2 (all boxes, seed 0, FRZ4's parts) and M1 (FRZ4 subset; S subset)
def d_one(d, key, spec, boxes, pre="B|"): return dchi2_sel(rp_only({2.2: (np.array(d["kv"]), est(d, key, spec, pre=pre, boxes=boxes))}), ALL)
rep = {}
if 2.2 in PR4 and 0 in PR4[2.2]:
    d4 = PR4[2.2][0]; rep["M2_FRZ4_all_boxes_seed0"] = {k: d_one(d4, k, "primary", None, "D2|") / max(d_one(d4, k, "primary", None), 1e-300) for k in UC}
if 2.2 in BR4 and 0 in BR4[2.2]:
    sb = BR4[2.2][0]["boxes"]; rep["M1_FRZ4_subset_seed0"] = {k: d_one(BR4[2.2][0], k, "M1_lin", sb) / max(d_one(PR[2.2][0], k, "primary", sb), 1e-300) for k in UC}
if 2.2 in BRS and 0 in BRS[2.2]:
    sb = BRS[2.2][0]["boxes"]; rep["M1_S_subset_seed0"] = {k: d_one(BRS[2.2][0], k, "M1_lin", sb) / max(d_one(PR[2.2][0], k, "primary", sb), 1e-300) for k in SC}
MU["reported_factors"] = rep
RES["mutations"] = MU
for k, v in MU.items():
    if k == "reported_factors": P(f"[{FOOT}] MUTATE reported (not graded) factors: {json.dumps(v, default=float)}", m=True); continue
    P(f"[{FOOT}] MUTATE {k} (seeds {SEEDS22}): " + "; ".join(f"{kk}: {json.dumps(vv, default=float)}" for kk, vv in v["rows"].items()), m=True)
mu_case = {key: bool(t1[key]["bites"] and t2[key]["bites"]) for key in CASES}

# ------------------------------------------------------------------ brackets (seed 0)
def d_multi(BRc, zs, key, spec, primary_subset_from):
    Rb_, Rp_ = {}, {}
    for z in zs:
        d = BRc[z][0]; sub = d["boxes"]
        Rb_[z] = (np.array(d["kv"]), est(d, key, spec, boxes=sub)); Rp_[z] = (np.array(PR[z][0]["kv"]), est(PR[z][0], key, "primary", boxes=sub))
    return dchi2_sel(rp_only(Rb_), ALL), dchi2_sel(rp_only(Rp_), ALL)
TAGS = ("lam_x0.5", "lam_x2", "lam_rec", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1")
MRT = ("lam_mr_lo", "lam_mr_mid", "lam_mr_hi")
BRK = {k: {} for k in CASES}; BRZ = {}
for key in CASES:
    BRc = BR4 if key in UC else BRS; CLc = CL4 if key in UC else CLS
    zs = [z for z in (2.2, 3.0) if z in BRc and 0 in BRc[z]]; BRZ[key] = zs
    for tag in TAGS + (() if key in UC else ("lam_mr_lo", "lam_mr_hi")):
        if zs: b_, p_ = d_multi(BRc, zs, key, tag, None); BRK[key][tag] = rows[key]["flux"] * b_ / max(p_, 1e-300)
    if key in UC:
        zm = [z for z in (2.2, 3.0) if z in MRU and 0 in MRU[z]]
        for tag in MRT:
            if zm: b_, p_ = d_multi(MRU, zm, key, tag, None); BRK[key][tag] = rows[key]["flux"] * b_ / max(p_, 1e-300)
    if 2.2 in CLc and 0 in CLc[2.2]:
        b_, p_ = d_multi(CLc, [2.2], key, "primary", None); BRK[key]["clustered"] = rows[key]["flux"] * b_ / max(p_, 1e-300)
RES["brackets"] = BRK
for key in CASES:
    P(f"[{FOOT}] brackets {key} (bins {BRZ[key]}; 12-bin estimates): " + "; ".join(f"{t} {v:.4g}" for t, v in BRK[key].items()))

# ------------------------------------------------------------------ labels (criteria section 8)
LAB = {}; LAB_MR = {}; LAB_A1 = {}; LAB_MR_A1 = {}
FROZEN_BR = TAGS + ("clustered",)
MR_BR = ("lam_mr_lo", "lam_mr_hi", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1", "clustered")
def label(key, brset, a1=False):
    D = rows[key]["flux"]; ka = ka_case(key, a1); e = KA["e"][key]; SE = e.get("SE", float("inf"))
    bad = [f"known answer {k} fails" for k, v in ka.items() if not v] + ([] if mu_case[key] else ["a twin does not bite"])
    if n22 < NSEED: bad.append(f"seed count not reached ({n22} of {NSEED})")
    if bad: return "NO VERDICT (" + ", ".join(bad) + ")"
    if D + 2 * SE < 4: lab = "FOREST ROW HOLDS AT FLUX LEVEL"
    elif D - 2 * SE > 4: lab = "FOREST ROW FAILS AT FLUX LEVEL"
    else: return f"NO VERDICT (unresolved at {n22} seeds: D {D:.3g}, SE {SE:.3g})"
    present = [t for t in brset if t in BRK[key]]
    frag = [t for t in present if (BRK[key][t] > 4) != (D > 4)]
    if frag: lab += ", FRAGILE (" + "; ".join(frag) + ")"
    if len(present) < len(brset): lab += " [brackets incomplete: " + ", ".join(t for t in brset if t not in BRK[key]) + "]"
    if lab.startswith("FOREST ROW HOLDS"): lab += "; a hit that awaits an independent blind re-grade, not a pass of the theory"
    return lab
for key in CASES:
    LAB[key] = label(key, FROZEN_BR); LAB_MR[key] = label(key, MR_BR); LAB_A1[key] = label(key, FROZEN_BR, True); LAB_MR_A1[key] = label(key, MR_BR, True)
    P(f"[{FOOT}] LABEL as frozen {key}: {LAB[key]}")
for key in CASES:
    P(f"[{FOOT}] LABEL under AMENDMENT_A1 (post hoc) {key}: {LAB_A1[key]}")
for key in CASES:
    P(f"[{FOOT}] measured-range reading (reported, not the label) {key}: as frozen {LAB_MR[key]} | under A1 {LAB_MR_A1[key]}")
RES["labels"] = LAB; RES["labels_A1"] = LAB_A1; RES["labels_measured_range_reading"] = LAB_MR; RES["labels_measured_range_reading_A1"] = LAB_MR_A1
json.dump(RES, open(os.path.join(HERE, f"frz6_grade_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"frz6_grade_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
json.dump(dict(lane="FRZ6", footing=FOOT, mutations=MU, note=RES["note"]), open(os.path.join(HERE, f"frz6_grade_{FOOT}_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"frz6_grade_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
