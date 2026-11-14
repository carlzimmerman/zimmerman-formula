#!/usr/bin/env python3
"""FWN2 build B grader (FROZEN_CRITERIA.md 26cb002843, section 3): COPY of FWN1R's fwn1r_grade.py (closure_2026_11_14/
FWN1R_blind_split_f_ceiling) with the cases J3.5, J4, J4.5. Changes: KA-5 (R and J5 against FWN1R's stored parts, and J5's D
and SE against FWN1R's stored values) in place of KA-3; KA-C, KA-INF and twin TW-A are read from FWN1R's committed grade
file (not recomputed); twin TW-B4 is the difference doubled at f = 4; the boundary-removed field U4 is reported, not a gate;
the ceiling adds this lane's points. dchi2, at_points, the ratio-of-seed-sums estimator, the jackknife SE, the bracket
estimate and the label rule are FWN1R's code unchanged. FWN1R's library is imported read-only from its own folder.
  nice -n 19 python3 -I -B fwn2b_grade.py -> fwn2b_grade.json / .out, fwn2b_grade_MUTATE.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import cho_solve
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FWN1R = os.path.join(REPO, "closure_2026_11_14", "FWN1R_blind_split_f_ceiling")
sys.path.insert(0, FWN1R)
ODIR = os.environ.get("FWN2B_ODIR") or HERE
import fwn1r_lib as X                                      # read-only
PARTS = os.environ.get("FWN2B_PARTS") or os.path.join(HERE, "parts_b")
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
G1R = json.load(open(os.path.join(FWN1R, "fwn1r_grade.json")))
FWN1R_PARTS = os.path.join(FWN1R, "parts")
GR = ["J3.5", "J4", "J4.5"]; FV = {"J3.5": 3.5, "J4": 4.0, "J4.5": 4.5}

def load(stage, ft):
    out = {}
    for f in sorted(glob.glob(os.path.join(PARTS, f"{stage}_z*_s*_{ft}.json"))):
        d = json.load(open(f))
        if stage == "br" and d["seed"] in out.get(d["z"], {}):                     # one file per bracket: merge
            e = out[d["z"]][d["seed"]]; e["flux"].update(d["flux"]); e["floored"].update(d["floored"]); continue
        out.setdefault(d["z"], {})[d["seed"]] = d
    return out

# ------------------------------------------------------------------ table-level known answer (membership)
TAB = {}
for z in X.ZB:
    T = X.tables(z, {"R": ("R", 0, "main")})
    for ft in X.FOOTS: TAB[(z, ft)] = dict(n_above=T[ft]["n_above"])

RES = dict(lane="FWN2B", criteria="26cb002843", md5_ok=MD5OK, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", footings={})
MUT = dict(lane="FWN2B", note=RES["note"], footings={})
for ft in X.FOOTS:
    PR = load("prim", ft); BR = load("br", ft)
    seeds = sorted(set.intersection(*[set(PR.get(z, {}).keys()) for z in X.ZB])); n = len(seeds)
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
    R = dict(seeds=seeds, n=n, cases={})
    P(f"[{ft}] seeds in all 12 bins: {seeds} (frozen: 0 to 3)")
    for nm in GR + ["J5", "U4"]:
        D, SE, Dj = DSE(nm)
        sig = {}
        for z in X.ZB:
            Rj = np.array([Rhat(PR, z, nm, [s for s in seeds if s != j]) for j in seeds])
            sig[z] = np.sqrt((n - 1) / n * np.sum((Rj - Rj.mean(0)) ** 2, 0))
        Dn = dchi2(at_points(kv, {z: 1.0 + sig[z] for z in X.ZB}))
        perbin = {f"{z:.1f}": dchi2(at_points(kv, {z: Rhat(PR, z, nm, seeds)}), FD["zs"] == z) for z in X.ZB}
        A = Dof(nm, seeds, X.ANCH, ASEL)
        RF = {f"{z:.1f}": [float(np.interp(math.log(x), np.log(kv[z][1:]), Rhat(PR, z, nm, seeds)[1:])) for x in (0.003, 0.01, 0.03)] for z in X.ZB}
        R["cases"][nm] = dict(D=D, SE=SE, D_jack=Dj.tolist(), KA_S=dict(D_noise=Dn, limit=0.1 * max(D, 4.0), pass_=bool(Dn <= 0.1 * max(D, 4.0))), A=A, per_bin=perbin, R_F_at_0p003_0p01_0p03=RF)
        P(f"[{ft}] {nm:5s}: D {D:.5g}  SE {SE:.3g}  D + 2 SE {D + 2 * SE:.5g}  D - 2 SE {D - 2 * SE:.5g}  (D_jack {', '.join(f'{x:.5g}' for x in Dj)}); seed test D_noise {Dn:.3g} vs {0.1 * max(D, 4):.3g} -> {'PASS' if Dn <= 0.1 * max(D, 4) else 'FAIL'}; anchors A {A:.4g}")
        P(f"[{ft}] {nm:5s} per bin: " + " ".join(f"{k}:{v:.3g}" for k, v in perbin.items()))
        P(f"[{ft}] {nm:5s} R_F at k_v 0.003/0.01/0.03: " + "; ".join(f"z {k} " + "/".join(f"{x:.5f}" for x in v) for k, v in RF.items()))
    KA = {}
    S1 = G1R["footings"][ft]
    # KA-5: R and J5 against FWN1R's stored parts; J5's D and SE against FWN1R's stored values; J5 still fails
    dev = 0.0; nfile = 0
    for z in X.ZB:
        for s in seeds:
            old = json.load(open(os.path.join(FWN1R_PARTS, f"prim_z{z:.1f}_s{s}_{ft}.json")))["flux"]["primary"]; nfile += 1
            for nm in ("R", "J5"):
                dev = max(dev, float(np.max(np.abs(np.array(PR[z][s]["flux"]["primary"][nm]["p"])[1:] / np.array(old[nm]["p"])[1:] - 1))))
    D5, SE5 = R["cases"]["J5"]["D"], R["cases"]["J5"]["SE"]; D5o, SE5o = S1["cases"]["J5"]["D"], S1["cases"]["J5"]["SE"]
    KA["KA_5"] = dict(max_dev=dev, files=nfile, D=D5, SE=SE5, D_FWN1R=D5o, SE_FWN1R=SE5o, rel_D=abs(D5 / D5o - 1), rel_SE=abs(SE5 / SE5o - 1), J5_still_fails=bool(D5 - 2 * SE5 > 4),
                      pass_=bool(dev <= 1e-6 and nfile == 48 and abs(D5 / D5o - 1) <= 1e-6 and abs(SE5 / SE5o - 1) <= 1e-6 and D5 - 2 * SE5 > 4))
    KA["KA_stored"] = dict(KA_C=bool(S1["known_answers"]["KA_C"]["pass_"]), KA_INF=bool(S1["known_answers"]["KA_INF"]["pass_"]), source="FWN1R fwn1r_grade.json (not recomputed)",
                           pass_=bool(S1["known_answers"]["KA_C"]["pass_"] and S1["known_answers"]["KA_INF"]["pass_"]))
    got = [TAB[(z, ft)]["n_above"] for z in X.ZB]; gotp = [PR[z][seeds[0]]["n_above"] for z in X.ZB]
    KA["KA_N"] = dict(mine=got, parts=gotp, JNT2=JNT2[ft], pass_=bool(got == JNT2[ft] and gotp == JNT2[ft]))
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
    fl = [v for z in PR for d in PR[z].values() for k, v in d["floored"].items()]
    KA["floored_max_primary"] = max(fl)
    R["known_answers"] = KA
    for k, v in KA.items():
        if isinstance(v, dict): P(f"[{ft}] known answer {k}: " + ("PASS" if v.get("pass_", all(v.get("pass_by_case", {}).values())) else "FAIL") + " " + json.dumps({kk: vv for kk, vv in v.items() if kk not in ("pass_", "rows")})[:600])
    worst = sorted(km.items(), key=lambda kv_: -abs(kv_[1]["realised"] - kv_[1]["expected"]) / kv_[1]["tol"])[:4]
    P(f"[{ft}] KA_M worst rows: " + "; ".join(f"{k}: {v['realised']:.5f} vs {v['expected']:.5f} (tol {v['tol']:.4f})" for k, v in worst))
    P(f"[{ft}] floored gas fraction, primary fields: max {max(fl):.2e}")
    # twins: TW-A read from FWN1R's committed grade; TW-B4 difference doubled at f = 4
    A4 = R["cases"]["J4"]["A"]; AB = Dof("TWB4", seeds, X.ANCH, ASEL)
    TW = dict(TWA_stored=dict(source="FWN1R fwn1r_grade.json (not recomputed)", **{k: S1["twins"]["TWA"][k] for k in ("D_C", "D_Jinf", "ratio", "bites")}),
              TWB4=dict(A=AB, A_J4=A4, factor=AB / A4 if A4 > 0 else float("inf"), bites=bool(A4 > 0 and AB / A4 >= 2.5)))
    # reported, not a gate: the boundary removed at f = 4 (U4 against J4), FWN1R's TW-A rule evaluated on it
    Du, SEu = R["cases"]["U4"]["D"], R["cases"]["U4"]["SE"]; D4, SE4 = R["cases"]["J4"]["D"], R["cases"]["J4"]["SE"]; rU = Du / D4 if D4 > 0 else float("inf")
    REP = dict(D_U4=Du, SE_U4=SEu, D_J4=D4, SE_J4=SE4, ratio=rU, rule_would_bite=bool((rU >= 1.25 or rU <= 0.8) and abs(Du - D4) > 2 * math.sqrt(SEu ** 2 + SE4 ** 2)), gate=False)
    R["twins"] = TW; R["reported_boundary_removed_f4"] = REP; MUT["footings"][ft] = dict(TW, reported_boundary_removed_f4=REP)
    P(f"[{ft}] twin TW-A boundary removed at f = inf (FWN1R's stored, not recomputed): D_C {TW['TWA_stored']['D_C']:.4g} vs D_Jinf {TW['TWA_stored']['D_Jinf']:.4g}, ratio {TW['TWA_stored']['ratio']:.3g} -> {'bites' if TW['TWA_stored']['bites'] else 'DOES NOT BITE'}", m=True)
    P(f"[{ft}] twin TW-B4 difference doubled at f = 4: anchors {AB:.4g} vs {A4:.4g} (x {TW['TWB4']['factor']:.3g}) -> {'bites' if TW['TWB4']['bites'] else 'DOES NOT BITE'}", m=True)
    P(f"[{ft}] REPORTED (not a gate) boundary removed at f = 4: D_U4 {Du:.4g} (SE {SEu:.3g}) vs D_J4 {D4:.4g} (SE {SE4:.3g}), ratio {rU:.3g} -> FWN1R's TW-A rule {'would bite' if REP['rule_would_bite'] else 'would NOT bite'}", m=True)
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
            P(f"[{ft}] {nm:5s} brackets (12-bin est.): " + "; ".join(f"{t} {v['est_12bin']:.4g}" for t, v in BRK[nm].items()))
    R["brackets"] = dict(seeds=bs, cases=BRK)
    # labels (FWN1R section 5)
    KLIST = ("KA_5", "KA_stored", "KA_N", "KA_F")
    kaok = all(KA[k]["pass_"] for k in KLIST) and n == 4 and seeds == [0, 1, 2, 3]
    twok = TW["TWA_stored"]["bites"] and TW["TWB4"]["bites"]
    LAB = {}; frozen_br = ("lam_x0.5", "lam_x2", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1")
    for nm in GR:
        c = R["cases"][nm]; D, SE = c["D"], c["SE"]; ok = kaok and twok and c["KA_S"]["pass_"] and KA["KA_M"]["pass_by_case"][nm]
        lab = "FOREST ROW HOLDS AT FLUX LEVEL" if (ok and D + 2 * SE < 4) else "FOREST ROW FAILS AT FLUX LEVEL" if D - 2 * SE > 4 else "NO VERDICT"
        cross = [t for t in frozen_br if t in BRK.get(nm, {}) and ((BRK[nm][t]["est_12bin"] > 4) != (D > 4))]
        if cross: lab += ", FRAGILE (" + "; ".join(cross) + ")"
        missing = [t for t in frozen_br if t not in BRK.get(nm, {})]
        fails = [k for k in KLIST if not KA[k]["pass_"]] + ([] if c["KA_S"]["pass_"] else ["KA_S"]) + ([] if KA["KA_M"]["pass_by_case"][nm] else ["KA_M"]) \
            + [k for k in ("TWA_stored", "TWB4") if not TW[k]["bites"]] + ([] if (n == 4 and seeds == [0, 1, 2, 3]) else ["seed count"])
        mr = {}
        for t in ("lam_91.4", "lam_138.6"):
            if t in BRK.get(nm, {}):
                ap = BRK[nm][t]; sc = ap["A"] / ap["A_primary_same_seeds"] if ap["A_primary_same_seeds"] > 0 else float("nan"); Dm, Sm = D * sc, SE * sc
                mr[t] = dict(D=Dm, SE=Sm, word=("HOLDS" if (ok and Dm + 2 * Sm < 4) else "FAILS" if Dm - 2 * Sm > 4 else "NO VERDICT"))
        LAB[nm] = dict(label=lab, D=D, SE=SE, known_answer_or_twin_failures=fails, missing_brackets=missing, measured_range=mr)
        P(f"[{ft}] {nm}: {lab}  (D {D:.5g}, SE {SE:.3g}; failures {fails or 'none'}; missing brackets {missing or 'none'}; measured range " + "; ".join(f"{t}: D {v['D']:.4g} -> {v['word']}" for t, v in mr.items()) + ")")
    P(f"[{ft}] control J5: D {D5:.5g} SE {SE5:.3g} -> {'FAILS' if D5 - 2 * SE5 > 4 else 'does not fail'}")
    # ceiling on f (reported): FRZ6R's f = 2, FWN1R's f = 3, 10, inf (stored), this lane's 3.5, 4, 4.5 and the recomputed 5
    g6 = json.load(open(os.path.join(X.REPO, "closure_2026_11_13", "FRZ6R_blind_forest_flux_candidate", "frz6r_grade.json")))["footings"][ft]["cases"]["J2"]
    pts = [(2.0, g6["D"], g6["SE"]), (3.0, S1["cases"]["J3"]["D"], S1["cases"]["J3"]["SE"])] + [(FV[nm], R["cases"][nm]["D"], R["cases"][nm]["SE"]) for nm in GR] \
        + [(5.0, D5, SE5), (10.0, S1["cases"]["J10"]["D"], S1["cases"]["J10"]["SE"]), (1e3, S1["cases"]["Jinf"]["D"], S1["cases"]["Jinf"]["SE"])]
    def cross_at(U):
        for (f1, u1), (f2, u2) in zip(U[:-1], U[1:]):
            if (u1 - 4) * (u2 - 4) <= 0 and u1 > 0 and u2 > 0 and u1 != u2:
                return math.exp(math.log(f1) + (math.log(4) - math.log(u1)) * (math.log(f2) - math.log(f1)) / (math.log(u2) - math.log(u1)))
        return "below 2" if U[0][1] > 4 else "above infinity point" if U[-1][1] < 4 else None
    CE = {lab_: cross_at([(f, D + k * SE) for f, D, SE in pts]) for lab_, k in (("D+2SE", 2), ("D", 0), ("D-2SE", -2))}
    R["ceiling"] = dict(points=pts, **CE)
    P(f"[{ft}] ceiling (reported, not a label): f where D + 2 SE = 4: {CE['D+2SE']}; where D = 4: {CE['D']}; where D - 2 SE = 4: {CE['D-2SE']}")
    P(f"[{ft}]   points f: D (SE): " + "; ".join(f"{f:g}: {D:.4g} ({SE:.3g})" for f, D, SE in pts))
    R["labels"] = LAB; RES["footings"][ft] = R
json.dump(RES, open(os.path.join(ODIR, "fwn2b_grade.json"), "w"), indent=1)
open(os.path.join(ODIR, "fwn2b_grade.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
json.dump(MUT, open(os.path.join(ODIR, "fwn2b_grade_MUTATE.json"), "w"), indent=1)
open(os.path.join(ODIR, "fwn2b_grade_MUTATE.out"), "w").write("\n".join(OUTM) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
