#!/usr/bin/env python3
"""HL3 (criteria ef4595f390 + AMENDMENT A1): the plain-law cluster residual rho = log10(g_obs / g_law) per cluster and
radius on the LENSING leg (CLASH, Tian+2020 84 points, g_tot from Umetsu+2016 lensing) and the HYDROSTATIC leg (X-COP,
M_FORW), both footings, radii in r/R500. Writes hl3_points.json (every point, both legs) and hl3_points.out (KA1-KA5).
    python3 hl3.py
Loaders executed from source, unchanged (NA2 -> QX7 iter_5 -> iter_4 -> QX5). Downloaded sources are parsed as text
only. kappa = 1/2 FITTED; not theory closed. Adopts nothing. 1 thread."""
import os, sys, io, re, json, math, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
DATA = os.path.join(REPO, "real_research", "data"); EXT = os.path.join(REPO, "_external_data", "hl3")
OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
def rel(p): return os.path.relpath(p, REPO)

# ------------------------------------------------------------------ NA2's prelude, executed from source (loaders, A0, glaw, x_eval, fit_x)
NA2 = os.path.join(REPO, "closure_2026_11_07", "NA2_compact_baryon_remnant", "na2.py")
src = open(NA2).read(); cut = src.index("# ------------------------------------------------------------------ GB1 battery")
NS = {"__file__": NA2, "__name__": "na2_reused"}; argv0, sys.argv = sys.argv, [NA2]; so = sys.stdout; sys.stdout = io.StringIO()
try: exec(compile(src[:cut], NA2, "exec"), NS)
finally: sys.argv = argv0; sys.stdout = so
A0, glaw, G, MS, KPC, XC, XINFO = (NS[k] for k in ("A0", "glaw", "G", "MS", "KPC", "XC", "XINFO"))
P(f"HL3 MAIN: footings {', '.join(f'{f} a0 {a:.4e}' for f, a in A0.items())} (the loaders' values, AMENDMENT A1 item 1). kappa = 1/2 FITTED; not theory closed.")
P(f"law: g = g_N/2 + sqrt(g_N^2/4 + a0 g_N), the inversion of g_N = g^2/(g + a0); rho = log10(g_obs / g_law(g_bar)).")
def rho_of(gobs, gbar, a0): return np.log10(np.asarray(gobs, float) / glaw(np.asarray(gbar, float), a0))
def li(r, m, t):
    """log-log interpolation inside the tabulated range, nan outside (QX5's li, restated here)."""
    r = np.asarray(r, float); m = np.asarray(m, float); t = float(t)
    if t < r[0] or t > r[-1]: return float("nan")
    return float(10 ** np.interp(math.log10(t), np.log10(r), np.log10(m)))

# ------------------------------------------------------------------ KA5: the inversion
P(); P("KA5 law inversion")
ka5 = {}
for f, a0 in A0.items():
    gN = np.array([1e10, 1e9]) * a0; hi = np.abs(glaw(gN, a0) / gN - 1)
    x = np.array([1e-3, 4e-4, 1e-4]); gd = x * a0; lo = np.abs(glaw(gd, a0) / np.sqrt(a0 * gd) - 1)
    g = glaw(np.geomspace(1e-6, 1e6, 25) * a0, a0); rt = np.abs(g ** 2 / (g + a0) / (np.geomspace(1e-6, 1e6, 25) * a0) - 1).max()
    ka5[f] = dict(hi_dev_1e10=float(hi[0]), hi_dev_1e9=float(hi[1]), deep_dev_1e_3=float(lo[0]), deep_dev_4e_4=float(lo[1]), deep_dev_1e_4=float(lo[2]), roundtrip_max=float(rt),
                  pass_hi=bool(hi[0] <= 1e-9), pass_deep_literal=bool(lo[0] <= 0.01), pass_deep_1e_4=bool(lo[2] <= 0.01), pass_roundtrip=bool(rt <= 1e-9))
    P(f"[{f}] g/g_N - 1 at g_N = 1e10 a0: {hi[0]:.2e} (1e9 a0: {hi[1]:.2e}); g/sqrt(a0 g_N) - 1 at g_N = 1e-3 a0: {lo[0]:.4f}, 4e-4 a0: {lo[1]:.4f}, 1e-4 a0: {lo[2]:.4f}; "
      f"round trip g^2/(g + a0) = g_N over 1e-6..1e6 a0: max dev {rt:.1e}")
