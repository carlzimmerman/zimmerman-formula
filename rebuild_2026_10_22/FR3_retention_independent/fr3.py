#!/usr/bin/env python3
"""FR3 part A (FROZEN_CRITERIA.md): Okabe x eRASS1 gas, Umetsu x E16, HIFLUGCS, eFEDS; line R. python3 -I fr3.py [--mutate]. Reinstates nothing. kappa = 1/2 FITTED, unused; not theory closed."""
import csv, json, math, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); sys.path.insert(0, HERE)
import numpy as np
from astropy.io import fits
from scipy.optimize import minimize
import fr3_parse as FP
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; CK = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(k, ok, v): CK[k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} ({v})")
LG = math.log10(6.2715); G = 1.05; SEED = 20261101; NB = 2000
H = (-0.121, 0.219); W = (-0.321, 0.263); LN = json.load(open(os.path.join(RB, "FR1_fair_share_retention", "fr1_line.json")))
HL = LN["H"]; HG = LN["HG"]; WXXL = LN["W_E16"]; line = lambda L, x: L[0] + L[1] * (x - 14.5)
# Eq. 17, Table B.1 M500 column
AL, BE, GA, DE = .079, .965, .665, -.258
Fz = lambda z: np.log((1 + z) / 1.21)
def to_true(M, z): F = Fz(z); return 1e14 * np.exp((np.log(M / 1e14) - AL - GA * F) / (BE + DE * F))
def to_wl(M, z): F = Fz(z); return 1e14 * np.exp(AL + (BE + DE * F) * np.log(M / 1e14) + GA * F)
# eRASS1
h = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data
E = {str(n).strip().split("J")[-1]: i for i, n in enumerate(h["NAME"])}
eMg, eM, eR, eZ, eCR, eRA, eDE = [np.array(h[k], float) for k in ("MGAS500", "M500", "R500", "BEST_Z", "CR500", "RA", "DEC")]; eMg = eMg * 1e11; eM = eM * 1e13
XT = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json"))); XC = []
for n, v in XT.items():
    p = os.path.join(REPO, "real_research", "data", "xcop", n, f"{n}_fgas_profile.fits")
    if os.path.exists(p):
        with fits.open(p) as q: XC.append((float(q[1].header["RA"]), float(q[1].header["DEC"]), v["z"]))
def sep(a, b, c, d):
    a, b, c, d = map(np.radians, (a, b, c, d)); return np.degrees(np.arccos(np.clip(np.sin(b) * np.sin(d) + np.cos(b) * np.cos(d) * np.cos(a - c), -1, 1)))
isx = lambda ra, de, z: any(sep(ra, de, x[0], x[1]) * 60 <= 6 and abs(z - x[2]) <= .02 for x in XC)
def Ez2(z, Om=.3): return Om * (1 + z) ** 3 + 1 - Om
Rho = lambda z: 3 * (70e3 / 3.0857e22) ** 2 * Ez2(z) / (8 * math.pi * 6.674e-11)
M_R = lambda Rk, z: 500 * Rho(z) * 4 / 3 * math.pi * (Rk * 3.0857e19) ** 3 / 1.989e30
# Okabe
ok = FP.okabe(); P("Parse")
nm = sum(r["id"] in E for r in ok); miss = [r["id"] for r in ok if r["id"] not in E]; check("K2a Okabe rows 78, with mass 72, id match 76", len(ok) == 78 and sum(r["M500"] is not None for r in ok) == 72 and nm == 76, f"{len(ok)}, {sum(r['M500'] is not None for r in ok)}, match {nm}, missing {miss}")
good = [i for i in range(len(eM)) if eM[i] > 0 and eR[i] > 0]; rt = np.log10(eM[good] / M_R(eR[good], eZ[good])); check("K2b eRASS1 M500 vs R500 at h 0.7, Om 0.3", abs(np.median(rt)) < .01 and np.percentile(np.abs(rt), 99) < .02, f"median {np.median(rt):+.4f} dex, 99% {np.percentile(np.abs(rt), 99):.4f}")
T = []
for r in ok:
    if r["id"] not in E or r["flag"] == "*" or r["z"] > .5: continue
    i = E[r["id"]]
    if not (eMg[i] > 0): continue
    T.append(dict(r, i=i, mg=eMg[i], mc=eM[i], cr=eCR[i], rc=eR[i], dz=abs(r["z"] - eZ[i]), s=.5 * (r["up"] + r["dn"]) * 1e14 if r["M500"] is not None else float("nan"), m=r["M500"] * 1e14 if r["M500"] is not None else float("nan")))
