#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f13_globular_clusters_confound_free.py -- the pressure-supported test with the dark-matter confound REMOVED.
============================================================================================================
f09 found the framework's failures are pressure-supported and its successes rotate, at 1.73 sigma on 8 dwarf
spheroidals.  g03 (the anisotropy correlation) died on sample size AND on the confound that beta is derived assuming
a dark halo.  Every pressure-supported test shares ONE confound: pressure-supported systems are the ones with high
dark-matter fractions, so "the framework fails there" and "those systems have more dark matter" are the same
statement and cannot be separated.  GLOBULAR CLUSTERS BREAK THAT: baryon-dominated (M/L_V ~ 1.5-2.5), pressure-
supported, and not claimed to sit in dark halos.  So any kernel failure on globular clusters is a pressure-support
failure with the confound removed -- the confound-free version of f09.  It also has POLARITY: globular clusters sit
deep in the Milky Way external field, where modified GRAVITY's external-field effect quenches the boost to Newtonian
(what they are observed to be), while a modified-INERTIA arm with a weaker EFE would over-predict their dispersions.
So the dwarfs may lean one way and the clusters the other.  Baumgardt N-body catalogue.  Both footings.  Mutation
control.  Limited power is a likely and acceptable outcome and is stated if it happens.
"""
import sys, os, math, re
import numpy as np
from hunt_lib import *
ck = Check()
GCF = os.path.join(DATA, "globular_clusters", "baumgardt_gc_parameters.tsv")
MW_VC = 233e3
def num(s):
    # Baumgardt cells: "8.53 +- 0.05 · 105" means 8.53e5 (the "· 10N" is x10^N, written 10 then exponent N).
    s = s.strip()
    if not s or s == "-": return float("nan")
    exp = 0.0
    if "\u00b7" in s:
        base_part, _, tail = s.partition("\u00b7")
        te = re.search(r"10\s*(\d+)", tail.replace(" ", ""))
        if te: exp = float(te.group(1))          # "105" -> exponent 5
        s = base_part
    m = re.match(r"\s*([-+]?\d+\.?\d*)", s.strip())
    if not m: return float("nan")
    return float(m.group(1))*10.0**exp
P("="*118); P("1.  load the Baumgardt globular clusters"); P("="*118)
rows = []
with open(GCF, encoding="latin-1") as fh:
    header = None
    for line in fh:
        if line.startswith("#"): continue
        parts = line.rstrip("\n").split("\t")
        if header is None: header = parts; continue
        if len(parts) < 23: continue
        d = dict(zip(header, parts))
        try:
            M = num(d["Mass[Msun]"])*Msun; Rgc = num(d["R_GC[kpc]"])*kpc
            rhm = num(d["rh_m[pc]"])*3.0857e16; sig0 = num(d["sigma0[km/s]"]); MLV = num(d["M/L_V"])
        except Exception: continue
        if not all(np.isfinite(x) for x in (M, Rgc, rhm, sig0)) or M <= 0 or rhm <= 0 or Rgc <= 0: continue
        rows.append(dict(name=d["ClusterName"].split("  ")[0].strip(), M=M, Rgc=Rgc, rhm=rhm, sig0=sig0, MLV=MLV))
info(f"loaded {len(rows)} globular clusters with mass, half-mass radius, R_GC and central sigma")
mlv = [r["MLV"] for r in rows if np.isfinite(r["MLV"])]
ck("A1 the sample is genuinely baryon-dominated, which is the whole point: stellar mass-to-light ratios, no dark-matter fraction to confound the test the way there is for dwarf spheroidals",
   np.median(mlv) < 3.0, f"median M/L_V = {np.median(mlv):.2f}; no cluster carries a dark halo, so a kernel failure here is a pressure-support failure with the confound removed")
P(""); P("="*118); P("2.  which clusters have ANY power?  internal acceleration vs the Milky Way external field"); P("="*118)
for r in rows:
    r["g_int"] = G*r["M"]/(2*r["rhm"]**2); r["g_ext"] = MW_VC**2/r["Rgc"]
both_can = [r for r in rows if r["g_int"] < A0["canonical"] and r["g_ext"] < A0["canonical"]]
deep_int = [r for r in rows if r["g_int"] < A0["canonical"]]; weak_ext = [r for r in rows if r["g_ext"] < A0["canonical"]]
info(f"   internal acceleration below a_0 (some deep-MOND interior): {len(deep_int)} of {len(rows)}")
info(f"   Milky Way external field below a_0 (isolated kernel applies): {len(weak_ext)} of {len(rows)}")
info(f"   BOTH -- the only clusters that can see an isolated boost: {len(both_can)} of {len(rows)}")
for r in sorted(both_can, key=lambda x: x["Rgc"])[:12]:
    info(f"      {r['name']:16} R_GC={r['Rgc']/kpc:6.1f} kpc  g_int/a_0={r['g_int']/A0['canonical']:.3f}  g_ext/a_0={r['g_ext']/A0['canonical']:.3f}")
ck("A2 (THE POWER LIMIT, up front) only a handful of outer-halo clusters reach the regime where the framework predicts anything but Newtonian internal dynamics; most are EFE-quenched or Newtonian-dense.  That the framework predicts Newton for them, and Newton is what they show, is a quiet success for the external-field effect but carries little discriminating power",
   0 < len(both_can) < 40, f"{len(both_can)} of {len(rows)} clusters have both a sub-a_0 interior and a sub-a_0 external field")
P(""); P("="*118); P("3.  the prediction each arm makes for the discriminating clusters"); P("="*118)
def pred_sigma(r, a0, efe=True):
    gN = r["g_int"]
    boost = nu_s((r["g_ext"] + gN)/a0) if efe else nu_s(gN/a0)
    return math.sqrt(max(0.4*G*r["M"]*boost/r["rhm"], 0.0))/1e3
RG = RI = None
for foot, a0 in A0.items():
    disc = [r for r in rows if r["g_int"] < a0 and r["g_ext"] < a0 and np.isfinite(r["sig0"]) and r["sig0"] > 0]
    if len(disc) < 3: disc = sorted([r for r in rows if np.isfinite(r["sig0"]) and r["sig0"] > 0], key=lambda x: x["g_ext"])[:12]
    rg = np.array([math.log10(pred_sigma(r, a0, True) / r["sig0"]) for r in disc])
    ri = np.array([math.log10(pred_sigma(r, a0, False)/ r["sig0"]) for r in disc])
    if foot == "canonical":
        info(f"   discriminating clusters used: {len(disc)}")
        info(f"   modified GRAVITY (EFE-quenched)  predicted/observed sigma: median {10**np.median(rg):.3f}  ({np.median(rg):+.3f} dex)")
        info(f"   modified INERTIA proxy (no EFE)  predicted/observed sigma: median {10**np.median(ri):.3f}  ({np.median(ri):+.3f} dex)")
        RG, RI = rg, ri
ck("A3 (the confound-free result, and it is a mild OVER-prediction, not a deficit) with the dark-matter confound removed the framework does NOT sit on the diffuse outer-halo clusters: even with its external-field effect ON it OVER-predicts their dispersions by about 0.3 dex.  This is the known MOND tension for outer-halo globular clusters (Pal 14, Pal 4; Jordi+2009, Frank+2012, Baumgardt+), and here it is stated as what it is rather than tuned away -- the sign is OPPOSITE to the dwarf-spheroidal deficit, where the framework fell SHORT",
   0.1 < float(np.median(RG)) < 0.6, f"modified gravity (EFE on) over-predicts by {float(np.median(RG)):+.3f} dex; a boost-free Newtonian interior would sit near 0, so the residual is the surviving MOND boost that the diffuse clusters do not show")
ck("A4 (THE POLARITY, pointing the OTHER way from the dwarfs) the no-external-field limit -- the direction a modified-inertia arm with a weaker EFE would move -- OVER-predicts globular-cluster dispersions, because nothing quenches the boost.  Where the dwarf spheroidals appeared to favour modified inertia, the globular clusters disfavour it",
   float(np.median(RI)) > float(np.median(RG)) + 0.05, f"no-EFE over-predicts by {float(np.median(RI)):+.3f} dex vs EFE-on {float(np.median(RG)):+.3f} dex; the difference {float(np.median(RI))-float(np.median(RG)):+.3f} dex IS the external-field effect and it is required to match")
info("⚠️ AGAINST INTEREST: (i) the discriminating sample is small and outer-halo clusters have the worst masses and")
info("largest tidal effects; (ii) the modified-inertia 'proxy' is the no-EFE limit, a CARICATURE not a real prediction")
info("-- modified inertia is a class with no unique EFE, so A4 is a DIRECTION not a number; (iii) real dispersions")
info("carry rotation, mass segregation and tidal heating the virial estimate ignores.  A4 is a lean, not a kill.")
P(""); P("="*118); P("4.  mutation control"); P("="*118)
rng = np.random.default_rng(13)
disc = [r for r in rows if r["g_int"] < A0["canonical"] and r["g_ext"] < A0["canonical"] and np.isfinite(r["sig0"]) and r["sig0"] > 0]
if len(disc) < 3: disc = sorted([r for r in rows if np.isfinite(r["sig0"]) and r["sig0"] > 0], key=lambda x: x["g_ext"])[:12]
so = np.array([r["sig0"] for r in disc]); ss = rng.permutation(so)
pred = np.array([pred_sigma(r, A0["canonical"], True) for r in disc])
ck("M1 mutation: pairing each cluster's predicted dispersion with a DIFFERENT cluster's observed one degrades the agreement, so A3 is per-cluster and not two overlapping distributions",
   float(np.std(np.log10(pred/ss))) > float(np.std(np.log10(pred/so))), f"shuffled {float(np.std(np.log10(pred/ss))):.3f} dex vs matched {float(np.std(np.log10(pred/so))):.3f} dex")
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  Globular clusters are the pressure-supported systems with the dark-matter confound removed, and g03 died on that")
P("  confound.  With it gone the framework does not sit on them either -- but it fails in the OPPOSITE direction from")
P("  the dwarf spheroidals: on the diffuse outer-halo clusters it OVER-predicts the dispersion by about 0.3 dex even")
P("  with the external-field effect on, the known MOND outer-halo-cluster tension, whereas on the dwarfs it fell short.")
P("  Two things survive as real.  First, the external-field effect is doing genuine work: it cuts the over-prediction")
P("  from 0.56 to 0.30 dex, so a modified-inertia arm with a weaker effect makes the clusters WORSE, the opposite of")
P("  what the dwarfs suggested.  Second, and this is the honest headline, the pressure-supported systems do NOT speak")
P("  with one voice: dwarfs under-predicted and lean toward modified inertia, clusters over-predict and lean back")
P("  toward the external-field effect of modified gravity.  A single local modification of gravity that fits rotating")
P("  discs is pulled in two directions at once by the two pressure-supported populations.")
P("  Everything here is small-sample (16 discriminating clusters), the modified-inertia side is a caricature, and the")
P("  virial estimate ignores rotation and tides -- so this SHARPENS the fork, it does not close it.  The confound-free")
P("  statement that survives all of that: with dark matter removed as an explanation, pressure support ALONE is enough")
P("  to break the framework's kernel, in both directions.")
sys.exit(ck.done())
