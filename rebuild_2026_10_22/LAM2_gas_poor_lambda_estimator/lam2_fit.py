"""LAM2 stage 1: pPXF LOSVD fit of each spec-lite in lam2_sample.csv, as frozen (fa14da563a): moments 6, degree 8, mdegree 0,
rest 3900-6800 A, pPXF emission mask plus 5577/6300 sky lines, instrumental FWHM from wdisp, E-MILES 9.0 (amendment A2).
One fit per spectrum. Single thread, preemptible: one JSON line per galaxy, done rows skipped, SIGTERM exits cleanly.
Run: python3 -I lam2_fit.py [N]   (N = fit only the first N, for testing; writes lam2_fit_testN.jsonl)"""
import os, sys, json, signal
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util, ppxf.sps_util as lib
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "_external_data")
SPD = os.path.join(EXT, "lam2_spectra_2026_11_03"); TPL = os.path.join(EXT, "lam2_templates_2026_11_03", "spectra_emiles_9.0.npz")
C = 299792.458; VELSCALE = C * np.log(10) * 1e-4; LO, HI = 3900.0, 6800.0
NTEST = int(sys.argv[1]) if len(sys.argv) > 1 else 0
OUT = os.path.join(HERE, f"lam2_fit_test{NTEST}.jsonl" if NTEST else "lam2_fit.jsonl")
stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term)

def fit(fn):
    h = fits.open(fn); t = h[1].data; z = float(h[2].data["Z"][0])
    lam = 10 ** t["loglam"] / (1 + z); s = (lam > LO) & (lam < HI)
    flux, ivar, mask, wd = t["flux"][s].astype(float), t["ivar"][s].astype(float), t["and_mask"][s], t["wdisp"][s].astype(float)
    lam = lam[s]; ln_lam = np.log(lam)
    fwhm = 2.355 * wd * lam * np.log(10) * 1e-4  # rest frame: observed FWHM and observed pixel both scale by 1/(1+z)
    med = np.nanmedian(flux[ivar > 0]); flux = flux / med
    noise = np.where(ivar > 0, 1 / np.sqrt(np.clip(ivar, 1e-30, None)) / med, 1e10)
    sps = lib.sps_lib(TPL, VELSCALE, fwhm_gal={"lam": lam, "fwhm": fwhm}, norm_range=[5070, 5950], lam_range=[3500, 7300])
    temps = sps.templates.reshape(sps.templates.shape[0], -1)
    lam_t = np.exp(sps.ln_lam_temp[[0, -1]])
    good = util.determine_goodpixels(ln_lam, lam_t, 0)
    obs = lam * (1 + z); sky = (np.abs(obs - 5577.3) < 5) | (np.abs(obs - 6300.3) < 5)
    keep = np.zeros(len(lam), bool); keep[good] = True; keep &= (ivar > 0) & (mask == 0) & ~sky & np.isfinite(flux)
    sig0 = float(h[2].data["VDISP"][0]) if "VDISP" in h[2].columns.names else 200.0
    pp = ppxf(temps, flux, noise, VELSCALE, [0.0, max(sig0, 80.0)], goodpixels=np.flatnonzero(keep), moments=6, degree=8,
              mdegree=0, lam=lam, lam_temp=sps.lam_temp, quiet=True)
    err = pp.error * np.sqrt(pp.chi2)
    return dict(V=pp.sol[0], sigma=pp.sol[1], h3=pp.sol[2], h4=pp.sol[3], h5=pp.sol[4], h6=pp.sol[5],
                eV=err[0], esigma=err[1], eh3=err[2], eh4=err[3], eh5=err[4], eh6=err[5], chi2=float(pp.chi2), ngood=int(keep.sum()), z=z)

a = np.loadtxt(os.path.join(HERE, "lam2_sample.csv"), delimiter=",", skiprows=1, dtype=str)
if NTEST: a = a[:NTEST]
done = set()
if os.path.exists(OUT): done = {json.loads(l)["specobjid"] for l in open(OUT) if l.strip()}
with open(OUT, "a") as fo:
    for row in a:
        if stop: print("SIGTERM: stopping cleanly", flush=True); break
        sid, pl, mj, fb = row[1], int(row[2]), int(row[3]), int(row[4])
        if sid in done: continue
        fn = os.path.join(SPD, f"spec-{pl:04d}-{mj}-{fb:04d}.fits")
        if not os.path.exists(fn): continue
        try: r = fit(fn); r["status"] = "ok"
        except Exception as e: r = dict(status=f"error: {e}")
        r.update(specobjid=sid, dynpop_row=int(row[0])); fo.write(json.dumps(r, default=float) + "\n"); fo.flush()
print("fitted", sum(1 for _ in open(OUT)), "rows in", OUT, flush=True)
