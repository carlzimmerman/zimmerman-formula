#!/usr/bin/env python3
"""CFG238 main: re-derive the pinned numbers of CFG224 and CFG224b (frozen criteria sections 2 and 4) and run controls C1-C5, C8, C9.
Pass lines are scored against README numbers only (scripts/json of CFG224 are not read in this script). Exit 0."""
import sys
from CFG238_common import *

outp, jp = out_paths("CFG238_main")
T = Tee(outp)
banner(T, "CFG238 main (CFG224 + CFG224b pinned numbers; controls)")
R = {}
LINES = []


def chk(lid, desc, mine, target, tol, nd=3):
    ok = (mine is not None) and abs(mine - target) <= tol + 1e-12
    LINES.append((lid, ok))
    T(f"  [{'PASS' if ok else 'MISS'}] {lid} {desc}: mine {mine if mine is None else round(mine, nd + 1)} README {target} (tol {tol})")
    return ok


def chkN(lid, desc, mine, target):
    ok = mine == target
    LINES.append((lid, ok))
    T(f"  [{'PASS' if ok else 'MISS'}] {lid} {desc}: mine {mine} README {target}")
    return ok


# ======================================================================= CFG224 (README A)
T("\n== A. CFG224 pair offsets")
d, S = s82_d()
st = msd(d)
K = Kfun(st["mean"], st["se"])
sig2 = [(r["logMgas_CO_errlo"] ** 2 + r["logMgas_dust_errlo"] ** 2) for r in S if r["logMgas_CO"] is not None and r["logMgas_dust"] is not None]
sint = math.sqrt(max(0, st["sd"] ** 2 - np.mean(sig2)))
T(f"Stripe82 CO-dust: N {st['N']} mean {st['mean']:.4f} SD {st['sd']:.4f} SE {st['se']:.4f} median {st['median']:.4f} 1.4826MAD {st['mad']:.4f} intrinsic SD {sint:.4f} K {K:.4f} [{Kclass(K)}]; boot68 {boot_mean_ci(d)}")
R["s82"] = dict(st, K=K, sint=sint)
chkN("H-A1a", "Stripe82 N", st["N"], 78)
chk("H-A2a", "S82 mean", st["mean"], -0.068, 0.01)
chk("H-A2b", "S82 SD", st["sd"], 0.155, 0.01)
chk("H-A2c", "S82 SE", st["se"], 0.018, 0.01)
chk("H-A2d", "S82 K", K, 0.038, 0.01)
chk("H-A2e", "S82 intrinsic SD", sint, 0.134, 0.01)

B = load_bourne()
dB = np.array([r["logCI"] - r["logDust"] for r in B])
sB = msd(dB)
KB = Kfun(sB["mean"], sB["se"])
T(f"Bourne [CI]-dust: N {sB['N']} mean {sB['mean']:.4f} SD {sB['sd']:.4f} SE {sB['se']:.4f} K {KB:.4f}; boot68 {boot_mean_ci(dB)}")
NO = load_noema()
ok5 = [r for r in NO if r["ok"] == 1]
ko5 = [r for r in NO if r["ok"] == 0]
P5 = noema_pairs(ok5)
cd = np.array([p["CO_dust"] for p in P5]); cc = np.array([p["CO_CI"] for p in P5]); idu = np.array([p["CI_dust"] for p in P5])
sN = {k: msd(v) for k, v in (("CO_dust", cd), ("CO_CI", cc), ("CI_dust", idu))}
for k, v in sN.items():
    T(f"NOEMA3D validated {k}: N {v['N']} mean {v['mean']:.4f} SD {v['sd']:.4f} SE {v['se']:.4f} K {Kfun(v['mean'], v['se']):.4f}")
