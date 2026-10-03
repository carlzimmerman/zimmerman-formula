#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG306 (PAPER40 referee): presentation checks.  Reads committed files at git HEAD (git show), never edits them.

  T1  abstract length (words, after stripping TeX) in the tex and in the Zenodo description;
  T2  e-mail addresses and home-directory paths in the paper's files and in the three lanes' committed files;
  T3  the committed PDF against the tex: page count, fonts embedded, and a sample of numbers present in the PDF text;
  T4  Zenodo metadata fields (creators, version, licence, title equals the tex title, description equals the abstract in substance);
  T5  figures: files exist, page sizes, fonts embedded;
  T6  the audit's substring matching: audit literals that occur more than once in their block (a pass can be satisfied by the wrong occurrence).
Writes cfg306_presentation_checks.out and cfg306_presentation_checks_results.json.
"""
import os, re, json, subprocess, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
PAP = "qwen_claude_field_theory/papers_2026/"
LOG, NUM = [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def show(path, binary=False):
    r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + path], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def detex(s):
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = re.sub(r"\\(textbf|emph|textit|mathrm|rm)\{([^}]*)\}", r"\2", s)
    s = re.sub(r"\$[^$]*\$", " X ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^]]*\])?", " ", s)
    s = s.replace("{", " ").replace("}", " ").replace("~", " ")
    return s


tex = show(PAP + "PAPER40_meerkat_a0_2026.tex")
abs_tex = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1)
words_tex = len(detex(abs_tex).split())
zen = json.loads(show(PAP + "PAPER40_meerkat_a0_2026.zenodo.json"))["metadata"]
desc = re.sub(r"<[^>]+>", " ", zen["description"])
words_zen = len(desc.split())
P(f"T1 abstract: {words_tex} words in the tex (TeX math counted as one token each); Zenodo description {words_zen} words")
NUM["T1"] = dict(abstract_words_tex=words_tex, zenodo_description_words=words_zen)

# T2 e-mail / home paths
files = [PAP + f for f in ("PAPER40_meerkat_a0_2026.tex", "PAPER40_audit.py", "make_paper40_figures.py", "PAPER40_figures_numbers.json",
                           "PAPER40_meerkat_a0_2026.zenodo.json", "zenodo_publish_paper40.py")]
ls = subprocess.run(["git", "-C", REPO, "ls-files", "campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain", "campaign_fresh_gravity/CFG302_mightee_cube_raw_widths",
                     "campaign_fresh_gravity/CFG304_mightee_flux_scale_alfalfa", "data_assembly/mightee_hi_catalogue_2026-10-02"], capture_output=True, text=True).stdout.split()
files += ls
hits = []
pat_mail = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
pat_home = re.compile(r"/Users/[A-Za-z]|/home/[A-Za-z]|C:\\\\Users")
for f in files:
    s = show(f)
    if s is None:
        continue
    for m in pat_mail.finditer(s):
        hits.append((f, "email-like", m.group(0)))
    for m in pat_home.finditer(s):
        hits.append((f, "home path", s[max(0, m.start() - 10):m.end() + 20].replace("\n", " ")))
    if re.search(r"\bCarl\b|Zimmerman", s):
        hits.append((f, "owner name", re.search(r".{0,30}(\bCarl\b|Zimmerman).{0,30}", s).group(0).replace("\n", " ")))
P(f"T2 scanned {len(files)} committed files; hits: {len(hits)}")
for h in hits:
    P(f"   {h[1]:11s} {h[0]}: {h[2]!r}")
pdfb = show(PAP + "PAPER40_meerkat_a0_2026.pdf", binary=True)
open(os.path.join(HERE, "_tmp_paper40.pdf"), "wb").write(pdfb)
pdftxt = ""
if shutil.which("pdftotext"):
    pdftxt = subprocess.run(["pdftotext", "-layout", os.path.join(HERE, "_tmp_paper40.pdf"), "-"], capture_output=True, text=True).stdout
    m_ = pat_mail.findall(pdftxt); h_ = pat_home.findall(pdftxt)
    P(f"   PDF text: e-mail-like {m_}; home paths {h_}; owner name present: {bool(re.search(r'Carl|Zimmerman', pdftxt))}")
NUM["T2"] = dict(n_files=len(files), hits=hits)

# T3 PDF vs tex
info = subprocess.run(["pdfinfo", os.path.join(HERE, "_tmp_paper40.pdf")], capture_output=True, text=True).stdout if shutil.which("pdfinfo") else ""
pages = int(re.search(r"Pages:\s+(\d+)", info).group(1)) if info else None
fonts = subprocess.run(["pdffonts", os.path.join(HERE, "_tmp_paper40.pdf")], capture_output=True, text=True).stdout if shutil.which("pdffonts") else ""
not_emb = [l for l in fonts.splitlines()[2:] if l.split() and " no " in l]
sample = ["1.046", "1.312", "0.143", "+0.048", "-0.034", "0.559", "0.195", "0.64", "6.06", "7.50", "+0.098", "1.31", "0.084", "1.304", "0.322", "0.392",
          "-0.443", "0.489", "0.275", "-0.137", "9.62", "0.514", "0.425", "1.50", "1.19", "0.009", "93 of 100"]
norm = lambda s: s.replace("−", "-").replace("–", "-").replace("\u2212", "-")
pt = norm(pdftxt)
miss = [x for x in sample if x not in pt]
P(f"T3 PDF: {pages} pages; fonts not embedded: {len(not_emb)}; {len(sample) - len(miss)} of {len(sample)} sampled tex numbers found in the PDF text; missing {miss}")
pdf_date = re.search(r"CreationDate:\s+(.*)", info).group(1).strip() if info else None
tex_date = subprocess.run(["git", "-C", REPO, "log", "-1", "--format=%ci", "--", PAP + "PAPER40_meerkat_a0_2026.tex"], capture_output=True, text=True).stdout.strip()
P(f"   PDF CreationDate {pdf_date}; tex last commit {tex_date}")
NUM["T3"] = dict(pages=pages, fonts_not_embedded=not_emb, sample_missing=miss, pdf_creation=pdf_date, tex_commit=tex_date)

# T4 Zenodo
title_tex = re.sub(r"\s+", " ", detex(re.search(r"\\Large\\bfseries (.*?)\}\\\\", tex, re.S).group(1))).strip()
P(f"T4 Zenodo: title {zen['title']!r}; tex title (detexed) {title_tex!r}; version {zen.get('version')}; licence {zen.get('license')}; creators {zen.get('creators')}")
P(f"   byline in the tex: {re.search(r'small (The authors[^}]*)', tex).group(1)!r}")
numre = r"\d+\.\d+"
diff_nums = sorted(set(re.findall(numre, abs_tex)) ^ set(re.findall(numre, desc)))
P(f"   decimal numbers in the tex abstract but not in the Zenodo description, or vice versa: {diff_nums}")
NUM["T4"] = dict(title=zen["title"], version=zen.get("version"), creators=zen.get("creators"), number_symdiff=diff_nums)

# T5 figures
fig = {}
for f in ("fig1_paper40_levels.pdf", "fig2_paper40_btfr.pdf"):
    b = show(PAP + f, binary=True)
    tmp = os.path.join(HERE, "_tmp_" + f); open(tmp, "wb").write(b)
    inf = subprocess.run(["pdfinfo", tmp], capture_output=True, text=True).stdout
    fo = subprocess.run(["pdffonts", tmp], capture_output=True, text=True).stdout
    fig[f] = dict(page_size=re.search(r"Page size:\s+(.*)", inf).group(1).strip(), fonts_not_embedded=[l for l in fo.splitlines()[2:] if " no " in l])
    os.remove(tmp)
    P(f"T5 {f}: page size {fig[f]['page_size']}; fonts not embedded {len(fig[f]['fonts_not_embedded'])}")
NUM["T5"] = fig
os.remove(os.path.join(HERE, "_tmp_paper40.pdf"))

# T6 audit literal multiplicity
os.environ["PAPER40_REPO"] = REPO
sys.path.insert(0, os.path.join(REPO, PAP))
import importlib.util
spec = importlib.util.spec_from_file_location("p40audit", os.path.join(REPO, PAP, "PAPER40_audit.py"))
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
blocks = A.tex_blocks(tex)
multi = []
for (b, expected, getter, tlit, kind) in A.ROWS:
    lit = A.norm_tex(tlit if tlit is not None else expected)
    c = blocks.get(b, "").count(lit)
    if c > 1:
        multi.append((b, lit, c))
short = [(b, A.norm_tex(t if t is not None else e)) for (b, e, g, t, k) in A.ROWS if len(A.norm_tex(t if t is not None else e)) <= 4]
P(f"T6 audit rows: {len(A.ROWS)}; literals occurring more than once in their block: {len(multi)}; literals of <= 4 characters: {len(short)}")
for m in multi[:40]:
    P(f"   {m[0]} {m[1]!r} x{m[2]}")
NUM["T6"] = dict(n_rows=len(A.ROWS), multi=multi, short=short)

json.dump(dict(lane="CFG306", script=os.path.basename(__file__), numbers=NUM), open(os.path.join(HERE, "cfg306_presentation_checks_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, "cfg306_presentation_checks.out"), "w").write(__doc__.strip() + "\n\n" + "\n".join(LOG) + "\n")
print("wrote cfg306_presentation_checks.out and cfg306_presentation_checks_results.json")
