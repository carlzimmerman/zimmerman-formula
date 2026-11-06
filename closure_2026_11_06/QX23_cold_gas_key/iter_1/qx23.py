#!/usr/bin/env python3
"""QX23 iter_1 (criteria e01a2a59a7): cold-gas key (A) vs baryon gap (B) for the law's hot/cold step.
python3 qx23.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "qx23_MUTATE" if MUT else "qx23"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
# QX20's build (which loads QX5's QX16-fixed samples), read-only: execute qx20.py up to its fitting section
src = open(os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.py")).read()
NS = {"__file__": os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.py"), "__name__": "qx20_lib"}
_argv = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:src.index("BGRID = ")], "qx20_lib", "exec"), NS); sys.argv = _argv
G, MS, A0, glaw, SP, build = NS["G"], NS["MS"], NS["A0"], NS["glaw"], NS["SP"], NS["build"]
Q20 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.json")))
Q22 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX22_support_key", "iter_1", "qx22.json")))
LW = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "LW1_law_scorecard", "lw1_dwarfs.json")))
DATA = os.path.join(REPO, "real_research", "data")

# SPARC galaxy f_HI (frozen definition: 1.33 M_HI / (1.33 M_HI + 0.5 L36))
TAB = {}
for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    t = ln.split()
    if len(t) != 19: continue
    try: TAB[t[0]] = dict(L36=float(t[7]), MHI=float(t[13]), T=float(t[1]))
    except ValueError: continue
FHI = {g["name"]: 1.33 * TAB[g["name"]]["MHI"] / (1.33 * TAB[g["name"]]["MHI"] + 0.5 * TAB[g["name"]]["L36"]) for g in SP}

def sparc_points(a0, ud=0.5, newton=False):
    """per galaxy arrays (x = log10 gbar/a0, residual dex); disk Upsilon ud, bulge 1.4 ud (QX5 base 0.5/0.7)."""
    law = (lambda g: g) if newton else (lambda g: glaw(g, a0)); out = {}
    for g in SP:
        vb2 = g["vg2"] + (ud / 0.5) * g["vd2"] + (1.4 * ud / 0.7) * g["vbu2"]; r = g["R"]
        ok = vb2 > 0; gb = vb2[ok] / r[ok]; go = g["V"][ok] ** 2 / r[ok]
        out[g["name"]] = (np.log10(gb / a0), np.log10(go / law(gb)))
    return out

def D1(pts, f, extra=None):
    """bin-count-weighted mean over 0.5-dex log y bins of mean(f<0.10) - mean(f>0.30) of per-galaxy bin-mean residuals."""
    allx = np.concatenate([v[0] for v in pts.values()]); lo = math.floor(allx.min() * 2) / 2
    per = {}
    for nm, (x, r) in pts.items():
        rr = r + (extra.get(nm, 0.0) if extra else 0.0); b = np.floor((x - lo) / 0.5).astype(int)
        for k in np.unique(b): per.setdefault(int(k), []).append((nm, float(rr[b == k].mean())))
    num = den = 0.0; nb = 0
    for k, lst in per.items():
        p = [v for nm, v in lst if f[nm] < 0.10]; q = [v for nm, v in lst if f[nm] > 0.30]
        if len(p) >= 3 and len(q) >= 3:
            w = len(p) + len(q); num += w * (np.mean(p) - np.mean(q)); den += w; nb += 1
    return (num / den if den else float("nan")), nb

def boot(pts, f, n=2000, seed=20261108):
    rng = np.random.default_rng(seed); names = list(pts); out = []
    for _ in range(n):
        pick = rng.integers(0, len(names), len(names)); bp, bf = {}, {}
        for j, i in enumerate(pick):
            k = f"{names[i]}#{j}"; bp[k] = pts[names[i]]; bf[k] = f[names[i]]
        out.append(D1(bp, bf)[0])
    return float(np.nanstd(out))

def nu_solve_k(y, delta, a0):
    """k with glaw(k gN) = 10^delta glaw(gN) at y = gN/a0."""
    gN = y * a0; tgt = 10 ** delta * glaw(gN, a0); lo, hi = 1e-6, 1e8
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if glaw(mid * gN, a0) < tgt: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)

# LG dwarf HI (LVD primary, McConnachie 2012 fallback)
HI = {}
for fn in ("lvd_dwarf_local_field.csv", "lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv"):
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
        if not r["mass_stellar"]: continue
        ms = 10 ** float(r["mass_stellar"])
        if r["mass_HI"]: HI[r["name"]] = dict(f=10 ** float(r["mass_HI"]) / ms, ul=False, src="LVD")
        elif r["mass_HI_ul"]: HI[r["name"]] = dict(f=10 ** float(r["mass_HI_ul"]) / ms, ul=True, src="LVD ul")
        else: HI[r["name"]] = dict(f=0.0, ul=True, src="LVD none listed")
MC = {r["Name"]: r for r in csv.DictReader(open(os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv")))}

RES = dict(tag=TAG, criteria="e01a2a59a7", note="kappa = 1/2 FITTED; not theory closed", foot={})
fails = 0
P(f"QX23 iter_1{' MUTATE' if MUT else ''}: cold-gas key (A) vs baryon gap (B). SPARC galaxies {len(SP)}; f_HI < 0.10: {sum(v < 0.10 for v in FHI.values())}, > 0.30: {sum(v > 0.30 for v in FHI.values())}")
for foot, a0 in A0.items():
    R = {}; S = Q20[foot]["vars"]["V4_gN"]["step"]
    pts = sparc_points(a0)
    allr = np.concatenate([v[1] for v in pts.values()]); ka1 = abs(float(allr.mean()) - Q20[foot]["sparc_mean"])
    R["KA1"] = ka1; P(f"\n[{foot}] KA1 SPARC mean {allr.mean():+.6f} vs QX20 {Q20[foot]['sparc_mean']:+.6f}: |d| {ka1:.1e} -> {'PASS' if ka1 <= 1e-6 else 'FAIL'}")
    fails += ka1 > 1e-6
    d1, nb = D1(pts, FHI); st = boot(pts, FHI)
    dU = max(abs(D1(sparc_points(a0, 0.4), FHI)[0] - d1), abs(D1(sparc_points(a0, 0.6), FHI)[0] - d1)); sd = math.sqrt(st ** 2 + dU ** 2)
    zero = {k: 0.0 for k in pts}
    pstep = D1({k: (v[0], np.zeros_like(v[1])) for k, v in pts.items()}, FHI, {k: (S if FHI[k] < 0.10 else 0.0) for k in pts})[0]
    plin = D1({k: (v[0], np.zeros_like(v[1])) for k, v in pts.items()}, FHI, {k: (S * (1 - FHI[k] / 0.30) if FHI[k] < 0.30 else 0.0) for k in pts})[0]
    preds = {"M-step": pstep, "M-lin": plin}
    zs = {m: (d1 - p) / sd for m, p in preds.items()}
    kill = all(d1 < p - 3 * sd for p in preds.values()); sup = d1 > 3 * sd and any(abs(d1 - p) <= 2 * sd for p in preds.values())
    T1 = "A KILLED in SPARC's range" if kill else ("A SUPPORTED" if sup else "NO VERDICT")
    # partial Spearman (report)
    gm = {}; allx = np.concatenate([v[0] for v in pts.values()]); lo = math.floor(allx.min() * 2) / 2; binm = {}
    for nm, (x, r) in pts.items():
        b = np.floor((x - lo) / 0.5).astype(int)
        for k in np.unique(b): binm.setdefault(int(k), []).append(float(r[b == k].mean()))
    for nm, (x, r) in pts.items():
        b = np.floor((x - lo) / 0.5).astype(int); gm[nm] = float(np.mean([r[b == k].mean() - np.mean(binm[int(k)]) for k in np.unique(b)]))
    from scipy.stats import spearmanr
    nm_ = list(gm); rho, pval = spearmanr([math.log10(max(FHI[n], 1e-4)) for n in nm_], [gm[n] for n in nm_])
    R["T1"] = dict(D1=d1, sigma=sd, stat=st, ups=dU, bins=nb, S=S, pred=preds, z=zs, label=T1, spearman_rho=float(rho), spearman_p=float(pval))
    P(f"[{foot}] T1 D1 (f_HI<0.10 minus >0.30, fixed g_bar) = {d1:+.4f} +- {sd:.4f} dex (stat {st:.4f}, Upsilon {dU:.4f}); bins {nb}")
    P(f"[{foot}]    S (QX20 g_N step) {S:+.3f}; M-step pred {pstep:+.3f} (z {zs['M-step']:+.1f}); M-lin pred {plin:+.3f} (z {zs['M-lin']:+.1f}) -> {T1}")
    P(f"[{foot}]    report: partial Spearman(log f_HI, galaxy residual) rho {rho:+.3f} (p {pval:.2g}); A predicts rho < 0")
    if MUT:
        rng = np.random.default_rng(7); nms = list(FHI); perm = rng.permutation([FHI[n] for n in nms]); fs = dict(zip(nms, perm))
        dsh = D1(pts, fs)[0]; m1 = abs(dsh) <= 2 * sd
        dpl = D1(pts, FHI, {k: (0.20 if FHI[k] < 0.10 else 0.0) for k in pts})[0]; m2 = abs((dpl - d1) - 0.20) <= 0.05
        ptsN = sparc_points(a0, newton=True); mN = float(np.concatenate([v[1] for v in ptsN.values()]).mean())
        R["M"] = dict(M1_shuffle_D1=dsh, M1_ok=bool(m1), M2_rise=dpl - d1, M2_ok=bool(m2), M3_newton_mean=mN, M3_moves=bool(abs(mN - allr.mean()) > 0.2))
        P(f"[{foot}] M1 shuffled f_HI D1 {dsh:+.4f} (|.| <= 2 sigma {2*sd:.4f}): {'PASS' if m1 else 'FAIL'}; M2 planted +0.20 rise {dpl - d1:+.4f}: {'PASS' if m2 else 'FAIL'}; "
          f"M3 Newton SPARC mean {mN:+.3f} (moves {mN - allr.mean():+.3f}): {'PASS' if R['M']['M3_moves'] else 'FAIL'}")
        fails += (not m1) + (not m2) + (not R["M"]["M3_moves"])
    # T2 LG dwarfs with measured HI
    ps = LW["footings"][foot]["per_system"]; anchor = Q20[foot]["sparc_mean"]
    poorP = ["Cetus", "Tucana", "Phoenix", "Leo T", "Pegasus dIrr", "Aquarius", "UGC 4879", "Antlia B"]; richP = ["IC 1613", "Leo A", "NGC 6822", "Sagittarius dIrr", "WLM"]
    mp = float(np.median([ps[k]["plain"] for k in poorP])) - anchor; mr = float(np.median([ps[k]["plain"] for k in richP])) - anchor
    q22 = Q22["foot"][foot]["T4"]; ka2 = max(abs(mp - q22["gas_poor_median_minus_anchor"]), abs(mr - q22["gas_rich_median_minus_anchor"]))
    P(f"[{foot}] KA2 QX22 provisional medians {mp:+.6f}/{mr:+.6f} vs {q22['gas_poor_median_minus_anchor']:+.6f}/{q22['gas_rich_median_minus_anchor']:+.6f}: |d| {ka2:.1e} -> {'PASS' if ka2 <= 1e-6 else 'FAIL'}")
    fails += ka2 > 1e-6
    rows = []
    for nm, v in ps.items():
        h = HI.get(nm)
        if h is None and nm in MC:
            mhi = MC[nm]["M.HI"]; h = dict(f=None, ul=not mhi, src="McC2012 (no M*)")
        if h is None or h["f"] is None: rows.append(dict(name=nm, cls=v["cls"], plain=v["plain"], f=None, grp="unmatched")); continue
        grp = "poor" if (h["f"] < 0.1 or (h["ul"] and h["f"] < 1.0)) else ("rich" if h["f"] > 1.0 else "mid")
        rows.append(dict(name=nm, cls=v["cls"], plain=v["plain"], f=h["f"], ul=h["ul"], src=h["src"], grp=grp))
    def d2(sel, hi_in=False):
        p = [r["plain"] for r in sel if r["grp"] == "poor"]; q = [r["plain"] - (0.5 * math.log10(1 + 2 * r["f"]) if hi_in else 0.0) for r in sel if r["grp"] == "rich"]
        if len(p) < 2 or len(q) < 2: return None, len(p), len(q), None
        D = float(np.median(p) - np.median(q)); rng = np.random.default_rng(20261108)
        bs = [np.median(rng.choice(p, len(p))) - np.median(rng.choice(q, len(q))) for _ in range(5000)]
        return D, len(p), len(q), float(np.std(bs))
    field = [r for r in rows if r["cls"] == "LG field"]
    D2, np_, nq, s2 = d2(field); D2b = d2(field, True)[0]
    if D2 is None: T2 = "NO VERDICT (too few)"
    else: T2 = "A SUPPORTED-DW" if D2 > 3 * s2 else ("A DISFAVOURED-DW" if (D2 < 2 * s2 and D2 < S - 3 * s2) else "NO VERDICT")
    sats = {}
    for c in ("MW classical", "bright M31", "M31 others", "MW ultra-faint"):
        sel = [r for r in rows if r["cls"] == c]; sats[c] = dict(n_poor=sum(r["grp"] == "poor" for r in sel), n_rich=sum(r["grp"] == "rich" for r in sel), n_mid=sum(r["grp"] == "mid" for r in sel),
                                                                  n_unmatched=sum(r["grp"] == "unmatched" for r in sel), median_plain_minus_anchor=float(np.median([r["plain"] for r in sel]) - anchor) if sel else None)
    R["T2"] = dict(D2=D2, sigma=s2, n_poor=np_, n_rich=nq, D2_HI_in=D2b, label=T2, field=[{k: r[k] for k in ("name", "plain", "f", "grp", "src") if k in r} for r in field], satellites=sats,
                   unmatched=[r["name"] for r in rows if r["grp"] == "unmatched"])
    P(f"[{foot}] T2 LG field, measured HI: poor {[r['name'] for r in field if r['grp']=='poor']}, rich {[r['name'] for r in field if r['grp']=='rich']}, mid {[r['name'] for r in field if r['grp']=='mid']}")
    P(f"[{foot}]    D2 = {D2 if D2 is None else f'{D2:+.3f}'} +- {s2 if s2 is None else f'{s2:.3f}'} dex (n {np_}/{nq}); with all HI inside r_h (deep-MOND bracket) {D2b if D2b is None else f'{D2b:+.3f}'}; S {S:+.3f} -> {T2}")
    for c, v in sats.items(): P(f"[{foot}]    report {c}: poor {v['n_poor']}, rich {v['n_rich']}, mid {v['n_mid']}, unmatched {v['n_unmatched']}; median plain - anchor {v['median_plain_minus_anchor']:+.3f}")
    # T4 reading B: uncounted-baryon factor per class
    H, _ = build(a0); T4 = {}
    CEIL = {"E": 0.2, "G": 0.3, "X": 0.3, "dw": 0.1}
    for c, lab in (("E", "ellipticals"), ("G", "groups"), ("X", "X-COP")):
        hh = [h for h in H if h["cls"] == c]; dl = float(np.mean([h["D"] for h in hh])) - anchor; y = float(np.median([h["V4_gN"] for h in hh]))
        k = nu_solve_k(y, dl, a0); ce = CEIL[c]; st_ = "ALLOWED" if k - 1 <= ce else ("EXCLUDED" if k - 1 > 2 * ce else "MARGINAL")
        T4[lab] = dict(delta=dl, y_med=y, k=k, ceiling=ce, status=st_)
    dwc = {"bright M31 dSphs": [v["plain"] for v in ps.values() if v["cls"] == "bright M31"], "MW classical dSphs": [v["plain"] for v in ps.values() if v["cls"] == "MW classical"],
           "LG gas-poor field (measured HI)": [r["plain"] for r in field if r["grp"] == "poor"]}
    for lab, vals in dwc.items():
        dl = float(np.median(vals)) - anchor; k = 10 ** (2 * dl); ce = CEIL["dw"]; st_ = "ALLOWED" if k - 1 <= ce else ("EXCLUDED" if k - 1 > 2 * ce else "MARGINAL")
        T4[lab] = dict(delta=dl, y_med=None, k=k, ceiling=ce, status=st_)
    R["T4"] = T4
    for lab, v in T4.items(): P(f"[{foot}] T4 {lab:32s} Delta {v['delta']:+.3f} dex, y {('%.3g' % v['y_med']) if v['y_med'] else 'deep'} -> k {v['k']:.2f} (uncounted {v['k']-1:.2f} x counted; ceiling {v['ceiling']}) -> B {v['status']}")
    R["B_all_allowed"] = all(v["status"] == "ALLOWED" for v in T4.values()); R["B_excluded_dwarf"] = any(v["status"] == "EXCLUDED" for k, v in T4.items() if "dSph" in k or "field" in k)
    RES["foot"][foot] = R
if not MUT:
    F = RES["foot"]
    t1k = all(F[f]["T1"]["label"].startswith("A KILLED") for f in F); t1s = all(F[f]["T1"]["label"] == "A SUPPORTED" for f in F)
    t2s = all(F[f]["T2"]["label"] == "A SUPPORTED-DW" for f in F)
    if t1s or (t2s and not t1k): lab = "COLD-GAS KEY SUPPORTED"
    elif all(F[f]["B_all_allowed"] for f in F): lab = "BARYON-GAP SUPPORTED"
    elif t1k and all(F[f]["B_excluded_dwarf"] for f in F): lab = "NEITHER"
    else: lab = "NO VERDICT"
    RES["label"] = lab; P(f"\nOVERALL LABEL: {lab}")
RES["fails"] = int(fails); P(f"failed checks: {fails}")
json.dump(RES, open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
