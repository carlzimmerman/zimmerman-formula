#!/usr/bin/env python3
"""CFG238 attack b: circularity of the optimised conversions (frozen D9-D12 and section 6b). Exit 0."""
import sys
from CFG238_common import *

outp, jp = out_paths("CFG238_b_circular")
T = Tee(outp)
banner(T, "CFG238 attack b (identity, raw-ratio slopes, shuffle control, toy optimiser, per-galaxy errors, cross-table differences)")
R = {}
LINES = []
EDGES = [10.5, 11.0, 11.5, 12.0, 12.5]


def line(lid, ok, msg):
    LINES.append((lid, ok))
    T(f"  [{'PASS' if ok else 'MISS'}] {lid} {msg}")


M, keys = load_master()
Mf = lambda i, k: fl(M[i][k])

# ------------------------------------------------------------------ 1 identity (D10)
T("\n== 1. Identity: is each catalogue mass exactly (factor x luminosity)?  residual = logMH2 - (log factor + log L)")
ident = {}


def report_ident(name, res):
    res = np.asarray(res)
    med = float(np.median(res)); sd = float(res.std(ddof=1)); fr = float((np.abs(res - med) < 0.01).mean())
    ident[name] = dict(N=len(res), median=med, sd=sd, frac_within_0p01=fr)
    T(f"  {name}: N {len(res)} median {med:+.4f} SD {sd:.4f} fraction within 0.01 of the median {fr:.3f}")
    return sd


# ad table (luminosities in the table)
ad = load_opt("ad")
r1, r1J, r1Jm, r2, Jv = [], [], [], [], []
for r in ad:
    a, L, J, mh, l8, a8 = fl(r["aCO"]), fl(r["logLCO"]), fl(r["JCorr"]), fl(r["logMH2"]), fl(r["logL850"]), fl(r["loga850"])
    if None in (a, L, J, mh, l8, a8) or a <= 0:
        continue
    r1.append(mh - (math.log10(a) + L)); r1J.append(mh - (math.log10(a) + L + J)); r1Jm.append(mh - (math.log10(a) + L - J))
    r2.append(mh - (l8 - a8)); Jv.append(J)
sdA = report_ident("ad CO: logMH2 - (log aCO + logLCO)", r1)
report_ident("ad CO with +JCorr (log)", r1J)
report_ident("ad CO with -JCorr (log)", r1Jm)
Jv = np.array(Jv); r1 = np.array(r1)
T(f"  JCorr nonzero rows in ad: {int((Jv != 0).sum())}; residual (no J) on those rows: mean {r1[Jv != 0].mean() if (Jv != 0).any() else float('nan'):+.4f}, SD {r1[Jv != 0].std() if (Jv != 0).sum() > 1 else float('nan'):.4f}; on J=0 rows: SD {r1[Jv == 0].std(ddof=1):.5f}")
sdB = report_ident("ad dust: logMH2 - (logL850 - loga850)", r2)
T(f"  log10(1.36) = {math.log10(1.36):.4f} (the He factor the dust residual is expected to equal if alpha_850 includes He)")
# other tables, via master luminosities; JCorr is the tables' own log line-luminosity correction (CO and CI, not dust)
for t, pairs in (("dax", (("CO", "aCO", False, "logLCO", +1), ("CI", "aCI", True, "logLCI", +1), ("dust", "a850", True, "logL850py", -1))),
                 ("xa", (("CO", "aCO", False, "logLCO", +1), ("CI", "aCI", True, "logLCI", +1))),
                 ("xd", (("CI", "aCI", True, "logLCI", +1), ("dust", "asub", True, "logL850", -1)))):
    rows, _ = joined(t)
    for nm, fc, islog, lc, sgn in pairs:
        for useJ in ((False, True) if sgn > 0 else (False,)):
            res = []
            for r in rows:
                mh, f_ = fl(r["logMH2"]), fl(r[fc])
                Lv = fl(r[lc]) if lc in r else Mf(r["_mi"], lc)
                J = (fl(r["JCorr"]) or 0.0) if useJ else 0.0
                if None in (mh, f_, Lv) or (not islog and f_ <= 0):
                    continue
                fv = f_ if islog else math.log10(f_)
                res.append(mh - (fv + Lv + J) if sgn > 0 else mh - (Lv - fv))
            if len(res) > 3:
                report_ident(f"{t} {nm}: logMH2 - (log {fc} + {lc}{' + JCorr' if useJ else ''})" if sgn > 0 else f"{t} {nm}: logMH2 - ({lc} - log {fc})", res)
