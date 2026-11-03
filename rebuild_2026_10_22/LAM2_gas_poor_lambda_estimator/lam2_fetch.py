"""LAM2 stage-0 fetch (criteria fa14da563a): SpecObj + MPA-JHU galSpecLine/galSpecIndx for DynPop Qual>=1 galaxies matched
to an SDSS DR17 SpecObj within 1 arcsec (LAM1's match). Run: python3 -I lam2_fetch.py. Writes _external_data/lam2_sdss_lines_2026_11_03/."""
import os, glob, math, time, urllib.parse, urllib.request, numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); EXT = os.path.join(ROOT, "_external_data")
OUTD = os.path.join(EXT, "lam2_sdss_lines_2026_11_03"); os.makedirs(OUTD, exist_ok=True)
URL = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch"
COLS = ("s.specobjid,s.plate,s.mjd,s.fiberID,s.velDisp,s.velDispErr,s.snMedian,l.h_alpha_eqw,l.h_alpha_flux,l.h_alpha_flux_err,"
        "l.sigma_balmer,i.d4000_n,i.lick_mgb,i.lick_fe5270,i.lick_hd_a")

def unit(ra, dec):
    r, d = np.radians(ra), np.radians(dec); return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]
dp = fits.open(os.path.join(EXT, "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits"))[1].data
good = (dp["Qual"] >= 1) & np.isfinite(dp["Lambda_Re"]) & np.isfinite(dp["Eps_MGE"]) & (dp["Eps_MGE"] >= 0)
ids = []
for fn in sorted(glob.glob(os.path.join(EXT, "lam1_sdss_specobj_2026_11_03", "dyn_ra*.csv"))):
    a = np.genfromtxt(fn, delimiter=",", skip_header=2, dtype=None, encoding=None)
    if a.size: ids += [(int(r[0]), float(r[1]), float(r[2])) for r in np.atleast_1d(a)]
sid = np.array([r[0] for r in ids], dtype=np.uint64); ra = np.array([r[1] for r in ids]); de = np.array([r[2] for r in ids])
d, j = cKDTree(unit(ra, de)).query(unit(dp["obj_ra"], dp["obj_dec"]), distance_upper_bound=2 * math.sin(math.radians(1 / 3600) / 2))
hit = good & np.isfinite(d)
want = sorted(set(int(x) for x in sid[j[hit]]))
print(f"matched DynPop {int(hit.sum())}, unique specobjid {len(want)}", flush=True)
np.savetxt(os.path.join(OUTD, "dynpop_match.csv"), np.c_[np.flatnonzero(hit), sid[j[hit]].astype(np.int64)], fmt="%d", delimiter=",",
           header="dynpop_row,specobjid", comments="")
total = 0
for k in range(0, len(want), 250):
    fn = os.path.join(OUTD, f"lines_{k // 250:03d}.csv")
    if os.path.exists(fn): total += os.path.getsize(fn); continue
    q = f"SELECT {COLS} FROM SpecObj s LEFT JOIN galSpecLine l ON l.specobjid=s.specobjid LEFT JOIN galSpecIndx i ON i.specobjid=s.specobjid WHERE s.specobjid IN ({','.join(map(str, want[k:k + 250]))})"
    for t in range(3):
        try:
            body = urllib.request.urlopen(URL + "?" + urllib.parse.urlencode({"cmd": q, "format": "csv"}), timeout=120).read(); break
        except Exception as e:
            print(f"  chunk {k // 250} try {t}: {e}", flush=True); time.sleep(5)
    else: raise SystemExit("fetch failed")
    open(fn, "wb").write(body); total += len(body)
print(f"wrote {len(glob.glob(os.path.join(OUTD, 'lines_*.csv')))} chunks, {total} bytes", flush=True)
