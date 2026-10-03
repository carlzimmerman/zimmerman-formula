#!/usr/bin/env python3
"""CFG310 -- second-round hostile referee: the numerical and compliance checks behind REFEREE_REPORT_MNRAS_v3.2.md and
REFEREE_REPORT_PAPER40_v1.1.md.  Read-only on the repository: it reads committed files (working tree at HEAD 24fcc8250, which equals
the tag mnras-v3.2 for the MNRAS directory) and writes only cfg310_referee_checks.out and cfg310_referee_checks_results.json next to
itself.  Post hoc referee diagnostics: NOT frozen, NOT an a0 measurement.  kappa = 1/2 is FITTED.  The cold mass is still required.
Nothing here says the data favour any law.

Sections
  M1  MNRAS abstract word counts (three conventions), keywords, AI disclosure, data availability, alt text, PDF size/pages
  M2  MNRAS bibliography: the ALESS 122.1 data sources (absent), Lee2025 against Crossref (JSON saved in this lane), entry count
  M3  RC100 native route: the Newtonian-floor fraction against redshift and a censoring-aware rank test (CFG303's per-galaxy CSV)
  M4  MUSE-DARK native rows as committed in paper_numbers.json (route ii with gas; route iii stars only)
  M5  KURVS native P2 cell and ALESS 122.1 fractions (paper_numbers.json), against what the text prints
  M6  the RC100 PUBLISHED table: which columns it carries (does it contain the SED M* column the native route uses?)
  P1  PAPER40 abstract word counts
  P2  PAPER40 single-dish flux readings: the quoted range against CFG304's frozen primary and the adopted record (STANDING CFG309)
  P3  PAPER40 H0 like-for-like comparison with the footings (1.208e-10) against the headline comparison (1.311e-10)
  P4  PAPER40 statistical error: bootstrap SD (committed) against the median's asymptotic error from the paper's own robust per-galaxy SD,
      and a re-run of the pooled estimator under 5 bootstrap seeds (chain re-implemented by exec of make_paper40_figures.py's first part)
  P5  PAPER40 joint-fit 68 per cent interval (committed, not printed) and the selection rows
  P6  PAPER40 Zenodo metadata sanity and PDF metadata
Usage: python3 cfg310_referee_checks.py
"""
import os, re, sys, json, math, subprocess, io, contextlib
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
P26 = os.path.join(REPO, "qwen_claude_field_theory", "papers_2026")
MN = os.path.join(P26, "mnras_submission_2026_v3")
TEXM = os.path.join(MN, "mnras_a0_lambda_v3.tex")
TEXP = os.path.join(P26, "PAPER40_meerkat_a0_2026.tex")
PN = json.load(open(os.path.join(MN, "paper_numbers.json")))
P40 = json.load(open(os.path.join(P26, "PAPER40_figures_numbers.json")))
OUT = []
RES = {}


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s); print(s)


def abstract_counts(tex):
    src = open(tex, encoding="utf-8").read()
    src = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("%"))
    ab = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", src, re.S).group(1)
    ab = ab.replace("\\noindent", " ")
    maths = re.findall(r"\$[^$]*\$", ab)
    nomath = re.sub(r"\$[^$]*\$", " ", ab)
    words_out = [w for w in re.split(r"\s+", nomath) if re.search(r"[A-Za-z0-9]", w)]
    raw = [w for w in re.split(r"\s+", ab) if w.strip()]
    return dict(words_outside_math=len(words_out), math_spans=len(maths), math_as_one_word=len(words_out) + len(maths),
                raw_whitespace_tokens=len(raw))


def pdf_text(pdf):
    return subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout


# ---------------------------------------------------------------- M1 MNRAS compliance
say("== M1 MNRAS compliance ==")
ac = abstract_counts(TEXM)
t = pdf_text(os.path.join(MN, "mnras_a0_lambda_v3.pdf"))
m = re.search(r"ABSTRACT(.*?)Key words", t, re.S)
ac["pdftotext_words"] = len(m.group(1).split()) if m else None
b02 = os.path.join(MN, "upload_bundle", "02_title_abstract_keywords.txt")
if os.path.exists(b02):
    bt = open(b02, encoding="utf-8").read()
    ac["scholarone_paste_text_words"] = len(re.search(r"ABSTRACT[^\n]*\n(.*?)\n\s*KEYWORDS", bt, re.S).group(1).split())
