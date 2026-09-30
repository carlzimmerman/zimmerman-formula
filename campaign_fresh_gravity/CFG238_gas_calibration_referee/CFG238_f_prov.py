#!/usr/bin/env python3
"""CFG238 attack f: provenance (hashes, TSV re-parse, HTML spot-check) and the convention table (frozen section 6f). Exit 0."""
import sys, html as htmlmod
from CFG238_common import *

outp, jp = out_paths("CFG238_f_prov")
T = Tee(outp)
banner(T, "CFG238 attack f (provenance, hashes, parse spot-checks, conventions)")
R = {}
LINES = []


def line(lid, ok, msg):
    LINES.append((lid, ok))
    T(f"  [{'PASS' if ok else 'MISS'}] {lid} {msg}")


# ------------------------------------------------------------------ 1 hashes
T("\n== 1. sha256 verification against the repo manifests")
ok_all = True
cnt = 0
for mf in ("manifest_multitracer.json", "manifest_ace.json"):
    man = json.load(open(os.path.join(MT, mf)))
    for fn, h in man.items():
        p = os.path.join(RAW, fn)
        if not os.path.exists(p):
            T(f"  MISSING {fn}"); ok_all = False; continue
        hh = sha(p); cnt += 1
        if hh != h:
            T(f"  MISMATCH {fn}: manifest {h[:12]} file {hh[:12]}"); ok_all = False
    T(f"  {mf}: {len(man)} entries checked")
T(f"  HTML pages in raw_small: {len(os.listdir(RAW))}; verified {cnt}; all match: {ok_all}")
dm = json.load(open(os.path.join(DU, "manifest.json")))
tsv = os.path.join(EXT, "dunne2022_J_MNRAS_517_962_asu.tsv")
T(f"  Dunne TSV location <ext>/dunne2022_J_MNRAS_517_962_asu.tsv exists: {os.path.exists(tsv)} (outside the repo; not committed)")
tsv_ok = False
if os.path.exists(tsv):
    hh = sha(tsv); sz = os.path.getsize(tsv)
    tsv_ok = (hh == dm["sha256"]) and (sz == dm["bytes"])
    T(f"  Dunne TSV: sha256 {hh[:16]}... (manifest {dm['sha256'][:16]}...), bytes {sz} (manifest {dm['bytes']}): {'MATCH' if tsv_ok else 'MISMATCH'}")
R["hash"] = dict(html_ok=ok_all, n_html=cnt, tsv_ok=tsv_ok)
line("H-C23a", ok_all and tsv_ok, "all manifest hashes and the Dunne TSV sha256 and size match")

# ------------------------------------------------------------------ 2 TSV re-parse
T("\n== 2. Independent re-parse of the Dunne TSV and comparison with the committed CSVs")
lines = open(tsv, encoding="utf8", errors="ignore").read().split("\n")
tabs = {}
cur = None
for ln in lines:
    m = re.match(r"#Name: J/MNRAS/517/962/(\w+)", ln)
    if m:
        cur = m.group(1); tabs[cur] = dict(header=None, rows=[]); continue
    if cur and ln.strip() and not ln.startswith("#"):
        if tabs[cur]["header"] is None:
            tabs[cur]["header"] = [h.strip() for h in ln.split("\t")]
        elif not set(ln.replace("\t", "")) <= set("- "):
            tabs[cur]["rows"].append([c.strip() for c in ln.split("\t")])
rng = np.random.default_rng(238)
pv = {}
for tname, d in tabs.items():
    csvp = os.path.join(DU, f"dunne2022_{tname}.csv")
    C = readcsv(csvp)
    same_n = len(C) == len(d["rows"])
    idx = rng.choice(len(d["rows"]), size=min(20, len(d["rows"])), replace=False)
    bad = 0; tot = 0
    for i in idx:
        for h, v in zip(d["header"], d["rows"][i]):
            tot += 1
            if C[i][h].strip() != v:
                bad += 1
    pv[tname] = dict(rows_tsv=len(d["rows"]), rows_csv=len(C), same_n=same_n, cells=tot, bad=bad)
    T(f"  {tname}: TSV rows {len(d['rows'])} CSV rows {len(C)} ({'same' if same_n else 'DIFFERENT'}); 20 random rows: {tot - bad}/{tot} cells equal")
R["tsv_parse"] = pv
line("H-C23b", all(v["same_n"] and v["bad"] == 0 for v in pv.values()), "committed Dunne CSVs equal an independent re-parse of the TSV (row counts, 20 random rows per table)")