chkN("H-A1b", "Bourne N", sB["N"], 9)
chkN("H-A1c", "NOEMA3D validated N", len(ok5), 5)
chk("H-A3a", "Bourne mean", sB["mean"], -0.294, 0.01)
chk("H-A3b", "Bourne SE", sB["se"], 0.059, 0.01)
chk("H-A3c", "Bourne K", KB, 0.158, 0.01)
chk("H-A3d", "NOEMA3D [CI]-dust mean", sN["CI_dust"]["mean"], -0.142, 0.01)
chk("H-A3e", "NOEMA3D [CI]-dust SE", sN["CI_dust"]["se"], 0.041, 0.01)
chk("H-A3f", "NOEMA3D [CI]-dust K", Kfun(sN["CI_dust"]["mean"], sN["CI_dust"]["se"]), 0.082, 0.01)
pool = np.concatenate([dB, idu])
sP = msd(pool)
KP = Kfun(sP["mean"], sP["se"])
T(f"pooled [CI]-dust: N {sP['N']} mean {sP['mean']:.4f} SD {sP['sd']:.4f} SE {sP['se']:.4f} K {KP:.4f} [{Kclass(KP)}]")
R["pooled"] = dict(sP, K=KP)
chkN("H-A3g", "pooled N", sP["N"], 14)
chk("H-A3h", "pooled mean", sP["mean"], -0.240, 0.01)
chk("H-A3i", "pooled SD", sP["sd"], 0.166, 0.01)
chk("H-A3j", "pooled SE", sP["se"], 0.044, 0.01)
chk("H-A3k", "pooled K", KP, 0.128, 0.01)
chk("H-A4a", "NOEMA3D CO-dust mean", sN["CO_dust"]["mean"], -0.017, 0.01)
chk("H-A4b", "NOEMA3D CO-dust SE", sN["CO_dust"]["se"], 0.060, 0.01)
chk("H-A4c", "NOEMA3D CO-dust K", Kfun(sN["CO_dust"]["mean"], sN["CO_dust"]["se"]), 0.061, 0.01)
chk("H-A4d", "NOEMA3D CO-CI mean", sN["CO_CI"]["mean"], 0.126, 0.01)
chk("H-A4e", "NOEMA3D CO-CI SE", sN["CO_CI"]["se"], 0.030, 0.01)
chk("H-A4f", "NOEMA3D CO-CI K", Kfun(sN["CO_CI"]["mean"], sN["CO_CI"]["se"]), 0.070, 0.01)
hA, hB, hC = hat(cd, cc, idu)  # A=CO, B=dust? see below
# hat with A=CO,B=CI,C=dust: d_AB=CO-CI (cc), d_AC=CO-dust (cd), d_BC=CI-dust (idu)
vCO, vCI, vdust = hat(cc, cd, idu)
T(f"hat variances: CO {vCO:.5f} CI {vCI:.5f} dust {vdust:.5f}; sigma CO {sgn_sqrt(vCO):.4f} CI {sgn_sqrt(vCI):.4f} dust {sgn_sqrt(vdust):.4f}")
R["hat5"] = dict(vCO=vCO, vCI=vCI, vdust=vdust)
chk("H-A4g", "hat sigma_CO", sgn_sqrt(vCO), 0.084, 0.01)
chk("H-A4h", "hat sigma_dust", sgn_sqrt(vdust), 0.105, 0.01)
LINES.append(("H-A4i", vCI < 0)); T(f"  [{'PASS' if vCI < 0 else 'MISS'}] H-A4i sigma_CI^2 negative: {vCI:.5f}")
# failing five sensitivity
for lab, co in (("Table 1 CO", "CO_t1"), ("recipe CO", "CO_rec")):
    v = np.array([r[co] - r["dust"] for r in ko5])
    s = msd(v)
    T(f"NOEMA3D failing five CO-dust ({lab}): N {s['N']} mean {s['mean']:.4f} SD {s['sd']:.4f} K {Kfun(s['mean'], s['se']):.4f}")
    R["fail5_" + co] = dict(s, K=Kfun(s["mean"], s["se"]))
