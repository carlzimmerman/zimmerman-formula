#!/usr/bin/env python3
"""CFG593 verdict (FROZEN_CRITERIA.md sections 4-6): overlap of the shear-allowed (a) and KiDS-allowed (b) regions of the declared profile
family, per footing; side constraints (c); convention flags; closest point; record rules.  Reads cfg593_{shear,kids,side}_results.json.
  nice -n 10 python3 cfg593_verdict.py -> cfg593_verdict.out, cfg593_verdict_results.json
DIAGNOSTIC, data-driven: an allowed profile is what the data require, NOT a framework derivation.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1")
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg593_lib as FL
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

JS = json.load(open(os.path.join(HERE, "cfg593_shear_results.json")))
JK = json.load(open(os.path.join(HERE, "cfg593_kids_results.json")))
JC = json.load(open(os.path.join(HERE, "cfg593_side_results.json")))
FOOTS = ("canonical", "alt")
PTS = FL.family_points()
X2C = float(stats.chi2.isf(0.01, 15))
key = lambda xe, f, y: f"{xe:.2f}|{f:.1f}|{y}"
P("CFG593 verdict -- FROZEN_CRITERIA.md. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
P("DIAGNOSTIC, data-driven: an allowed profile is what the data require, NOT a framework derivation.")
P(f"controls: shear {JS['controls']}; KiDS K3i {JK['controls']['K3i']:.1e} K3ii {JK['controls']['K3ii']} K3iii {JK['controls']['K3iii']:.1e}; side {JC['controls']}")
ctl_ok = JS["controls"]["K1_pass"] and JS["controls"]["K2_pass"] and JS["controls"]["K5_pass"] and JK["controls"]["K3i_pass"] and JK["controls"]["K3ii_pass"] \
    and JK["controls"]["K3iii_pass"] and JC["controls"]["K4_pass"] and JC["controls"]["KMW_pass"]
P(f"all load-bearing controls pass: {ctl_ok}")


def region(ft, bary="cen", band="fid", kconv="total", sconv="total"):
    A, B, C, rows = set(), set(), set(), {}
    for (xe, f, y) in PTS:
        k = key(xe, f, y)
        s = JS["scan"][f"{ft}|{bary}|{k}"]; kd = JK["scan"][f"{ft}|{kconv}|{k}"]; sd = JC["scan"][f"{ft}|{sconv}|{k}"]
        a = s["allowed_fid"] if band == "fid" else s["allowed_full"]
        zs = s["Zmax_best_fid"] if band == "fid" else s["Zmax_best_full"]
        x2 = max(kd["chi2_A"], kd["chi2_B"])
        if a: A.add(k)
        if kd["allowed"]: B.add(k)
        if sd["allowed"]: C.add(k)
        rows[k] = dict(xe=xe, f=f, y=y, Zs=zs, x2=x2, dist=max(zs / 2.0, x2 / X2C), groups_Z=sd["groups_Z"], mw_pass=sd["mw_pass"])
    return A, B, C, rows


res = dict(lane="CFG593", script="cfg593_verdict", date="2026-10-10", chi2_crit_p001=X2C, controls_pass=bool(ctl_ok), footings={})
VARS = {"PRIMARY": {}, "baryons to r_ta (shear)": dict(bary="emg"), "KiDS lane convention": dict(kconv="lane"),
        "full feedback band 7.3-8.3": dict(band="full"), "groups lane convention": dict(sconv="lane")}
for ft in FOOTS:
    P(f"\n===================== footing {ft} =====================")
    out = {}
    for vn, kw in VARS.items():
        A, B, C, rows = region(ft, **kw)
        Oab = sorted(A & B); Oabc = sorted(A & B & C)
        best = min(rows.values(), key=lambda r: r["dist"])
        out[vn] = dict(n_shear=len(A), n_kids=len(B), n_side=len(C), overlap_ab=Oab, overlap_abc=Oabc, OVERLAP=bool(Oab),
                       closest=best, n_points=len(PTS))
        P(f"  [{vn:28s}] shear-allowed {len(A):3d}, KiDS-allowed {len(B):3d}, side-allowed {len(C):3d}, of {len(PTS)};  overlap (a)&(b) {len(Oab)}; with (c) {len(Oabc)}"
          f" -> {'OVERLAP' if Oab else 'NO OVERLAP'}; closest point x_e {best['xe']} f {best['f']} y {best['y']}: Zmax {best['Zs']:.2f} (need < 2), "
          f"max chi2 {best['x2']:.2f} (need < {X2C:.2f}), groups Z {best['groups_Z']:+.2f}, MW {best['mw_pass']}")
    prim = out["PRIMARY"]
    sens = sorted(vn for vn, o in out.items() if vn != "PRIMARY" and o["OVERLAP"] != prim["OVERLAP"])
    verdict = ("OVERLAP" if prim["OVERLAP"] else "NO OVERLAP") + (" (CONVENTION-SENSITIVE: " + ", ".join(sens) + ")" if sens else "")
    P(f"  VERDICT [{ft}]: {verdict}")
    # where each constraint sits (PRIMARY): the KiDS-allowed and shear-allowed sets in (x_e, f, y)
    A, B, C, rows = region(ft)
    def summ(S):
        if not S:
            return "none"
        xs = sorted({rows[k]["xe"] for k in S}); fs = sorted({rows[k]["f"] for k in S}); ys = sorted({rows[k]["y"] for k in S})
        return f"x_e {xs[0]}-{xs[-1]}, f {fs[0]}-{fs[-1]}, y {ys}"
    P(f"  shear-allowed: {summ(A)};  KiDS-allowed: {summ(B)};  side-allowed: {summ(C)}")
    # f = 1 content
    f1 = [k for k in prim["overlap_ab"] if rows[k]["f"] == 1.0]
    # closest shear-allowed point to KiDS, and closest KiDS-allowed point to shear
    sa_best = min((rows[k] for k in A), key=lambda r: r["x2"]) if A else None
    ka_best = min((rows[k] for k in B), key=lambda r: r["Zs"]) if B else None
    if sa_best:
        P(f"  best KiDS fit inside the shear-allowed region: x_e {sa_best['xe']} f {sa_best['f']} y {sa_best['y']}: max chi2 {sa_best['x2']:.2f} (p {stats.chi2.sf(sa_best['x2'], 15):.1e})")
    if ka_best:
        P(f"  best shear inside the KiDS-allowed region: x_e {ka_best['xe']} f {ka_best['f']} y {ka_best['y']}: Zmax {ka_best['Zs']:.2f}")
    # overlap profile description
    desc = {}
    if prim["overlap_ab"]:
        ov = [rows[k] for k in prim["overlap_ab"]]
        rep = min(ov, key=lambda r: r["dist"])
        rp = (rep["xe"], rep["f"], rep["y"])
        H = FL.H556(); MTA = H["MTA"]; LM = H["LM"]
        prof = {}
        for lt in (12, 13, 14, 15):
            hb = H["halo_basics"](10 ** np.interp(lt, np.log10(MTA), LM))
            r, M, inf = FL.hm_profile(hb, ft, *rp)
            prof[str(lt)] = dict(ratios={str(x): float(np.interp(x * hb["rta"], r, M) / H["M_L"](hb, x * hb["rta"])) for x in (0.05, 0.1, 0.2, 0.3, 0.5)},
                                 q=inf["q"], re_over_rta=inf["re_over_rta"], rin_over_rta=inf["rin"] / hb["rta"], r200m_over_rta=hb["r200"] / hb["rta"],
                                 capped_supply=bool(inf.get("capped_supply", False)))
            P(f"    representative overlap point {rp}: log M_ta {lt}: M/M_L at 0.05/0.1/0.2/0.3/0.5 r_ta = "
              + " ".join(f"{v:.2f}" for v in prof[str(lt)]["ratios"].values()) + f"; r_e/r_ta {inf['re_over_rta']:.3f}, r_in/r_ta {inf['rin'] / hb['rta']:.3f}, "
              f"r200m/r_ta {hb['r200'] / hb['rta']:.3f}, drained-shell depth q {inf['q']:+.3f}")
        desc = dict(representative=rp, profiles=prof, xe_range=[min(r["xe"] for r in ov), max(r["xe"] for r in ov)],
                    f_range=[min(r["f"] for r in ov), max(r["f"] for r in ov)], y_values=sorted({r["y"] for r in ov}), contains_f1=bool(f1))
        P(f"  overlap: x_e {desc['xe_range']}, f {desc['f_range']}, y {desc['y_values']}; contains a fully settled (f = 1) point: {bool(f1)}")
    # record rules
    rec = {}
    pairs = {"CFG556/541 census edge": ("CFG556 census edge (= CFG541 analytic edge)", "CFG529 census (stored)"),
             "emergent edge": ("CFG556 emergent edge", "emergent edge (x_e = 1, supply cap), total"),
             "CFG557 finite-age supply": ("CFG557 finite-age supply (TESTED)", "CFG557 finite-age supply (stored)"),
             "CFG559 kinetic PRIMARY": ("CFG559 kinetic PRIMARY", "CFG559 kinetic PRIMARY (stored)"),
             "CFG559 kinetic full supply": ("CFG559 kinetic full supply", "CFG559 kinetic full supply (stored)")}
    for n, (sk, kk) in pairs.items():
        s = JS["record_rules"][ft][sk]; k = JK["record_rules"][ft][kk]
        rec[n] = dict(shear_allowed=s["allowed_fid"], shear_Zmax=s["Zmax_best_fid"], kids_allowed=k["allowed"], kids_chi2_A=k["A"]["chi2"], kids_chi2_B=k["B"]["chi2"],
                      predicts_overlap=bool(s["allowed_fid"] and k["allowed"]))
        P(f"  record rule {n:28s}: shear Zmax {s['Zmax_best_fid']:.2f} ({'allowed' if s['allowed_fid'] else 'excluded'}); KiDS chi2 A {k['A']['chi2']:.2f} B {k['B']['chi2']:.2f} "
          f"({'allowed' if k['allowed'] else 'excluded'}) -> predicts the overlap: {rec[n]['predicts_overlap']}")
    rec["CFG542 dissipative principle"] = dict(predicts_overlap=False, note="switch is an INPUT; no profile prediction")
    P("  record rule CFG542 dissipative principle: switch is an INPUT -> no profile prediction")
    res["footings"][ft] = dict(variants=out, verdict=verdict, convention_sensitive=sens, overlap_f1_points=f1, overlap_description=desc, record_rules=rec,
                               best_kids_in_shear_region=sa_best, best_shear_in_kids_region=ka_best)

json.dump(res, open(os.path.join(HERE, "cfg593_verdict_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg593_verdict.out"), "w").write("\n".join(OUT) + "\n")
