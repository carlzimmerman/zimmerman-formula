#!/usr/bin/env python3
"""CFG305 step 1: independent confirmation of the reported published != repo differences (FROZEN_CRITERIA.md, 82dfcc1b3).

Reads the journal PDFs in place (the data-release chat's scratch copy; its location is given on the command line and is never written
into an output, where it appears as <journal>), runs pdftotext -layout itself, parses RC100 Table B1 (all 100 rows x z, log M_baryon,
R_e, f_DM, V_c, sigma_0) and Umehata+25 Tables 2 / 3 / 4 / C1 (row A7), and compares them with the repo's tables.  Context only: the
arXiv v1 PDF of Umehata+25 in the external-data folder (outside the repo, already on disk).
Usage:  python3 campaign_fresh_gravity/CFG305_published_tables/cfg305_confirm.py <journal_dir>
Writes cfg305_confirm.out and cfg305_confirm_results.json here.  Exit 1 if any control fails.
"""
import csv, hashlib, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
JDIR = os.path.abspath(sys.argv[1])
CORR = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv")
ORIG = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv")
B289 = os.path.join(REPO, "campaign_fresh_gravity", "CFG289_rc100_csv_bound", "cfg289_build_corrected_results.json")
LIT = os.path.join(REPO, "data_assembly", "adf22_5_literature_2026-10-02", "adf22_5_literature_values.csv")
DIR = os.path.join(REPO, "data_assembly", "adf22_5_literature_2026-10-02", "adf22_pdf_direct_reads_A7.csv")
PDF = {"rc100": "rc100_apj944_78.pdf", "fs18": "fs18_apjs238_21.pdf", "umehata25": "umehata25_apj997_79.pdf"}
FIELDS = ["z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "Vc_Re_kms", "sigma0_kms"]
REPORTED_RC = {("87", "logMbar_Msun"): "10.72", ("87", "Re_kpc"): "3.85", ("87", "fDM_within_Re"): "0.44", ("87", "Vc_Re_kms"): "250",
               ("87", "sigma0_kms"): "37", ("78", "sigma0_kms"): "77"}
REPORTED_UM = {"n": 1.42, "Re": 1.58, "ba": 0.435, "PA": 17.9}
lines, checks = [], []
P = lambda s="": (print(s), lines.append(s))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
fl = lambda s: float(s.replace("\u2212", "-"))


def check(name, ok, detail=""):
    checks.append(dict(check=name, ok=bool(ok), detail=detail))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


def layout(pdf):
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "t.txt")
        subprocess.run(["pdftotext", "-layout", pdf, out], check=True)
        return open(out, encoding="utf-8").read().splitlines()


P(f"CFG305 confirm: FROZEN_CRITERIA.md sha256 {sha(os.path.join(HERE, 'FROZEN_CRITERIA.md'))[:16]}; pdftotext -layout on the journal PDFs (<journal> = the data-release chat's scratch copy)")
# ---------------------------------------------------------------- J0 hashes
ref = {l.split()[0]: l.split()[2] for l in open(os.path.join(JDIR, "SHA256.txt")) if l.strip()}
hashes = {k: sha(os.path.join(JDIR, v)) for k, v in PDF.items()}
for k, v in PDF.items():
    P(f"  {v}: sha256 {hashes[k][:16]}... (SHA256.txt {ref.get(v, '-')[:16]}...)")
check("J0 each journal PDF's sha256 equals the data-release chat's SHA256.txt", all(hashes[k] == ref.get(v) for k, v in PDF.items()))

# ---------------------------------------------------------------- RC100 Table B1
L = layout(os.path.join(JDIR, PDF["rc100"]))
CORE = re.compile(r"(?P<lms>[\d.]+)\s+(?P<lmb>\d+\.\d+)\s*\((?P<elmb>[\d.]+)\)\s+(?P<lbu>\d+\.\d+)\s*\((?P<elbu>[\d.]+)\)\s+"
                  r"(?:(?P<re>\d+\.\d+)\s+(?P<fdm>\d+\.\d+)\s+)?(?P<vc>\d+)\s*\((?P<evc>\d+)\)\s+(?P<s0>\d+)\s*\((?P<es0>\d+)\)")
