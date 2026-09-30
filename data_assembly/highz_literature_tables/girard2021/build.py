#!/usr/bin/env python3
"""Parse Tables 1 and 2 of Girard et al. 2021 (arXiv:2101.04122, 'Systematic difference between ionized and molecular gas velocity dispersion in z~1-2 disks and local analogues')
from the arXiv HTML page (fetched 2026-09-29; sha256 in manifest.json).  Table 1: z, M*, SFR, f_gas, v_rot (ionised and molecular), sigma_0 (ionised and molecular), reference.
Table 2: R_1/2 of SFR, CO and stars; hydrostatic and dynamical-equilibrium pressures.  Purpose: the same-galaxy ionised-vs-molecular dispersion pairs (the pressure-support axis).
Nothing is computed beyond checks and descriptive counts; the paper's own ratio (2.45 +- 0.38 after the thermal correction) is not recomputed here."""
import sys, os, json, hashlib, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from tabutil import *
SRC = os.path.join(HERE, "..", "raw_small", "arxiv_2101.04122_html_fetched_2026-09-29.html"); s = open(SRC, errors="ignore").read(); LOG = []
def log(m): LOG.append(m); print(m)
def tab(tid, names, text=()):
    out = []
    for r in rows(s, tid):
        if len(r) != len(names) + 1 or not re.match(r"^[A-Za-z0-9][A-Za-z0-9\-_ ]*$", r[0]) or r[0] in ("Galaxy",): continue
        d = {"galaxy": r[0]}
        for k, nm in enumerate(names, start=1):
            if nm in text: d[nm] = r[k]; continue
            v, lo, hi, fl = val(r[k]); d[nm] = v; d[nm + "_errlo"] = lo; d[nm + "_errhi"] = hi
            if fl: d[nm + "_flag"] = fl
        out.append(d)
    return out
T1 = tab("S1.T1.2", ["z", "Mstar_1e10Msun", "SFR_Msun_yr", "fgas", "vrot_ion_kms", "vrot_mol_kms", "sigma0_ion_kms", "sigma0_mol_kms", "reference"], text=("reference",))
T2 = tab("A2.T2.2", ["R12_SFR_kpc", "R12_CO_kpc", "R12_star_kpc", "logPH_ion", "logPH_mol", "logPH_mol_aCO", "logPDE_mol", "reference_radius"], text=("reference_radius",))
write(os.path.join(HERE, "girard2021_table1_galaxy_properties.csv"), T1); write(os.path.join(HERE, "girard2021_table2_radii_pressures.csv"), T2)
log(f"Table 1: {len(T1)} galaxies; Table 2: {len(T2)} galaxies; Table 1 galaxies missing from Table 2: {sorted(set(d['galaxy'] for d in T1) - set(d['galaxy'] for d in T2))}; Table 2 extras (local THINGS/HERACLES-type NGC galaxies): {sorted(set(d['galaxy'] for d in T2) - set(d['galaxy'] for d in T1))}")
both = [d for d in T1 if d["sigma0_ion_kms"] is not None and d["sigma0_mol_kms"] is not None]
log(f"galaxies with both sigma_0,ion and sigma_0,mol: {len(both)}; z range {min(d['z'] for d in T1):.3f}-{max(d['z'] for d in T1):.3f}; with z > 0.5: {sum(d['z'] > 0.5 for d in T1)}; z > 1: {sum(d['z'] > 1 for d in T1)}")
log("references: " + "; ".join(f"{k}={sum(d['reference']==k for d in T1)}" for k in sorted({d['reference'] for d in T1})))
log(f"sigma_ion > sigma_mol in {sum(d['sigma0_ion_kms'] > d['sigma0_mol_kms'] for d in both)} of {len(both)} (descriptive count)")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
json.dump(dict(source_html_sha256=hashlib.sha256(open(SRC, "rb").read()).hexdigest(), url="https://arxiv.org/html/2101.04122", fetched="2026-09-29", bytes=os.path.getsize(SRC)), open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