# ------------------------------------------------------------------ 3 HTML spot-check
T("\n== 3. Spot-check of parsed values against the fetched HTML (heuristic: token within 600 characters after the row identifier; chance baseline from another row's values)")


def text_of(fn):
    t = open(os.path.join(RAW, fn), errors="ignore").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<annotation.*?</annotation>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = htmlmod.unescape(t)
    return re.sub(r"\s+", " ", t)


SPEC = [  # (label, csv, html, id column, key columns, sample size)
    ("Stripe82", "stripe82_z_lt0.3_CO_dust.csv", "arxiv_1803.08926_html_fetched_2026-09-30.html", "id", ["z", "Z_12logOH", "logMdust", "logMgas_CO", "logMgas_dust"], 10),
    ("Bourne+19", "bourne2019_z1_CI_CO_dust.csv", "arxiv_1810.01640_html_fetched_2026-09-30.html", "cid", ["z", "Mmol_CI_1e9", "Mmol_cont_1e9"], 5),
    ("H-ATLAS z=0.35", "hatlas_z035_CI_CO_dust.csv", "arxiv_2111.09067_html_fetched_2026-09-30.html", "id", ["LCI_log", "LCO_log", "L850_log", "logMH2"], 5),
    ("Kirkpatrick+19", "kirkpatrick2019_z2_CO_dust.csv", "arxiv_1905.11417_html_fetched_2026-09-30.html", "id", ["LCO10_1e10", "Mmol_CO_1e11", "Mmol_RJ_1e11"], 5),
    ("SMGs 2404.05596", "smg_CI_CO_3mm_arxiv2404.05596.csv", "arxiv_2404.05596_html_fetched_2026-09-30.html", "id", ["z", "LpCI_1e10", "LpCO10_1e10", "Mgas_CI_1e10"], 5),
    ("SPT 2306.03153", "spt_dsfg_CI_CO_CII_fluxes_arxiv2306.03153.csv", "arxiv_2306.03153_html_fetched_2026-09-30.html", "id", ["z", "CI10_Jykms", "CI21_Jykms"], 5),
    ("ACE 2609.20926", "ace_dgr_2609.20926.csv", "arxiv_2609.20926_html_fetched_2026-09-30.html", "id", ["z", "logMdust", "logMmol", "OH"], 5),
    ("ACE 2609.21040", "ace_dust_2609.21040.csv", "arxiv_2609.21040_html_fetched_2026-09-30.html", "id", ["z", "Mdust_1e7", "OH"], 5),
    ("ACE 2609.21072", "ace_gas_2609.21072.csv", "arxiv_2609.21072_html_fetched_2026-09-30.html", "id", ["z", "Mmol_CO_1e10", "OH"], 5),
    ("ACE 2609.21604", "ace_fluxes_2609.21604.csv", "arxiv_2609.21604_html_fetched_2026-09-30.html", "id", ["SCO32_mJykms", "B7_mJy"], 5),
]
spot = {}
post_fix = 0
for lab, cf, hf, idc, cols, ns in SPEC:
    rows = readcsv(os.path.join(MT, cf))
    txt = text_of(hf)
    good = [r for r in rows if all(r.get(c, "").strip() not in ("", "nan") for c in cols) and r.get(idc, "").strip()]
    if not good:
        T(f"  {lab}: no complete rows"); continue
    rng = np.random.default_rng(238)
    pick = rng.choice(len(good), size=min(ns, len(good)), replace=False)
    found = tried = chance_found = 0
    miss = []
    for k in pick:
        r = good[k]
        rid = r[idc].strip()
        wins = [txt[m.start(): m.start() + 600] for m in re.finditer(r"(?<![\w.])" + re.escape(rid) + r"(?![\w.])", txt)]
        other = good[int(rng.integers(0, len(good)))]
        for c in cols:
            v = r[c].strip(); tried += 1
            tok = re.compile(r"(?<![\d.])" + re.escape(v) + r"(?![\d])")
            hit = any(tok.search(w) for w in wins)
            if not hit and v.endswith(".0"):
                tokb = re.compile(r"(?<![\d.])" + re.escape(v[:-2]) + r"(?![\d.])")
                if any(tokb.search(w) for w in wins):
                    post_fix += 1
            found += int(hit)
            if not hit:
                miss.append((rid, c, v))
            vo = other[c].strip()
            tok2 = re.compile(r"(?<![\d.])" + re.escape(vo) + r"(?![\d])")
            chance_found += int(any(tok2.search(w) for w in wins)) if other[idc] != r[idc] else 0
    spot[lab] = dict(found=found, tried=tried, chance=chance_found, n_windows_min=int(min(len(re.findall(r"(?<![\w.])" + re.escape(good[k][idc].strip()) + r"(?![\w.])", txt)) for k in pick)))
    T(f"  {lab}: sampled rows {len(pick)}: cells found {found}/{tried}; chance baseline (another row's values in the same windows) {chance_found}/{tried}; rows with no identifier hit in the text: {sum(1 for k in pick if not re.search(r'(?<![\w.])' + re.escape(good[k][idc].strip()) + r'(?![\w.])', txt))}; unmatched cells: {miss[:4]}")
