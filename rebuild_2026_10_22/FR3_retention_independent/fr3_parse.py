#!/usr/bin/env python3
"""FR3 parse: Okabe+25 Table E.1 (PDF text, own regex) and VizieR TSVs into dicts. No downloaded code run. python3 -I. kappa = 1/2 FITTED, unused; not theory closed."""
import os, re, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "data")
NUM = r"(\d+\.\d+)"
def okabe():
    t = subprocess.run(["pdftotext", "-f", "25", "-l", "26", "-raw", os.path.join(DATA, "okabe25.pdf"), "-"], capture_output=True, text=True).stdout.replace("−", "-")
    idx = [m for m in re.finditer(r"^J(\d{6}\.\d[+-]\d{6})(\S*)", t, re.M)]; R = []
    for i, m in enumerate(idx):
        c = t[m.end():idx[i + 1].start() if i + 1 < len(idx) else len(t)]; c = c.split("Notes")[0]; c = re.sub(r"\s+", " ", c)
        q = re.search(NUM + r" " + NUM + r" ± " + NUM + r" (.*)", c)
        if q is None: raise SystemExit("okabe parse fail " + m.group(1) + " " + c[:80])
        rest = q.group(4); e = re.match(NUM + r"\+" + NUM + r" -" + NUM + r" " + NUM + r"\+" + NUM + r" -" + NUM, rest)
        row = dict(id=m.group(1), flag=m.group(2), z=float(q.group(1)), lam=float(q.group(2)), M500=None, up=None, dn=None, M200=None)
        if e: row.update(M500=float(e.group(1)), up=float(e.group(2)), dn=float(e.group(3)), M200=float(e.group(4)))
        elif not rest.startswith("- -"): raise SystemExit("okabe mass parse fail " + m.group(1) + " " + rest[:60])
        R.append(row)
    return R
def tsv(path, table=None):
    """VizieR asu-tsv: returns {table name: list of dict}. Table name from '#Name:' before the columns."""
    T = {}; name = None; hdr = None; st = 0
    for ln in open(path):
        ln = ln.rstrip("\n")
        if ln.startswith("#Name:"): name = ln.split(":", 1)[1].strip(); st = 0; continue
        if ln.startswith("#") or not ln.strip(): 
            if not ln.strip(): st = 0 if st == 3 else st
            continue
        if st == 0: hdr = [h.strip() for h in ln.split("\t")]; st = 1; continue
        if st == 1: st = 2; continue
        if st == 2:
            if set(ln.strip()) <= set("- \t"): st = 3; continue
        v = [x.strip() for x in ln.split("\t")]; T.setdefault(name, []).append(dict(zip(hdr, v)))
    return T
def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
def fl(x):
    try: return float(x)
    except (TypeError, ValueError): return float("nan")