dzs = sorted(t["dz"] for t in T); check("K2c matched redshifts: at most one |dz| > 0.05, kept as frozen, effect printed", dzs[-2] < .05, f"largest {dzs[-1]:.3f}, next {dzs[-2]:.3f}, N {len(T)} z <= 0.5 with eRASS1 gas")
ALL = np.array([t["mg"] for t in T]); zA = np.array([t["z"] for t in T]); sA = np.array([t["s"] for t in T]); mA = np.array([t["m"] for t in T]); mcA = np.array([t["mc"] for t in T]); crA = np.array([t["cr"] for t in T]); pf = np.array([t["flag"] == "♮" for t in T]); nomass = ~np.isfinite(mA)
ZB = np.array([0, .2, .35, .5001]); zb = np.clip(np.digitize(zA, ZB) - 1, 0, 2); s_med = np.array([np.nanmedian(sA[zb == k]) for k in range(3)]); wA = 1 / s_med[zb] ** 2; P(f"  median table error by z bin, 1e14: {(s_med / 1e14).round(2).tolist()}; N eligible with mass {int((~nomass).sum())}, poor-fit with value {int((pf & ~nomass).sum())}, no value {int(nomass.sum())}")
def est(ix, m=None, g=G, corr=True):
    m = mA if m is None else m; w = wA[ix]; mb = np.sum(w * m[ix]) / w.sum(); zb_ = np.sum(w * zA[ix]) / w.sum(); mt = float(to_true(np.array(mb), zb_)) if corr and mb > 0 else mb; mgb = np.sum(w * ALL[ix]) / w.sum(); mcb = np.sum(w * mcA[ix]) / w.sum(); d = math.log10(mt / mcb) / 3; mg = mgb * 10 ** (g * d); return dict(x=math.log10(mt), lgY=math.log10(6.2715 * mg / mt), lgMg=math.log10(mg), delta=d, n=int(len(ix)), raw_shift=math.log10(mb / mt), z=zb_, mcat=math.log10(mcb), mbar=mb)
def boot(ix, m=None, **k):
    rg = np.random.default_rng(SEED); Y = []; X = []
    for _ in range(NB):
        e = est(rg.choice(ix, len(ix)), m, **k); Y.append(e["lgY"]); X.append(e["x"])
    return np.std(Y), np.std(X), np.array(Y), np.array(X)
lgm = np.log10(ALL); hasm = ~nomass
BIN = (12.75, 13.58)
if MUT:
    lmw = np.log10(np.clip(mA, 1e10, None)); pri = np.where(hasm & (lmw >= 14) & (lmw < 14.5))[0]; P("MUTATE (a): binned on WL mass 14-14.5")