start = next(i for i, l in enumerate(L) if "RC100 Galaxy Best-" in l)
rowlines = []
for i in range(start, len(L)):
    m = CORE.search(L[i])
    if not m:
        continue
    pre = L[i][:m.start("lms")].split()
    ints = []
    for t in pre:
        if re.fullmatch(r"\d{1,3}", t):
            ints.append(t)
        else:
            break
    if not ints:
        continue
    rowlines.append((i, ints[-1], pre[len(ints):], m))
PUB, displaced = {}, []
for k, (i, idx, toks, m) in enumerate(rowlines):
    nxt = rowlines[k + 1][0] if k + 1 < len(rowlines) else len(L)
    re_, fdm = m.group("re"), m.group("fdm")
    if re_ is None:
        for j in range(i + 1, nxt):
            mm = re.search(r"(?:^|\s)(\d+\.\d+)\s+(\d+\.\d+)\s*$", L[j])
            if mm and "(" not in L[j]:
                re_, fdm = mm.group(1), mm.group(2)
                displaced.append(idx)
                break
    zt = toks[-4] if len(toks) >= 4 else ""
    # tokens before log M*: [name ...] z FWHM T_int dSFR  -> z is the 4th from the right (a glued 'name+z' token keeps only its d.dd tail)
    mz = re.search(r"(\d\.\d{1,2})$", zt)
    PUB[idx] = dict(z=mz.group(1) if mz else None, logMbar_Msun=m.group("lmb"), Re_kpc=re_, fDM_within_Re=fdm, Vc_Re_kms=m.group("vc"),
                    sigma0_kms=m.group("s0"), name_tokens=" ".join(t for t in toks[:-4]), line=i + 1)
idxs = list(PUB)
ok1 = idxs == [str(i) for i in range(1, 101)] and all(all(PUB[i][f] is not None for f in FIELDS) for i in idxs)
check("J1 all 100 RC100 Table B1 rows parse, in order, with all six numeric fields", ok1,
      f"rows parsed {len(idxs)}; R_e/f_DM recovered from a separate page-break line for rows {displaced}")

C = {r["idx"]: r for r in csv.DictReader(open(CORR, newline=""))}
O = {r["idx"]: r for r in csv.DictReader(open(ORIG, newline=""))}


def diffs(T):
    out = []
    for i in idxs:
        for f in FIELDS:
            a, b = PUB[i][f], T[i][f]
            if a is None or abs(fl(a) - fl(b)) > 1e-9:
                out.append(dict(idx=i, name=T[i]["name"], field=f, published=a, repo=b))
    return out


DC, DO = diffs(C), diffs(O)
P(f"\nRC100: published Table B1 vs the CORRECTED CSV, {len(idxs) * len(FIELDS)} numeric cells: {len(DC)} differ")
for d in DC:
    P(f"  row {d['idx']:>3} {d['name']:<14} {d['field']:<14} published {d['published']:>7}  CORRECTED {d['repo']:>7}")
c289 = [c for c in json.load(open(B289))["changed"] if c["field"] != "name"]
j2 = [(c["idx"], c["field"]) for c in c289 if abs(fl(PUB[c["idx"]][c["field"]]) - fl(C[c["idx"]][c["field"]])) > 1e-9]
check("J2 (positive) the 12 value cells CFG289 corrected equal the CORRECTED CSV in the published table", len(c289) == 12 and not j2,
      f"{len(c289)} cells (rows {sorted({c['idx'] for c in c289}, key=int)}); mismatches {j2}")
dset = {(d["idx"], d["field"]) for d in DO}
j3 = [(c["idx"], c["field"]) for c in c289 if (c["idx"], c["field"]) not in dset]
check("J3 (negative) against the ORIGINAL CSV the comparison reports all 12 of those cells as differences", not j3,
      f"original CSV: {len(DO)} differing cells in all; of the 12, not seen: {j3}")