P("KA5 reading: the high end and the round trip pass. The deep end at exactly g_N = 1e-3 a0 deviates by sqrt(x)/2 = 1.58 % by the law's own exact expansion"
  " g = sqrt(a0 g_N) (1 + sqrt(x)/2 + ...); the literal 1 % bar is met from g_N <= 4e-4 a0. The bar as frozen cannot be met by any correct implementation at 1e-3; disclosed, not amended.")

# ------------------------------------------------------------------ the lensing leg: Tian+2020 points (on disk)
P(); P("LENSING LEG: Tian+2020 (VizieR J/ApJ/896/70/fig2) 84 points, g_tot from Umetsu+2016 joint SL+WL lensing, g_bar = Donahue+2014 gas + BCG")
T = []
for line in open(os.path.join(DATA, "clash_rar_tian2020_fig2.tsv")):
    if line.startswith("#") or not line.strip(): continue
    f = line.rstrip("\n").split("\t")
    if len(f) < 7: continue
    try: r, a, b, ea, eb = (float(x) for x in f[2:7])
    except ValueError: continue
    T.append(dict(name=f[1].strip(), r_kpc=r, lgbar=a, lgtot=b, e_lgbar=ea, e_lgtot=eb))
assert len(T) == 84, len(T)
def key(name):
    """cluster key: 'A' + number for Abell; the 4-digit RA code otherwise (prefix letters dropped: MACSJ1532 = RXJ1532)."""
    n = name.replace("~", "").replace(" ", "").replace("*", "")
    m = re.match(r"^A(?:bell)?(\d+)$", n, re.I)
    if m: return "A" + m.group(1)
    m = re.search(r"(\d{4})", n); return m.group(1) if m else n
def tex_rows(path, skip_prefixes=()):
    rows = []
    for ln in open(path, errors="replace"):
        if "&" not in ln or ln.lstrip().startswith(("\\", "%")): continue
        cells = [re.sub(r"\\tablenotemark\{\w\}|\$|\\pm.*|\\\\|~", "", c).strip() for c in ln.split("&")]
        if any(cells[0].replace(" ", "").startswith(p) for p in skip_prefixes): continue
        rows.append(cells)
    return rows
def pm(cell):
    m = re.match(r"\s*([-+]?\d*\.?\d+)\s*(?:\\pm\s*([-+]?\d*\.?\d+))?", cell); return (float(m.group(1)), float(m.group(2)) if m.group(2) else None) if m else (None, None)
U = os.path.join(EXT, "umetsu16", "src"); D = os.path.join(EXT, "donahue14", "src")
# Umetsu table1: z_l; table3: M2500c, M1000c, M500c ... (1e14 Msun, h 0.7, Om 0.27, OL 0.73, NFW fits to the lensing profiles)
Z = {}; M500L = {}; SAMPLE = {}; sect = "xray"
for ln in open(os.path.join(U, "table1.tex"), errors="replace"):
    if "High Magnification" in ln: sect = "himag"
    if ln.lstrip().startswith("~~"):
        c = ln.split("&"); Z[key(c[0])] = float(c[1].replace("$", "")); SAMPLE[key(c[0])] = sect
for ln in open(os.path.join(U, "table3.tex"), errors="replace"):
    if ln.lstrip().startswith("~~"):
        c = ln.split("&"); M500L[key(c[0])] = pm(c[3].replace("$", ""))
for ln in open(os.path.join(U, "table2.tex"), errors="replace"):
    if ln.lstrip().startswith("~~"):
        c = ln.split("&"); SAMPLE.setdefault(key(c[0]), sect)