R["spot"] = spot
tf = sum(v["found"] for v in spot.values()); tt = sum(v["tried"] for v in spot.values()); tc = sum(v["chance"] for v in spot.values())
T(f"  TOTAL cells found {tf}/{tt} ({tf / tt:.2f}); chance baseline {tc}/{tt} ({tc / tt:.2f})")
T(f"  [INFO] post hoc: of the unmatched cells, {post_fix} are integer-valued floats printed in the CSV as 'N.0' but as 'N' in the page text (format artefact of the frozen token rule); with them counted the found share is {(tf + post_fix) / tt:.2f}")
line("H-C23c", tf / tt >= 0.95, f"HTML spot-check found {tf / tt:.2f} of sampled key cells (estimate >= 0.95); chance baseline {tc / tt:.2f}")

# Bourne+19 masses sit in a different table keyed by an integer ID: targeted pattern check (post hoc, labelled)
bt = text_of("arxiv_1810.01640_html_fetched_2026-09-30.html")
nb = 0; tot_b = 0
for r in readcsv(os.path.join(MT, "bourne2019_z1_CI_CO_dust.csv")):
    try:
        a, ea, c, ec = (int(float(r[k])) for k in ("Mmol_CI_1e9", "Mmol_CI_1e9_errlo", "Mmol_cont_1e9", "Mmol_cont_1e9_errlo"))
    except Exception:
        continue
    tot_b += 1
    hit = re.search(rf"(?<![\d.]){a} \u00b1 {ea} {c} \u00b1 {ec}(?![\d])", bt) is not None
    nb += int(hit)
T(f"  [INFO] Bourne+19 mass pair pattern 'M_[CI] +- e  M_cont +- e' found for {nb}/{tot_b} rows (post hoc targeted check; the general token rule could not reach that table)")
R["bourne_pattern"] = (nb, tot_b)

# ------------------------------------------------------------------ 4 conventions
T("\n== 4. Convention table (sources: repo HTML and CSV headers; 'not stated' where the repo does not say)")
CONV = [
    ("Stripe82", "CO mass: 3.2 L' x metallicity factor x 1.36 (He) [repo HTML eq. 11]; dust gas mass = M_dust + 2 - 0.85 (Z - 8.67) [eq. 13], M_dust = 1.2e15 SFR T^-5.5 (Genzel+15) [eq. 12]; dust gas = total H2 + HI (Leroy+11), CO = H2 only", "gas phases differ; dust mass is a formula of SFR and T_dust"),
    ("Bourne+19", "[CI] mass H2 + He, Q10 = 0.35, X_CI = 3e-5; dust kappa_850 = 0.077 m2/kg; continuum gas-mass convention (He, dust-to-gas) NOT stated on disk", "He treatment of the continuum mass unresolved (0.134 dex)"),
    ("NOEMA3D", "alpha_CO 4.36 (incl. He), alpha_850 6.7e12 (Scoville), alpha_CI 18.7 (Dunne+22); dust at the CO tuning frequency, T_d 25 K, beta 1.8 (the data chat's assumption)", "CO control validates the CO branch only"),
    ("Dunne+22 CDS", "logMH2, aCO, XCI, GDR exclude He; log aCI, log a850 include 1.36 (identity residual -0.134 confirmed in section 1 of attack b); JCorr = additive log correction to the CO and CI line luminosities", "He constant cancels in slopes"),
    ("ACE", "alpha_CO = 1.36 x Accurso+17 (Z) (implied to 0.01 dex, attack c); r31 = 0.77; dust single band 873 um, T_d 25 K, beta 2.08, kappa 0.4 m2/kg at 250 um (recipe reproduced to 0.011 dex, attack c)", "kappa_850 equivalent 0.031 m2/kg: 0.35 dex below Dunne+22, 0.39 below Bourne+19"),
]
for s_, c_, n_ in CONV:
    T(f"  {s_}: {c_}  => {n_}")
R["conv"] = CONV
R["lines"] = LINES
dump(jp, R)
T.close()
sys.exit(0)
