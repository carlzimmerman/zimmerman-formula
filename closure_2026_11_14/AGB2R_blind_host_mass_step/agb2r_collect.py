"""AGB2R collector: applies the checks and the frozen words (as frozen, and as amended by AMENDMENT_1.md), and Part J.

Inputs: agb2r_KG.json, agb2r_design.json (K3), agb2r_K1.json, agb2r_H.json, agb2r_J_full.json, agb2r_J_des_only.json,
and AGB1's committed agb1_A_full.json, agb1_A_des_only.json, agb1_results.json.
Writes agb2r_results.json; print to agb2r_collect.out.
"""
import json, os, sys
import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
AGB1 = os.path.join(REPO, "closure_2026_11_13", "AGB1_progenitor_age_bias")
ld = lambda p: json.load(open(p))
FINE = np.round(np.arange(-1.0, 2.0 + 1e-9, 0.001), 3)
FORKS = ("P", "median", "bins40", "measured")
FORK_NAME = {"P": "reading P", "median": "median age", "bins40": "40 bins", "measured": "sample measured"}


def w1(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"


def j2(q0, dt):
    if q0 < 0 and dt >= 4: return "ACCELERATING TODAY"
    if q0 > 0 and dt >= 4: return "DECELERATING TODAY"
    return "SIGN NOT SETTLED"


def j3(dn):
    if dn >= 9: return "NEVER-ACCELERATED EXCLUDED AT 3 SIGMA"
    if dn >= 4: return "NEVER-ACCELERATED DISFAVOURED"
    return "NEVER-ACCELERATED ALLOWED"


def spline_of(d, grid_keys):
    a = np.array(sorted(grid_keys)); return CubicSpline(a, [d[x] for x in a])


def main():
    out = {}; P = lambda m: print(m, flush=True)
    KG = ld(os.path.join(HERE, "agb2r_KG.json"))["KG"]; DS = ld(os.path.join(HERE, "agb2r_design.json"))
    K1 = ld(os.path.join(HERE, "agb2r_K1.json")); H = ld(os.path.join(HERE, "agb2r_H.json"))
    JF = {s: ld(os.path.join(HERE, f"agb2r_J_{s}.json")) for s in ("full", "des_only")}
    A1 = {s: ld(os.path.join(AGB1, f"agb1_A_{s}.json")) for s in ("full", "des_only")}
    A1R = ld(os.path.join(AGB1, "agb1_results.json"))
    K3 = DS["K3"]; K4 = H["K4"]; K2 = H["K2"]; HH = H["H"]
    # ---------------- checks ----------------
    chk = dict(KG=KG["passed"], K1=K1["passed"], K3_full=K3["passed_full"], K3_diag=K3["passed_diag"],
               K2_full=K2["full|passed"], K2_diag=K2["diag|passed"],
               K4_frozen_full=all(K4[f"full|{t}"]["passed_frozen"] for t in ("step", "host")),
               K4_amended_diag=all(K4[f"diag|{t}"]["passed_amended"] for t in ("step", "host")))
    for t in ("step", "host"):
        chk[f"K4_frozen_full_{t}"] = K4[f"full|{t}"]["passed_frozen"]; chk[f"K4_amended_diag_{t}"] = K4[f"diag|{t}"]["passed_amended"]
        chk[f"K4_amended_full_{t}"] = K4[f"full|{t}"]["passed_amended"]; chk[f"K4_frozen_diag_{t}"] = K4[f"diag|{t}"]["passed_frozen"]
    out["checks"] = chk
    P("CHECKS")
    for k, v in chk.items(): P(f"  {k:26s} {'PASS' if v else 'FAIL'}")
    evaluable = dict(full=chk["KG"] and chk["K1"] and chk["K3_full"] and chk["K4_frozen_full"],
                     diag=chk["KG"] and chk["K1"] and chk["K3_diag"] and chk["K4_amended_diag"])
    out["H_evaluable"] = evaluable
    P(f"  H evaluable as frozen (full covariance): {evaluable['full']};  as amended (diagonal): {evaluable['diag']}")
    # ---------------- Part H words ----------------
    words = {}
    for w, tag in (("full", "as frozen"), ("diag", "amendment 1")):
        k2ok = chk[f"K2_{w}"]
        for t, H_ in (("step", "H1"), ("host", "H2")):
            base = "primary" if k2ok else "P"
            d = HH[f"{w}|{t}|{base}"]; first = w1(d["D_A0"], d["D_A1"])
            fk = {f: w1(HH[f"{w}|{t}|{f}"]["D_A0"], HH[f"{w}|{t}|{f}"]["D_A1"]) for f in FORKS if f != base}
            diff = [FORK_NAME[f] for f, v in fk.items() if v != first]
            if not k2ok: second = "FRAGILE (no R)"
            else: second = "ROBUST" if not diff else "FRAGILE (" + ", ".join(diff) + ")"
            word = f"{first}, {second}" if evaluable[w] else f"NOT EVALUABLE (reading: {first}, {second})"
            words[f"{H_}|{w}"] = dict(word=word, first=first, second=second, forks=fk, judged_on=base,
                                      A=d["A"], sA=d["sA"], D_A0=d["D_A0"], D_A1=d["D_A1"], evaluable=evaluable[w], tag=tag)
            P(f"{H_} [{tag}] {word}")
            P(f"     A {d['A']:+.4f} +- {d['sA']:.4f}  dchi2(A=0) {d['D_A0']:.3f}  dchi2(A=1) {d['D_A1']:.3f}  forks: "
              + "; ".join(f"{FORK_NAME[f]} {HH[f'{w}|{t}|{f}']['A']:+.4f}+-{HH[f'{w}|{t}|{f}']['sA']:.4f} -> {v}" for f, v in fk.items()))
    out["H_words"] = words
    # ---------------- Part J ----------------
    J = {}
    prof = {s: {float(k): v for k, v in A1[s]["profile"].items() if -1.0 - 1e-9 <= float(k) <= 2.0 + 1e-9} for s in A1}
    fsp = {s: spline_of({a: v["chi2"] for a, v in prof[s].items()}, prof[s].keys()) for s in prof}
    q0g = {s: (np.array(sorted(prof[s])), np.array([prof[s][a]["q0"] for a in sorted(prof[s])])) for s in prof}
    tsp = {s: spline_of({float(k): v["chi2"] for k, v in JF[s]["t"].items()}, [float(k) for k in JF[s]["t"]]) for s in JF}
    nsp = {s: spline_of({float(k): v["chi2"] for k, v in JF[s]["n"].items()}, [float(k) for k in JF[s]["n"]]) for s in JF}
    # KJ
    kj = {}
    ok = True
    for s in ("full", "des_only"):
        fv = fsp[s](FINE); i = int(np.argmin(fv)); m = float(fv[i])
        d0 = float(fsp[s](0.0)) - m; d1 = float(fsp[s](1.0)) - m
        r0, r1 = A1R["A"][s]["D_A0"], A1R["A"][s]["D_A1"]
        a = abs(d0 - r0) <= 0.02 and abs(d1 - r1) <= 0.02
        b = all(abs(JF[s]["KJ_refit"][k]["diff"]) <= 1e-3 for k in ("+0.00", "+1.00"))
        c = True; fkv = {}
        for key, A in (("A0", 0.0), ("A1", 1.0)):
            dt_ = JF[s]["t"][f"{A:+.2f}"]["chi2"] - prof[s][A]["chi2"]; dn_ = JF[s]["n"][f"{A:+.2f}"]["chi2"] - prof[s][A]["chi2"]
            rt, rn = A1R["A"][s]["forks"][key]["D_today"], A1R["A"][s]["forks"][key]["D_never"]
            c = c and abs(dt_ - rt) <= 0.01 and abs(dn_ - rn) <= 0.01
            fkv[key] = dict(D_today=dt_, D_today_agb1=rt, D_never=dn_, D_never_agb1=rn)
        kj[s] = dict(D_A0=d0, D_A0_agb1=r0, D_A1=d1, D_A1_agb1=r1, spline_min_A=float(FINE[i]), refit=JF[s]["KJ_refit"],
                     forks=fkv, passed=bool(a and b and c), parts=[bool(a), bool(b), bool(c)])
        ok = ok and a and b and c
        P(f"KJ {s}: dchi2(A=0) {d0:.4f} (AGB1 {r0:.4f}), dchi2(A=1) {d1:.4f} (AGB1 {r1:.4f}); refit diffs "
          f"{JF[s]['KJ_refit']['+0.00']['diff']:+.1e} {JF[s]['KJ_refit']['+1.00']['diff']:+.1e}; "
          + "; ".join(f"{k}: today {v['D_today']:.4f} ({v['D_today_agb1']:.4f}) never {v['D_never']:.4f} ({v['D_never_agb1']:.4f})" for k, v in fkv.items())
          + f" -> {'PASS' if a and b and c else 'FAIL'} {kj[s]['parts']}")
    J["KJ"] = kj; J["KJ_passed"] = bool(ok)
    for w, tag in (("full", "as frozen"), ("diag", "amendment 1")):
        base = "primary" if chk[f"K2_{w}"] else "P"
        amps = {"R": (HH[f"{w}|step|{base}"]["A"], HH[f"{w}|step|{base}"]["sA"]), "P": (HH[f"{w}|step|P"]["A"], HH[f"{w}|step|P"]["sA"]),
                "H2": (HH[f"{w}|host|{base}"]["A"], HH[f"{w}|host|{base}"]["sA"])}
        evalJ = evaluable[w] and ok
        combos = {}
        for s in ("full", "des_only"):
            for lab in ("R", "P", "H2"):
                Ah, sh = amps[lab]; prior = ((FINE - Ah)/sh)**2
                cf = fsp[s](FINE) + prior; i = int(np.argmin(cf)); m = float(cf[i]); Aj = float(FINE[i])
                d0 = float(cf[np.argmin(np.abs(FINE))] - m); d1 = float(cf[np.argmin(np.abs(FINE - 1))] - m)
                lo68 = FINE[cf - m <= 1].min(); hi68 = FINE[cf - m <= 1].max(); lo95 = FINE[cf - m <= 4].min(); hi95 = FINE[cf - m <= 4].max()
                ct = tsp[s](FINE) + prior; cn = nsp[s](FINE) + prior
                dtd = float(ct.min() - m); dnv = float(cn.min() - m)
                q0J = float(np.interp(Aj, *q0g[s]))
                combos[f"{s}|{lab}"] = dict(A_H=Ah, sA_H=sh, A_joint=Aj, chi2_min=m, D_A0=d0, D_A1=d1, ci68=[float(lo68), float(hi68)],
                                           ci95=[float(lo95), float(hi95)], edge=bool(i == 0 or i == len(FINE) - 1),
                                           ci_at_edge=bool(lo95 <= -1.0 or hi95 >= 2.0),
                                           J1_first=w1(d0, d1), D_today=dtd, D_never=dnv, q0_J=q0J, J2=j2(q0J, dtd), J3=j3(dnv),
                                           A_today_min=float(FINE[int(np.argmin(ct))]), A_never_min=float(FINE[int(np.argmin(cn))]))
        pr = combos["full|R"]
        alt = {"AGB1 des_only": combos["des_only|R"]["J1_first"], "H1 reading P": combos["full|P"]["J1_first"],
               "both": combos["des_only|P"]["J1_first"]}
        diff = [k for k, v in alt.items() if v != pr["J1_first"]]
        second = "ROBUST" if not diff else "FRAGILE (" + ", ".join(diff) + ")"
        wd = dict(J1=f"{pr['J1_first']}, {second}", J2=pr["J2"], J3=pr["J3"])
        if not evalJ: wd = {k: f"NOT EVALUABLE (reading: {v})" for k, v in wd.items()}
        J[w] = dict(tag=tag, evaluable=bool(evalJ), judged_on_H1=base, words=wd, combos=combos, J1_alt=alt)
        P(f"PART J [{tag}] judged on AGB1 full with H1 {('reading R' if base == 'primary' else 'reading P')}: "
          f"A_H1 {pr['A_H']:+.4f} +- {pr['sA_H']:.4f}")
        P(f"  J1 {wd['J1']}    J2 {wd['J2']}    J3 {wd['J3']}")
        for k, c in combos.items():
            P(f"  {k:12s} A_H {c['A_H']:+.4f}+-{c['sA_H']:.4f}  joint A {c['A_joint']:+.3f} 68% [{c['ci68'][0]:+.3f}, {c['ci68'][1]:+.3f}]"
              f" 95% [{c['ci95'][0]:+.3f}, {c['ci95'][1]:+.3f}]  dchi2(0) {c['D_A0']:.3f} dchi2(1) {c['D_A1']:.3f} -> {c['J1_first']}"
              f" | q0_J {c['q0_J']:+.4f} dchi2_today {c['D_today']:.3f} -> {c['J2']} | dchi2_never {c['D_never']:.3f} -> {c['J3']}"
              f"{'  EDGE' if c['edge'] else ''}")
    out["J"] = J
    # difference between the host amplitude and AGB1's
    agb1 = A1R["A"]["full"]; dd = {}
    for w in ("full", "diag"):
        Ah, sh = HH[f"{w}|step|primary"]["A"], HH[f"{w}|step|primary"]["sA"]
        side = (agb1["ci68"][0] - agb1["A"]) if Ah < agb1["A"] else (agb1["ci68"][1] - agb1["A"])
        comb = float(np.hypot(sh, abs(side))); dd[w] = dict(A_H1=Ah, sA_H1=sh, A_AGB1=agb1["A"], sA_AGB1_side=abs(side),
                                                             diff=Ah - agb1["A"], z=(Ah - agb1["A"])/comb)
        P(f"H1 [{w}] minus AGB1 full: {Ah:+.4f} - {agb1['A']:+.4f} = {Ah - agb1['A']:+.4f}; combined error {comb:.4f}; {dd[w]['z']:+.2f} sigma")
    out["H1_minus_AGB1"] = dd
    with open(os.path.join(HERE, "agb2r_results.json"), "w") as fh: json.dump(out, fh, indent=1, default=float)
    P("wrote agb2r_results.json")


if __name__ == "__main__":
    main()
