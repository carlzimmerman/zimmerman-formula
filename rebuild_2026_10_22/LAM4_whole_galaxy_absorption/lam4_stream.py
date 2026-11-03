"""LAM4: draw the sample, then stream DR17 LOGCUBEs, sum each inside the half-light ellipse, save the integrated spectrum,
delete the cube (criteria 1023fbaae9). Resumable: galaxies with a saved sum are skipped. Each worker is single thread.
Run: python3 -I lam4_stream.py [NWORKERS] [--test CUBE.fits.gz PLATEIFU]"""
import os, sys, math, json, time, subprocess
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); EXT = os.path.join(ROOT, "_external_data")
L2 = os.path.join(os.path.dirname(HERE), "LAM2_gas_poor_lambda_estimator")
OUTD = os.path.join(EXT, "lam4_integrated_2026_11_03"); TMP = os.path.join(EXT, "lam4_cube_tmp"); os.makedirs(OUTD, exist_ok=True); os.makedirs(TMP, exist_ok=True)
SEED = 20261103; LO, HI = 3900.0, 6800.0
DP = os.path.join(EXT, "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits")

def draw():
    """All slow + 604 random fast from LAM2's gas-poor graded set; random download order. Written once."""
    fn = os.path.join(HERE, "lam4_sample.csv")
    if os.path.exists(fn): return [l.strip().split(",") for l in open(fn).readlines()[1:]]
    sys_argv = sys.argv; sys.argv = ["lam2_grade.py"]
    src = open(os.path.join(L2, "lam2_grade.py")).read().split("# ---- K1")[0]
    G = {"__file__": os.path.join(L2, "lam2_grade.py"), "__name__": "lam2"}; exec(compile(src, "lam2_grade.py", "exec"), G); sys.argv = sys_argv
    sel = np.flatnonzero(G["finite"](G["B"] + G["POP"] + G["SH"], G["poor"] & G["fitok"]))
    sl = sel[G["slow"][sel]]; fa = sel[~G["slow"][sel]]; rng = np.random.default_rng(SEED)
    pick = np.r_[sl, rng.choice(fa, 604, replace=False)]; pick = pick[rng.permutation(len(pick))]
    dp = fits.open(DP)[1].data; rows = []
    with open(fn, "w") as fo:
        fo.write("order,lam2_index,dynpop_row,plateifu,slow\n")
        for o, i in enumerate(pick):
            r = int(G["row"][i]); rows.append([str(o), str(i), str(r), dp["plateifu"][r].strip(), str(int(G["slow"][i]))])
            fo.write(",".join(rows[-1]) + "\n")
    return rows

def integrate(cube, r):
    dp = fits.open(DP)[1].data; z = float(dp["z"][r]); re = float(dp["Re_arcsec_MGE"][r]); eps = float(dp["Eps_MGE"][r]); pa = float(dp["PA_phot"][r])
    h = fits.open(cube); w = h["WAVE"].data.astype(float); hdr = h["FLUX"].header
    ra0, de0 = h[0].header["OBJRA"], h[0].header["OBJDEC"]
    ny, nx = hdr["NAXIS2"], hdr["NAXIS1"]; yy, xx = np.mgrid[0:ny, 0:nx]
    sky = WCS(hdr).celestial.pixel_to_world_values(xx, yy)
    xE = (sky[0] - ra0) * math.cos(math.radians(de0)) * 3600; yN = (sky[1] - de0) * 3600
    a, b = re / math.sqrt(1 - eps), re * math.sqrt(1 - eps); p = math.radians(pa)
    u = xE * math.sin(p) + yN * math.cos(p); v = xE * math.cos(p) - yN * math.sin(p)
    inside = (u / a)**2 + (v / b)**2 <= 1
    win = (w / (1 + z) > LO) & (w / (1 + z) < HI)
    flux = h["FLUX"].data; ivar = h["IVAR"].data; mask = h["MASK"].data
    good = (mask == 0) & (ivar > 0)
    use = inside & (good[win].mean(axis=0) >= 0.80); N = int(use.sum())
    if N == 0: return None, dict(n_inside=int(inside.sum()), n_used=0)
    f = flux[:, use].astype(float); iv = ivar[:, use].astype(float); g = good[:, use]
    lsf = h["LSFPOST"].data[:, use].astype(float)
    med = np.array([np.median(f[win, k][g[win, k]]) for k in range(N)]); med = np.clip(med, 0, None)
    F = np.where(g, f, 0).sum(axis=1); V = np.where(g, 1 / np.where(g, iv, 1), 0).sum(axis=1)
    miss = ((~g) * med[None, :]).sum(axis=1) / max(med.sum(), 1e-30)
    wts = np.where(g, np.clip(f, 0, None), 0); LS = (wts * lsf).sum(axis=1) / np.clip(wts.sum(axis=1), 1e-30, None)
    corr = (1 + 1.62 * math.log10(min(N, 100)))**2
    bad = (miss > 0.05) | (V <= 0) | ~np.isfinite(F)
    return dict(wave=w.astype(np.float32), flux=F.astype(np.float32), var=(V * corr).astype(np.float32), bad=bad,
                lsf_sigma=LS.astype(np.float32), z=np.float32(z)), dict(n_inside=int(inside.sum()), n_used=N, corr=corr, frac_bad=float(bad[win].mean()))

def work(row):
    o, _, r, pifu, _ = row; out = os.path.join(OUTD, f"{pifu}.npz")
    if os.path.exists(out): return pifu, "done"
    pl = pifu.split("-")[0]; url = f"https://data.sdss.org/sas/dr17/manga/spectro/redux/v3_1_1/{pl}/stack/manga-{pifu}-LOGCUBE.fits.gz"
    cube = os.path.join(TMP, f"manga-{pifu}-LOGCUBE.fits.gz")
    for t in range(8):
        rc = subprocess.run(["curl", "-s", "-f", "-C", "-", "-m", "1800", "-o", cube, url]).returncode
        if rc in (0, 33) and os.path.exists(cube):
            try: fits.open(cube)["WAVE"].data; break
            except Exception: os.remove(cube)
        time.sleep(15)
    else: return pifu, "download failed"
    try:
        s, info = integrate(cube, int(r))
        if s is None: status = f"no spaxels {info}"
        else: np.savez(out + ".part.npz", **s, info=json.dumps(info)); os.replace(out + ".part.npz", out); status = "ok"
    except Exception as e: status = f"error {e}"
    os.remove(cube); return pifu, status

if __name__ == "__main__":
    if "--test" in sys.argv:
        i = sys.argv.index("--test"); cube, pifu = sys.argv[i + 1], sys.argv[i + 2]
        dp = fits.open(DP)[1].data; r = int(np.flatnonzero(np.char.strip(dp["plateifu"]) == pifu)[0])
        s, info = integrate(cube, r); print(pifu, info, {k: (v.shape if hasattr(v, "shape") else v) for k, v in s.items()}); sys.exit()
    rows = draw(); n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print(f"sample {len(rows)}, slow {sum(int(x[4]) for x in rows)}; workers {n}", flush=True)
    from concurrent.futures import ProcessPoolExecutor
    log = open(os.path.join(HERE, "lam4_stream.log"), "a")
    with ProcessPoolExecutor(n) as ex:
        for k, (pifu, st) in enumerate(ex.map(work, rows)):
            log.write(f"{pifu},{st}\n"); log.flush()
            if (k + 1) % 25 == 0: print(k + 1, "processed", flush=True)
    print("done", flush=True)
