#!/usr/bin/env python3
"""BJ1 build B grader (FROZEN_CRITERIA.md 9e7ce0dfe6, sections 2 and 3; AMENDMENT_A1): a copy of XJ1's second-pass grader
xj1b2_grade.py (closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface) with the case list changed to B1, B2, B3
(cases not built, or narrowed out by BJ1B_CASES, read "flux level not run"), KA-R2 replaced by KA-R (this lane's R equals
XJ1's first-pass R, same z, seed, footing, to 1e-6 at every mode k_v > 0), KA-E / KA-K replaced by this lane's
profile-level known answers (bj1_ka_tables.json, items i to vii with AMENDMENT_A1) and XJ1's caustic-table check KA-K
(xj1_ka_tables3.json, read), the control J5 and its known answer KA-5, KA-C, KA-INF and TW-A read as XJ1's second pass
reads them, the twin TW-B at B1 (TWB = R + 2 (B1 - R) at the anchors, bites at a factor >= 2.5; replaced by XJ1's
first-pass TW-B when B1's anchor statistic is below 0.05), no window or ceiling words, and BJ1's lane words of criteria
section 3 per footing and case, composed with G-RC (bj1_sparc.json) and G-L (bj1_lens.json). Estimator, D, SE, gate 4,
seed test, brackets and label rule are XJ1's unchanged. Reads parts_b/*.json and XJ1's parts_b/ (R only).
  nice -n 19 python3 -I -B bj1b_grade.py -> bj1b_grade.json / .out, bj1b_grade_MUTATE.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import cho_solve
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ODIR = os.environ.get("BJ1B_ODIR") or HERE
import bj1_lib as BL
X = BL.X
XJ1 = BL.XJ1; G1DIR = XJ1
PARTS = os.environ.get("BJ1B_PARTS") or os.path.join(HERE, "parts_b"); PARTS1 = os.path.join(XJ1, "parts_b")
OUT, OUTM = [], []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)

FD = X.forest_data(); MD5OK = FD["md5"] == "33d7fc21bfd3d745ed71a0bbe80ca433"
cf, lower = FD["CF"]; Uc = np.tril(cf).T if lower else np.triu(cf); COV = Uc.T @ Uc
ALL = np.ones(FD["NB"], bool); ASEL = np.isin(FD["zs"], X.ANCH)
def dchi2(r, sel=ALL):
    d = ((r - 1.0) * FD["Pd"])
    if sel is ALL: return float(d @ cho_solve(FD["CF"], d))
    d = d[sel]; return float(d @ np.linalg.solve(COV[np.ix_(sel, sel)], d))
def at_points(kv, Rz):
    r = np.ones(FD["NB"])
    for z, R in Rz.items():
        s_ = FD["zs"] == round(z, 2); r[s_] = np.interp(np.log(FD["ks"][s_]), np.log(kv[z][1:]), R[1:])
    return r
JNT2 = dict(canonical=[170, 176, 181, 187, 192, 197, 202, 206, 211, 215, 219, 223], alt=[160, 166, 172, 177, 182, 187, 192, 196, 201, 205, 209, 213])
FWN1R_DIR = os.path.join(X.REPO, "closure_2026_11_14", "FWN1R_blind_split_f_ceiling")
FWN1R_PARTS = os.path.join(FWN1R_DIR, "parts"); FWN1R_G = json.load(open(os.path.join(FWN1R_DIR, "fwn1r_grade.json")))["footings"]
FRZ6R_G = json.load(open(os.path.join(X.REPO, "closure_2026_11_13", "FRZ6R_blind_forest_flux_candidate", "frz6r_grade.json")))["footings"]
KAT = json.load(open(os.path.join(HERE, "bj1_ka_tables.json"))); KAT3 = json.load(open(os.path.join(XJ1, "xj1_ka_tables3.json")))
SPC = json.load(open(os.path.join(HERE, "bj1_sparc.json")))["footings"]; LNS = json.load(open(os.path.join(HERE, "bj1_lens.json")))["cfg"]
G1 = json.load(open(os.path.join(G1DIR, "xj1b_grade.json")))["footings"]
GR_ALL = ["B1", "B2", "B3"]; GR_ENV = [c for c in os.environ.get("BJ1B_CASES", "B1,B2,B3").split(",") if c]

def load(stage, ft):
    out = {}
    for f in sorted(glob.glob(os.path.join(PARTS, f"{stage}_z*_s*_{ft}.json"))):
        d = json.load(open(f))
        if stage == "br" and d["seed"] in out.get(d["z"], {}):                     # one file per bracket: merge
            e = out[d["z"]][d["seed"]]; e["flux"].update(d["flux"]); e["floored"].update(d["floored"]); continue
        out.setdefault(d["z"], {})[d["seed"]] = d
    return out

def lane_words(ft, labels):
    """criteria section 3, per footing and case: G-RC from bj1_sparc.json, G-L from bj1_lens.json, G-F from the flux label."""
    out = {}
    for nm in GR_ALL:
        k = nm[1]; grc = SPC[ft]["cases"][nm]["word"]; gl = LNS[f"{ft}|{nm}"]["gate"]["status"]
        lab = labels.get(nm, dict(label="NO VERDICT (flux level not run)"))["label"]
        fails = []
        if grc == "FAIL": fails.append(f"FAILS ON ROTATION CURVES (caustic {k})")
        if lab.startswith("FOREST ROW FAILS"): fails.append(f"FAILS THE FOREST (caustic {k})" + (", " + lab.split(", ", 1)[1] if ", FRAGILE" in lab else ""))
        if gl == "FAIL": fails.append(f"FAILS LENSING (caustic {k})")
        if fails: out[nm] = "; ".join(fails)
        elif grc == "PASS" and gl == "PASS" and lab.startswith("FOREST ROW HOLDS"):
            out[nm] = f"BUDGET JUNCTION HOLDS AT CAUSTIC {k}" + (", " + lab.split(", ", 1)[1] if ", FRAGILE" in lab else "") + " (a hit awaiting a blind re-grade)"
        else:
            cause = "flux level not run" if "not run" in lab else ("G-L " + gl if gl != "PASS" else "") or ("G-F " + lab)
            out[nm] = f"NOT RESOLVED (caustic {k}): {cause}"
    return out

RES = dict(lane="BJ1", build="B (FWN1R's library, XJ1's second-pass driver)", criteria="9e7ce0dfe6", amendment="A1 1334d9f23b", md5_ok=MD5OK,
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.", footings={})
MUT = dict(lane="BJ1", note=RES["note"], footings={})
for ft in X.FOOTS:
    PR = load("prim", ft); BR = load("br", ft)
    have = [set(PR.get(z, {}).keys()) for z in X.ZB]
    GR = [c for c in GR_ALL if c in GR_ENV and all(c in d["flux"]["primary"] for zz in PR for d in PR[zz].values())] if PR else []
    seeds = sorted(set.intersection(*have)) if all(have) else []; n = len(seeds)
    R = dict(seeds=seeds, n=n, cases={})
    P(f"[{ft}] seeds in all 12 bins: {seeds}")
    if n < 4:
        P(f"[{ft}] fewer than 4 seeds in all 12 bins: flux level not run or not finished; nothing graded"); R["labels"] = {nm: dict(label="NO VERDICT (flux level not run)") for nm in GR_ALL}
        R["lane_words"] = lane_words(ft, R["labels"]); RES["footings"][ft] = R
        for k_, v_ in R["lane_words"].items(): P(f"[{ft}] lane word {k_}: {v_}")
        continue
    kv = {z: np.array(PR[z][seeds[0]]["kv"]) for z in X.ZB}
    def Rhat(parts, z, nm, ss, tag="primary"):
        num = sum(np.array(parts[z][s]["flux"][tag][nm]["p"]) for s in ss); den = sum(np.array(parts[z][s]["flux"][tag]["R"]["p"]) for s in ss)
        return num / den
    def Dof(nm, ss, zs=X.ZB, sel=ALL, parts=None, tag="primary"):
        parts = parts or PR
        return dchi2(at_points(kv, {z: Rhat(parts, z, nm, ss, tag) for z in zs}), sel)
    def DSE(nm, zs=X.ZB, sel=ALL):
        D = Dof(nm, seeds, zs, sel); Dj = np.array([Dof(nm, [s for s in seeds if s != j], zs, sel) for j in seeds])
        return D, math.sqrt((n - 1) / n * np.sum((Dj - Dj.mean()) ** 2)), Dj
    for nm in GR:
        D, SE, Dj = DSE(nm)
        sig = {}
        for z in X.ZB:
            Rj = np.array([Rhat(PR, z, nm, [s for s in seeds if s != j]) for j in seeds])
            sig[z] = np.sqrt((n - 1) / n * np.sum((Rj - Rj.mean(0)) ** 2, 0))
        Dn = dchi2(at_points(kv, {z: 1.0 + sig[z] for z in X.ZB}))
        perbin = {f"{z:.1f}": dchi2(at_points(kv, {z: Rhat(PR, z, nm, seeds)}), FD["zs"] == z) for z in X.ZB}
        A = Dof(nm, seeds, X.ANCH, ASEL)
        RF = {f"{z:.1f}": [float(np.interp(math.log(x), np.log(kv[z][1:]), Rhat(PR, z, nm, seeds)[1:])) for x in (0.003, 0.01, 0.03)] for z in X.ZB}
        li = {f"{z:.1f}": PR[z][seeds[0]].get("layout_info", {}).get(nm) for z in X.ZB}
        R["cases"][nm] = dict(D=D, SE=SE, D_jack=Dj.tolist(), KA_S=dict(D_noise=Dn, limit=0.1 * max(D, 4.0), pass_=bool(Dn <= 0.1 * max(D, 4.0))), A=A, per_bin=perbin,
                              R_F_at_0p003_0p01_0p03=RF, layout_info=li)
        P(f"[{ft}] {nm:4s}: D {D:.5g}  SE {SE:.3g}  D + 2 SE {D + 2 * SE:.5g}  D - 2 SE {D - 2 * SE:.5g}  (D_jack {', '.join(f'{x:.5g}' for x in Dj)}); seed test D_noise {Dn:.3g} vs {0.1 * max(D, 4):.3g} -> {'PASS' if Dn <= 0.1 * max(D, 4) else 'FAIL'}; anchors A {A:.4g}")
        P(f"[{ft}] {nm:4s} per bin: " + " ".join(f"{k}:{v:.3g}" for k, v in perbin.items()))
        P(f"[{ft}] {nm:4s} R_F at k_v 0.003/0.01/0.03: " + "; ".join(f"z {k} " + "/".join(f"{x:.5f}" for x in v) for k, v in RF.items()))
        P(f"[{ft}] {nm:4s} branches (under / over) at z 2.2, 3.0, 4.4: " + "; ".join(f"z {zz}: {li[zz]['n_under']} / {li[zz]['n_over']}, R_set/R_fold {li[zz]['Rset_over_Rfold_min_max']}" if li.get(zz) else f"z {zz}: -" for zz in ("2.2", "3.0", "4.4")))
    KA = {}
    # KA-R: this lane's R against XJ1's first-pass R; the control J5 and KA-5 are XJ1's first pass's
    dev = 0.0; nfile = 0
    for z in X.ZB:
        for s in seeds:
            fo = os.path.join(PARTS1, f"prim_z{z:.1f}_s{s}_{ft}.json")
            if not os.path.exists(fo): continue
            old = json.load(open(fo))["flux"]["primary"]; nfile += 1
            dev = max(dev, float(np.max(np.abs(np.array(PR[z][s]["flux"]["primary"]["R"]["p"])[1:] / np.array(old["R"]["p"])[1:] - 1))))
    g1 = G1[ft]; D5, SE5 = g1["cases"]["J5"]["D"], g1["cases"]["J5"]["SE"]
    KA["KA_R"] = dict(max_dev=dev, files=nfile, pass_=bool(dev <= 1e-6 and nfile == 12 * n))
    KA["KA_5"] = dict(read_from="XJ1 xj1b_grade.json (first pass)", pass_=bool(g1["known_answers"]["KA_5"]["pass_"]), D=D5, SE=SE5)
    ok_ = FWN1R_G[ft]["known_answers"]
    KA["KA_C"] = dict(read_from="fwn1r_grade.json", pass_=bool(ok_["KA_C"]["pass_"]), D=ok_["KA_C"]["D"], SE=ok_["KA_C"]["SE"])
    KA["KA_INF"] = dict(read_from="fwn1r_grade.json", pass_=bool(ok_["KA_INF"]["pass_"]))
    gotp = [PR[z][seeds[0]]["n_above"] for z in X.ZB]; gott = [KAT["KA"][f"{ft}|{z}"]["n_above"] for z in X.ZB]
    KA["KA_N"] = dict(parts=gotp, tables=gott, JNT2=JNT2[ft], pass_=bool(gotp == JNT2[ft] and gott == JNT2[ft]))
    dm = 0.0
    for parts in (PR, BR):
        for z in parts:
            for d in parts[z].values():
                for tag, fl in d["flux"].items():
                    for v in fl.values(): dm = max(dm, abs(v["meanF"] - v["target"]))
    KA["KA_F"] = dict(max_abs=dm, pass_=bool(dm <= 1e-4))
    km = {}; okm = {}
    for nm in GR:
        okm[nm] = True
        for z in X.ANCH:
            k = np.array(PR[z][seeds[0]]["P3D"]["k"]); num = sum(np.array(PR[z][s]["P3D"][nm]) for s in seeds); den = sum(np.array(PR[z][s]["P3D"]["R"]) for s in seeds)
            g = (den > 0) & np.isfinite(num); rr = num[g] / den[g]
            for i, x in enumerate((1.0, 3.0, 5.0)):
                v = float(np.interp(math.log(x), np.log(k[g]), rr)); E = PR[z][seeds[0]]["expected"][nm][i]; tol = 0.01 + 0.3 * abs(E - 1)
                km[f"{nm} z{z} k{x:g}"] = dict(realised=v, expected=E, tol=tol, ok=bool(abs(v - E) <= tol)); okm[nm] &= abs(v - E) <= tol
    KA["KA_M"] = dict(rows=km, pass_by_case={k: bool(v) for k, v in okm.items()})
    KA["KA_B"] = dict(read_from="bj1_ka_tables.json (items i to vii, AMENDMENT_A1 tolerance on iv)", pass_=bool(all(KAT["KA"][f"{ft}|{z}"]["pass_"] for z in X.ZB)),
                      worst_iv_min_step=min(KAT["KA"][f"{ft}|{z}"]["iv_min_step"] for z in X.ZB))
    KA["KA_K"] = dict(read_from="XJ1 xj1_ka_tables3.json", **{k: v for k, v in KAT3["KA_K"].items()})
    fl = [v for z in PR for d in PR[z].values() for k, v in d["floored"].items()]
    KA["floored_max_primary"] = max(fl)
    R["known_answers"] = KA
    for k, v in KA.items():
        if isinstance(v, dict): P(f"[{ft}] known answer {k}: " + ("PASS" if v.get("pass_", all(v.get("pass_by_case", {}).values())) else "FAIL") + " " + json.dumps({kk: vv for kk, vv in v.items() if kk not in ("pass_", "rows")})[:600])
    worst = sorted(km.items(), key=lambda kv_: -abs(kv_[1]["realised"] - kv_[1]["expected"]) / kv_[1]["tol"])[:6]
    P(f"[{ft}] KA_M worst rows: " + "; ".join(f"{k}: {v['realised']:.5f} vs {v['expected']:.5f} (tol {v['tol']:.4f})" for k, v in worst))
    P(f"[{ft}] floored gas fraction, primary fields: max {max(fl):.2e}")
    # twins
    A1_ = R["cases"]["B1"]["A"] if "B1" in R["cases"] else Dof("B1", seeds, X.ANCH, ASEL); AB = Dof("TWB", seeds, X.ANCH, ASEL); twa = FWN1R_G[ft]["twins"]["TWA"]; tb1 = g1["twins"]["TWB"]; small = A1_ < 0.05
    TW = dict(TWA=dict(read_from="fwn1r_grade.json", bites=bool(twa["bites"]), ratio=twa["ratio"]),
              TWB=dict(A=AB, A_B1=A1_, factor=AB / A1_ if A1_ > 0 else float("inf"), replaced_by_XJ1_first_pass_TWB=bool(small), first_pass_bites=bool(tb1["bites"]),
                       bites=bool(tb1["bites"]) if small else bool(AB / A1_ >= 2.5)))
    R["twins"] = TW; MUT["footings"][ft] = TW
    P(f"[{ft}] twin TW-A boundary removed at f = inf (read from FWN1R's grade file): ratio {twa['ratio']:.3g} -> {'bites' if TW['TWA']['bites'] else 'DOES NOT BITE'}", m=True)
    P(f"[{ft}] twin TW-B difference doubled at B1: anchors {AB:.4g} vs {A1_:.4g} (x {TW['TWB']['factor']:.3g})" + (" [B1's anchors below 0.05: replaced by XJ1's first-pass TW-B]" if small else "") + f" -> {'bites' if TW['TWB']['bites'] else 'DOES NOT BITE'}", m=True)
    # brackets
    bs = sorted(set.intersection(*[set(BR.get(z, {}).keys()) for z in X.ANCH])) if all(z in BR for z in X.ANCH) else []
    BRK = {}
    if bs:
        for nm in GR:
            Ap = Dof(nm, bs, X.ANCH, ASEL); BRK[nm] = {}
            for tag in ("lam_x0.5", "lam_x2", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1", "lam_91.4", "lam_138.6"):
                if not all(tag in BR[z][s]["flux"] for z in X.ANCH for s in bs): continue
                Ab = Dof(nm, bs, X.ANCH, ASEL, parts=BR, tag=tag); D = R["cases"][nm]["D"]
                BRK[nm][tag] = dict(A=Ab, A_primary_same_seeds=Ap, est_12bin=D * Ab / Ap if Ap > 0 else float("nan"))
            P(f"[{ft}] {nm:4s} brackets (12-bin est.): " + "; ".join(f"{t} {v['est_12bin']:.4g}" for t, v in BRK[nm].items()))
    R["brackets"] = dict(seeds=bs, cases=BRK)
    # labels
    kaok = all(KA[k]["pass_"] for k in ("KA_R", "KA_5", "KA_C", "KA_INF", "KA_N", "KA_F", "KA_B", "KA_K"))
    twok = TW["TWA"]["bites"] and TW["TWB"]["bites"]
    LAB = {}; frozen_br = ("lam_x0.5", "lam_x2", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1")
    for nm in GR:
        c = R["cases"][nm]; D, SE = c["D"], c["SE"]; ok = kaok and twok and c["KA_S"]["pass_"] and KA["KA_M"]["pass_by_case"][nm]
        lab = "FOREST ROW HOLDS AT FLUX LEVEL" if (ok and D + 2 * SE < 4) else "FOREST ROW FAILS AT FLUX LEVEL" if D - 2 * SE > 4 else "NO VERDICT"
        cross = [t for t in frozen_br if t in BRK.get(nm, {}) and ((BRK[nm][t]["est_12bin"] > 4) != (D > 4))]
        if cross: lab += ", FRAGILE (" + "; ".join(cross) + ")"
        missing = [t for t in frozen_br if t not in BRK.get(nm, {})]
        fails = [k for k in ("KA_R", "KA_5", "KA_C", "KA_INF", "KA_N", "KA_F", "KA_B", "KA_K") if not KA[k]["pass_"]] + ([] if c["KA_S"]["pass_"] else ["KA_S"]) + ([] if KA["KA_M"]["pass_by_case"][nm] else ["KA_M"]) \
            + [k for k in ("TWA", "TWB") if not TW[k]["bites"]]
        cause = None
        if lab.startswith("NO VERDICT"):
            cause = "unresolved: |D - 4| <= 2 SE" if abs(D - 4) <= 2 * SE else ("known answer or twin: " + ", ".join(fails))
        mr = {}
        for t in ("lam_91.4", "lam_138.6"):
            if t in BRK.get(nm, {}):
                ap = BRK[nm][t]; sc = ap["A"] / ap["A_primary_same_seeds"] if ap["A_primary_same_seeds"] > 0 else float("nan"); Dm, Sm = D * sc, SE * sc
                mr[t] = dict(D=Dm, SE=Sm, word=("HOLDS" if (ok and Dm + 2 * Sm < 4) else "FAILS" if Dm - 2 * Sm > 4 else "NO VERDICT"))
        LAB[nm] = dict(label=lab, D=D, SE=SE, no_verdict_cause=cause, known_answer_or_twin_failures=fails, missing_brackets=missing, measured_range=mr)
        P(f"[{ft}] {nm}: {lab}" + (f" [{cause}]" if cause else "") + f"  (D {D:.5g}, SE {SE:.3g}; failures {fails or 'none'}; missing brackets {missing or 'none'}; measured range " + "; ".join(f"{t}: D {v['D']:.4g} -> {v['word']}" for t, v in mr.items()) + ")")
    P(f"[{ft}] control J5 (first pass): D {D5:.5g} SE {SE5:.3g} -> {'FAILS' if D5 - 2 * SE5 > 4 else 'does not fail'}")
    for nm in GR_ALL:
        if nm not in LAB: LAB[nm] = dict(label="NO VERDICT (flux level not run)")
    R["lane_words"] = lane_words(ft, LAB)
    for k_, v_ in R["lane_words"].items(): P(f"[{ft}] lane word {k_}: {v_}")
    R["labels"] = LAB; RES["footings"][ft] = R
json.dump(RES, open(os.path.join(ODIR, "bj1b_grade.json"), "w"), indent=1)
open(os.path.join(ODIR, "bj1b_grade.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
json.dump(MUT, open(os.path.join(ODIR, "bj1b_grade_MUTATE.json"), "w"), indent=1)
open(os.path.join(ODIR, "bj1b_grade_MUTATE.out"), "w").write("\n".join(OUTM) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
