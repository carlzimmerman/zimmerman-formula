#!/usr/bin/env python3
"""Cross-match the fetched DESI DR1 MWS per-pixel rvtab files with our wide-binary components.
Keys: (1) REF_ID == Gaia source_id (REF_CAT 'G2' = Gaia DR2 ids; they equal DR3 ids for most stars) ; (2) for rows with REF_ID == 0 or no id match, a position match within 1.5 arcsec to the Gaia position moved back to 2015.5.
Every DESI row that matches one of our components is kept (repeats, several programs).  Output desi_mws_matches.csv; summary desi_mws_crossmatch_summary.json.  No gravity inference is made here."""
import csv, glob, json, os, sys, numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); WB = os.path.join(HERE, "..", "..", "real_research", "data", "widebinaries", "dr3_extract")
RV = os.path.expanduser("~/new_physics/_external_data/desi_mws/rvtab")
pairs = {}
for fn in ("wide_binaries_dr3.csv", "wide_binaries_dr3_elbadryR.csv"):
    pairs[fn] = [(int(r["source_id1"]), int(r["source_id2"])) for r in csv.DictReader(open(os.path.join(WB, fn)))]
ids = sorted({i for p in pairs.values() for pr in p for i in pr})
G = {}
for f in sorted(glob.glob(os.path.join(WB, "chunk_*.fits"))):
    d = fits.open(f, memmap=True)[1].data; sid = np.array(d["source_id"]); m = np.isin(sid, ids)
    for i in np.where(m)[0]: G[int(sid[i])] = dict(ra=float(d["ra"][i]), dec=float(d["dec"][i]), pmra=float(d["pmra"][i]), pmdec=float(d["pmdec"][i]), g=float(d["phot_g_mean_mag"][i]), rv=float(d["radial_velocity"][i]), rve=float(d["radial_velocity_error"][i]))
print("components:", len(ids), "with Gaia record:", len(G))
# positions at epoch 2015.5
pos = {}
for i, v in G.items():
    dec = np.radians(v["dec"]); dt = -0.5 / 3.6e6
    ra15 = v["ra"] + (v["pmra"] if np.isfinite(v["pmra"]) else 0) * dt / np.cos(dec); dec15 = v["dec"] + (v["pmdec"] if np.isfinite(v["pmdec"]) else 0) * dt
    pos[i] = (ra15, dec15)
byhpx = {}
for i in ids: byhpx.setdefault(i >> 47, []).append(i)
out = []; nfiles = 0; nrows = 0
def dec_(x): return x.decode().strip() if isinstance(x, bytes) else str(x).strip()
for path in sorted(glob.glob(os.path.join(RV, "rvtab_coadd-*.fits"))):
    base = os.path.basename(path)[len("rvtab_coadd-"):-5]; sv, pg, hp = base.split("-"); hp = int(hp)
    try: h = fits.open(path, memmap=False); rv = h["RVTAB"].data; fm = h["FIBERMAP"].data
    except Exception as e: print("bad file", path, e); continue
    nfiles += 1; nrows += len(rv)
    cand = byhpx.get(hp, [])
    if not cand: continue
    rid = np.array(rv["REF_ID"]).astype(np.int64); ra = np.array(rv["TARGET_RA"]); dec = np.array(rv["TARGET_DEC"])
    cs = set(cand)
    for k in range(len(rv)):
        src = None; how = None; sep = None
        if int(rid[k]) in cs: src = int(rid[k]); how = "ref_id"
        if src is None:
            for i in cand:
                r0, d0 = pos[i]; s = 3600 * np.hypot((ra[k] - r0) * np.cos(np.radians(d0)), dec[k] - d0)
                if s < 1.5 and (src is None or s < sep): src, sep, how = i, s, "position"
        if src is None: continue
        if sep is None: r0, d0 = pos[src]; sep = 3600 * np.hypot((ra[k] - r0) * np.cos(np.radians(d0)), dec[k] - d0)
        out.append(dict(source_id=src, survey=sv, program=pg, healpix=hp, match=how, sep_arcsec=round(float(sep), 3), targetid=int(rv["TARGETID"][k]), ref_id=int(rid[k]), ref_cat=dec_(rv["REF_CAT"][k]), vrad=float(rv["VRAD"][k]), vrad_err=float(rv["VRAD_ERR"][k]), vrad_skew=float(rv["VRAD_SKEW"][k]),
                        rvs_warn=int(rv["RVS_WARN"][k]), vsini=float(rv["VSINI"][k]), sn_b=float(rv["SN_B"][k]), sn_r=float(rv["SN_R"][k]), sn_z=float(rv["SN_Z"][k]), success=int(bool(rv["SUCCESS"][k])), rr_spectype=dec_(rv["RR_SPECTYPE"][k]),
                        teff=float(rv["TEFF"][k]), logg=float(rv["LOGG"][k]), feh=float(rv["FEH"][k]), fiberstatus=int(fm["COADD_FIBERSTATUS"][k]), numexp=int(fm["COADD_NUMEXP"][k]), exptime=float(fm["COADD_EXPTIME"][k]),
                        mws_target=int(fm["MWS_TARGET"][k]), desi_g=float(fm["GAIA_PHOT_G_MEAN_MAG"][k]), gaia_g=G[src]["g"], gaia_rv=G[src]["rv"], gaia_rv_err=G[src]["rve"]))
print("files read", nfiles, "rows", nrows, "matched rows", len(out))
keys = list(out[0].keys()); w = csv.DictWriter(open(os.path.join(HERE, "desi_mws_matches.csv"), "w", newline=""), fieldnames=keys); w.writeheader(); w.writerows(out)
json.dump(dict(files=nfiles, rows=nrows, matched_rows=len(out)), open(os.path.join(HERE, "desi_mws_crossmatch_summary.json"), "w"))