R["identity"] = ident
sdAJ = ident["ad CO with +JCorr (log)"]["sd"]
line("H-C7a", sdAJ < 0.01, f"ad CO identity SD with JCorr added (frozen D10 variant) {sdAJ:.5f} < 0.01; without JCorr {sdA:.4f} (fails on the 12 rows with JCorr != 0)")
line("H-C7b", sdB < 0.01, f"ad dust identity SD {sdB:.5f} < 0.01 (constant offset allowed)")

# ------------------------------------------------------------------ 2 raw ratio slopes (D9)
T("\n== 2. Raw luminosity ratios versus z at fixed L_IR (no conversion, no optimisation) and the optimised-factor slopes")
rat = {}
rows, _ = joined("ad")
z, L, Rr, ya, yk, Jj, RrU = [], [], [], [], [], [], []
for r in rows:
    a, l8, lc, a8, J = fl(r["aCO"]), fl(r["logL850"]), fl(r["logLCO"]), fl(r["loga850"]), fl(r["JCorr"])
    Lv = r["_LIRm"] if r["_LIRm"] is not None else r["_LIRo"]
    if None in (a, l8, lc, a8, Lv) or a <= 0:
        continue
    z.append(r["_z"]); L.append(Lv); Rr.append(l8 - lc - (J or 0)); ya.append(math.log10(a)); yk.append(a8); Jj.append(J or 0)
    RrU.append(l8 - lc)
z, L, Rr, ya, yk, Jj, RrU = map(np.array, (z, L, Rr, ya, yk, Jj, RrU))
x = np.log10(1 + z)
sl = {}
wU = slope_fit(dict(x=x, L=L, y=RrU), True, 10000, 238)
T(f"  ad raw log(L850/L'CO) WITHOUT the JCorr line correction: with L_IR b {wU['b']:+.3f} +- {wU['b_boot_sd']:.3f} (the 12 JCorr rows move the slope by {wU['b'] - slope_fit(dict(x=x, L=L, y=Rr), True, 4000, 238)['b']:+.3f})")
rat["ad_uncorrected"] = wU
for nm, yy in (("raw log(L850/L'CO)", Rr), ("log alpha_CO (opt)", ya), ("log alpha_850 (opt)", yk)):
    w = slope_fit(dict(x=x, L=L, y=yy), True, 10000, 238)
    wo = slope_fit(dict(x=x, L=L, y=yy), False, 10000, 238)
    sl[nm] = dict(with_L=w, without_L=wo)
    T(f"  ad {nm}: N {w['N']} with L_IR b {w['b']:+.3f} +- {w['b_boot_sd']:.3f}; without L_IR b {wo['b']:+.3f} +- {wo['b_boot_sd']:.3f}")
sR_, sa_, sk_ = (sl[k]["with_L"]["b"] for k in ("raw log(L850/L'CO)", "log alpha_CO (opt)", "log alpha_850 (opt)"))
T(f"  identity check of slopes: slope(alpha_CO) + slope(alpha_850) = {sa_ + sk_:+.6f} vs slope(raw ratio, line luminosity with JCorr) = {sR_:+.6f} (difference {sa_ + sk_ - sR_:+.2e}; He constant absorbed)")
T(f"  prior share: slope(alpha_CO)/slope(raw) = {sa_ / sR_ if abs(sR_) > 1e-9 else float('nan'):.2f}")
m0 = Jj == 0
w = slope_fit(dict(x=x[m0], L=L[m0], y=Rr[m0]), True, 10000, 238)
T(f"  raw ratio with JCorr == 0 only: N {w['N']} b {w['b']:+.3f} +- {w['b_boot_sd']:.3f}")
rat["ad"] = sl; rat["ad_J0"] = w
# xd table: CI / 850
rows, _ = joined("xd")
z, L, Rc = [], [], []
for r in rows:
    lc, l8 = fl(r["logLCI"]), fl(r["logL850"])
    Lv = r["_LIRm"] if r["_LIRm"] is not None else r["_LIRo"]
    if None in (lc, l8, Lv):
        continue
    z.append(r["_z"]); L.append(Lv); Rc.append(lc + (fl(r["JCorr"]) or 0.0) - l8)
