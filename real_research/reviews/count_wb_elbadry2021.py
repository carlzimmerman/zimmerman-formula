#!/usr/bin/env python3
"""Count CLEAN El-Badry+2021 wide binaries per separation bin beyond 30 kAU.

This answers the single number that decides whether the s^3 gate-opening law is measurable on Gaia DR3
today or has to wait for DR4. Requirement from mi_wb_exponent_pipeline_2026.py: ~2000 clean pairs per
bin to separate exponent 3 from the contaminant exponent 0.5 at ~5 sigma (~400/bin gives only ~2.3
sigma). COUNTS ONLY -- no fitting, no science claim here.
"""
import numpy as np
from astropy.io import fits

F = 'elbadry2021.fits.gz'
hdul = fits.open(F, memmap=True)
tb = hdul[1]
cols = [c.name for c in tb.columns]
print(f"rows: {tb.header['NAXIS2']}   columns: {len(cols)}")

def pick(*cands):
    for c in cands:
        if c in cols: return c
    low = {c.lower(): c for c in cols}
    for c in cands:
        if c.lower() in low: return low[c.lower()]
    return None

c_sep   = pick('sep_AU', 'sep_au', 'sepAU')
c_chan  = pick('R_chance_align', 'R_chance_align_1', 'Rchance')
c_ruwe1 = pick('ruwe1'); c_ruwe2 = pick('ruwe2')
c_plx1  = pick('parallax1'); c_type = pick('binary_type', 'type')
print("using columns:", dict(sep=c_sep, chance=c_chan, ruwe1=c_ruwe1, ruwe2=c_ruwe2,
                             plx1=c_plx1, btype=c_type))
if c_sep is None:
    print("SEP COLUMN NOT FOUND -- all columns:"); print(cols); raise SystemExit(1)

d = tb.data
sep = np.asarray(d[c_sep], dtype=float)                      # AU
plx = np.asarray(d[c_plx1], dtype=float) if c_plx1 else None
dist = 1000.0/plx if plx is not None else None               # pc

m = np.isfinite(sep)
print(f"\nstage cuts (each applied cumulatively):")
print(f"  finite sep                          : {m.sum():>10,}")
if dist is not None:
    m &= np.isfinite(dist) & (dist > 0) & (dist < 200.0)
    print(f"  + d < 200 pc                        : {m.sum():>10,}")
if c_chan:
    ch = np.asarray(d[c_chan], dtype=float)
    m &= np.isfinite(ch) & (ch < 0.1)
    print(f"  + R_chance_align < 0.1              : {m.sum():>10,}")
if c_ruwe1 and c_ruwe2:
    r1 = np.asarray(d[c_ruwe1], dtype=float); r2 = np.asarray(d[c_ruwe2], dtype=float)
    m &= np.isfinite(r1) & np.isfinite(r2) & (r1 < 1.4) & (r2 < 1.4)
    print(f"  + RUWE < 1.4 both components        : {m.sum():>10,}")
if c_type:
    t = np.asarray(d[c_type])
    ts = np.array([str(x).strip().upper() for x in t])
    m &= (ts == 'MSMS')
    print(f"  + binary_type == MSMS               : {m.sum():>10,}")

print(f"\nCLEAN SAMPLE: {m.sum():,} pairs\n")
EDGES = [30e3, 42e3, 59e3, 84e3, 118e3, 167e3, 236e3]        # log-spaced kAU edges -> 6 bins
NEED_5SIG, NEED_3SIG = 2000, 400
print(f"  {'bin [kAU]':>16}{'N clean':>12}{'vs 2000 (5sig)':>17}{'vs 400 (2.3sig)':>18}")
print("  "+"-"*70)
rows = []
for lo, hi in zip(EDGES[:-1], EDGES[1:]):
    n = int(((sep >= lo) & (sep < hi) & m).sum())
    rows.append(((lo/1e3, hi/1e3), n))
    print(f"  {f'{lo/1e3:.0f}-{hi/1e3:.0f}':>16}{n:>12,}"
          f"{('PASS' if n>=NEED_5SIG else 'short'):>17}{('PASS' if n>=NEED_3SIG else 'short'):>18}")
n50 = int(((sep >= 50e3) & m).sum())
n100 = int(((sep >= 100e3) & m).sum())
print(f"\n  total clean beyond  50 kAU: {n50:,}")
print(f"  total clean beyond 100 kAU: {n100:,}")
nb5 = sum(1 for _, n in rows if n >= NEED_5SIG)
nb3 = sum(1 for _, n in rows if n >= NEED_3SIG)
print(f"\n  bins meeting the 5-sigma requirement (>=2000): {nb5} of {len(rows)}")
print(f"  bins meeting the 2.3-sigma level    (>=400) : {nb3} of {len(rows)}")
print("\n  VERDICT: " + (
    "MEASURABLE ON DR3 NOW -- enough bins clear the shape-test requirement." if nb5 >= 3 else
    "PARTIAL -- some bins clear 400 but not 2000; a reduced-bin fit may work, else DR4." if nb3 >= 3 else
    "NOT MEASURABLE ON DR3 -- the >50 kAU clean sample is too small; waits for DR4."))
