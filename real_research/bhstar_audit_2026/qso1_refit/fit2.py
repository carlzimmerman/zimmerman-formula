"""Core fits (model2) for each law on the DATA; then real-noise calibration of Delta chi^2 (kepler - framework).
Usage: python3 fit2.py data            -> fits2_data.json
       python3 fit2.py calib <truth> <n> -> calib2_<truth>.json   (truth = kepler_canonical | framework_canonical)"""
import numpy as np, json, sys, time, os
from multiprocessing import Pool
from scipy.optimize import minimize
from model import load
from model2 import BOUNDS, NAMES, f, chi2, disk_cube, outflow_cube, mask_for

D0 = load()
MSK = mask_for(D0["data"].shape[1:])
LAWS = [("kepler", "canonical"), ("framework", "canonical"), ("framework", "alt"), ("rival", "canonical"),
        ("rival", "alt")]


def polish(law, footing, D, st, fev=5000):
    r = minimize(f, st, args=(law, footing, D, MSK), method="Powell", bounds=BOUNDS,
                 options={"maxfev": fev, "xtol": 1e-4, "ftol": 1e-8})
    r2 = minimize(f, r.x, args=(law, footing, D, MSK), method="Nelder-Mead",
                  options={"maxfev": 3000, "xatol": 1e-4, "fatol": 1e-4})
    return (r2 if r2.fun < r.fun else r)


def rstart(rng):
    return [rng.uniform(6.8, 8.3), rng.uniform(max(0.3, BOUNDS[1][0]), min(0.9, BOUNDS[1][1])), rng.uniform(0, np.pi), rng.uniform(19, 21),
            rng.uniform(18, 20), rng.uniform(-40, 10), rng.uniform(5, 50), rng.uniform(10, 150), rng.uniform(0.7, 3),
            rng.uniform(0, np.pi), rng.uniform(2.6, 5.5), rng.uniform(max(0.1, BOUNDS[11][0] + 0.005), 0.28), rng.uniform(-100, 0),
            rng.uniform(60, 200)]


def job_data(args):
    law, footing, seed = args
    rng = np.random.default_rng(seed)
    r = polish(law, footing, D0, rstart(rng))
    return law, footing, float(r.fun), list(map(float, r.x))


def job_seed(args):
    law, footing, x = args
    r = polish(law, footing, D0, x)
    return law, footing, float(r.fun), list(map(float, r.x))


def job_calib(args):
    truth, k, fits = args
    import noise as calib
    lt, ft = truth.split("_")
    pt = fits[truth]["x"]
    sh = D0["data"].shape[1:]
    _, a = chi2(pt, lt, ft, D0, MSK)
    sim = a[0] * disk_cube(pt, lt, ft, sh, D0["v"], D0["dv"]) + a[1] * outflow_cube(pt, sh, D0["v"], D0["dv"])
    D = dict(D0); D["data"] = sim + calib.noise_block(k)
    out = {"k": k}
    laws = [tuple(x.split("_")) for x in os.environ.get("CALIB_LAWS", "kepler_canonical,framework_canonical").split(",")]
    starts = [fits[f"{l}_{f}"]["x"] for l, f in laws] + [pt]
    for law, foot in laws:
        best = None
        for st in starts:
            r = polish(law, foot, D, st, fev=3000)
            if best is None or r.fun < best.fun:
                best = r
        out[f"chi2_{law}_{foot}"] = float(best.fun); out[f"logM_{law}_{foot}"] = float(best.x[0])
        if foot == "canonical":
            out[f"chi2_{law}"] = float(best.fun); out[f"logM_{law}"] = float(best.x[0])
    out["dchi2"] = out["chi2_kepler"] - out.get("chi2_framework", out["chi2_kepler"])
    if "chi2_rival" in out:
        out["dchi2_rival"] = out["chi2_kepler"] - out["chi2_rival"]
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    t = time.time()
    if mode == "data":
        jobs = [(law, ft, s) for law, ft in LAWS for s in range(int(os.environ.get("NSTARTS", "24")))]
        with Pool(8) as pool:
            res = pool.map(job_data, jobs)
            # CROSS-SEEDING: polish every law from every law's best solution (removes spurious gaps from stuck searches)
            best0 = {}
            for law, ft in LAWS:
                rs = sorted([r for r in res if r[0] == law and r[1] == ft], key=lambda r: r[2])
                best0[(law, ft)] = rs[0][3]
            xjobs = [(law, ft, x) for law, ft in LAWS for x in best0.values()]
            xres = pool.map(job_seed, xjobs)
            res = res + xres
        out = {}
        for law, ft in LAWS:
            rs = sorted([r for r in res if r[0] == law and r[1] == ft], key=lambda r: r[2])
            out[f"{law}_{ft}"] = {"chi2": rs[0][2], "x": rs[0][3], "next": [r[2] for r in rs[1:4]]}
            print(f"{law+'_'+ft:22s} chi2 = {rs[0][2]:.2f}  next {[round(r[2],2) for r in rs[1:4]]}  " +
                  " ".join(f"{n}={v:.3f}" for n, v in zip(NAMES, rs[0][3])), flush=True)
        json.dump(out, open(os.environ.get("FITS_OUT", "fits2_data.json"), "w"), indent=1)
    else:
        truth, n = sys.argv[2], int(sys.argv[3])
        fits = json.load(open(os.environ.get("CALIB_FITS", "fits2_data.json")))
        with Pool(8) as pool:
            res = pool.map(job_calib, [(truth, k, fits) for k in range(n)])
        json.dump(res, open(f"calib2_{truth}{os.environ.get('CALIB_SUFFIX', '')}.json", "w"), indent=1)
        d = np.array([r["dchi2"] for r in res])
        print(truth, f"Delta chi2 (kepler - framework): mean {d.mean():.2f} sd {d.std():.2f} min {d.min():.2f} max {d.max():.2f}")
    print(f"t = {time.time()-t:.0f}s")
