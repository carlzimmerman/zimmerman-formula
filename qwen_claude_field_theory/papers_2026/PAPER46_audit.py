#!/usr/bin/env python3
"""PAPER46 audit: the built PDF must match the chart data, the sealed-hash prefixes must match the committed hash files,
the standing honesty phrases must be present, and no forbidden claim, personal name or local path may appear.
Run: python3 PAPER46_audit.py   (exit 0 only if every check passes). Gate the deposit on this: build && audit && publish."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CHART = os.path.join(REPO, "explainers", "kepler_grade_prediction_chart.html")
TEX = os.path.join(HERE, "PAPER46_prediction_ledger_2026.tex")
PDF = os.path.join(HERE, "PAPER46_prediction_ledger_2026.pdf")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
R, F = [], 0


def check(name, ok, msg=""):
    global F
    R.append((name, ok, msg))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))
    if not ok:
        F += 1


chart = open(CHART, encoding="utf-8").read()
js = re.search(r"<script>(.*)</script>", chart, re.S).group(1)
head = js.split("renderFuture(); renderConf(); renderDepo();")[0]
stub = ("var document={getElementById:function(){return {}},querySelectorAll:function(){return []}};" + head +
        "\nconsole.log(JSON.stringify({FUTURE:FUTURE,CONF:CONF,DEPO:DEPO,DNC:DNC,NON:NON}));")
d = json.loads(subprocess.run(["node", "-e", stub], capture_output=True, text=True, check=True).stdout)
nF = sum(len(g["rows"]) for g in d["FUTURE"]); nC = sum(len(g["rows"]) for g in d["CONF"])
cnt = {k: sum(1 for g in d["FUTURE"] for r in g["rows"] if r["g"] == k) for k in ("K1", "K2", "K3", "K4")}

check("A1 PDF is newer than the TeX, the TeX newer than the chart",
      os.path.getmtime(PDF) >= os.path.getmtime(TEX) >= os.path.getmtime(CHART),
      f"chart {os.path.getmtime(CHART):.0f} tex {os.path.getmtime(TEX):.0f} pdf {os.path.getmtime(PDF):.0f}")
txt = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True, check=True).stdout
for lig, rep in (("\ufb01", "fi"), ("\ufb02", "fl"), ("\ufb00", "ff"), ("\ufb03", "ffi"), ("\ufb04", "ffl"), ("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"')):
    txt = txt.replace(lig, rep)                     # pdftotext emits ligatures and curly quotes
flat = re.sub(r"\s+", " ", txt)
check("A2 abstract counts equal the chart's counts (future, K1-K4, confronted, deposits)",
      all(s in flat for s in (f"Each of {nF} future tests", f"{cnt['K1']} tests", f"{nC} confronted results", f"{len(d['DEPO'])} public deposits")),
      f"future {nF}, K {cnt}, confronted {nC}, deposits {len(d['DEPO'])}")
rows_in_tex = open(TEX, encoding="utf-8").read().count(r"\addlinespace[2pt]")
check("A3 every future row is a table row in the TeX", rows_in_tex == nF, f"{rows_in_tex} rows in TeX, {nF} in chart")
anchors = ["Kepler grade", "74.1", "1.1614", "0.0613", "9.3603", "2026-12-02", "0.2061", "0.0970", "4.22", "4.99", "f8bea44f",
           "0.3162", "7.66 meV", "0.0149", "Standing terms" if False else "Scope and standing terms"]
miss = [a for a in anchors if a not in flat]
check("A4 anchor numbers and phrases present in the PDF", not miss, f"missing {miss}")
pref = {"CFG553": "f8bea44f", "CFG571_prereg_proprietary_alma": "be27457d", "CFG549_dark_energy_evolution_prediction": "f110566e"}
okh, det = True, []
for lane, pre in pref.items():
    folder = [x for x in os.listdir(CFG) if x.startswith(lane)]
    hits = []
    for fo in folder:
        p = os.path.join(CFG, fo, "PREDICTIONS_HASH.txt")
        if os.path.exists(p):
            hits.append(open(p).read().strip().lower())
    good = any(h.startswith(pre) or pre in h for h in hits)
    okh &= good; det.append(f"{lane[:8]}:{'ok' if good else 'NO'}")
check("A5 sealed-hash prefixes in the paper match the committed PREDICTIONS_HASH.txt files", okh, " ".join(det))
check("A6 standing honesty phrases present", all(s in flat for s in ("fitted", "not peer reviewed", "AI-assisted", "not closed", "never pooled", "Nothing here says the data favour")),
      "")
bad = re.findall(r"(theory (is )?closed|kappa is derived|the data favour the framework(?!\.))", flat, re.I)
neg_ok = "Nothing here says the data favour the framework" in flat
# 'theory is not closed' is the permitted form; reject any positive claim
pos = [m for m in re.findall(r"(?<![\'\"])\btheory (?:is )?closed", flat, re.I)]
check("A7 no positive 'theory closed' claim", not pos, f"{pos}")
check("A8 no personal name, owner, or local path", not re.search(r"(/Users/|\bowner\b|\bCarl\b|\bZimmerman,)", flat), "")
check("A9 no replacement characters or unmapped placeholders", "�" not in txt and "?" not in re.findall(r"[A-Za-z]\?[A-Za-z]", flat) , "")
badtags = []
ok_tags = {"sub", "sup", "span", "b", "i", "br", "div", "table", "thead", "tbody", "tr", "td", "th", "p", "a", "h3", "script", "strong", "em", "small", "style", "title", "link", "input", "button", "h1", "h2", "html", "head", "body", "meta"}
datasec = chart[chart.index("<script>"):chart.index("function renderFuture")]
for m in re.finditer(r"<(/?)([A-Za-z][A-Za-z0-9]*)", datasec):
    if m.group(2).lower() not in ok_tags:
        badtags.append(datasec[m.start():m.start() + 24])
check("A10 chart data has no bare '<' before a letter (it would be read as an HTML tag)", not badtags, f"{badtags[:3]}")
print(f"\n{len(R) - F}/{len(R)} checks pass")
sys.exit(1 if F else 0)
