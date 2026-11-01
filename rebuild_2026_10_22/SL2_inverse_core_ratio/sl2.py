#!/usr/bin/env python3
"""SL2_inverse_core_ratio (FROZEN_CRITERIA.md): A each scale asks for on NR1 PRIMARY; the virial law with one FITTED eps. SL1's cache and graders, read only. kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys, math
HERE2 = os.path.dirname(os.path.abspath(__file__)); RB2 = os.path.dirname(HERE2); SL1 = os.path.join(RB2, "SL1_symbolic_law_search"); __file__ = os.path.join(SL1, "x.py"); os.environ["SL1_HERE"] = SL1
exec(compile(open(os.path.join(SL1, "discover_law.py")).read().split('if __name__ == "__main__" and "--sweep"')[0], "discover_law", "exec"))
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
_ri, _rho = Sys.__init__, Sys.rho; EPS = {"v": 0.0}
def _init(s, *a, **k): _ri(s, *a, **k); s.V["qc"] = np.zeros_like(s.r0); s.V["Eps"] = EPS
def _r(s, t):
    if isinstance(t, float): return np.full_like(s.r0, t)
    s.V["Eps"] = EPS["v"]; return _rho(s, t)
Sys.__init__, Sys.rho = _init, _r
D = Data(); RES = dict(); GRID = np.geomspace(0.05, 20, 241); cc = D.c; ge = cc["GE"]; IU = {u: int(np.argmin(abs(D.UPS - u))) for u in (0.5, 0.55, 0.6)}; R0 = np.random.default_rng(20261101)
def boot(x, n=20000): x = np.asarray(x); return np.percentile(np.median(x[R0.integers(0, len(x), (n, len(x)))], axis=1), [2.5, 97.5]).tolist()
def bin_of(v):
    for k, (l, h) in enumerate(BINS):
        if l <= v < h or (h == 400 and v == 400): return k
    return -1
# ------------------------------------------------------- SPARC
def gal_arrays(q, tag):
    h = q["halo"][tag]; Rm = q["Rm"]; Mout = math.pi * h["S"] * h["r0"] ** 2 * Bf(h["R200"] / h["r0"]); return h, Rm, Mout
def A_ups(q, tag, U, go=None):
    h, Rm, Mout = gal_arrays(q, tag); iu = IU[U]; ok = q["OK"][:, iu]; lo = np.log10(q["GO"]) if go is None else go; w = q["W"]; best = (1e300, None)
    for A in GRID:
        re = A * h["r0"]; g = ge * Mout * Bf(np.minimum(Rm, h["R200"]) / re) / Bf(h["R200"] / re) / Rm ** 2; r = (lo - np.log10(np.maximum(q["GB"][:, iu] + g, 1e-300)))[ok]; m = float(np.sum(w[ok] * r * r) / max(np.sum(w[ok]), 1e-300))
        if m < best[0]: best = (m, A)
    return best[1]
SEL = D.sel; G = D.gals; T1 = {}; P("SL2 inversion on NR1 PRIMARY; kappa = 1/2 FITTED; not theory closed\n\n=== Part 1a SPARC, A at fixed Upsilon, median [95 %], and A from ET1's S")
for tag in TAGS:
    T1[tag] = {}
    for k, (l, h_) in enumerate(BINS):
        gs = [G[i] for i in SEL if bin_of(G[i]["vf"]) == k]; row = dict(n=len(gs), lgM=float(np.median([math.log10(q["halo"][tag]["M2"] / cc["MSUNE"]) for q in gs])))
        for U in (0.55, 0.60): x = [A_ups(q, tag, U) for q in gs]; row[f"U{U}"] = dict(med=float(np.median(x)), ci=boot(x))
        r0, R, Mo = (float(np.median([gal_arrays(q, tag)[j] for q in gs])) if j else None for j in ()) if False else (float(np.median([q["halo"][tag]["r0"] for q in gs])), float(np.median([q["halo"][tag]["R200"] for q in gs])), float(np.median([gal_arrays(q, tag)[2] for q in gs])))
        Sg = Mo / (math.pi * (GRID * r0) ** 2 * Bf(R / (GRID * r0))) / (cc["MSUNE"] / cc["PC2"]); ET = json.load(open(os.path.join(RB2, "ET1_core_strength_needed", "et1_results.json")))["ups"]["0.50"]["bins"][f"{l}-{h_}"]; pick = lambda s_: float(GRID[np.argmin(np.abs(np.log(Sg / s_)) + 1e-6 * np.abs(np.log(GRID)))]); row["AS"] = dict(med=pick(ET["med"]), lo=pick(ET["ci"][1]), hi=pick(ET["ci"][0])); T1[tag][f"{l}-{h_}"] = row
        P(f"  [{tag[:1]}] V {l}-{h_} n {row['n']} lgM {row['lgM']:.2f}: A(U .55) {row['U0.55']['med']:.2f} [{row['U0.55']['ci'][0]:.2f},{row['U0.55']['ci'][1]:.2f}]; A(U .60) {row['U0.6']['med']:.2f} [{row['U0.6']['ci'][0]:.2f},{row['U0.6']['ci'][1]:.2f}]; A from S {row['AS']['med']:.2f} [{row['AS']['lo']:.2f},{row['AS']['hi']:.2f}]")
RES["sparc"] = T1
# ------------------------------------------------------- LITTLE THINGS, groups, X-COP, constant A
a0 = D.a0["canonical"]; L1 = np.geomspace(0.1, 10, 93); LT = {}
for t in TAGS:
    e = np.array([np.median(D.lt_E(t, float(a), "1", a0)) for a in L1]); ok = np.abs(e) <= 0.05; LT[t] = dict(A0=float(L1[np.argmin(np.abs(e))]), lo=float(L1[ok].min()) if ok.any() else None, hi=float(L1[ok].max()) if ok.any() else None); P(f"LITTLE THINGS [{t[:1]}]: E = 0 at A {LT[t]['A0']:.2f}; |E| <= 0.05 for A in [{LT[t]['lo']}, {LT[t]['hi']}]")
Ag = np.geomspace(0.25, 8, 37); gz = [(float(a), D.groups(float(a), "1")) for a in Ag]; ok = [a for a, g in gz if g and abs(g["Z"]) <= 1.5 and g["verdict"] == "CONSISTENT"]; RES["groups"] = dict(rows=[(a, g["Z"], g["mean"], g["verdict"]) for a, g in gz if g], range=(min(ok), max(ok)) if ok else None); P(f"Groups: |Z| <= 1.5 for A in {RES['groups']['range']}; Z(A=1) {D.groups(1.0, '1')['Z']:+.2f}; Z(A=2) {D.groups(2.0, '1')['Z']:+.2f}; lgM200 median {np.median([math.log10(o['h+0.00']['M2'] / cc['MSUNE']) for o in D.gr['rows']]):.2f}")
xs = [(float(a), D.xcop(float(a), "1")) for a in Ag]; ok = [a for a, x in xs if x["PASS"]]; okr = [a for a, x in xs if x["rms"] <= 0.10]; RES["xcop"] = dict(rows=[(a, x["mean"], x["rms"]) for a, x in xs], range=(min(ok), max(ok)) if ok else None, rms_range=(min(okr), max(okr)) if okr else None); P(f"X-COP (bracket, hydrostatic): line for A in {RES['xcop']['range']}; rms <= 0.10 for A in {RES['xcop']['rms_range']}; lgMtot {np.log10((D.xc['s'].Mout / cc['MSUNE']).mean()):.2f}")
# ------------------------------------------------------- clusters exact
CG = [float(a) for a in np.geomspace(0.5, 5, 19)]; ef = os.path.join(HERE2, "sl2_cluster_exact.json")
if not os.path.exists(ef):
    tf = os.path.join(HERE2, "sl2_trees.json"); json.dump([[a, "1", ["canonical", "alt"]] for a in CG], open(tf, "w")); env = dict(os.environ, SL1_LANE=SL1, SL1_TREES=tf, SL1_OUT=ef); subprocess.run(["nice", "-n", "15", sys.executable, os.path.join(SL1, "sl1_harvest.py"), os.path.join(SL1, "sl1_tail_exact.py")], env=env, stdout=open(os.path.join(HERE2, "sl2_cluster.log"), "w"), stderr=subprocess.STDOUT, check=True)
XJ = json.load(open(ef)); KK = XJ["keys"]; C = {}; P("\n=== Part 1b clusters, exact dvecN, constant A")
for f in ("canonical", "alt"):
    W = np.array([np.maximum(np.abs(r["Z"][f][HKS[0]]), np.abs(r["Z"][f][HKS[1]])) for r in XJ["res"]]); nb = (W > 2).sum(1); C[f] = dict(nbad=nb.tolist(), all15=[CG[i] for i in np.where(nb == 0)[0]], per={k: [CG[i] for i in np.where(W[:, j] <= 2)[0]] for j, k in enumerate(KK)}, W=W.tolist())
    P(f" {f}: all 15 keys for A in {('[%.2f, %.2f]' % (min(C[f]['all15']), max(C[f]['all15']))) if C[f]['all15'] else 'NONE'}")
    P("   A: failing count " + ", ".join(f"{a:.2f}:{n}" for a, n in zip(CG, nb)))
    if f == "canonical":
        for k in ("G-IN-Mall", "G-IN-all", "G-MID-T3", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-OUT-Mall", "G-OUT-all"): q = C[f]["per"][k]; P(f"   {k}: A in {('[%.2f, %.2f]' % (min(q), max(q))) if q else 'NONE on grid'}")
        for i in np.linspace(0, 18, 7).astype(int): P(f"   A {CG[i]:.2f}: fails " + ", ".join(f"{KK[j]} {XJ['res'][i]['Z'][f][HKS[0]][j]:+.2f}" for j in np.where(W[i] > 2)[0]))
RES["clusters"] = C; cm = np.log10((D.cl[HKS[0]]["s"].Mout + 0) / cc["MSUNE"]); P(f" clusters' lg M_cold median {np.median(cm):.2f}")
# ------------------------------------------------------- reads
tag = TA; rowsU = [T1[tag][f"{l}-{h}"] for l, h in BINS]; meds = [r["U0.55"]["med"] for r in rowsU]; lgs = [r["lgM"] for r in rowsU]; PRED = {10: 0.70, 11: 0.80, 12: (0.95, 1.00), 13: 1.35, 14: 2.30}; P("\n=== Relay's curve scored (A(U .55) nearest bin; groups at 13; all-keys at 14)")
near = lambda L: min(range(6), key=lambda i: abs(lgs[i] - L))
for L, v in PRED.items():
    if L <= 12: r = rowsU[near(L)]["U0.55"]; lo, hi = r["ci"]; me = f"bin lgM {lgs[near(L)]:.2f}: {r['med']:.2f} [{lo:.2f},{hi:.2f}]"
    elif L == 13: rg = RES["groups"]["range"]; lo, hi = rg if rg else (None, None); me = f"groups {rg}"
    else: q = C["canonical"]["all15"]; lo, hi = (min(q), max(q)) if q else (None, None); me = f"clusters all keys {(lo, hi)}"
    vv = v if isinstance(v, tuple) else (v, v); hit = lo is not None and vv[1] >= lo and vv[0] <= hi; P(f"  10^{L}: relay {v}; measured {me}: {'HIT' if hit else 'MISS'}")
crossing = [(lgs[i], rowsU[i]["U0.55"]["ci"][0] <= 1 <= rowsU[i]["U0.55"]["ci"][1]) for i in range(6)]; P(f"  A = 1 inside interval by bin (lgM, inside): {[(round(a,2), b) for a, b in crossing]}; A medians {[round(m,2) for m in meds]}; monotonic among bins: {all(meds[i] <= meds[i+1] for i in range(5))}")
# ------------------------------------------------------- q_contract
SGN = 1; X39 = open(os.path.join(RB2, "X39_baryonic_contraction", "x39_contraction.py")).read(); exec(compile(X39[X39.index("def contract(r, Mb, M0, F, gnedin=None):"):X39.index('P("\\n=== checks")')], "x39", "exec"))
def W_(rg, Mb, Mc): dM = np.diff(Mc); rm = 0.5 * (rg[1:] + rg[:-1]); return -ge * float(np.sum(0.5 * (Mb[1:] + Mb[:-1] + Mc[1:] + Mc[:-1]) * dM / rm))
def contr(q, tag, mb=1.0):
    h = q["halo"][tag]; R = h["R200"]; r0 = h["r0"]; Rm = q["Rm"]; rg = np.geomspace(Rm[0] * 0.05, R, 600); Mo = math.pi * h["S"] * r0 ** 2; M0 = Mo * Bf(rg / r0); iu = IU[0.5]; Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * Rm ** 2 / ge, 0.0)) * mb; Mt = max(float(Mbk[-1]), mb * (0.5 * q["L36"] + 1.33 * q["MHI"]) * 1e9 * cc["MSUNE"])
    Mbg = np.where(rg < Rm[0], Mbk[0] * (rg / Rm[0]) ** 2, np.interp(np.log(rg), np.log(Rm), Mbk)); o_ = rg > Rm[-1]
    if o_.any(): t_ = np.clip(np.log(rg[o_] / Rm[-1]) / math.log(3.0), 0, 1); Mbg[o_] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t_) + np.log(Mt) * t_)
    Mbg = np.maximum.accumulate(Mbg); Mf, _, _ = contract(rg, Mbg, M0, Mt / h["M2"]); E = max(0.0, (W_(rg, Mbg, M0) - W_(rg, Mbg, Mf)) / 2); Wc = ge * Mo ** 2 / r0 * I1; Wh = abs(W_(rg, Mbg, M0)); i50 = int(np.argmin(abs(rg - r0))); return E, Wc, Wh, float(Mf[i50] / M0[i50])
Qc = {t: {} for t in TAGS}
for t in TAGS:
    for i, q in enumerate(G): Qc[t][i] = contr(q, t)
_rr = np.geomspace(1e18, 1e22, 4000); _M0 = 1e20 * _rr; _Mz, _, _ = contract(_rr, np.zeros_like(_rr), _M0, 0.0); k2a = float(np.max(np.abs(_Mz / _M0 - 1)[5:-5]))
# ------------------------------------------------------- eps_req
P("\n=== Part 2 eps_req = (1 + q_contract - 1/A_req) / q_diss (W_core0 primary; halo W alternate)"); ER = {}
def line(lab, A, qc, qd, alt=None):
    lo, hi = sorted(((1 + qc - 1 / A[0]) / qd, (1 + qc - 1 / A[1]) / qd)); ER[lab] = (lo, hi); P(f"  {lab}: A [{A[0]:.2f},{A[1]:.2f}], q_contract {qc:.3g}, q_diss {qd:.3g}: eps_req [{lo:.3g}, {hi:.3g}]" + (f"; halo W: q_c {alt[0]:.3g}, q_d {alt[1]:.3g}, eps [{min((1+alt[0]-1/A[0])/alt[1],(1+alt[0]-1/A[1])/alt[1]):.3g}, {max((1+alt[0]-1/A[0])/alt[1],(1+alt[0]-1/A[1])/alt[1]):.3g}]" if alt else ""))
o = D.sparc(SEL, TA); qdv = o["s"].V["q"]; vfs = o["vf"]
for k, (l, h) in enumerate(BINS):
    idx = [j for j, i in enumerate(SEL) if bin_of(G[i]["vf"]) == k]; qc = float(np.median([Qc[TA][SEL[j]][0] / Qc[TA][SEL[j]][1] for j in idx])); qd = float(np.median(qdv[idx])); qca = float(np.median([Qc[TA][SEL[j]][0] / Qc[TA][SEL[j]][2] for j in idx])); qda = float(np.median([qdv[j] * Qc[TA][SEL[j]][1] / Qc[TA][SEL[j]][2] for j in idx])); line(f"V {l}-{h}", rowsU[k]["U0.55"]["ci"], qc, qd, (qca, qda))
rg = RES["groups"]["range"]
if rg: qd = float(np.median([Sys(cc, [10 ** o_["lM"]], [o_["h+0.00"]]).V["q"][0] for o_ in D.gr["rows"]])); line("groups", rg, 0.0, qd)
q = C["canonical"]["all15"]; qd = float(np.median(D.cl[HKS[0]]["s"].V["q"])); c_ = D.cl[HKS[0]]; dM = np.diff(c_["M0"], axis=1); rm = 0.5 * (c_["nd"][:, 1:] + c_["nd"][:, :-1]); Wha = ge * np.sum(0.5 * (c_["Mb"][:, 1:] + c_["Mb"][:, :-1] + c_["M0"][:, 1:] + c_["M0"][:, :-1]) * dM / rm, axis=1); Wco = ge * (math.pi * c_["s"].S * c_["s"].r0 ** 2) ** 2 / c_["s"].r0 * I1; qda = float(np.median(c_["s"].V["q"] * Wco / Wha))
if q: line("clusters, 15 keys", (min(q), max(q)), 0.0, qd, (0.0, qda))
else: P(f"  clusters: no constant A clears 15 keys; q_diss {qd:.3g}")
ov = (max(v[0] for v in ER.values()), min(v[1] for v in ER.values())); disagree = ov[0] > ov[1]; P(f"  overlap of all intervals: max lower {ov[0]:.3g}, min upper {ov[1]:.3g}: {'NO OVERLAP' if disagree else 'OVERLAP'}")
# ------------------------------------------------------- forward, eps fitted
LB = np.array([G[i]["lMb"] for i in range(len(G))]); QCA = np.array([Qc[TA][i][0] / Qc[TA][i][1] for i in range(len(G))]); srt = np.argsort(LB)
def setqc(eps):
    EPS["v"] = eps
TREE = ("inv1p", ("sub", "qc", ("mul", "Eps", "q")))
for idx in (D.split["train"], D.split["holdout"], SEL, list(range(len(G)))):
    for t in TAGS: o_ = D.sparc(idx, t); o_["s"].V["qc"] = np.array([Qc[t][i][0] / Qc[t][i][1] for i in idx])
for t in TAGS: qq = np.array([Qc[t][i][0] / Qc[t][i][1] for i in range(len(G))]); D.lt[t]["s"].V["qc"] = np.interp([r["logMb"] for r in D.C["lt"]], LB[srt], np.log1p(qq[srt])); D.lt[t]["s"].V["qc"] = np.expm1(D.lt[t]["s"].V["qc"])
P("\n=== Forward: one FITTED eps, train gates, surrogate"); FW = []
for eps in np.r_[0.0, np.geomspace(1e-6, 1.0, 121)]:
    setqc(float(eps)); r = D.grade(TREE, "1"); FW.append((float(eps), None if r is None else dict(gate=r["gate"], g1=r["g1"], g2=r["g2"], g3=r["g3"], g4=r["g4"], bad=r["detail"]["bad"], U=r["detail"][TA]["U"], tilt=r["detail"][TA]["tilt"])))
val = [(e, r) for e, r in FW if r]; P(f"  eps bound on every system: {len(val)}/{len(FW)}, range {val[0][0] if val else None}..{val[-1][0] if val else None}"); P(f"  q_contract median SPARC {np.median(QCA):.3g}; A at r0 from contraction M_f/M_0 median {np.median([Qc[TA][i][3] for i in SEL]):.2f}")
for e, r in sorted(val, key=lambda x: x[1]["gate"])[:3] + ([val[0]] if val else []): P(f"  eps {e:.3g}: gate {r['gate']:.3f} g1 {r['g1']:.2f} g2 {r['g2']:.2f} g3 {r['g3']:.2f} g4 {r['g4']:.2f} U {r['U']:.2f} tilt {r['tilt']:+.2f} bad {r['bad']}")
best = min(val, key=lambda x: x[1]["gate"]) if val else None; lab = "FAILS, SCALES DISAGREE" if disagree or not q else ("FAILS: " + str({k: round(best[1][k], 2) for k in ("g1", "g2", "g3", "g4")}) if best and best[1]["gate"] > 0 else "GATES CLEAR, GAUNTLET PENDING"); P("VERDICT: " + lab + " (eps FITTED)")
# ------------------------------------------------------- checks
_o = D.sparc(SEL, TA); _f0, _f1 = D.sparc_fit(_o, "1", "1", a0), D.sparc_fit(_o, 1.0, "1", a0); k1 = float(np.max(np.abs(_f0[1] - _f1[1]))) < 1e-9 and abs(D.xcop(1.0, "1")["rms"] - D.C["xcop"]["canonical"]["rms"]) < 1e-9; q0 = G[SEL[60]]; h = q0["halo"][TA]; iu = IU[0.55]; re = 0.8 * h["r0"]; Mo = math.pi * h["S"] * h["r0"] ** 2 * Bf(h["R200"] / h["r0"]); gp = np.log10(np.maximum(q0["GB"][:, iu] + ge * Mo * Bf(q0["Rm"] / re) / Bf(h["R200"] / re) / q0["Rm"] ** 2, 1e-300)); got = A_ups(q0, TA, 0.55, gp); k3 = abs(math.log(got / 0.8)) <= math.log(GRID[1] / GRID[0]); m2 = np.median([contr(G[i], TA, 2.0)[0] / contr(G[i], TA)[0] for i in SEL[:20] if contr(G[i], TA)[0] > 0])
P(f"\nK1 A = 1 returns SL1's baseline: {'PASS' if k1 else 'FAIL'}; K2 contraction identity {k2a:.1e}: {'PASS' if k2a < 1e-6 else 'FAIL'}; K3 planted 0.8 -> {got:.3f}: {'PASS' if k3 else 'FAIL'}; MUTATE M_b x 2 moves E_contract x {m2:.2f}: {'BITES' if abs(m2-1) > 0.05 else 'NO BITE'}")
P("\n=== Post-result, reported only: constant A on train, surrogate")
for v in (0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0):
    EPS["v"] = v; r = D.grade("Eps", "1"); gg = D.groups(v, "1"); xx = D.xcop(v, "1"); P(f"  A {v}: g1 {r['g1']:.2f} g2 {r['g2']:.2f} g3 {r['g3']:.2f} g4 {r['g4']:.2f}; U {r['detail'][TA]['U']:.2f}/{r['detail'][TB]['U']:.2f} tilt {r['detail'][TA]['tilt']:+.2f}/{r['detail'][TB]['tilt']:+.2f}; S_z {[round(z,1) for z in r['detail']['S_z']]}; LT {r['detail']['E_'+TA]:+.3f}; groups Z {gg['Z']:+.2f}")
for v in (0.8, 1.0, 1.22, 1.39, 1.58, 1.8, 2.04, 3.0): xx = D.xcop(v, "1"); P(f"  X-COP A {v}: mean {xx['mean']:+.3f} rms {xx['rms']:.3f}")
json.dump(dict(RES=RES, ER=ER, forward=FW, verdict=lab), open(os.path.join(HERE2, "sl2_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE2, "sl2.out"), "w").write("\n".join(OUT) + "\n")