chk("H-A4j", "fail5 CO-dust Table1 mean", R["fail5_CO_t1"]["mean"], -0.235, 0.01)
chk("H-A4k", "fail5 CO-dust recipe mean", R["fail5_CO_rec"]["mean"], -0.008, 0.01)
# singles
T("singles (stated masses, own conversions):")
pks = dict(CI=3.1e11, CO=0.73e11, dust=2.2e11); md = dict(CO=1.7e11, dust=7e10); jj = dict(CO=8.8e10, dust=5.7e10, CII=9.8e10)
sing = dict(pks_CO_CI=math.log10(pks["CO"] / pks["CI"]), pks_CO_dust=math.log10(pks["CO"] / pks["dust"]), pks_CI_dust=math.log10(pks["CI"] / pks["dust"]),
            md94_CO_dust=math.log10(md["CO"] / md["dust"]), j_CO_CII=math.log10(jj["CO"] / jj["CII"]), j_CO_dust=math.log10(jj["CO"] / jj["dust"]),
            j_CII_dust=math.log10(jj["CII"] / jj["dust"]), d49_CI_dust_bound=11.22 - 11.19)
for k, v in sing.items():
    T(f"  {k} {v:+.3f}")
R["singles"] = sing
for k, tg in (("pks_CO_CI", -0.63), ("pks_CO_dust", -0.48), ("pks_CI_dust", 0.15), ("md94_CO_dust", 0.39), ("j_CO_CII", -0.05), ("j_CO_dust", 0.19), ("j_CII_dust", 0.24)):
    chk("H-A6:" + k, k, sing[k], tg, 0.01)
# SMGs
sm = readcsv(os.path.join(MT, "smg_CI_CO_3mm_arxiv2404.05596.csv"))
rr, jup, al = [], [], []
for r in sm:
    a, b, m, j = fl(r["LpCI_1e10"]), fl(r["LpCO10_1e10"]), fl(r["Mgas_CI_1e10"]), fl(r["Jup"])
    if a and b and m:
        rr.append(math.log10(a / b)); jup.append(j); al.append(m / b)
rr = np.array(rr); jup = np.array(jup); al = np.array(al)
s = msd(rr)
T(f"SMG log L'CI/L'CO(1-0): N {s['N']} mean {s['mean']:.3f} SD {s['sd']:.3f} SE {s['se']:.3f}")
chkN("H-A1d", "SMG N", s["N"], 20)
chk("H-A7a", "SMG mean r", s["mean"], -0.70, 0.01); chk("H-A7b", "SMG SD r", s["sd"], 0.29, 0.01); chk("H-A7c", "SMG SE r", s["se"], 0.064, 0.01)
byJ = {}
for jv, tg, nn in ((3, -0.89, 6), (4, -0.52, 11), (5, -0.94, 3)):
    m = jup == jv
    byJ[jv] = (int(m.sum()), float(rr[m].mean()) if m.sum() else None)
    T(f"  Jup={jv}: N {m.sum()} mean {rr[m].mean():.3f}")
    chkN(f"H-A7d:J{jv}N", f"N Jup={jv}", int(m.sum()), nn); chk(f"H-A7d:J{jv}", f"mean Jup={jv}", float(rr[m].mean()), tg, 0.01)
la = np.log10(al)
T(f"implied alpha_CO: median {np.median(al):.3f} SD(log) {la.std(ddof=1):.3f}")
chk("H-A7e", "implied alpha median", float(np.median(al)), 0.91, 0.01); chk("H-A7f", "implied alpha SD log", float(la.std(ddof=1)), 0.29, 0.01)
for a0, tg in ((0.8, -0.008), (3.6, 0.645), (4.36, 0.729)):
    v = np.log10(a0 / al)
    T(f"  offset alpha_assumed {a0}: mean {v.mean():.3f} SD {v.std(ddof=1):.3f}")
    chk(f"H-A7g:{a0}", f"SMG offset at {a0}", float(v.mean()), tg, 0.01)