# Donahue Chandra HSE table: r500 (h70 Mpc) is column 11 (0-based), sigma column 12
R500D = {}
blk = open(os.path.join(D, "xray_clash.tex"), errors="replace").read()
blk = blk[blk.index("Chandra HSE Masses"):]; blk = blk[blk.index("\\startdata"):blk.index("\\enddata")]
for ln in blk.splitlines():
    c = [x.strip() for x in ln.split("&")]
    if len(c) < 13 or not re.search(r"\d", c[0]) or c[0].startswith(("CLJ1226", "MACS2129", "MACS1311", "MACS1423")) or "1423" in c[0]: continue
    try: R500D[key(c[0])] = (float(c[11].replace("\\\\", "").split()[0]), float(c[12].replace("\\\\", "").split()[0]))
    except (ValueError, IndexError): pass
H0 = 70.0 * 1e3 / (1e3 * KPC); OM, OL = 0.27, 0.73   # Umetsu's stated convention; the same background convention as X-COP's Ettori R500
def r500_from_m500(M14, z):
    Ez2 = OM * (1 + z) ** 3 + OL; rhoc = 3 * H0 ** 2 * Ez2 / (8 * math.pi * G)
    return (3 * M14 * 1e14 * MS / (4 * math.pi * 500 * rhoc)) ** (1 / 3) / KPC
MERGERS = sorted(k for k, s in SAMPLE.items() if s == "himag")
P(f"Umetsu+2016 table1/3: {len(Z)} clusters with z, {len(M500L)} with M500c; high-magnification (mergers): {MERGERS}; Donahue+2014 Chandra r500 for {len(R500D)} of them")
LENS = []; names = sorted({t["name"] for t in T})
for nm in names:
    k = key(nm); z = Z[k]; M5, eM5 = M500L[k]; R5 = r500_from_m500(M5, z); R5lo, R5hi = r500_from_m500(M5 - eM5, z), r500_from_m500(M5 + eM5, z)
    RD = R500D[k][0] * 1e3
    for t in T:
        if t["name"] != nm: continue
        rec = dict(leg="lensing", name=nm, key=k, z=z, merger=SAMPLE[k] == "himag", r_kpc=t["r_kpc"], R500_kpc=R5, R500_lo=R5lo, R500_hi=R5hi, R500_donahue_kpc=RD,
                   x=t["r_kpc"] / R5, x_donahue=t["r_kpc"] / RD, lgbar=t["lgbar"], lgtot=t["lgtot"], e_lgbar=t["e_lgbar"], e_lgtot=t["e_lgtot"])
        for f, a0 in A0.items(): rec[f"rho_{f}"] = float(rho_of(10 ** t["lgtot"], 10 ** t["lgbar"], a0))
        LENS.append(rec)
P(f"lensing leg: {len(LENS)} points, {len(names)} clusters ({sum(1 for k in set(r['key'] for r in LENS) if SAMPLE[k] == 'xray')} X-ray selected + {len(MERGERS)} mergers); r/R500 spans "
  f"{min(r['x'] for r in LENS):.3f}-{max(r['x'] for r in LENS):.3f} (Umetsu M500c), {min(r['x_donahue'] for r in LENS):.3f}-{max(r['x_donahue'] for r in LENS):.3f} (Donahue r500)")
P("  per cluster: name  z  M500c[1e14]  R500[kpc] (Umetsu)  r500[kpc] (Donahue)  points  x range  merger")
for nm in names:
    rs = [r for r in LENS if r["name"] == nm]; r0 = rs[0]
    P(f"  {nm:9s} {r0['z']:.3f} {M500L[r0['key']][0]:6.2f} {r0['R500_kpc']:7.0f} {r0['R500_donahue_kpc']:7.0f} {len(rs):2d} {min(r['x'] for r in rs):.3f}-{max(r['x'] for r in rs):.3f} {'MERGER' if r0['merger'] else ''}")
P("  D1 extension beyond 600 kpc: NOT RUN (Umetsu+2016's source carries the profiles as figures only; AMENDMENT A1 item 4). D3 LoCuSS: NOT RUN (shear profiles as figures only).")

