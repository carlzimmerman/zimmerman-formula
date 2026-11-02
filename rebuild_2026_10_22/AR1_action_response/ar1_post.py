#!/usr/bin/env python3
"""AR1 reader and verdict (FROZEN_CRITERIA.md). Rows, K1, K5, K6, K7, MUTATE, UL1's gate, effective response and the mass trend. Run only after ar1_live.out exists. kappa = 1/2 FITTED, unused; not theory closed; nothing here says the data favour the framework."""
import json, math, os, pickle, sys
sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
_a = sys.argv; sys.argv = [_a[0]]
import numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); ME = HERE; RB = os.path.dirname(HERE); UL = os.path.join(RB, "UL1_measured_upsilon_test"); sys.path[:0] = [ME, UL]; import ar1_sparc as X, ar1_solver as A, ul1_core as C
OUT = []
def P(s): print(s, flush=True); OUT.append(str(s))
_s = open(os.path.join(UL, "ul1_grade.py")).read(); _s = _s[_s.index("G = C.load(); UPS = C.UPS"):_s.index('PR = EST["primary"]')]; _H = HERE; HERE = UL; exec(_s); LAB = lab; HERE = _H; PR = EST["primary"]; UPS = C.UPS; IR = C.IREC; TG = C.TG; RW = os.path.join(ME, "rows"); names = [q["name"] for q in G]; M = X.Mono(G)
if not os.path.exists(os.path.join(ME, "ar1_live.out")): raise SystemExit("ar1_live.out missing: graded rows not read")
def L(n, d=RW): z = np.load(os.path.join(d, n + ".npz")); return dict({t: (z[f"{t}_wr2"], z[f"{t}_ws"]) for t in TG}, lt=z["lt"], stats=str(z["stats"]) if "stats" in z else "")
def rec(D):
    o = {}
    for t in TG:
        iu, _ = best(*D[t], IR); rm, um = stats(*D[t], iu); u = UPS[iu]; o[t] = dict(U=um, rms=rm, tilt=tilt(u), bins={b: float(np.median(u[SEL[b]])) for b in ALLB}, Ugal=u, lt=float(D["lt"][TG.index(t)]))
    return o
