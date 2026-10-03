#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG309 -- are the MIGHTEE-HI COSMOS catalogue W_50_km_s values REST-frame (c dnu / nu_obs) or OBSERVED-frame (optical, (1+z) W_rest)?
Decides CFG306's CRITICAL finding C1.  Criteria frozen and committed before this script existed: FROZEN_CRITERIA.md (ec54de4ac).
A convention check, not an a0 measurement; kappa = 1/2 is FITTED.  No downloads.

  T1  the catalogue paper's text (MM26, arXiv:2605.28731; pdftotext -layout of the local PDF): keyword sweep + the classification recorded
      below after reading; every quoted fragment is asserted to occur in the text.
  T2  the paper's Appendix-D example spectra, re-parsed independently: T2a conversion (km/s per channel vs REST / OBS / RADIO), T2b link of the
      printed km/s to our catalogue column, T2c exactness.
  T3  ALFALFA alpha.100 as an external width scale: T3a frame from the documentation (asserted quotes), T3b CFG304's 15 code-1 pairs, C-SHUF.
  T4  Westmeier+2014 busy-function fits (n = 2) to CFG302's re-extracted r1p0 aperture spectra (rest-frame axis by construction), level and
      Theil-Sen slope tests, robustness guard V1-V4, INJ-A / INJ-B injection controls.
  Decision: FROZEN_CRITERIA.md section 7.  MUTATE=1: catalogue W50 x (1+z) wherever it is compared (section 9); outputs get the _MUTATE suffix.