# ------------------------------------------------------------------ KA1: h56 replay (one a0, h56's kernel nu = 1/(1 - e^-sqrt y), its grid)
P(); P("KA1 h56 replay on the 84 points (h56's kernel and grid; a read-the-leg check)")
lgb = np.array([t["lgbar"] for t in T]); lgt = np.array([t["lgtot"] for t in T]); elgb = np.array([t["e_lgbar"] for t in T]); elgt = np.array([t["e_lgtot"] for t in T]); nmz = np.array([t["name"] for t in T])
def nu56(y): y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def dl56(y): y = np.maximum(np.asarray(y, float), 1e-12); s = np.sqrt(y); return 1.0 - s * np.exp(-s) / (2.0 * (1.0 - np.exp(-s)))
def chi56(la0, b, t, eb, et):
    a0 = 10 ** la0; y = 10 ** b / a0; sig2 = et ** 2 + (dl56(y) * eb) ** 2; r = t - np.log10(10 ** b * nu56(y)); return float(np.sum(r * r / sig2))
grid = np.linspace(-11.5, -8.0, 3501); ch = np.array([chi56(v, lgb, lgt, elgb, elgt) for v in grid]); la_best = grid[np.argmin(ch)]; chi_best = ch.min()
per = []
for cl in names:
    m = nmz == cl
    if m.sum() < 2: continue
    per.append(grid[np.argmin([chi56(v, lgb[m], lgt[m], elgb[m], elgt[m]) for v in grid])])
sc56 = float(np.std(per, ddof=1))
ka1 = dict(chi2=chi_best, chi2_ref=136.1, a0_fit=10 ** la_best, scatter=sc56, scatter_ref=0.176, n_clusters=len(per),
           passed=bool(abs(chi_best / 136.1 - 1) <= 0.01 and abs(sc56 / 0.176 - 1) <= 0.01))
P(f"one a0 for all 84 points: a0 = {10 ** la_best:.3e}, chi2 = {chi_best:.1f} (h56: 136.1); per-cluster log a0 scatter {sc56:.3f} dex over {len(per)} clusters (h56: 0.176) -> {'PASS' if ka1['passed'] else 'FAIL'}")

# ------------------------------------------------------------------ KA2: Tian+2020 slope-1/2 fit, g_tot = sqrt(g_ddagger g_bar)
w = 1.0 / (elgt ** 2 + 0.25 * elgb ** 2); lgdd = float(np.sum(w * (2 * lgt - lgb)) / np.sum(w)); e_lgdd = float(1 / math.sqrt(np.sum(w)))
gdd = 10 ** lgdd; ka2 = dict(g_ddagger=gdd, err_dex=e_lgdd, ref=2.02e-9, passed=bool(abs(gdd / 2.02e-9 - 1) <= 0.10))
P(); P(f"KA2 slope-fixed fit log g_tot = 1/2 log g_bar + 1/2 log g_ddagger (weights 1/(e_tot^2 + e_bar^2/4)): g_ddagger = {gdd:.3e} m/s^2 (+- {e_lgdd:.3f} dex; Tian+2020: 2.02e-9) -> {'PASS' if ka2['passed'] else 'FAIL'}")

# ------------------------------------------------------------------ the hydrostatic leg: X-COP (12 on disk, 7 with measured stars)
P(); P("HYDROSTATIC LEG: X-COP per-cluster profiles (hydro M_FORW, gas MGAS, stars MSTAR), R500 from the Ettori 2019 json, radii = the gas-profile grid where all three profiles are tabulated")
R5J = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json")))
XD = os.path.join(DATA, "xcop"); XN = sorted(d for d in os.listdir(XD) if os.path.isdir(os.path.join(XD, d)))
PROF = {}
for name in XN:
    p_ = os.path.join(XD, name)
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500h = float(h[1].header["R500"])
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy()
    st = None
    if os.path.exists(os.path.join(p_, f"{name}_mstar.fits")):
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    hr = np.array(hm["RADIUS"], float); hM = np.array(hm["M_FORW"], float); okh = np.isfinite(hM) & (hM > 0)
    gr = np.array(gas["RADIUS"], float) * r500h; gM = np.array(gas["MGAS"], float); okg = np.isfinite(gM) & (gM > 0) & (gr > 0)
    d = dict(hr=hr[okh], hM=hM[okh], gr=gr[okg], gM=gM[okg], r500_fits=r500h, R500=R5J[name]["R500"] * 1e3, stars=st is not None)
    if st is not None:
        sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float); oks = np.isfinite(sM) & (sM > 0) & (sr > 0); d["sr"], d["sM"] = sr[oks], sM[oks]
    PROF[name] = d
