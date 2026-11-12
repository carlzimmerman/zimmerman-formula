#!/usr/bin/env python3
"""HL3 fetch (criteria ef4595f390; owner's go 2026-11-08 "Yes, download them"): data files only, into
_external_data/hl3/<source>/ at the repo root (untracked). Nothing downloaded is executed; tarballs are unpacked
with tarfile's data filter. Every file is logged in FETCH_LOG.md (URL, bytes, sha256, use), repo-relative paths only.
    python3 -I hl3_fetch.py           # fetch + log
VizieR CfA first, CDS second; two time-outs -> logged and skipped. Budget < 200 MB. kappa = 1/2 FITTED; not theory closed."""
import os, sys, hashlib, tarfile, urllib.request, urllib.error, socket, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
EXT = os.path.join(REPO, "_external_data", "hl3"); LOG = os.path.join(HERE, "FETCH_LOG.md")
def rel(p): return os.path.relpath(p, REPO)
ROWS = []; TOTAL = 0
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def get(url, dest, tries=2, timeout=90):
    global TOTAL
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hl3-fetch/1.0 (data download)"})
            with urllib.request.urlopen(req, timeout=timeout) as r, open(dest, "wb") as f:
                n = 0
                while True:
                    b = r.read(1 << 20)
                    if not b: break
                    f.write(b); n += len(b)
                    if TOTAL + n > 200 * 1024 * 1024: raise RuntimeError("200 MB budget")
            TOTAL += n; return n, None
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
            err = f"{type(e).__name__}: {str(e)[:80]}"; time.sleep(2)
        except RuntimeError as e: return None, str(e)
    return None, err
def vizier_probe(cat, source):
    """ASU-TSV header only (-out.max=3); CfA then CDS. Records whether the catalogue exists."""
    d = os.path.join(EXT, source); os.makedirs(d, exist_ok=True)
    for host in ("vizier.cfa.harvard.edu", "vizier.cds.unistra.fr"):
        url = f"https://{host}/viz-bin/asu-tsv?-source={cat}&-out.max=3"; dest = os.path.join(d, f"vizier_probe_{host.split('.')[1]}.tsv")
        n, err = get(url, dest, timeout=60)
        if n is None: ROWS.append((source, url, "-", "-", f"NOT FETCHED ({err})")); continue
        txt = open(dest, errors="replace").read(); status = "catalogue not found" if "Error=" in txt or "not found" in txt.lower() else ("tables listed" if "#Table" in txt else "empty reply")
        ROWS.append((source, url, str(n), sha(dest)[:16], f"probe: {status}; {rel(dest)}"))
        if status == "tables listed": return True
    return False
def arxiv_source(aid, source, use):
    d = os.path.join(EXT, source); os.makedirs(d, exist_ok=True); dest = os.path.join(d, f"arXiv-{aid}.tar.gz")
    url = f"https://arxiv.org/e-print/{aid}"; n, err = get(url, dest)
    if n is None: ROWS.append((source, url, "-", "-", f"NOT FETCHED ({err}); {use}")); return False
    ROWS.append((source, url, str(n), sha(dest)[:16], f"{use}; {rel(dest)}"))
    out = os.path.join(d, "src"); os.makedirs(out, exist_ok=True)
    try:
        with tarfile.open(dest) as tf: tf.extractall(out, filter="data")
        names = sorted(os.listdir(out)); ROWS.append((source, "(unpacked)", "-", "-", f"{len(names)} entries under {rel(out)}: " + ", ".join(names[:12]) + (" ..." if len(names) > 12 else "")))
    except tarfile.TarError as e:
        ROWS.append((source, "(unpack)", "-", "-", f"not a tar archive ({type(e).__name__}); single file kept"))
    return True
if __name__ == "__main__":
    os.makedirs(EXT, exist_ok=True)
    st = os.statvfs(REPO); free_gib = st.f_bavail * st.f_frsize / 2 ** 30
    if free_gib < 2.0: sys.exit(f"STOP: {free_gib:.2f} GiB free < 2 GiB")
    # D1 Umetsu+2016 CLASH lensing profiles: VizieR J/ApJ/821/116, fallback arXiv 1507.04385
    if not vizier_probe("J/ApJ/821/116", "umetsu16_vizier"): arxiv_source("1507.04385", "umetsu16", "D1 CLASH lensing profiles / NFW M500 (fallback source)")
    # D2 Donahue+2014 gas + BCG: VizieR J/ApJ/794/136, fallback arXiv 1405.7876
    if not vizier_probe("J/ApJ/794/136", "donahue14_vizier"): arxiv_source("1405.7876", "donahue14", "D2 CLASH X-ray gas profiles, M500, BCG (fallback source)")
    # D3 conditional LoCuSS: Okabe & Smith 2016 source (per-radius shear only if machine readable)
    arxiv_source("1507.04493", "okabe16", "D3 LoCuSS shear profiles (conditional)")
    with open(LOG, "w") as f:
        f.write("# HL3 FETCH LOG\n")
        f.write(f"Fetched 2026-11-08 to `_external_data/hl3/<source>/` at the repo root (untracked). Data only; nothing downloaded was executed; tarballs unpacked with the data filter. Owner's go (verbatim): \"Yes, download them\". Free disk before fetch {free_gib:.1f} GiB. Total bytes fetched {TOTAL}.\n\n")
        f.write("| source | URL | bytes | sha256 (first 16) | use / where |\n|---|---|---|---|---|\n")
        for r in ROWS: f.write("| " + " | ".join(r) + " |\n")
    print(open(LOG).read())