z, L, Rc = map(np.array, (z, L, Rc)); x = np.log10(1 + z)
w = slope_fit(dict(x=x, L=L, y=Rc), True, 10000, 238)
T(f"  xd raw log(L'CI/L850): N {w['N']} with L_IR b {w['b']:+.3f} +- {w['b_boot_sd']:.3f}")
rat["xd_CI_850"] = w
# master ratios with both luminosities
for nm, ka, kb in (("CI/CO", "logLCI", "logLCO"), ("850/CO", "logL850py", "logLCO"), ("850/CI", "logL850py", "logLCI")):
    z, L, yy = [], [], []
    for r in M:
        a, b, Lv, zz = fl(r[ka]), fl(r[kb]), fl(r["logLIR"]), fl(r["z"])
        if None in (a, b, Lv, zz) or (ka == "logLCI" and a <= 0) or (kb == "logLCI" and b <= 0):
            continue
        J = fl(r["JCorr"]) or 0.0
        a = a + (J if ka in ("logLCI", "logLCO") else 0.0); b = b + (J if kb in ("logLCI", "logLCO") else 0.0)
        z.append(zz); L.append(Lv); yy.append(a - b)
    z, L, yy = map(np.array, (z, L, yy)); x = np.log10(1 + z)
    w = slope_fit(dict(x=x, L=L, y=yy), True, 10000, 238)
    wo = slope_fit(dict(x=x, L=L, y=yy), False, 10000, 238)
    T(f"  master raw log({nm}): N {w['N']} with L_IR b {w['b']:+.3f} +- {w['b_boot_sd']:.3f} ({w['b'] / w['b_boot_sd']:+.1f} sigma); without b {wo['b']:+.3f} +- {wo['b_boot_sd']:.3f}")
    rat["master_" + nm] = dict(with_L=w, without_L=wo)
R["raw_slopes"] = rat
rw = sl["raw log(L850/L'CO)"]["with_L"]
line("H-C9a", abs(rw["b"]) < 2 * rw["b_boot_sd"], f"raw ratio slope {rw['b']:+.3f} +- {rw['b_boot_sd']:.3f} ({rw['b'] / rw['b_boot_sd']:+.2f} sigma)")
line("H-C9b", 0.04 <= rw["b_boot_sd"] <= 0.10, f"raw-ratio slope SE {rw['b_boot_sd']:.3f} in [0.04, 0.10]")
line("H-C9c", abs(sa_) <= abs(sR_), f"|slope alpha_CO| {abs(sa_):.3f} <= |slope raw| {abs(sR_):.3f}")

# ------------------------------------------------------------------ 3 shuffle control and toy optimiser (D11, D12)
T("\n== 3. Shuffle control (random partner tracer at matched L_IR) and the toy optimiser")


def merge_bins(idx, minN):
    idx = idx.copy()
    changed = True
    while changed:
        changed = False
        u = sorted(set(idx.tolist()))
        for k, b in enumerate(u):
            if (idx == b).sum() < minN and len(u) > 1:
                tgt = u[k - 1] if k > 0 else u[k + 1]
                idx[idx == b] = tgt; changed = True
                break
    return idx


def within_sd(Ltr, ratio):
    b = merge_bins(np.digitize(Ltr, EDGES), 10)
    ss, dof = 0.0, 0
    for g in set(b.tolist()):
        v = ratio[b == g]
        ss += ((v - v.mean()) ** 2).sum(); dof += len(v) - 1
    return math.sqrt(ss / dof)


