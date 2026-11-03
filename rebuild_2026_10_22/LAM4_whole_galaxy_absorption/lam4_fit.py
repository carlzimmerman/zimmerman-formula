"""LAM4: pPXF fit of each integrated spectrum (criteria 1023fbaae9). LAM2's settings; rest window starts at the first
lambda >= 3900 A where the galaxy's rest FWHM >= 2.51 A (E-MILES). One fit per galaxy. Single thread, preemptible.
Run: python3 -I lam4_fit.py            (fits every saved sum not yet fitted; writes lam4_fit.jsonl)
     python3 -I lam4_fit.py --k2       (K2: 200 synthetic integrated spectra; writes lam4_k2.jsonl/.out/.json)"""
import os, sys, json, signal, glob
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util, ppxf.sps_util as lib
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "_external_data")
SUMS = os.path.join(EXT, "lam4_integrated_2026_11_03"); TPL = os.path.join(EXT, "lam2_templates_2026_11_03", "spectra_emiles_9.0.npz")
C = 299792.458; VELSCALE = C * np.log(10) * 1e-4; LO, HI, FT = 3900.0, 6800.0, 2.51; SEED = 20261103
stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term)

def prep(fn):
    d = np.load(fn); z = float(d["z"]); lam = d["wave"].astype(float) / (1 + z); fw = 2.355 * d["lsf_sigma"].astype(float) / (1 + z)
    ok_res = (lam >= LO) & (fw >= FT); start = lam[np.flatnonzero(ok_res)[0]]
    s = (lam >= start) & (lam < HI); lam = lam[s]; fw = fw[s]
    flux, var, bad = d["flux"][s].astype(float), d["var"][s].astype(float), d["bad"][s]
    med = np.median(flux[~bad]); flux = flux / med; noise = np.where(~bad & (var > 0), np.sqrt(np.clip(var, 1e-30, None)) / med, 1e10)
    sps = lib.sps_lib(TPL, VELSCALE, fwhm_gal={"lam": lam, "fwhm": fw}, norm_range=[5070, 5950], lam_range=[3500, 7300])
    temps = sps.templates.reshape(sps.templates.shape[0], -1)
    good = util.determine_goodpixels(np.log(lam), np.exp(sps.ln_lam_temp[[0, -1]]), 0)
    obs = lam * (1 + z); sky = (np.abs(obs - 5577.3) < 5) | (np.abs(obs - 6300.3) < 5)
    keep = np.zeros(len(lam), bool); keep[good] = True; keep &= ~bad & np.isfinite(flux) & (noise < 1e9) & ~sky
    return dict(flux=flux, noise=noise, lam=lam, temps=temps, lam_temp=sps.lam_temp, good=np.flatnonzero(keep), start=float(start))

def run(p, flux, temps=None, start=None, fixed=None, degree=8, moments=6):
    return ppxf(p["temps"] if temps is None else temps, flux, p["noise"], VELSCALE, start or [0.0, 200.0], goodpixels=p["good"],
                moments=moments, degree=degree, mdegree=0, lam=p["lam"], lam_temp=p["lam_temp"], quiet=True, fixed=fixed)

def fit_all():
    out = os.path.join(HERE, "lam4_fit.jsonl"); done = {json.loads(l)["plateifu"] for l in open(out)} if os.path.exists(out) else set()
    with open(out, "a") as fo:
        for fn in sorted(glob.glob(os.path.join(SUMS, "*.npz"))):
            if stop: print("SIGTERM: stopping cleanly", flush=True); break
            pifu = os.path.basename(fn)[:-4]
            if pifu in done: continue
            try:
                p = prep(fn); pp = run(p, p["flux"]); e = pp.error * np.sqrt(pp.chi2)
                r = dict(status="ok", V=pp.sol[0], sigma=pp.sol[1], h3=pp.sol[2], h4=pp.sol[3], h5=pp.sol[4], h6=pp.sol[5], eV=e[0], esigma=e[1],
                         eh4=e[3], eh6=e[5], chi2=float(pp.chi2), ngood=int(len(p["good"])), start=p["start"],
                         sn=float(np.median(p["flux"][p["good"]] / p["noise"][p["good"]])))
            except Exception as ex: r = dict(status=f"error: {ex}")
            r["plateifu"] = pifu; fo.write(json.dumps(r, default=float) + "\n"); fo.flush()

def k2():
    """As LAM2's K2, 200 synthetics over the integrated sample."""
    out = os.path.join(HERE, "lam4_k2.jsonl"); files = sorted(glob.glob(os.path.join(SUMS, "*.npz")))
    F = {json.loads(l)["plateifu"]: json.loads(l) for l in open(os.path.join(HERE, "lam4_fit.jsonl"))}
    sig = np.array([v["sigma"] for v in F.values() if v["status"] == "ok"]); rng = np.random.default_rng(SEED)
    plan = [(i, files[int(rng.integers(len(files)))], float(rng.choice(sig)), float(rng.uniform(-0.10, 0.10)), int(rng.integers(2**31))) for i in range(200)]
    done = {json.loads(l)["i"] for l in open(out)} if os.path.exists(out) else set()
    with open(out, "a") as fo:
        for i, fn, s, h4, ns in plan:
            if stop: break
            if i in done: continue
            r = dict(i=i, plateifu=os.path.basename(fn)[:-4], sigma_in=s, h4_in=h4)
            try:
                p = prep(fn); pp = run(p, p["flux"]); tpl = p["temps"] @ pp.weights
                mod = run(p, p["flux"], temps=tpl[:, None], start=[0.0, s, 0.0, h4, 0.0, 0.0], fixed=[1] * 6, degree=-1).bestfit
                mod = mod / np.median(mod[p["good"]])
                syn = mod + np.random.default_rng(ns).normal(0, 1, mod.size) * np.where(p["noise"] < 1e9, p["noise"], 0)
                q = run(p, syn); r.update(status="ok", h4_out=float(q.sol[3]), sigma_out=float(q.sol[1]))
            except Exception as ex: r["status"] = f"error: {ex}"
            fo.write(json.dumps(r) + "\n"); fo.flush()
    rows = [json.loads(l) for l in open(out)]; ok = [x for x in rows if x["status"] == "ok"]
    if len(rows) == 200:
        d = np.array([x["h4_out"] - x["h4_in"] for x in ok]); rms = float(np.sqrt(np.mean(d**2)))
        txt = (f"K2: {len(ok)} of 200 ok; recovered h4 rms {rms:.4f} (<= 0.03): {'PASS' if rms <= 0.03 else 'FAIL -> h4 NOT MEASURABLE'}; "
               f"bias {np.mean(d):+.4f}; slope {np.polyfit([x['h4_in'] for x in ok], [x['h4_out'] for x in ok], 1)[0]:.3f}")
        print(txt); open(os.path.join(HERE, "lam4_k2.out"), "w").write(txt + "\n")
        json.dump(dict(rms=rms, pass_=bool(rms <= 0.03), n_ok=len(ok)), open(os.path.join(HERE, "lam4_k2.json"), "w"), indent=1)

if __name__ == "__main__":
    k2() if "--k2" in sys.argv else fit_all()