say("abstract:", ac, "(limit 250)")
RES["M1_abstract"] = ac
srcm = open(TEXM, encoding="utf-8").read()
kw = re.search(r"\\begin\{keywords\}(.*?)\\end\{keywords\}", srcm, re.S).group(1).strip()
kws = [k.strip() for k in kw.split("--")]
say("keywords:", len(kws), kws)
RES["M1_keywords"] = kws
ai = re.search(r"Generative artificial-intelligence tools.*?responsibility for it\.", srcm, re.S)
say("AI disclosure present:", bool(ai), "| providers named:", [p for p in ["Claude", "OpenAI", "DeepSeek", "GLM", "Qwen", "Gemini"] if ai and p in ai.group(0)])
say("Data Availability present:", "\\section*{Data Availability}" in srcm, "| names tag mnras-v3.2:", "mnras-v3.2" in srcm)
tag = subprocess.run(["git", "-C", REPO, "rev-parse", "mnras-v3.2"], capture_output=True, text=True).stdout.strip()
say("tag mnras-v3.2 ->", tag[:9])
alt = os.path.join(MN, "upload_bundle", "04_alt_text_for_figures.txt")
if os.path.exists(alt):
    t = open(alt, encoding="utf-8").read()
    say("alt text (git-ignored bundle): figures with alt text:", len(re.findall(r"^Figure \d", t, re.M)))
else:
    say("alt text: bundle not present (git-ignored); make_upload_bundle.py writes it")
pdfm = os.path.join(MN, "mnras_a0_lambda_v3.pdf")
info = subprocess.run(["pdfinfo", pdfm], capture_output=True, text=True).stdout
pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
say("PDF:", os.path.getsize(pdfm), "bytes,", pages, "pages (limit 10 MB)")
RES["M1_pdf"] = dict(bytes=os.path.getsize(pdfm), pages=pages, tag=tag)
cover = open(os.path.join(MN, "COVER_LETTER.md"), encoding="utf-8").read()
say("cover letter still says 'must be finalised by the author (TODO-AI-DISCLOSURE)':", "TODO-AI-DISCLOSURE" in cover)
say("'framework-native' occurrences in the manuscript (term never defined for a journal reader):",
    len(re.findall(r"framework-native", "\n".join(l for l in srcm.splitlines() if not l.lstrip().startswith("%")))))

# ---------------------------------------------------------------- M2 bibliography
say("\n== M2 MNRAS bibliography ==")
bib = open(os.path.join(MN, "references.bib"), encoding="utf-8").read()
say("bib entries:", len(re.findall(r"^@", bib, re.M)))
for nm in ["Dunne", "Calistro", "Amvrosiadis"]:
    say(f"  '{nm}' in references.bib: {nm.lower() in bib.lower()}   in tex: {nm.lower() in srcm.lower()}")
say("  'ALESS 122.1' named in the tex:", srcm.count("ALESS 122.1"), "times")
cr = json.load(open(os.path.join(HERE, "cfg310_lee2025_crossref.json")))["message"]
lee = re.search(r"@ARTICLE\{Lee2025,.*?\}\}", bib, re.S).group(0)
ok_lee = (str(cr["volume"]) == "701" and (cr.get("article-number") or cr.get("page")) == "A260" and cr["author"][0]["family"] == "Lee"
          and "10.1051/0004-6361/202555362" in lee and "ALMA-CRISTAL" in cr["title"][0])
say("  Lee2025 vs Crossref (A&A 701, A260, first author Lee, DOI, title 'The ALMA-CRISTAL survey ...'):", "MATCH" if ok_lee else "MISMATCH")
RES["M2"] = dict(lee2025_crossref_match=ok_lee, aless_sources_in_bib=False)

