#!/usr/bin/env python3
"""CFG533: MW exceptionalism.
A: SPARC external outer-slope control at the MW's scaled window (R/R_d and R/r_M, both footings).
B: inside-view search for direction-split MW rotation-curve tables in the on-disk .tex sources.
C: order-of-magnitude disequilibrium bracket (PROVISIONAL).
Frozen criteria: FROZEN_CRITERIA.md (committed alone first, 45897b75d).
kappa = 1/2 FITTED; footings never pooled; kernel nu_mono; no EFE; cold energy mass still required; not theory closed.
Run: nice -n 10 python3 cfg533_mw_exceptionalism.py      MUTATE: CFG533_MUTATE=1 (exit 1 = DETECTED)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "2"
import sys, json, math, re, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
SRC = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg532_work", "src"))
MUT = os.environ.get("CFG533_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
G = 4.30091e-6                       # kpc (km/s)^2 / Msun
CONV = 3.0857e19 / 1e6               # m/s^2 -> (km/s)^2/kpc
A0_SI = {"canonical": 9.36e-11, "alt": 1.13e-10}
A0 = {k: v * CONV for k, v in A0_SI.items()}
UPS_D, UPS_B = 0.5, 0.7
RD_MW = 2.50
MB_MW = 5.4516175961e10 + 1.1901640628e10     # CFG532 B1 grid stars + gas (cfg532_results.json 'baryons')
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}")


def nu(y):
    y = np.maximum(y, 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def slope(R, V, E):                  # identical to CFG532 slope() inside a pre-selected window
    x, y, w = np.log(R), np.log(V), (V / E) ** 2
    A = np.vstack([np.ones_like(x), x]).T
    C = np.linalg.inv(A.T @ (A * w[:, None]))
    b = C @ (A.T @ (w * y))
    return float(b[1]), float(math.sqrt(C[1, 1]))


# ------------------------------------------------------------------ SPARC
def load():
    tab = {}
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            vals = [float(t) for t in tok[1:18]]
        except ValueError:
            continue
        tab[tok[0]] = dict(zip(keys, vals))
    gal, nall = [], 0
    d_ = os.path.join(DATA, "sparc_data")
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        d = np.genfromtxt(os.path.join(d_, f), comments="#")
        if d.ndim != 2 or d.shape[1] < 8:
            continue
        nall += 1
        name = f.replace("_rotmod.dat", "")
        m = tab.get(name)
        if m is None or int(m["Q"]) > 2 or m["Inc"] < 30:
            continue
        gal.append(dict(name=name, R=d[:, 0], V=d[:, 1], eV=d[:, 2], Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5], meta=m))
    return gal, nall, tab


def vlaw(g, a0):
    Vb2 = g["Vg"] * np.abs(g["Vg"]) + UPS_D * g["Vd"] ** 2 + UPS_B * g["Vb"] ** 2
    gb = Vb2 / g["R"]
    ok = gb > 0
    V = np.full_like(g["R"], np.nan)
    V[ok] = np.sqrt(g["R"][ok] * nu(gb[ok] / a0) * gb[ok])
    return V, gb


P("=" * 110)
P(f"CFG533 MW exceptionalism{'  [MUTATE: Keplerian tail beyond each window inner edge]' if MUT else ''}")
P("=" * 110)
GALS, NALL, TAB = load()
P(f"  rotmod files {NALL}; Q<=2 and Inc>=30: {len(GALS)}")

# ------------------------------------------------------------------ controls
P("\n--- controls")
Rt = np.linspace(15, 27.5, 12)
bk, _ = slope(Rt, 200 * (Rt / 15) ** -0.5, np.full(12, 5.0)); bf, _ = slope(Rt, np.full(12, 200.0), np.full(12, 5.0))
check(abs(bk + 0.5) < 1e-9 and abs(bf) < 1e-9, f"K1 slope estimator: Kepler {bk:+.9f}, flat {bf:+.9f}")
# K2: ALG weighted rms on all Q<=2 points (CFG516 statistic; its own Q<=2 set, no inclination cut)
gq2 = []
d_ = os.path.join(DATA, "sparc_data")
for f in sorted(os.listdir(d_)):
    if f.endswith("_rotmod.dat"):
        nm = f.replace("_rotmod.dat", ""); m = TAB.get(nm)
        if m is None or int(m["Q"]) > 2:
            continue
        d = np.genfromtxt(os.path.join(d_, f), comments="#")
        gq2.append(dict(R=d[:, 0], V=d[:, 1], eV=d[:, 2], Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5]))
K2 = {}
ref516 = {"canonical": 0.1117, "alt": 0.1005}
for k in ("canonical", "alt"):
    rs, ws = [], []
    for g in gq2:
        V, gb = vlaw(g, A0[k])
        gobs = g["V"] ** 2 / g["R"]
        mk = (gobs > 0) & (gb > 0) & np.isfinite(V)
        rs.append(np.log10(gobs[mk]) - np.log10(V[mk] ** 2 / g["R"][mk])); ws.append((g["V"][mk] / np.maximum(g["eV"][mk], 1e-3)) ** 2)
    r, w = np.concatenate(rs), np.concatenate(ws)
    K2[k] = float(np.sqrt(np.sum(w * r * r) / np.sum(w)))
    check(abs(K2[k] - ref516[k]) <= 0.005, f"K2 ALG weighted rms [{k}] {K2[k]:.4f} vs CFG516 ALG_rotmod {ref516[k]} (|d| <= 0.005), {len(gq2)} gals, {len(r)} pts")
J532 = json.load(open(os.path.join(HERE, "..", "CFG532_mw_gaia_rotation_curves", "cfg532b_results.json")))
MWD = {}
for foot in ("canonical", "alt"):
    for rule in ("RMv", "RMphi"):
        c = J532["combined"]["RGB_LIM"][f"{foot}|{rule}"]
        MWD[f"{foot}|{rule}"] = dict(primary_delta=c["primary"]["mean"], primary_sig=c["primary"]["sig"], primary_Z=c["primary"]["Z"], Z_range=c["Z_range"])
check(len(MWD) == 4, "K3 MW combined Delta read from cfg532b_results.json: " + ", ".join(f"{k} {v['primary_delta']:+.3f}" for k, v in MWD.items()))

# ------------------------------------------------------------------ Part A
P("\n" + "=" * 110 + "\nPART A: SPARC outer slopes in the MW's scaled window (law = ALG on rotmod baryons)\n" + "=" * 110)
rM_MW = {k: math.sqrt(G * MB_MW / A0[k]) for k in A0}
WIN = {"S-Rd": {k: (15 / RD_MW, 27.5 / RD_MW) for k in A0}, "S-rM": {k: (15 / rM_MW[k], 27.5 / rM_MW[k]) for k in A0}}
P(f"  MW: R_d {RD_MW} kpc, M_b {MB_MW:.4e}; r_M canonical {rM_MW['canonical']:.3f}, alt {rM_MW['alt']:.3f} kpc")
for w, d in WIN.items():
    P(f"  window {w}: " + "  ".join(f"{k} [{d[k][0]:.3f}, {d[k][1]:.3f}]" for k in d))


def mb_sparc(m):
    return (0.5 * m["L36"] + 1.33 * m["MHI"]) * 1e9


def an_V(m):
    return 180 <= m["Vflat"] <= 260


def an_M(m):
    return 3.32e10 <= mb_sparc(m) <= 13.3e10


def verdict(arr, nmin):
    n = len(arr)
    if n < 2:
        return dict(n=n, verdict="NOT DIAGNOSTIC")
    mean = float(np.mean(arr)); se = float(np.std(arr, ddof=1) / math.sqrt(n)); med = float(np.median(arr))
    rng = np.random.default_rng(533)
    bs = np.median(rng.choice(arr, size=(2000, n), replace=True), axis=1)
    Z = mean / se if se > 0 else float("nan")
    if n < nmin or se > 0.05:
        v = "NOT DIAGNOSTIC"
    elif abs(mean) <= 0.05 and abs(med) <= 0.05:
        v = "LAW MATCHES EXTERNAL SLOPES"
    elif abs(mean) > 0.05 and abs(Z) >= 3:
        v = "LAW MISSES EXTERNAL SLOPES"
    else:
        v = "NOT DIAGNOSTIC"
    return dict(n=n, mean=mean, se=se, Z=Z, median=med, med_lo=float(np.percentile(bs, 16)), med_hi=float(np.percentile(bs, 84)),
                std=float(np.std(arr, ddof=1)), verdict=v)


cells, pergal = {}, {}
nreach = {}
for w in WIN:
    for foot in ("canonical", "alt"):
        lo, hi = WIN[w][foot]
        rows = []
        n_an = {"AN-V": 0, "AN-M": 0}; n_an_reach = {"AN-V": 0, "AN-M": 0}
        for g in GALS:
            m = g["meta"]
            scale = m["Rdisk"] if w == "S-Rd" else math.sqrt(G * mb_sparc(m) / A0[foot])
            isV, isM = an_V(m), an_M(m)
            n_an["AN-V"] += isV; n_an["AN-M"] += isM
            if not (scale > 0):
                continue
            x = g["R"] / scale
            V, gb = vlaw(g, A0[foot])
            sel = (x >= lo) & (x <= hi) & np.isfinite(V) & (g["V"] > 0) & (g["eV"] > 0)
            if sel.sum() < 4 or g["R"][sel].max() / g["R"][sel].min() < 1.35:
                continue
            n_an_reach["AN-V"] += isV; n_an_reach["AN-M"] += isM
            R, Vo, E, Vl = g["R"][sel], g["V"][sel], g["eV"][sel], V[sel]
            if MUT:
                Rlo = lo * scale
                # law value at the window's inner edge (interpolated in the full curve), Keplerian beyond it
                ok = np.isfinite(V)
                VRlo = float(np.interp(Rlo, g["R"][ok], V[ok]))
                Vl = VRlo * (R / Rlo) ** -0.5
            bd, sd = slope(R, Vo, E)
            bl, _ = slope(R, Vl, E)
            rows.append(dict(name=g["name"], n=int(sel.sum()), Rmin=float(R.min()), Rmax=float(R.max()), b_data=bd, sig=sd, b_law=bl,
                             delta=bd - bl, Vflat=m["Vflat"], Mb=mb_sparc(m), Rd=m["Rdisk"], anV=bool(isV), anM=bool(isM)))
        key = f"{w}|{foot}"
        D = np.array([r["delta"] for r in rows])
        res = verdict(D, 10)
        sig = np.sqrt(np.array([r["sig"] for r in rows]) ** 2 + 0.03 ** 2)
        res["ivw_mean"] = float(np.sum(D / sig ** 2) / np.sum(1 / sig ** 2)); res["ivw_err"] = float(1 / math.sqrt(np.sum(1 / sig ** 2)))
        bdat = np.array([r["b_data"] for r in rows]); blaw = np.array([r["b_law"] for r in rows])
        res["b_data_median"] = float(np.median(bdat)); res["b_law_median"] = float(np.median(blaw))
        res["frac_bdata_le_m028"] = float(np.mean(bdat <= -0.28))
        res["n_bdata_le_m028"] = int(np.sum(bdat <= -0.28))
        # MW percentile in the external Delta distribution (vs the matching-footing MW combined Delta, both rules)
        res["MW_percentile"] = {rule: float(np.mean(D <= MWD[f"{foot}|{rule}"]["primary_delta"])) for rule in ("RMv", "RMphi")}
        an = {}
        for a, fl in (("AN-V", "anV"), ("AN-M", "anM")):
            sub = [r for r in rows if r[fl]]
            Da = np.array([r["delta"] for r in sub])
            an[a] = verdict(Da, 5) if len(Da) >= 2 else dict(n=len(Da), verdict="NOT DIAGNOSTIC")
            an[a]["n_total"] = n_an[a]; an[a]["n_reach"] = n_an_reach[a]
            an[a]["b_data"] = {r["name"]: round(r["b_data"], 3) for r in sub}
            an[a]["b_law"] = {r["name"]: round(r["b_law"], 3) for r in sub}
            an[a]["n_bdata_le_m028"] = int(sum(r["b_data"] <= -0.28 for r in sub))
            an[a]["MW_percentile"] = {rule: (float(np.mean(Da <= MWD[f"{foot}|{rule}"]["primary_delta"])) if len(Da) else None) for rule in ("RMv", "RMphi")}
        res["analogues"] = an
        cells[key] = res; pergal[key] = rows
        P(f"\n  [{key}] window [{lo:.3f}, {hi:.3f}]  scored N = {res['n']} of {len(GALS)}")
        if res["n"] >= 2:
            P(f"    Delta = b_data - b_law: mean {res['mean']:+.4f} +- {res['se']:.4f} (Z {res['Z']:+.2f}), median {res['median']:+.4f} "
              f"[{res['med_lo']:+.4f}, {res['med_hi']:+.4f}], scatter {res['std']:.3f}; IVW (sig+0.03) {res['ivw_mean']:+.4f} +- {res['ivw_err']:.4f}")
            P(f"    median slopes: data {res['b_data_median']:+.3f}, law {res['b_law_median']:+.3f}; data slope <= -0.28 in {res['n_bdata_le_m028']}/{res['n']} "
              f"({res['frac_bdata_le_m028']:.1%}); MW combined Delta percentile: RM-v {res['MW_percentile']['RMv']:.1%}, RM-phi {res['MW_percentile']['RMphi']:.1%}")
        P(f"    -> {res['verdict']}")
        for a in ("AN-V", "AN-M"):
            x = an[a]
            s = f"    {a}: {x['n_total']} in sample, {x['n_reach']} reach the window"
            if x["n"] >= 2:
                s += (f"; Delta mean {x['mean']:+.3f} +- {x['se']:.3f}, median {x['median']:+.3f}; data slope <= -0.28: {x['n_bdata_le_m028']}/{x['n']}"
                      f"; MW pct RM-v {x['MW_percentile']['RMv']:.0%} -> {x['verdict']}")
            P(s)
            if x["n"]:
                P("      " + ", ".join(f"{nm} {x['b_data'][nm]:+.2f}/{x['b_law'][nm]:+.2f}" for nm in x["b_data"]))

diag = [c for c in cells.values() if c["verdict"] != "NOT DIAGNOSTIC"]
if any(c["verdict"] == "LAW MISSES EXTERNAL SLOPES" for c in diag):
    VA = "LAW MISSES EXTERNAL SLOPES"
elif diag and all(c["verdict"] == "LAW MATCHES EXTERNAL SLOPES" for c in diag):
    VA = "LAW MATCHES EXTERNAL SLOPES"
else:
    VA = "NOT DIAGNOSTIC"
miss_sign = [math.copysign(1, c["mean"]) for c in diag if c["verdict"] == "LAW MISSES EXTERNAL SLOPES"]
P(f"\n  VERDICT A: {VA}" + (f"  (miss sign(s) {miss_sign})" if miss_sign else ""))

# ------------------------------------------------------------------ Part B
P("\n" + "=" * 110 + "\nPART B: direction-split MW rotation-curve tables in the on-disk .tex sources\n" + "=" * 110)
B = dict(tables=[], split_tables=[])
pat = re.compile(r"\\begin\{(table\*?|deluxetable\*?)\}(.*?)\\end\{\1\}", re.S)
kw = re.compile(r"north|south|hemisph|z\s*[<>]\s*0|azimuth|\\phi|wedge|anti-?cent|slice", re.I)
rc = re.compile(r"V_?\{?\\?r?m?\s*\{?c|v_c|circular|rotation|V_\\phi|V_\{\\phi\}", re.I)
if os.path.isdir(SRC):
    for fn in sorted(glob.glob(os.path.join(SRC, "*", "*.tex"))) + sorted(glob.glob(os.path.join(SRC, "*.tex"))):
        txt = open(fn, errors="ignore").read()
        for mt in pat.finditer(txt):
            body = mt.group(2)
            cap = re.search(r"\\caption\{(.*?)\}\s*(\\label|$|\n)", body, re.S)
            capt = (cap.group(1) if cap else body[:200]).replace("\n", " ")[:160]
            rel = os.path.relpath(fn, SRC)
            line = txt[:mt.start()].count("\n") + 1
            isrc = bool(rc.search(body)); issplit = bool(kw.search(body))
            B["tables"].append(dict(file=rel, line=line, caption=capt, rc_like=isrc, split_kw=issplit))
            if isrc and issplit:
                B["split_tables"].append(dict(file=rel, line=line, caption=capt))
    P(f"  table environments scanned: {len(B['tables'])} in {SRC.split('/')[-3]}/.../src")
    for t in B["tables"]:
        P(f"    {t['file']}:{t['line']}  rc-like {t['rc_like']!s:<5} split-kw {t['split_kw']!s:<5}  {t['caption'][:110]}")
    P(f"  candidate split RC tables (rc-like AND split keyword): {len(B['split_tables'])}")
    for t in B["split_tables"]:
        P(f"    CANDIDATE {t['file']}:{t['line']}  {t['caption']}")
else:
    P("  source directory not found")
# manual inspection result of any candidates (declared in README): SL24 table is reduced chi^2 per |z| slice for model fits,
# not a rotation curve; no per-bin V_c by azimuth/hemisphere/height exists in any table.
B["manual_inspection"] = ("both candidates inspected by eye: 2211.05668:775 is Wang+23's single anticentre (160<l<200) V_c table (R, v_c, sigma) -- "
                          "the keyword hit is 'anti-center', not a split; 2410.14307:774 is reduced chi2 of model fits per |z| slice (no V_c values). "
                          "No tabulated V_c split by azimuth, hemisphere or height exists on disk")
P("  manual inspection: " + B["manual_inspection"])
# text-level bounds -> largest Delta slope they allow (delta V/V at R_out over ln(R_out/15))
TXT = [("Jiao+23 l-split (160-180 vs 180-200 deg), text: < 2% within 22 kpc", 0.02, 22.0),
       ("Jiao+23 beyond 22 kpc, 'comparable to the cross-term' (cross-term up to ~8% near 27 kpc), text", 0.08, 27.0),
       ("Zhou+23 phi split (-30..0 vs 0..30 deg), text: <~ 1% overall (to 24 kpc)", 0.01, 24.0),
       ("Feng+26 azimuthal wedges, text: <= 3% (Cepheids, to 17.6 kpc)", 0.03, 17.6)]
B["text_bounds"] = []
for lab, f, Ro in TXT:
    db = f / math.log(Ro / 15.0)
    B["text_bounds"].append(dict(label=lab, frac=f, R_out=Ro, max_dslope=db))
    P(f"  text bound: {lab}: max |d slope| ~ {db:.3f}")
P("  Wang+23 text: for R > 15 kpc V_phi shows no significant variation with |Z| (|Z|, not signed; figures only)")
VB = "NO DATA"
P(f"\n  VERDICT B: {VB}")

# ------------------------------------------------------------------ Part C
P("\n" + "=" * 110 + "\nPART C: disequilibrium bracket, ORDER OF MAGNITUDE ONLY (PROVISIONAL)\n" + "=" * 110)
Vc = 200.0; L = math.log(27.5 / 15)
C = {}
for dv in (10.0, 20.0):
    C[f"ramp_{int(dv)}"] = (dv / Vc) / L
    P(f"  (i) bias ramping 0 -> {dv:.0f} km/s across 15-27.5 kpc: d slope ~ {C[f'ramp_{int(dv)}']:.3f}")
P("  (ii) constant offset: d slope ~ 0 to first order (amplitude only)")
for sR in (28.4, 35.0):     # 28.4 on disk (Zhou+23); 35 recalled (PROVISIONAL)
    dv = sR ** 2 / Vc / 2   # dV ~ sigma_R^2 * (error in the log-derivative sum) / (2V), per unit error
    C[f"jeans_sigR{sR}"] = dv
    P(f"  Jeans pressure term: sigma_R {sR} km/s{' (recalled)' if sR == 35.0 else ' (Zhou+23, on disk)'}: dV ~ {dv:.1f} km/s per unit error in "
      f"(dln nu/dlnR + dln sigma_R^2/dlnR); a unit error ramping across the window -> d slope ~ {dv / Vc / L:.3f}")
need = {k: -v["primary_delta"] for k, v in MWD.items()}
P("  MW miss to explain (CFG532b primary, -Delta): " + ", ".join(f"{k} {v:.3f}" for k, v in need.items()))
P("  -> 10-20 km/s of non-circular bias growing outward gives 0.08-0.17, the size of the miss; a uniform offset does not.")

# ------------------------------------------------------------------ post-run diagnostics (added after the first run; NOT verdict inputs)
P("\n" + "=" * 110 + "\nPOST-RUN DIAGNOSTICS (added after the first run; disclosed; not verdict inputs)\n" + "=" * 110)
PR = {}
for key, rows in pergal.items():
    bd = np.array([r["b_data"] for r in rows]); bl = np.array([r["b_law"] for r in rows]); sg = np.array([r["sig"] for r in rows])
    D = bd - bl
    d = {}
    sel = bl <= -0.10                                   # (a) select on the PREDICTION (independent of data noise)
    d["a_law_declining"] = dict(n=int(sel.sum()), mean=float(D[sel].mean()) if sel.sum() else None,
                                se=float(D[sel].std(ddof=1) / math.sqrt(sel.sum())) if sel.sum() > 1 else None,
                                b_data_mean=float(bd[sel].mean()) if sel.sum() else None, b_law_mean=float(bl[sel].mean()) if sel.sum() else None)
    A = np.vstack([np.ones_like(bl), bl]).T                # (b) OLS b_data on b_law (undefined if b_law is constant, e.g. MUTATE)
    if np.std(bl) > 1e-6:
        cf, res_, _, _ = np.linalg.lstsq(A, bd, rcond=None)
        s2 = float(np.sum((bd - A @ cf) ** 2) / (len(bd) - 2)); cov = s2 * np.linalg.inv(A.T @ A)
        d["b_ols"] = dict(intercept=float(cf[0]), slope=float(cf[1]), slope_err=float(math.sqrt(cov[1, 1])))
    else:
        cf = [float("nan"), float("nan")]; d["b_ols"] = dict(intercept=None, slope=None, slope_err=float("nan"))
    ms = float(np.median(sg)); sc = float(np.std(D, ddof=1))  # (c) noise vs scatter
    d["c_scatter"] = dict(scatter=sc, median_sig=ms, intrinsic=float(math.sqrt(max(sc ** 2 - ms ** 2, 0))))
    seld = bd <= -0.20                                   # (d) select on DATA (biased by regression to the mean)
    d["d_data_declining"] = dict(n=int(seld.sum()), mean=float(D[seld].mean()) if seld.sum() else None)
    PR[key] = d
    a = d["a_law_declining"]
    P(f"  [{key}] (a) law-predicted decliners (b_law <= -0.10): N {a['n']}" + (f", Delta {a['mean']:+.3f} +- {a['se']:.3f}, <b_data> {a['b_data_mean']:+.3f} vs <b_law> {a['b_law_mean']:+.3f}" if a["n"] > 1 else ""))
    P(f"           (b) OLS b_data = {cf[0]:+.3f} + {cf[1]:.2f}(+-{d['b_ols']['slope_err']:.2f}) b_law;  (c) scatter {sc:.3f}, median per-galaxy sigma {ms:.3f}, "
      f"implied intrinsic {d['c_scatter']['intrinsic']:.3f};  (d) data-selected b_data <= -0.20: N {d['d_data_declining']['n']}, Delta "
      + (f"{d['d_data_declining']['mean']:+.3f}" if d['d_data_declining']['n'] else "-") + " (biased low by construction)")

# ------------------------------------------------------------------ overall
if VA == "LAW MATCHES EXTERNAL SLOPES":
    VO = "MW TENSION LOCALISED TO MW"
elif VA == "LAW MISSES EXTERNAL SLOPES" and any(s < 0 and abs(c["mean"]) > 0.05 for s, c in zip(miss_sign, [c for c in diag if c["verdict"] == "LAW MISSES EXTERNAL SLOPES"])):
    VO = "GRAVITY-LEVEL TENSION"
else:
    VO = "OPEN"
P(f"\nOVERALL: A {VA}; B {VB}; -> {VO}")
P(f"checks {sum(o for o, _ in CHECKS)}/{len(CHECKS)} pass")

RES = dict(mutate=MUT, n_rotmod=NALL, n_sample=len(GALS), windows=WIN, rM_MW=rM_MW, MB_MW=MB_MW, RD_MW=RD_MW, K2=K2, MW_combined=MWD,
           cells=cells, verdict_A=VA, miss_sign=miss_sign, partB=B, verdict_B=VB, partC=dict(values=C, provisional=True, need=need),
           verdict_overall=VO, post_run=PR, per_galaxy=pergal, checks=[dict(ok=o, msg=m) for o, m in CHECKS])
json.dump(RES, open(os.path.join(HERE, f"cfg533_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg533{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    det = all(c["verdict"] == "LAW MISSES EXTERNAL SLOPES" and c["mean"] > 0 for c in cells.values())
    P(f"MUTATE: {'DETECTED' if det else 'NOT DETECTED'} ({sum(c['verdict'] == 'LAW MISSES EXTERNAL SLOPES' and c['mean'] > 0 for c in cells.values())}/4 cells)")
    open(os.path.join(HERE, f"cfg533{TAG}.out"), "a").write(OUT[-1] + "\n")
    sys.exit(1 if det else 0)