# SPT
sp = readcsv(os.path.join(MT, "spt_dsfg_CI_CO_CII_fluxes_arxiv2306.03153.csv"))
r21, rcii = [], []
for r in sp:
    a, b, c = fl(r["CI10_Jykms"]), fl(r["CI21_Jykms"]), fl(r["CII_Jykms"])
    if a and b:
        r21.append(math.log10((b / a) * (492.1607 / 809.3446) ** 2))
    if a and c:
        rcii.append(math.log10((c / a) * (492.1607 / 1900.5369) ** 2))
T(f"SPT [CI]2-1/1-0: N {len(r21)} mean {np.mean(r21):.3f} SD {np.std(r21, ddof=1):.3f}; [CII]/[CI]1-0: N {len(rcii)} mean {np.mean(rcii):.3f} SD {np.std(rcii, ddof=1):.3f}")
chkN("H-A1e", "SPT rows with flux table", len(sp), 29)
chk("H-A7h", "SPT CI21/CI10 mean", float(np.mean(r21)), -0.21, 0.01); chk("H-A7i", "SPT CI21/CI10 SD", float(np.std(r21, ddof=1)), 0.21, 0.01)
chk("H-A7j", "SPT CII/CI mean", float(np.mean(rcii)), 0.27, 0.01); chk("H-A7k", "SPT CII/CI SD", float(np.std(rcii, ddof=1)), 0.42, 0.01)
chkN("H-A7l", "SPT N CI21/CI10", len(r21), 20); chkN("H-A7m", "SPT N CII/CI", len(rcii), 10)
kp = readcsv(os.path.join(MT, "kirkpatrick2019_z2_CO_dust.csv"))
kk = [math.log10(fl(r["Mmol_CO_1e11"]) / fl(r["Mmol_RJ_1e11"])) for r in kp if fl(r["Mmol_CO_1e11"]) and fl(r["Mmol_RJ_1e11"])]
T(f"Kirkpatrick (beside, not independent): N {len(kk)} mean {np.mean(kk):.3f} SD {np.std(kk, ddof=1):.3f}")
chkN("H-A1f", "Kirkpatrick rows", len(kp), 12)
chk("H-A7n", "Kirkpatrick mean", float(np.mean(kk)), -0.069, 0.01); chk("H-A7o", "Kirkpatrick SD", float(np.std(kk, ddof=1)), 0.152, 0.01)

# ======================================================================= CFG224b (README B)
T("\n== B. CFG224b joins, bins, drifts, slopes")
JN = {"ad": 318, "dax": 99, "xa": 106, "xd": 137}
for t in TABLES:
    rows, info = joined(t)
    T(f"join {t}: table {info['n_table']} joined {info['n_join']} unmatched {len(info['unmatched'])} ambiguous {len(info['ambiguous'])}")
    chkN(f"H-B1:{t}", f"join {t}", info["n_join"], JN[t])
R["joins"] = {t: joined(t)[1]["n_join"] for t in TABLES}
DR = {("ad", "aCO"): {"B2": (-0.101, 0.028), "B3": (-0.090, 0.022), "B4": (-0.058, 0.033)},
      ("dax", "aCO"): {"B4": (0.064, 0.043)}, ("xa", "aCO"): {"B4": (0.104, 0.041)},
      ("dax", "XCI"): {"B4": (0.135, 0.040)}, ("xa", "XCI"): {"B4": (0.094, None)}, ("xd", "XCI"): {"B4": (0.051, None)},
      ("ad", "kappaH"): {"B2": (0.084, None), "B3": (0.085, None), "B4": (0.060, None)},
      ("dax", "GDR"): {"B2": (0.146, None), "B3": (0.170, None), "B4": (0.091, None)},
      ("xd", "GDR"): {"B2": (0.070, None), "B3": (0.128, None), "B4": (0.072, None)}}
SW = {("ad", "aCO"): (0.056, 0.050), ("dax", "aCO"): (0.004, 0.072), ("xa", "aCO"): (-0.002, 0.066), ("dax", "XCI"): (-0.039, 0.080),
      ("xa", "XCI"): (-0.026, 0.064), ("xd", "XCI"): (-0.104, 0.066), ("ad", "kappaH"): (-0.056, 0.042), ("dax", "GDR"): (-0.025, 0.078), ("xd", "GDR"): (-0.084, 0.066)}
