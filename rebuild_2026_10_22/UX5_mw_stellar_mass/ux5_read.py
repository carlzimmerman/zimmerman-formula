#!/usr/bin/env python3
"""UX5 part 1 read. Classes per form, footing, box; Q3 on all cells; form-Q minus form-A; convergence; labels. kappa = 1/2 FITTED; not theory closed."""
import json, sys
from ux5_core import *
OUT = []; RES = {}
def P(s): print(s, flush=True); OUT.append(s)
def cls(rows, f):
    a = [r for r in rows if all(r[f][l] for l in ("L1", "L2a", "L2b", "L3"))]; vk = [r for r in rows if all(r[f][l] for l in ("L1", "L2a", "L2b"))]; ip = [r for r in a if r["inp"]]; ipvk = [r for r in vk if r["inp"]]
    c = "FEASIBLE IN PRIORS" if ip else "FEASIBLE (WIDE PRIORS ONLY)" if a else "V+K ONLY" if vk else "INFEASIBLE"; b = min(rows, key=lambda r: r[f]["D"]); pr = [r for r in rows if r["inp"]]; bi = min(pr, key=lambda r: r[f]["D"]) if pr else None; ds = lambda r: {k: r.get(k) for k in ("sb", "mbb", "rd", "ht", "hk", "fk", "rdk", "Mstar")} | {k: r[f][k] for k in ("vc", "K0", "cK", "cO", "h", "D")} if r else None
    x = [r for r in rows if r[f]["L1"]]; return dict(cls=c, n=len(rows), n_all=len(a), n_inprior=len(ip), n_VK=len(vk), n_VK_inprior=len(ipvk), strict=sum(r[f]["Lh"] for r in a), strict_inprior=sum(r[f]["Lh"] for r in ip), best=ds(b), best_ip=ds(bi), Kmin_given_vc=min((r[f]["K0"] for r in x), default=None), Kmin_given_vc_ip=min((r[f]["K0"] for r in x if r["inp"]), default=None), ip_cells=[ds(r) for r in ip][:40], h_ip=[min((r[f]["h"] for r in ip), default=None), max((r[f]["h"] for r in ip), default=None)])
for foot in ("canonical", "alt"):
    for ax in (1.0, 1.5):
        rows = [json.loads(l) for l in open(f"cache/{foot}_{ax}.jsonl")]; R = RES[f"{foot}|{ax}"] = {}
        for box in ("B175", "BV", "BV2"):
            rb = [r for r in rows if r["box"] == box]
            if not rb: continue
            for f in ("A", "Q", "R"):
                c = cls(rb, f); R[f"{box}|{f}"] = c; b, bi = c["best"], c["best_ip"]
                P(f"[{foot} a0x{ax}] {box} form {f}: {c['cls']}; n {c['n']} all4 {c['n_all']} in-prior {c['n_inprior']} V+K {c['n_VK']} (in-prior {c['n_VK_inprior']}); strict {c['strict']} (in-prior {c['strict_inprior']}); min K(R0) with v_c in line {c['Kmin_given_vc']:.1f} (in-prior {c['Kmin_given_vc_ip'] if c['Kmin_given_vc_ip'] is None else round(c['Kmin_given_vc_ip'], 1)}); best D {b['D']:.2f} Rd {b['rd']:.2f} vc {b['vc']:.1f} K {b['K0']:.1f} h {b['h']:.2f} Ou {b['cO']:.0f}; in-prior best D {bi['D']:.2f} vc {bi['vc']:.1f} K {bi['K0']:.1f} h {bi['h']:.2f} ht {bi['ht']} hk {bi['hk']} fk {bi['fk']} Sb {bi['sb']} Mbb {bi['mbb']:.3g}" if bi else "no prior")
        d = np.array([r["Q"]["K0"] / r["A"]["K0"] - 1 for r in rows]); dv = np.array([r["Q"]["vc"] / r["A"]["vc"] - 1 for r in rows]); dr = np.array([r["R"]["K0"] / r["A"]["K0"] - 1 for r in rows]); dh = np.array([r["Q"]["h"] - r["A"]["h"] for r in rows]); R["QvsA"] = dict(K=[float(d.min()), float(np.median(d)), float(d.max())], vc=[float(dv.min()), float(np.median(dv)), float(dv.max())], R_over_A=[float(dr.min()), float(np.median(dr)), float(dr.max())], h=[float(dh.min()), float(dh.max())])
        P(f"[{foot} a0x{ax}] K(R0) Q/A-1 min, med, max {np.round(R['QvsA']['K'], 4).tolist()}; v_c Q/A-1 {np.round(R['QvsA']['vc'], 4).tolist()}; R/A-1 {np.round(R['QvsA']['R_over_A'], 3).tolist()}; dh {np.round(R['QvsA']['h'], 3).tolist()}")
        if ax == 1.0:
            lw = [json.loads(l) for l in open(os.path.join(RB, "LW1_law_scorecard", "cache_mw", f"{foot}_1.0.jsonl"))]; lw = [x for x in lw if not x.get("mcm")]; rb = [r for r in rows if r["box"] == "B175"]; e = max(abs(r[f_][a] / x[f_][b] - 1) for r, x in zip(rb, lw) for f_ in ("A", "R") for a, b in (("vc", "vc_R0"), ("K0", "K_R0"), ("cK", "chi2_Kz"))); R["Q3"] = e; P(f"Q3 all 175 cells forms A, R vs LW1 max rel {e:.1e}: {'PASS' if e <= 1e-6 else 'FAIL'}")