# ---------------------------------------------------------------- M3 RC100 native censoring
say("\n== M3 RC100 native route: Newtonian-floor fraction vs z (CFG303 per-galaxy CSV) ==")
d = pd.read_csv(os.path.join(REPO, "campaign_fresh_gravity", "CFG303_lcdm_free_inputs", "cfg303_rc100_pergalaxy_LCDMFREE.csv"))
f = 1 - d.g_bar_native_B_ms2 / d.g_obs_ms2
ok = (f > 0.02) & (f < 0.98)
a0 = np.where(ok, (1 - f) * d.g_obs_ms2 / np.log(1 / f.clip(1e-9)) ** 2, np.nan)
la = np.log10(a0)
floor = ~ok
say("N inverted", int(ok.sum()), "| floor (f <= 0.02)", int(floor.sum()))
bins = [(0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 2.6)]
rows = []
for lo, hi in bins:
    m = (d.z >= lo) & (d.z < hi)
    lc = np.where(ok[m], la[m], -99.0)
    med = float(np.median(lc))
    rows.append(dict(z=f"{lo}-{hi}", n=int(m.sum()), floor=int(floor[m].sum()), frac=round(float(floor[m].mean()), 2),
                     median_log_a0_censored=None if med < -50 else round(med, 3), median_log_a0_inverted_only=round(float(np.nanmedian(la[m])), 3)))
    say("  ", rows[-1])
rf = spearmanr(d.z, floor.astype(int))
ru = spearmanr(d.z[ok], la[ok])
rc = spearmanr(d.z, np.where(ok, la, -99.0))
say(f"Spearman(z, floor) = {rf.statistic:+.3f} (p {rf.pvalue:.3f});  Spearman(z, log a0) inverted only = {ru.statistic:+.3f} (p {ru.pvalue:.3f});"
    f"  with the floor discs ranked lowest = {rc.statistic:+.3f} (p {rc.pvalue:.4f})")
say("Reading: the floor fraction rises with z (27% -> 51%); excluding floor discs removes the low-a0 tail preferentially at high z. With the"
    " censoring kept, the native implied a0 FALLS with z -- inconsistent with all three laws, i.e. a z-dependent bias of the native baryons,"
    " which the paper's own decision rule ('inconsistent with all of them counts against all of them') would read as a calibration failure.")
RES["M3"] = dict(bins=rows, spearman_floor=[rf.statistic, rf.pvalue], spearman_inverted=[ru.statistic, ru.pvalue], spearman_censored=[rc.statistic, rc.pvalue])

# ---------------------------------------------------------------- M4 MUSE-DARK native rows
say("\n== M4 MUSE-DARK native rows (paper_numbers.json S7.native.musedark) ==")
md = PN["S7"]["native"]["musedark"]
for route in ("ii_rows", "iii_rows"):
    for r in md[route]:
        say(f"  route {route[:-5]:>3} z {r['z']:.2f}: s* {r['s']:.3f} (no root {r['no_root']}), 95% log s [{r['itv']['lo95']:+.2f}, {r['itv']['hi95']:+.2f}],"
            f" D<1 {r['n_D_lt1']}/{r['n']}, FLAT inside 95%: {r['flags95']['FLAT']}, H(z) inside: {r['flags95']['H(z)']}")
say("  totals (rows where the law's s* is inside the 95% interval, of 6):", md["flags"])
say("  route iii z3 - z1 =", round(md["iii"]["d"], 3), "+-", round(md["iii"]["sd"], 3), "(the number the text quotes)")
say("Reading: with molecular gas (route ii) the implied scale is 0.22 / 0.27 x canonical and FLAT lies outside the 95% interval in 2 of 3 thirds"
    " (z 0.88 excluded, z 1.20 no root). The abstract's 'the MUSE-DARK rise ... disappears' and Conclusion (vi) 'on SED masses no route rises'"
    " omit that the gas-inclusive native route is inconsistent with constancy too.")
RES["M4"] = dict(flags=md["flags"], iii=md["iii"])

# ---------------------------------------------------------------- M5 KURVS / ALESS
say("\n== M5 KURVS native P2 cell, ALESS 122.1 fractions ==")
k = PN["S7"]["native"]["kurvs"]
say("  KURVS native P2 cell: FLAT residual", [round(x, 3) for x in k["P2"]["cell"]["flat"]], " rival residual", [round(x, 3) for x in k["P2"]["cell"]["rival"]],
    " class:", k["P2"]["cls"], "| cells lean flat/rival/neither:", k["lean_flat"], k["lean_rival"], k["neither"])
