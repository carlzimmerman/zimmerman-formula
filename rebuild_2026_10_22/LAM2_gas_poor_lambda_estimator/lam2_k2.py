"""LAM2 K2, h4 recovery (criteria fa14da563a): 200 synthetic spectra per S/N tercile of the gas-poor sample. Each takes a random
gas-poor galaxy's best-fit template mix (its own frozen fit setup), convolves it with a Gauss-Hermite LOSVD (sigma drawn from the
sample's velDisp, h4 uniform in [-0.10, 0.10], h3 = h5 = h6 = 0), adds Gaussian noise with that galaxy's own noise vector, and refits
with the frozen setup. Pass: recovered h4 rms <= 0.03 over all 600. Single thread, preemptible (JSON line per synthetic).
Run: python3 -I lam2_k2.py"""
import os, json, signal
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util, ppxf.sps_util as lib
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "_external_data")
SPD = os.path.join(EXT, "lam2_spectra_2026_11_03"); TPL = os.path.join(EXT, "lam2_templates_2026_11_03", "spectra_emiles_9.0.npz")
C = 299792.458; VELSCALE = C * np.log(10) * 1e-4; LO, HI = 3900.0, 6800.0; SEED = 20261103
OUT = os.path.join(HERE, "lam2_k2.jsonl"); stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term)

def prep(fn):
    """Same steps as lam2_fit.fit, up to the fit."""
    h = fits.open(fn); t = h[1].data; z = float(h[2].data["Z"][0])
    lam = 10 ** t["loglam"] / (1 + z); s = (lam > LO) & (lam < HI)
    flux, ivar, mask, wd = t["flux"][s].astype(float), t["ivar"][s].astype(float), t["and_mask"][s], t["wdisp"][s].astype(float)
    lam = lam[s]; ln_lam = np.log(lam); fwhm = 2.355 * wd * lam * np.log(10) * 1e-4
    med = np.nanmedian(flux[ivar > 0]); flux = flux / med
    noise = np.where(ivar > 0, 1 / np.sqrt(np.clip(ivar, 1e-30, None)) / med, 1e10)
    sps = lib.sps_lib(TPL, VELSCALE, fwhm_gal={"lam": lam, "fwhm": fwhm}, norm_range=[5070, 5950], lam_range=[3500, 7300])
    temps = sps.templates.reshape(sps.templates.shape[0], -1)
    good = util.determine_goodpixels(ln_lam, np.exp(sps.ln_lam_temp[[0, -1]]), 0)
    obs = lam * (1 + z); sky = (np.abs(obs - 5577.3) < 5) | (np.abs(obs - 6300.3) < 5)
    keep = np.zeros(len(lam), bool); keep[good] = True; keep &= (ivar > 0) & (mask == 0) & ~sky & np.isfinite(flux)
    sig0 = float(h[2].data["VDISP"][0]) if "VDISP" in h[2].columns.names else 200.0
    return dict(flux=flux, noise=noise, lam=lam, temps=temps, lam_temp=sps.lam_temp, good=np.flatnonzero(keep), sig0=max(sig0, 80.0))

def run(p, flux, temps=None, start=None, fixed=None, degree=8, moments=6):
    return ppxf(p["temps"] if temps is None else temps, flux, p["noise"], VELSCALE, start or [0.0, p["sig0"]], goodpixels=p["good"],
                moments=moments, degree=degree, mdegree=0, lam=p["lam"], lam_temp=p["lam_temp"], quiet=True, fixed=fixed)

a = np.loadtxt(os.path.join(HERE, "lam2_sample.csv"), delimiter=",", skiprows=1, dtype=str)
L = {}
import glob
for fn in sorted(glob.glob(os.path.join(EXT, "lam2_sdss_lines_2026_11_03", "lines_*.csv"))):
    for l in open(fn).read().splitlines()[2:]:
        c = l.split(","); L[c[0]] = (float(c[6] or "nan"), float(c[4] or "nan"))  # snMedian, velDisp
