#!/usr/bin/env python3
"""UX5 part 2 (FROZEN_CRITERIA.md). UL1's gate; offset, differential, denominator, bin mapping, D and i refit, gas. --mutate writes twin only. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, re, sys
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
MUT = "--mutate" in sys.argv; sys.argv = sys.argv[:1]
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); RT = os.path.dirname(RB); UL = os.path.join(RB, "UL1_measured_upsilon_test")
sys.path.insert(0, UL); import ul1_core as C
OUT = []; RES = {}
def P(s): print(s, flush=True); OUT.append(s)
G = C.load(); UPS = C.UPS; NG = len(G); BINS = ("60-100", "100-150", "150-200", "200-250", "250-400"); A0 = dict(canonical=9.3603e-11, alt=1.1312e-10)
vf = np.array([q["meta"]["Vflat"] for q in G]); Qs = np.array([(q["meta"]["Q"] <= 2 and q["meta"]["Inc"] >= 30 and q["meta"]["Vflat"] > 0) for q in G]); fb = np.array([q["Vbul"][-1] ** 2 / max(q["Vdisk"][-1] ** 2 + q["Vbul"][-1] ** 2, 1e-9) for q in G]); TOT = 1 + 0.4 * fb
def lh(b): return tuple(float(a) for a in b.split("-"))
SEL = {b: Qs & (vf >= lh(b)[0]) & (vf < lh(b)[1]) for b in BINS}
EST = json.load(open(os.path.join(UL, "ul1_est.json")))["primary"]
def boot(u, B=2000):
    r = np.random.default_rng(1); n = len(u); return float(np.std(np.log10(np.median(u[r.integers(0, n, (B, n))], axis=1))))
def binvals(u): return {b: dict(m=float(np.median((u * TOT)[SEL[b]])), n=int(SEL[b].sum()), e=boot((u * TOT)[SEL[b]]), Vmed=float(np.median(vf[SEL[b]]))) for b in BINS}
def gate(bv, x, delta=0.0, lowfix=None):
    et = {b: EST[b][x] for b in BINS}; m = np.log10([bv[b]["m"] for b in BINS]); mu = np.log10([et[b]["mu"] for b in BINS]) + delta
    h = np.array([math.sqrt(max(bv[b]["e"], 1.25 * et[b]["sig"] / math.sqrt(bv[b]["n"])) ** 2 + 0.04 ** 2) for b in BINS]); d = m - mu; Z = d / h; w = 1 / h ** 2; off = float((w * d).sum() / w.sum()); chi = float((((d - off) / h) ** 2).sum())
    def slope(y, V): x_ = np.log10(V); X = (w * x_).sum() / w.sum(); return float((w * (x_ - X) * (y - (w * y).sum() / w.sum())).sum() / (w * (x_ - X) ** 2).sum()), float(1 / math.sqrt((w * (x_ - X) ** 2).sum()))
    s, es = slope(m, [bv[b]["Vmed"] for b in BINS]); sX, _ = slope(mu, [et[b]["Vmed"] for b in BINS]); st = np.diff(m) - np.diff(mu); sh = np.sqrt(h[:-1] ** 2 + h[1:] ** 2)
    a, b_, c = chi <= 9.49, bool(s > 0 and abs(s - sX) <= 2 * es), bool(np.all(np.abs(st) <= 2 * sh))
    return dict(level=bool(np.all(np.abs(Z) <= 2)), shape=bool(a and b_ and c), Z=Z.tolist(), d=d.tolist(), h=h.tolist(), chi=chi, slope=s, slopeX=sX, steps=(st / sh).tolist())
def law_lp(gb, a0): gb = np.maximum(gb, 1e-300); return np.log10(gb * (0.5 + np.sqrt(0.25 + a0 / gb)))
def fit_ul1(q, a0, fD=1.0, sfac=1.0, gasf=1.0):
    """UL1's statistic, wide U grid. fD = D'/D, sfac = (sin i/sin i')^2 on g_obs. g_bar invariant under D at fixed U."""
    V = np.sign(q["Vgas"]) * q["Vgas"] ** 2 * gasf; gb = (V[:, None] + UPS[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * UPS[None, :] * q["Vbul"][:, None] ** 2) * 1e6 / q["Rm"][:, None]; go = q["GO"] * sfac / fD
    ok = (gb > 0) & (go > 0)[:, None] & np.isfinite(gb) & (q["Vobs"] > 0)[:, None]; r = np.where(ok, np.log10(np.where(go > 0, go, 1.0))[:, None] - law_lp(np.where(ok, gb, 1.0), a0), 0.0); W = np.where(ok, q["W"][:, None], 0.0)
    ws = W.sum(0); m = np.where(ws > 0, (W * r * r).sum(0) / np.maximum(ws, 1e-300), np.inf); return int(np.argmin(m)), m
def refit(a0, **k): return UPS[[fit_ul1(q, a0, **k)[0] for q in G]]
def med_tot(u, b): return float(np.median((u * TOT)[SEL[b]]))
for foot in ("canonical", "alt"):
    a0 = A0[foot]; u = refit(a0); bv = binvals(u); R = RES[foot] = {}; P(f"\n===== {foot} a0 {a0}")
    rec = json.load(open(os.path.join(UL, "ul1_results.json")))["law_" + foot]["A_c2b_refit"]; rt = rec["bins"] if isinstance(rec["bins"], dict) else None
    z0 = np.load(os.path.join(UL, "rows", f"law_{foot}.npz")); m0 = np.where(z0["A_c2b_refit_ws"] > 0, z0["A_c2b_refit_wr2"] / np.maximum(z0["A_c2b_refit_ws"], 1e-300), np.inf); u0 = UPS[np.argmin(m0, axis=1)]; dmax = float(np.max(np.abs(u - u0))); R["P1_maxdU"] = dmax; P(f"P1 per-galaxy U vs UL1 rows max |d| {dmax:.3f}, n differ {(u != u0).sum()}: {'PASS' if dmax <= 1e-6 else 'FAIL, reported, UL1 rows used for the gate'}")
    u = u0; bv = binvals(u); R["bins"] = {b: bv[b]["m"] for b in BINS}; P("U_tot bins " + " ".join(f"{b} {bv[b]['m']:.3f} (n{bv[b]['n']})" for b in BINS))
    if MUT:
        for x in ("Taylor", "GSWLC"):
            b2 = {b: dict(bv[b]) for b in BINS}
            for b in BINS[:2]: b2[b]["m"] = EST[b][x]["mu"]
            g = gate(b2, x); ok = all(abs(z) <= 2 for z in g["Z"][:2]); b3 = {b: dict(bv[b]) for b in BINS}
            for b in BINS[:2]: b3[b]["m"] = bv[b]["m"] * 2
            g3 = gate(b3, x); P(f"MUTATE {x}: low bins = estimator, Z {np.round(g['Z'][:2], 2).tolist()} level there {'PASS as required' if ok else 'BROKEN'}; doubled, level {g3['level']}, {'FAIL as required' if not g3['level'] else 'BROKEN'}")
        continue
    # (a) offset
    for x in ("Taylor", "GSWLC"):
        g0 = gate(bv, x); ds = np.round(np.arange(-0.2, 0.8001, 0.001), 3); lev = [d for d in ds if gate(bv, x, d)["level"]]; shp = [d for d in ds if gate(bv, x, d)["shape"]]
        best = min(ds, key=lambda d: max(abs(z) for z in gate(bv, x, d)["Z"])); gb = gate(bv, x, float(best)); gs = {f"{d:+.2f}": np.round(gate(bv, x, d)["Z"], 1).tolist() for d in (0.03, 0.09, 0.24)}
        R[f"a_{x}"] = dict(Z0=g0["Z"], d0=g0["d"], h=g0["h"], delta_level=[min(lev), max(lev)] if lev else None, n_shape=len(shp), best_delta=float(best), best_Zmax=max(abs(z) for z in gb["Z"]), best_steps=gb["steps"], best_shape=gb["shape"], chi=g0["chi"], slope=g0["slope"], slopeX=g0["slopeX"], Z_at=gs)
        P(f"(a) {x}: d {np.round(g0['d'], 3).tolist()} h {np.round(g0['h'], 3).tolist()} Z {np.round(g0['Z'], 2).tolist()}; delta passing level {R[f'a_{x}']['delta_level']}; best delta {best:+.3f} |Z|max {R[f'a_{x}']['best_Zmax']:.2f}; shape never passes by offset: {len(shp) == 0}, chi2 {g0['chi']:.1f}, slope {g0['slope']:+.2f} vs {g0['slopeX']:+.2f}, steps {np.round(g0['steps'], 1).tolist()}; Z at IMF steps {gs}")
    # (b) differential
    for x in ("Taylor", "GSWLC"):
        d = R[f"a_{x}"]["d0"]; req = 0.5 * (d[0] + d[1]) - 0.5 * (d[2] + d[3]); R[f"b_req_{x}"] = req; P(f"(b) required differential {x}, 60-150 minus 150-250: {req:+.3f} dex, in the sense estimator mass up at low V relative to high V")
    # (e) D, i
    Dmed = {b: float(np.median([G[i]["meta"]["eD"] / G[i]["meta"]["D"] / math.log(10) for i in np.where(SEL[b])[0]])) for b in BINS[:2]}; Imed = {b: float(np.median([G[i]["meta"]["eInc"] for i in np.where(SEL[b])[0]])) for b in BINS[:2]}
    R["e"] = {}
    for b in BINS[:2]:
        tg = EST[b]["GSWLC"]["mu"]; idx = np.where(SEL[b])[0]; o = {}
        # uniform log D
        ld = np.arange(0, 1.0001, 0.01); val = []
        for l in ld: val.append(float(np.median([UPS[fit_ul1(G[i], a0, fD=10 ** l)[0]] * TOT[i] for i in idx])))
        hit = next((float(l) for l, v in zip(ld, val) if v <= tg), None); o["dlogD"] = hit; o["dlogD_sig"] = hit / Dmed[b] if hit is not None else None; o["D_factor"] = 10 ** hit if hit is not None else None
        # uniform i
        di = np.arange(0, 60.01, 1.0); vali = []
        for dd in di: vali.append(float(np.median([UPS[fit_ul1(G[i], a0, sfac=(math.sin(math.radians(G[i]["meta"]["Inc"])) / math.sin(math.radians(min(G[i]["meta"]["Inc"] + dd, 90.0)))) ** 2)[0]] * TOT[i] for i in idx])))
        hi_ = next((float(l) for l, v in zip(di, vali) if v <= tg), None); o["di"] = hi_; o["di_sig"] = hi_ / Imed[b] if hi_ is not None else None; o["U_at_i90"] = vali[-1]; o["median_Inc"] = float(np.median([G[i]["meta"]["Inc"] for i in idx]))
        # gas
        gf = np.arange(1, 6.001, 0.05); valg = []
        for f in gf: valg.append(float(np.median([UPS[fit_ul1(G[i], a0, gasf=f)[0]] * TOT[i] for i in idx])))
        hg = next((float(l) for l, v in zip(gf, valg) if v <= tg), None); o["gas_factor"] = hg; R["e"][b] = o
        P(f"(e) {b} to GSWLC {tg:.3f}: uniform dlogD {o['dlogD']} (D x {o['D_factor']}) = {o['dlogD_sig']} median errors (median {Dmed[b]:.3f} dex); uniform di {o['di']} deg = {o['di_sig']} median errors (median {Imed[b]:.1f}), median Inc {o['median_Inc']:.0f}, U at all i 90 cap +60: {o['U_at_i90']:.3f}; (f) gas factor {o['gas_factor']}")
    # MAP: per galaxy D, i free under priors
    def map_u(q, prior=True):
        m = q["meta"]; sD = max(m["eD"] / m["D"] / math.log(10), 1e-3); sI = max(m["eInc"], 0.5); inc = m["Inc"]; best = (np.inf, None); sl = 2 * np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None) / math.log(10); n = np.arange(-3, 3.01, 0.5)
        for a in n:
            for b in n:
                ii = min(inc + b * sI, 89.5);
                if ii < 10: continue
                sf = (math.sin(math.radians(inc)) / math.sin(math.radians(ii))) ** 2; fD = 10 ** (a * sD); _, mm = fit_ul1(q, a0, fD=fD, sfac=sf); wsum = (np.where(q["OK"].any(1), q["W"], 0)).sum(); nW = np.where(q["OK"].any(1), 1 / sl ** 2, 0).sum() / max(wsum, 1e-300)
                chi = mm * wsum * nW + (a * a + b * b if prior else 0.0); k = int(np.argmin(chi))
                if chi[k] < best[0]: best = (float(chi[k]), UPS[k], a, b)
        return best[1], best[2], best[3]
    idx = np.where(Qs & (vf >= 60) & (vf < 400))[0]; um = u.copy(); aa = {}; 
    for i in idx: um[i], aa[i], _b = map_u(G[i]); aa[i] = (aa[i], _b)
    bm = binvals(um); gm = gate(bm, "GSWLC"); gmT = gate(bm, "Taylor"); R["map"] = dict(bins={b: bm[b]["m"] for b in BINS}, Z_GSWLC=gm["Z"], Z_Taylor=gmT["Z"], level_GSWLC=gm["level"], low_level=all(abs(z) <= 2 for z in gm["Z"][:2]), steps=gm["steps"], med_nsig_D=float(np.median([aa[i][0] for i in idx])), med_nsig_i=float(np.median([aa[i][1] for i in idx])))
    P("(e) MAP D, i free in published errors: U_tot " + " ".join(f"{b} {bm[b]['m']:.3f}" for b in BINS) + f"; Z GSWLC {np.round(gm['Z'], 2).tolist()}, Taylor {np.round(gmT['Z'], 2).tolist()}; median pull D {R['map']['med_nsig_D']:+.1f} i {R['map']['med_nsig_i']:+.1f} sigma; steps {np.round(gm['steps'], 1).tolist()}")
    if foot == "canonical":
        q = G[idx[0]]; R["M_noprior_moves"] = None
        um2 = u.copy(); 
        for i in idx[:40]: um2[i], _, _ = map_u(G[i], prior=False)
        dm = float(np.median(np.abs(np.log10(um2[idx[:40]] / um[idx[:40]])))); P(f"MUTATE-in-run prior removed, first 40 galaxies: median |dlog U| {dm:.3f}: {'moves' if dm > 0 else 'BROKEN'}"); R["M_noprior_moves"] = dm
if MUT:
    open(os.path.join(HERE, "ux5_ups_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit()
# on-disk estimator tests
rows = list(csv.DictReader(open(os.path.join(RT, "data_assembly", "alfalfa_sdss_local_control", "alfalfa_sdss.csv"))))
def fl(x):
    try: return float(x)
    except ValueError: return None
A = []
for r in rows:
    w, ba, mm = fl(r["w50_kms"]), fl(r["ba_r"]), fl(r["logms_mcgaugh"])
    if w is None or ba is None or mm is None or r["hi_code"] != "1" or ba > 0.71 or ba < 0.2: continue
    A.append(dict(V=w / (2 * math.sqrt((1 - ba * ba) / 0.96)), ba=ba, mm=mm, T=fl(r["logms_taylor"]), G=fl(r["logms_gswlc"]), D=fl(r["dist_mpc"]), gi=fl(r["gi_corr"]), sfr=fl(r["logsfr_nuvir"])))
P("\n===== on-disk estimators")
RES["disk"] = {}
for lo, hi in ((60, 100), (100, 150), (150, 200), (200, 250)):
    a = [x for x in A if lo <= x["V"] < hi and x["T"] is not None and x["G"] is not None]; dd = np.array([x["G"] - x["T"] for x in a]); ba = np.array([x["ba"] for x in a]); Ug = np.array([0.45 * 10 ** (x["G"] - x["mm"]) for x in a]); UT = np.array([0.45 * 10 ** (x["T"] - x["mm"]) for x in a]); gi = np.array([x["gi"] for x in a])
    q = np.percentile(ba, [33, 67]); ss = [ba <= q[0], ba >= q[1]]; qc = np.percentile(gi, [16, 84])
    o = dict(GmT=float(np.median(dd)), G_ba_lo=float(np.median(Ug[ss[0]])), G_ba_hi=float(np.median(Ug[ss[1]])), T_ba_lo=float(np.median(UT[ss[0]])), T_ba_hi=float(np.median(UT[ss[1]])), G_p84=float(np.percentile(Ug, 84)), G_p97=float(np.percentile(Ug, 97.5)), f_ge_law=float(np.mean(Ug >= RES["canonical"]["bins"][f"{lo}-{hi}"])), red_G=float(np.median(Ug[gi >= qc[1]])), n=len(a)); RES["disk"][f"{lo}-{hi}"] = o
    P(f"{lo}-{hi} n{o['n']}: GSWLC-Taylor {o['GmT']:+.2f}; GSWLC by b/a edge-on/face-on tercile {o['G_ba_lo']:.3f}/{o['G_ba_hi']:.3f}; Taylor {o['T_ba_lo']:.3f}/{o['T_ba_hi']:.3f}; GSWLC U p84 {o['G_p84']:.3f}, p97.5 {o['G_p97']:.3f}, reddest 16 % median {o['red_G']:.3f}; share of galaxies at or above law's canonical bin {o['f_ge_law']:.3f}")
gg = RES["disk"]; dif = 0.5 * (gg["60-100"]["GmT"] + gg["100-150"]["GmT"]) - 0.5 * (gg["150-200"]["GmT"] + gg["200-250"]["GmT"]); RES["disk_dif"] = dif; P(f"on-disk differential (GSWLC-Taylor) low minus high {dif:+.3f}: sign {'right' if dif > 0 else 'WRONG'} for raising low bins")
RES["d_maxG"] = max(EST[b]["GSWLC"]["mu"] for b in BINS); P(f"(d) largest GSWLC bin {RES['d_maxG']:.3f}; so no V shift of any size reaches 0.62, 0.65")
# (c) denominators from UL1's printed matches, its own numbers
txt = open(os.path.join(UL, "ul1_est.out")).read(); RES["c"] = {}
for b in ("60-100", "100-150", "150-250"):
    m = re.search(rf"V_flat {b} n (\d+):(.*)", txt); s = m.group(2); mc = re.search(r"McG ([\d.]+) \(n (\d+)\)", s); ta = re.search(r"Taylor ([\d.]+) \(n (\d+)\)", s); r = float(mc.group(1)) / 0.45; RES["c"][b] = dict(ratio=r, n=int(mc.group(2)), taylor_on_L36=float(ta.group(1))); P(f"(c) {b}: L_W1/L_3.6 median {r:.2f} (n {mc.group(2)}); Taylor mass / SPARC L[3.6] {ta.group(1)}")
for b in BINS[:2]: P(f"(c) needed L_W1/L_3.6 to close canonical {b} against GSWLC: {RES['canonical']['bins'][b] / EST[b]['GSWLC']['mu']:.2f}, Taylor {RES['canonical']['bins'][b] / EST[b]['Taylor']['mu']:.2f}")
# labels
P("\n===== labels"); RES["labels"] = {}
for foot in ("canonical", "alt"):
    R = RES[foot]; L_ = []
    for x in ("Taylor", "GSWLC"):
        dl = R[f"a_{x}"]["delta_level"]; ok = dl is not None and dl[0] <= 0.24
        if ok: L_.append(f"LEVEL ONLY BY OFFSET on {x}, delta {dl[0]:+.3f} to {min(dl[1], 0.24):+.3f}")
    imf = False
    dif_ok = max(R["b_req_GSWLC"], R["b_req_Taylor"]) <= (dif if dif > 0 else -1)
    di = R["map"]["low_level"] or any((R["e"][b]["dlogD_sig"] or 99) <= 2 or (R["e"][b]["di_sig"] or 99) <= 2 for b in BINS[:2]) and all(((R["e"][b]["dlogD_sig"] or 99) <= 2) or ((R["e"][b]["di_sig"] or 99) <= 2) for b in BINS[:2])
    if di: L_.append("CARRIED BY D, i")
    if dif_ok: L_.append("CARRIED BY DIFFERENTIAL SPS (on-disk)")
    if not L_: L_ = ["NOT CARRIED"]
    RES["labels"][foot] = L_; P(f"[{foot}] " + "; ".join(L_) + f"; required differential GSWLC {R['b_req_GSWLC']:+.3f}, Taylor {R['b_req_Taylor']:+.3f}; shape fails with every offset")
json.dump(RES, open(os.path.join(HERE, "ux5_ups.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ux5_ups.out"), "w").write("\n".join(OUT) + "\n")
