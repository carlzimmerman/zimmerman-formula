#!/usr/bin/env python3
"""SR1_r2_on_sluggs, post-result and reporting only (no class moves): (a) the decisive r_1/2 column recomputed from the raw TSVs with no machinery;
(b) ceiling and null rungs on the frozen split into 12 non-centrals and 4 centrals; (c) the catalogue against ATLAS3D's Chabrier inside r_1/2.
    OMP_NUM_THREADS=1 nice -n 15 python3 -B sr1_post.py   kappa = 1/2 FITTED; footings never pooled."""
import json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
R = json.load(open(os.path.join(HERE, "sr1_results.json")))
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def vz(fn):
    L = [l.rstrip("\n") for l in open(os.path.join(DATA, fn), encoding="latin-1") if l.strip() and not l.startswith("#")]
    k = next(i for i, l in enumerate(L) if set(l.replace("\t", "").strip()) <= set("- "))
    H = [h.strip() for h in L[k - 2].split("\t")]
    return [dict(zip(H, [x.strip() for x in l.split("\t")])) for l in L[k + 1:]]
SL = {"NGC" + r["NGC"]: r for r in vz("sluggs_forbes2017_galaxies.tsv")}
AL = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "atlas3d_fj_table.tsv")) if l.strip() and not l.startswith("#")]
A = {r[0]: dict(zip(AL[0], r)) for r in AL[1:]}
names = [g["name"] for g in R["galaxies"]]
AS = 1.0 / 206264.806
d0, c0 = [], []
for n in names:
    s, a = SL[n], A[n]
    D, DA = float(s["Dist"]), float(a["Dist_Mpc"])
    Re = float(s["Reff"]) * AS * D * 1e3; ah = Re / 1.8153
    r12 = 10 ** float(a["logr12"]) * AS * D * 1e3
    fH = r12 ** 2 / (r12 + ah) ** 2
    Mj = 10 ** (float(a["logML_JAM"]) + float(a["logL"])) * D / DA
    Ms = 10 ** float(s["logM*"])
    d0.append(math.log10(0.5 * Mj) - math.log10(fH * Ms))
    Mch = 10 ** (float(a["logML_Salp"]) + float(a["logL"]) - 0.25) * (D / DA) ** 2
    c0.append(math.log10(fH * Ms) - math.log10(0.5 * Mch))
d0 = np.array(d0); j = np.array(R["per_galaxy"]["stars"]["R0"]["r12"])
P("(a) Independent r_1/2 column from the raw TSVs, no machinery")
P(f"    max |d| against sr1_results.json, per galaxy: {np.max(np.abs(d0 - j)):.1e} dex (h50 rounds arcsec per radian, so up to about 1e-6 is expected)")
for k, dl in R["rungs"].items():
    P(f"    {k:2s} median d lg M at r_1/2: {np.median(d0 - dl):+.3f}, over M_dyn in {(d0 - dl < 0).sum()} of {len(d0)}")
P("\n(b) Rungs on the frozen split: median rung at the r_1/2 ceiling, median rung that zeroes 1-5 R_e, median gap")
cen = np.array([n in ("NGC4486", "NGC4365", "NGC4374", "NGC5846") for n in names])
for lab in ("stars", "law|canonical", "law|alt", "routeE|canonical", "routeE|alt", "native"):
    r = R["roots"][lab]; c, nu_, g = np.array(r["ceil"]), np.array(r["null"]), np.array(r["gap"])
    P(f"    {lab:18s} non-centrals (12): ceil {np.nanmedian(c[~cen]):+.3f}, null {np.nanmedian(nu_[~cen]):+.3f}, gap {np.nanmedian(g[~cen]):+.3f};  centrals (4): ceil {np.nanmedian(c[cen]):+.3f}, null {np.nanmedian(nu_[cen]):+.3f}, gap {np.nanmedian(g[cen]):+.3f}")
P("\n(c) Inside r_1/2: lg M*(catalogue, Hernquist) - lg M*(ATLAS3D Chabrier, half the same light), per galaxy")
c0 = np.array(c0)
P(f"    median {np.median(c0):+.3f}, range {c0.min():+.3f} to {c0.max():+.3f}; non-centrals {np.median(c0[~cen]):+.3f}, centrals {np.median(c0[cen]):+.3f}")
P("    " + ", ".join(f"{n} {v:+.2f}" for n, v in zip(names, c0)))
open(os.path.join(HERE, "sr1_post.out"), "w").write("\n".join(OUT) + "\n")