SO = {("ad", "aCO"): (-0.124, 0.032), ("ad", "kappaH"): (0.117, 0.028), ("dax", "XCI"): (0.181, 0.043), ("dax", "GDR"): (0.216, 0.052)}
R["bins"] = {}; R["slopes_with"] = {}; R["slopes_without"] = {}
for combo in COMBOS:
    t, c = combo
    A = factor_arrays(t, c)
    bs = bin_stats(A)
    dr = drifts(bs)
    key = f"{t}:{c}"
    R["bins"][key] = dict(bins=bs, drifts=dr)
    T(f"\n{key} ({FACTORS[combo]}): N={len(A['y'])}")
    for b in ("B1", "B2", "B3", "B4"):
        if b in bs:
            T(f"  {b}: N {bs[b]['N']} mean log10 {bs[b]['mean']:.3f} SD {bs[b]['sd']:.3f} SE {bs[b]['se']:.3f}")
    for b, v in dr.items():
        T(f"  drift {b}: {v['drift']:+.3f} +- {v['se_drift']:.3f}  K_direct {v['K_direct']:.3f} ({Kclass(v['K_direct'])}) K_local {v['K_local']:.3f} ({Kclass(v['K_local'])})")
    for b, (tg, tse) in DR.get(combo, {}).items():
        if b in dr:
            chk(f"H-B2:{key}:{b}", "drift", dr[b]["drift"], tg, 0.01)
            if tse:
                chk(f"H-B2:{key}:{b}se", "drift SE", dr[b]["se_drift"], tse, 0.01)
    if combo == ("ad", "aCO"):
        for b, nn, mm in (("B1", 196, 0.528), ("B2", 16, 0.427), ("B3", 74, 0.438), ("B4", 32, 0.470)):
            chkN(f"H-B2:ad:N{b}", f"N {b}", bs[b]["N"], nn); chk(f"H-B2:ad:mean{b}", f"mean {b}", bs[b]["mean"], mm, 0.01)
        for b, kd, kl in (("B3", 0.021, 0.093), ("B4", 0.032, 0.067), ("B2", None, 0.105)):
            if kd:
                chk(f"H-B2:ad:Kd{b}", "K_direct", dr[b]["K_direct"], kd, 0.01)
            chk(f"H-B2:ad:Kl{b}", "K_local", dr[b]["K_local"], kl, 0.01)
    if len(A["y"]) >= 30:
        for seed in (238, 239):
            w = slope_fit(A, True, 10000, seed)
            if seed == 238:
                R["slopes_with"][key] = w
                T(f"  slope WITH L_IR (seed 238): N {w['N']} b {w['b']:+.3f} boot SD {w['b_boot_sd']:.3f} [{w['b_lo']:+.3f},{w['b_hi']:+.3f}] ols SE {w['b_se_ols']:.3f}; c {w['c']:+.3f} +- {w['c_boot_sd']:.3f}")
            else:
                T(f"    seed 239: b {w['b']:+.3f} SD {w['b_boot_sd']:.3f} [{w['b_lo']:+.3f},{w['b_hi']:+.3f}]")
                R["slopes_with"][key]["seed239"] = dict(lo=w["b_lo"], hi=w["b_hi"], sd=w["b_boot_sd"])
        w = R["slopes_with"][key]
        tb, tsd = SW[combo]
        ok_b = abs(w["b"] - tb) <= 0.03
        ok_sd = abs(w["b_boot_sd"] - tsd) <= 0.02
        ok_e = abs(w["b_lo"] - (tb - 1.96 * tsd)) <= 0.03 and abs(w["b_hi"] - (tb + 1.96 * tsd)) <= 0.03
        for nm_, ok_ in (("b", ok_b), ("sd", ok_sd), ("edges", ok_e)):
            LINES.append((f"H-B3:{key}:{nm_}", ok_))
        T(f"  [{'PASS' if ok_b else 'MISS'}] H-B3 {key} b {w['b']:+.3f} vs {tb:+.3f}; SD {w['b_boot_sd']:.3f} vs {tsd} [{'PASS' if ok_sd else 'MISS'}]; edges mine [{w['b_lo']:+.3f},{w['b_hi']:+.3f}] vs derived [{tb - 1.96 * tsd:+.3f},{tb + 1.96 * tsd:+.3f}] [{'PASS' if ok_e else 'MISS'}]")
        wo = slope_fit(A, False, 10000, 238)
        R["slopes_without"][key] = wo
        nsig = wo["b"] / wo["b_boot_sd"]
        T(f"  slope WITHOUT L_IR: b {wo['b']:+.3f} boot SD {wo['b_boot_sd']:.3f} ({nsig:+.1f} sigma)")
        if combo in SO:
            tb, tsd = SO[combo]
            LINES.append((f"H-B4:{key}", abs(wo["b"] - tb) <= 0.03 and abs(nsig) >= 2))
            T(f"  [{'PASS' if abs(wo['b'] - tb) <= 0.03 and abs(nsig) >= 2 else 'MISS'}] H-B4 {key}: b {wo['b']:+.3f} vs {tb:+.3f}, |sigma| {abs(nsig):.1f} >= 2; SD {wo['b_boot_sd']:.3f} vs {tsd}")
        if combo == ("ad", "aCO"):
            chk("H-B5", "L_IR coefficient alpha_CO ad", w["c"], -0.058, 0.01)
            chk("H-B5sd", "L_IR coeff SD", w["c_boot_sd"], 0.012, 0.01)