WITH = [n for n in XN if PROF[n]["stars"]]; WITHOUT = [n for n in XN if not PROF[n]["stars"]]
P(f"clusters: {len(XN)}; with measured stellar profiles (PRIMARY): {WITH}; gas + hydro only (12-cluster bracket, stars imputed): {WITHOUT}")
# imputation table: median over the 7 of M_star/M_gas at r/R500, on a log grid
xg = np.geomspace(0.02, 2.0, 60); FR = []
for n in WITH:
    d = PROF[n]; fr = []
    for x in xg:
        r = x * d["R500"]; mg, ms = li(d["gr"], d["gM"], r), li(d["sr"], d["sM"], r); fr.append(ms / mg if np.isfinite(mg) and np.isfinite(ms) else np.nan)
    FR.append(fr)
FR = np.array(FR)
import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore'); fstar_med = np.nanmedian(FR, axis=0)
okf = np.isfinite(fstar_med)
def fstar(x): return float(np.interp(math.log(x), np.log(xg[okf]), fstar_med[okf]))
P(f"imputation (bracket only): median M_star/M_gas over the 7 = {fstar(0.1):.3f} at 0.1 R500, {fstar(0.3):.3f} at 0.3, {fstar(0.7):.3f} at 0.7, {fstar(1.0):.3f} at 1.0")
HYD = []
for name in XN:
    d = PROF[name]; n_pts = 0
    for r in d["gr"]:
        mh, mg = li(d["hr"], d["hM"], r), li(d["gr"], d["gM"], r)
        if d["stars"]: ms = li(d["sr"], d["sM"], r); imput = False
        else: ms = fstar(r / d["R500"]) * mg if np.isfinite(mg) else np.nan; imput = True
        if not (np.isfinite(mh) and np.isfinite(mg) and np.isfinite(ms)): continue
        rm = r * KPC; gobs = G * mh * MS / rm ** 2; gbar = G * (mg + ms) * MS / rm ** 2
        rec = dict(leg="hydrostatic", name=name, r_kpc=float(r), R500_kpc=d["R500"], x=float(r / d["R500"]), lgbar=float(np.log10(gbar)), lgtot=float(np.log10(gobs)),
                   M_hyd=mh, M_gas=mg, M_star=ms, stars_measured=not imput, a2319=name == "A2319", mforw_beyond_gas=False)
        for f, a0 in A0.items(): rec[f"rho_{f}"] = float(rho_of(gobs, gbar, a0))
        HYD.append(rec); n_pts += 1
    xs = [h["x"] for h in HYD if h["name"] == name]
    P(f"  {name:8s} R500 {d['R500']:.0f} kpc (fits header {d['r500_fits']:.0f}); {n_pts} radii, r/R500 {min(xs):.3f}-{max(xs):.3f}; stars {'measured' if d['stars'] else 'IMPUTED'}{'; A2319 flagged (non-thermal pressure claim)' if name == 'A2319' else ''}")
P(f"hydrostatic leg: {len(HYD)} points in {len(XN)} clusters ({sum(1 for h in HYD if h['stars_measured'])} points with measured stars in {len(WITH)} clusters)")

# ------------------------------------------------------------------ KA3: NA2's bins through NA2's own machinery
P(); P("KA3 NA2 replay through NA2's loaders (fit_x / x_eval executed from na2.py)")
ka3 = {}
for f in A0:
    Fb = NS["fit_x"](f, "baryon"); Fs = NS["fit_x"](f, "stars"); e = NS["x_eval"](f, "stars", Fs); bins = [b["mean"] for b in e["bins"][:3]]
    ref_F = {"canonical": 4.206, "alt": 3.811}[f]; ref_b = {"canonical": (-0.068, 0.089, 0.070), "alt": (-0.059, 0.086, 0.059)}[f]
    ok = abs(Fb / ref_F - 1) <= 0.01 and all(abs(b - r) <= 0.005 for b, r in zip(bins, ref_b))
    ka3[f] = dict(F_baryon=Fb, F_baryon_ref=ref_F, F_stars=Fs, stars_bins=bins, stars_bins_ref=list(ref_b), n_per_bin=[b["n"] for b in e["bins"]], passed=bool(ok))
    P(f"[{f}] baryon-traced F {Fb:.4f} (NA2 {ref_F}); stars-traced F {Fs:.4f}, bins 0-0.25 / 0.25-0.5 / 0.5-0.75: {bins[0]:+.4f} / {bins[1]:+.4f} / {bins[2]:+.4f} (NA2 {ref_b[0]:+.3f} / {ref_b[1]:+.3f} / {ref_b[2]:+.3f}) -> {'PASS' if ok else 'FAIL'}")