decisions = []
P("\nRC100 decision per reported cell (CONFIRMED = published equals the reported value and differs from the CORRECTED CSV)")
for (i, f), rep in REPORTED_RC.items():
    pub, rp = PUB[i][f], C[i][f]
    ok = abs(fl(pub) - fl(rep)) < 1e-9 and abs(fl(pub) - fl(rp)) > 1e-9
    decisions.append(dict(table="RC100 Table B1", idx=i, name=C[i]["name"], field=f, reported=rep, published=pub, repo=rp,
                          decision="CONFIRMED" if ok else "REFUTED"))
    P(f"  row {i:>3} {C[i]['name']:<14} {f:<14} reported {rep:>6}  published {pub:>6}  CORRECTED {rp:>6}  -> {'CONFIRMED' if ok else 'REFUTED'}")
new = [d for d in DC if (d["idx"], d["field"]) not in REPORTED_RC]
P(f"  NEW published != CORRECTED cells not in the chat's report: {len(new)}" + (f" {[(d['idx'], d['field']) for d in new]}" if new else ""))
P(f"  printed row lines (for the page-image read): row 78 at text line {PUB['78']['line']}, row 87 at text line {PUB['87']['line']}")

# ---------------------------------------------------------------- Umehata+25
U = layout(os.path.join(JDIR, PDF["umehata25"]))
PM = re.compile(r"(-?[\d.]+)\s*\u00b1\s*([\d.]+)")


def table_row(LL, title, rowname, after=0):
    t = next(i for i in range(after, len(LL)) if re.search(title, LL[i]))
    r = next(i for i in range(t, min(t + 40, len(LL))) if re.search(re.escape(rowname) + r"\s", LL[i]))
    seg = LL[r]
    return t, r, seg


def a7_cells(seg, start_at=None):
    s = seg[seg.index("A7") + 2:] if start_at is None else seg[start_at:]
    return [(fl(a), fl(b)) for a, b in PM.findall(s.replace("\u2212", "-"))]


t3, r3, s3 = table_row(U, r"^\s*Table 3\s*$", "ADF22.A7")
tab3 = a7_cells(s3)
t4, r4, s4 = table_row(U, r"^\s*Table 4\s*$", "ADF22.A7")
tab4 = a7_cells(s4)
n1_4 = re.search(r"\u00b1\s*[\d.]+\s+(1\.00)\s+", s4[s4.index("A7"):])
tC, rC, sC = table_row(U, r"\bTable C1\s*$", "ADF22.A7")
tabC = a7_cells(sC[sC.index("ADF22.A7"):])
t2, r2, s2 = table_row(U, r"^\s*Table 2\s*$", "ADF22.A7")
pos2 = re.findall(r"\d\d:\d\d:\d\d\.\d+", s2)
tab2 = a7_cells(s2[s2.index("ADF22.A7"):])
P(f"\nUmehata+25 (ApJ 997:79) row ADF22.A7, extracted:")
P(f"  Table 3 (ALMA 870 um) masked n/R_e/b-a/PA: {tab3[:4]}; unmasked: {tab3[4:8]}")
P(f"  Table 4 (F444W) free n: {tab4[:4]}; fixed n = 1 (n printed {n1_4.group(1) if n1_4 else '?'}): {tab4[4:7]}")
P(f"  Table C1 (870 um, n = 1): {tabC[:3]}")
P(f"  Table 2: position {pos2}; first flux pairs {tab2[:3]}")
LV = {r["quantity"]: r for r in csv.DictReader(open(LIT, newline=""))}
DV = {r["quantity"]: r for r in csv.DictReader(open(DIR, newline=""))}
ok3 = len(tab3) == 8 and len(tab4) == 7 and len(tabC) == 3
check("J1b the Umehata+25 Table 3 (8 pairs), Table 4 (4 + 3 pairs) and Table C1 (3 pairs) A7 rows parse", ok3,
      f"pairs {len(tab3)}, {len(tab4)}, {len(tabC)}")
