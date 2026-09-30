#!/usr/bin/env python3
"""Single-epoch DESI MWS radial velocities for the matched components: from rvtab_spectra files (rv_output/240521/healpix/...), every spectrum (exposure/tile combination) of each matched TARGETID.
Descriptive RV-variability indicators per target: number of epochs, weighted-mean RV, chi2 about it with the catalogue errors, and peak-to-peak.  Output desi_mws_epochs.csv and desi_mws_epoch_stats.json."""
import csv, glob, json, os, numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.expanduser("~/new_physics/_external_data/desi_mws/rvtab_spectra")
M = list(csv.DictReader(open(os.path.join(HERE, "desi_mws_matches.csv"))))
need = {}
for r in M: need.setdefault((r["survey"], r["program"], int(r["healpix"])), {})[int(r["targetid"])] = int(r["source_id"])
rows = []; missing = 0
for (sv, pg, hp), tids in need.items():
    path = os.path.join(SP, f"rvtab_spectra-{sv}-{pg}-{hp}.fits")
    if not os.path.exists(path): missing += 1; continue
    h = fits.open(path, memmap=False); rv = h["RVTAB"].data; tid = np.array(rv["TARGETID"]); fm = h["FIBERMAP"].data if "FIBERMAP" in [x.name for x in h] else None
    for t, src in tids.items():
        for k in np.where(tid == t)[0]:
            rows.append(dict(source_id=src, survey=sv, program=pg, healpix=hp, targetid=t, vrad=float(rv["VRAD"][k]), vrad_err=float(rv["VRAD_ERR"][k]), rvs_warn=int(rv["RVS_WARN"][k]), sn_r=float(rv["SN_R"][k]), success=int(bool(rv["SUCCESS"][k])),
                             mjd=float(fm["MJD"][k]) if fm is not None and "MJD" in fm.columns.names else float("nan"), tileid=int(fm["TILEID"][k]) if fm is not None and "TILEID" in fm.columns.names else -1))
print("matched (survey, program, pixel) groups:", len(need), "spectra files missing:", missing, "epoch rows:", len(rows))
if rows:
    w = csv.DictWriter(open(os.path.join(HERE, "desi_mws_epochs.csv"), "w", newline=""), fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
by = {}
for r in rows:
    if r["rvs_warn"] == 0 and r["success"] == 1 and np.isfinite(r["vrad"]) and r["vrad_err"] > 0: by.setdefault(r["source_id"], []).append(r)
st = []
for s, L in by.items():
    v = np.array([x["vrad"] for x in L]); e = np.array([x["vrad_err"] for x in L]); n = len(L)
    if n >= 2:
        wm = np.sum(v / e**2) / np.sum(1 / e**2); chi2 = float(np.sum(((v - wm) / e) ** 2)); st.append(dict(source_id=s, n=n, p2p=float(v.max() - v.min()), chi2=chi2, dof=n - 1))
json.dump(dict(groups=len(need), missing=missing, epoch_rows=len(rows), targets_with_good_epochs=len(by), targets_with_ge2_epochs=len(st), ge2_p2p_median=float(np.median([x["p2p"] for x in st])) if st else None,
               n_chi2_over_3_per_dof=sum(1 for x in st if x["chi2"] / x["dof"] > 3), detail=st), open(os.path.join(HERE, "desi_mws_epoch_stats.json"), "w"), indent=0)
print("targets with >=1 good epoch:", len(by), "; with >=2:", len(st), "; chi2/dof > 3 (catalogue errors only, no 1 km/s floor):", sum(1 for x in st if x["chi2"] / x["dof"] > 3))