else: pri = np.where(hasm & (lgm >= BIN[0]) & (lgm < BIN[1]))[0]
e0 = est(pri); sY, sX, By, Bx = boot(pri); D_b = By - (H[0] + H[1] * (Bx - 14.5))
P(f"\nPRIMARY bin: N {e0['n']}, gas bin {BIN}, mean z {e0['z']:.3f}, weighted lg Mg {e0['lgMg']:.3f}"); P(f"  raw lg<M_WL> {math.log10(e0['mbar']):.3f}, eq. 17 shift {e0['raw_shift']:+.4f}, corrected x {e0['x']:.3f} +- {sX:.3f}; lg<M_cat> {e0['mcat']:.3f}, aperture delta {e0['delta']:+.4f}")
P(f"  lg Y500 {e0['lgY']:+.3f} +- {sY:.3f}. H there {line(H, e0['x']):+.3f}, W {line(W, e0['x']):+.3f}")
e_raw = est(pri, corr=False); e_g1 = est(pri, g=.75); e_g2 = est(pri, g=1.35); Sap = .5 * abs(e_g2["lgY"] - e_g1["lgY"]); Sbi = .5 * abs(e_raw["lgY"] - e0["lgY"] + 0); P(f"  raw (no eq. 17): x {e_raw['x']:.3f} lg Y {e_raw['lgY']:+.3f}, D_H {e_raw['lgY'] - line(H, e_raw['x']):+.3f}, D_W {e_raw['lgY'] - line(W, e_raw['x']):+.3f}")
# Per-cluster median
pc = np.array([math.log10(6.2715 * ALL[i] * (max(mA[i], 1e12) / mcA[i]) ** (G / 3) / max(mA[i], 1e12)) for i in pri]); P(f"  per-cluster aperture, median lg Y (reported only, log noise biased) {np.median(pc):+.3f}, values with M < 1e13 floored")
# CR cross-check
if not MUT:
    ord_ = np.argsort(crA); rk = np.empty(len(ord_), int); rk[ord_] = np.arange(len(ord_)); r0 = np.median(rk[pri]); dist = np.abs(rk - r0); cand = np.where(hasm)[0]; cri = cand[np.argsort(dist[cand])[:len(pri)]]; ec = est(cri); scy = boot(cri)[0]; P(f"  CR-rank bin N {ec['n']}: x {ec['x']:.3f}, lg Y {ec['lgY']:+.3f} +- {scy:.3f}, D_H {ec['lgY'] - line(H, ec['x']):+.3f}, D_W {ec['lgY'] - line(W, ec['x']):+.3f}"); RES["CR"] = ec
    n_pf = pri[~pf[pri]]; epf = est(n_pf); P(f"  without poor-fit N {epf['n']}: x {epf['x']:.3f}, lg Y {epf['lgY']:+.3f}, D_H {epf['lgY'] - line(H, epf['x']):+.3f}, D_W {epf['lgY'] - line(W, epf['x']):+.3f}"); RES["no_poorfit"] = epf
    m0 = np.where(nomass, 0.0, mA); pz = np.where((lgm >= BIN[0]) & (lgm < BIN[1]))[0]; e_0 = est(pz, m0); P(f"  unmeasured as M = 0, N {e_0['n']}: x {e_0['x']:.3f}, lg Y {e_0['lgY']:+.3f}, D_H {e_0['lgY'] - line(H, e_0['x']):+.3f}, D_W {e_0['lgY'] - line(W, e_0['x']):+.3f}"); RES["unmeasured_zero"] = e_0
    dzarr = np.array([t["dz"] for t in T]); ed = est(pri[dzarr[pri] < .05]); P(f"  without the |dz| 0.139 cluster N {ed['n']}: x {ed['x']:.3f}, lg Y {ed['lgY']:+.3f}, D_H {ed['lgY'] - line(H, ed['x']):+.3f}, D_W {ed['lgY'] - line(W, ed['x']):+.3f}"); RES["no_dz"] = ed
    for lo, hi in ((12.0, 12.75), (12.75, 13.2), (13.2, 13.58), (13.58, 14.5)):
        q = np.where(hasm & (lgm >= lo) & (lgm < hi))[0]
        if len(q) >= 4: e = est(q); sy = boot(q)[0]; P(f"  gas bin {lo}-{hi}: N {e['n']}, x {e['x']:.3f}, lg Y {e['lgY']:+.3f} +- {sy:.3f}, D_H {e['lgY'] - line(H, e['x']):+.3f}, D_W {e['lgY'] - line(W, e['x']):+.3f}")
# K3 mock, injected line, on real gas, z, weights
def inv_line(L, lg_mg_cat, mc, sc=0.0):
    """Solve true M with aperture: M = 6.2715 Mg_cat (M/Mc)^(g/3) / Y(M), Y on L. Scatter sc in lg gas at fixed M."""
    x = 14.0 + 0 * lg_mg_cat
    for _ in range(60): x = x - .7 * (x - (LG + lg_mg_cat + sc + G / 3 * (x - np.log10(mc)) - (L[0] + L[1] * (x - 14.5))))
    return x
def mock(L, N=500, seed=1, mf=0.0, sg=.10):
    rg = np.random.default_rng(seed); Dout = []; ix = pri
    for _ in range(N):
        sc = rg.normal(0, sg, len(mA)) - mf; lt = inv_line(L, lgm, mcA, sc); Mw = to_wl(10 ** lt, zA); m = Mw + rg.normal(0, s_med[zb]); m[nomass] = np.nan; e = est(ix, m); Dout.append(e["lgY"] - line(L, e["x"]))
    return float(np.mean(Dout)), float(np.std(Dout))