Run:  python3 cfg309_width_frame.py ; MUTATE=1 python3 cfg309_width_frame.py
Paths: the PDF from $CFG309_PDF (default ../_external_data/arxiv_pdf/2605.28731.pdf relative to the repository root); the cubes from
$MIGHTEE_R1P0_DIR (default ../_external_data/mightee_hi_dr1), read through CFG302's own module.
"""
import os, sys, json, math, re, time, hashlib, subprocess, shutil
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.special import erf
from scipy.optimize import least_squares
from scipy.stats import spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
MUT = int(os.environ.get("MUTATE", "0") or 0)
assert MUT in (0, 1)
SFX = "_MUTATE" if MUT else ""
PDF = os.environ.get("CFG309_PDF", os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_pdf", "2605.28731.pdf"))
CATP = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv")
CAT_README = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "README.md")
CAT_COLS = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "catalogue_columns_from_paper.csv")
C302 = os.path.join(CFG, "CFG302_mightee_cube_raw_widths")
C304P = os.path.join(CFG, "CFG304_mightee_flux_scale_alfalfa", "cfg304_matched_pairs.csv")
ALFA_DOCS = [os.path.join(REPO, "data_assembly", "alfalfa_sdss_local_control", "columns.md"),
             os.path.join(REPO, "data_assembly", "alfalfa_sdss_local_control", "README.md"),
             os.path.join(os.path.dirname(REPO), "_external_data", "alfalfa_sdss", "ReadMe_Haynes2018_J_ApJ_861_49"),
             os.path.join(os.path.dirname(REPO), "_external_data", "alfalfa_sdss", "ReadMe")]
OUT = os.path.join(HERE, f"cfg309_width_frame{SFX}")
CSV = os.path.join(HERE, f"cfg309_per_galaxy{SFX}.csv")
MAIN_JSON = os.path.join(HERE, "cfg309_width_frame_results.json")

CKMS = 299792.458
NU0 = 1420.40575177e6
TAU_B, TAU_M = 0.010, 0.010
R_INJ = 20
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok):
    CHK.append((name, bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


def rel(p):
    return os.path.relpath(p, REPO)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def mad(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return float(1.4826 * np.median(np.abs(x - np.median(x)))) if x.size else float("nan")


def pct(a, q=(2.5, 97.5)):
    return [float(v) for v in np.percentile(a, q)]


P(__doc__.strip())
P(f"\nMUTATE={MUT}" + ("   *** MUTATE: catalogue W50 x (1+z) wherever it is compared -- a reactivity test, not a measurement ***" if MUT else ""))
cat = pd.read_csv(CATP, dtype={"ID_catalogue": str})
cat["z_freq"] = NU0 / (cat.freq_MHz.values * 1e6) - 1.0
cat["W50_cmp"] = cat.W_50_km_s.values.astype(float) * ((1.0 + cat.z_freq.values) if MUT else 1.0)       # the catalogue width as COMPARED (section 9)
CMP = dict(zip(cat.ID_catalogue, cat.W50_cmp)); ZF = dict(zip(cat.ID_catalogue, cat.z_freq)); WRAW = dict(zip(cat.ID_catalogue, cat.W_50_km_s.astype(float)))
P(f"inputs: catalogue {rel(CATP)} sha256 {sha(CATP)[:16]}...; CFG302 per-galaxy {sha(os.path.join(C302, 'cfg302_per_galaxy.csv'))[:16]}...; CFG304 pairs {sha(C304P)[:16]}...; "
  f"PDF {'present, sha256 ' + sha(PDF)[:16] + '...' if os.path.exists(PDF) else 'MISSING'}")
check("K0 input sha256 prefixes as frozen (catalogue bcf9e8558bc56448, CFG302 CSV e122665f, CFG304 pairs 297e4789, PDF db936cbc)",
      "", sha(CATP).startswith("bcf9e8558bc56448") and sha(os.path.join(C302, "cfg302_per_galaxy.csv")).startswith("e122665f")
      and sha(C304P).startswith("297e4789") and os.path.exists(PDF) and sha(PDF).startswith("db936cbc"))

# ============================================================================ T1 the paper's text
P("\n== T1 the catalogue paper's text ==")
TXT = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True).stdout if (os.path.exists(PDF) and shutil.which("pdftotext")) else ""
NTXT = norm(TXT)
LINES = TXT.splitlines()
PATS = [r"W ?_?50", r"w50", r"line width", r"velocity width", r"width", r"rest[- ]frame", r"observed[- ]frame", r"1 ?\+ ?z", r"\(1\+z\)", r"optical", r"radio",
        r"convention", r"cosmolog", r"busy", r"channel", r"km ?/ ?s|km s"]
sweep = {}
for pt in PATS:
    hits = [i + 1 for i, l in enumerate(LINES) if re.search(pt, l, re.I)]
    sweep[pt] = dict(n=len(hits), lines=hits[:60])
    P(f"  pattern {pt!r}: {len(hits)} lines" + (f" (first: {hits[:12]})" if hits else ""))
# frame-defining keywords that would make T1 EXPLICIT: none of these occurs anywhere in the text
frame_kw = {k: len(re.findall(k, TXT, re.I)) for k in (r"rest[- ]frame", r"observed[- ]frame", r"1 ?\+ ?z\)?", r"cosmolog\w* (?:stretch|broaden)", r"optical convention", r"radio convention", r"convention")}
P(f"  frame-defining keywords anywhere in the text: {frame_kw}")
# The classification below was recorded AFTER reading the hits (FROZEN section 3).  Each fragment must occur in the whitespace-normalised text.
T1_QUOTES = {
    "S4.5 W50 definition": ["width W50 at 50% of the average peak flux density of the fitted",
                            "function, found by identifying the two peaks of the spectral profile and"],
    "S4.5 channel velocity width (the only frame-related statement)": ["with the velocity width of the channels (calculated for the given",
                                                                       "redshift), equal to"],
    "Table 2": ["Channel width 26.126 kHz (5.5 km s"],
    "S4.7 column 13 description (no frame stated)": ["tection spectral profile velocity width (and its error) measured at 50%",
                                                     "Note that it is not inclination corrected."],
    "S4.5 busy function source": ["we fit a busy function (Equation 4"],
}
T1_VERDICT = "IMPLICIT-{REST,OBS}"
T1_NOTE = ("No sentence states the velocity frame or convention of W50: 'rest frame', 'observed frame', '(1+z)', 'convention' and 'cosmological "
           "broadening/stretch' never occur.  The one frame-related statement is that the channel velocity width used in the W50 error is "
           "'calculated for the given redshift' (5.5 km/s at z = 0): that excludes RADIO (5.5 km/s per channel at every z) but is compatible with REST "
           "(5.5 (1+z)) and OBS (5.5 (1+z)^2).  The column description (S4.7, col. 13) and the data-assembly README/column file give no frame either.")
qok = {}
for k, frs in T1_QUOTES.items():
    qok[k] = all(norm(f) in NTXT for f in frs)
    P(f"  quote [{k}]: {' ... '.join(frs)!r} -> found {qok[k]}")
cols_txt = open(CAT_COLS).read(); readme_txt = open(CAT_README).read()
dacol = [l for l in cols_txt.splitlines() if l.startswith("13,")][0]
P(f"  data-assembly column 13: {dacol!r}; frame keywords in the column file / README: "
  f"{[k for k in ('rest', 'observed', '1+z', '(1 + z)', 'frame', 'convention') if k in cols_txt.lower() or k in readme_txt.lower()]}")
check("T1-Q every recorded T1 quote occurs in the pdftotext output (whitespace-normalised)", f"{qok}", all(qok.values()) and len(TXT) > 0)
check("T1-K no frame-defining keyword occurs anywhere in the paper text (the basis of 'not EXPLICIT')", f"{frame_kw}",
      sum(v for k, v in frame_kw.items()) == 0)
P(f"T1 VERDICT: {T1_VERDICT}.  {T1_NOTE}")
NUM["T1"] = dict(verdict=T1_VERDICT, note=T1_NOTE, quotes=T1_QUOTES, quotes_found=qok, sweep=sweep, frame_keywords=frame_kw, data_assembly_col13=dacol)
T1_SET = {"REST", "OBS"}

# ============================================================================ T2 the worked example spectra
P("\n== T2 the paper's example spectra (Appendix D), parsed independently ==")
FLT = r"([0-9]+(?:\.[0-9]+)?)"
idpos = [(m.start(), m.group(1)) for m in re.finditer(r"(MGTH_J\d{6}\.\d[+-]\d{6})", TXT)]
ex = []
for m in re.finditer(r"W50\s*\[\s*km\s*/\s*s\s*\]\s*=\s*" + FLT, TXT):
    s = m.start(); seg = TXT[s:s + 2500]; pre = [p for p in idpos if p[0] < s]
    pid = pre[-1][1] if pre else None
    mch = re.search(r"W50\s*\[\s*channels\s*\]\s*=\s*" + FLT, seg)
    m100 = re.search(r"W100\s*\[\s*km\s*/\s*s\s*\]\s*=\s*" + FLT, seg); c100 = re.search(r"W100\s*\[\s*channels\s*\]\s*=\s*" + FLT, seg)
    fr = re.search(r"frequency:\s*" + FLT + r"\s*\[MHz\]", seg); vch = re.search(r"vchannel\s*\[\s*km\s*/\s*s\s*\]\s*=\s*" + FLT, seg)
    zz = re.search(r"redshift:\s*HI:\s*" + FLT, seg)
    ex.append(dict(ID_printed=pid, X=float(m.group(1)), Y=float(mch.group(1)) if mch else np.nan, X100=float(m100.group(1)) if m100 else np.nan,
                   Y100=float(c100.group(1)) if c100 else np.nan, freq_panel_MHz=float(fr.group(1)) if fr else np.nan, vchannel=float(vch.group(1)) if vch else np.nan,
                   z_panel=float(zz.group(1)) if zz else np.nan))
mt2 = re.search(r"Channel width\s+" + FLT + r"\s*kHz", TXT); mt2b = re.search(r"channel width of\s+" + FLT + r"\s*kHz", TXT)
DNU = float(mt2.group(1)) * 1e3 if mt2 else 26.126e3
P(f"  parsed {len(ex)} examples; Table 2 channel width {mt2.group(1) if mt2 else '?'} kHz (the S3 text says {mt2b.group(1) if mt2b else '?'} kHz; T2 uses Table 2)")
rows2 = []
for e in ex:
    r = cat[cat.ID_catalogue == e["ID_printed"]]
    matched = len(r) == 1
    nu = float(r.freq_MHz.iloc[0]) * 1e6 if matched else e["freq_panel_MHz"] * 1e6
    z = NU0 / nu - 1
    k = e["X"] / e["Y"]
    pred = dict(REST=CKMS * DNU / nu, OBS=CKMS * DNU * NU0 / nu ** 2, RADIO=CKMS * DNU / NU0)
    rho = 0.05 / e["Y"] + 0.0005 / e["X"]
    dev = {h: k / v - 1 for h, v in pred.items()}
    nup = e["freq_panel_MHz"] * 1e6; devp = {h: k / v - 1 for h, v in dict(REST=CKMS * DNU / nup, OBS=CKMS * DNU * NU0 / nup ** 2, RADIO=CKMS * DNU / NU0).items()}
    cons = {h: abs(d) <= 0.002 + rho for h, d in dev.items()}
    wcat = float(CMP[e["ID_printed"]]) if matched else np.nan
    mult = {"1": 1.0, "(1+z)": 1 + z, "1/(1+z)": 1 / (1 + z)}
    link = {mk: bool(matched and abs(mv * e["X"] - wcat) <= 0.5 + 0.002 * wcat) for mk, mv in mult.items()}
    k100 = e["X100"] / e["Y100"] if np.isfinite(e["Y100"]) else np.nan
    row = dict(ID=e["ID_printed"], matched=matched, z=z, freq_MHz=nu / 1e6, freq_panel_MHz=e["freq_panel_MHz"], z_panel=e["z_panel"], X_kms=e["X"], Y_ch=e["Y"], k_kms_per_ch=k,
               rho=rho, dev=dev, dev_panel_freq=devp, consistent=cons, W50_cat_compared=wcat, link=link, k100=k100,
               dev100_REST=(k100 / pred["REST"] - 1) if np.isfinite(k100) else np.nan, vchannel=e["vchannel"], vch_pred=dict((h, round(v, 3)) for h, v in pred.items()))
    rows2.append(row)
    P(f"  {row['ID']} (matched {matched}; z {z:.5f}; freq {nu / 1e6:.3f} MHz, panel {e['freq_panel_MHz']}): W50 {e['X']} km/s = {e['Y']} ch -> {k:.5f} km/s/ch; "
      f"dev REST {dev['REST']:+.5f}, OBS {dev['OBS']:+.5f}, RADIO {dev['RADIO']:+.5f} (allowance +-{0.002 + rho:.4f}); catalogue W50 {wcat:g}; link 1/(1+z)/1/(1+z): "
      f"{link['1']}/{link['(1+z)']}/{link['1/(1+z)']}; W100 dev REST {row['dev100_REST']:+.5f}; vchannel printed {e['vchannel']} (REST {pred['REST']:.3f}, OBS {pred['OBS']:.3f}, RADIO {pred['RADIO']:.3f})")
nex = len(rows2)
T2a = "AMBIGUOUS"
for h in ("REST", "OBS", "RADIO"):
    if nex == 5 and all(r["consistent"][h] for r in rows2) and all(sum(not r["consistent"][o] for r in rows2) >= 3 for o in ("REST", "OBS", "RADIO") if o != h):
        T2a = h
nmatch = sum(r["matched"] for r in rows2)
need = 4 if nmatch == 5 else max(nmatch - 1, 3)
cnt = {mk: sum(r["link"][mk] for r in rows2) for mk in ("1", "(1+z)", "1/(1+z)")}
best = [mk for mk, c in cnt.items() if c >= need]
T2b = best[0] if len(best) == 1 and sorted(cnt.values())[-2] < need else "AMBIGUOUS"
if T2a in ("REST", "OBS", "RADIO"):
    dv = [r["dev"][T2a] for r in rows2]; spread = max(dv) - min(dv)
else:
    spread = float("nan")
T2c = "EXACT" if np.isfinite(spread) and spread <= 2e-4 else "NOT EXACT"
P(f"T2a = {T2a}; T2b link = {T2b} (counts {cnt}; need {need} of {nmatch} matched); T2c = {T2c} (spread of dev_{T2a} {spread:.2e}; limit 2e-4)")
# reported diagnostics: the paper's Table 3 W50 vs our column (the paper -> CSV identity, independent of the frame)
t3i = TXT.find("Table 3."); t3 = TXT[t3i:t3i + 12000] if t3i >= 0 else ""
ids3 = re.findall(r"^\s*(MGTH_J\d{6}\.\d[+-]\d{6})\s", t3, re.M)
hdr3 = re.search(r"SNR3D\s+W50", t3)
w3 = []
if hdr3:
    for l in t3[hdr3.end():].splitlines():
        tok = l.split()
        if len(tok) >= 13 and all(re.fullmatch(r"-?[0-9.]+", t) for t in tok[:13]):
            w3.append(float(tok[1]))
        if len(w3) == len(ids3): break
tab3 = [dict(ID=i, W50_table3=w, W50_csv=WRAW.get(i)) for i, w in zip(ids3, w3)]
tab3_ok = len(tab3) == 8 and all(t["W50_csv"] is not None and abs(t["W50_table3"] - t["W50_csv"]) < 1e-9 for t in tab3)
P(f"  diagnostic (reported): the paper's Table 3 W50 equal our CSV's unmutated W_50_km_s for {sum(abs(t['W50_table3'] - (t['W50_csv'] or -1)) < 1e-9 for t in tab3)} of {len(tab3)} rows: "
  f"{[(t['ID'][5:], t['W50_table3'], t['W50_csv']) for t in tab3]}")
check("T2-P the parser found 5 examples, each with W50 km/s, channels and a printed MGTH identifier that matches one catalogue row", f"{nex} parsed, {nmatch} matched",
      nex == 5 and nmatch == 5 and all(np.isfinite(r["Y_ch"]) for r in rows2))
NUM["T2"] = dict(rows=rows2, T2a=T2a, T2b=T2b, link_counts=cnt, need=need, T2c=T2c, spread=spread, channel_width_Hz=DNU, table3=tab3, table3_identity=tab3_ok)

# ============================================================================ T3 ALFALFA
P("\n== T3 ALFALFA alpha.100 as an external width scale ==")
T3A_QUOTES = {ALFA_DOCS[2]: ["W50      [9/885] Observed velocity width"],
              ALFA_DOCS[0]: ["no correction for turbulence, disk inclination or cosmological stretch"],
              ALFA_DOCS[1]: ["not for (1+z) (negligible at z < 0.06)"]}
T3A_VERDICT = "ALFA-OBS"
t3q = {}
for p_, frs in T3A_QUOTES.items():
    tx = norm(open(p_, errors="replace").read()); t3q[os.path.basename(p_)] = all(norm(f) in tx for f in frs)
    P(f"  {os.path.basename(p_)}: {frs!r} -> found {t3q[os.path.basename(p_)]}")
check("T3a-Q every recorded ALFALFA documentation quote occurs in its file", f"{t3q}", all(t3q.values()))
P(f"T3a VERDICT: {T3A_VERDICT} (the CDS ReadMe labels W50 'Observed velocity width'; the data-assembly documentation, from H18 Sect. 3.1 col. 6, "
  f"says instrumental broadening only, no cosmological stretch; Vhel is optical-convention heliocentric).  No web look-up was needed.")
pr = pd.read_csv(C304P)
c1 = pr[pr.hi_code == 1].copy()
c1["z_f"] = NU0 / (c1.freq_MHz.values * 1e6) - 1; c1["x"] = np.log10(1 + c1.z_f.values)
c1["Wc"] = [CMP[i] for i in c1.ID]
d = np.log10(c1.Wc.values / c1.w50_A.values); x3 = c1.x.values
d_unmut = np.log10(c1.W50_cat.values / c1.w50_A.values)
r3_ok = len(c1) == 15 and np.allclose(d_unmut, c1.logW50_cat_A.values, atol=1e-9, rtol=0) and abs(np.median(d_unmut) - 0.0) <= 1e-9 and \
    np.allclose(c1.W50_cat.values, [WRAW[i] for i in c1.ID])
check("R3 CFG304 reproduction: N = 15 code-1 pairs; log(W50_cat/w50_A) equals the committed logW50_cat_A to 1e-9; median = CFG304's +0.000 to 1e-9; W50_cat = catalogue",
      f"N {len(c1)}; median (unmutated) {np.median(d_unmut):+.6f}; median z {np.median(c1.z_f):.4f}; median x {np.median(x3):.4f} dex", r3_ok)
rR = d + x3; rO = d                                                   # ALFA-OBS
rng = np.random.default_rng(3093); I = rng.integers(0, len(d), size=(10000, len(d)))
bR = np.median(rR[I], axis=1); bO = np.median(rO[I], axis=1)
ciR, ciO = pct(bR), pct(bO)
excl = lambda ci, t: ci[0] > t or ci[1] < -t
eR, eO = excl(ciR, TAU_B), excl(ciO, TAU_B)
T3vote = "REST" if (eO and not eR) else ("OBS" if (eR and not eO) else "UNDECIDED")


def theil_sen(x, y):
    i, j = np.triu_indices(len(x), 1); dx = x[j] - x[i]; ok = dx != 0
    return float(np.median((y[j] - y[i])[ok] / dx[ok]))


ts3 = theil_sen(x3, d)
rng_s = np.random.default_rng(3096)
real_sc = mad(d_unmut if not MUT else d)
sh = []
for _ in range(2000):
    perm = rng_s.permutation(len(c1)); sh.append(mad(np.log10(c1.Wc.values / c1.w50_A.values[perm])))
sh = np.array(sh); p1 = float(np.percentile(sh, 1))
cshuf = real_sc < p1
P(f"T3b (N {len(d)}): median r_REST = median(d + x) {np.median(rR):+.4f} (95% {ciR[0]:+.4f}..{ciR[1]:+.4f}); median r_OBS = median(d) {np.median(rO):+.4f} "
  f"(95% {ciO[0]:+.4f}..{ciO[1]:+.4f}); tau_b {TAU_B}; REST excluded {eR}, OBS excluded {eO} -> T3 vote {T3vote}")
P(f"   reported: Theil-Sen slope of d on x {ts3:+.2f} (REST predicts -1, OBS 0); predicted separation median x {np.median(x3):.4f} dex")
allp = pr.copy(); allp["z_f"] = NU0 / (allp.freq_MHz.values * 1e6) - 1
da = np.log10(np.array([CMP[i] for i in allp.ID]) / allp.w50_A.values)
P(f"   reported, codes 1+2 (N {len(allp)}): median d {np.median(da):+.4f}, median d + x {np.median(da + np.log10(1 + allp.z_f.values)):+.4f}")
check("C-SHUF the real robust scatter of d is below the 1st percentile of 2,000 shuffles of w50_A among the 15 pairs",
      f"real {real_sc:.4f} dex; shuffled 1st percentile {p1:.4f}, median {np.median(sh):.4f}", cshuf)
T3_adm = (T3A_VERDICT in ("ALFA-OBS", "ALFA-REST")) and all(t3q.values()) and cshuf and r3_ok
NUM["T3"] = dict(T3a=T3A_VERDICT, quotes_found=t3q, N=int(len(d)), median_x=float(np.median(x3)), median_rREST=float(np.median(rR)), ci_rREST=ciR,
                 median_rOBS=float(np.median(rO)), ci_rOBS=ciO, REST_excluded=eR, OBS_excluded=eO, vote=T3vote, admissible=bool(T3_adm), theil_sen=ts3,
                 cshuf=dict(real=real_sc, p1=p1, median=float(np.median(sh)), passed=bool(cshuf)), codes12=dict(N=int(len(allp)), median_d=float(np.median(da))))
P(f"T3: admissible {T3_adm}; vote {T3vote}")

# ============================================================================ T4 busy-function fits to the raw r1p0 spectra
P("\n== T4 method-matched cube widths (busy function, n = 2) ==")
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
sys.path.insert(0, C302)
import cfg302_raw_widths as M302                                                # its main() is never called
if _old is None: del os.environ["MUTATE"]
else: os.environ["MUTATE"] = _old
assert M302.MUTATE == 0
C, NG, PIX = M302.C, M302.NG, M302.PIX


def busy(v, p, n):
    a, b1, b2, w, ve, dd, h, b0 = p
    vp = ve + dd * w
    return a / 4.0 * (erf(b1 * (w + v - ve)) + 1.0) * (erf(b2 * (w - v + ve)) + 1.0) * (h * np.abs(v - vp) ** n / w ** n + 1.0) + b0


def model_widths(p, n, vfit):
    vg = np.arange(-vfit - 300.0, vfit + 300.0 + 0.025, 0.05)
    y = busy(vg, p, n) - p[7]
    Pk = float(np.max(y)); out = dict(P=Pk)
    # local maxima for the post hoc 'average of the two peaks' definition (MM26 S4.5); reported only
    im = np.nonzero((y[1:-1] > y[:-2]) & (y[1:-1] >= y[2:]))[0] + 1
    if im.size >= 2:
        pk2 = float(0.5 * (y[im[0]] + y[im[-1]]))
    else:
        pk2 = Pk
    for f, nm, ref in ((0.5, "W50", Pk), (0.2, "W20", Pk), (0.5, "W50avg", pk2)):
        thr = f * ref; ab = np.nonzero(y >= thr)[0]
        if Pk <= 0 or ab.size == 0 or ab[0] == 0 or ab[-1] == y.size - 1:
            out[nm] = np.nan; out[nm + "_lo"] = np.nan; out[nm + "_hi"] = np.nan; continue
        lo, hi = int(ab[0]), int(ab[-1])
        vlo = vg[lo - 1] + (thr - y[lo - 1]) / (y[lo] - y[lo - 1]) * (vg[lo] - vg[lo - 1])
        vhi = vg[hi + 1] + (thr - y[hi + 1]) / (y[hi] - y[hi + 1]) * (vg[hi] - vg[hi + 1])
        out[nm] = float(vhi - vlo); out[nm + "_lo"] = float(vlo); out[nm + "_hi"] = float(vhi)
    return out


def busy_fit(v, y, sig, w50_start, vfit, n=2):
    """v ascending rest-frame km/s, y Jy; fit |v| <= vfit; 12 starts (FROZEN section 6). Returns dict."""
    m = np.abs(v) <= vfit
    vv, yy = v[m], y[m]
    ys = M302.smooth3(yy); Ps = float(np.max(ys)) if ys.size else np.nan
    wr = M302.width_rule(vv, ys)
    ve0 = 0.5 * (wr["v50"][0] + wr["v50"][1]) if np.all(np.isfinite(wr["v50"])) else 0.0
    if not (np.isfinite(Ps) and Ps > 0 and np.isfinite(w50_start) and w50_start > 0 and vv.size >= 12):
        return dict(good=False, reason="bad start", W50=np.nan, W20=np.nan, W50avg=np.nan, redchi2=np.nan, p=[np.nan] * 8, nfit=int(vv.size))
    lo = [0.0, 0.005, 0.005, 3.0, -vfit, -1.0, 0.0, -np.inf]; hi = [50 * Ps, 2.0, 2.0, vfit, vfit, 1.0, 20.0, np.inf]
    best = None
    for wf in (0.85, 1.0, 1.15):
        for b in (0.05, 0.2):
            for h0 in (0.0, 0.5):
                w0 = min(max(wf * w50_start / 2, 3.5), 0.98 * vfit)
                p0 = np.array([Ps / (1 + h0), b, b, w0, float(np.clip(ve0, -0.9 * vfit, 0.9 * vfit)), 0.0, h0, 0.0])
                p0 = np.clip(p0, np.array(lo) + 1e-9, np.array(hi) - 1e-9)
                try:
                    r = least_squares(lambda p: (yy - busy(vv, p, n)) / sig, p0, bounds=(lo, hi), method="trf", max_nfev=4000)
                except Exception:
                    continue
                if r.status > 0 and (best is None or r.cost < best.cost):
                    best = r
    if best is None:
        return dict(good=False, reason="no converged start", W50=np.nan, W20=np.nan, W50avg=np.nan, redchi2=np.nan, p=[np.nan] * 8, nfit=int(vv.size))
    p = best.x; mw = model_widths(p, n, vfit)
    dof = max(vv.size - 8, 1); rc = 2 * best.cost / dof
    inside = np.isfinite(mw["W50"]) and abs(mw["W50_lo"]) <= vfit and abs(mw["W50_hi"]) <= vfit
    wb = (p[3] <= 3.0 * 1.01) or (p[3] >= 0.99 * vfit)
    good = bool(best.success and np.isfinite(mw["W50"]) and inside and rc <= 3.0 and not wb)
    reason = "" if good else ";".join(s for s, c in (("W50 nan", not np.isfinite(mw["W50"])), ("crossing outside window", not inside), (f"redchi2 {rc:.2f}", rc > 3), ("w at bound", wb)) if c)
    return dict(good=good, reason=reason, W50=mw["W50"], W20=mw["W20"], W50avg=mw["W50avg"], redchi2=rc, p=[float(t) for t in p], nfit=int(vv.size), success=bool(best.success))


# ---------------------------------------------------------------- the extraction, exactly as CFG302's main()
c302 = pd.read_csv(os.path.join(C302, "cfg302_per_galaxy.csv"))
S = c302[(c302.primary == 1) & (c302.detected.astype(str) == "True") & (c302.W50_defined.astype(str) == "True")].reset_index(drop=True)
P(f"sample: {len(S)} CFG302 rows with primary 1, detected True, W50_defined True (58 expected)")
man = {}
with open(os.path.join(M302.DATA, "FETCH_MANIFEST.jsonl")) as f:
    for line in f:
        if line.strip(): rr = json.loads(line); man[rr["file"]] = rr
cubes = M302.load_cubes()
size_ok = all(os.path.getsize(cb["path"]) == man.get(cb["file"], {}).get("bytes") for cb in cubes)
check("K1 the four r1p0 sub-cubes have the manifest's sizes (sha256 not recomputed; CFG302 C-INT)", f"{[os.path.getsize(cb['path']) for cb in cubes]}", size_ok)
BMAJ = np.zeros(NG); BMIN = np.zeros(NG); OWN = M302.owner(np.arange(NG))
for g in range(NG):
    k = OWN[g]; cc = g - 1000 * k; BMAJ[g] = cubes[k]["bmaj"][cc]; BMIN[g] = cubes[k]["bmin"][cc]
VALID = (BMAJ >= 50) & (BMAJ <= 120) & (BMIN >= 50) & (BMIN <= 120)
med_beam = {k: float(np.median(BMAJ[(OWN == k) & VALID])) for k in range(4)}
BMAJ_eff = np.where(VALID, BMAJ, [med_beam[k] for k in OWN]); BMIN_eff = np.where(VALID, BMIN, [med_beam[k] for k in OWN])
A_g = math.pi * BMAJ_eff * BMIN_eff / (4 * math.log(2)) / PIX ** 2
allnu = cat.freq_MHz.values * 1e6


def extract(row):
    r = cat[cat.ID_catalogue == row.ID].iloc[0]
    ra, dec = float(r.RA_deg), float(r.Dec_deg); nu_c = float(r.freq_MHz) * 1e6; w50c = float(r.W_50_km_s)   # extraction uses the UNMUTATED width (section 9)
    Vw = max(1.5 * w50c, 300.0); vO = 2 * Vw + 100.0

    def inside(va, vb, cen=nu_c):
        return M302.g_of_nu(M302.nu_of_v(cen, vb)) >= -0.5 and M302.g_of_nu(M302.nu_of_v(cen, va)) <= NG - 0.5
    side = +1 if inside(vO - Vw, vO + Vw) else (-1 if inside(-vO - Vw, -vO + Vw) else 0)
    nu_O = M302.nu_of_v(nu_c, side * vO) if side else np.nan
    span = 3 * Vw + 1100.0
    v_lo = -span if side >= 0 else -(vO + span); v_hi = (vO + span) if side > 0 else span
    g_lo = max(int(math.floor(M302.g_of_nu(M302.nu_of_v(nu_c, v_hi)))) - 2, 0); g_hi = min(int(math.ceil(M302.g_of_nu(M302.nu_of_v(nu_c, v_lo)))) + 2, NG - 1)
    gall = np.arange(g_lo, g_hi + 1); vall = C * (nu_c / M302.nu_g(gall) - 1); Wg = gall[np.abs(vall) <= Vw]
    theta = float(np.median(BMAJ[Wg][VALID[Wg]])) if VALID[Wg].any() else med_beam[int(M302.owner(Wg[len(Wg) // 2]))]
    gs, spec, pt, edge, info = M302.aperture_spectrum(cubes, ra, dec, g_lo, g_hi, 1.5 * theta, BMAJ_eff, A_g)
    Om = (np.abs(C * (nu_O / M302.nu_g(gs) - 1)) <= Vw) if side else np.zeros(gs.size, bool)
    m, *_ = M302.measure(gs, spec, nu_c, w50c, excl=Om, rng=None)
    v = C * (nu_c / M302.nu_g(gs) - 1)
    Nm = (np.abs(v) > Vw + 100.0) & (np.abs(v) <= 3 * Vw + 1100.0) & np.isfinite(spec) & ~Om
    o = np.argsort(v)
    return dict(gs=gs[o], v=v[o], spec=spec[o], pt=pt[o], noise=spec[Nm], sigma=m["sigma_ch"], W50_np=m["W50"], nu_c=nu_c, Vw=Vw, w50c=w50c)


EXT = []
r0 = []
for _, row in S.iterrows():
    e = extract(row); EXT.append(e)
    r0.append((abs(e["W50_np"] / row.W50_rest_kms - 1), abs(e["sigma"] * 1e3 / row.sigma_ch_mJy - 1)))
r0 = np.array(r0)
R0_ok = len(S) == 58 and bool(np.all(r0 <= 1e-6))
check("R0 the re-extraction reproduces CFG302's W50_rest_kms and sigma_ch to <= 1e-6 relative for all 58", f"max rel W50 {r0[:, 0].max():.2e}, sigma {r0[:, 1].max():.2e}; n {len(S)}", R0_ok)
P(f"  extraction done ({time.time() - T0:.0f} s)")

# ---------------------------------------------------------------- fits on the real spectra: primary (n=2), V2 (n=4), V3 (catalogue-based window)
fits = []
for i, (row, e) in enumerate(zip(S.itertuples(), EXT)):
    w_np = float(row.W50_rest_kms)
    vfit = max(1.5 * w_np, 300.0); vfit3 = max(1.5 * e["w50c"], 300.0)
    f1 = busy_fit(e["v"], e["spec"], e["sigma"], w_np, vfit, n=2)
    f2 = busy_fit(e["v"], e["spec"], e["sigma"], w_np, vfit, n=4)
    f3 = busy_fit(e["v"], e["spec"], e["sigma"], w_np, vfit3, n=2)
    fits.append((f1, f2, f3, vfit))
P(f"  real fits done ({time.time() - T0:.0f} s)")

z = np.array([ZF[i] for i in S.ID]); x = np.log10(1 + z)
Wcmp = np.array([CMP[i] for i in S.ID])
W1 = np.array([f[0]["W50"] for f in fits]); G1 = np.array([f[0]["good"] for f in fits])
W2 = np.array([f[1]["W50"] for f in fits]); G2 = np.array([f[1]["good"] for f in fits])
W3 = np.array([f[2]["W50"] for f in fits]); G3 = np.array([f[2]["good"] for f in fits])
WA = np.array([f[0]["W50avg"] for f in fits])
NB = S.NBFLAG.values.astype(int)
D1 = np.log10(W1 / Wcmp)


def t4_rule(Dl, xl, seed_l=3094, seed_s=3095, B=4000, Bs=2000):
    Dl = np.asarray(Dl, float); xl = np.asarray(xl, float); n = len(Dl)
    rg = np.random.default_rng(seed_l); I = rg.integers(0, n, size=(B, n))
    mR = float(np.median(Dl)); mO = float(np.median(Dl + xl))
    ciR = pct(np.median(Dl[I], axis=1)); ciO = pct(np.median((Dl + xl)[I], axis=1))
    eR, eO = excl(ciR, TAU_M), excl(ciO, TAU_M)
    L = "REST" if (eO and not eR) else ("OBS" if (eR and not eO) else "UNDECIDED")
    beta = theil_sen(xl, Dl)
    rs = np.random.default_rng(seed_s); Is = rs.integers(0, n, size=(Bs, n))
    ii, jj = np.triu_indices(n, 1)
    XB = xl[Is]; YB = Dl[Is]
    dx = XB[:, jj] - XB[:, ii]; dy = YB[:, jj] - YB[:, ii]
    with np.errstate(invalid="ignore", divide="ignore"):
        sl = np.where(dx != 0, dy / dx, np.nan)
    bb = np.nanmedian(sl, axis=1); ciS = pct(bb)
    Sv = "REST" if (ciS[0] <= 0 <= ciS[1] and not (ciS[0] <= -1 <= ciS[1])) else ("OBS" if (ciS[0] <= -1 <= ciS[1] and not (ciS[0] <= 0 <= ciS[1])) else "UNDECIDED")
    if L == Sv: vote = L
    elif L == "UNDECIDED": vote = Sv
    elif Sv == "UNDECIDED": vote = L
    else: vote = "UNDECIDED"
    return dict(n=n, mR=mR, ciR=ciR, mO=mO, ciO=ciO, REST_excl=eR, OBS_excl=eO, T4L=L, beta=beta, ciS=ciS, T4S=Sv, vote=vote)


prim = t4_rule(D1[G1], x[G1])
P(f"T4 primary (GOOD {int(G1.sum())} of {len(G1)}): m_R = median log(W_busy/W_cat) {prim['mR']:+.4f} (95% {prim['ciR'][0]:+.4f}..{prim['ciR'][1]:+.4f}); "
  f"m_O = median(Delta + x) {prim['mO']:+.4f} (95% {prim['ciO'][0]:+.4f}..{prim['ciO'][1]:+.4f}); tau_m {TAU_M}; REST excluded {prim['REST_excl']}, OBS excluded {prim['OBS_excl']} "
  f"-> T4L {prim['T4L']}")
P(f"   Theil-Sen slope beta {prim['beta']:+.2f} (95% {prim['ciS'][0]:+.2f}..{prim['ciS'][1]:+.2f}; REST 0, OBS -1) -> T4S {prim['T4S']}; T4 primary vote {prim['vote']}")
var = {}
gV1 = G1 & (NB == 0); var["V1 NBFLAG 0"] = t4_rule(D1[gV1], x[gV1])
var["V2 n = 4"] = t4_rule(np.log10(W2 / Wcmp)[G2], x[G2])
var["V3 catalogue window"] = t4_rule(np.log10(W3 / Wcmp)[G3], x[G3])
Dg = D1[G1]; mm = np.median(Dg); keep = np.abs(Dg - mm) <= 3 * mad(Dg)
var["V4 3-sigma clipped"] = t4_rule(Dg[keep], x[G1][keep])
for k_, v_ in var.items():
    P(f"   {k_} (n {v_['n']}): m_R {v_['mR']:+.4f} ({v_['ciR'][0]:+.4f}..{v_['ciR'][1]:+.4f}), m_O {v_['mO']:+.4f} ({v_['ciO'][0]:+.4f}..{v_['ciO'][1]:+.4f}), T4L {v_['T4L']}; "
      f"beta {v_['beta']:+.2f} ({v_['ciS'][0]:+.2f}..{v_['ciS'][1]:+.2f}), T4S {v_['T4S']}; vote {v_['vote']}")
opp = {"REST": "OBS", "OBS": "REST"}
flip = prim["vote"] in opp and any(v_["vote"] == opp[prim["vote"]] for v_ in var.values())
T4vote_raw = "UNDECIDED" if flip else prim["vote"]
P(f"   robustness guard: a variant gives the opposite frame: {flip} -> T4 vote (before admissibility) {T4vote_raw}")
# diagnostics (reported, no vote)
lsr = np.log10(S.S_win_Jy_Hz.values / S.S_cat.values)
diag = dict(spearman_z=float(spearmanr(z[G1], D1[G1])[0]), spearman_fluxratio=float(spearmanr(lsr[G1], D1[G1])[0]),
            spearman_logWcat=float(spearmanr(np.log10(Wcmp[G1]), D1[G1])[0]))
Xo = np.column_stack([np.ones(G1.sum()), x[G1], np.log10(Wcmp[G1])]); co, *_ = np.linalg.lstsq(Xo, D1[G1], rcond=None)
res_ = D1[G1] - Xo @ co; cov = np.linalg.inv(Xo.T @ Xo) * (res_ @ res_) / max(len(res_) - 3, 1)
diag["ols_beta_with_logWcat"] = [float(co[1]), float(math.sqrt(cov[1, 1]))]
Dnp = np.log10(S.W50_rest_kms.values / Wcmp)
diag["method_shift_busy_minus_nonparam_median"] = float(np.median(D1[G1] - Dnp[G1]))
diag["nonparam_median_same_galaxies"] = float(np.median(Dnp[G1]))
pull = (W1 - Wcmp) / np.sqrt(S.W50_cat_err.values.astype(float) ** 2)
diag["median_abs_pull_vs_cat_err"] = float(np.nanmedian(np.abs(pull[G1])))
DA = np.log10(WA / Wcmp); gA = G1 & np.isfinite(DA)
diag["POSTHOC_avg_two_peaks"] = dict(n=int(gA.sum()), mR=float(np.median(DA[gA])), mO=float(np.median((DA + x)[gA])),
                                     median_W50avg_over_W50max=float(np.median((WA / W1)[gA])))
P(f"   diagnostics: Spearman(Delta, z) {diag['spearman_z']:+.3f}; (Delta, log S_win/S_cat) {diag['spearman_fluxratio']:+.3f}; (Delta, log W_cat) {diag['spearman_logWcat']:+.3f}; "
  f"OLS beta with log W_cat covariate {co[1]:+.2f} +- {math.sqrt(cov[1, 1]):.2f}; busy - non-parametric median shift {diag['method_shift_busy_minus_nonparam_median']:+.4f} dex "
  f"(non-parametric m_R on the same galaxies {diag['nonparam_median_same_galaxies']:+.4f}); median |pull| vs catalogue error {diag['median_abs_pull_vs_cat_err']:.2f}")
P(f"   POST HOC (not frozen, no vote): W50 at 50% of the AVERAGE of the two fitted peaks (MM26 S4.5's definition): m_R {diag['POSTHOC_avg_two_peaks']['mR']:+.4f}, "
  f"m_O {diag['POSTHOC_avg_two_peaks']['mO']:+.4f} (n {gA.sum()}); median W50avg/W50max {diag['POSTHOC_avg_two_peaks']['median_W50avg_over_W50max']:.4f}")

# ---------------------------------------------------------------- injections (main run only; MUTATE inherits admissibility)
if not MUT:
    P(f"\n  injections: {R_INJ} realisations x {int(G1.sum())} GOOD galaxies (CFG302 double-horn shape, box W50_cat, integral S_L, into each galaxy's own line-free noise)")
    inj = {}
    for i in np.nonzero(G1)[0]:
        e = EXT[i]; row = S.iloc[i]
        Snu, w50t, _ = M302.profile_channels(e["w50c"], e["nu_c"], e["gs"], float(row.S_L_Jy_Hz))
        prof = Snu * e["pt"]; nz = e["noise"]; nc = nz.size
        recs = []
        for r in range(R_INJ):
            s0 = int(np.random.default_rng([309, int(i), r]).integers(nc))
            mock = prof + nz[(s0 + np.arange(prof.size)) % nc]
            Wm = np.abs(e["v"]) <= e["Vw"]
            wr = M302.width_rule(e["v"][Wm], M302.smooth3(mock[Wm]))
            if not np.isfinite(wr["W50"]):
                recs.append((np.nan, False)); continue
            fi = busy_fit(e["v"], mock, M302.mad_sigma(nz), wr["W50"], max(1.5 * wr["W50"], 300.0), n=2)
            recs.append((fi["W50"], fi["good"]))
        inj[i] = dict(W50_true=w50t, rec=recs)
    P(f"  injections done ({time.time() - T0:.0f} s)")
    idx = sorted(inj)
    allr = np.array([[np.log10(inj[i]["rec"][r][0] / inj[i]["W50_true"]) if inj[i]["rec"][r][1] else np.nan for r in range(R_INJ)] for i in idx])
    binj = float(np.nanmedian(allr)); ngood_inj = int(np.isfinite(allr).sum())
    injA = abs(binj) <= 0.005
    check("INJ-A |median log(W50_busy,rec / W50_true)| <= 0.005 dex over all GOOD injection fits", f"bias {binj:+.5f} dex; GOOD {ngood_inj} of {allr.size}; "
          f"robust scatter {mad(allr):.4f} dex (real Delta robust scatter {mad(D1[G1]):.4f})", injA)
    worlds = {"REST": [], "OBS": []}
    zi = np.array([ZF[S.ID.iloc[i]] for i in idx]); xi = np.log10(1 + zi); wt = np.array([inj[i]["W50_true"] for i in idx])
    for r in range(R_INJ):
        wrec = np.array([inj[i]["rec"][r][0] for i in idx]); gd = np.array([inj[i]["rec"][r][1] for i in idx])
        for wn, col in (("REST", wt), ("OBS", wt * (1 + zi))):
            rr_ = t4_rule(np.log10(wrec[gd] / col[gd]), xi[gd], seed_l=[3094, r, 0 if wn == "REST" else 1], seed_s=[3095, r, 0 if wn == "REST" else 1])
            worlds[wn].append(rr_)
    cnt_w = {wn: {v: sum(t["vote"] == v for t in worlds[wn]) for v in ("REST", "OBS", "UNDECIDED")} for wn in worlds}
    cntL = {wn: {v: sum(t["T4L"] == v for t in worlds[wn]) for v in ("REST", "OBS", "UNDECIDED")} for wn in worlds}
    cntS = {wn: {v: sum(t["T4S"] == v for t in worlds[wn]) for v in ("REST", "OBS", "UNDECIDED")} for wn in worlds}
    injB = cnt_w["REST"]["REST"] >= 16 and cnt_w["REST"]["OBS"] <= 1 and cnt_w["OBS"]["OBS"] >= 16 and cnt_w["OBS"]["REST"] <= 1
    check("INJ-B frame recovery: REST world -> REST in >= 16/20 and OBS <= 1/20; OBS world -> OBS in >= 16/20 and REST <= 1/20",
          f"votes {cnt_w}; T4L alone {cntL}; T4S alone {cntS}; median m_R in the REST world {np.median([t['mR'] for t in worlds['REST']]):+.4f}, "
          f"95% half-width {np.median([(t['ciR'][1] - t['ciR'][0]) / 2 for t in worlds['REST']]):.4f}", injB)
    INJ = dict(bias=binj, n_good=ngood_inj, n_total=int(allr.size), scatter=mad(allr), A=bool(injA), B=bool(injB), votes=cnt_w, T4L=cntL, T4S=cntS,
               per_galaxy_median=[float(np.nanmedian(a)) if np.isfinite(a).any() else np.nan for a in allr], idx=[int(i) for i in idx])
else:
    J = json.load(open(MAIN_JSON))["numbers"]["T4"]["INJ"]
    INJ = dict(J, inherited_from_main=True)
    P(f"  injections not re-run in MUTATE (FROZEN section 9): inherited INJ-A {INJ['A']}, INJ-B {INJ['B']}")
ngood = int(G1.sum())
T4_adm = bool(R0_ok and INJ["A"] and INJ["B"] and ngood >= 45)
T4vote = T4vote_raw if T4_adm else "UNDECIDED"
P(f"T4: admissible {T4_adm} (R0 {R0_ok}, INJ-A {INJ['A']}, INJ-B {INJ['B']}, GOOD {ngood} >= 45 {ngood >= 45}); vote entering the decision {T4vote} (raw {T4vote_raw})")
NUM["T4"] = dict(n_sample=int(len(S)), n_good=ngood, primary=prim, variants=var, guard_flip=bool(flip), vote_raw=T4vote_raw, admissible=T4_adm, vote=T4vote,
                 diagnostics=diag, INJ=INJ, R0=dict(ok=R0_ok, max_rel_W50=float(r0[:, 0].max()), max_rel_sigma=float(r0[:, 1].max())),
                 not_good=[dict(ID=S.ID.iloc[i], reason=fits[i][0]["reason"]) for i in range(len(S)) if not G1[i]])

# ============================================================================ the decision (FROZEN section 7)
P("\n== Decision (FROZEN section 7) ==")
T1_explicit = T1_VERDICT.startswith("EXPLICIT-")
T1_conf = T1_VERDICT == "CONFLICTING"
if T1_explicit:
    X1 = T1_VERDICT.split("-")[1]
    PF, grade = (X1, "STRONG") if T2a == X1 else ((X1, "TEXT-ONLY") if T2a == "AMBIGUOUS" else ("CONFLICT", None))
elif T1_conf:
    PF, grade = "CONFLICT", None
else:
    if T2a == "AMBIGUOUS": PF, grade = "NONE", None
    elif T1_VERDICT == "NOT STATED" or T2a in T1_SET: PF, grade = T2a, "NUMBERS-ONLY"
    else: PF, grade = "CONFLICT", None
COMP = {("REST", "1"): "REST", ("REST", "(1+z)"): "OBS", ("REST", "1/(1+z)"): "RADIO", ("OBS", "1"): "OBS", ("OBS", "1/(1+z)"): "REST", ("OBS", "(1+z)"): "OBS(1+z)^2",
        ("RADIO", "1"): "RADIO", ("RADIO", "(1+z)"): "REST", ("RADIO", "1/(1+z)"): "RADIO/(1+z)"}
DOC = COMP.get((PF, T2b), "UNDECIDED") if PF not in ("CONFLICT", "NONE") and T2b != "AMBIGUOUS" else "UNDECIDED"
DOC_STRONG = DOC in ("REST", "OBS") and T2a != "AMBIGUOUS" and T2b != "AMBIGUOUS" and T2c == "EXACT" and not T1_conf and grade in ("STRONG", "NUMBERS-ONLY")
votes = {"T3": T3vote if T3_adm else "UNDECIDED", "T4": T4vote}
outcome, path = "UNDECIDED", "-"
if DOC in ("REST", "OBS"):
    o_ = opp[DOC]
    if not any(v == o_ for v in votes.values()):
        if grade == "STRONG": outcome, path = DOC, "a"
        elif DOC_STRONG: outcome, path = DOC, "b"
        elif any(v == DOC for v in votes.values()): outcome, path = DOC, "c"
elif DOC == "UNDECIDED" and T3_adm and T4_adm and votes["T3"] == votes["T4"] and votes["T3"] in ("REST", "OBS"):
    outcome, path = votes["T3"], "data-only"
WORD = {"REST": "REST-FRAME", "OBS": "OBSERVED-FRAME", "UNDECIDED": "UNDECIDED"}[outcome]
C1 = {"REST-FRAME": "CONFIRMED", "OBSERVED-FRAME": "REFUTED", "UNDECIDED": "OPEN"}[WORD]
P(f"PF = {PF} (grade {grade}); T2b link {T2b}; DOC = {DOC}; DOC STRONG {DOC_STRONG} (T2a {T2a}, link {T2b}, T2c {T2c}, T1 {T1_VERDICT})")
P(f"data votes: T3 {votes['T3']} (admissible {T3_adm}, raw {T3vote}); T4 {votes['T4']} (admissible {T4_adm}, raw {T4vote_raw})")
P(f"OUTCOME: {WORD}   (path {path})   -> CFG306 C1 {C1}")
NUM["decision"] = dict(PF=PF, grade=grade, DOC=DOC, DOC_STRONG=bool(DOC_STRONG), votes=votes, outcome=WORD, path=path, C1=C1)

# ============================================================================ MUTATE checks
if MUT:
    P("\n== MUTATE checks (FROZEN section 9) ==")
    JM = json.load(open(MAIN_JSON))["numbers"]
    mainlink = JM["T2"]["T2b"]
    expect = {"1": "(1+z)", "1/(1+z)": "1", "(1+z)": "(1+z)^2"}.get(mainlink)
    check("M-a the T2b link moves from the main run's link to that link times (1 + z)", f"main {mainlink} -> MUTATE {T2b} (expected {expect}; a (1+z)^2 link is not testable and reads AMBIGUOUS)",
          (T2b == expect) or (expect == "(1+z)^2" and T2b == "AMBIGUOUS"))
    mg = pd.read_csv(os.path.join(HERE, "cfg309_per_galaxy.csv"), dtype={"ID": str})
    dm = dict(zip(mg.ID, mg.Delta)); sh_ = np.array([D1[i] - dm[S.ID.iloc[i]] for i in range(len(S))]); okb = np.nanmax(np.abs(sh_ + x)) <= 1e-12
    check("M-b per-galaxy Delta_MUT - Delta_main = -log10(1+z) to <= 1e-12 (identical fits)", f"max |dev| {np.nanmax(np.abs(sh_ + x)):.2e}", okb)
    mo = JM["decision"]["outcome"]
    if mo == "REST-FRAME": okc, exp_ = WORD == "OBSERVED-FRAME", "OBSERVED-FRAME"
    elif mo == "OBSERVED-FRAME": okc, exp_ = WORD != "OBSERVED-FRAME", "not OBSERVED-FRAME"
    else: okc, exp_ = None, "not applicable"
    if okc is None:
        P(f"  [N/A ] M-c the decision flips: main {mo} -> MUTATE {WORD} (not applicable from UNDECIDED)")
    else:
        check("M-c the decision flips", f"main {mo} -> MUTATE {WORD} (required {exp_})", okc)
    NUM["MUTATE"] = dict(main_link=mainlink, link=T2b, main_outcome=mo, outcome=WORD)

# ============================================================================ outputs
rows = []
for i in range(len(S)):
    f1, f2, f3, vfit = fits[i]
    rows.append(dict(ID=S.ID.iloc[i], z_freq=z[i], log1pz=x[i], W50_cat_compared=Wcmp[i], W50_cat_raw=WRAW[S.ID.iloc[i]], W50_nonparam_CFG302=S.W50_rest_kms.iloc[i],
                     NBFLAG=NB[i], logratio_S_CFG302=lsr[i], V_fit=vfit, good=f1["good"], reason=f1["reason"], redchi2=f1["redchi2"], W50_busy=f1["W50"], W20_busy=f1["W20"],
                     W50_busy_avgpeaks_POSTHOC=f1["W50avg"], Delta=D1[i], a=f1["p"][0], b1=f1["p"][1], b2=f1["p"][2], w=f1["p"][3], v_e=f1["p"][4], d=f1["p"][5], h=f1["p"][6], b0=f1["p"][7],
                     good_n4=f2["good"], W50_busy_n4=f2["W50"], good_catwin=f3["good"], W50_busy_catwin=f3["W50"]))
pg = pd.DataFrame(rows)
if not MUT:
    pg["inj_median_logratio"] = np.nan
    for j, i in enumerate(INJ["idx"]): pg.loc[i, "inj_median_logratio"] = INJ["per_galaxy_median"][j]
pg.to_csv(CSV, index=False, float_format="%.10g")
npass = sum(ok for _, ok in CHK)
P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")
open(OUT + ".out", "w").write("\n".join(LOG).replace(REPO, "<repo>").replace(os.path.dirname(REPO), "<repo>/..") + "\n")


def jc(o):
    if isinstance(o, dict): return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jc(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, float) and not math.isfinite(o): return None
    return o


json.dump(dict(lane="CFG309", frozen="ec54de4ac", script=os.path.basename(__file__), mutate=MUT, checks=[dict(name=n, ok=ok) for n, ok in CHK], n_pass=npass,
               n_checks=len(CHK), numbers=jc(NUM)), open(OUT + "_results.json", "w"), indent=1)
print(f"wrote {os.path.basename(OUT)}.out, _results.json and {os.path.basename(CSV)}")
