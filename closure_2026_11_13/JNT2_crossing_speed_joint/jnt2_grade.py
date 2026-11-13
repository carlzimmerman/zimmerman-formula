#!/usr/bin/env python3
"""JNT2 (FROZEN_CRITERIA.md, e186b314ef): grade. Reads this lane's outputs and the owners' stored files (read-only); applies
section 3 (labels), section 4 (twins, known answers) and the marks of section 2.  python3 jnt2_grade.py -> jnt2_grade.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, warnings
warnings.filterwarnings("ignore"); sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2_common as C
def J(*p): return json.load(open(os.path.join(*p)))
def Jh(n): return J(HERE, n)
SRJ2 = os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint"); SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
FZS = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
FG = (0.75, 1.0, 1.25, 1.5, 2.0, 3.0); FOOTS = ("canonical", "alt")
LE = {m: Jh("jnt2_lens.json" if m == "main" else f"jnt2_lens_MUTATE_{m}.json") for m in C.MODES}
RC = {m: Jh("jnt2_rc.json" if m == "main" else f"jnt2_rc_MUTATE_{m}.json") for m in C.MODES}
CL = {m: Jh("jnt2_clusters.json" if m == "main" else f"jnt2_clusters_MUTATE_{m}.json") for m in C.MODES}
SRHL = J(SRH, "srh1_lens.json"); SRJL = J(SRJ2, "srj2_lens.json")
def early(cfg): return cfg["gate"]["lines"]["G-K1 early"]["z"]
def zs(cfg): L = cfg["gate"]["lines"]; return [L["G-K1 all"]["z"], L["G-K1 late"]["z"], L["G-K1 early"]["z"], L["G-K3 type difference"]["z"]], L["G-K2 all profile"]["chi2"]
def rows_at(ft, f, m):
    """the row words at f for mode m (only where the mode was run)."""
    k = f"f{f:.2f}"; o = {}
    FO = Jh(f"jnt2_forest_{ft}.json" if m == "main" else f"jnt2_forest_{ft}_MUTATE_{m}.json")["cases"]
    if k in FO: o["G1"] = dict(stat=FO[k]["dchi2"], pass_=FO[k]["dchi2"] <= 4)
    r = RC[m]["foot"][ft]
    if f"G2_model_{k}" in r["RC100"]: o["G2"] = dict(stat=r["RC100"][f"G2_model_{k}"]["covered"], pass_=r["RC100"][f"G2_model_{k}"]["pass_"])
    if k in r["G3"]: o["G3"] = dict(stat=r["G3"][k]["b"]["all"]["rms"], pass_=r["G3"][k]["pass_"])
    c = CL[m]["foot"][ft].get(f"model_{k}")
    if c: o["C"] = dict(stat=dict(q=c["a_last"][0], bins=c["b_bins"], gq=c["c"][0]), pass_=c["labels"]["a_last"] == "CONSISTENT" and c["labels"]["b"] == "CONSISTENT" and c["labels"]["c"] == "CONSISTENT",
                        R500=c["labels"]["a_R500"], xlaw=c["n_xcop_law"], glaw=c["n_groups_law"], d_ref=c["max_diff_from_reference"])
    lc = LE[m]["cfg"].get(f"{ft}|{k}")
    if lc: o["G4"] = dict(stat=early(lc), pass_=lc["gate"]["status"] == "PASS", z=zs(lc))
    return o
RES = dict(lane="JNT2", criteria="e186b314ef", foot={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
for ft in FOOTS:
    R = RES["foot"][ft] = {}; P(f"\n[{ft}] ================================================")
    T = {f: rows_at(ft, f, "main") for f in FG}; R["table"] = {f"{f:.2f}": T[f] for f in FG}
    # marks
    lf0 = LE["main"]["cfg"][f"{ft}|f0"]; z0, c0 = zs(lf0)
    marks = {}
    for f in FG:
        t = T[f]; mk = {}
        mk["G1"] = "TRIVIAL" if t["G1"]["stat"] < 1 else ""
        zf, cf = t["G4"]["z"]; triv4 = max(abs(a - b) for a, b in zip(zf, z0)) <= 0.10 and abs(cf - c0) <= 0.10
        sk = f"{ft}|f{f:.2f}"; eq4 = None
        if sk in SRHL["cfg"]: zh, ch = zs(SRHL["cfg"][sk]); eq4 = max(abs(a - b) for a, b in zip(zf, zh)) <= 0.10 and abs(cf - ch) <= 0.10
        mk["G4"] = "TRIVIAL" if triv4 else ("EQUAL TO THE LAW" if eq4 else ("not compared (SRH1 has no f 3)" if eq4 is None else ""))
        rc = RC["main"]["foot"][ft]; mk["G3"] = "EQUAL TO THE LAW" if rc["SPARC"]["n_above_model"] == 0 and rc["SPARC"]["n_above_measured"] == 0 else ""
        mk["C"] = ("X-COP TRIVIAL" if t["C"]["xlaw"] == 0 else f"X-COP law in {t['C']['xlaw']}") + "; " + ("groups EQUAL TO THE LAW" if t["C"]["glaw"] == 20 else f"groups law in {t['C']['glaw']} / 20")
        mk["G2"] = "coverage only; data above v*: NO POWER (SRJ3)"
        marks[f"{f:.2f}"] = mk
    R["marks"] = marks
    for f in FG:
        t = T[f]; mk = marks[f"{f:.2f}"]
        P(f"[{ft}] f {f:.2f}: G1 {t['G1']['stat']:.3f} {'P' if t['G1']['pass_'] else 'F'} {mk['G1']} | G2 covered {t['G2']['stat']} {'P' if t['G2']['pass_'] else 'F'} | G3 {'P' if t['G3']['pass_'] else 'F'} {mk['G3']} | "
          f"C q {t['C']['stat']['q']:.3f}, shape " + "/".join(f"{x:+.3f}" for x in t['C']['stat']['bins']) + f", groups {t['C']['stat']['gq']:.3f} {'P' if t['C']['pass_'] else 'F'} (R500 {t['C']['R500']}) {mk['C']} | "
          f"G4 early {t['G4']['stat']:+.3f} {'P' if t['G4']['pass_'] else 'F'} {mk['G4']}")
    # known answers
    KA = {}
    KA["KA3"] = dict(v=C.vstar0_kms(ft), pass_=round(C.vstar0_kms(ft)) == {"canonical": 669, "alt": 808}[ft])
    fo = Jh(f"jnt2_forest_{ft}.json")["cases"]; KA["KA0_G1"] = dict(v=fo["KA_0"]["dchi2"], pass_=abs(fo["KA_0"]["dchi2"]) <= 1e-10)
    zm, cm = zs(lf0); zh, ch = zs(SRHL["cfg"][f"{ft}|f0"]); KA["KA0_G4"] = dict(v=max(abs(a - b) for a, b in zip(zm, zh)), pass_=max(abs(a - b) for a, b in zip(zm, zh)) <= 0.005 and abs(cm - ch) <= 0.01)
    KA["KA0_C"] = dict(v=CL["main"]["foot"][ft]["KA0"]["max_dev"], pass_=CL["main"]["foot"][ft]["KA0"]["pass_"])
    s1 = Jh(f"jnt2_forest_{ft}_MUTATE_S.json")["cases"]["f1.00"]["dchi2"]; s1r = J(SRJ2, f"srj2_forest_{ft}.json")["cases"]["on_f1.00"]["dchi2"]
    zS, cS = zs(LE["S"]["cfg"][f"{ft}|f1.00"]); zR, cR = zs(SRJL["cfg"][f"{ft}|on_f1.00"])
    KA["KA1"] = dict(G1=s1, G1_srj2=s1r, G4_dev=max(abs(a - b) for a, b in zip(zS, zR)), pass_=abs(s1 / s1r - 1) <= 1e-6 and max(abs(a - b) for a, b in zip(zS, zR)) <= 0.005 and abs(cS - cR) <= 0.01)
    o1 = Jh(f"jnt2_forest_{ft}_MUTATE_0.json")["cases"]["f1.00"]["dchi2"]; o1r = J(FZS, f"fzs1_forest_{ft}.json")["cases"]["primary"]["dchi2"]
    z0_, c0_ = zs(LE["0"]["cfg"][f"{ft}|f1.00"]); zH, cH = zs(SRHL["cfg"][f"{ft}|f1.00"])
    KA["KA2"] = dict(G1=o1, G1_fzs1=o1r, G4_dev=max(abs(a - b) for a, b in zip(z0_, zH)), pass_=abs(o1 - o1r) <= 0.01 and max(abs(a - b) for a, b in zip(z0_, zH)) <= 0.005 and abs(c0_ - cH) <= 0.01)
    R["KA"] = KA
    P(f"[{ft}] known answers: " + "; ".join(f"{k} {'PASS' if v['pass_'] else 'FAIL'}" for k, v in KA.items()) + f" (v* {C.vstar0_kms(ft):.2f} km/s; TW-S G1 {s1:.6f} vs SRJ2 {s1r:.6f}; TW-0 G1 {o1:.3f} vs FZS1 {o1r:.3f})")
    # TW-S and TW-0 words
    tS = rows_at(ft, 1.0, "S"); t0 = rows_at(ft, 1.0, "0")
    nS = RC["S"]["foot"][ft]["RC100"]["n_above_model"]
    twS = dict(G2_n=nS, G2_fail=not tS["G2"]["pass_"], G4_fail=not tS["G4"]["pass_"], G1_trivial_hold=tS["G1"]["stat"] < 1, C_trivial=tS["C"]["xlaw"] == 0 and tS["C"]["glaw"] == 0 and tS["C"]["pass_"])
    twS["reproduces"] = bool(nS == {"canonical": 31, "alt": 22}[ft] and twS["G2_fail"] and twS["G4_fail"] and twS["G1_trivial_hold"] and twS["C_trivial"])
    tw0 = dict(G1_fail=not t0["G1"]["pass_"], G4_fail=not t0["G4"]["pass_"], C_shape=CL["0"]["foot"][ft]["model_f1.00"]["labels"]["b"])
    tw0["reproduces"] = bool(tw0["G1_fail"] and tw0["G4_fail"] and tw0["C_shape"] == "FAILS")
    R["TW_S"], R["TW_0"] = twS, tw0
    P(f"[{ft}] TW-S (v_stiff, SRJ2 membership): {twS} -> {'reproduces SRJ2' if twS['reproduces'] else 'DOES NOT REPRODUCE'}")
    P(f"[{ft}] TW-0 (no boundary): {tw0} -> {'reproduces SRH1 / SRJ1' if tw0['reproduces'] else 'DOES NOT REPRODUCE'}")
    # TW-H, TW-D bite
    for m in ("H", "D"):
        bites = []; det = {}
        for f in (1.25, 2.0):
            a, b = rows_at(ft, f, "main"), rows_at(ft, f, m)
            for row in ("G1", "G2", "G3", "C", "G4"):
                if row in a and row in b and a[row]["pass_"] != b[row]["pass_"]: bites.append(f"{row} word at f {f}")
            d1 = abs(a["G1"]["stat"] - b["G1"]["stat"]); d4 = abs(a["G4"]["stat"] - b["G4"]["stat"])
            dq = abs(a["C"]["stat"]["q"] - b["C"]["stat"]["q"]); dg = abs(a["C"]["stat"]["gq"] - b["C"]["stat"]["gq"])
            db = max(abs(x - y) for x, y in zip(a["C"]["stat"]["bins"], b["C"]["stat"]["bins"]) if math.isfinite(x) and math.isfinite(y))
            if d1 > 1: bites.append(f"G1 moves {d1:.2f} at f {f}")
            if d4 > 0.10: bites.append(f"G4 early moves {d4:.3f} at f {f}")
            if dq > 0.02 or dg > 0.02: bites.append(f"C q moves {max(dq, dg):.3f} at f {f}")
            if db > 0.05: bites.append(f"C shape bin moves {db:.3f} at f {f}")
            det[f"f{f:.2f}"] = dict(dG1=d1, dG4=d4, dq=dq, dgq=dg, dbin=db, G2_covered=(a["G2"]["stat"], b["G2"]["stat"]), words={r: (a[r]["pass_"], b[r]["pass_"]) for r in a if r in b})
        R[f"TW_{m}"] = dict(bites=bool(bites), why=bites, detail=det)
        P(f"[{ft}] TW-{m} ({'v*/2' if m == 'H' else '2 v*'}): {'bites: ' + '; '.join(bites) if bites else 'DOES NOT BITE'} | " + "; ".join(f"{k}: dG1 {v['dG1']:.3f}, dG4 {v['dG4']:.3f}, dq {v['dq']:.3f}, dgq {v['dgq']:.3f}, dbin {v['dbin']:.3f}, G2 covered {v['G2_covered']}" for k, v in det.items()))
    # label
    ok_checks = all(v["pass_"] for v in KA.values()) and twS["reproduces"] and tw0["reproduces"] and R["TW_H"]["bites"] and R["TW_D"]["bites"]
    allfail = [row for row in ("G1", "G2", "G3", "C", "G4") if all(not T[f][row]["pass_"] for f in FG)]
    win = [f for f in FG if all(T[f][row]["pass_"] for row in ("G1", "G2", "G3", "C", "G4"))]
    win_noG2 = [f for f in FG if all(T[f][row]["pass_"] for row in ("G1", "G3", "C", "G4"))]
    if not ok_checks: lab = "NO VERDICT"
    elif allfail: lab = "JOINT FAILS ON " + ", ".join(r + (" (coverage)" if r == "G2" else " (data)") for r in allfail)
    elif win: lab = f"JOINT COMPLETE ON POWERED ROWS [{win[0]}, {win[-1]}]" + ("" if len(win) == FG.index(win[-1]) - FG.index(win[0]) + 1 else f" (grid points {win})")
    else: lab = "JOINT FAILS (no common f): " + ", ".join(r for r in ("G1", "G2", "G3", "C", "G4"))
    # measured-rule bracket (FRAGILE)
    rcm = RC["main"]["foot"][ft]; frag = []
    for f in FG:
        k = f"f{f:.2f}"
        if rcm["RC100"][f"G2_measured_{k}"]["pass_"] != T[f]["G2"]["pass_"]: frag.append(f"G2 at f {f}")
        if rcm["SPARC"][f"G3a_measured_{k}"]["pass_"] != rcm["SPARC"][f"G3a_model_{k}"]["pass_"]: frag.append(f"G3(a) at f {f}")
        cm = CL["main"]["foot"][ft][f"measured_{k}"]["labels"]; cmo = CL["main"]["foot"][ft][f"model_{k}"]["labels"]
        if any(cm[x] != cmo[x] for x in ("a_last", "b", "c")): frag.append(f"C at f {f}")
    R.update(label=lab, checks_ok=ok_checks, rows_failing_every_f=allfail, window=win, window_without_G2=win_noG2, fragile_measured=frag)
    P(f"[{ft}] LABEL: {lab}; window without G2 (reported): {win_noG2}; measured-rule FRAGILE: {frag or 'none'}")
json.dump(RES, open(os.path.join(HERE, "jnt2_grade.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "jnt2_grade.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