zf = k["P2"]["cell"]["flat"][0] / k["P2"]["cell"]["flat"][1]; zr = k["P2"]["cell"]["rival"][0] / k["P2"]["cell"]["rival"][1]
say(f"  both laws under-predict: FLAT {zf:.1f} sigma, rival {zr:.1f} sigma (the text gives no magnitudes)")
al = PN["S7"]["native"]["aless122"]["decision"]
say("  ALESS 122.1: N", al["N"], " FLAT excluded", round(al["f_FLAT_excl"], 3), " H(z) excluded", round(al["f_Hz_excl"], 3), " FLAT below", al["f_FLAT_below"],
    " no root", round(al["f_noroot"], 3), " native s*", round(PN["S7"]["native"]["aless122"]["s"], 2))
say("  the text quotes only the no-root fraction (44%) and the range; it omits FLAT excluded in 27% (always from above) vs H(z) 15%")
RES["M5"] = dict(kurvs_P2=k["P2"]["cell"], aless=al)

# ---------------------------------------------------------------- M6 PUBLISHED table columns
say("\n== M6 the RC100 PUBLISHED table ==")
pub = pd.read_csv(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_PUBLISHED.csv"))
say("  columns:", list(pub.columns))
has_mstar = any("star" in c.lower() or "sed" in c.lower() for c in pub.columns)
say("  carries an SED stellar-mass column:", has_mstar, "-> the native route's M* (CFG303 transcription of arXiv-v1 column 6) is not part of the",
    "journal-checked table; only row 87's M* was compared with the journal (CFG305 README)")
RES["M6"] = dict(columns=list(pub.columns), has_sed_mstar=has_mstar)

# ---------------------------------------------------------------- P1 PAPER40 abstract
say("\n== P1 PAPER40 abstract ==")
ap = abstract_counts(TEXP)
say("abstract:", ap, "(MNRAS limit 250 if ever submitted; Zenodo has no limit)")
RES["P1_abstract"] = ap

# ---------------------------------------------------------------- P2 PAPER40 flux readings
say("\n== P2 PAPER40 single-dish flux readings (PAPER40_figures_numbers.json flux_k0) ==")
fl = P40["post_hoc_rows"]["flux_k0"]
A0C, A0A = 9.3603e-11, 1.1312e-10
for kk, v in fl.items():
    say(f"  {kk:>13}: R {v['R']:+.3f}  a0_gas {v['a0_gas']*1e10:.3f}e-10  vs canonical {math.log10(v['a0_gas']/A0C):+.3f} dex, alt {math.log10(v['a0_gas']/A0A):+.3f} dex  ({v['label']})")
lo_q, mid_q, hi_q = fl["pairs7"]["a0_gas"], fl["snr_extrap"]["a0_gas"], fl["z_extrap"]["a0_gas"]
say(f"  quoted: {mid_q*1e10:.2f} ({lo_q*1e10:.2f}-{hi_q*1e10:.2f}); CFG304's frozen primary (15 code-1 pairs, R -0.195) gives {fl['c1']['a0_gas']*1e10:.2f}, OUTSIDE the quoted range;")
say("  CFG306 recommended 0.90-1.06 (or 0.90-1.13); STANDING (CFG309 entry) records 0.90-1.06 and 'about 0.9-1.31e-10 between flux scales';")
say("  the paper's 'honest range is about 1.0 to 1.31' also drops 0.90.  The central 1.07 is a linear extrapolation in SNR_3D of 15 pairs (post hoc).")
RES["P2"] = dict(readings={k_: v["a0_gas"] for k_, v in fl.items()}, quoted=[mid_q, lo_q, hi_q])

# ---------------------------------------------------------------- P3 PAPER40 H0 like-for-like
say("\n== P3 PAPER40 H0 like-for-like ==")
J = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG309_mightee_width_frame", "cfg309_cfg301chain_stageB_FRAME_results.json")))["numbers"]
pool = J["results"]["pooled"]
a0p = pool["a0"]; rh = pool["recipe_half"]
h0row = J["recipe"]["pooled"]["rows"]["h0"]          # CFG309's committed H0 = 67.4 knob (the chain re-run, not a scaling)
rh_noH0 = math.sqrt(max(rh ** 2 - h0row["half"] ** 2, 0))
a0_674 = 10 ** h0row["log_s"][0] * A0C
q = pool["q"]  # bootstrap log s* percentiles 2.5/16/84/97.5
lo95 = 10 ** q[0] * A0C; lo95_674 = lo95 * (a0_674 / a0p)
say(f"  headline a0 {a0p*1e10:.4f}e-10, recipe {rh:.4f}; 95% stat lower {lo95*1e10:.3f}")
say(f"  H0 = 67.4 ('like-for-like' in the paper): a0 {a0_674*1e10:.4f}e-10;  canonical {math.log10(a0_674/A0C):+.4f} dex, alt {math.log10(a0_674/A0A):+.4f} dex;"
    f"  95% stat lower {lo95_674*1e10:.3f}e-10 (alt footing 1.131 {'INSIDE' if A0A > lo95_674 else 'outside'})")
say(f"  recipe without the H0 knob (once the H0 shift is applied, it is a correction, not a systematic): {rh_noH0:.4f} dex ->"
    f" canonical {'INSIDE' if math.log10(a0_674/A0C) < rh_noH0 else 'outside'} ; with the H0 knob kept ({rh:.4f}) also"
    f" {'INSIDE' if math.log10(a0_674/A0C) < rh else 'outside'}")
say("Reading: on the value the paper itself calls like-for-like, the canonical footing is INSIDE the recipe width and the alternative footing is inside"
    " the 95% statistical interval; the abstract's 'canonical footing just outside the recipe width' and 'both footings outside the 95% statistical"
    " interval' hold only on the catalogue's H0 = 70 distances.")
RES["P3"] = dict(a0_674=a0_674, d_can=math.log10(a0_674 / A0C), d_alt=math.log10(a0_674 / A0A), recipe=rh, recipe_noH0=rh_noH0, lo95_674=lo95_674)

# ---------------------------------------------------------------- P4 PAPER40 statistical error
say("\n== P4 PAPER40 statistical error ==")
rsd = P40["post_hoc_rows"]["residuals_k0"]["per_gal_robust_sd"]
n = 47
se_asym = math.sqrt(math.pi / 2) * rsd / math.sqrt(n)
say(f"  committed bootstrap SD {pool['sd']:.4f} dex;  per-galaxy robust SD (paper's own JSON) {rsd:.4f} -> asymptotic SE of a median {se_asym:.4f} dex")
say(f"  with SE {se_asym:.3f}: 95% half-width {1.96*se_asym:.3f} dex; alt footing is {math.log10(a0p/A0A):.3f} dex below -> {'inside' if math.log10(a0p/A0A) < 1.96*se_asym else 'outside'}")
# re-run the pooled estimator under several bootstrap seeds with the paper's own chain (exec of make_paper40_figures.py up to 'gate = []')
src = open(os.path.join(P26, "make_paper40_figures.py"), encoding="utf-8").read()
head = src.split("\ngate = []")[0]
ns = {"__file__": os.path.join(P26, "make_paper40_figures.py"), "__name__": "cfg310_exec"}
argv0 = sys.argv; sys.argv = ["make_paper40_figures.py", "--check"]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, "make_paper40_figures_head", "exec"), ns)
sys.argv = argv0
dd = ns["chain"](ns["a"], ns["W"], ns["RECP"])
l0 = ns["est"](dd)[0]
say(f"  exec'd chain: pooled log s* {l0:.6f} (committed {pool['log_s']:.6f}; {'MATCH' if abs(l0-pool['log_s'])<1e-9 else 'MISMATCH'})")
sds = []
for seed in (1, 2, 3, 4, 5):
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, n, n)
        bs.append(ns["est"]({"D": dd["D"][i], "gb": dd["gb"][i]})[0])
    bs = np.array(bs)
    sds.append(float(np.std(bs)))
    say(f"   seed {seed}: bootstrap SD {np.std(bs):.4f}, 68% [{np.percentile(bs,16)-l0:+.4f}, {np.percentile(bs,84)-l0:+.4f}], 95% [{np.percentile(bs,2.5)-l0:+.4f}, {np.percentile(bs,97.5)-l0:+.4f}]")