P("\nUmehata+25 Table 3 masked A7: published vs repo (adf22_pdf_direct_reads_A7.csv = the arXiv v1 PDF read; adf22_5_literature_values.csv alma870_*)")
KEYS = [("n", "umehata25_870um_masked_n", "alma870_sersic_n"), ("Re", "umehata25_870um_masked_Re", "alma870_Re"),
        ("ba", "umehata25_870um_masked_ba", "alma870_axis_ratio"), ("PA", "umehata25_870um_masked_PA", "alma870_PA")]
um_cells = []
for k, (q, qd, ql) in enumerate(KEYS):
    pv, pe = tab3[k]
    dv, de = float(DV[qd]["value"]), float(DV[qd]["err_hi"])
    lv, le = float(LV[ql]["value"]), float(LV[ql]["err_hi"])
    ok = abs(pv - REPORTED_UM[q]) < 1e-9 and abs(pv - dv) > 1e-9 and abs(pv - lv) > 1e-9
    decisions.append(dict(table="Umehata+25 Table 3 masked", idx="A7", field=q, reported=REPORTED_UM[q], published=pv, published_err=pe,
                          repo=dv, repo_err=de, decision="CONFIRMED" if ok else "REFUTED"))
    um_cells.append(dict(field=q, direct_quantity=qd, lit_quantity=ql, value=pv, err=pe, repo_value=dv, repo_err=de, value_differs=abs(pv - dv) > 1e-9,
                         err_differs=abs(pe - de) > 1e-9))
    P(f"  {q:3s} reported {REPORTED_UM[q]:<6} published {pv} +- {pe}   repo {dv} +- {de} (literature CSV {lv} +- {le})  -> {'CONFIRMED' if ok else 'REFUTED'}"
      + (f"; error bar also differs ({de} -> {pe})" if abs(pe - de) > 1e-9 else ""))
UNM = [("n", "umehata25_870um_unmasked_n"), ("Re", "umehata25_870um_unmasked_Re"), ("ba", "umehata25_870um_unmasked_ba"), ("PA", "umehata25_870um_unmasked_PA")]
um_extra = []
P("  unmasked fit (context; not a reported cell):")
for k, (q, qd) in enumerate(UNM):
    pv, pe = tab3[4 + k]
    dv, de = float(DV[qd]["value"]), float(DV[qd]["err_hi"])
    st = "same" if abs(pv - dv) < 1e-9 and abs(pe - de) < 1e-9 else ("ERROR BAR DIFFERS" if abs(pv - dv) < 1e-9 else "VALUE DIFFERS")
    if st != "same":
        um_extra.append(dict(field=q, direct_quantity=qd, value=pv, err=pe, repo_value=dv, repo_err=de, status=st))
    P(f"    {q:3s} published {pv} +- {pe}   repo {dv} +- {de}   {st}")
import math
i_pub, i_rep = math.degrees(math.acos(tab3[2][0])), math.degrees(math.acos(float(DV["umehata25_870um_masked_ba"]["value"])))
P(f"  thin-disc inclination arccos(b/a), masked fit: published {i_pub:.2f} deg vs repo {i_rep:.2f} deg")
# J4: Table 2 and Table 4 cells reported as matching
j4 = []
for (v, e), q in zip(tab4[:4], ("F444W_sersic_n", "F444W_Re", "F444W_axis_ratio", "F444W_PA")):
    if abs(v - float(LV[q]["value"])) > 1e-9 or abs(e - float(LV[q]["err_hi"])) > 1e-9:
        j4.append(q)
for (v, e), q in zip(tab4[4:7], ("umehata25_F444W_n1_Re", "umehata25_F444W_n1_ba", "umehata25_F444W_n1_PA")):
    if abs(v - float(DV[q]["value"])) > 1e-9 or abs(e - float(DV[q]["err_hi"])) > 1e-9:
        j4.append(q)
if pos2[:2] != LV["position_umehata25"]["value"].replace("+", "").split()[:2]:
    j4.append("position_umehata25")
s11 = [p for p in tab2 if abs(p[0] - 2.03) < 1e-9]
if not s11 or abs(s11[0][1] - 0.04) > 1e-9:
    j4.append("S_1.1mm_1arcsec")