# ======================================================================= ACE (frozen per-galaxy definition)
T("\n== C. ACE offset to Stripe82 (peer's frozen definition)")
AC = [r for r in load_ace() if r["both"]]
Rg = np.array([r["logMdust"] - math.log10(r["Mmol"] * 1e10) for r in AC])
ZA = np.array([r["OH"] for r in AC])
chkN("H-B1:ACE", "ACE both-detected N", len(AC), 15)
sR = msd(Rg)
T(f"ACE R: N {sR['N']} mean {sR['mean']:.3f} SD {sR['sd']:.3f}; mean 12+logOH {ZA.mean():.3f} ({ZA.min():.2f}-{ZA.max():.2f})")
chk("H-B6a", "ACE R mean", sR["mean"], -2.37, 0.01); chk("H-B6b", "ACE R SD", sR["sd"], 0.18, 0.01)
Rs = np.array([r["logMdust"] - r["logMgas_CO"] for r in S if r["logMdust"] is not None and r["logMgas_CO"] is not None])
Zs = np.array([r["Z_12logOH"] for r in S if r["logMdust"] is not None and r["logMgas_CO"] is not None])
Xs = np.column_stack([np.ones_like(Zs), Zs])
bet, bse, rsd = ols(Xs, Rs)
bo = ols_boot(Xs, Rs, 10000, 238)
T(f"S82 OLS R = a + b Z: a {bet[0]:.3f} b {bet[1]:+.3f} +- {bo[:, 1].std(ddof=1):.3f} (analytic {bse[1]:.3f}) residual SD {rsd:.3f}; N {len(Rs)}; Z range {Zs.min():.2f}-{Zs.max():.2f}, mean {Zs.mean():.3f}")
chk("H-B7a", "S82 OLS slope", bet[1], -0.49, 0.03); chk("H-B7b", "S82 OLS slope SD", float(bo[:, 1].std(ddof=1)), 0.33, 0.03)
dev = Rg - (bet[0] + bet[1] * ZA)
D_ols = dev.mean()
D_0 = Rg.mean() - Rs.mean()
D_p1 = (Rg - (Rs.mean() + 1.0 * (ZA - Zs.mean()))).mean()
for nm_, Dv, tg in (("OLS", D_ols, -0.67), ("slope 0", D_0, -0.52), ("slope +1", D_p1, -0.21)):
    seA = Rg.std(ddof=1) / math.sqrt(len(Rg))
    sev = math.sqrt(seA ** 2 + (rsd / math.sqrt(len(Rs))) ** 2)
    T(f"  offset {nm_}: {Dv:+.3f}  K(SE ACE only) {Kfun(Dv, seA):.3f}  K(SE incl S82 residual) {Kfun(Dv, sev):.3f}")
    chk(f"H-B6:{nm_}", f"offset {nm_} (sign: ACE below)", Dv, tg, 0.01)