P(f"  NA2's X-COP points: {len(XC)} = 7 clusters x r/R500 (0.1, 0.2, 0.3, 0.5, 0.7); HL3's hydrostatic leg uses the full gas-profile grid instead (above).")

# ------------------------------------------------------------------ KA4: HL2 replay (numbers; the Delta_b consistency check is in hl3_grade.py)
P(); P("KA4 HL2 replay")
H2 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "HL2_combined_mass_pairs", "hl2_results.json")))
post = open(os.path.join(REPO, "rebuild_2026_10_22", "HL2_combined_mass_pairs", "hl2_post.out")).read()
m = re.search(r"all three sources: n (\d+), g ([+-][\d.]+) \+- ([\d.]+)", post)
ka4 = dict(json_n=H2["n"], json_g=H2["g"], json_se=H2["se"], json_cls=H2["cls"], post_n=int(m.group(1)), post_g=float(m.group(2)), post_se=float(m.group(3)),
           passed=bool(abs(H2["g"] - 0.031) <= 0.001 and abs(float(m.group(2)) - 0.031) <= 0.001 and abs(float(m.group(3)) - 0.020) <= 0.001))
P(f"hl2_results.json (frozen main read): n {H2['n']}, g = log M_lens - log M_hyd at R500 = {H2['g']:+.4f} +- {H2['se']:.4f}, {H2['cls']}; hl2_post.out all three sources: n {ka4['post_n']}, g {ka4['post_g']:+.3f} +- {ka4['post_se']:.3f} -> {'PASS' if ka4['passed'] else 'FAIL'} (numbers replayed; the Delta_b check waits for the grader)")

KA = dict(KA1=ka1, KA2=ka2, KA3=ka3, KA4=ka4, KA5=ka5)
all_pass = ka1["passed"] and ka2["passed"] and all(v["passed"] for v in ka3.values()) and ka4["passed"] and all(v["pass_hi"] and v["pass_roundtrip"] and v["pass_deep_1e_4"] for v in ka5.values())
P(); P(f"KNOWN ANSWERS: KA1 {'PASS' if ka1['passed'] else 'FAIL'}, KA2 {'PASS' if ka2['passed'] else 'FAIL'}, KA3 {'PASS' if all(v['passed'] for v in ka3.values()) else 'FAIL'}, KA4 {'PASS' if ka4['passed'] else 'FAIL'}, "
  f"KA5 {'PASS (deep end 1 % met from g_N <= 4e-4 a0, 0.5 % at 1e-4 a0; the literal 1e-3 line reads 1.58 %, disclosed)' if all(v['pass_hi'] and v['pass_roundtrip'] and v['pass_deep_1e_4'] for v in ka5.values()) else 'FAIL'} -> {'grade may be read' if all_pass else 'DO NOT READ THE GRADE'}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6; P(f"peak RSS {rss:.0f} MB")
json.dump(dict(footings=A0, mergers=MERGERS, xcop_with_stars=WITH, xcop_without_stars=WITHOUT, bin_edges=[0.0, 0.25, 0.5, 0.75, 1.0, 2.0], lensing=LENS, hydrostatic=HYD, KA=KA, ka_all_pass=bool(all_pass),
               r500_convention="R500 for CLASH from Umetsu+2016 M500c with rho_c(z), h 0.7, Omega_m 0.27, Omega_Lambda 0.73 (Umetsu's stated convention); bracket Donahue+2014 Chandra r500 (h70); X-COP from Ettori 2019 json",
               rss_MB=rss), open(os.path.join(HERE, "hl3_points.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "hl3_points.out"), "w").write("\n".join(OUT) + "\n")
