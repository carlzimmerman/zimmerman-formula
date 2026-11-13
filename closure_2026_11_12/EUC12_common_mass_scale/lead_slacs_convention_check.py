#!/usr/bin/env python3
"""EUC12, lead's check (2026-11-12, after the lane's RESULT): why the record's SLACS reference (+0.082 / +0.070)
is not reproduced when SLACS is treated the way Euclid's lenses are.

Two stellar-mass conventions for the same SLACS lenses, law S, lensing at the true source redshifts, through EUC1's
own machinery (imported, not rewritten):
  (a) the record's (EUC1 K5, EUC5 J3/J4, A55/A70): total mass = Fs x Mass / M2D_frac(R_E; Re(V), n = 4), where Fs is
      Auger's Salpeter stellar fraction inside the Einstein radius and Mass is the Einstein mass;
  (b) like Euclid's lenses: Auger's total Salpeter stellar mass, column logMs.

Run from the repository root:  python3 -B closure_2026_11_12/EUC12_common_mass_scale/lead_slacs_convention_check.py
Writes lead_slacs_convention_check.out beside this file. kappa = 1/2 FITTED. Adopts nothing.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "EUC1_eclipse_saturation_ceiling"))
import euc1 as E  # noqa: E402

SLACS = os.path.join("real_research", "data", "slacs_auger2009_lenses.tsv")
EUC12_SLACS = os.path.join(HERE, "euc12_slacs.csv")
OUT = []


def P(s):
    OUT.append(s)
    print(s)


def fl(x):
    try:
        return float(x.strip())
    except Exception:
        return float("nan")


lines = [l.rstrip("\n") for l in open(SLACS, encoding="latin-1")]
hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
hdr = lines[hi].split("\t")
col = {c: i for i, c in enumerate(hdr)}
L = []
for l in lines[hi + 3:]:
    if not l.strip() or l.startswith("#"):
        continue
    r = l.split("\t")
    if len(r) < len(hdr):
        continue
    d = dict(name=r[col["SDSS"]].strip(), zl=fl(r[col["zlens"]]), zs=fl(r[col["zsrc"]]), RE=fl(r[col["RE"]]),
             lME=fl(r[col["Mass"]]), Fs=fl(r[col["Fs"]]), ReV=fl(r[col["Re(V)"]]), logMs=fl(r[col["logMs"]]))
    ok = all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["ReV"], d["logMs"]])) and d["RE"] > 0
    if ok:
        L.append(d)

P("EUC12 lead's check: SLACS under law S, two stellar-mass conventions (EUC1's machinery)")
P("lenses with both conventions available: %d" % len(L))
zl = np.array([d["zl"] for d in L])
zs = np.array([d["zs"] for d in L])
REs = np.array([d["RE"] for d in L]) * E.KPC
Res = np.array([d["ReV"] for d in L]) * E.ARCSEC * E.AUGER.DA(zl)
frac = E.M2D_frac(REs, Res, 4.0)
Ma = np.array([d["Fs"] * 10.0 ** d["lME"] for d in L]) / frac * E.MSUN
Mb = np.array([10.0 ** d["logMs"] for d in L]) * E.MSUN
dl = np.log10(Ma / Mb)
P("log10(mass (a) / mass (b)): median %+.4f, 16-84 %% [%+.3f, %+.3f]" % (np.median(dl), *np.percentile(dl, [16, 84])))
P("median light fraction inside R_E for n = 4 and Re(V): %.3f; median Fs x Mass / total mass (b): %.3f"
  % (np.median(frac), np.median(Ma * frac / Mb)))
Mmin = math.pi * REs ** 2 * E.AUGER.sigcr(zl, zs)
P("lensing b_med at the true source redshifts (canonical / alt):")
for tag, M in (("(a) record, Fs x Mass", Ma), ("(b) Auger total logMs", Mb)):
    eng = E.Engine(REs, Res, np.full(len(L), 4.0), M)
    bc = float(np.median(eng.solve_b(Mmin, 9.3603e-11, "S")))
    ba = float(np.median(eng.solve_b(Mmin, 1.132e-10, "S")))
    P("  %-22s %+.4f / %+.4f" % (tag, bc, ba))

# Dynamics on convention (b), from the lane's own per-lens table (published dispersions, 1.5 arcsec seeing),
# split into the lenses of the record's sample and the rest.
if os.path.exists(EUC12_SLACS):
    import csv
    rows = list(csv.DictReader(open(EUC12_SLACS)))
    names = {d["name"] for d in L}
    P("dynamics b_med on convention (b), published dispersions, from euc12_slacs.csv (canonical / alt):")
    for lab, sel in (("all rows", lambda n: True), ("record's sample", lambda n: n in names),
                     ("outside it", lambda n: n not in names)):
        c = np.array([fl(r["b_pub_canonical_1.5"]) for r in rows if sel(r["name"])])
        a = np.array([fl(r["b_pub_alt_1.5"]) for r in rows if sel(r["name"])])
        P("  %-16s N %2d  %+.4f / %+.4f" % (lab, int(np.isfinite(c).sum()), np.nanmedian(c), np.nanmedian(a)))
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "lead_slacs_convention_check.out"), "w").write("\n".join(OUT) + "\n")