ps = np.array([ns["est"]({"D": dd["D"][[i]], "gb": dd["gb"][[i]]})[0] for i in range(n)])
srt = np.sort(ps)
gaps = np.diff(srt)
mid = n // 2
say(f"  per-galaxy log s* around the median: {np.round(srt[mid-4:mid+5],3).tolist()} (gaps {np.round(gaps[mid-4:mid+4],3).tolist()})")
say("Reading: the bootstrap SD is stable across seeds but is ~30% below the median's asymptotic error implied by the per-galaxy spread; the"
    " sample is peaked near its median. 'Both footings outside the 95% statistical interval' rests on the narrower figure; quote both.")
RES["P4"] = dict(boot_sd=pool["sd"], robust_sd=rsd, se_asym=se_asym, boot_sd_seeds=sds)

# ---------------------------------------------------------------- P5 joint fit, selection
say("\n== P5 PAPER40 joint fit and selection ==")
jf = P40["post_hoc_rows"]["residuals_k0"]["joint_fit"]
say(f"  b_z {jf['b_z']:+.2f}, 68% [{jf['b_z_68'][0]:+.2f}, {jf['b_z_68'][1]:+.2f}] (excludes 0; not printed), 95% [{jf['b_z_95'][0]:+.2f}, {jf['b_z_95'][1]:+.2f}] (printed)")
sel = P40["post_hoc_rows"]["selection_snr"]
say(f"  no SNR cut: a0 {sel['0']['a0']*1e10:.2f}e-10 ({sel['0']['dlog_vs_primary']:+.3f}); removed 23: {sel['removed_by_8']['a0']*1e10:.2f}e-10 ({sel['removed_by_8']['dlog_vs_primary']:+.3f});"
    " the abstract lists flux, width and kernel systematics but not selection")