# Q5 convergence
P(""); 
for foot in ("canonical", "alt"):
    a0 = A0[foot]; g, Mu = grid(a0); gh, _ = grid(a0, hi=True); L0, L1 = Lapl(g), Lapl(gh); R = RES[f"{foot}|1.0"]; cases = [("McMillan", ns["rho_mcm"], "QA")]
    for f in ("A", "Q"):
        for tag in ("best", "best_ip"):
            b = R[f"BV|{f}"][tag]; rh, _ = rho_struct(b["sb"], b["mbb"], b["rd"], b["ht"], b["hk"], b["fk"]); cases.append((f"BV {f} {tag}", rh, f))
        b = R[f"B175|{f}"]["best"]; rh, _ = rho_struct(b["sb"], b["mbb"], b["rd"]); cases.append((f"B175 {f} best", rh, f))
    mx = 0
    for n, rh, fs in cases:
        o0 = solve(rh, a0, g, Mu, L0, fs); o1 = solve(rh, a0, gh, Mu, L1, fs)
        for f in fs: dK, dv = o1[f]["K0"] - o0[f]["K0"], o1[f]["vc"] - o0[f]["vc"]; mx = max(mx, abs(dK)); P(f"Q5 [{foot}] {n} form {f}: K {o0[f]['K0']:.2f} -> {o1[f]['K0']:.2f} (d {dK:+.2f}); v_c {o0[f]['vc']:.2f} -> {o1[f]['vc']:.2f} (d {dv:+.2f}); chi2Kz {o0[f]['cK']:.1f} -> {o1[f]['cK']:.1f}")
    RES[f"Q5_{foot}"] = mx; P(f"Q5 [{foot}] max |dK| {mx:.2f}: {'[GRID-DEPENDENT]' if mx > 1 else 'converged at frozen tolerance'}")
P("\nLabels")
for foot in ("canonical", "alt"):
    R = RES[f"{foot}|1.0"]; 
    for f in ("A", "Q"):
        ipvk = lambda b: R[f"{b}|{f}"]["n_VK_inprior"]; lab = "K_z FAILURE SURVIVES" if ipvk("B175") == 0 and ipvk("BV") == 0 and ipvk("BV2") == 0 else "K_z FAILURE REMOVED BY FORM" if f == "Q" and ipvk("B175") else "REMOVED ONLY BY STRUCTURE"; RES[f"label_{foot}_{f}"] = lab; P(f"[{foot}] form {f}: {lab}; B175 {R[f'B175|{f}']['cls']}, BV {R[f'BV|{f}']['cls']}, BV2 {R[f'BV2|{f}']['cls']}")
open("ux5_read.out", "w").write("\n".join(OUT) + "\n"); json.dump(RES, open("ux5_read.json", "w"), indent=1, default=float)