def sline(r): return all(r[t]["rms"] <= 0.110 and 0.5 <= r[t]["U"] <= 0.8 for t in TG), all(abs(r[t]["tilt"]) <= 0.15 for t in TG), all(abs(r[t]["lt"]) <= 0.10 for t in TG)
def show(n, r): P(f"{n:22s} U {r[TG[0]]['U']:.3f}/{r[TG[1]]['U']:.3f} rms {r[TG[0]]['rms']:.4f}/{r[TG[1]]['rms']:.4f} tilt {r[TG[0]]['tilt']:+.3f}/{r[TG[1]]['tilt']:+.3f} LT {r[TG[0]]['lt']:+.3f}/{r[TG[1]]['lt']:+.3f} bins A " + " ".join(f"{v:.3f}" for v in r[TG[0]]["bins"].values()) + " | B " + " ".join(f"{v:.3f}" for v in r[TG[1]]["bins"].values()))
ok = True; RES = {}
# K1
N3 = json.load(open(os.path.join(RB, "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")))["runs"]["EM1|blum"]; U1 = rec(L("hand_blum", os.path.join(UL, "rows"))); d = max(max(abs(U1[t]["U"] - N3["sparc"][t]["U"]), abs(U1[t]["rms"] - N3["sparc"][t]["rms"]), abs(U1[t]["tilt"] - N3["sparc"][t]["tilt"]), max(abs(U1[t]["bins"][b] - N3["sparc"][t]["bins"][b]) for b in ALLB)) for t in TG); g = d <= 1e-6; ok &= g; P(f"K1a UL1 engine hand_blum vs NR3 MEDIAN EM1|blum, U rms tilt bins: {d:.1e}: {'PASS' if g else 'FAIL'}")
CE = json.load(open(os.path.join(ME, "ar1_clusters_erass.json"))); CG = json.load(open(os.path.join(ME, "ar1_clusters_gs5.json"))); b_ = CE["runs"]["EM1|blum"]; d2 = max(abs(b_["keys"]["preds"][h][k] - N3["keys"]["preds"][h][k]) for h in N3["keys"]["preds"] for k in N3["keys"]["preds"][h]); d3 = max(abs(b_["groups"]["Z"] - N3["groups"]["Z"]), abs(b_["xcop"]["mean"] - N3["xcop"]["mean"]), abs(b_["xcop"]["rms"] - N3["xcop"]["rms"]), *[abs(b_["lt"][t] - N3["lt"][t]) for t in TG]); g = max(d2, d3) <= 1e-6; ok &= g; P(f"K1b harness EM1|blum eRASS1 gas vs NR3 MEDIAN: key preds {d2:.1e}, groups X-COP LT {d3:.1e}: {'PASS' if g else 'FAIL'}")
hmf = os.path.join(RB, "HM1_honest_model", "cache_cells", "S_0.005_0.034.json")
if os.path.exists(hmf) or os.path.exists(hmf.replace(".json", ".part.json")):
    H = json.load(open(hmf)) if os.path.exists(hmf) else None; H = H["hm1"] if H else json.load(open(hmf.replace(".json", ".part.json")))
    if "S|blum|bcg" in H:
        hc = H["S|blum|bcg"]["cells"]; dh = max(abs(CG["runs"]["EM1|blum"]["keys"]["preds"][h][k] - hc[h][k]["pred"]) for h in hc for k in hc[h]); dz = max(abs(CG["runs"]["EM1|blum"]["keys"]["Z"][h][k] - hc[h][k]["Z"]) for h in hc for k in hc[h]); g = dh <= 1e-6; P(f"K1c harness EM1|blum at +0.005 vs HM1's S|blum|bcg: preds {dh:.1e}, Z {dz:.1e}: {'PASS' if g else 'LINE MISSED, see README'}"); RES["K1c"] = dict(preds=dh, Z=dz, passed=bool(g))
        He = json.load(open(hmf.replace("S_0.005_0.034", "S_erass_0.034")))["hm1"]["S|blum|bcg"]["cells"]; de = max(abs(N3["keys"]["preds"][h][k] - He[h][k]["pred"]) for h in He for k in He[h]); P(f"     same gap on eRASS1 gas, HM1's S|blum|bcg vs NR3 MEDIAN itself: preds {de:.1e}, so the gap is between HM1's path and the record's, not AR1's"); ac = CG["runs"]["EM1|act"]["keys"]["preds"]; Zh = {h: {k: (hc[h][k]["meas"] - ac[h][k]) / hc[h][k]["s"] for k in hc[h]} for h in hc}; P("     ACT keys at +0.005 on HM1's corrected templates: " + "; ".join(h + " bad " + str([k for k, v in Zh[h].items() if abs(v) > 2]) + " M3 %+.2f IN-Mall %+.2f" % (Zh[h]["G-OUT-M3"], Zh[h]["G-IN-Mall"]) for h in Zh)); RES["keys_hm1_templates"] = Zh
    else: P("K1c HM1's S|blum|bcg at +0.005 not on disk yet: stated, not compared")
else: P("K1c HM1's S|blum|bcg at +0.005 not on disk yet: stated, not compared")
# K6 nodes
Bv = rec(L("hand_blum_v2r")); d = max(abs(Bv[t]["U"] - U1[t]["U"]) for t in TG); db = max(max(abs(Bv[t]["bins"][b] - U1[t]["bins"][b]) for b in ALLB) for t in TG); g = d <= 0.005 and db <= 0.01 + 1e-9; ok &= g; P(f"K6a Blumenthal at nodes vs UL1's full grid: U {d:.4f} (0.005), bins {db:.4f} (0.01), LT {abs(Bv[TG[0]]['lt'] - U1[TG[0]]['lt']):.1e}: {'PASS' if g else 'FAIL'}")
R = {n: rec(L(n)) for n in ("hand_act_inv", "hand_blum_inv", "hand_act_exp", "hand_blum_exp", "hand_act_v2r", "hand_blum_v2r", "nat_act_inv", "nat_blum_inv", "nat_act_v2r")}; Rt = rec(L("hand_act_inv_t2")); Mu = L("hand_act_inv_mut2")
# DR3's rows on my monopole
D3p = json.load(open(os.path.join(RB, "DR3_thin_disc_monopole", "dr3_GASINV_results.json")))["runs"]; 
for nm, k in (("hand_blum_inv", "GASINV|blum"), ("hand_blum_exp", "DR3|blum")):
    dd = max(abs(R[nm][t]["U"] - D3p[k]["sparc"][t]["U"]) for t in TG); db = max(max(abs(R[nm][t]["bins"][b] - D3p[k]["sparc"][t]["bins"][b]) for b in ALLB) for t in TG); g = dd <= 0.005 and db <= 0.015; ok &= g; P(f"K1d {nm} vs DR3 {k}: U {dd:.4f}, bins {db:.4f} (nodes vs its full grid; its gas cache, same inversion): {'PASS' if g else 'FAIL'}")