shuf = {}
for nm, tab in (("ad: log(L850/L'CO)", "ad"), ("xd: log(L'CI/L850)", "xd")):
    rows, _ = joined(tab)
    La, Lb, LIR = [], [], []
    for r in rows:
        if tab == "ad":
            a, b = fl(r["logL850"]), fl(r["logLCO"])
        else:
            a, b = fl(r["logLCI"]), fl(r["logL850"])
        Lv = r["_LIRm"] if r["_LIRm"] is not None else r["_LIRo"]
        if None in (a, b, Lv):
            continue
        La.append(a); Lb.append(b); LIR.append(Lv)
    La, Lb, LIR = map(np.array, (La, Lb, LIR))
    real = within_sd(LIR, La - Lb)
    bins = merge_bins(np.digitize(LIR, EDGES), 10)
    rng = np.random.default_rng(2386)
    sh = []
    for k in range(300):
        Las = La.copy()
        for g in set(bins.tolist()):
            ii = np.where(bins == g)[0]
            Las[ii] = La[rng.permutation(ii)]
        sh.append(within_sd(LIR, Las - Lb))
    shm = float(np.mean(sh))
    # a second null: pairing shuffled within the whole sample (no L_IR matching)
    Lag = La[np.random.default_rng(2387).permutation(len(La))]
    glob = within_sd(LIR, Lag - Lb)
    T(f"  {nm}: N {len(La)}; within-L_IR-bin SD real {real:.3f}; shuffled-partner (300 shuffles, seed 2386) mean {shm:.3f} (2.5-97.5%: {np.percentile(sh, 2.5):.3f}-{np.percentile(sh, 97.5):.3f}); fully random partner {glob:.3f}; ratio real/shuffled {real / shm:.2f}")
    shuf[nm] = dict(N=len(La), real=real, shuffled=shm, ratio=real / shm, random=glob)
R["shuffle"] = shuf
k0 = "ad: log(L850/L'CO)"
line("H-C8a", 0.15 <= shuf[k0]["real"] <= 0.30, f"ad real within-bin SD {shuf[k0]['real']:.3f} in [0.15, 0.30]")
line("H-C8b", shuf[k0]["ratio"] < 0.8, f"ad real/shuffled {shuf[k0]['ratio']:.2f} < 0.8")
# toy optimiser
rng = np.random.default_rng(2388)
toy = {}
for w_ in (0.25, 0.5, 0.75):
    La = rng.normal(11, 0.5, 2000); Lb = rng.normal(24, 0.5, 2000)  # random inputs
    ma, mb, da, db, r_ = toy_optimise(La, Lb, 0.6, -13.0, w_)
    agree = float(np.max(np.abs(ma - mb)))
    xx = rng.uniform(0.0, 0.8, 2000)
    d_rel = 0.20
    ma2, mb2, da2, db2, r2_ = toy_optimise(La + d_rel * xx, Lb, 0.6, -13.0, w_)
    sda = np.polyfit(xx, da2 - da, 1)[0]; sdb = np.polyfit(xx, db2 - db, 1)[0]
    cm = 0.30 * xx
    ma3, mb3, da3, db3, r3_ = toy_optimise(La + cm, Lb + cm, 0.6, -13.0, w_)   # common-mode drift on both luminosities (masses)
    T(f"  toy w={w_}: max |mass_a - mass_b| {agree:.1e}; relative drift 0.20 per unit x in tracer a -> factor-a slope {sda:+.4f} (expect {-w_ * d_rel:+.4f}), factor-b slope {sdb:+.4f} (expect {(1 - w_) * d_rel:+.4f}); common-mode 0.30/x on both: factor slopes {np.polyfit(xx, da3 - da, 1)[0]:+.1e}, {np.polyfit(xx, db3 - db, 1)[0]:+.1e}; mass slopes {np.polyfit(xx, ma3 - ma, 1)[0]:+.3f}")
    toy[w_] = dict(agree=agree, sda=sda, sdb=sdb)
R["toy"] = toy
ctl6 = all(v["agree"] < 1e-12 for v in toy.values()) and all(abs(v["sda"] + w_ * 0.2) < 1e-9 and abs(v["sdb"] - (1 - w_) * 0.2) < 1e-9 for w_, v in toy.items())
T(f"[{'PASS' if ctl6 else 'FAIL'}] C6 toy optimiser: masses agree to <1e-12 for any input; a relative drift d appears as -w d and (1-w) d; a common-mode drift shifts the masses but not the factors")

