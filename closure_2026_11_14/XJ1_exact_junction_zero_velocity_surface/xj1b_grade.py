#!/usr/bin/env python3
"""XJ1 build B grader (FROZEN_CRITERIA.md ef8ccdde98 sections 4 to 6, AMENDMENT_A1 38c6539631). COPY of FWN1R's fwn1r_grade.py
(closure_2026_11_14/FWN1R_blind_split_f_ceiling) with the case list changed to E1, E2, E3, Ezv, the control J5 compared
with FWN1R's stored parts and grade file (KA-5), KA-C / KA-INF / TW-A read from FWN1R's committed grade file, TW-B at E3,
KA-E / KA-Z read from xj1_ka_tables.json, and the junction comparison against FRZ6R's J2 and FWN1R's J3 (reported).
Reads parts_b/*.json. Footings never pooled.
  nice -n 19 python3 -I -B xj1b_grade.py -> xj1b_grade.json / .out, xj1b_grade_MUTATE.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import cho_solve
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ODIR = os.environ.get("XJ1B_ODIR") or HERE
import xj1_lib as XL
X = XL.X
PARTS = os.environ.get("XJ1B_PARTS") or os.path.join(HERE, "parts_b")
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
KAT = json.load(open(os.path.join(HERE, "xj1_ka_tables.json")))
GR = ["E1", "E2", "E3", "Ezv"]; FOF = {"E1": 1.0, "E2": 2.0, "E3": 3.0}

def load(stage, ft):
    out = {}
    for f in sorted(glob.glob(os.path.join(PARTS, f"{stage}_z*_s*_{ft}.json"))):
        d = json.load(open(f))
        if stage == "br" and d["seed"] in out.get(d["z"], {}):                     # one file per bracket: merge
            e = out[d["z"]][d["seed"]]; e["flux"].update(d["flux"]); e["floored"].update(d["floored"]); continue
        out.setdefault(d["z"], {})[d["seed"]] = d
    return out

RES = dict(lane="XJ1", build="B (FWN1R's library)", criteria="ef8ccdde98", amendment="38c6539631", md5_ok=MD5OK,
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", footings={})
MUT = dict(lane="XJ1", note=RES["note"], footings={})
for ft in X.FOOTS:
    PR = load("prim", ft); BR = load("br", ft)
    have = [set(PR.get(z, {}).keys()) for z in X.ZB]
    seeds = sorted(set.intersection(*have)) if all(have) else []; n = len(seeds)
    R = dict(seeds=seeds, n=n, cases={})
    P(f"[{ft}] seeds in all 12 bins: {seeds}")
    if n < 4:
        P(f"[{ft}] fewer than 4 seeds in all 12 bins: every case NO VERDICT (seed count); nothing graded"); R["labels"] = {nm: dict(label="NO VERDICT (seed count)") for nm in GR}
        RES["footings"][ft] = R; continue
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
    for nm in GR + ["J5"]:
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
        if nm in GR:
            P(f"[{ft}] {nm:4s} t (min, max) / s (min, max) / share capped at r_ta, z 2.2, 3.0, 4.4: " + "; ".join(
                f"z {zz}: t {li[zz]['t_min_max']}, s {li[zz]['s_min_max']}, capped {li[zz]['frac_capped_at_rta']}" if li.get(zz) else f"z {zz}: -" for zz in ("2.2", "3.0", "4.4")))
    KA = {}
    # KA-5: R and J5 against FWN1R's stored parts; J5's D, SE against FWN1R's grade file; J5 still fails
    dev = 0.0; nfile = 0
    for z in X.ZB:
        for s in seeds:
            old = json.load(open(os.path.join(FWN1R_PARTS, f"prim_z{z:.1f}_s{s}_{ft}.json")))["flux"]["primary"]; nfile += 1
            for nm in ("R", "J5"):
                dev = max(dev, float(np.max(np.abs(np.array(PR[z][s]["flux"]["primary"][nm]["p"])[1:] / np.array(old[nm]["p"])[1:] - 1))))
    D5, SE5 = R["cases"]["J5"]["D"], R["cases"]["J5"]["SE"]; o5 = FWN1R_G[ft]["cases"]["J5"]
    KA["KA_5"] = dict(max_dev=dev, files=nfile, D=D5, SE=SE5, FWN1R_D=o5["D"], FWN1R_SE=o5["SE"], rel_D=D5 / o5["D"] - 1, rel_SE=SE5 / o5["SE"] - 1, control_fails=bool(D5 - 2 * SE5 > 4),
                      pass_=bool(dev <= 1e-6 and nfile == 48 and abs(D5 / o5["D"] - 1) <= 1e-6 and abs(SE5 / o5["SE"] - 1) <= 1e-6 and D5 - 2 * SE5 > 4))
    ok_ = FWN1R_G[ft]["known_answers"]
    KA["KA_C"] = dict(read_from="fwn1r_grade.json", pass_=bool(ok_["KA_C"]["pass_"]), D=ok_["KA_C"]["D"], SE=ok_["KA_C"]["SE"])
    KA["KA_INF"] = dict(read_from="fwn1r_grade.json", pass_=bool(ok_["KA_INF"]["pass_"]))
    gotp = [PR[z][seeds[0]]["n_above"] for z in X.ZB]; gott = [321 - KAT["KA_E"][f"{ft}|{z}"]["n_below"] for z in X.ZB]
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
    KA["KA_E"] = dict(read_from="xj1_ka_tables.json (AMENDMENT_A1 tolerance on iv)", pass_=bool(all(KAT["KA_E"][f"{ft}|{z}"]["pass_"] for z in X.ZB)),
                      worst_t_min=min(KAT["KA_E"][f"{ft}|{z}"]["tmin"] for z in X.ZB))
    KA["KA_Z"] = dict(read_from="xj1_ka_tables.json", pass_=bool(KAT["KA_Z"]["pass_"]), i_max_rel=KAT["KA_Z"]["i_max_rel"], ii_max_abs_kpc=KAT["KA_Z"]["ii_max_abs_kpc"])
    fl = [v for z in PR for d in PR[z].values() for k, v in d["floored"].items()]
    KA["floored_max_primary"] = max(fl)
    R["known_answers"] = KA
    for k, v in KA.items():
        if isinstance(v, dict): P(f"[{ft}] known answer {k}: " + ("PASS" if v.get("pass_", all(v.get("pass_by_case", {}).values())) else "FAIL") + " " + json.dumps({kk: vv for kk, vv in v.items() if kk not in ("pass_", "rows")})[:600])
    worst = sorted(km.items(), key=lambda kv_: -abs(kv_[1]["realised"] - kv_[1]["expected"]) / kv_[1]["tol"])[:6]
    P(f"[{ft}] KA_M worst rows: " + "; ".join(f"{k}: {v['realised']:.5f} vs {v['expected']:.5f} (tol {v['tol']:.4f})" for k, v in worst))
    P(f"[{ft}] floored gas fraction, primary fields: max {max(fl):.2e}")
    # twins
    A3 = R["cases"]["E3"]["A"]; AB = Dof("TWB", seeds, X.ANCH, ASEL); twa = FWN1R_G[ft]["twins"]["TWA"]
    TW = dict(TWA=dict(read_from="fwn1r_grade.json", bites=bool(twa["bites"]), ratio=twa["ratio"]),
              TWB=dict(A=AB, A_E3=A3, factor=AB / A3 if A3 > 0 else float("inf"), bites=bool(A3 > 0 and AB / A3 >= 2.5)))
    R["twins"] = TW; MUT["footings"][ft] = TW
    P(f"[{ft}] twin TW-A boundary removed at f = inf (read from FWN1R's grade file): ratio {twa['ratio']:.3g} -> {'bites' if TW['TWA']['bites'] else 'DOES NOT BITE'}", m=True)
    P(f"[{ft}] twin TW-B difference doubled at E3: anchors {AB:.4g} vs {A3:.4g} (x {TW['TWB']['factor']:.3g}) -> {'bites' if TW['TWB']['bites'] else 'DOES NOT BITE'}", m=True)
    # the junction's own effect (reported, not a gate): E2 against FRZ6R's J2, E3 against FWN1R's J3
    j2 = FRZ6R_G[ft]["cases"]["J2"]; j3 = FWN1R_G[ft]["cases"]["J3"]; JC = {}
    for nm, old, src in (("E2", j2, "FRZ6R J2"), ("E3", j3, "FWN1R J3")):
        D, SE = R["cases"][nm]["D"], R["cases"][nm]["SE"]; r_ = D / old["D"] if old["D"] > 0 else float("inf")
        JC[nm] = dict(D_E=D, SE_E=SE, D_J=old["D"], SE_J=old["SE"], source=src, ratio=r_, bites=bool((r_ >= 1.25 or r_ <= 0.8) and abs(D - old["D"]) > 2 * math.sqrt(SE ** 2 + old["SE"] ** 2)))
        P(f"[{ft}] junction comparison at {nm[1]} R_fold (reported): exact {D:.5g} (SE {SE:.3g}) vs FZS1's {old['D']:.5g} (SE {old['SE']:.3g}; {src}), ratio {r_:.3g} -> {'differs' if JC[nm]['bites'] else 'does not differ'}")
    R["junction_comparison"] = JC
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
    kaok = all(KA[k]["pass_"] for k in ("KA_5", "KA_C", "KA_INF", "KA_N", "KA_F", "KA_E", "KA_Z"))
    twok = TW["TWA"]["bites"] and TW["TWB"]["bites"]
    LAB = {}; frozen_br = ("lam_x0.5", "lam_x2", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1")
    for nm in GR:
        c = R["cases"][nm]; D, SE = c["D"], c["SE"]; ok = kaok and twok and c["KA_S"]["pass_"] and KA["KA_M"]["pass_by_case"][nm]
        lab = "FOREST ROW HOLDS AT FLUX LEVEL" if (ok and D + 2 * SE < 4) else "FOREST ROW FAILS AT FLUX LEVEL" if D - 2 * SE > 4 else "NO VERDICT"
        cross = [t for t in frozen_br if t in BRK.get(nm, {}) and ((BRK[nm][t]["est_12bin"] > 4) != (D > 4))]
        if cross: lab += ", FRAGILE (" + "; ".join(cross) + ")"
        missing = [t for t in frozen_br if t not in BRK.get(nm, {})]
        fails = [k for k in ("KA_5", "KA_C", "KA_INF", "KA_N", "KA_F", "KA_E", "KA_Z") if not KA[k]["pass_"]] + ([] if c["KA_S"]["pass_"] else ["KA_S"]) + ([] if KA["KA_M"]["pass_by_case"][nm] else ["KA_M"]) \
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
    P(f"[{ft}] control J5: D {D5:.5g} SE {SE5:.3g} -> {'FAILS' if D5 - 2 * SE5 > 4 else 'does not fail'}")
    # lane words
    w = lambda nm: LAB[nm]["label"]
    held = [f"{nm[1]}" + (" (" + w(nm).split(", ", 1)[1] + ")" if ", FRAGILE" in w(nm) else "") for nm in ("E2", "E3") if w(nm).startswith("FOREST ROW HOLDS")]
    if held: q1 = "THE HOLD SURVIVES THE EXACT JUNCTION AT f = " + ", ".join(held)
    elif all(w(nm).startswith("FOREST ROW FAILS") for nm in ("E2", "E3")): q1 = "THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION"
    else: q1 = "NOT RESOLVED (E2: " + w("E2") + "; E3: " + w("E3") + ")"
    q2 = {}
    for nm, surf in (("E1", "the fold radius"), ("Ezv", "the zero-velocity surface")):
        q2[nm] = (f"HOLDS WITH NO FREE CONSTANT ({surf})" + (", " + w(nm).split(", ", 1)[1] if ", FRAGILE" in w(nm) else "")) if w(nm).startswith("FOREST ROW HOLDS") else \
                 (f"FAILS ({surf})" + (", " + w(nm).split(", ", 1)[1] if ", FRAGILE" in w(nm) else "")) if w(nm).startswith("FOREST ROW FAILS") else f"NOT RESOLVED ({surf}): " + w(nm)
    R["lane_words"] = dict(Q1=q1, Q2=q2)
    P(f"[{ft}] Q1, the junction: {q1}")
    for nm in q2: P(f"[{ft}] Q2, {nm}: {q2[nm]}")
    # D against f for the exact junction (reported)
    pts = [(FOF[nm], R["cases"][nm]["D"], R["cases"][nm]["SE"]) for nm in ("E1", "E2", "E3")]
    def cross_at(U):
        for (f1, u1), (f2, u2) in zip(U[:-1], U[1:]):
            if (u1 - 4) * (u2 - 4) <= 0 and u1 > 0 and u2 > 0 and u1 != u2:
                return math.exp(math.log(f1) + (math.log(4) - math.log(u1)) * (math.log(f2) - math.log(f1)) / (math.log(u2) - math.log(u1)))
        return "below 1" if U[0][1] > 4 else "above 3" if U[-1][1] < 4 else None
    R["ceiling_exact_junction"] = dict(points=pts, **{lab_: cross_at([(f, D + k * SE) for f, D, SE in pts]) for lab_, k in (("D+2SE", 2), ("D", 0), ("D-2SE", -2))})
    P(f"[{ft}] exact junction, f where D + 2 SE / D / D - 2 SE reaches 4 (reported): {R['ceiling_exact_junction']['D+2SE']} / {R['ceiling_exact_junction']['D']} / {R['ceiling_exact_junction']['D-2SE']}")
    R["labels"] = LAB; RES["footings"][ft] = R
json.dump(RES, open(os.path.join(ODIR, "xj1b_grade.json"), "w"), indent=1)
open(os.path.join(ODIR, "xj1b_grade.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
json.dump(MUT, open(os.path.join(ODIR, "xj1b_grade_MUTATE.json"), "w"), indent=1)
open(os.path.join(ODIR, "xj1b_grade_MUTATE.out"), "w").write("\n".join(OUTM) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
