#!/usr/bin/env python3
"""CFG442 fetch (owner-approved for this lane). Downloads, with curl, into ../_external_data/cfg442/ (git-ignored) or ./data/ (small):
  - Cosmicflows-4 table2 + ReadMe (VizieR J/ApJ/944/94)           -> external (10.7 MB)
  - Oh+2015 LITTLE THINGS VizieR tables (J/AJ/149/180)             -> data/
  - Hunter+2012 table1 + refs (J/AJ/144/134)                       -> data/
  - Oh+2015 arXiv source (1502.01281) tarball                      -> external; the 26 disk-halo figure PDFs extracted to external/oh15_figs/
  - CDS Sesame coordinates (+ identifiers) for the SR candidate SPARC names -> data/sesame_sr.json
Appends one line per file to FETCH_LOG.md (URL, UTC date, bytes, sha256). Paths written relative to the repo. Run: python3 cfg442_fetch.py [--parse-only]   (--parse-only: no downloads; re-parse the stored Sesame XML into data/sesame_sr.json)
"""
import os, sys, io, json, gzip, hashlib, subprocess, tarfile, datetime, contextlib, re, urllib.parse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
EXT = os.path.join(LANES, "_external_data", "cfg442"); DAT = os.path.join(HERE, "data")
os.makedirs(EXT, exist_ok=True); os.makedirs(DAT, exist_ok=True)
LOG = os.path.join(HERE, "FETCH_LOG.md")
def rel(p): return os.path.relpath(p, os.path.dirname(LANES))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
PARSE_ONLY = "--parse-only" in sys.argv
def get(url, dest):
    if PARSE_ONLY: return dest
    subprocess.run(["curl", "-sL", "-m", "180", "-o", dest, url], check=True)
    b = os.path.getsize(dest); head = open(dest, "rb").read(200)
    if b"404 Not Found" in head or b"<!DOCTYPE HTML" in head: raise SystemExit(f"fetch failed (HTML): {url}")
    line = f"| {url} | {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')} | {b} | {sha(dest)} | {rel(dest)} |"
    open(LOG, "a").write(line + "\n"); print(line); return dest
def gunz(p):
    out = p[:-3]; open(out, "wb").write(gzip.open(p).read()); return out
if not os.path.exists(LOG):
    open(LOG, "w").write("# CFG442 fetch log (owner-approved for this lane, chat 10-06)\n\n| URL | date (UTC) | bytes | sha256 | stored at |\n|---|---|---|---|---|\n")
CDS = "https://cdsarc.cds.unistra.fr/ftp/"
if not PARSE_ONLY:
    get(CDS + "J/ApJ/944/94/ReadMe", os.path.join(EXT, "cf4_ReadMe"))
    gunz(get(CDS + "J/ApJ/944/94/table2.dat.gz", os.path.join(EXT, "cf4_table2.dat.gz")))
    get(CDS + "J/AJ/149/180/ReadMe", os.path.join(DAT, "oh15_ReadMe"))
    for f in ("table1.dat", "table2.dat", "rotdmbar.dat", "rotdm.dat"):
        gunz(get(CDS + f"J/AJ/149/180/{f}.gz", os.path.join(DAT, f"oh15_{f}.gz"))); os.remove(os.path.join(DAT, f"oh15_{f}.gz"))
    get(CDS + "J/AJ/144/134/ReadMe", os.path.join(DAT, "hunter12_ReadMe"))
    for f in ("table1.dat", "refs.dat"):
        gunz(get(CDS + f"J/AJ/144/134/{f}.gz", os.path.join(DAT, f"hunter12_{f}.gz"))); os.remove(os.path.join(DAT, f"hunter12_{f}.gz"))
    tgz = get("https://arxiv.org/e-print/1502.01281", os.path.join(EXT, "oh15_arxiv_1502.01281.tar.gz"))
    FIG = os.path.join(EXT, "oh15_figs"); os.makedirs(FIG, exist_ok=True)
    with tarfile.open(tgz) as t:
        for m in t.getmembers():
            if os.path.basename(m.name).startswith("rMD_DH_DM_profiles_") and m.name.endswith(".pdf"):
                open(os.path.join(FIG, os.path.basename(m.name)), "wb").write(t.extractfile(m).read())
    man = {f: sha(os.path.join(FIG, f)) for f in sorted(os.listdir(FIG))}
    json.dump(man, open(os.path.join(DAT, "oh15_figs_sha256.json"), "w"), indent=1)
    print(f"extracted {len(man)} disk-halo figure PDFs (sha256 manifest data/oh15_figs_sha256.json)")
# SR candidates: CFG397 selection (Q<=2, >=3 gas points), f_D in {1, 4}
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
def nsel(g):
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2; vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    return int(((vg2 >= 0.7 * vb2) & (vb2 > 0) & (g["Vobs"] > 0)).sum())
cand = [g["name"] for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2 and nsel(g) >= 3 and g["meta"]["fD"] in (1, 4)]
def simbad_name(n):
    m = re.match(r"^(UGC|NGC|IC|DDO|UGCA|PGC)0*(\d+)$", n)
    if m: return f"{m.group(1)} {m.group(2)}"
    m = re.match(r"^([DF])(\d{3})-(\d+)$", n)                 # LSB catalogue names (D631-7, F563-V1 handled below)
    if m: return f"LSBC {m.group(1)}{m.group(2)}-{int(m.group(3)):02d}"
    m = re.match(r"^F(\d{3})-V(\d+)$", n)
    if m: return f"LSBC F{m.group(1)}-V{m.group(2)}"
    return n
ses = {}
for n in cand:
    q = simbad_name(n); dest = os.path.join(EXT, f"sesame_{n}.xml")
    get("https://cdsweb.u-strasbg.fr/cgi-bin/nph-sesame/-oxpI/SNV?" + urllib.parse.quote(q), dest)
    x = open(dest).read()
    ra = re.search(r"<jradeg>([-+0-9.]+)</jradeg>", x); de = re.search(r"<jdedeg>([-+0-9.]+)</jdedeg>", x)
    pgc = re.search(r"<alias>PGC\s+(\d+)</alias>", x)
    ses[n] = dict(query=q, ra=float(ra.group(1)) if ra else None, dec=float(de.group(1)) if de else None, pgc=int(pgc.group(1)) if pgc else None)
    print(n, ses[n])
json.dump(ses, open(os.path.join(DAT, "sesame_sr.json"), "w"), indent=1)
print(f"SR candidates: {len(cand)}")