# ------------------------------------------------------------------ 4 per-galaxy uncertainty
T("\n== 4. Per-galaxy uncertainty: catalogue e_logMH2 and factor scatter by z bin")
pg = {}
for t in TABLES:
    rows, _ = joined(t)
    for b, lo, hi in BINS:
        ee = [fl(r["e_logMH2"]) for r in rows if lo <= r["_z"] < hi and fl(r["e_logMH2"]) is not None]
        if len(ee) >= 3:
            pg[f"{t}:{b}"] = dict(N=len(ee), median=float(np.median(ee)), frac_le_0p10=float((np.array(ee) <= 0.10).mean()), p84=float(np.percentile(ee, 84)))
            T(f"  {t} {b}: N {len(ee)} median e_logMH2 {np.median(ee):.3f}  share <= 0.10: {np.mean(np.array(ee) <= 0.10):.2f}  84th pct {np.percentile(ee, 84):.3f}")
R["per_galaxy"] = pg
for combo in COMBOS:
    A = factor_arrays(*combo)
    sds = {b: float(A["y"][(A["z"] >= lo) & (A["z"] < hi)].std(ddof=1)) for b, lo, hi in BINS if ((A["z"] >= lo) & (A["z"] < hi)).sum() > 2}
    T(f"  SD of log {combo[1]} ({combo[0]}) per bin: " + ", ".join(f"{b} {v:.3f}" for b, v in sds.items()))
    R.setdefault("factor_sd", {})[f"{combo[0]}:{combo[1]}"] = sds
med_ok = all(0.07 <= v["median"] <= 0.13 for v in pg.values())
line("H-C10a", med_ok, f"median e_logMH2 per (table, bin) in [0.07, 0.13]: " + str({k: round(v['median'], 3) for k, v in pg.items()}))
sdad = R["factor_sd"]["ad:aCO"]
line("H-C10b", all(abs(v - 0.14) <= 0.03 for v in sdad.values()), f"SD of log aCO (ad) per bin {({k: round(v, 3) for k, v in sdad.items()})} within 0.14 +- 0.03")
T(f"  claim check: per-galaxy uncertainty above 0.10 dex in any (table, bin)? {[k for k, v in pg.items() if v['median'] > 0.10]}")

# ------------------------------------------------------------------ 5 cross-table model dependence
T("\n== 5. Cross-table differences for the same galaxy (the three optimisation routes)")
ct = {}
cache = {t: {r["Name"]: r for r in joined(t)[0]} for t in TABLES}
for (t1, t2, col, lab) in (("dax", "ad", "aCO", "alpha_CO"), ("dax", "xa", "aCO", "alpha_CO"), ("xa", "ad", "aCO", "alpha_CO"), ("dax", "xa", "XCI", "X_CI"), ("xd", "dax", "XCI", "X_CI")):
    names = [n for n in cache[t1] if n in cache[t2]]
    dd, zz, LL = [], [], []
    for n in names:
        a, b = fl(cache[t1][n][col]), fl(cache[t2][n][col])
        if a and b and a > 0 and b > 0:
            dd.append(math.log10(a) - math.log10(b)); zz.append(cache[t1][n]["_z"])
            LL.append(cache[t1][n]["_LIRm"] if cache[t1][n]["_LIRm"] is not None else cache[t1][n]["_LIRo"])
    dd, zz = np.array(dd), np.array(zz)
    if len(dd) < 5:
        continue
    s = msd(dd)
    x = np.log10(1 + zz)
    bb = ols_boot(np.column_stack([np.ones_like(x), x]), dd, 5000, 238)
    bz = np.polyfit(x, dd, 1)[0]
    byb = {b: (int(((zz >= lo) & (zz < hi)).sum()), float(dd[(zz >= lo) & (zz < hi)].mean())) for b, lo, hi in BINS if ((zz >= lo) & (zz < hi)).sum() > 2}
    T(f"  {lab}: log({t1}/{t2}) N {s['N']} mean {s['mean']:+.3f} SD {s['sd']:.3f}; slope vs log10(1+z) {bz:+.3f} +- {bb[:, 1].std():.3f}; by bin (N, mean) {byb}")
    ct[f"{t1}-{t2}:{col}"] = dict(N=s["N"], mean=s["mean"], sd=s["sd"], slope=float(bz), slope_sd=float(bb[:, 1].std()), byb=byb)
R["cross_table"] = ct
R["lines"] = LINES
R["C6"] = ctl6
dump(jp, R)
T.close()
sys.exit(0)
