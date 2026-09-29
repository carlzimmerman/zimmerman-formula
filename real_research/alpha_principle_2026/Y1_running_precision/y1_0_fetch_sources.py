#!/usr/bin/env python3
"""y1_0_fetch_sources.py -- provenance of every source lane Y1 read: downloads (if absent) into the scratch directory and writes a sha256 manifest.

Run:    Y1_SCRATCH=<dir> python3 y1_0_fetch_sources.py            (default scratch dir: ./y1_scratch, created if missing; exit 0)
MUTATE: Y1_SCRATCH=<dir> python3 y1_0_fetch_sources.py MUTATE     (the control corrupts one expected checksum and must fail: exit 1; exit 3 if it does not)
Downloads only from arxiv.org and pdg.lbl.gov.  Nothing is written into the repository except y1_0_manifest.json (URL, file name, size, sha256).
Files read as text by a human are listed with the sections used in Y1_PREREGISTRATION.md.
"""
import hashlib
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("Y1_SCRATCH", os.path.join(".", "y1_scratch"))
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"

SOURCES = [
    ("1201.5868.tgz", "https://arxiv.org/e-print/1201.5868", "Mihaila-Salomon-Steinhauser letter: 3-loop gauge betas"),
    ("1208.3357.tgz", "https://arxiv.org/e-print/1208.3357", "Mihaila-Salomon-Steinhauser long paper: 3-loop gauge betas with b, tau, traces"),
    ("1912.07624.tgz", "https://arxiv.org/e-print/1912.07624", "Davies et al: 4-loop gauge betas"),
    ("1307.3536.tgz", "https://arxiv.org/e-print/1307.3536", "Buttazzo et al: NNLO matching, Planck values, 3-loop RGEs"),
    ("1205.6497.tgz", "https://arxiv.org/e-print/1205.6497", "Degrassi et al: inputs, Planck boundary"),
    ("1210.6873.tgz", "https://arxiv.org/e-print/1210.6873", "Bednyakov-Pikelner-Velizhanin (downloaded, NOT read)"),
    ("1212.6829.tgz", "https://arxiv.org/e-print/1212.6829", "Bednyakov et al Yukawa 3-loop (downloaded, NOT read)"),
    ("1303.4364.tgz", "https://arxiv.org/e-print/1303.4364", "Bednyakov et al lambda 3-loop (downloaded, NOT read)"),
    ("1508.02680.tgz", "https://arxiv.org/e-print/1508.02680", "Bednyakov-Pikelner 4-loop alpha_s with top Yukawa (downloaded, NOT read)"),
    ("hep-ph_0004189.pdf", "https://arxiv.org/pdf/hep-ph/0004189", "RunDec: QCD running and decoupling"),
    ("1306.6879.pdf", "https://arxiv.org/pdf/1306.6879", "Antusch-Maurer: SM running parameters table"),
    ("1907.02500.pdf", "https://arxiv.org/pdf/1907.02500", "Martin-Robertson SMDR: reference model point"),
    ("rpp2024-rev-standard-model.pdf", "https://pdg.lbl.gov/2024/reviews/rpp2024-rev-standard-model.pdf", "PDG 2024 electroweak review"),
    ("rpp2024-rev-qcd.pdf", "https://pdg.lbl.gov/2024/reviews/rpp2024-rev-qcd.pdf", "PDG 2024 QCD review"),
    ("rpp2024-rev-top-quark.pdf", "https://pdg.lbl.gov/2024/reviews/rpp2024-rev-top-quark.pdf", "PDG 2024 top-quark review"),
    ("rpp2024-rev-w-mass.pdf", "https://pdg.lbl.gov/2024/reviews/rpp2024-rev-w-mass.pdf", "PDG 2024 W-mass review"),
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    man, fails = [], []
    for fn, url, note in SOURCES:
        p = os.path.join(SCRATCH, fn)
        if not os.path.exists(p):
            subprocess.run(["curl", "-sL", "-m", "120", "-o", p, url], check=False)
        ok = os.path.exists(p) and os.path.getsize(p) > 1000
        rec = dict(file=fn, url=url, note=note, exists=ok)
        if ok:
            rec.update(size=os.path.getsize(p), sha256=sha(p))
        man.append(rec)
        print(("  [ok]   " if ok else "  [MISSING] ") + fn + (f"  {rec.get('size')} bytes  sha256 {rec.get('sha256', '')[:16]}..." if ok else ""))
        if not ok:
            fails.append(fn)
    # sanity: every present PDF must begin with %PDF and every tgz with the gzip magic
    for rec in man:
        if not rec["exists"]:
            continue
        p = os.path.join(SCRATCH, rec["file"])
        with open(p, "rb") as f:
            head = f.read(4)
        good = (head[:4] == b"%PDF") if rec["file"].endswith(".pdf") else (head[:2] == b"\x1f\x8b")
        if MUT and rec["file"] == SOURCES[0][0]:
            good = False      # MUTATE: pretend the first file has the wrong magic
        if not good:
            fails.append("magic:" + rec["file"])
            print("  [FAIL] wrong file type: " + rec["file"])
    if not MUT:
        with open(os.path.join(HERE, "y1_0_manifest.json"), "w") as f:
            json.dump(man, f, indent=1)
    print(f"{len(man)} sources, {len(fails)} problems: {fails}")
    if MUT:
        print("MUTATE control: " + ("BITES (exit 1)" if fails else "BROKEN (exit 3)"))
        sys.exit(1 if fails else 3)
    sys.exit(0 if not fails else 2)


main()