R["ace"] = dict(R_mean=sR["mean"], R_sd=sR["sd"], S82_slope=bet[1], S82_a=bet[0], D_ols=D_ols, D_0=D_0, D_p1=D_p1)
chk("H-B6:K_ols", "K OLS", Kfun(D_ols, Rg.std(ddof=1) / math.sqrt(15)), 0.34, 0.01)
chk("H-B6:K_0", "K slope 0", Kfun(D_0, Rg.std(ddof=1) / math.sqrt(15)), 0.26, 0.01)
chk("H-B6:K_p1", "K slope +1", Kfun(D_p1, Rg.std(ddof=1) / math.sqrt(15)), 0.11, 0.01)

# ======================================================================= controls
T("\n== D. Controls")
CT = []


def ctl(name, ok, msg):
    CT.append((name, ok))
    T(f"[{'PASS' if ok else 'FAIL'}] {name} {msg}")


ctl("C1", all(ok for lid, ok in LINES if lid.startswith(("H-A1", "H-B1"))), "counts (H-A1*, H-B1*) all equal")
rng = np.random.default_rng(2381)
d0 = rng.normal(0.10, 0.15, 500)
s0 = msd(d0)
lo, hi = boot_mean_ci(d0, 10000, 238)
ctl("C2", abs(s0["mean"] - 0.10) < 3 * s0["se"] and abs(s0["sd"] - 0.15) < 3 * 0.15 / math.sqrt(2 * 499) and abs((hi - lo) / 2 - s0["se"]) < 0.1 * s0["se"],
    f"estimator identity: mean {s0['mean']:.4f} SD {s0['sd']:.4f} SE {s0['se']:.4f} boot half-width {(hi - lo) / 2:.4f}")
covs = {}
for N in (9, 14, 40, 78):
    rng = np.random.default_rng(2381 + N)
    Kmock, Bb = 2000, 1000
    hit = 0
    mu_true = 0.0
    for ch in range(20):
        dd = rng.normal(mu_true, 0.15, (100, N))
        idx = rng.integers(0, N, (100, Bb, N))
        bm = np.take_along_axis(dd[:, None, :].repeat(Bb, 1), idx, 2).mean(2)
        l16, l84 = np.percentile(bm, 16, 1), np.percentile(bm, 84, 1)
        hit += int(((l16 <= mu_true) & (mu_true <= l84)).sum())
    covs[N] = hit / Kmock
