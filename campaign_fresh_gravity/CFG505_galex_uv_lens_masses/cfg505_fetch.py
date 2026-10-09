#!/usr/bin/env python3
"""CFG505 fetch: GALEX positional cross-match of the KiDS isolated-lens sample (stack P, 181,477 lenses; lr_lenses.npz as built by
real_research/reviews/lensing_rar/lr_esd_remeasure.py and used by CFG377 / CFG413 / CFG502 / CFG503).

Owner approval (2026-10-08, in chat): upload ONLY public sky coordinates (RA, Dec) to the CDS XMatch service and retrieve matched
GALEX FUV/NUV magnitudes. Nothing else is uploaded (no IDs, no masses, no redshifts). No other downloads.
  tables  vizier:II/335/galex_ais  (GUVcat_AIS, Bianchi+2017; the "gal_ais" table of the approval is named galex_ais in XMatch)
          vizier:II/312/mis        (GALEX GR5 MIS, Bianchi+2011; the deeper medium-imaging survey, where it covers the lenses)
  radius  3 arcsec (all counterparts within 3" returned; the nearest is chosen later, in cfg505_masses.py)
  chunks  20,000 coordinates per request
Output (data dir, not in git): ../../../_external_data/cfg505_work/xm_<table>.csv (+ the uploaded coordinate file) and FETCH_LOG.md
Run: nice -n 15 python3 cfg505_fetch.py
"""
import os, sys, time, hashlib, datetime
import numpy as np
import astropy.units as u
from astropy.table import Table, vstack
from astroquery.xmatch import XMatch

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg505_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
os.makedirs(WORK, exist_ok=True)
TABLES = {"galex_ais": "vizier:II/335/galex_ais", "gr5_mis": "vizier:II/312/mis"}
RADIUS = 3.0
CHUNK = 20000


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 22), b""):
            h.update(ch)
    return h.hexdigest()


ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
ra, dec = ln["ra"].astype(float), ln["dec"].astype(float)
up = Table([ra, dec], names=("ra", "dec"))
upf = os.path.join(WORK, "upload_coords_radec.csv")
up.write(upf, format="ascii.csv", overwrite=True, formats={"ra": "%.7f", "dec": "%.7f"})
print(f"lenses {len(ra)}; upload file columns {up.colnames} (RA, Dec only)", flush=True)

log = [f"\n## {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%MZ')} UTC: CFG505 GALEX cross-match (owner go in chat 2026-10-08)",
       f"- Service: CDS XMatch (astroquery.xmatch {__import__('astroquery').__version__}); uploaded columns: ra, dec only "
       f"({len(ra)} KiDS isolated lenses, stack P of lr_lenses.npz); radius {RADIUS} arcsec; {CHUNK} rows per request.",
       f"- Uploaded coordinate file: upload_coords_radec.csv, sha256 {sha(upf)}"]
for key, tab in TABLES.items():
    out = os.path.join(WORK, f"xm_{key}.csv")
    if os.path.exists(out):
        print(f"{key}: exists, skipped", flush=True)
        continue
    parts = []
    t0 = time.time()
    for i0 in range(0, len(ra), CHUNK):
        sub = up[i0:i0 + CHUNK]
        for attempt in range(4):
            try:
                r = XMatch.query(cat1=sub, cat2=tab, max_distance=RADIUS * u.arcsec, colRA1="ra", colDec1="dec")
                break
            except Exception as e:                       # transient service errors: retry with back-off
                print(f"  {key} chunk {i0}: attempt {attempt + 1} failed: {type(e).__name__}: {str(e)[:200]}", flush=True)
                time.sleep(20 * (attempt + 1))
        else:
            sys.exit(f"{key}: chunk {i0} failed four times")
        parts.append(r)
        print(f"  {key}: rows {i0 + len(sub)}/{len(ra)} -> {len(r)} matches ({time.time() - t0:.0f} s)", flush=True)
    T = vstack(parts, metadata_conflicts="silent")
    T.write(out, format="ascii.csv", overwrite=True)
    log.append(f"- Table {tab}: {len(T)} match rows (all counterparts within {RADIUS}\"), {len(T.colnames)} columns; "
               f"file xm_{key}.csv, {os.path.getsize(out)} B, sha256 {sha(out)}")
    print(f"{key}: {len(T)} rows -> xm_{key}.csv", flush=True)
log.append("- Content treated as data only. The Menard/Anthropic inpainted UV sky map was NOT used.")
FL = os.path.join(WORK, "FETCH_LOG.md")
new = not os.path.exists(FL)
with open(FL, "a") as f:
    if new:
        f.write("# FETCH_LOG (cfg505_work)\n")
    f.write("\n".join(log) + "\n")
print("done")