RES["P5"] = dict(joint=jf, sel0=sel["0"], removed=sel["removed_by_8"])

# ---------------------------------------------------------------- P6 Zenodo metadata
say("\n== P6 PAPER40 Zenodo metadata and PDF metadata ==")
z = json.load(open(os.path.join(P26, "PAPER40_meerkat_a0_2026.zenodo.json")))["metadata"]
texp = open(TEXP, encoding="utf-8").read()
title_tex = re.search(r"\{\\Large\\bfseries (.*?)\}\\\\", texp).group(1)
say("  title matches tex:", z["title"] == title_tex, "| version:", z["version"], "| license:", z["license"], "| keywords:", len(z["keywords"]))
say("  creators:", len(z["creators"]), "entry, with affiliation:", all("affiliation" in c for c in z["creators"]), "(a personal name; tex byline: 'The authors'; name not printed here)")
say("  related_identifiers present:", "related_identifiers" in z, "| communities:", "communities" in z, "| notes:", "notes" in z)
desc = re.sub(r"<[^>]+>", " ", z["description"])
for s in ["1.31e-10", "0.034 dex", "0.128 dex", "0.70 or 0.58", "1.07 (0.97-1.13)", "0.06-0.07 dex", "0.009 dex", "375 of 375"]:
    say(f"   description carries '{s}':", s in desc)
say("  description refers to 'Version 1.0' (never deposited) and to internal lane labels CFG306/CFG309:", "Version 1.0" in z["description"], "CFG306" in z["description"])
infop = subprocess.run(["pdfinfo", os.path.join(P26, "PAPER40_meerkat_a0_2026.pdf")], capture_output=True, text=True).stdout
say("  PAPER40 PDF Title/Author metadata:", "Title:" in infop, "Author:" in infop, "| pages", re.search(r"Pages:\s+(\d+)", infop).group(1))
RES["P6"] = dict(title_match=z["title"] == title_tex, version=z["version"], related_identifiers="related_identifiers" in z)

json.dump(RES, open(os.path.join(HERE, "cfg310_referee_checks_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg310_referee_checks.out"), "w").write("\n".join(OUT) + "\n")
