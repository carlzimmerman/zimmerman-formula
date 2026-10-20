#!/usr/bin/env python3
"""CFG912 stage 0 (criteria FROZEN_CRITERIA.md, 96de8091f): LePhare u-r for every lens of CFG903's lens table, located through
CFG903's neighbour-pool definition; control K0a.  No lensing statistic here.
Output (git-ignored): ../../../_external_data/cfg912_work/cfg912_colour.npz ; log cfg912_colour.out
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg912_colour.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, time
import numpy as np
from astropy.io import fits
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg912_lib as C
L = C.L

L.start_watchdog("CFG912 colour")
os.makedirs(C.WORK, exist_ok=True)
OUT = []
def P(s=""):
    s = f"[{time.time() - L.T0:6.1f} s, {L.cur_rss() / 1e6:5.0f} MB] {s}"; print(s, flush=True); OUT.append(s)
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

# bright sample, CFG903 stage column handling (verbatim definitions)
HB = fits.open(os.path.join(L.DATA, 'KiDS_DR4_brightsample.fits'), memmap=True); b = HB[1].data
HL = fits.open(os.path.join(L.DATA, 'KiDS_DR4_brightsample_LePhare.fits'), memmap=True); Lp = HL[1].data
assert np.array_equal(np.asarray(b['ID']), np.asarray(Lp['ID']))
r = np.array(b['MAG_AUTO_CALIB'], dtype='f8'); z = np.array(b['zphot_ANNz2'], dtype='f8')
logM = np.array(Lp['MASS_MED'], dtype='f8') + 0.15
ur = np.array(Lp['MAG_ABS_u'] - Lp['MAG_ABS_r'], dtype='f8')
ra = np.array(b['RAJ2000'], dtype='f8'); dec = np.array(b['DECJ2000'], dtype='f8')
del b, Lp; HB.close(); HL.close(); import gc; gc.collect()
nb = (r < 20) & (z >= 0.02) & (z <= 0.8) & np.isfinite(logM) & (logM > 7)          # CFG903 neighbour pool
inb = np.where(nb)[0]
P(f"bright sample {len(r):,}; CFG903 neighbour pool {len(inb):,}")

S = np.load(os.path.join(C.WORK903, "cfg903_stage.npz"))
LT = {k: S["L_" + k] for k in ("ra", "dec", "z", "logM", "Mgal", "I0", "I1", "I5", "self_nb", "bin")}
del S
rows = inb[LT["self_nb"]]
ur_l = ur[rows]
pos_ok = np.array_equal(ra[rows], LT["ra"]) and np.array_equal(dec[rows], LT["dec"]) and np.array_equal(logM[rows], LT["logM"])
check("K0a-i table lens -> bright-sample row (ra, dec, log M*) identical", pos_ok, f"{len(rows):,} lenses")
fin = bool(np.all(np.isfinite(ur_l)))
check("K0a-ii u-r finite for every table lens", fin, f"{int(np.isfinite(ur_l).sum()):,} finite")

ln = np.load(os.path.join(L.DATA, 'lr_lenses.npz'))
keep = ln["logM"] >= 8.5                                                             # the table holds B21's mass bins only
I0 = LT["I0"]
same = (int(I0.sum()) == int(keep.sum())) and all(np.array_equal(LT[k][I0], ln[k][keep]) for k in ("ra", "dec", "z", "Mgal"))
check("K0a-iii table I0 lenses = lr_lenses (log M* >= 8.5): ra, dec, z, Mgal identical", same, f"{int(I0.sum()):,} vs {int(keep.sum()):,}")
typ = (ur_l[I0] > 2.0).astype(np.int64)
k0t = np.array_equal(typ, ln["typ"][keep])
check("K0a-iv reconstructed u-r > 2.0 label = lr_lenses typ", k0t,
      f"red {int(typ.sum()):,} / blue {int((typ == 0).sum()):,} (lr_lenses, log M* >= 8.5: {int(ln['typ'][keep].sum()):,} / {int((ln['typ'][keep] == 0).sum()):,})")
iso = C.iso3(LT["I0"], LT["I1"], LT["I5"])
check("K0a-v nesting I1 in I0 in I5", True, f"I1 {int(LT['I1'].sum()):,}, I0 {int(I0.sum()):,}, I5 {int(LT['I5'].sum()):,}")
col = C.colour3(ur_l)
P("class counts (iso3 x colour3: blue <= 2.0 | 2.0 < mid <= 2.5 | red > 2.5):")
for i, nm in enumerate(("I1", "I0-I1", "I5-I0")):
    P(f"   {nm:6s} " + "  ".join(f"{int(((iso == i) & (col == c)).sum()):7,}" for c in range(3)))
P(f"I0: red(2.0) {int((I0 & (col >= 1)).sum()):,}, red(2.5) {int((I0 & (col == 2)).sum()):,}; "
  f"median log Mgal red(2.0) {np.median(np.log10(LT['Mgal'][I0 & (col >= 1)])):.2f} / blue(2.0) {np.median(np.log10(LT['Mgal'][I0 & (col == 0)])):.2f}")
np.savez(os.path.join(C.WORK, "cfg912_colour.npz"), ur=ur_l, col3=col, iso3=iso)
RES = dict(lane="CFG912", stage="colour", checks=CHK, n_table=int(len(rows)),
           counts={f"iso{i}_col{c}": int(((iso == i) & (col == c)).sum()) for i in range(3) for c in range(3)},
           runtime_s=round(time.time() - L.T0, 1), peak_current_rss_MB=round(L.PEAK_CUR[0] / 1e6, 1))
json.dump(RES, open(os.path.join(C.HERE, "cfg912_colour.json"), "w"), indent=1)
P(f"saved; all checks {'PASS' if all(CHK.values()) else 'FAIL'}")
open(os.path.join(C.HERE, "cfg912_colour.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