mH = mock(H); mW = mock(W); P("\nK3 mock, injected on real gas, z, weights; mean D, sd"); P(f"  input H: D_H {mH[0]:+.4f} sd {mH[1]:.4f}; input W: D_W {mW[0]:+.4f} sd {mW[1]:.4f}")
# mass-function shift at fixed gas: at fixed lg gas, lnM lower by alpha sigma^2, alpha 1.8, sigma 0.10/(1+b) dex
sg_lnM = .10 / 1.22 * math.log(10); mfsh = 1.8 * sg_lnM ** 2 / math.log(10); mH2 = mock(H, N=300, seed=2, mf=mfsh * 1.22); P(f"  with mass-function selection at fixed gas (alpha 1.8, added detail, not in the criteria by name): shift {mfsh:.4f} dex in M; input H D_H {mH2[0]:+.4f}")
sep_s = .5 * (mH[1] + mW[1]); gap_mock = abs(line(H, 14.25) - line(W, 14.25)); check("K3 injected-line recovery", abs(mH[0]) <= .02 and abs(mW[0]) <= .02 and gap_mock > 2 * sep_s, f"|bias| H {abs(mH[0]):.4f}, W {abs(mW[0]):.4f} <= 0.02; gap {gap_mock:.3f} vs sd {sep_s:.3f}")
Sse = max(abs(mH[0]), abs(mW[0]), abs(mH2[0])); Ssh = .015
St = math.sqrt(sY ** 2 + Sap ** 2 + Sbi ** 2 + Sse ** 2 + Ssh ** 2); DH = e0["lgY"] - line(H, e0["x"]); DW = e0["lgY"] - line(W, e0["x"]); sDH = float(np.std(D_b)); sDW = float(np.std(By - (W[0] + W[1] * (Bx - 14.5)))); StH = math.sqrt(sDH ** 2 + Sap ** 2 + Sbi ** 2 + Sse ** 2 + Ssh ** 2); StW = math.sqrt(sDW ** 2 + Sap ** 2 + Sbi ** 2 + Sse ** 2 + Ssh ** 2)
P(f"\nBudget, dex: bootstrap on lg Y {sY:.3f} (on D_H {sDH:.3f}, D_W {sDW:.3f}), aperture g 0.75-1.35 {Sap:.3f}, half eq. 17 shift {Sbi:.3f}, selection {Sse:.3f}, shear + photo-z {Ssh:.3f}. sigma_tot on lg Y {St:.3f}; on D_H {StH:.3f}, D_W {StW:.3f}. GS4 gas +-0.017 not added.")
P(f"D_H {DH:+.3f} ({DH / StH:+.1f} sigma), D_W {DW:+.3f} ({DW / StW:+.1f} sigma)")
# Akino: from FR2's table only: 14.0 -0.36, 14.5 -0.21
akx = -.36 + (.15 / .5) * (e0["x"] - 14.0); P(f"Akino at x, from FR2's table, interpolated: {akx:+.3f}; D {e0['lgY'] - akx:+.3f}")
hgy = HG["a"] + HG["b"] * (e0["lgMg"] - 13.5); P(f"HG cross-check at the bin's gas {e0['lgMg']:.3f}: {hgy:+.3f}, Y minus it {e0['lgY'] - hgy:+.3f}")
if abs(DH) <= 2 * StH and abs(DW) >= 3 * StW: LAB = "H FAVOURED"
elif abs(DW) <= 2 * StW and abs(DH) >= 3 * StH: LAB = "W FAVOURED"
else: LAB = "UNDECIDED" + (" [BETWEEN]" if abs(DH) >= 2 * StH and abs(DW) >= 2 * StW else "")
RES["primary"] = dict(e0, sY=sY, sX=sX, DH=DH, DW=DW, StH=StH, StW=StW, St=St, Sap=Sap, Sbi=Sbi, Sse=Sse, Ssh=Ssh, label=LAB, raw=e_raw); P(f"LABEL PRIMARY{' MUTATE' if MUT else ''}: {LAB}")
if MUT:
    b = json.load(open(os.path.join(HERE, "fr3_results.json"))) if os.path.exists(os.path.join(HERE, "fr3_results.json")) else None
    if b: P(f"MUTATE (a) lg Y at x {e0['x']:.3f}: D_H {DH:+.3f} against the gas-binned {b['primary']['DH']:+.3f}; shift {DH - b['primary']['DH']:+.3f}: {'BITES' if abs(DH - b['primary']['DH']) > .02 else 'DOES NOT BITE'}")
    open(os.path.join(HERE, "fr3_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit()
# Line R
def Mhat(a, b, mg, mc):
    x = np.full(len(mg), 14.2); lg = np.log10(mg); lc = np.log10(mc)
    for _ in range(40):
        lgp = lg + G / 3 * (x - lc); x = x - .7 * (x - (LG + lgp - (a + b * (lgp - 13.5))))
    return x
def fitR(ix):
    def f(p): lt = Mhat(p[0], p[1], ALL[ix], mcA[ix]); r = mA[ix] - to_wl(10 ** lt, zA[ix]); return float(np.sum(wA[ix] * (r / 1e14) ** 2))
    q = minimize(f, [-.3, .2], method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-6, maxiter=400)); return q.x
fitix = np.where(hasm)[0]; a_, b_ = fitR(fitix); rg = np.random.default_rng(SEED); Bp = np.array([fitR(rg.choice(fitix, len(fitix))) for _ in range(NB // 4)]); sa_, sb_ = Bp.std(0); P(f"\nLine R fit on {len(fitix)} clusters, lg Y = a + b (lg Mg - 13.5): a {a_:+.3f} +- {sa_:.3f}, b {b_:+.3f} +- {sb_:.3f} (500 bootstraps)")
lt = Mhat(a_, b_, ALL[fitix], mcA[fitix]); n143 = int(np.sum(lt < 14.3)); P(f"  eligible with M-hat lg M500 < 14.3: {n143}")
def mapM(a, b): return dict(mode="line", x="M", a=(a + .2027 * b) / (1 - b), b=b / (1 - b), piv=14.5)
Ra = e0["lgY"]; bG = HG["b"]; a_anc = e0["lgY"] - bG * (e0["lgMg"] - 13.5); LR_fit = mapM(a_, b_); LR_anc = mapM(a_anc, bG); useF = sb_ <= .10
P(f"  anchored: a {a_anc:+.3f}, b {bG:+.4f}; in lg M: fit a {LR_fit['a']:+.3f}, b {LR_fit['b']:+.3f}; anchored a {LR_anc['a']:+.3f}, b {LR_anc['b']:+.3f}. Label row: {'fit' if useF else 'anchored'} (SE b {sb_:.3f})")
RES["R"] = dict(fit=LR_fit, anchored=LR_anc, use="fit" if useF else "anchored", a=a_, b=b_, sa=sa_, sb=sb_, a_anc=a_anc, n143=n143, St=St)
# Umetsu x E16
U = FP.tsv(os.path.join(HERE, "data", "umetsu20_table2.tsv"))["J/ApJ/890/148/table2"]; check("K2d Umetsu rows 136", len(U) == 136, len(U)); X = {int(r["XLSSC"]): r for r in list(FP.tsv(os.path.join(REPO, "_external_data", "gs4", "xxl100", "xxl100gc.tsv")).values())[0]}
Ur = []
for r in U:
    x = X.get(int(r["XLSSC"]))
    if x is None: continue
    z = FP.fl(r["z"]); mg = FP.fl(x["Mgas500"]) * 1e13; R = FP.fl(x["r500MT"]) * 1e3; mu = FP.fl(r["M500"]) * 1e14; su = FP.fl(r["e_M500"]) * 1e14
    if z <= .5 and mg > 0 and R > 0 and np.isfinite(mu): Ur.append(dict(z=z, mg=mg, m_e=M_R(R, z), m=mu, s=su, mt=FP.fl(r["M500MT"]) * 1e14))
zu = np.array([u["z"] for u in Ur]); mu = np.array([u["m"] for u in Ur]); me = np.array([u["m_e"] for u in Ur]); gu = np.array([u["mg"] for u in Ur]); su = np.array([u["s"] for u in Ur]); mtu = np.array([u["mt"] for u in Ur]); zbu = np.clip(np.digitize(zu, ZB) - 1, 0, 2); smu = np.array([np.median(su[zbu == k]) for k in range(3)]); wu = 1 / smu[zbu] ** 2
def U_est(ix, m): w = wu[ix] * np.isfinite(m[ix]); mm = np.nan_to_num(m[ix]); mb = (w * mm).sum() / w.sum(); mcb = (w * me[ix]).sum() / w.sum(); g = (w * gu[ix]).sum() / w.sum(); d = math.log10(mb / mcb) / 3; g2 = g * 10 ** (G * d); return math.log10(mb), math.log10(6.2715 * g2 / mb), d, math.log10(mb / mcb)
ui = np.where((np.log10(gu) >= BIN[0]) & (np.log10(gu) < BIN[1]))[0]; x_, y_, d_, rr = U_est(ui, mu); rg = np.random.default_rng(SEED); By_u = []
for _ in range(NB): j = rg.choice(ui, len(ui)); q = U_est(j, mu); By_u.append((q[0], q[1], q[3]))
By_u = np.array(By_u); sU = By_u[:, 1].std(); yE = lambda x: WXXL["a"] + WXXL["b"] * (x - 14.5); sapU = abs(d_) * .3; stU = math.sqrt(sU ** 2 + sapU ** 2 + (.021 * (1)) ** 2); dE = y_ - yE(x_); dHu = y_ - line(H, x_); sXXL = se = WXXL["sa"]; stU2 = math.sqrt(stU ** 2 + sXXL ** 2)
P(f"\nUmetsu x E16, z <= 0.5, gas bin: N {len(ui)} of {len(Ur)} joined. raw M500 mean x {x_:.3f} (h 0.7), lg Y {y_:+.3f} +- {sU:.3f}, sigma_tot {stU:.3f} (aperture {sapU:.3f}, 5 % mass). FR1's XXL alone there {yE(x_):+.3f} (+-{sXXL:.3f}), H {line(H, x_):+.3f}, W {line(W, x_):+.3f}. D_XXL {dE:+.3f} ({dE / stU2:+.1f}), D_H {dHu:+.3f} ({dHu / stU:+.1f}), D_W {y_ - line(W, x_):+.3f} ({(y_ - line(W, x_)) / stU:+.1f})")
xmt, ymt, _, rmt = U_est(ui, mtu); P(f"  M500MT row (T-based, HSC calibrated): x {xmt:.3f}, lg Y {ymt:+.3f}, D_XXL {ymt - yE(xmt):+.3f}, D_H {ymt - line(H, xmt):+.3f}")
P(f"  lg <M500 Umetsu> / <M from E16 r500MT> on same clusters: {rr:+.3f} +- {By_u[:, 2].std():.3f}; MT {rmt:+.3f}")
Ulab = "W ANCHOR HOLDS" if abs(dE) <= 2 * stU2 and abs(dHu) >= 3 * stU else ("W ANCHOR FAILS" if dE >= 3 * stU2 and abs(dHu) <= 2 * stU else "UNSETTLED"); P(f"  LABEL UMETSU: {Ulab}"); RES["umetsu"] = dict(N=len(ui), x=x_, y=y_, s=stU, dE=dE, dH=dHu, ratio=rr, xmt=xmt, ymt=ymt, label=Ulab)
# HIFLUGCS
HF = FP.tsv(os.path.join(HERE, "data", "hiflugcs.tsv")); b2 = HF["J/MNRAS/469/3738/tableb2"]; b3 = {r["Name"]: r for r in HF["J/MNRAS/469/3738/tableb3"]}; check("K2e HIFLUGCS rows 64", len(b2) == 64 and len(b3) == 64, len(b2))
def sx(s): a = [float(v) for v in s.replace("+", "").split()]; sg = -1 if s.strip().startswith("-") else 1; return sg * (abs(a[0]) + a[1] / 60 + a[2] / 3600)
GS = list(csv.DictReader(open(os.path.join(RB, "GS4_pointed_gas_offset", "gs4_inputs.csv"))))
HR = []; nX = 0
for r in b2:
    ra = 15 * sx(r["RAJ2000"]); de = sx(r["DEJ2000"]); z = FP.fl(r["z"])
    if isx(ra, de, z): nX += 1; continue
    t = b3[r["Name"]]; M = {k: FP.fl(t[k]) * 1e14 for k in ("M500NFWFreeze", "M500kTextrp", "M500NFWHudson", "M500NFWAll")}
    d = sep(ra, de, eRA, eDE) * 60; j = np.where((d <= 6) & (np.abs(eZ - z) <= .02) & (eMg > 0))[0]; rec = dict(name=r["Name"], z=z, M=M)
    if len(j): i = j[np.argmin(d[j])]; rec.update(mge=eMg[i], mce=eM[i])
    pg = []
    for q in GS:
        if q["cat"] == "E16" or q["Mgas"] in ("", "nan") or q["R500"] in ("", "nan"): continue
        if abs(float(q["ra"]) - ra) > 1 or abs(float(q["z"]) - z) > .02: continue
        if sep(ra, de, float(q["ra"]), float(q["dec"])) * 60 <= 6:
            hh = float(q["h"]); m0 = M_R(float(q["R500"]) * hh / .7, z); pg.append(math.log10(float(q["Mgas"])) + 2.5 * math.log10(hh / .7) + G / 3 * (math.log10(M["M500NFWFreeze"]) - math.log10(m0)))
    if pg: rec["lgp"] = float(np.median(pg))
    HR.append(rec)
P(f"\nHIFLUGCS: X-COP removed {nX}; with eRASS1 gas {sum('mge' in r for r in HR)}; with pointed gas {sum('lgp' in r for r in HR)}")
def ols(x, y): rg = np.random.default_rng(SEED); x = np.array(x); y = np.array(y); b, a = np.polyfit(x - 14.5, y, 1); n = len(x); B = np.array([np.polyfit(x[i] - 14.5, y[i], 1) for i in rg.integers(0, n, (NB, n))]); return a, b, B[:, 1].std(), B[:, 0].std(), n, x.min(), x.max(), float(np.std(y - a - b * (x - 14.5))), a + b * (14.34 - 14.5), float(np.std(B[:, 1] + B[:, 0] * (14.34 - 14.5)))
def hrow(k, src):
    X = []; Y = []
    for r in HR:
        m = r["M"][k]
        if not m > 0: continue
        if src == "e" and "mge" in r: g2 = r["mge"] * (m / r["mce"]) ** (G / 3)
        elif src == "p" and "lgp" in r: g2 = 10 ** r["lgp"]
        else: continue
        X.append(math.log10(m)); Y.append(math.log10(6.2715 * g2 / m))
    return ols(X, Y)
Rh = {}
for k in ("M500NFWFreeze", "M500kTextrp", "M500NFWHudson", "M500NFWAll"):
    for s_ in ("e", "p"):
        a, b, sa, sb, n, lo, hi, rm, y34, s34 = hrow(k, s_); Rh[(k, s_)] = (a, b, sa, sb, n); P(f"  {k}, gas {'eRASS1' if s_ == 'e' else 'pointed'}: N {n}, lg M {lo:.2f}-{hi:.2f}, a {a:+.3f} +- {sa:.3f}, b {b:+.3f} +- {sb:.3f}, rms {rm:.3f}, Y at 14.34 {y34:+.3f} +- {s34:.3f} (H {line(H, 14.34):+.3f}, W {line(W, 14.34):+.3f})")
a, b, sa, sb, n = Rh[("M500NFWFreeze", "e")]; HLab = "NOT MEASURED" if sb > .08 else ("NO STEP NEEDED" if abs(b - .219) <= 2 * sb else ("STEP" if b + 2 * sb < .219 else "NOT MEASURED")); P(f"  LABEL HIFLUGCS: {HLab}; reading on eRASS1 gas, NFWFreeze: b {b:+.3f} +- {sb:.3f}"); RES["hiflugcs"] = dict(b=b, sb=sb, n=n, a=a, label=HLab, pointed=Rh[("M500NFWFreeze", "p")])
Ch = list(FP.tsv(os.path.join(HERE, "data", "chiu22.tsv")).values())[0]; check("K2f Chiu rows 457", len(Ch) == 457, len(Ch))  # eFEDS row itself: fr3_diag.py, report only
RES["checks"] = CK
json.dump(RES, open(os.path.join(HERE, "fr3_results.json"), "w"), indent=0, default=float); open(os.path.join(HERE, "fr3.out"), "w").write("\n".join(OUT) + "\n")