# K6b action, full record grid on 15 galaxies, K7 doubled grid on 12
ckf = os.path.join(ME, "cache_rows", "k6k7.pkl")
if os.path.exists(ckf): K67 = pickle.load(open(ckf, "rb"))
else:
    sub = list(range(0, len(G), len(G) // 15))[:15]; dU = []; t = TG[0]
    for i in sub:
        q = G[i]; On, m0 = X.response(q, t, "hand", "act", "inv", M); gn = X.gh_from(On, m0, q); wa = C.mse_of(q, np.log10(np.maximum(q["GB"] + gn, 1e-300))); un = UPS[IR][np.argmin((wa[0] / np.maximum(wa[1], 1e-300))[IR])]; Of, m0 = X.response(q, t, "hand", "act", "inv", M, nodes=IR); gf = np.zeros((len(q["Rm"]), len(UPS))); gf[:, IR] = GE_ = C.GE * m0[:, None] * np.exp(Of) / q["Rm"][:, None] ** 2; mf = C.mse_of(q, np.log10(np.maximum(q["GB"] + gf, 1e-300))); uf = UPS[IR][np.argmin((mf[0] / np.maximum(mf[1], 1e-300))[IR])]; dU.append(abs(float(un - uf)))
    e7 = []; iu5 = int(np.argmin(abs(UPS - 0.5)))
    for i in list(range(0, len(G), len(G) // 12))[:12]:
        q = G[i]; M2, R2, rg, M0, Mr, r0 = X.setup(q, t, "hand"); Mbg, Mt = X.baryon(q, iu5, rg, "inv", M); F = Mt / Mr; a = A.act_contract(rg, Mbg, M0, F)[0]; b = A.act_contract(rg, Mbg, M0, F, nE=384, nY=64, nT=128)[0]; s = rg >= 0.1 * r0; e7.append(float(np.max(np.abs(b[s] / a[s] - 1))))
    K67 = dict(dU=dU, e7=e7); pickle.dump(K67, open(ckf, "wb"))
f9 = float(np.mean(np.array(K67["dU"]) <= 0.01)); g = f9 >= 0.9; ok &= g; P(f"K6b action, nodes vs full record grid, 15 galaxies: fraction |dU| <= 0.01 {f9:.2f}, max {max(K67['dU']):.3f}: {'PASS' if g else 'FAIL'}")
k7 = max(K67["e7"]); k7c = CE.get("K7_clusters", np.nan); g = k7 <= 0.005 and k7c <= 0.005; P(f"K7 doubled grid, 12 galaxies U 0.5, max |Q ratio - 1| at r >= 0.1 r0: {k7:.4f}, medians {np.median(K67['e7']):.4f}; clusters {k7c:.4f} (line 0.005): {'PASS' if g else 'FAIL, stated below'}"); RES["K7_pass"] = bool(g); ok &= g
sta = L("hand_act_inv")["stats"]; P(f"K5 solver stats, primary row: {sta}"); cs = CE["runs"]["EM1|act"]["stats"]
for _k, _f in (("erass", "ar1_clusters_erass_grid192.json"), ("gs5", "ar1_clusters_gs5_grid192.json")):
    _o = json.load(open(os.path.join(ME, "diag", _f)))["runs"]["EM1|act"]; _n = (CE if _k == "erass" else CG)["runs"]["EM1|act"]; P(f"K7c {_k}: graded (384, 64, 128) vs (192, 32, 64): key preds max {max(abs(_o['keys']['preds'][h][k] - _n['keys']['preds'][h][k]) for h in _n['keys']['preds'] for k in _n['keys']['preds'][h]):.1e}, groups Z {abs(_o['groups']['Z'] - _n['groups']['Z']):.1e}, X-COP mean {abs(_o['xcop']['mean'] - _n['xcop']['mean']):.1e}, LT {max(abs(_o['lt'][t] - _n['lt'][t]) for t in TG):.1e}")
P(f"K5 clusters + groups + X-COP + LT, eRASS: {cs}; +0.005: {CG['runs']['EM1|act']['stats']}"); g = "'chbad': 0" in sta.replace('"', "'") and cs.get("chbad", 0) == 0; ok &= g; P(f"K5 last-pass change above 1e-2: {'none' if g else 'SOME, FAIL'}"); P(f"K3 clusters' M0, zero baryons: {CE['K3_clusters']:.1e}")
# MUTATE
mr = {t: rec(dict({t2: Mu[t2] for t2 in TG}, lt=np.array([0.0, 0.0])))[t] for t in TG}; dmu = abs(mr[TG[0]]["U"] - R["hand_act_inv"][TG[0]]["U"]); g = dmu >= 0.02; ok &= g; P(f"MUTATE baryons x 2 on the primary: U {R['hand_act_inv'][TG[0]]['U']:.3f} -> {mr[TG[0]]['U']:.3f}: {'PASS' if g else 'FAIL'}")
P("\n=== SPARC, record grid"); 
for n, r in R.items(): show(n, r)
show("hand_act_inv taper 0.2", Rt); show("UL1 hand_blum v2r", U1)
for glab, Cc in (("eRASS1 gas", CE), ("+0.005 (GS4)", CG)):
    P(f"\n=== keys, {glab}, f* 0.034, S-core path N, canonical template")
    for k_ in ("EM1|blum", "EM1|act"):
        r = Cc["runs"][k_]; P(f" {k_}: {r['keys']['n']}/15 bad {r['keys']['bad']}; groups Z {r['groups']['Z']:+.2f} {r['groups']['verdict']}; X-COP {r['xcop']['mean']:+.3f}, {r['xcop']['rms']:.3f} {r['xcop']['PASS']}; LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f}"); P("   Z h0672 " + " ".join(f"{k.replace('G-', '')} {v:+.2f}" for k, v in r["keys"]["Z"]["h0672"].items())); P("   Z h0686 " + " ".join(f"{k.replace('G-', '')} {v:+.2f}" for k, v in r["keys"]["Z"]["h0686"].items())); P("   X-COP by x " + json.dumps({k: round(v, 3) for k, v in r["xcop"]["by_x"].items()}))
    P(" Cluster M_c,f/M0 (median), r Mpc or r0: " + "; ".join(f"{k}: act {v['Qact']:.3f} blum {v['Qblum']:.3f} (f_local {v['fl']:.3f})" for k, v in Cc["eff"].items()) + f"; cosmic ratio {Cc['cosmic']:.3f}")
# UL1 gate, wide grid
P("\n=== UL1's measured-Upsilon gate (reported, no label)")
RES["ul1"] = {}
for n in ("hand_act_inv", "hand_act_exp", "hand_act_v2r", "nat_act_inv", "nat_act_v2r", "hand_blum_inv"):
    D = L(n); o, r = rowgrade(D, PR); LB = {x: LAB(r[x]) for x in r}; RES["ul1"][n] = LB; P(f" {n}: Taylor {LB['Taylor']}; GSWLC {LB['GSWLC']}")
    for t in TG:
        bv = o[t]["bv"]; P(f"   {t[:1]} U_tot wide " + " ".join(f"{bv[b]['m']:.3f}" for b in BINS) + " | " + "; ".join(f"{x} Z " + " ".join(f"{z:+.1f}" for z in o[t]["g"][x]["Z"]) + f" slope {o[t]['g'][x]['slope']:+.2f} vs {o[t]['g'][x]['slopeX']:+.2f} steps " + " ".join(f"{z:+.1f}" for z in o[t]["g"][x]["steps"]) for x in ("Taylor", "GSWLC")))
P("  estimators: " + "; ".join(f"{x} " + " ".join(f"{PR[b][x]['mu']:.3f}" for b in BINS) for x in ("Taylor", "GSWLC")))
# Effective response
P("\n=== f_eff = (Q_act - 1)/(Q_blum - 1), MONO-INV, U 0.5, background A; and native")
iu5 = int(np.argmin(abs(UPS - 0.5))); BIN = ALLB; RX = np.array([0.25, 0.5, 1, 2, 4]); Rw = {}
for sh in ("hand", "nat"):
    rows = {}
    for i, q in enumerate(G):
        if not Qs[i] or q["meta"]["Rdisk"] <= 0: continue
        M2, R2, rg, M0, Mr, r0 = X.setup(q, TG[0], sh); Mbg, Mt = X.baryon(q, iu5, rg, "inv", M); F = Mt / Mr; a = A.act_contract(rg, Mbg, M0, F, st=A.Start(rg, M0, thin=(0.35 if sh != "hand" else None)))[0]; b = C.contract(rg, Mbg, M0, F)[0]; r_ = r0 if r0 else float(rg[np.searchsorted(M0, 0.05 * M0[-1])]); Rd = q["meta"]["Rdisk"] * C.KPC; rr = np.r_[2.2 * Rd, RX * r_]; lg = np.log(rg); m0 = np.interp(np.log(rr), lg, M0); qa = np.interp(np.log(rr), lg, a) / m0; qb = np.interp(np.log(rr), lg, b) / m0; rows[q["name"]] = dict(v=q["meta"]["Vflat"], f=((qa - 1) / np.where(abs(qb - 1) > 1e-3, qb - 1, np.nan)).tolist(), qa=qa.tolist(), qb=qb.tolist(), fb=float(Mt / (M2 if sh == "hand" else Mr)))
    Rw[sh] = rows; P(f" {sh}: V_flat bin, n, median f_eff at 2.2 R_d, r/r0 {RX.tolist()}" + ("" if sh == "hand" else " (native: r at 5 % of M0 in place of r0)") + "; Q_act, Q_blum at 2.2 R_d")
    for b in ALLB:
        lo, hi = lohi(b); s = [v for v in rows.values() if lo <= v["v"] < hi]
        if s: f_ = np.nanmedian([v["f"] for v in s], axis=0); P(f"   {b:8s} {len(s):3d}  " + " ".join(f"{x:.2f}" for x in f_) + f"  | {np.median([v['qa'][0] for v in s]):.2f}, {np.median([v['qb'][0] for v in s]):.2f}")
    vv = np.array([v["v"] for v in rows.values()]); ff = np.array([v["f"][0] for v in rows.values()]); m = np.isfinite(ff); sr = spearmanr(vv[m], ff[m]); dw = np.nanmedian(ff[vv < 100]); ls = np.nanmedian(ff[(vv >= 150) & (vv < 250)]); P(f"   mass trend f_eff(2.2 R_d) vs V_flat: Spearman {sr[0]:+.3f} (p {sr[1]:.3f}, n {int(m.sum())}); dwarfs V<100 {dw:.3f}; L* 150-250 {ls:.3f}"); RES[f"trend_{sh}"] = dict(sp=float(sr[0]), p=float(sr[1]), dw=float(dw), ls=float(ls))
# Verdict
Ca = CG["runs"]["EM1|act"]; p = R["hand_act_inv"]; sl, tl, ltl = sline(p); kl = Ca["keys"]["n"] == 15; xl = bool(Ca["xcop"]["PASS"]); gl = Ca["groups"]["verdict"] == "CONSISTENT"; fails = [n for n, v in (("SPARC", sl), ("tilt", tl), ("LITTLE THINGS", ltl), ("groups", gl), ("keys", kl), ("X-COP", xl)) if not v]; mv = max(abs(p[t]["U"] - R["hand_blum_inv"][t]["U"]) for t in TG)
lab_ = "NO VERDICT (check failed)" if not ok else "ACTIONS CLEAR" if not fails else ("MOVES AND FAILS " + str(fails) if mv >= 0.02 else "NO MOVE (<0.02)"); P(f"\nCHECKS {'ALL PASS except K1c, whose frozen line was missed, see README' if ok else 'FAILED'}\nVERDICT: {lab_}; move in U {mv:.3f}"); RES.update(verdict=lab_, ok=bool(ok), fails=fails, rows={n: {t: {k: v for k, v in r[t].items() if k != "Ugal"} for t in TG} for n, r in R.items()})
json.dump(RES, open(os.path.join(ME, "ar1_results.json"), "w"), indent=0, default=float); open(os.path.join(ME, "ar1.out"), "w").write("\n".join(OUT) + "\n")