check("J4 Umehata+25 Table 4 A7 (free n and n = 1) and Table 2 A7 (position, S_1.1mm 2.03 +- 0.04) equal the repo's values", not j4,
      f"mismatches {j4}")
# context: the arXiv v1 PDF already on disk
ctx = {}
pv1 = os.path.join(EXT, "arxiv_pdf", "2502.01868.pdf")
if os.path.exists(pv1):
    V1 = layout(pv1)
    stamp = re.findall(r"arXiv:2502\.01868v\d", "\n".join(V1[:200]))
    try:
        _, _, sv = table_row(V1, r"Table 3\.\s+ALMA 870", "ADF22.A7")   # arXiv v1 prints "Table 3. ALMA 870 um profile measurements"
        ctx = dict(sha256=sha(pv1), stamp=stamp[:1], table3_A7=a7_cells(sv))
    except StopIteration:
        ctx = dict(sha256=sha(pv1), stamp=stamp[:1], table3_A7=None)
    P(f"\nCONTEXT: the arXiv PDF on disk (<external-data>/arxiv_pdf/2502.01868.pdf, sha256 {ctx['sha256'][:16]}..., stamp {ctx['stamp']}) Table 3 A7: {ctx['table3_A7']}")
    if ctx.get("table3_A7"):
        P(f"  masked fit in arXiv v1 vs the journal: " + "; ".join(f"{q} {a[0]}+-{a[1]} -> {b[0]}+-{b[1]}" for q, a, b in zip(("n", "Re", "b/a", "PA"), ctx["table3_A7"][:4], tab3[:4])))
        P(f"  the repo's values equal arXiv v1: {all(abs(a[0] - c['repo_value']) < 1e-9 for a, c in zip(ctx['table3_A7'][:4], um_cells))}")
else:
    P("\nCONTEXT: the arXiv v1 PDF of Umehata+25 is not on disk; not used")

conf_rc = [d for d in decisions if d["table"].startswith("RC100") and d["decision"] == "CONFIRMED"]
conf_um = [d for d in decisions if d["table"].startswith("Umehata") and d["decision"] == "CONFIRMED"]
P(f"\nSUMMARY: RC100 {len(conf_rc)}/{len(REPORTED_RC)} reported cells CONFIRMED; Umehata+25 {len(conf_um)}/{len(REPORTED_UM)} CONFIRMED; "
  f"NEW RC100 differences {len(new)}; other Umehata cells that differ from the repo: {[(c['direct_quantity'], c['status']) for c in um_extra] + [(c['direct_quantity'], 'ERROR BAR DIFFERS') for c in um_cells if c['err_differs']]}")
n_ok = sum(c["ok"] for c in checks)
P(f"{n_ok}/{len(checks)} checks pass")
res = dict(frozen_criteria_sha256=sha(os.path.join(HERE, "FROZEN_CRITERIA.md")), pdf_sha256=hashes, rc100_published=PUB, rc100_displaced_rows=displaced,
           rc100_vs_corrected=DC, rc100_vs_original_n=len(DO), decisions=decisions, rc100_new=new,
           rc100_confirmed_cells=[dict(idx=d["idx"], field=d["field"], published=d["published"]) for d in conf_rc],
           umehata=dict(table3_A7=tab3, table4_A7=tab4, tableC1_A7=tabC, table2_A7=dict(position=pos2, pairs=tab2), masked=um_cells, other_differences=um_extra,
                        inclination_published=i_pub, inclination_repo=i_rep), arxiv_v1_context=ctx, checks=checks)
txt = json.dumps(res, indent=1).replace(JDIR, "<journal>").replace(EXT, "<external-data>")
open(os.path.join(HERE, "cfg305_confirm_results.json"), "w").write(txt)
open(os.path.join(HERE, "cfg305_confirm.out"), "w").write(("\n".join(lines) + "\n").replace(JDIR, "<journal>").replace(EXT, "<external-data>"))
sys.exit(0 if n_ok == len(checks) else 1)