poor = a[a[:, 5] == "1"]; sn = np.array([L[s][0] for s in poor[:, 1]]); vd = np.array([L[s][1] for s in poor[:, 1]])
edges = np.percentile(sn, [0, 100 / 3, 200 / 3, 100]); rng = np.random.default_rng(SEED)
plan = []
for k in range(3):
    idx = np.flatnonzero((sn >= edges[k]) & (sn <= edges[k + 1]))
    for i in range(200): plan.append((k, i, int(rng.choice(idx)), float(rng.choice(vd)), float(rng.uniform(-0.10, 0.10)), int(rng.integers(2**31))))
done = {(json.loads(l)["tercile"], json.loads(l)["i"]) for l in open(OUT)} if os.path.exists(OUT) else set()
with open(OUT, "a") as fo:
    for k, i, gi, sig, h4, ns in plan:
        if stop: print("SIGTERM: stopping cleanly", flush=True); break
        if (k, i) in done: continue
        sid, pl, mj, fb = poor[gi, 1], int(poor[gi, 2]), int(poor[gi, 3]), int(poor[gi, 4])
        fn = os.path.join(SPD, f"spec-{pl:04d}-{mj}-{fb:04d}.fits"); r = dict(tercile=k, i=i, specobjid=sid, sigma_in=sig, h4_in=h4, sn=float(sn[gi]))
        try:
            p = prep(fn); pp = run(p, p["flux"])                      # the galaxy's own frozen fit
            tpl = p["temps"] @ pp.weights                             # best-fit template mix, no polynomial
            mod = run(p, p["flux"], temps=tpl[:, None], start=[0.0, sig, 0.0, h4, 0.0, 0.0], fixed=[1] * 6, degree=-1).bestfit
            mod = mod / np.median(mod[p["good"]])
            syn = mod + np.random.default_rng(ns).normal(0, 1, mod.size) * np.where(p["noise"] < 1e9, p["noise"], 0)
            q = run(p, syn); r.update(status="ok", sigma_out=float(q.sol[1]), h4_out=float(q.sol[3]), h3_out=float(q.sol[2]), h6_out=float(q.sol[5]))
        except Exception as e: r["status"] = f"error: {e}"
        fo.write(json.dumps(r) + "\n"); fo.flush()
rows = [json.loads(l) for l in open(OUT)]; ok = [x for x in rows if x["status"] == "ok"]
if len(rows) == len(plan):
    d = np.array([x["h4_out"] - x["h4_in"] for x in ok]); rms = float(np.sqrt(np.mean(d**2)))
    out = [f"K2: {len(ok)} of {len(plan)} synthetic fits ok; recovered h4 rms {rms:.4f} (need <= 0.03): {'PASS' if rms <= 0.03 else 'FAIL -> STOP: h4 NOT MEASURABLE'}"]
    for k in range(3):
        dk = np.array([x["h4_out"] - x["h4_in"] for x in ok if x["tercile"] == k])
        out.append(f"  S/N tercile {k} ({edges[k]:.1f}-{edges[k + 1]:.1f}): rms {np.sqrt(np.mean(dk**2)):.4f}, bias {np.mean(dk):+.4f}, n {len(dk)}")
    hi = np.array([x["h4_in"] for x in ok]); ho = np.array([x["h4_out"] for x in ok])
    out.append(f"  slope of h4_out on h4_in {np.polyfit(hi, ho, 1)[0]:.3f}; sigma_out/sigma_in median {np.median([x['sigma_out'] / x['sigma_in'] for x in ok]):.3f}")
    print("\n".join(out)); open(os.path.join(HERE, "lam2_k2.out"), "w").write("\n".join(out) + "\n")
    json.dump(dict(rms=rms, pass_=bool(rms <= 0.03), n_ok=len(ok), n=len(plan)), open(os.path.join(HERE, "lam2_k2.json"), "w"), indent=1)
else: print(f"K2 partial: {len(rows)} of {len(plan)}")