ctl("C3", all(0.60 <= v <= 0.76 for v in covs.values()), f"bootstrap 68% coverage {covs} (K=2000 mocks, B=1000)")
Ad = factor_arrays("ad", "aCO")
mk = np.isfinite(Ad["L"])
Ad = {k: (v[mk] if isinstance(v, np.ndarray) else v) for k, v in Ad.items()}
Xd = design(Ad["x"], Ad["L"])
rng = np.random.default_rng(2381)
yt = Xd @ np.array([0.0, 0.30, -0.10]) + rng.normal(0, 0.15, len(Ad["y"]))
bt, _, _ = ols(Xd, yt)
bob = ols_boot(Xd, yt, 4000, 238)
okrec = abs(bt[1] - 0.30) < 3 * bob[:, 1].std() and abs(bt[2] + 0.10) < 3 * bob[:, 2].std()
rng = np.random.default_rng(2381)
Yn = (Xd @ np.array([0.0, 0.0, -0.06]))[:, None] + rng.normal(0, 0.15, (len(Ad["y"]), 2000))
XtXi = np.linalg.inv(Xd.T @ Xd)
Bn = np.linalg.lstsq(Xd, Yn, rcond=None)[0]
res = Yn - Xd @ Bn
s2 = (res ** 2).sum(0) / (len(Ad["y"]) - 3)
z_ = Bn[1] / np.sqrt(s2 * XtXi[1, 1])
frac = float((np.abs(z_) < 2).mean())
ctl("C4", okrec and frac >= 0.94, f"planted (b,c)=(0.30,-0.10) recovered b {bt[1]:.3f} c {bt[2]:.3f} (boot SD {bob[:, 1].std():.3f}, {bob[:, 2].std():.3f}); null (0,-0.06): |b/SE|<2 in {frac:.3f} of 2000")
rng = np.random.default_rng(2385)
sg = np.array([0.10, 0.15, 0.20]); N = 300
e = rng.normal(0, 1, (N, 3)) * sg
cA, cB, cC = e[:, 0], e[:, 1], e[:, 2]
vA, vB, vC = hat(cA - cB, cA - cC, cB - cC)
rec = np.sqrt([vA, vB, vC])
ctl("C5", bool(np.all(np.abs(rec / sg - 1) < 0.15)), f"hat recovery N=300: {rec.round(3).tolist()} vs {sg.tolist()}")
neg = 0
K5 = 20000
rng = np.random.default_rng(2385)
e = rng.normal(0, 1, (K5, 5, 3)) * 0.10
vv = np.var(e[:, :, 0] - e[:, :, 1], axis=1, ddof=1), np.var(e[:, :, 0] - e[:, :, 2], axis=1, ddof=1), np.var(e[:, :, 1] - e[:, :, 2], axis=1, ddof=1)
sA = (vv[0] + vv[1] - vv[2]) / 2; sB_ = (vv[0] + vv[2] - vv[1]) / 2; sC = (vv[1] + vv[2] - vv[0]) / 2
fneg = float(((sA < 0) | (sB_ < 0) | (sC < 0)).mean())
T(f"[INFO] C5b N=5 mock truth (0.10,0.10,0.10): fraction with at least one negative variance {fneg:.3f}; each {float((sA < 0).mean()):.3f}")
R["C5b_negfrac"] = fneg
acel = load_ace()
nco = sum(1 for r in acel if r["Mmol"] is not None and r["Mmol_flag"].strip() != "<")
ndu = sum(1 for r in acel if r["logMdust"] is not None and r["dust_flag"].strip() != "<")
zr = (min(r["z"] for r in acel), max(r["z"] for r in acel))
d21040 = sum(1 for r in acel if r["Mdust21040"] is not None and r["d21040_flag"].strip() != "<")
T(f"[INFO] C8b dust detections by table: 2609.20926 flags {ndu}; 2609.21040 flags {d21040}")
ctl("C8", len(acel) == 26 and nco == 17 and (ndu == 18) and len(AC) == 15 and abs(zr[0] - 2.086) < 1e-9 and abs(zr[1] - 2.494) < 1e-9,
    f"ACE flags: rows {len(acel)} CO det {nco} dust det {ndu} both {len(AC)} z {zr}")
ctl("C9", all(len(joined(t)[1]["ambiguous"]) == 0 for t in TABLES) and all(len({r['Name'] for r in joined(t)[0]}) == len(joined(t)[0]) for t in TABLES),
    "no ambiguous join, no duplicated name in any table")

npass = sum(1 for _, ok in LINES if ok)
T(f"\nSUMMARY pass lines: {npass} PASS / {len(LINES) - npass} MISS of {len(LINES)}; controls {sum(ok for _, ok in CT)}/{len(CT)} pass")
R["lines"] = LINES; R["controls"] = CT
dump(jp, R)
T.close()
sys.exit(0)
